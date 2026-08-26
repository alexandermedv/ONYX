from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import unquote, urlparse

from contracts.ids import derive_seed
from contracts.models import JobSpec, ProviderRef
from contracts.validation import validate_job_spec

from .config import ProviderRuntimeConfig, RuntimeConfig
from .execution_plan import (
    ExecutionPlan,
    GenerationTask,
    MaterializedProvider,
    ResolvedIdentityProfile,
    ResolvedReference,
)


class MaterializationError(ValueError):
    """Raised when canonical intent cannot be resolved on this machine."""


def _safe_join(root_value: str, relative_parts: list[str], *, uri: str) -> str:
    root = Path(root_value).expanduser().resolve(strict=False)
    if not root.is_absolute():
        raise MaterializationError(f"Configured root must be absolute for {uri}: {root_value}")
    if not relative_parts or any(part in {"", ".", ".."} for part in relative_parts):
        raise MaterializationError(f"Logical URI has an invalid or unsafe path: {uri}")
    if any("\\" in part or "/" in part for part in relative_parts):
        raise MaterializationError(f"Logical URI contains an encoded path separator: {uri}")
    resolved = root.joinpath(*relative_parts).resolve(strict=False)
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise MaterializationError(f"Logical URI escapes configured root: {uri}") from exc
    return str(resolved)


def _uri_parts(uri: str) -> tuple[str, list[str]]:
    parsed = urlparse(uri)
    if not parsed.netloc:
        raise MaterializationError(f"Logical URI must include an authority: {uri}")
    if parsed.query or parsed.fragment or parsed.username or parsed.password:
        raise MaterializationError(f"Logical URI contains unsupported components: {uri}")
    try:
        port = parsed.port
    except ValueError as exc:
        raise MaterializationError(f"Logical URI contains an invalid authority: {uri}") from exc
    if port is not None:
        raise MaterializationError(f"Logical URI contains unsupported components: {uri}")
    raw_parts = [parsed.netloc, *parsed.path.split("/")]
    parts = [unquote(part) for part in raw_parts if part]
    if any(len(part) >= 2 and part[0].isalpha() and part[1] == ":" for part in parts):
        raise MaterializationError(f"Logical URI contains a Windows drive path: {uri}")
    return parsed.scheme.lower(), parts


def resolve_logical_uri(
    uri: str,
    runtime: RuntimeConfig,
    *,
    provider_id: str | None = None,
) -> str:
    scheme, parts = _uri_parts(uri)
    if scheme == "client":
        return _safe_join(runtime.client_root, parts, uri=uri)
    if scheme == "workspace":
        return _safe_join(runtime.workspace_root, parts, uri=uri)
    if scheme == "repo":
        return _safe_join(runtime.repo_root, parts, uri=uri)
    if scheme == "model":
        if provider_id is None:
            raise MaterializationError(f"model URI requires provider context: {uri}")
        provider = runtime.providers.get(provider_id)
        if provider is None:
            raise MaterializationError(f"Missing runtime mapping for provider {provider_id}")
        if len(parts) < 2:
            raise MaterializationError(f"model URI must include root alias and relative path: {uri}")
        root_alias, model_parts = parts[0], parts[1:]
        root = provider.model_roots.get(root_alias)
        if root is None:
            raise MaterializationError(
                f"Provider {provider_id} has no model root alias {root_alias!r} for {uri}"
            )
        return _safe_join(root, model_parts, uri=uri)
    raise MaterializationError(f"Unsupported logical URI scheme: {scheme or '<missing>'}")


def _runtime_path(value: str | None, label: str) -> str | None:
    if value is None:
        return None
    path = Path(value).expanduser().resolve(strict=False)
    if not path.is_absolute():
        raise MaterializationError(f"{label} must be an absolute path: {value}")
    return str(path)


def _materialize_provider(
    provider_ref: ProviderRef,
    provider_runtime: ProviderRuntimeConfig,
    runtime: RuntimeConfig,
) -> MaterializedProvider:
    workflow_path = None
    if provider_ref.workflow_uri:
        workflow_path = resolve_logical_uri(
            provider_ref.workflow_uri,
            runtime,
            provider_id=provider_ref.provider_id,
        )
    elif provider_runtime.workflow_root and provider_ref.workflow_id:
        workflow_path = _safe_join(
            provider_runtime.workflow_root,
            [provider_ref.workflow_id],
            uri=f"provider workflow {provider_ref.workflow_id}",
        )

    model_path = None
    if provider_ref.model_id:
        model_uri = provider_runtime.models.get(provider_ref.model_id)
        if model_uri is None:
            raise MaterializationError(
                f"Provider {provider_ref.provider_id} has no runtime model mapping for {provider_ref.model_id!r}"
            )
        if not model_uri.startswith("model://"):
            raise MaterializationError(
                f"Runtime model mapping for {provider_ref.model_id!r} must be a model:// URI"
            )
        model_path = resolve_logical_uri(model_uri, runtime, provider_id=provider_ref.provider_id)

    return MaterializedProvider(
        provider_id=provider_ref.provider_id,
        provider_kind=provider_ref.provider_kind,
        implementation_version=provider_ref.implementation_version,
        model_id=provider_ref.model_id,
        model_version=provider_ref.model_version,
        model_hash=provider_ref.model_hash,
        workflow_id=provider_ref.workflow_id,
        workflow_version=provider_ref.workflow_version,
        workflow_uri=provider_ref.workflow_uri,
        workflow_hash=provider_ref.workflow_hash,
        identity_aware=provider_ref.identity_aware,
        identity_mode=provider_ref.identity_mode,
        endpoint=provider_runtime.endpoint,
        root=_runtime_path(provider_runtime.root, f"provider {provider_ref.provider_id} root"),
        python_executable=_runtime_path(
            provider_runtime.python_executable,
            f"provider {provider_ref.provider_id} python_executable",
        ),
        input_root=_runtime_path(provider_runtime.input_root, f"provider {provider_ref.provider_id} input_root"),
        output_root=_runtime_path(provider_runtime.output_root, f"provider {provider_ref.provider_id} output_root"),
        workflow_path=workflow_path,
        model_path=model_path,
        capabilities=tuple(sorted(provider_runtime.capabilities)),
        runtime_metadata_json=json.dumps(
            provider_runtime.metadata,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ),
    )


def materialize_job(job_spec: JobSpec, runtime_config: RuntimeConfig) -> ExecutionPlan:
    validate_job_spec(job_spec)

    enabled_refs: dict[str, ProviderRef] = {}
    for config in job_spec.scene_generators:
        if config.enabled:
            is_lora = (
                config.provider.identity_mode == "personal_lora"
                or "lora" in config.provider.provider_id.lower()
            )
            if is_lora and job_spec.service_tier.lower() != "vip":
                raise MaterializationError("Personal LoRA is VIP-only")
            enabled_refs[config.provider.provider_id] = config.provider
    for config in job_spec.identity_providers:
        if config.enabled:
            enabled_refs[config.provider.provider_id] = config.provider
    for config in job_spec.quality_plan.evaluators:
        if config.enabled:
            enabled_refs[config.provider.provider_id] = config.provider
    if job_spec.postprocessing and job_spec.postprocessing.enabled:
        enabled_refs[job_spec.postprocessing.provider.provider_id] = job_spec.postprocessing.provider
    if job_spec.delivery:
        enabled_refs[job_spec.delivery.provider.provider_id] = job_spec.delivery.provider

    missing = sorted(set(enabled_refs) - set(runtime_config.providers))
    if missing:
        raise MaterializationError(f"Missing runtime mapping for enabled providers: {missing}")

    providers = tuple(
        _materialize_provider(ref, runtime_config.providers[provider_id], runtime_config)
        for provider_id, ref in sorted(enabled_refs.items())
    )

    workspace_uri = job_spec.workspace_uri or f"workspace://jobs/{job_spec.job_id}"
    workspace_path = resolve_logical_uri(workspace_uri, runtime_config)

    profiles: list[ResolvedIdentityProfile] = []
    references: list[ResolvedReference] = []
    for profile in job_spec.identity_profiles:
        if profile.client_profile_uri:
            profiles.append(
                ResolvedIdentityProfile(
                    profile_id=profile.profile_id,
                    client_profile_uri=profile.client_profile_uri,
                    client_profile_path=resolve_logical_uri(
                        profile.client_profile_uri,
                        runtime_config,
                    ),
                )
            )
        for reference in profile.references:
            references.append(
                ResolvedReference(
                    profile_id=profile.profile_id,
                    reference_id=reference.reference_id,
                    role=reference.role,
                    logical_uri=reference.uri,
                    resolved_path=resolve_logical_uri(reference.uri, runtime_config),
                )
            )

    tasks: list[GenerationTask] = []
    for scene in job_spec.scenes:
        for generator in job_spec.scene_generators:
            if not generator.enabled:
                continue
            provider_id = generator.provider.provider_id
            for candidate_index in range(generator.candidate_count_per_scene):
                tasks.append(
                    GenerationTask(
                        scene_id=scene.scene_id,
                        provider_id=provider_id,
                        candidate_index=candidate_index,
                        seed=derive_seed(
                            base_seed=job_spec.base_seed,
                            job_id=job_spec.job_id,
                            scene_id=scene.scene_id,
                            provider_id=provider_id,
                            candidate_index=candidate_index,
                            stage="generation",
                        ),
                        output_path=_safe_join(
                            workspace_path,
                            ["generation", provider_id, scene.scene_id, f"candidate_{candidate_index:03d}"],
                            uri="materialized generation output",
                        ),
                        identity_profile_id=generator.identity_profile_id,
                        scene_inputs_json=json.dumps(
                            {
                                "subject": scene.subject,
                                "prompt": scene.prompt,
                                "explicit_prompts": scene.explicit_prompts,
                            },
                            ensure_ascii=False,
                            sort_keys=True,
                            separators=(",", ":"),
                        ),
                        provider_parameters_json=json.dumps(
                            generator.parameters,
                            ensure_ascii=False,
                            sort_keys=True,
                            separators=(",", ":"),
                        ),
                    )
                )

    delivery_path = None
    if job_spec.delivery:
        delivery_path = resolve_logical_uri(job_spec.delivery.destination_uri, runtime_config)

    return ExecutionPlan(
        job_id=job_spec.job_id,
        machine_id=runtime_config.machine_id,
        workspace_uri=workspace_uri,
        workspace_path=workspace_path,
        providers=providers,
        identity_profiles=tuple(profiles),
        identity_references=tuple(references),
        generation_tasks=tuple(tasks),
        delivery_path=delivery_path,
    )
