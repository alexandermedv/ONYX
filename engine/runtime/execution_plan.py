from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class ResolvedReference:
    profile_id: str
    reference_id: str
    role: str
    logical_uri: str
    resolved_path: str


@dataclass(frozen=True)
class ResolvedIdentityProfile:
    profile_id: str
    client_profile_uri: str
    client_profile_path: str


@dataclass(frozen=True)
class MaterializedProvider:
    provider_id: str
    provider_kind: str
    implementation_version: str
    model_id: str | None = None
    model_version: str | None = None
    model_hash: str | None = None
    workflow_id: str | None = None
    workflow_version: str | None = None
    workflow_uri: str | None = None
    workflow_hash: str | None = None
    identity_aware: bool = False
    identity_mode: str | None = None
    endpoint: str | None = None
    root: str | None = None
    python_executable: str | None = None
    input_root: str | None = None
    output_root: str | None = None
    workflow_path: str | None = None
    model_path: str | None = None
    capabilities: tuple[str, ...] = ()
    runtime_metadata_json: str = "{}"

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["capabilities"] = list(self.capabilities)
        result["runtime_metadata"] = json.loads(self.runtime_metadata_json)
        del result["runtime_metadata_json"]
        return result


@dataclass(frozen=True)
class GenerationTask:
    scene_id: str
    provider_id: str
    candidate_index: int
    seed: int
    output_path: str
    identity_profile_id: str | None = None
    scene_inputs_json: str = "{}"
    provider_parameters_json: str = "{}"

    def to_dict(self) -> dict[str, Any]:
        return {
            "scene_id": self.scene_id,
            "provider_id": self.provider_id,
            "candidate_index": self.candidate_index,
            "seed": self.seed,
            "output_path": self.output_path,
            "identity_profile_id": self.identity_profile_id,
            "scene_inputs": json.loads(self.scene_inputs_json),
            "provider_parameters": json.loads(self.provider_parameters_json),
        }


@dataclass(frozen=True)
class ExecutionPlan:
    job_id: str
    machine_id: str
    workspace_uri: str
    workspace_path: str
    providers: tuple[MaterializedProvider, ...]
    identity_profiles: tuple[ResolvedIdentityProfile, ...]
    identity_references: tuple[ResolvedReference, ...]
    generation_tasks: tuple[GenerationTask, ...]
    delivery_path: str | None = None

    def resolved_runtime_snapshot(self) -> dict[str, Any]:
        return {
            "runtime_config_schema": "onyx.runtime_config",
            "runtime_config_version": "1.0",
            "machine_id": self.machine_id,
            "workspace_uri": self.workspace_uri,
            "workspace_path": self.workspace_path,
            "providers": [provider.to_dict() for provider in self.providers],
            "identity_profiles": [asdict(profile) for profile in self.identity_profiles],
            "identity_references": [asdict(reference) for reference in self.identity_references],
            "delivery_path": self.delivery_path,
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "job_id": self.job_id,
            "machine_id": self.machine_id,
            "workspace_uri": self.workspace_uri,
            "workspace_path": self.workspace_path,
            "providers": [provider.to_dict() for provider in self.providers],
            "identity_profiles": [asdict(profile) for profile in self.identity_profiles],
            "identity_references": [asdict(reference) for reference in self.identity_references],
            "generation_tasks": [task.to_dict() for task in self.generation_tasks],
            "delivery_path": self.delivery_path,
        }
