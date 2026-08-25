from __future__ import annotations

from dataclasses import dataclass, field, fields, is_dataclass
from enum import Enum
from types import UnionType
from typing import Any, TypeVar, Union, get_args, get_origin, get_type_hints


JOB_SPEC_SCHEMA = "onyx.job_spec"
MANIFEST_SCHEMA = "onyx.manifest"
SCHEMA_VERSION = "1.0"


class RuntimeStatus(str, Enum):
    PLANNED = "planned"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    SKIPPED = "skipped"
    CANCELLED = "cancelled"


class SelectionStatus(str, Enum):
    PENDING = "pending"
    SELECTED = "selected"
    REJECTED = "rejected"


T = TypeVar("T", bound="Serializable")


def _encode(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return {item.name: _encode(getattr(value, item.name)) for item in fields(value)}
    if isinstance(value, dict):
        return {key: _encode(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_encode(item) for item in value]
    return value


def _decode(annotation: Any, value: Any) -> Any:
    if value is None:
        return None
    origin = get_origin(annotation)
    args = get_args(annotation)
    if origin in (Union, UnionType):
        non_none = [arg for arg in args if arg is not type(None)]
        return _decode(non_none[0], value) if len(non_none) == 1 else value
    if origin is list:
        return [_decode(args[0], item) for item in value]
    if origin is dict:
        return dict(value)
    if isinstance(annotation, type) and issubclass(annotation, Enum):
        return annotation(value)
    if isinstance(annotation, type) and is_dataclass(annotation):
        return annotation.from_dict(value)
    return value


@dataclass
class Serializable:
    """Small standard-library serialization base for contract dataclasses."""

    def to_dict(self) -> dict[str, Any]:
        return _encode(self)

    @classmethod
    def from_dict(cls: type[T], data: dict[str, Any]) -> T:
        hints = get_type_hints(cls)
        known = {item.name for item in fields(cls)}
        unknown = set(data) - known
        if unknown:
            raise ValueError(f"Unknown {cls.__name__} fields: {sorted(unknown)}")
        values = {
            item.name: _decode(hints.get(item.name, Any), data[item.name])
            for item in fields(cls)
            if item.name in data
        }
        return cls(**values)


@dataclass
class ErrorRecord(Serializable):
    code: str
    category: str
    message: str
    retryable: bool = False
    details: dict[str, Any] = field(default_factory=dict)
    attempt_id: str | None = None
    log_uri: str | None = None


@dataclass
class ProviderRef(Serializable):
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


@dataclass
class ReferenceRecord(Serializable):
    reference_id: str
    uri: str
    role: str = "supporting"


@dataclass
class IdentityProfile(Serializable):
    profile_id: str
    client_profile_uri: str | None = None
    references: list[ReferenceRecord] = field(default_factory=list)


@dataclass
class SceneSpec(Serializable):
    scene_id: str
    subject: str
    prompt: dict[str, Any] = field(default_factory=dict)
    explicit_prompts: dict[str, str] = field(default_factory=dict)
    seed: int | None = None


@dataclass
class SceneGeneratorConfig(Serializable):
    provider: ProviderRef
    enabled: bool = True
    candidate_count_per_scene: int = 1
    identity_profile_id: str | None = None
    parameters: dict[str, Any] = field(default_factory=dict)


@dataclass
class IdentityProviderConfig(Serializable):
    provider: ProviderRef
    enabled: bool = True
    apply_to_generator_ids: list[str] = field(default_factory=list)
    result_count_per_candidate: int = 1
    parameters: dict[str, Any] = field(default_factory=dict)


@dataclass
class EvaluatorConfig(Serializable):
    provider: ProviderRef
    enabled: bool = True
    required: bool = True
    parameters: dict[str, Any] = field(default_factory=dict)


@dataclass
class QualityPlan(Serializable):
    evaluators: list[EvaluatorConfig] = field(default_factory=list)
    human_review_required: bool = True
    rubric_id: str = "portrait-review-v1"
    rubric_version: str = "1.0"


@dataclass
class SelectionPolicy(Serializable):
    policy_id: str = "selection.human_required_v1"
    policy_version: str = "1.0"
    automatic_hard_fail_blocks: bool = True
    human_client_ready_required: bool = True


@dataclass
class PostProcessConfig(Serializable):
    provider: ProviderRef
    enabled: bool = True
    selected_candidates_only: bool = True
    parameters: dict[str, Any] = field(default_factory=dict)


@dataclass
class DeliveryConfig(Serializable):
    provider: ProviderRef
    destination_uri: str
    filename_template: str = "ONYX_{sequence:03d}{extension}"


@dataclass
class JobSpec(Serializable):
    schema: str
    schema_version: str
    job_id: str
    client_id: str
    service_tier: str
    base_seed: int
    scenes: list[SceneSpec]
    scene_generators: list[SceneGeneratorConfig]
    identity_profiles: list[IdentityProfile] = field(default_factory=list)
    identity_providers: list[IdentityProviderConfig] = field(default_factory=list)
    quality_plan: QualityPlan = field(default_factory=QualityPlan)
    selection_policy: SelectionPolicy = field(default_factory=SelectionPolicy)
    postprocessing: PostProcessConfig | None = None
    delivery: DeliveryConfig | None = None
    workspace_uri: str | None = None
    continue_independent_failures: bool = True
    legacy: dict[str, Any] = field(default_factory=dict)


@dataclass
class ArtifactRecord(Serializable):
    artifact_id: str
    kind: str
    role: str
    uri: str
    created_by_id: str
    sha256: str | None = None
    mime_type: str | None = None
    size_bytes: int | None = None
    width: int | None = None
    height: int | None = None
    resolved_path: str | None = None


@dataclass
class AttemptRecord(Serializable):
    attempt_id: str
    result_id: str
    attempt_number: int
    status: RuntimeStatus
    started_at: str | None = None
    finished_at: str | None = None
    duration_ms: int | None = None
    runtime: dict[str, Any] = field(default_factory=dict)
    error: ErrorRecord | None = None


@dataclass
class GenerationResult(Serializable):
    result_id: str
    scene_id: str
    candidate_index: int
    status: RuntimeStatus
    provider: ProviderRef
    inputs: dict[str, Any]
    outputs: dict[str, Any] = field(default_factory=dict)
    attempt_ids: list[str] = field(default_factory=list)
    idempotency_key: str | None = None
    started_at: str | None = None
    finished_at: str | None = None
    duration_ms: int | None = None
    error: ErrorRecord | None = None


@dataclass
class IdentityResult(Serializable):
    result_id: str
    generation_result_id: str
    status: RuntimeStatus
    provider: ProviderRef
    mode: str
    inputs: dict[str, Any]
    outputs: dict[str, Any] = field(default_factory=dict)
    attempt_ids: list[str] = field(default_factory=list)
    idempotency_key: str | None = None
    started_at: str | None = None
    finished_at: str | None = None
    duration_ms: int | None = None
    error: ErrorRecord | None = None


@dataclass
class EvaluationResult(Serializable):
    result_id: str
    identity_result_id: str
    status: RuntimeStatus
    provider: ProviderRef
    inputs: dict[str, Any]
    metrics: dict[str, Any] = field(default_factory=dict)
    hard_fail: bool = False
    verdict: str | None = None
    attempt_ids: list[str] = field(default_factory=list)
    started_at: str | None = None
    finished_at: str | None = None
    duration_ms: int | None = None
    error: ErrorRecord | None = None


@dataclass
class HumanReview(Serializable):
    result_id: str
    identity_result_id: str
    status: RuntimeStatus
    provider: ProviderRef
    reviewer_id: str
    rubric_id: str
    rubric_version: str
    inputs: dict[str, Any]
    ratings: dict[str, Any] = field(default_factory=dict)
    started_at: str | None = None
    finished_at: str | None = None
    duration_ms: int | None = None
    error: ErrorRecord | None = None


@dataclass
class SelectionDecision(Serializable):
    result_id: str
    identity_result_id: str
    status: SelectionStatus
    provider: ProviderRef
    evaluation_result_ids: list[str] = field(default_factory=list)
    human_review_ids: list[str] = field(default_factory=list)
    inputs: dict[str, Any] = field(default_factory=dict)
    reasons: list[str] = field(default_factory=list)
    decided_at: str | None = None
    error: ErrorRecord | None = None


@dataclass
class PostProcessResult(Serializable):
    result_id: str
    selection_decision_id: str
    identity_result_id: str
    status: RuntimeStatus
    provider: ProviderRef
    inputs: dict[str, Any]
    outputs: dict[str, Any] = field(default_factory=dict)
    attempt_ids: list[str] = field(default_factory=list)
    idempotency_key: str | None = None
    started_at: str | None = None
    finished_at: str | None = None
    duration_ms: int | None = None
    error: ErrorRecord | None = None


@dataclass
class DeliveryResult(Serializable):
    result_id: str
    postprocess_result_id: str
    status: RuntimeStatus
    provider: ProviderRef
    inputs: dict[str, Any]
    outputs: dict[str, Any] = field(default_factory=dict)
    attempt_ids: list[str] = field(default_factory=list)
    idempotency_key: str | None = None
    started_at: str | None = None
    finished_at: str | None = None
    duration_ms: int | None = None
    error: ErrorRecord | None = None


@dataclass
class Manifest(Serializable):
    schema: str
    schema_version: str
    manifest_id: str
    job_id: str
    revision: int
    status: RuntimeStatus = RuntimeStatus.PLANNED
    created_at: str | None = None
    updated_at: str | None = None
    job_spec_uri: str | None = None
    job_spec_hash: str | None = None
    quality_plan: QualityPlan = field(default_factory=QualityPlan)
    resolved_runtime: dict[str, Any] = field(default_factory=dict)
    generation_results: list[GenerationResult] = field(default_factory=list)
    identity_results: list[IdentityResult] = field(default_factory=list)
    evaluation_results: list[EvaluationResult] = field(default_factory=list)
    human_reviews: list[HumanReview] = field(default_factory=list)
    selection_decisions: list[SelectionDecision] = field(default_factory=list)
    postprocess_results: list[PostProcessResult] = field(default_factory=list)
    delivery_results: list[DeliveryResult] = field(default_factory=list)
    artifacts: list[ArtifactRecord] = field(default_factory=list)
    attempts: list[AttemptRecord] = field(default_factory=list)
    compatibility: dict[str, Any] = field(default_factory=dict)
