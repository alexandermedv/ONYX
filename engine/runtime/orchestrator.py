from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping

from contracts.ids import generation_result_id, stable_id
from contracts.job_spec import dumps_job_spec
from contracts.models import (
    MANIFEST_SCHEMA,
    SCHEMA_VERSION,
    ArtifactRecord,
    AttemptRecord,
    ErrorRecord,
    GenerationResult,
    JobSpec,
    Manifest,
    ProviderRef,
    QualityPlan,
    RuntimeStatus,
)
from contracts.persistence import load_manifest, save_manifest_atomic

from .execution_plan import ExecutionPlan, GenerationTask, MaterializedProvider
from .providers import ProviderArtifact, ProviderError, ProviderExecutionResult, SceneGenerator, SceneGeneratorRequest


class OrchestrationError(RuntimeError):
    """Raised when a canonical execution plan cannot be run safely."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def attempt_record_id(*, result_id: str, attempt_number: int) -> str:
    """Stable attempt ID dimensions: logical result ID plus 1-based attempt number."""
    if attempt_number < 1:
        raise ValueError("attempt_number must be positive")
    return stable_id("attempt", result_id=result_id, attempt_number=attempt_number)


def _job_spec_hash(job_spec: JobSpec) -> str:
    return hashlib.sha256(dumps_job_spec(job_spec).encode("utf-8")).hexdigest()


def _inside(path_value: str | Path, root_value: str | Path, label: str) -> Path:
    path = Path(path_value).resolve(strict=False)
    root = Path(root_value).resolve(strict=False)
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise OrchestrationError(f"{label} must be inside execution workspace: {path}") from exc
    return path


def _provider_ref(provider: MaterializedProvider) -> ProviderRef:
    return ProviderRef(
        provider_id=provider.provider_id,
        provider_kind=provider.provider_kind,
        implementation_version=provider.implementation_version,
        model_id=provider.model_id,
        model_version=provider.model_version,
        model_hash=provider.model_hash,
        workflow_id=provider.workflow_id,
        workflow_version=provider.workflow_version,
        workflow_uri=provider.workflow_uri,
        workflow_hash=provider.workflow_hash,
        identity_aware=provider.identity_aware,
        identity_mode=provider.identity_mode,
    )


def initialize_manifest(
    job_spec: JobSpec,
    execution_plan: ExecutionPlan,
    *,
    job_spec_uri: str | None = None,
) -> Manifest:
    if job_spec.job_id != execution_plan.job_id:
        raise OrchestrationError("JobSpec and ExecutionPlan job_id do not match")
    return Manifest(
        schema=MANIFEST_SCHEMA,
        schema_version=SCHEMA_VERSION,
        manifest_id=stable_id("manifest", job_id=job_spec.job_id),
        job_id=job_spec.job_id,
        revision=0,
        status=RuntimeStatus.PLANNED,
        created_at=utc_now(),
        updated_at=utc_now(),
        job_spec_uri=job_spec_uri,
        job_spec_hash=_job_spec_hash(job_spec),
        quality_plan=QualityPlan.from_dict(job_spec.quality_plan.to_dict()),
        resolved_runtime=execution_plan.resolved_runtime_snapshot(),
    )


@dataclass
class ManifestWriter:
    path: Path
    manifest: Manifest

    def __post_init__(self) -> None:
        self.path = self.path.resolve(strict=False)
        self._last_revision = self.manifest.revision

    def persist(self) -> None:
        if self.manifest.revision != self._last_revision:
            raise OrchestrationError(
                "Manifest revision changed outside the single writer "
                f"(expected {self._last_revision}, got {self.manifest.revision})"
            )
        previous_updated_at = self.manifest.updated_at
        self.manifest.revision = self._last_revision + 1
        self.manifest.updated_at = utc_now()
        try:
            save_manifest_atomic(self.path, self.manifest)
        except Exception:
            self.manifest.revision = self._last_revision
            self.manifest.updated_at = previous_updated_at
            raise
        self._last_revision = self.manifest.revision


def _result_for_task(manifest: Manifest, task: GenerationTask) -> GenerationResult | None:
    result_id = generation_result_id(
        job_id=manifest.job_id,
        scene_id=task.scene_id,
        provider_id=task.provider_id,
        candidate_index=task.candidate_index,
    )
    return next((item for item in manifest.generation_results if item.result_id == result_id), None)


def _artifact_is_resumable(manifest: Manifest, result: GenerationResult) -> bool:
    artifact_ids = result.outputs.get("artifact_ids", [])
    if not isinstance(artifact_ids, list) or not artifact_ids:
        return False
    records = {item.artifact_id: item for item in manifest.artifacts}
    for artifact_id in artifact_ids:
        record = records.get(artifact_id)
        if record is None or not record.resolved_path or not Path(record.resolved_path).is_file():
            return False
    return True


def _canonical_error(error: ProviderError, attempt_id: str) -> ErrorRecord:
    return ErrorRecord(
        code=error.code,
        category=error.category,
        message=error.message,
        retryable=error.retryable,
        attempt_id=attempt_id,
    )


def _exception_error(exc: Exception, attempt_id: str) -> ErrorRecord:
    return ErrorRecord(
        code="PROVIDER_EXCEPTION",
        category="provider_exception",
        message=str(exc) or type(exc).__name__,
        retryable=False,
        details={"exception_type": type(exc).__name__},
        attempt_id=attempt_id,
    )


def _artifact_uri(plan: ExecutionPlan, resolved_path: Path) -> str:
    workspace = Path(plan.workspace_path).resolve(strict=False)
    relative = resolved_path.relative_to(workspace).as_posix()
    return f"{plan.workspace_uri.rstrip('/')}/{relative}"


def _record_artifacts(
    manifest: Manifest,
    plan: ExecutionPlan,
    task: GenerationTask,
    result: GenerationResult,
    attempt: AttemptRecord,
    artifacts: tuple[ProviderArtifact, ...],
) -> list[str]:
    if not artifacts:
        raise OrchestrationError("Successful provider execution produced no artifacts")
    task_root = Path(task.output_path).resolve(strict=False)
    workspace_root = Path(plan.workspace_path).resolve(strict=False)
    artifact_ids: list[str] = []
    for index, produced in enumerate(artifacts):
        path = _inside(produced.resolved_path, task_root, "Provider artifact")
        _inside(path, workspace_root, "Provider artifact")
        if not path.is_file():
            raise OrchestrationError(f"Provider artifact does not exist: {path}")
        payload = path.read_bytes()
        artifact_id = stable_id(
            "artifact",
            result_id=result.result_id,
            attempt_number=attempt.attempt_number,
            artifact_index=index,
        )
        manifest.artifacts.append(
            ArtifactRecord(
                artifact_id=artifact_id,
                kind=produced.kind,
                role=produced.role,
                uri=_artifact_uri(plan, path),
                created_by_id=result.result_id,
                sha256=hashlib.sha256(payload).hexdigest(),
                mime_type=produced.mime_type,
                size_bytes=len(payload),
                resolved_path=str(path),
            )
        )
        artifact_ids.append(artifact_id)
    return artifact_ids


def _mark_stale_attempts(manifest: Manifest, result: GenerationResult, now: str) -> None:
    attempts = {item.attempt_id: item for item in manifest.attempts}
    for attempt_id in result.attempt_ids:
        attempt = attempts.get(attempt_id)
        if attempt and attempt.status == RuntimeStatus.RUNNING:
            error = ErrorRecord(
                code="INTERRUPTED_ATTEMPT",
                category="orchestration",
                message="Attempt was still running when execution resumed",
                retryable=True,
                attempt_id=attempt.attempt_id,
            )
            attempt.status = RuntimeStatus.FAILED
            attempt.finished_at = now
            attempt.error = error


def _next_attempt_number(manifest: Manifest, result_id: str) -> int:
    numbers = [item.attempt_number for item in manifest.attempts if item.result_id == result_id]
    return max(numbers, default=0) + 1


def _start_attempt(
    writer: ManifestWriter,
    task: GenerationTask,
    provider: MaterializedProvider,
) -> tuple[GenerationResult, AttemptRecord]:
    manifest = writer.manifest
    result_id = generation_result_id(
        job_id=manifest.job_id,
        scene_id=task.scene_id,
        provider_id=task.provider_id,
        candidate_index=task.candidate_index,
    )
    result = _result_for_task(manifest, task)
    now = utc_now()
    if result is None:
        result = GenerationResult(
            result_id=result_id,
            scene_id=task.scene_id,
            candidate_index=task.candidate_index,
            status=RuntimeStatus.PLANNED,
            provider=_provider_ref(provider),
            inputs={
                "seed": task.seed,
                "scene_inputs": json.loads(task.scene_inputs_json),
                "provider_parameters": json.loads(task.provider_parameters_json),
                "intended_output_path": task.output_path,
            },
            idempotency_key=result_id,
        )
        manifest.generation_results.append(result)
    _mark_stale_attempts(manifest, result, now)
    attempt_number = _next_attempt_number(manifest, result_id)
    attempt_id = attempt_record_id(result_id=result_id, attempt_number=attempt_number)
    attempt = AttemptRecord(
        attempt_id=attempt_id,
        result_id=result_id,
        attempt_number=attempt_number,
        status=RuntimeStatus.RUNNING,
        started_at=now,
        runtime={"provider_id": task.provider_id, "machine_id": writer.manifest.resolved_runtime.get("machine_id")},
    )
    manifest.attempts.append(attempt)
    result.attempt_ids.append(attempt_id)
    result.status = RuntimeStatus.RUNNING
    result.started_at = result.started_at or now
    result.finished_at = None
    result.error = None
    result.outputs = {}
    manifest.status = RuntimeStatus.RUNNING
    writer.persist()
    return result, attempt


def _provider_request(
    plan: ExecutionPlan,
    task: GenerationTask,
    provider: MaterializedProvider,
    result: GenerationResult,
) -> SceneGeneratorRequest:
    return SceneGeneratorRequest(
        generation_result_id=result.result_id,
        job_id=plan.job_id,
        scene_id=task.scene_id,
        provider_id=task.provider_id,
        candidate_index=task.candidate_index,
        seed=task.seed,
        output_path=task.output_path,
        scene_inputs_json=task.scene_inputs_json,
        provider_parameters_json=task.provider_parameters_json,
        provider=provider,
    )


def _finish_attempt(
    writer: ManifestWriter,
    plan: ExecutionPlan,
    task: GenerationTask,
    result: GenerationResult,
    attempt: AttemptRecord,
    outcome: ProviderExecutionResult,
    started: float,
) -> bool:
    now = utc_now()
    duration_ms = max(0, round((time.monotonic() - started) * 1000))
    attempt.finished_at = now
    attempt.duration_ms = duration_ms
    attempt.runtime.update(json.loads(outcome.metadata_json))
    result.finished_at = now
    result.duration_ms = duration_ms
    if outcome.succeeded:
        try:
            artifact_ids = _record_artifacts(
                writer.manifest, plan, task, result, attempt, outcome.artifacts
            )
        except Exception as exc:
            error = _exception_error(exc, attempt.attempt_id)
            attempt.status = RuntimeStatus.FAILED
            attempt.error = error
            result.status = RuntimeStatus.FAILED
            result.error = error
            result.outputs = {}
            writer.persist()
            return False
        attempt.status = RuntimeStatus.SUCCEEDED
        attempt.error = None
        result.status = RuntimeStatus.SUCCEEDED
        result.error = None
        result.outputs = {"artifact_ids": artifact_ids}
        writer.persist()
        return True

    provider_error = outcome.error or ProviderError(
        "PROVIDER_FAILED", "provider_execution", "Provider returned failure without error"
    )
    error = _canonical_error(provider_error, attempt.attempt_id)
    attempt.status = RuntimeStatus.FAILED
    attempt.error = error
    result.status = RuntimeStatus.FAILED
    result.error = error
    result.outputs = {}
    writer.persist()
    return False


def run_generation_plan(
    job_spec: JobSpec,
    execution_plan: ExecutionPlan,
    manifest_path: Path,
    providers: Mapping[str, SceneGenerator],
    *,
    resume: bool = True,
    max_attempts_per_task: int = 1,
    job_spec_uri: str | None = None,
) -> Manifest:
    if max_attempts_per_task < 1:
        raise ValueError("max_attempts_per_task must be positive")
    manifest_path = _inside(manifest_path, execution_plan.workspace_path, "Manifest path")
    materialized = {item.provider_id: item for item in execution_plan.providers}
    for task in execution_plan.generation_tasks:
        provider = materialized.get(task.provider_id)
        if provider is None:
            raise OrchestrationError(f"ExecutionPlan has no materialized provider {task.provider_id}")
        if provider.identity_aware:
            raise OrchestrationError(
                f"Identity-aware provider {task.provider_id} requires native identity lifecycle, "
                "which is outside Phase 1B.2"
            )

    if manifest_path.exists():
        if not resume:
            raise OrchestrationError(f"Manifest already exists: {manifest_path}")
        manifest = load_manifest(manifest_path)
        if manifest.job_id != job_spec.job_id or manifest.job_spec_hash != _job_spec_hash(job_spec):
            raise OrchestrationError("Existing Manifest does not match JobSpec")
        if manifest.resolved_runtime != execution_plan.resolved_runtime_snapshot():
            raise OrchestrationError("Existing Manifest does not match ExecutionPlan runtime snapshot")
    else:
        manifest = initialize_manifest(job_spec, execution_plan, job_spec_uri=job_spec_uri)

    writer = ManifestWriter(manifest_path, manifest)
    if not manifest_path.exists():
        writer.persist()

    stop_on_error = not job_spec.continue_independent_failures
    for task in execution_plan.generation_tasks:
        existing = _result_for_task(manifest, task)
        if existing and existing.status == RuntimeStatus.SUCCEEDED and _artifact_is_resumable(manifest, existing):
            continue
        materialized_provider = materialized[task.provider_id]
        implementation = providers.get(task.provider_id)
        task_succeeded = False
        for _ in range(max_attempts_per_task):
            result, attempt = _start_attempt(writer, task, materialized_provider)
            request = _provider_request(execution_plan, task, materialized_provider, result)
            started = time.monotonic()
            try:
                if implementation is None:
                    outcome = ProviderExecutionResult.failure(
                        "PROVIDER_NOT_REGISTERED",
                        "orchestration",
                        f"No SceneGenerator implementation registered for {task.provider_id}",
                    )
                else:
                    outcome = implementation.execute(request)
                if not isinstance(outcome, ProviderExecutionResult):
                    raise TypeError("SceneGenerator returned an invalid execution result")
            except Exception as exc:
                outcome = ProviderExecutionResult(
                    succeeded=False,
                    error=ProviderError(
                        "PROVIDER_EXCEPTION",
                        "provider_exception",
                        str(exc) or type(exc).__name__,
                        False,
                    ),
                    metadata_json=json.dumps({"exception_type": type(exc).__name__}),
                )
            task_succeeded = _finish_attempt(
                writer, execution_plan, task, result, attempt, outcome, started
            )
            if task_succeeded:
                break
        if not task_succeeded and stop_on_error:
            break

    task_results = [_result_for_task(manifest, task) for task in execution_plan.generation_tasks]
    final_status = (
        RuntimeStatus.SUCCEEDED
        if task_results and all(item and item.status == RuntimeStatus.SUCCEEDED for item in task_results)
        else RuntimeStatus.FAILED
    )
    if manifest.status != final_status:
        manifest.status = final_status
        writer.persist()
    return manifest
