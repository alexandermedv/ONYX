from __future__ import annotations

import copy
import json
import os
import sys
import tempfile
import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "engine"))

from contracts.models import (
    JOB_SPEC_SCHEMA,
    SCHEMA_VERSION,
    DeliveryConfig,
    IdentityProfile,
    JobSpec,
    ProviderRef,
    QualityPlan,
    ReferenceRecord,
    SceneGeneratorConfig,
    SceneSpec,
)
from runtime import (
    MaterializationError,
    ProviderRuntimeConfig,
    RuntimeConfig,
    dumps_runtime_config,
    load_runtime_config,
    materialize_job,
    resolve_logical_uri,
)


def provider(
    provider_id: str,
    *,
    model_id: str | None = None,
    identity_aware: bool = False,
    identity_mode: str | None = None,
) -> ProviderRef:
    return ProviderRef(
        provider_id=provider_id,
        provider_kind="scene_generator" if provider_id.startswith("scene.") else "delivery_provider",
        implementation_version="1.0",
        model_id=model_id,
        workflow_id="workflow-v1" if provider_id.startswith("scene.") else None,
        workflow_uri="repo://workflows/generator.json" if provider_id.startswith("scene.") else None,
        identity_aware=identity_aware,
        identity_mode=identity_mode,
    )


def make_job(*, tier: str = "vip", lora: bool = False, candidates: int = 2) -> JobSpec:
    generator = provider(
        "scene.flux_personal_lora" if lora else "scene.flux",
        model_id="portrait-model",
        identity_aware=lora,
        identity_mode="personal_lora" if lora else None,
    )
    return JobSpec(
        schema=JOB_SPEC_SCHEMA,
        schema_version=SCHEMA_VERSION,
        job_id="job_runtime",
        client_id="fixture-client",
        service_tier=tier,
        base_seed=12345,
        scenes=[SceneSpec(scene_id="scene_001", subject="adult portrait subject")],
        scene_generators=[
            SceneGeneratorConfig(
                provider=generator,
                candidate_count_per_scene=candidates,
                identity_profile_id="identity_fixture" if lora else None,
            )
        ],
        identity_profiles=[
            IdentityProfile(
                profile_id="identity_fixture",
                client_profile_uri="client://fixture-client/profile/client_profile.json",
                references=[ReferenceRecord("ref_001", "client://fixture-client/source/ref.png", "primary")],
            )
        ],
        quality_plan=QualityPlan(human_review_required=True),
        delivery=DeliveryConfig(
            provider=provider("delivery.local"),
            destination_uri="workspace://delivery/job_runtime",
        ),
        workspace_uri="workspace://jobs/job_runtime",
    )


def make_runtime(root: Path, *, provider_id: str = "scene.flux") -> RuntimeConfig:
    return RuntimeConfig(
        schema="onyx.runtime_config",
        schema_version="1.0",
        machine_id="test-machine",
        repo_root=str(root / "repo"),
        workspace_root=str(root / "workspace"),
        client_root=str(root / "clients"),
        providers={
            provider_id: ProviderRuntimeConfig(
                endpoint="http://127.0.0.1:8188",
                model_roots={"checkpoints": str(root / "models")},
                models={"portrait-model": "model://checkpoints/portrait.safetensors"},
            ),
            "delivery.local": ProviderRuntimeConfig(),
        },
    )


class RuntimeConfigTests(unittest.TestCase):
    def test_runtime_config_serialization_and_loading(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            original = make_runtime(root)
            path = root / "runtime.json"
            path.write_text(dumps_runtime_config(original), encoding="utf-8")
            self.assertEqual(original, load_runtime_config(path))

    def test_example_config_parses(self) -> None:
        config = load_runtime_config(ROOT / "config" / "runtime.example.json")
        self.assertEqual("example-windows-workstation", config.machine_id)
        self.assertIn("scene.flux", config.providers)

    def test_environment_selects_alternative_config(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            path = root / "selected.json"
            path.write_text(dumps_runtime_config(make_runtime(root)), encoding="utf-8")
            with patch.dict(os.environ, {"ONYX_RUNTIME_CONFIG": str(path)}):
                self.assertEqual("test-machine", load_runtime_config().machine_id)

    def test_windows_style_paths_parse(self) -> None:
        config = load_runtime_config(ROOT / "config" / "runtime.example.json")
        self.assertEqual(r"D:\AI\ONYX", config.repo_root)


class LogicalUriTests(unittest.TestCase):
    def test_client_workspace_and_repo_resolution(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            runtime = make_runtime(Path(folder))
            self.assertEqual(
                str((Path(folder) / "clients" / "client-a" / "source" / "ref.png").resolve()),
                resolve_logical_uri("client://client-a/source/ref.png", runtime),
            )
            self.assertEqual(
                str((Path(folder) / "workspace" / "jobs" / "one").resolve()),
                resolve_logical_uri("workspace://jobs/one", runtime),
            )
            self.assertEqual(
                str((Path(folder) / "repo" / "workflows" / "one.json").resolve()),
                resolve_logical_uri("repo://workflows/one.json", runtime),
            )

    def test_model_resolution_uses_provider_root(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            runtime = make_runtime(Path(folder))
            self.assertEqual(
                str((Path(folder) / "models" / "portrait.safetensors").resolve()),
                resolve_logical_uri(
                    "model://checkpoints/portrait.safetensors",
                    runtime,
                    provider_id="scene.flux",
                ),
            )

    def test_traversal_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            runtime = make_runtime(Path(folder))
            unsafe = (
                "client://../../outside",
                "workspace://jobs/%2e%2e/outside",
                "repo://workflows/%2Foutside",
            )
            for uri in unsafe:
                with self.subTest(uri=uri), self.assertRaises(MaterializationError):
                    resolve_logical_uri(uri, runtime)

    def test_absolute_and_windows_drive_injection_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            runtime = make_runtime(Path(folder))
            unsafe = (
                "client:///absolute/path",
                "workspace:////server/share",
                "repo://C:/Windows/System32",
                "client://C%3A/outside",
                "model://C:/outside.bin",
            )
            for uri in unsafe:
                with self.subTest(uri=uri), self.assertRaises(MaterializationError):
                    resolve_logical_uri(uri, runtime, provider_id="scene.flux")


class MaterializationTests(unittest.TestCase):
    def test_job_is_not_mutated(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            job = make_job()
            before = copy.deepcopy(job)
            before_bytes = json.dumps(job.to_dict(), sort_keys=True, separators=(",", ":"))
            materialize_job(job, make_runtime(Path(folder)))
            self.assertEqual(before, job)
            self.assertEqual(
                before_bytes,
                json.dumps(job.to_dict(), sort_keys=True, separators=(",", ":")),
            )

    def test_execution_plan_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            job = make_job()
            runtime = make_runtime(Path(folder))
            self.assertEqual(materialize_job(job, runtime), materialize_job(job, runtime))

    def test_execution_plan_is_frozen(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            plan = materialize_job(make_job(), make_runtime(Path(folder)))
            with self.assertRaises(FrozenInstanceError):
                plan.machine_id = "other-machine"

    def test_generation_task_contains_canonical_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            job = make_job(candidates=1)
            job.scenes[0].prompt["lighting"] = "soft daylight"
            job.scene_generators[0].parameters["steps"] = 20
            task = materialize_job(job, make_runtime(Path(folder))).generation_tasks[0]
            materialized = task.to_dict()
            self.assertEqual("soft daylight", materialized["scene_inputs"]["prompt"]["lighting"])
            self.assertEqual(20, materialized["provider_parameters"]["steps"])

    def test_identity_profile_and_reference_are_resolved(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            plan = materialize_job(make_job(), make_runtime(Path(folder)))
            self.assertTrue(plan.identity_profiles[0].client_profile_path.endswith("client_profile.json"))
            self.assertTrue(plan.identity_references[0].resolved_path.endswith("ref.png"))

    def test_generation_seeds_are_canonical_and_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            runtime = make_runtime(Path(folder))
            plan = materialize_job(make_job(), runtime)
            repeated = materialize_job(make_job(), runtime)
            self.assertEqual(plan.generation_tasks[0].seed, repeated.generation_tasks[0].seed)
            self.assertNotEqual(plan.generation_tasks[0].seed, plan.generation_tasks[1].seed)

    def test_changing_provider_changes_seed(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            flux = materialize_job(make_job(candidates=1), make_runtime(root)).generation_tasks[0].seed
            other_job = make_job(candidates=1)
            other_job.scene_generators[0].provider.provider_id = "scene.other"
            other = materialize_job(
                other_job,
                make_runtime(root, provider_id="scene.other"),
            ).generation_tasks[0].seed
            self.assertNotEqual(flux, other)

    def test_enabled_provider_requires_runtime_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            runtime = make_runtime(Path(folder))
            del runtime.providers["scene.flux"]
            with self.assertRaisesRegex(MaterializationError, "Missing runtime mapping"):
                materialize_job(make_job(), runtime)

    def test_unused_provider_does_not_require_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            job = make_job()
            job.scene_generators.append(
                SceneGeneratorConfig(provider=provider("scene.unused"), enabled=False)
            )
            materialize_job(job, make_runtime(Path(folder)))

    def test_vip_lora_materializes(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            plan = materialize_job(
                make_job(lora=True),
                make_runtime(root, provider_id="scene.flux_personal_lora"),
            )
            self.assertEqual("scene.flux_personal_lora", plan.generation_tasks[0].provider_id)

    def test_non_vip_lora_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaisesRegex(ValueError, "VIP-only"):
                materialize_job(
                    make_job(tier="premium", lora=True),
                    make_runtime(Path(folder), provider_id="scene.flux_personal_lora"),
                )

    def test_snapshot_is_json_serializable(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            plan = materialize_job(make_job(), make_runtime(Path(folder)))
            json.dumps(plan.resolved_runtime_snapshot())

    def test_snapshot_excludes_unrelated_provider_secrets(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            runtime = make_runtime(Path(folder))
            runtime.providers["unused.remote"] = ProviderRuntimeConfig(
                metadata={"api_token": "must-not-leak"}
            )
            snapshot = materialize_job(make_job(), runtime).resolved_runtime_snapshot()
            serialized = json.dumps(snapshot)
            self.assertNotIn("unused.remote", serialized)
            self.assertNotIn("must-not-leak", serialized)

    def test_materialization_has_no_external_side_effects(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            plan = materialize_job(make_job(), make_runtime(root))
            self.assertFalse((root / "workspace").exists())
            self.assertFalse(Path(plan.workspace_path).exists())


if __name__ == "__main__":
    unittest.main()
