from __future__ import annotations

import hashlib
import io
import json
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "engine"))

from contracts.models import (
    JOB_SPEC_SCHEMA,
    SCHEMA_VERSION,
    JobSpec,
    ProviderRef,
    QualityPlan,
    SceneGeneratorConfig,
    SceneSpec,
)
from contracts.validation import validate_manifest
from runtime import (
    FluxSceneGenerator,
    MaterializedProvider,
    ProviderRuntimeConfig,
    RuntimeConfig,
    SceneGeneratorRequest,
    materialize_job,
    run_generation_plan,
)


WORKFLOW_SOURCE = ROOT / "engine" / "flux_scene_generator" / "ONYX_Flux_Scene_Generator_0.3_API.json"
WORKFLOW_HASH = hashlib.sha256(WORKFLOW_SOURCE.read_bytes()).hexdigest()
PNG_BYTES = b"\x89PNG\r\n\x1a\ncanonical-test-image"


class FakeResponse:
    def __init__(self, payload: bytes) -> None:
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def read(self) -> bytes:
        return self.payload


class FakeTransport:
    def __init__(self, *, history=None, view=PNG_BYTES, prompt_id="prompt-123") -> None:
        self.history = history if history is not None else successful_history(prompt_id)
        self.view = view
        self.prompt_id = prompt_id
        self.requests = []
        self.failures: dict[str, Exception] = {}

    def __call__(self, request, timeout):
        self.requests.append((request, timeout))
        url = request.full_url
        for fragment, error in self.failures.items():
            if fragment in url:
                raise error
        if url.endswith("/prompt"):
            return FakeResponse(json.dumps({"prompt_id": self.prompt_id}).encode())
        if "/history/" in url:
            payload = self.history() if callable(self.history) else self.history
            return FakeResponse(json.dumps(payload).encode())
        if "/view?" in url:
            return FakeResponse(self.view)
        raise AssertionError(f"Unexpected URL: {url}")

    @property
    def post_requests(self):
        return [item for item, _ in self.requests if item.full_url.endswith("/prompt")]

    @property
    def history_requests(self):
        return [item for item, _ in self.requests if "/history/" in item.full_url]

    @property
    def view_requests(self):
        return [item for item, _ in self.requests if "/view?" in item.full_url]

    def submitted_workflow(self):
        payload = json.loads(self.post_requests[0].data.decode())
        return payload["prompt"]


class FakeClock:
    def __init__(self) -> None:
        self.value = 0.0
        self.sleeps = []

    def __call__(self) -> float:
        return self.value

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        self.value += seconds


def successful_history(prompt_id="prompt-123", *, images=None, node_id="9"):
    if images is None:
        images = [{"filename": "flux_00001_.png", "subfolder": "ONYX/test", "type": "output"}]
    return {
        prompt_id: {
            "status": {"status_str": "success", "completed": True},
            "outputs": {node_id: {"images": images}},
        }
    }


def http_error(url: str, status: int) -> urllib.error.HTTPError:
    return urllib.error.HTTPError(url, status, "test", {}, io.BytesIO(b"rejected"))


class FluxFixture:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.workflow = root / "workflow.json"
        self.workflow.write_bytes(WORKFLOW_SOURCE.read_bytes())
        self.model = root / "models" / "diffusion_models" / "flux1-dev.safetensors"
        self.model.parent.mkdir(parents=True)
        self.model.write_bytes(b"not-a-real-model")
        self.output = root / "workspace" / "generation" / "scene.flux" / "scene_001" / "candidate_000"

    def provider(self, **changes) -> MaterializedProvider:
        values = {
            "provider_id": "scene.flux",
            "provider_kind": "scene_generator",
            "implementation_version": "flux-adapter-v1",
            "model_id": "flux1-dev",
            "workflow_id": "onyx-flux-0.3-api",
            "workflow_hash": WORKFLOW_HASH,
            "endpoint": "http://comfy.test:8188",
            "workflow_path": str(self.workflow),
            "model_path": str(self.model),
            "capabilities": ("comfyui_api",),
            "runtime_metadata_json": json.dumps(
                {
                    "request_timeout_seconds": 2,
                    "generation_timeout_seconds": 3,
                    "poll_interval_seconds": 1,
                }
            ),
        }
        values.update(changes)
        return MaterializedProvider(**values)

    def request(self, **changes) -> SceneGeneratorRequest:
        values = {
            "generation_result_id": "generation-result-123",
            "job_id": "job_flux_test",
            "scene_id": "scene_001",
            "provider_id": "scene.flux",
            "candidate_index": 0,
            "seed": 912345678901,
            "output_path": str(self.output),
            "scene_inputs_json": json.dumps(
                {
                    "subject": "one adult",
                    "prompt": {"text": "exact canonical prompt"},
                    "explicit_prompts": {"scene.flux": "explicit FLUX prompt"},
                }
            ),
            "provider_parameters_json": json.dumps(
                {
                    "width": 768,
                    "height": 1024,
                    "steps": 12,
                    "cfg": 1.5,
                    "sampler_name": "euler",
                    "scheduler": "simple",
                    "denoise": 0.9,
                }
            ),
            "provider": self.provider(),
        }
        values.update(changes)
        return SceneGeneratorRequest(**values)


class WorkflowAndSubmissionTests(unittest.TestCase):
    def test_exact_seed_prompt_dimensions_and_parameters_are_submitted(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            fixture = FluxFixture(Path(folder))
            transport = FakeTransport()
            request = fixture.request()
            result = FluxSceneGenerator(opener=transport).execute(request)
            self.assertTrue(result.succeeded)
            workflow = transport.submitted_workflow()
            self.assertEqual(request.seed, workflow["56:58"]["inputs"]["seed"])
            self.assertEqual("explicit FLUX prompt", workflow["56:51"]["inputs"]["text"])
            self.assertEqual(768, workflow["56:50"]["inputs"]["width"])
            self.assertEqual(1024, workflow["56:50"]["inputs"]["height"])
            self.assertEqual(1, workflow["56:50"]["inputs"]["batch_size"])
            for key, expected in {
                "steps": 12,
                "cfg": 1.5,
                "sampler_name": "euler",
                "scheduler": "simple",
                "denoise": 0.9,
            }.items():
                self.assertEqual(expected, workflow["56:58"]["inputs"][key])

    def test_prompt_text_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            fixture = FluxFixture(Path(folder))
            transport = FakeTransport()
            request = fixture.request(
                scene_inputs_json=json.dumps({"prompt": {"text": "fallback prompt"}})
            )
            result = FluxSceneGenerator(opener=transport).execute(request)
            self.assertTrue(result.succeeded)
            self.assertEqual("fallback prompt", transport.submitted_workflow()["56:51"]["inputs"]["text"])

    def test_invalid_prompt_and_parameters_submit_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            fixture = FluxFixture(Path(folder))
            for changes in (
                {"scene_inputs_json": json.dumps({"prompt": {}})},
                {"provider_parameters_json": json.dumps({"batch_size": 2})},
                {"provider_parameters_json": json.dumps({"width": 65})},
                {"scene_inputs_json": json.dumps([])},
                {"provider_parameters_json": json.dumps([])},
            ):
                transport = FakeTransport()
                result = FluxSceneGenerator(opener=transport).execute(fixture.request(**changes))
                self.assertEqual("INVALID_SCENE_INPUT", result.error.code)
                self.assertEqual([], transport.requests)

    def test_actual_workflow_file_and_hash_are_used(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            fixture = FluxFixture(Path(folder))
            transport = FakeTransport()
            result = FluxSceneGenerator(opener=transport).execute(fixture.request())
            self.assertTrue(result.succeeded)
            metadata = json.loads(result.metadata_json)
            self.assertEqual(WORKFLOW_HASH, metadata["actual_workflow_sha256"])

    def test_hash_or_node_mismatch_submits_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            fixture = FluxFixture(Path(folder))
            transport = FakeTransport()
            bad_provider = fixture.provider(workflow_hash="0" * 64)
            result = FluxSceneGenerator(opener=transport).execute(
                fixture.request(provider=bad_provider)
            )
            self.assertEqual("WORKFLOW_INVALID", result.error.code)
            self.assertEqual([], transport.requests)

            workflow = json.loads(fixture.workflow.read_text(encoding="utf-8"))
            workflow["56:51"]["class_type"] = "WrongNode"
            fixture.workflow.write_text(json.dumps(workflow), encoding="utf-8")
            provider = fixture.provider(workflow_hash=None)
            result = FluxSceneGenerator(opener=transport).execute(
                fixture.request(provider=provider)
            )
            self.assertEqual("WORKFLOW_INVALID", result.error.code)
            self.assertEqual([], transport.requests)

    def test_materialized_model_filename_is_patched(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            fixture = FluxFixture(Path(folder))
            mapped = fixture.model.with_name("mapped-flux.safetensors")
            mapped.write_bytes(b"mapped")
            transport = FakeTransport()
            result = FluxSceneGenerator(opener=transport).execute(
                fixture.request(provider=fixture.provider(model_path=str(mapped)))
            )
            self.assertTrue(result.succeeded)
            self.assertEqual(
                "mapped-flux.safetensors",
                transport.submitted_workflow()["56:48"]["inputs"]["unet_name"],
            )

    def test_post_prompt_occurs_exactly_once_and_captures_id(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            fixture = FluxFixture(Path(folder))
            transport = FakeTransport(prompt_id="captured-id")
            result = FluxSceneGenerator(opener=transport).execute(fixture.request())
            self.assertTrue(result.succeeded)
            self.assertEqual(1, len(transport.post_requests))
            self.assertEqual("captured-id", json.loads(result.metadata_json)["comfyui_prompt_id"])


class HistoryAndOutputTests(unittest.TestCase):
    def test_relative_output_subfolders_normalize_to_posix_form(self) -> None:
        from runtime.flux_scene_generator import _normalized_subfolder

        cases = {
            "ONYX_Canonical": "ONYX_Canonical",
            "ONYX_Canonical/phase_test": "ONYX_Canonical/phase_test",
            "ONYX_Canonical\\phase_test": "ONYX_Canonical/phase_test",
            "nested\\windows\\subfolder": "nested/windows/subfolder",
        }
        for subfolder, expected in cases.items():
            with self.subTest(subfolder=subfolder):
                self.assertEqual(expected, _normalized_subfolder(subfolder))

    def test_unsafe_output_subfolders_remain_rejected(self) -> None:
        from runtime.flux_scene_generator import FluxOutputSafetyError, _normalized_subfolder

        unsafe = (
            "../escape",
            "..\\escape",
            "foo/../../escape",
            "foo\\..\\..\\escape",
            "C:\\escape",
            "C:/escape",
            "\\\\server\\share",
            "//server/share",
            "\\escape",
            "/escape",
        )
        for subfolder in unsafe:
            with self.subTest(subfolder=subfolder), self.assertRaises(FluxOutputSafetyError):
                _normalized_subfolder(subfolder)

    def test_polling_uses_only_returned_prompt_and_exact_view_descriptor(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            fixture = FluxFixture(Path(folder))
            calls = 0

            def histories():
                nonlocal calls
                calls += 1
                if calls == 1:
                    return {"unrelated": successful_history()["prompt-123"]}
                return successful_history("prompt-123")

            clock = FakeClock()
            transport = FakeTransport(history=histories)
            result = FluxSceneGenerator(
                opener=transport, clock=clock, sleeper=clock.sleep
            ).execute(fixture.request())
            self.assertTrue(result.succeeded)
            self.assertEqual(2, len(transport.history_requests))
            self.assertTrue(all(item.full_url.endswith("/history/prompt-123") for item in transport.history_requests))
            self.assertEqual(1, len(transport.view_requests))
            query = transport.view_requests[0].full_url
            self.assertIn("filename=flux_00001_.png", query)
            self.assertIn("subfolder=ONYX%2Ftest", query)
            self.assertIn("type=output", query)

    def test_execution_failure(self) -> None:
        history = {
            "prompt-123": {
                "status": {"status_str": "error", "completed": False, "messages": ["failed"]},
                "outputs": {},
            }
        }
        with tempfile.TemporaryDirectory() as folder:
            fixture = FluxFixture(Path(folder))
            result = FluxSceneGenerator(opener=FakeTransport(history=history)).execute(fixture.request())
            self.assertEqual("EXECUTION_FAILED", result.error.code)

    def test_timeout_is_deterministic_and_does_not_resubmit(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            fixture = FluxFixture(Path(folder))
            transport = FakeTransport(history={})
            clock = FakeClock()
            result = FluxSceneGenerator(
                opener=transport, clock=clock, sleeper=clock.sleep
            ).execute(fixture.request())
            self.assertEqual("GENERATION_TIMEOUT", result.error.code)
            self.assertFalse(result.error.retryable)
            self.assertEqual(1, len(transport.post_requests))
            self.assertEqual([1, 1, 1], clock.sleeps)

    def test_incomplete_history_keeps_polling(self) -> None:
        calls = 0

        def histories():
            nonlocal calls
            calls += 1
            if calls == 1:
                return {
                    "prompt-123": {
                        "status": {"status_str": "running", "completed": False},
                        "outputs": {},
                    }
                }
            return successful_history()

        with tempfile.TemporaryDirectory() as folder:
            fixture = FluxFixture(Path(folder))
            clock = FakeClock()
            result = FluxSceneGenerator(
                opener=FakeTransport(history=histories), clock=clock, sleeper=clock.sleep
            ).execute(fixture.request())
            self.assertTrue(result.succeeded)
            self.assertEqual(2, calls)

    def test_malformed_history(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            fixture = FluxFixture(Path(folder))
            result = FluxSceneGenerator(
                opener=FakeTransport(history={"prompt-123": {"outputs": {}}})
            ).execute(fixture.request())
            self.assertEqual("MALFORMED_HISTORY", result.error.code)

    def test_missing_multiple_and_unrelated_node_outputs(self) -> None:
        cases = (
            (successful_history(images=[]), "MISSING_OUTPUT"),
            (
                successful_history(
                    images=[
                        {"filename": "one.png", "subfolder": "", "type": "output"},
                        {"filename": "two.png", "subfolder": "", "type": "output"},
                    ]
                ),
                "MISSING_OUTPUT",
            ),
            (successful_history(node_id="other"), "MISSING_OUTPUT"),
        )
        with tempfile.TemporaryDirectory() as folder:
            fixture = FluxFixture(Path(folder))
            for history, code in cases:
                result = FluxSceneGenerator(opener=FakeTransport(history=history)).execute(fixture.request())
                self.assertEqual(code, result.error.code)

    def test_output_descriptor_cannot_escape_local_path(self) -> None:
        unsafe = [
            {"filename": "../escape.png", "subfolder": "", "type": "output"},
            {"filename": "safe.png", "subfolder": "../escape", "type": "output"},
            {"filename": "safe.png", "subfolder": "%2e%2e/escape", "type": "output"},
            {"filename": "%2e%2e%2fescape.png", "subfolder": "", "type": "output"},
            {"filename": "safe.png", "subfolder": "safe%5cescape", "type": "output"},
            {"filename": "safe.png", "subfolder": "C:/escape", "type": "output"},
        ]
        with tempfile.TemporaryDirectory() as folder:
            fixture = FluxFixture(Path(folder))
            for descriptor in unsafe:
                transport = FakeTransport(history=successful_history(images=[descriptor]))
                result = FluxSceneGenerator(opener=transport).execute(fixture.request())
                self.assertEqual("OUTPUT_PATH_UNSAFE", result.error.code)
                self.assertEqual([], transport.view_requests)
                self.assertFalse(fixture.output.exists())

    def test_success_writes_one_task_local_artifact_atomically(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            fixture = FluxFixture(Path(folder))
            replacements = []
            from runtime import flux_scene_generator as module

            real_replace = module.os.replace

            def observed_replace(source, destination):
                self.assertTrue(Path(source).is_file())
                self.assertTrue(str(Path(source)).startswith(str(fixture.output)))
                replacements.append((Path(source), Path(destination)))
                real_replace(source, destination)

            with patch.object(module.os, "replace", observed_replace):
                result = FluxSceneGenerator(opener=FakeTransport()).execute(fixture.request())
            self.assertTrue(result.succeeded)
            self.assertEqual(1, len(result.artifacts))
            artifact = Path(result.artifacts[0].resolved_path)
            self.assertEqual(fixture.output, artifact.parent)
            self.assertEqual(PNG_BYTES, artifact.read_bytes())
            self.assertEqual(1, len(replacements))
            self.assertFalse(replacements[0][0].exists())


class FailureMappingTests(unittest.TestCase):
    def test_invalid_provider_workflow_and_model(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            fixture = FluxFixture(Path(folder))
            cases = (
                (fixture.provider(endpoint=None), "INVALID_PROVIDER_CONFIG"),
                (fixture.provider(workflow_path=str(fixture.root / "missing.json")), "WORKFLOW_NOT_FOUND"),
                (fixture.provider(model_path=str(fixture.root / "missing-model")), "INVALID_PROVIDER_CONFIG"),
            )
            for provider, expected in cases:
                transport = FakeTransport()
                result = FluxSceneGenerator(opener=transport).execute(fixture.request(provider=provider))
                self.assertEqual(expected, result.error.code)
                self.assertEqual([], transport.requests)

    def test_connection_failure_and_post_rejection_are_not_retried(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            fixture = FluxFixture(Path(folder))
            unavailable = FakeTransport()
            unavailable.failures["/prompt"] = urllib.error.URLError("offline")
            result = FluxSceneGenerator(opener=unavailable).execute(fixture.request())
            self.assertEqual("COMFYUI_UNAVAILABLE", result.error.code)
            self.assertEqual(1, len(unavailable.post_requests))

            rejected = FakeTransport()
            rejected.failures["/prompt"] = http_error("http://comfy.test/prompt", 400)
            result = FluxSceneGenerator(opener=rejected).execute(fixture.request())
            self.assertEqual("WORKFLOW_REJECTED", result.error.code)
            self.assertEqual(1, len(rejected.post_requests))

            malformed = FakeTransport()
            malformed.prompt_id = "unused"

            def malformed_open(request, timeout):
                malformed.requests.append((request, timeout))
                return FakeResponse(b"not-json")

            result = FluxSceneGenerator(opener=malformed_open).execute(fixture.request())
            self.assertEqual("WORKFLOW_REJECTED", result.error.code)
            self.assertEqual(1, len(malformed.post_requests))

    def test_http_server_error_and_view_failure(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            fixture = FluxFixture(Path(folder))
            server_error = FakeTransport()
            server_error.failures["/history/"] = http_error("http://comfy.test/history", 503)
            result = FluxSceneGenerator(opener=server_error).execute(fixture.request())
            self.assertEqual("COMFYUI_HTTP_ERROR", result.error.code)
            self.assertTrue(result.error.retryable)

            view_error = FakeTransport()
            view_error.failures["/view?"] = urllib.error.URLError("download failed")
            result = FluxSceneGenerator(opener=view_error).execute(fixture.request())
            self.assertEqual("OUTPUT_DOWNLOAD_FAILED", result.error.code)
            metadata = json.loads(result.metadata_json)
            self.assertEqual("output download", metadata["operation"])

    def test_history_transport_failure_preserves_submission_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            fixture = FluxFixture(Path(folder))
            transport = FakeTransport(prompt_id="submitted-before-disconnect")
            transport.failures["/history/"] = urllib.error.URLError("connection lost")

            result = FluxSceneGenerator(opener=transport).execute(fixture.request())

            self.assertEqual("COMFYUI_UNAVAILABLE", result.error.code)
            self.assertEqual(1, len(transport.post_requests))
            metadata = json.loads(result.metadata_json)
            self.assertEqual("submitted-before-disconnect", metadata["comfyui_prompt_id"])
            self.assertEqual(912345678901, metadata["submitted_seed"])
            self.assertEqual(WORKFLOW_HASH, metadata["actual_workflow_sha256"])
            self.assertEqual("history polling for submitted-before-disconnect", metadata["operation"])
            self.assertEqual("http://comfy.test:8188", metadata["endpoint"])


class OrchestratorIntegrationTests(unittest.TestCase):
    def _context(self, root: Path):
        model_root = root / "models" / "diffusion_models"
        model_root.mkdir(parents=True)
        (model_root / "flux1-dev.safetensors").write_bytes(b"fake")
        job = JobSpec(
            schema=JOB_SPEC_SCHEMA,
            schema_version=SCHEMA_VERSION,
            job_id="job_flux_integration",
            client_id="fixture-client",
            service_tier="mass",
            base_seed=20260826,
            scenes=[
                SceneSpec(
                    scene_id="scene_001",
                    subject="one adult",
                    explicit_prompts={"scene.flux": "integration prompt"},
                )
            ],
            scene_generators=[
                SceneGeneratorConfig(
                    provider=ProviderRef(
                        provider_id="scene.flux",
                        provider_kind="scene_generator",
                        implementation_version="flux-adapter-v1",
                        model_id="flux1-dev",
                        workflow_id="onyx-flux-0.3-api",
                        workflow_version="0.3",
                        workflow_uri="repo://engine/flux_scene_generator/ONYX_Flux_Scene_Generator_0.3_API.json",
                        workflow_hash=WORKFLOW_HASH,
                    ),
                    parameters={"width": 768, "height": 1024},
                )
            ],
            quality_plan=QualityPlan(human_review_required=True),
            workspace_uri="workspace://jobs/job_flux_integration",
        )
        runtime = RuntimeConfig(
            schema="onyx.runtime_config",
            schema_version="1.0",
            machine_id="cpu-flux-test",
            repo_root=str(ROOT),
            workspace_root=str(root / "workspace"),
            client_root=str(root / "clients"),
            providers={
                "scene.flux": ProviderRuntimeConfig(
                    endpoint="http://comfy.test:8188",
                    model_roots={"diffusion_models": str(model_root)},
                    models={"flux1-dev": "model://diffusion_models/flux1-dev.safetensors"},
                    capabilities=("comfyui_api",),
                    metadata={"generation_timeout_seconds": 3, "poll_interval_seconds": 1},
                )
            },
        )
        plan = materialize_job(job, runtime)
        manifest_path = Path(plan.workspace_path) / "manifest.json"
        return job, plan, manifest_path

    def test_canonical_chain_and_seed_proof(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            job, plan, manifest_path = self._context(Path(folder))
            transport = FakeTransport()
            manifest = run_generation_plan(
                job,
                plan,
                manifest_path,
                {"scene.flux": FluxSceneGenerator(opener=transport)},
                max_attempts_per_task=1,
            )
            validate_manifest(manifest)
            result = manifest.generation_results[0]
            attempt = manifest.attempts[0]
            artifact = manifest.artifacts[0]
            submitted_seed = transport.submitted_workflow()["56:58"]["inputs"]["seed"]
            self.assertEqual(plan.generation_tasks[0].seed, submitted_seed)
            self.assertEqual(submitted_seed, result.inputs["seed"])
            self.assertEqual(submitted_seed, attempt.runtime["submitted_seed"])
            self.assertEqual(transport.prompt_id, attempt.runtime["comfyui_prompt_id"])
            self.assertEqual(result.outputs["artifact_ids"], [artifact.artifact_id])
            self.assertEqual(result.result_id, artifact.created_by_id)
            self.assertEqual(hashlib.sha256(PNG_BYTES).hexdigest(), artifact.sha256)
            self.assertEqual(len(PNG_BYTES), artifact.size_bytes)

    def test_resume_and_missing_artifact_remain_orchestrator_owned(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            job, plan, manifest_path = self._context(Path(folder))
            first_transport = FakeTransport()
            first = run_generation_plan(
                job, plan, manifest_path, {"scene.flux": FluxSceneGenerator(opener=first_transport)}
            )
            self.assertEqual(1, len(first_transport.post_requests))

            resumed_transport = FakeTransport()
            resumed = run_generation_plan(
                job, plan, manifest_path, {"scene.flux": FluxSceneGenerator(opener=resumed_transport)}
            )
            self.assertEqual(0, len(resumed_transport.post_requests))
            self.assertEqual(1, len(resumed.attempts))

            Path(first.artifacts[0].resolved_path).unlink()
            retry_transport = FakeTransport(prompt_id="retry-prompt")
            retried = run_generation_plan(
                job, plan, manifest_path, {"scene.flux": FluxSceneGenerator(opener=retry_transport)}
            )
            self.assertEqual(1, len(retry_transport.post_requests))
            self.assertEqual(2, len(retried.attempts))
            self.assertEqual(1, len(retried.generation_results))
            self.assertEqual(
                retried.attempts[0].result_id,
                retried.attempts[1].result_id,
            )


if __name__ == "__main__":
    unittest.main()
