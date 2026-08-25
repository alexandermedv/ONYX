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


GENERATOR_MAP = {
    "flux": ("scene.flux", False, None),
    "juggernautxl": ("scene.juggernautxl", False, None),
    "dreamo": ("scene.dreamo_t2i", True, "reference_images"),
    "lora": ("scene.flux_personal_lora", True, "personal_lora"),
}


def _workflow_uri(name: str) -> str:
    return f"repo://09 Experiments/ensemble_generator_0.2/workflows/{name}"


def parse_ensemble_job(data: dict[str, Any], *, source_uri: str | None = None) -> JobSpec:
    """Read an Ensemble v0.2/v0.3 job without retaining machine runtime paths."""
    required = {"job_id", "generators", "scenes"}
    missing = required - set(data)
    if missing:
        raise ValueError(f"Not an Ensemble job; missing: {sorted(missing)}")
    identity_data = dict(data.get("identity", {}))
    profile_id = f"identity_{data['job_id']}"
    reference = identity_data.get("dreamo_reference")
    references = []
    if reference:
        references.append(
            ReferenceRecord(
                reference_id="legacy_dreamo_reference",
                uri=f"client://{data.get('client_id', 'legacy-client')}/source/{Path(str(reference)).name}",
                role="primary",
            )
        )
    profile = IdentityProfile(profile_id=profile_id, references=references)

    generators: list[SceneGeneratorConfig] = []
    for legacy_name in data.get("generators", []):
        provider_id, identity_aware, identity_mode = GENERATOR_MAP.get(
            legacy_name, (f"scene.legacy.{legacy_name}", False, None)
        )
        workflow_name = {
            "flux": "flux_api.json",
            "juggernautxl": "ONYX_JuggernautXL_Generator_v0.3_weighted.json",
            "dreamo": "dreamo_api.json",
            "lora": "lora_api.json",
        }.get(legacy_name, f"{legacy_name}.json")
        generators.append(
            SceneGeneratorConfig(
                provider=ProviderRef(
                    provider_id=provider_id,
                    provider_kind="scene_generator",
                    implementation_version="ensemble-v0.3",
                    workflow_id=f"legacy-{legacy_name}",
                    workflow_version="0.3",
                    workflow_uri=_workflow_uri(workflow_name),
                    identity_aware=identity_aware,
                    identity_mode=identity_mode,
                ),
                enabled=(legacy_name != "lora" or bool(identity_data.get("lora", {}).get("enabled", False))),
                identity_profile_id=profile_id if identity_aware else None,
                parameters=(
                    {"trigger_word": data.get("trigger_word", "")}
                    if legacy_name == "lora"
                    else dict(data.get("renderer_settings", {}).get(legacy_name, {}))
                ),
            )
        )

    generator_ids = [item.provider.provider_id for item in generators]
    identity_providers: list[IdentityProviderConfig] = []
    facefusion = identity_data.get("facefusion", {})
    if facefusion.get("enabled", False):
        identity_providers.append(
            IdentityProviderConfig(
                provider=ProviderRef(
                    provider_id="identity.facefusion",
                    provider_kind="identity_provider",
                    implementation_version="ensemble-v0.3",
                    model_id="hyperswap_1a_256",
                ),
                apply_to_generator_ids=[item for item in generator_ids if item in {"scene.flux", "scene.juggernautxl"}],
                parameters={"legacy_configuration_present": True},
            )
        )
    dreamo_img2img = identity_data.get("dreamo_img2img", {})
    if dreamo_img2img.get("enabled", False):
        workflow_name = dreamo_img2img.get("workflow", "dreamo_img2img_api.json")
        identity_providers.append(
            IdentityProviderConfig(
                provider=ProviderRef(
                    provider_id="identity.dreamo_img2img",
                    provider_kind="identity_provider",
                    implementation_version="ensemble-v0.3",
                    model_id="dreamo",
                    workflow_id="legacy-dreamo-img2img",
                    workflow_version="0.3",
                    workflow_uri=_workflow_uri(Path(str(workflow_name)).name),
                ),
                apply_to_generator_ids=[item for item in generator_ids if item in {"scene.flux", "scene.juggernautxl"}],
                parameters={"legacy_seed_offset": dreamo_img2img.get("seed_offset", 100000)},
            )
        )

    scenes = [
        SceneSpec(
            scene_id=str(scene["scene_id"]),
            subject=str(scene.get("subject", "portrait subject")),
            prompt={
                key: value
                for key, value in scene.items()
                if key not in {"scene_id", "subject", "prompts", "seed"}
            },
            explicit_prompts=dict(scene.get("prompts", {})),
            seed=scene.get("seed"),
        )
        for scene in data["scenes"]
    ]
    post_data = dict(data.get("postprocess", {}))
    post = None
    if post_data:
        workflow_name = Path(str(post_data.get("workflow", "ONYX_Postprocessor v0.1.json"))).name
        post = PostProcessConfig(
            provider=ProviderRef(
                provider_id="postprocess.siax",
                provider_kind="postprocessor",
                implementation_version="ensemble-v0.3",
                model_id=str(post_data.get("model", "4x_NMKD-Siax_200k.pth")),
                workflow_id="onyx-postprocessor",
                workflow_version="0.1",
                workflow_uri=_workflow_uri(workflow_name),
            ),
            enabled=bool(post_data.get("enabled", False)),
            parameters={
                "legacy_methods": list(post_data.get("methods", [])),
                "legacy_scene_ids": list(post_data.get("scene_ids", [])),
            },
        )

    job_id = str(data["job_id"])
    job = JobSpec(
        schema=JOB_SPEC_SCHEMA,
        schema_version=SCHEMA_VERSION,
        job_id=job_id,
        client_id=str(data.get("client_id", "legacy-client")),
        service_tier=str(data.get("service_tier", "mass")).lower(),
        base_seed=int(data.get("base_seed", 0)),
        scenes=scenes,
        scene_generators=generators,
        identity_profiles=[profile],
        identity_providers=identity_providers,
        quality_plan=QualityPlan(human_review_required=True),
        postprocessing=post,
        delivery=DeliveryConfig(
            provider=ProviderRef(
                provider_id="delivery.local",
                provider_kind="delivery_provider",
                implementation_version="1.0",
            ),
            destination_uri=f"workspace://final_results/{job_id}",
        ),
        workspace_uri=f"workspace://runs/{job_id}",
        continue_independent_failures=not bool(data.get("stop_on_error", False)),
        legacy={
            "source_format": "onyx.ensemble.job.v0.3",
            "source_uri": source_uri,
            "machine_runtime_fields_omitted": [
                key for key in ("work_root", "final_results_root") if key in data
            ],
        },
    )
    validate_job_spec(job)
    return job


def load_ensemble_job(path: Path) -> JobSpec:
    return parse_ensemble_job(
        json.loads(path.read_text(encoding="utf-8-sig")),
        source_uri=f"repo://{path.name}",
    )

