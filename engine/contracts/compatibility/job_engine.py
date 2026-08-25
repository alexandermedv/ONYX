from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..models import (
    JOB_SPEC_SCHEMA,
    SCHEMA_VERSION,
    DeliveryConfig,
    IdentityProfile,
    IdentityProviderConfig,
    JobSpec,
    PostProcessConfig,
    ProviderRef,
    QualityPlan,
    ReferenceRecord,
    SceneGeneratorConfig,
    SceneSpec,
)
from ..validation import validate_job_spec


def _repo_workflow(command: list[str], flag: str) -> str | None:
    try:
        value = command[command.index(flag) + 1]
    except (ValueError, IndexError):
        return None
    name = Path(value).name
    return f"repo://legacy/workflows/{name}" if name else None


def parse_job_engine_job(data: dict[str, Any], *, source_uri: str | None = None) -> JobSpec:
    """Read a Job Engine v1 job into canonical, machine-independent intent."""
    required = {"schema_version", "job_id", "client_id", "pipeline"}
    missing = required - set(data)
    if missing:
        raise ValueError(f"Not a Job Engine job; missing: {sorted(missing)}")
    pipeline = data["pipeline"]
    scene_cfg = pipeline.get("scene_generator", {})
    face_cfg = pipeline.get("facefusion", {})
    post_cfg = pipeline.get("postprocessor", {})
    scene_command = list(scene_cfg.get("command", []))
    post_command = list(post_cfg.get("command", []))
    count = int(scene_cfg.get("minimum_output_images", 1))
    client_id = str(data["client_id"])

    scenes = [
        SceneSpec(scene_id=f"scene_{index:03d}", subject="legacy client portrait")
        for index in range(1, count + 1)
    ]
    profile = IdentityProfile(
        profile_id=f"identity_{client_id}_legacy",
        client_profile_uri=f"client://{client_id}/profile/client_profile.json",
        references=[
            ReferenceRecord(
                reference_id=f"{client_id}_legacy_source_set",
                uri=f"client://{client_id}/source/",
                role="source_set",
            )
        ],
    )
    generator = SceneGeneratorConfig(
        provider=ProviderRef(
            provider_id="scene.flux_legacy",
            provider_kind="scene_generator",
            implementation_version="job-engine-v1",
            workflow_id="legacy-scene-workflow",
            workflow_version="unknown",
            workflow_uri=_repo_workflow(scene_command, "--workflow"),
        ),
        candidate_count_per_scene=1,
        parameters={"legacy_minimum_output_images": count},
    )
    identity = IdentityProviderConfig(
        provider=ProviderRef(
            provider_id="identity.facefusion",
            provider_kind="identity_provider",
            implementation_version="legacy",
            model_id="hyperswap_1a_256",
        ),
        enabled=bool(face_cfg.get("enabled", True)),
        apply_to_generator_ids=[generator.provider.provider_id],
        parameters={"legacy_minimum_output_images": face_cfg.get("minimum_output_images", 1)},
    )
    post = PostProcessConfig(
        provider=ProviderRef(
            provider_id="postprocess.portrait_legacy",
            provider_kind="postprocessor",
            implementation_version="job-engine-v1",
            workflow_id="legacy-portrait-postprocessor",
            workflow_version="1.0",
            workflow_uri=_repo_workflow(post_command, "--workflow"),
        ),
        enabled=bool(post_cfg.get("enabled", True)),
    )
    job = JobSpec(
        schema=JOB_SPEC_SCHEMA,
        schema_version=SCHEMA_VERSION,
        job_id=str(data["job_id"]),
        client_id=client_id,
        service_tier="mass",
        base_seed=0,
        scenes=scenes,
        scene_generators=[generator],
        identity_profiles=[profile],
        identity_providers=[identity],
        quality_plan=QualityPlan(human_review_required=True),
        postprocessing=post,
        delivery=DeliveryConfig(
            provider=ProviderRef(
                provider_id="delivery.local",
                provider_kind="delivery_provider",
                implementation_version="1.0",
            ),
            destination_uri=f"workspace://jobs/{data['job_id']}/04_final",
        ),
        workspace_uri=f"workspace://jobs/{data['job_id']}",
        legacy={
            "source_format": "onyx.job_engine.job.v1",
            "source_schema_version": str(data.get("schema_version", "unknown")),
            "source_uri": source_uri,
            "legacy_pipeline_stages": list(pipeline),
            "machine_runtime_fields_omitted": [
                "paths.client_profile",
                *[f"pipeline.{name}.command" for name in pipeline],
            ],
        },
    )
    validate_job_spec(job)
    return job


def load_job_engine_job(path: Path) -> JobSpec:
    return parse_job_engine_job(
        json.loads(path.read_text(encoding="utf-8-sig")),
        source_uri=f"repo://{path.name}",
    )
