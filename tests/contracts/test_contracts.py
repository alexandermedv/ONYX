from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "engine"))

from contracts.ids import (
    delivery_result_id,
    derive_seed,
    evaluation_result_id,
    generation_result_id,
    identity_result_id,
    postprocess_result_id,
    stable_id,
)
from contracts.job_spec import dumps_job_spec, loads_job_spec
from contracts.manifest import dumps_manifest, loads_manifest
from contracts.models import (
    JOB_SPEC_SCHEMA,
    MANIFEST_SCHEMA,
    SCHEMA_VERSION,
    ArtifactRecord,
    DeliveryConfig,
    DeliveryResult,
    ErrorRecord,
    EvaluationResult,
    EvaluatorConfig,
    GenerationResult,
    HumanReview,
    IdentityProfile,
    IdentityResult,
    JobSpec,
    Manifest,
    PostProcessConfig,
    PostProcessResult,
    ProviderRef,
    QualityPlan,
    ReferenceRecord,
    RuntimeStatus,
    SceneGeneratorConfig,
    SceneSpec,
    SelectionDecision,
    SelectionStatus,
)
from contracts.persistence import load_manifest, save_manifest_atomic
from contracts.validation import ContractValidationError, validate_job_spec, validate_manifest


def provider(provider_id: str, kind: str, *, identity_aware: bool = False, identity_mode: str | None = None) -> ProviderRef:
    return ProviderRef(
        provider_id=provider_id,
        provider_kind=kind,
        implementation_version="1.0",
        identity_aware=identity_aware,
        identity_mode=identity_mode,
    )


def make_job(*, tier: str = "vip", include_lora: bool = True) -> JobSpec:
    generators = [
        SceneGeneratorConfig(provider=provider("scene.flux", "scene_generator")),
    ]
    if include_lora:
        generators.append(
            SceneGeneratorConfig(
                provider=provider(
                    "scene.flux_personal_lora",
                    "scene_generator",
                    identity_aware=True,
                    identity_mode="personal_lora",
                ),
                identity_profile_id="identity_fixture",
            )
        )
    return JobSpec(
        schema=JOB_SPEC_SCHEMA,
        schema_version=SCHEMA_VERSION,
        job_id="job_fixture",
        client_id="fixture-client",
        service_tier=tier,
        base_seed=12345,
        scenes=[SceneSpec(scene_id="scene_001", subject="adult portrait subject")],
        scene_generators=generators,
        identity_profiles=[
            IdentityProfile(
                profile_id="identity_fixture",
                references=[ReferenceRecord("ref_001", "client://fixture-client/source/ref.png", "primary")],
            )
        ],
        quality_plan=QualityPlan(human_review_required=True),
        postprocessing=PostProcessConfig(provider=provider("postprocess.siax", "postprocessor")),
        delivery=DeliveryConfig(
            provider=provider("delivery.local", "delivery_provider"),
            destination_uri="workspace://final_results/job_fixture",
        ),
        workspace_uri="workspace://runs/job_fixture",
    )


def make_manifest(*, native: bool = False) -> Manifest:
    generation_id = stable_id(
        "generation", job_id="job_fixture", scene_id="scene_001", provider_id="scene.dreamo" if native else "scene.flux", candidate_index=0
    )
    identity_id = stable_id("identity", generation_result_id=generation_id, provider_id="identity.native" if native else "identity.facefusion")
    evaluation_id = stable_id("evaluation", identity_result_id=identity_id, provider_id="quality.identity")
    review_id = stable_id("human_review", identity_result_id=identity_id, reviewer_id="reviewer_1")
    selection_id = stable_id("selection", identity_result_id=identity_id, policy_id="selection.v1")
    post_id = stable_id("postprocess", selection_id=selection_id, provider_id="postprocess.siax")
    delivery_id = stable_id("delivery", postprocess_id=post_id, provider_id="delivery.local")
    generation_provider = provider(
        "scene.dreamo" if native else "scene.flux",
        "scene_generator",
        identity_aware=native,
        identity_mode="reference_images" if native else None,
    )
    manifest = Manifest(
        schema=MANIFEST_SCHEMA,
        schema_version=SCHEMA_VERSION,
        manifest_id="manifest_job_fixture",
        job_id="job_fixture",
        revision=1,
        status=RuntimeStatus.RUNNING,
        quality_plan=QualityPlan(
            evaluators=[
                EvaluatorConfig(
                    provider=provider("quality.identity", "quality_evaluator"),
                    required=True,
                ),
                EvaluatorConfig(
                    provider=provider("quality.artifact", "quality_evaluator"),
                    required=False,
                ),
            ],
            human_review_required=True,
        ),
        generation_results=[
            GenerationResult(
                result_id=generation_id,
                scene_id="scene_001",
                candidate_index=0,
                status=RuntimeStatus.SUCCEEDED,
                provider=generation_provider,
                inputs={"seed": 1},
                outputs={"artifact_ids": ["art_generation"]},
            )
        ],
        identity_results=[
            IdentityResult(
                result_id=identity_id,
                generation_result_id=generation_id,
                status=RuntimeStatus.SUCCEEDED,
                provider=provider("identity.native" if native else "identity.facefusion", "identity_provider"),
                mode="native_passthrough" if native else "transformed",
                inputs={"source_artifact_id": "art_generation"},
                outputs={"artifact_ids": ["art_generation" if native else "art_identity"]},
            )
        ],
        evaluation_results=[
            EvaluationResult(
                result_id=evaluation_id,
                identity_result_id=identity_id,
                status=RuntimeStatus.SUCCEEDED,
                provider=provider("quality.identity", "quality_evaluator"),
                inputs={"artifact_id": "art_generation" if native else "art_identity"},
                metrics={"identity_similarity_mean": 0.75},
            )
        ],
        human_reviews=[
            HumanReview(
                result_id=review_id,
                identity_result_id=identity_id,
                status=RuntimeStatus.SUCCEEDED,
                provider=provider("quality.human", "human_reviewer"),
                reviewer_id="reviewer_1",
                rubric_id="portrait-review-v1",
                rubric_version="1.0",
                inputs={},
                ratings={"identity": 3, "quality": 3, "client_ready": True},
            )
        ],
        selection_decisions=[
            SelectionDecision(
                result_id=selection_id,
                identity_result_id=identity_id,
                status=SelectionStatus.SELECTED,
                provider=provider("selection.v1", "candidate_selector"),
                evaluation_result_ids=[evaluation_id],
                human_review_ids=[review_id],
            )
        ],
        postprocess_results=[
            PostProcessResult(
                result_id=post_id,
                selection_decision_id=selection_id,
                identity_result_id=identity_id,
                status=RuntimeStatus.SUCCEEDED,
                provider=provider("postprocess.siax", "postprocessor"),
                inputs={"source_identity_result_id": identity_id},
                outputs={"artifact_ids": ["art_post"]},
            )
        ],
        delivery_results=[
            DeliveryResult(
                result_id=delivery_id,
                postprocess_result_id=post_id,
                status=RuntimeStatus.SUCCEEDED,
                provider=provider("delivery.local", "delivery_provider"),
                inputs={"source_artifact_id": "art_post"},
                outputs={"artifact_ids": ["art_delivery"], "customer_filename": "ONYX_001.png"},
            )
        ],
    )
    manifest.artifacts = [
        ArtifactRecord("art_generation", "image", "generation_output", "workspace://runs/job_fixture/generation.png", generation_id),
        *(
            []
            if native
            else [ArtifactRecord("art_identity", "image", "identity_output", "workspace://runs/job_fixture/identity.png", identity_id)]
        ),
        ArtifactRecord("art_post", "image", "postprocess_output", "workspace://runs/job_fixture/post.png", post_id),
        ArtifactRecord("art_delivery", "image", "delivery_output", "workspace://final_results/job_fixture/ONYX_001.png", delivery_id),
    ]
    return manifest


class JobSpecTests(unittest.TestCase):
    def test_job_spec_serialization_round_trip(self) -> None:
        original = make_job()
        restored = loads_job_spec(dumps_job_spec(original))
        self.assertEqual(original, restored)

    def test_vip_lora_accepted(self) -> None:
        validate_job_spec(make_job(tier="vip"))

    def test_non_vip_lora_rejected(self) -> None:
        with self.assertRaisesRegex(ContractValidationError, "VIP-only"):
            validate_job_spec(make_job(tier="premium"))


class IdentityAndSeedTests(unittest.TestCase):
    def test_stable_ids_are_deterministic(self) -> None:
        first = stable_id("generation", job_id="a", scene_id="b", provider_id="c", candidate_index=0)
        second = stable_id("generation", job_id="a", scene_id="b", provider_id="c", candidate_index=0)
        self.assertEqual(first, second)

    def test_seed_is_deterministic(self) -> None:
        values = dict(base_seed=1, job_id="job", scene_id="scene", provider_id="scene.flux", candidate_index=0, stage="generation")
        self.assertEqual(derive_seed(**values), derive_seed(**values))

    def test_seed_changes_with_stable_dimensions(self) -> None:
        base = dict(base_seed=1, job_id="job", scene_id="scene", provider_id="scene.flux", candidate_index=0, stage="generation")
        changed = {**base, "candidate_index": 1}
        self.assertNotEqual(derive_seed(**base), derive_seed(**changed))

    def test_seed_golden_vector(self) -> None:
        self.assertEqual(
            918736127301361616,
            derive_seed(
                base_seed=202608260001,
                job_id="job_golden",
                scene_id="scene_007",
                provider_id="scene.flux",
                candidate_index=2,
                stage="generation",
            ),
        )

    def test_entity_specific_ids_are_deterministic(self) -> None:
        generation = generation_result_id(
            job_id="job", scene_id="scene", provider_id="scene.flux", candidate_index=0
        )
        identity = identity_result_id(
            generation_result_id=generation, provider_id="identity.facefusion"
        )
        evaluation = evaluation_result_id(
            identity_result_id=identity, provider_id="quality.identity"
        )
        postprocess = postprocess_result_id(
            selection_decision_id="sel_fixed", provider_id="postprocess.siax"
        )
        delivery = delivery_result_id(
            postprocess_result_id=postprocess, provider_id="delivery.local"
        )
        self.assertEqual(
            generation,
            generation_result_id(
                job_id="job", scene_id="scene", provider_id="scene.flux", candidate_index=0
            ),
        )
        self.assertEqual(identity, identity_result_id(generation_result_id=generation, provider_id="identity.facefusion"))
        self.assertEqual(evaluation, evaluation_result_id(identity_result_id=identity, provider_id="quality.identity"))
        self.assertEqual(postprocess, postprocess_result_id(selection_decision_id="sel_fixed", provider_id="postprocess.siax"))
        self.assertEqual(delivery, delivery_result_id(postprocess_result_id=postprocess, provider_id="delivery.local"))

    def test_multiple_identity_results_from_generation(self) -> None:
        manifest = make_manifest()
        parent = manifest.generation_results[0].result_id
        second = IdentityResult(
            result_id=stable_id("identity", generation_result_id=parent, provider_id="identity.dreamo_img2img"),
            generation_result_id=parent,
            status=RuntimeStatus.SUCCEEDED,
            provider=provider("identity.dreamo_img2img", "identity_provider"),
            mode="transformed",
            inputs={},
        )
        manifest.identity_results.append(second)
        validate_manifest(manifest)
        self.assertEqual(2, len([item for item in manifest.identity_results if item.generation_result_id == parent]))

    def test_native_passthrough_identity_result(self) -> None:
        manifest = make_manifest(native=True)
        validate_manifest(manifest)
        self.assertEqual("native_passthrough", manifest.identity_results[0].mode)
        self.assertEqual(
            manifest.generation_results[0].outputs["artifact_ids"],
            manifest.identity_results[0].outputs["artifact_ids"],
        )


class ManifestTests(unittest.TestCase):
    def test_manifest_serialization_round_trip(self) -> None:
        original = make_manifest()
        restored = loads_manifest(dumps_manifest(original))
        self.assertEqual(original, restored)

    def test_valid_parent_provenance(self) -> None:
        validate_manifest(make_manifest())

    def test_invalid_parent_provenance_rejected(self) -> None:
        manifest = make_manifest()
        manifest.identity_results[0].generation_result_id = "gen_missing"
        with self.assertRaisesRegex(ContractValidationError, "unknown generation parent"):
            validate_manifest(manifest)

    def test_postprocess_requires_selected_input(self) -> None:
        manifest = make_manifest()
        manifest.selection_decisions[0].status = SelectionStatus.REJECTED
        with self.assertRaisesRegex(ContractValidationError, "requires selected input"):
            validate_manifest(manifest)

    def test_selected_requires_client_ready_true(self) -> None:
        manifest = make_manifest()
        manifest.human_reviews[0].ratings["client_ready"] = False
        with self.assertRaisesRegex(ContractValidationError, "client_ready=true"):
            validate_manifest(manifest)

    def test_selected_accepts_completed_client_ready_review(self) -> None:
        validate_manifest(make_manifest())

    def test_required_evaluation_present_and_passing(self) -> None:
        validate_manifest(make_manifest())

    def test_required_evaluation_missing(self) -> None:
        manifest = make_manifest()
        manifest.selection_decisions[0].evaluation_result_ids.clear()
        with self.assertRaisesRegex(ContractValidationError, "missing required evaluation"):
            validate_manifest(manifest)

    def test_required_evaluation_failed(self) -> None:
        manifest = make_manifest()
        evaluation = manifest.evaluation_results[0]
        evaluation.status = RuntimeStatus.FAILED
        evaluation.error = ErrorRecord("EVALUATION_FAILED", "quality", "evaluation failed")
        with self.assertRaisesRegex(ContractValidationError, "requires succeeded evaluations"):
            validate_manifest(manifest)

    def test_optional_evaluation_missing(self) -> None:
        validate_manifest(make_manifest())

    def test_unknown_output_artifact_rejected(self) -> None:
        manifest = make_manifest()
        manifest.delivery_results[0].outputs["artifact_ids"] = ["art_missing"]
        with self.assertRaisesRegex(ContractValidationError, "references unknown artifacts"):
            validate_manifest(manifest)

    def test_output_artifacts_resolve(self) -> None:
        validate_manifest(make_manifest())

    def test_delivery_requires_successful_postprocess(self) -> None:
        manifest = make_manifest()
        manifest.postprocess_results[0].status = RuntimeStatus.FAILED
        manifest.postprocess_results[0].error = ErrorRecord(
            "POSTPROCESS_FAILED", "provider_runtime", "postprocessing failed"
        )
        with self.assertRaisesRegex(ContractValidationError, "requires succeeded postprocessing"):
            validate_manifest(manifest)

    def test_failed_runtime_result_requires_error(self) -> None:
        manifest = make_manifest()
        manifest.generation_results[0].status = RuntimeStatus.FAILED
        with self.assertRaisesRegex(ContractValidationError, "requires error"):
            validate_manifest(manifest)

    def test_succeeded_runtime_result_rejects_error(self) -> None:
        manifest = make_manifest()
        manifest.generation_results[0].error = ErrorRecord(
            "UNEXPECTED", "unknown", "should not be present"
        )
        with self.assertRaisesRegex(ContractValidationError, "must not contain error"):
            validate_manifest(manifest)

    def test_atomic_manifest_save_and_load(self) -> None:
        manifest = make_manifest()
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "manifest.json"
            save_manifest_atomic(path, manifest)
            self.assertEqual(manifest, load_manifest(path))
            self.assertFalse(path.with_name("manifest.json.writing").exists())


if __name__ == "__main__":
    unittest.main()
