from __future__ import annotations

from collections import Counter
from urllib.parse import urlparse

from .models import (
    JOB_SPEC_SCHEMA,
    MANIFEST_SCHEMA,
    SCHEMA_VERSION,
    JobSpec,
    Manifest,
    RuntimeStatus,
    SelectionStatus,
)


class ContractValidationError(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractValidationError(message)


def _unique(values: list[str], label: str) -> None:
    duplicates = sorted(value for value, count in Counter(values).items() if count > 1)
    _require(not duplicates, f"Duplicate {label}: {duplicates}")


def _logical_uri(value: str | None, label: str) -> None:
    if value is None:
        return
    parsed = urlparse(value)
    _require(parsed.scheme in {"client", "workspace", "repo", "model"}, f"{label} must be a logical URI")


def _validate_status_error(item: object, label: str) -> None:
    status = getattr(item, "status")
    error = getattr(item, "error")
    if status == RuntimeStatus.FAILED:
        _require(error is not None, f"Failed {label} requires error")
    if status == RuntimeStatus.SUCCEEDED:
        _require(error is None, f"Succeeded {label} must not contain error")


def _output_artifact_ids(outputs: dict[str, object]) -> set[str]:
    references: set[str] = set()
    for key, value in outputs.items():
        if key == "artifact_id" and isinstance(value, str):
            references.add(value)
        elif key == "artifact_ids" and isinstance(value, list):
            references.update(item for item in value if isinstance(item, str))
        elif isinstance(value, dict):
            references.update(_output_artifact_ids(value))
    return references


def validate_job_spec(job: JobSpec) -> None:
    _require(job.schema == JOB_SPEC_SCHEMA, f"Unsupported JobSpec schema: {job.schema}")
    _require(job.schema_version == SCHEMA_VERSION, f"Unsupported JobSpec version: {job.schema_version}")
    _require(bool(job.job_id), "job_id is required")
    _require(bool(job.client_id), "client_id is required")
    _require(job.base_seed >= 0, "base_seed must be non-negative")
    _require(job.quality_plan.human_review_required, "Human review is required in ONYX v1")

    _unique([scene.scene_id for scene in job.scenes], "scene IDs")
    generator_ids = [item.provider.provider_id for item in job.scene_generators]
    identity_provider_ids = [item.provider.provider_id for item in job.identity_providers]
    profile_ids = [item.profile_id for item in job.identity_profiles]
    _unique(generator_ids, "scene generator provider IDs")
    _unique(identity_provider_ids, "identity provider IDs")
    _unique(profile_ids, "identity profile IDs")

    for profile in job.identity_profiles:
        _logical_uri(profile.client_profile_uri, "client_profile_uri")
        _unique([item.reference_id for item in profile.references], f"reference IDs in {profile.profile_id}")
        for reference in profile.references:
            _logical_uri(reference.uri, f"reference {reference.reference_id} URI")

    for config in job.scene_generators:
        _require(config.candidate_count_per_scene > 0, "candidate_count_per_scene must be positive")
        provider = config.provider
        is_personal_lora = provider.identity_mode == "personal_lora" or "lora" in provider.provider_id.lower()
        if config.enabled and is_personal_lora:
            _require(job.service_tier.lower() == "vip", "Personal LoRA is VIP-only")
            _require(provider.identity_aware, "Personal LoRA must be identity-aware")
        if config.identity_profile_id:
            _require(config.identity_profile_id in profile_ids, f"Unknown identity profile: {config.identity_profile_id}")
        _logical_uri(provider.workflow_uri, f"workflow URI for {provider.provider_id}")

    for config in job.identity_providers:
        unknown = set(config.apply_to_generator_ids) - set(generator_ids)
        _require(not unknown, f"Identity provider {config.provider.provider_id} targets unknown generators: {sorted(unknown)}")
        _logical_uri(config.provider.workflow_uri, f"workflow URI for {config.provider.provider_id}")

    if job.postprocessing:
        _require(job.postprocessing.selected_candidates_only, "ONYX v1 postprocessing must be selected-candidates-only")
        _logical_uri(job.postprocessing.provider.workflow_uri, "postprocessing workflow URI")
    if job.delivery:
        _logical_uri(job.delivery.destination_uri, "delivery destination_uri")
    _logical_uri(job.workspace_uri, "workspace_uri")


def validate_manifest(manifest: Manifest) -> None:
    _require(manifest.schema == MANIFEST_SCHEMA, f"Unsupported Manifest schema: {manifest.schema}")
    _require(manifest.schema_version == SCHEMA_VERSION, f"Unsupported Manifest version: {manifest.schema_version}")
    _require(manifest.revision >= 0, "Manifest revision must be non-negative")

    collections = [
        manifest.generation_results,
        manifest.identity_results,
        manifest.evaluation_results,
        manifest.human_reviews,
        manifest.selection_decisions,
        manifest.postprocess_results,
        manifest.delivery_results,
    ]
    result_ids = [item.result_id for collection in collections for item in collection]
    _unique(result_ids, "result IDs")
    _unique([item.artifact_id for item in manifest.artifacts], "artifact IDs")
    _unique([item.attempt_id for item in manifest.attempts], "attempt IDs")

    generations = {item.result_id: item for item in manifest.generation_results}
    identities = {item.result_id: item for item in manifest.identity_results}
    evaluations = {item.result_id: item for item in manifest.evaluation_results}
    reviews = {item.result_id: item for item in manifest.human_reviews}
    selections = {item.result_id: item for item in manifest.selection_decisions}
    posts = {item.result_id: item for item in manifest.postprocess_results}

    runtime_entities = [
        *manifest.generation_results,
        *manifest.identity_results,
        *manifest.evaluation_results,
        *manifest.human_reviews,
        *manifest.postprocess_results,
        *manifest.delivery_results,
        *manifest.attempts,
    ]
    for item in runtime_entities:
        _validate_status_error(item, type(item).__name__)

    for identity in manifest.identity_results:
        _require(identity.generation_result_id in generations, f"IdentityResult {identity.result_id} has unknown generation parent")
        if identity.mode == "native_passthrough":
            _require(identity.provider.provider_id == "identity.native", "native_passthrough must use identity.native")

    for evaluation in manifest.evaluation_results:
        _require(evaluation.identity_result_id in identities, f"EvaluationResult {evaluation.result_id} must reference an IdentityResult")

    for review in manifest.human_reviews:
        _require(review.identity_result_id in identities, f"HumanReview {review.result_id} must reference an IdentityResult")

    for selection in manifest.selection_decisions:
        _require(selection.identity_result_id in identities, f"SelectionDecision {selection.result_id} must reference an IdentityResult")
        _require(set(selection.evaluation_result_ids) <= set(evaluations), f"SelectionDecision {selection.result_id} references unknown evaluations")
        _require(set(selection.human_review_ids) <= set(reviews), f"SelectionDecision {selection.result_id} references unknown reviews")
        for evaluation_id in selection.evaluation_result_ids:
            _require(evaluations[evaluation_id].identity_result_id == selection.identity_result_id, "Selection evaluation has a different identity parent")
        for review_id in selection.human_review_ids:
            _require(reviews[review_id].identity_result_id == selection.identity_result_id, "Selection review has a different identity parent")
        if selection.status == SelectionStatus.SELECTED:
            _require(bool(selection.human_review_ids), "Selected candidate requires human review")
            _require(all(reviews[item].status == RuntimeStatus.SUCCEEDED for item in selection.human_review_ids), "Selected candidate requires succeeded human review")
            _require(
                any(reviews[item].ratings.get("client_ready") is True for item in selection.human_review_ids),
                "Selected candidate requires human client_ready=true",
            )
            selected_evaluations = [evaluations[item] for item in selection.evaluation_result_ids]
            _require(
                all(item.status == RuntimeStatus.SUCCEEDED for item in selected_evaluations),
                "Selected candidate requires succeeded evaluations",
            )
            _require(
                not any(item.hard_fail or item.verdict == "fail" for item in selected_evaluations),
                "Automatic technical hard-fail blocks selection",
            )
            for required in (
                item for item in manifest.quality_plan.evaluators
                if item.enabled and item.required
            ):
                matches = [
                    item for item in selected_evaluations
                    if item.provider.provider_id == required.provider.provider_id
                ]
                _require(
                    bool(matches),
                    f"Selected candidate is missing required evaluation: {required.provider.provider_id}",
                )

    for post in manifest.postprocess_results:
        _require(post.selection_decision_id in selections, f"PostProcessResult {post.result_id} has unknown selection parent")
        selection = selections[post.selection_decision_id]
        _require(selection.status == SelectionStatus.SELECTED, f"PostProcessResult {post.result_id} requires selected input")
        _require(post.identity_result_id == selection.identity_result_id, "Postprocess identity does not match selection")

    for delivery in manifest.delivery_results:
        _require(delivery.postprocess_result_id in posts, f"DeliveryResult {delivery.result_id} has unknown postprocess parent")
        _require(posts[delivery.postprocess_result_id].status == RuntimeStatus.SUCCEEDED, f"DeliveryResult {delivery.result_id} requires succeeded postprocessing")
        _require("client_ready" not in delivery.outputs, "client_ready belongs to selection/quality, not DeliveryResult")

    for generation in manifest.generation_results:
        if generation.status == RuntimeStatus.SUCCEEDED and generation.provider.identity_aware:
            native = [
                item for item in manifest.identity_results
                if item.generation_result_id == generation.result_id and item.mode == "native_passthrough"
            ]
            _require(bool(native), f"Identity-aware generation {generation.result_id} requires native_passthrough IdentityResult")

    all_results = set(result_ids)
    for attempt in manifest.attempts:
        _require(attempt.result_id in all_results, f"Attempt {attempt.attempt_id} references unknown result")
    for artifact in manifest.artifacts:
        _require(artifact.created_by_id in all_results, f"Artifact {artifact.artifact_id} references unknown creator")
        _logical_uri(artifact.uri, f"artifact {artifact.artifact_id} URI")

    artifact_ids = {item.artifact_id for item in manifest.artifacts}
    artifact_producers = [
        *manifest.generation_results,
        *manifest.identity_results,
        *manifest.postprocess_results,
        *manifest.delivery_results,
    ]
    for result in artifact_producers:
        missing = _output_artifact_ids(result.outputs) - artifact_ids
        _require(not missing, f"{type(result).__name__} {result.result_id} references unknown artifacts: {sorted(missing)}")
