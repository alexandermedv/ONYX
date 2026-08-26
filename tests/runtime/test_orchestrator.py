from __future__ import annotations

import json
import sys
import tempfile
import unittest
from dataclasses import fields
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "engine"))

import runtime.orchestrator as orchestrator_module
from contracts.ids import generation_result_id
from contracts.models import (
    JOB_SPEC_SCHEMA,
    SCHEMA_VERSION,
    JobSpec,
    ProviderRef,
    QualityPlan,
    RuntimeStatus,
    SceneGeneratorConfig,
    SceneSpec,
)
from contracts.persistence import load_manifest
from contracts.validation import validate_manifest
from runtime import (
    FakeSceneGenerator,
    ProviderRuntimeConfig,
    RuntimeConfig,
    SceneGeneratorRequest,
    initialize_manifest,
    materialize_job,
    run_generation_plan,
)


def make_job(*, scenes: int = 1, candidates: int = 1, continue_failures: bool = True) -> JobSpec:
    return JobSpec(
        schema=JOB_SPEC_SCHEMA,
        schema_version=SCHEMA_VERSION,
        job_id="job_orchestrator",
        client_id="fixture-client",
        service_tier="mass",
        base_seed=98765,
        scenes=[
            SceneSpec(
                scene_id=f"scene_{index:03d}",
                subject="adult portrait subject",
                prompt={"lighting": "soft daylight"},
            )
            for index in range(1, scenes + 1)
        ],
        scene_generators=[
            SceneGeneratorConfig(
                provider=ProviderRef(
                    provider_id="scene.fake",
                    provider_kind="scene_generator",
                    implementation_version="fake-v1",
                    workflow_id="fake-workflow",
                    workflow_version="1.0",
                    workflow_uri="repo://workflows/fake.json",
                ),
                candidate_count_per_scene=candidates,
                parameters={"format": "json"},
            )
        ],
        quality_plan=QualityPlan(human_review_required=True),
        workspace_uri="workspace://jobs/job_orchestrator",
        continue_independent_failures=continue_failures,
    )


def make_runtime(root: Path) -> RuntimeConfig:
    return RuntimeConfig(
        schema="onyx.runtime_config",
        schema_version="1.0",
        machine_id="cpu-test-machine",
        repo_root=str(root / "repo"),
        workspace_root=str(root / "workspace"),
        client_root=str(root / "clients"),
        providers={
            "scene.fake": ProviderRuntimeConfig(capabilities=("cpu_fake",)),
        },
    )


def context(root: Path, **job_options):
    job = make_job(**job_options)
    plan = materialize_job(job, make_runtime(root))
    path = Path(plan.workspace_path) / "manifest.json"
    return job, plan, path


class CrashProvider:
    def execute(self, request: SceneGeneratorRequest):
        raise KeyboardInterrupt("simulated process death")


class ManifestAwareProbe:
    def __init__(self, manifest_path: Path) -> None:
        self.manifest_path = manifest_path
        self.saw_running_attempt = False

    def execute(self, request: SceneGeneratorRequest):
        manifest = load_manifest(self.manifest_path)
        self.saw_running_attempt = (
            manifest.generation_results[0].status == RuntimeStatus.RUNNING
            and manifest.attempts[0].status == RuntimeStatus.RUNNING
        )
        return FakeSceneGenerator().execute(request)


class ManifestInitializationTests(unittest.TestCase):
    def test_manifest_initialization_from_execution_plan(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            job, plan, _ = context(Path(folder))
            manifest = initialize_manifest(job, plan, job_spec_uri="repo://jobs/job.json")
            self.assertEqual(0, manifest.revision)
            self.assertEqual(RuntimeStatus.PLANNED, manifest.status)
            self.assertEqual("repo://jobs/job.json", manifest.job_spec_uri)
            self.assertEqual(64, len(manifest.job_spec_hash or ""))
            self.assertEqual(job.quality_plan, manifest.quality_plan)
            validate_manifest(manifest)

    def test_resolved_runtime_is_copied(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            job, plan, _ = context(Path(folder))
            self.assertEqual(
                plan.resolved_runtime_snapshot(),
                initialize_manifest(job, plan).resolved_runtime,
            )

    def test_generation_result_id_is_deterministic(self) -> None:
        expected = generation_result_id(
            job_id="job_orchestrator",
            scene_id="scene_001",
            provider_id="scene.fake",
            candidate_index=0,
        )
        with tempfile.TemporaryDirectory() as folder:
            job, plan, path = context(Path(folder))
            manifest = run_generation_plan(
                job, plan, path, {"scene.fake": FakeSceneGenerator()}
            )
            self.assertEqual(expected, manifest.generation_results[0].result_id)

    def test_provider_result_cannot_supply_canonical_id(self) -> None:
        request_fields = {item.name for item in fields(SceneGeneratorRequest)}
        self.assertIn("generation_result_id", request_fields)
        from runtime.providers import ProviderExecutionResult

        result_fields = {item.name for item in fields(ProviderExecutionResult)}
        self.assertNotIn("generation_result_id", result_fields)
        self.assertNotIn("result_id", result_fields)


class GenerationLifecycleTests(unittest.TestCase):
    def test_first_success_registers_and_links_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            job, plan, path = context(Path(folder))
            manifest = run_generation_plan(
                job, plan, path, {"scene.fake": FakeSceneGenerator()}
            )
            result = manifest.generation_results[0]
            self.assertEqual(RuntimeStatus.SUCCEEDED, result.status)
            self.assertEqual(RuntimeStatus.SUCCEEDED, manifest.attempts[0].status)
            artifact_id = result.outputs["artifact_ids"][0]
            artifact = next(item for item in manifest.artifacts if item.artifact_id == artifact_id)
            self.assertEqual(result.result_id, artifact.created_by_id)
            self.assertTrue(Path(artifact.resolved_path or "").is_file())
            self.assertTrue(artifact.sha256)
            self.assertGreater(artifact.size_bytes or 0, 0)
            validate_manifest(manifest)

    def test_failed_execution_records_result_and_attempt_error(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            job, plan, path = context(Path(folder))
            manifest = run_generation_plan(
                job, plan, path, {"scene.fake": FakeSceneGenerator(fail=True)}
            )
            result = manifest.generation_results[0]
            attempt = manifest.attempts[0]
            self.assertEqual(RuntimeStatus.FAILED, result.status)
            self.assertEqual(RuntimeStatus.FAILED, attempt.status)
            self.assertEqual("FAKE_GENERATION_FAILED", result.error.code)
            self.assertEqual(attempt.attempt_id, result.error.attempt_id)
            validate_manifest(manifest)

    def test_sibling_continues_after_failure(self) -> None:
        class FirstFails:
            def __init__(self) -> None:
                self.calls = 0
                self.delegate = FakeSceneGenerator()

            def execute(self, request):
                self.calls += 1
                if self.calls == 1:
                    from runtime import ProviderExecutionResult
                    return ProviderExecutionResult.failure("FIRST_FAILED", "provider_execution", "first failed")
                return self.delegate.execute(request)

        with tempfile.TemporaryDirectory() as folder:
            job, plan, path = context(Path(folder), scenes=2)
            provider = FirstFails()
            manifest = run_generation_plan(job, plan, path, {"scene.fake": provider})
            self.assertEqual(2, provider.calls)
            self.assertEqual(
                [RuntimeStatus.FAILED, RuntimeStatus.SUCCEEDED],
                [item.status for item in manifest.generation_results],
            )
            self.assertEqual(RuntimeStatus.FAILED, manifest.status)

    def test_provider_exception_becomes_canonical_failure(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            job, plan, path = context(Path(folder))
            manifest = run_generation_plan(
                job,
                plan,
                path,
                {"scene.fake": FakeSceneGenerator(raise_exception=True)},
            )
            error = manifest.generation_results[0].error
            self.assertEqual("PROVIDER_EXCEPTION", error.code)
            self.assertEqual("provider_exception", error.category)
            self.assertNotIn("Traceback", error.message)

    def test_seed_reaches_provider_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            job, plan, path = context(Path(folder))
            provider = FakeSceneGenerator()
            run_generation_plan(job, plan, path, {"scene.fake": provider})
            self.assertEqual(plan.generation_tasks[0].seed, provider.requests[0].seed)

    def test_manifest_is_persisted_before_invocation(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            job, plan, path = context(Path(folder))
            probe = ManifestAwareProbe(path)
            run_generation_plan(job, plan, path, {"scene.fake": probe})
            self.assertTrue(probe.saw_running_attempt)

    def test_fake_provider_output_is_deterministic(self) -> None:
        payloads = []
        for _ in range(2):
            with tempfile.TemporaryDirectory() as folder:
                job, plan, path = context(Path(folder))
                manifest = run_generation_plan(
                    job, plan, path, {"scene.fake": FakeSceneGenerator()}
                )
                artifact = manifest.artifacts[0]
                payloads.append(Path(artifact.resolved_path or "").read_bytes())
        self.assertEqual(payloads[0], payloads[1])


class RetryAndResumeTests(unittest.TestCase):
    def test_fail_first_then_success_keeps_result_and_adds_attempt(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            job, plan, path = context(Path(folder))
            manifest = run_generation_plan(
                job,
                plan,
                path,
                {"scene.fake": FakeSceneGenerator(fail_first_n=1)},
                max_attempts_per_task=2,
            )
            self.assertEqual(1, len(manifest.generation_results))
            self.assertEqual(2, len(manifest.attempts))
            self.assertNotEqual(manifest.attempts[0].attempt_id, manifest.attempts[1].attempt_id)
            self.assertEqual(manifest.attempts[0].result_id, manifest.attempts[1].result_id)
            self.assertEqual(RuntimeStatus.SUCCEEDED, manifest.generation_results[0].status)

    def test_succeeded_existing_artifact_is_skipped_without_attempt(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            job, plan, path = context(Path(folder))
            first = FakeSceneGenerator()
            manifest = run_generation_plan(job, plan, path, {"scene.fake": first})
            revision = manifest.revision
            resumed = FakeSceneGenerator()
            manifest = run_generation_plan(job, plan, path, {"scene.fake": resumed})
            self.assertEqual(0, resumed.invocation_count)
            self.assertEqual(1, len(manifest.attempts))
            self.assertEqual(revision, manifest.revision)

    def test_failed_result_is_retried_with_same_result_id(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            job, plan, path = context(Path(folder))
            failed = run_generation_plan(
                job, plan, path, {"scene.fake": FakeSceneGenerator(fail=True)}
            )
            result_id = failed.generation_results[0].result_id
            resumed = run_generation_plan(
                job, plan, path, {"scene.fake": FakeSceneGenerator()}
            )
            self.assertEqual(result_id, resumed.generation_results[0].result_id)
            self.assertEqual(2, len(resumed.attempts))
            self.assertEqual(RuntimeStatus.SUCCEEDED, resumed.generation_results[0].status)

    def test_stale_running_attempt_is_preserved_and_retried(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            job, plan, path = context(Path(folder))
            with self.assertRaises(KeyboardInterrupt):
                run_generation_plan(job, plan, path, {"scene.fake": CrashProvider()})
            crashed = load_manifest(path)
            self.assertEqual(RuntimeStatus.RUNNING, crashed.attempts[0].status)
            resumed = run_generation_plan(
                job, plan, path, {"scene.fake": FakeSceneGenerator()}
            )
            self.assertEqual(2, len(resumed.attempts))
            self.assertEqual(RuntimeStatus.FAILED, resumed.attempts[0].status)
            self.assertEqual("INTERRUPTED_ATTEMPT", resumed.attempts[0].error.code)
            self.assertEqual(RuntimeStatus.SUCCEEDED, resumed.attempts[1].status)

    def test_missing_artifact_forces_retry_and_preserves_history(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            job, plan, path = context(Path(folder))
            first = run_generation_plan(
                job, plan, path, {"scene.fake": FakeSceneGenerator()}
            )
            old_attempt = first.attempts[0].attempt_id
            Path(first.artifacts[0].resolved_path or "").unlink()
            provider = FakeSceneGenerator()
            resumed = run_generation_plan(job, plan, path, {"scene.fake": provider})
            self.assertEqual(1, provider.invocation_count)
            self.assertEqual(2, len(resumed.attempts))
            self.assertEqual(old_attempt, resumed.attempts[0].attempt_id)
            self.assertEqual(2, len(resumed.artifacts))
            self.assertEqual(
                resumed.artifacts[1].artifact_id,
                resumed.generation_results[0].outputs["artifact_ids"][0],
            )

    def test_attempt_ids_are_deterministic_and_numbered(self) -> None:
        from runtime import attempt_record_id

        first = attempt_record_id(result_id="gen_fixed", attempt_number=1)
        self.assertEqual(first, attempt_record_id(result_id="gen_fixed", attempt_number=1))
        self.assertNotEqual(first, attempt_record_id(result_id="gen_fixed", attempt_number=2))


class PersistenceTests(unittest.TestCase):
    def test_revisions_increment_for_each_transition(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            job, plan, path = context(Path(folder))
            manifest = run_generation_plan(
                job,
                plan,
                path,
                {"scene.fake": FakeSceneGenerator(fail_first_n=1)},
                max_attempts_per_task=2,
            )
            self.assertEqual(6, manifest.revision)

    def test_every_persisted_transition_is_valid_and_atomic(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            job, plan, path = context(Path(folder))
            revisions = []
            real_save = orchestrator_module.save_manifest_atomic

            def recording_save(target, manifest):
                validate_manifest(manifest)
                revisions.append(manifest.revision)
                real_save(target, manifest)
                self.assertFalse(target.with_name(target.name + ".writing").exists())

            with patch.object(orchestrator_module, "save_manifest_atomic", recording_save):
                run_generation_plan(job, plan, path, {"scene.fake": FakeSceneGenerator()})
            self.assertEqual([1, 2, 3, 4], revisions)

    def test_no_network_subprocess_or_gpu_dependency(self) -> None:
        forbidden = {"subprocess", "requests", "urllib", "torch", "comfyui"}
        self.assertTrue(forbidden.isdisjoint(orchestrator_module.__dict__))
        import runtime.providers as providers_module

        self.assertTrue(forbidden.isdisjoint(providers_module.__dict__))


if __name__ == "__main__":
    unittest.main()
