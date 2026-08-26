from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from .execution_plan import MaterializedProvider


@dataclass(frozen=True)
class SceneGeneratorRequest:
    generation_result_id: str
    job_id: str
    scene_id: str
    provider_id: str
    candidate_index: int
    seed: int
    output_path: str
    scene_inputs_json: str
    provider_parameters_json: str
    provider: MaterializedProvider

    def scene_inputs(self) -> dict[str, object]:
        return json.loads(self.scene_inputs_json)

    def provider_parameters(self) -> dict[str, object]:
        return json.loads(self.provider_parameters_json)


@dataclass(frozen=True)
class ProviderArtifact:
    resolved_path: str
    kind: str = "file"
    role: str = "generation_output"
    mime_type: str | None = None


@dataclass(frozen=True)
class ProviderError:
    code: str
    category: str
    message: str
    retryable: bool = False


@dataclass(frozen=True)
class ProviderExecutionResult:
    succeeded: bool
    artifacts: tuple[ProviderArtifact, ...] = ()
    metadata_json: str = "{}"
    error: ProviderError | None = None

    @classmethod
    def success(
        cls,
        *artifacts: ProviderArtifact,
        metadata: dict[str, object] | None = None,
    ) -> ProviderExecutionResult:
        return cls(
            succeeded=True,
            artifacts=tuple(artifacts),
            metadata_json=json.dumps(
                metadata or {}, ensure_ascii=False, sort_keys=True, separators=(",", ":")
            ),
        )

    @classmethod
    def failure(
        cls,
        code: str,
        category: str,
        message: str,
        *,
        retryable: bool = False,
        metadata: dict[str, object] | None = None,
    ) -> ProviderExecutionResult:
        return cls(
            succeeded=False,
            metadata_json=json.dumps(
                metadata or {}, ensure_ascii=False, sort_keys=True, separators=(",", ":")
            ),
            error=ProviderError(code, category, message, retryable),
        )


class SceneGenerator(Protocol):
    def execute(self, request: SceneGeneratorRequest) -> ProviderExecutionResult:
        """Execute one resolved generation request without accessing Manifest."""


class FakeSceneGenerator:
    """Deterministic CPU-only provider used to verify orchestration semantics."""

    def __init__(
        self,
        *,
        fail: bool = False,
        fail_first_n: int = 0,
        raise_exception: bool = False,
    ) -> None:
        self.fail = fail
        self.fail_first_n = fail_first_n
        self.raise_exception = raise_exception
        self.invocation_count = 0
        self.requests: list[SceneGeneratorRequest] = []

    def execute(self, request: SceneGeneratorRequest) -> ProviderExecutionResult:
        self.invocation_count += 1
        self.requests.append(request)
        if self.raise_exception:
            raise RuntimeError("Configured fake provider exception")
        if self.fail or self.invocation_count <= self.fail_first_n:
            return ProviderExecutionResult.failure(
                "FAKE_GENERATION_FAILED",
                "provider_execution",
                "Configured fake generation failure",
                retryable=True,
                metadata={"fake_attempt": self.invocation_count},
            )

        output_dir = Path(request.output_path)
        output_dir.mkdir(parents=True, exist_ok=True)
        output = output_dir / "artifact.json"
        payload = {
            "candidate_index": request.candidate_index,
            "generation_result_id": request.generation_result_id,
            "job_id": request.job_id,
            "provider_id": request.provider_id,
            "provider_parameters": request.provider_parameters(),
            "scene_id": request.scene_id,
            "scene_inputs": request.scene_inputs(),
            "seed": request.seed,
        }
        output.write_text(
            json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
            encoding="utf-8",
        )
        return ProviderExecutionResult.success(
            ProviderArtifact(str(output), kind="data", mime_type="application/json"),
            metadata={"fake_provider": True},
        )
