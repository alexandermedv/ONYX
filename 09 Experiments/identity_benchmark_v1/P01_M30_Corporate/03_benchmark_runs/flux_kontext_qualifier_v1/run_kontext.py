"""Run the bounded three-scene P01 FLUX.1 Kontext Dev qualifier."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import sys
import threading
import time
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image

ROOT = Path(__file__).resolve().parents[5]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.production_pilot.runner import memory_snapshot
from engine.runtime.comfyui_client import ComfyUIClient

RUN_ROOT = Path(__file__).resolve().parent
PLAN_PATH = RUN_ROOT / "run_plan.json"
TEMPLATE_PATH = RUN_ROOT / "workflow_template_api.json"
BUS01_PATH = RUN_ROOT.parent / "checkpoint_benchmark_v1" / "run_plan.json"
SCENES_PATH = RUN_ROOT.parent / "pulid_multiscene_v1" / "scene_specs.json"
REF_PATH = RUN_ROOT.parent.parent / "01_references" / "P01_REF01_frontal.png"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".writing")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class GpuMonitor:
    def __init__(self) -> None:
        self.stop = threading.Event()
        self.samples: list[dict[str, Any]] = []
        self.thread = threading.Thread(target=self._run, daemon=True)

    def _run(self) -> None:
        while not self.stop.is_set():
            try:
                self.samples.append(memory_snapshot())
            except Exception as exc:
                self.samples.append({"timestamp": utc_now(), "telemetry_error": repr(exc)})
            self.stop.wait(2)

    def __enter__(self) -> "GpuMonitor":
        self.thread.start()
        return self

    def __exit__(self, *_: object) -> None:
        self.stop.set()
        self.thread.join(timeout=5)

    def peak_gpu_used_mib(self) -> int | None:
        values = [sample.get("gpu", {}).get("used_mib") for sample in self.samples]
        values = [value for value in values if isinstance(value, int)]
        return max(values) if values else None


def free_models(client: ComfyUIClient) -> None:
    request = urllib.request.Request(
        client.endpoint + "/free",
        data=json.dumps({"unload_models": True, "free_memory": True}).encode("utf-8"),
        headers={"Content-Type": "application/json", "Connection": "close"},
    )
    client._open(request, operation="model release")


def canonical_scenes(plan: dict[str, Any]) -> dict[str, dict[str, Any]]:
    bus01 = read_json(BUS01_PATH)["scene"]
    sibling = {item["scene_id"]: item for item in read_json(SCENES_PATH)["scenes"]}
    result = {"BUS_01": {"scene_id": "BUS_01", "prompt": bus01["canonical_prompt"], "source_name": "Classic Business Headshot"}}
    result.update({scene_id: sibling[scene_id] for scene_id in ("BUS_06", "BUS_09")})
    expected = {item["scene_id"]: item["seed"] for item in plan["scenes"]}
    bus01_seed = read_json(BUS01_PATH)["generation"]["seed"]
    if set(result) != set(expected) or bus01_seed != expected["BUS_01"] or any(sibling[key]["seed"] != expected[key] for key in ("BUS_06", "BUS_09")):
        raise ValueError("unexpected qualifier scene set")
    return result


def validate_contract(plan: dict[str, Any], template: dict[str, Any]) -> dict[str, dict[str, Any]]:
    if not REF_PATH.is_file() or sha256(REF_PATH).lower() != plan["identity"]["primary_reference_sha256"]:
        raise ValueError("canonical primary reference is unavailable or hash-mismatched")
    for path in (BUS01_PATH, SCENES_PATH, Path(plan["model"]["unet_path"])):
        if not path.is_file():
            raise FileNotFoundError(path)
    expected = plan["generation"]
    sampler = template["12"]["inputs"]
    if (sampler["steps"], sampler["cfg"], sampler["sampler_name"], sampler["scheduler"], sampler["denoise"]) != (expected["steps"], expected["cfg"], expected["sampler_name"], expected["scheduler"], expected["denoise"]):
        raise ValueError("template sampler contract differs from the existing Kontext workflow")
    if template["10"]["inputs"]["guidance"] != expected["guidance"]:
        raise ValueError("template guidance differs from existing Kontext workflow")
    required = {"LoadImage", "ImageStitch", "FluxKontextImageScale", "VAEEncode", "ReferenceLatent", "FluxGuidance", "KSampler", "SaveImage"}
    if not required.issubset({node["class_type"] for node in template.values()}):
        raise ValueError("template no longer represents the reused one-reference Kontext graph")
    return canonical_scenes(plan)


def render(template: dict[str, Any], plan: dict[str, Any], scene: dict[str, Any], seed: int) -> dict[str, Any]:
    workflow = copy.deepcopy(template)
    canonical_prompt = scene["prompt"]
    prompt = f"Place the same adult man in this scene: {canonical_prompt} Preserve his facial features, apparent age, bald head, natural skin texture, identity, and photorealistic quality. Do not add other people."
    workflow["1"]["inputs"]["image"] = plan["identity"]["comfy_input"]
    workflow["8"]["inputs"]["text"] = prompt
    workflow["12"]["inputs"]["seed"] = seed
    workflow["14"]["inputs"]["filename_prefix"] = f"P01_{scene['scene_id']}_KONTEXT"
    return workflow


def validate_png(path: Path) -> dict[str, Any]:
    with Image.open(path) as image:
        image.load()
        if image.format != "PNG":
            raise ValueError(f"unexpected output format: {image.format}")
        return {"exists": True, "decodable": True, "format": image.format, "width": image.width, "height": image.height}


def initial_manifest(plan: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "onyx.identity_benchmark.flux_kontext_qualifier_run", "schema_version": "1.0",
        "run_id": plan["run_id"], "status": "running", "started_at": utc_now(),
        "plan": str(PLAN_PATH.resolve()), "plan_sha256": sha256(PLAN_PATH),
        "workflow_template": str(TEMPLATE_PATH.resolve()), "workflow_template_sha256": sha256(TEMPLATE_PATH),
        "existing_workflow_source": plan["existing_workflow_source"], "existing_workflow_subgraph": plan["existing_workflow_subgraph"],
        "identity": {**plan["identity"], "source_path": str(REF_PATH.resolve()), "source_sha256_verified": sha256(REF_PATH)},
        "model": {**plan["model"], "unet_size_bytes": Path(plan["model"]["unet_path"]).stat().st_size},
        "generation": plan["generation"], "runtime_flags": ["--windows-standalone-build", "--disable-async-offload", "--disable-pinned-memory"],
        "results": [], "warnings": [], "errors": [], "telemetry": {"before_series": memory_snapshot()},
    }


def refresh_validation(manifest: dict[str, Any]) -> None:
    results = manifest["results"]
    write_json(RUN_ROOT / "technical_validation.json", {
        "schema": "onyx.identity_benchmark.technical_validation", "schema_version": "1.0", "run_id": manifest["run_id"],
        "generated_at": utc_now(), "expected_output_count": 3, "validated_output_count": len(results), "all_expected_outputs_present": len(results) == 3,
        "results": [{key: item[key] for key in ("scene_id", "seed", "output", "output_sha256", "technical_validation")} for item in results],
    })


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--endpoint", default="http://127.0.0.1:8188")
    args = parser.parse_args()
    plan, template = read_json(PLAN_PATH), read_json(TEMPLATE_PATH)
    scenes = validate_contract(plan, template)
    if args.check_only:
        print(json.dumps({"status": "contract_valid", "scenes": [item["scene_id"] for item in plan["scenes"]], "primary_reference": plan["identity"]["primary_reference_id"], "workflow_template_sha256": sha256(TEMPLATE_PATH)}))
        return 0
    manifest_path = RUN_ROOT / "run_manifest.json"
    if manifest_path.is_file():
        raise FileExistsError(f"refusing to resume or overwrite qualifier manifest: {manifest_path}")
    manifest = initial_manifest(plan)
    client = ComfyUIClient(args.endpoint)
    try:
        for item in plan["scenes"]:
            scene_id, seed = item["scene_id"], item["seed"]
            scene = scenes[scene_id]
            target = RUN_ROOT / "outputs" / f"P01_{scene_id}_KONTEXT.png"
            if target.exists():
                raise FileExistsError(target)
            workflow = render(template, plan, scene, seed)
            request_path = RUN_ROOT / "requests" / f"{scene_id}.json"
            history_path = RUN_ROOT / "history" / f"{scene_id}.json"
            write_json(request_path, workflow)
            before, started = memory_snapshot(), time.monotonic()
            with GpuMonitor() as monitor:
                prompt_id = client.submit(workflow, uuid.uuid4().hex)
                history = client.wait_for_history(prompt_id, timeout_seconds=1800)
            elapsed = time.monotonic() - started
            write_json(history_path, history)
            image = client.one_image(history)
            if image.output_type != "output" or image.subfolder:
                raise ValueError(f"unexpected Comfy output: {image}")
            generated = RUN_ROOT / "outputs" / image.filename
            if not generated.is_file():
                raise FileNotFoundError(generated)
            os.replace(generated, target)
            validation = validate_png(target)
            record = {
                "scene_id": scene_id, "source_name": scene["source_name"], "canonical_scene_prompt": scene["prompt"], "prompt": workflow["8"]["inputs"]["text"], "seed": seed,
                "status": "completed", "prompt_id": prompt_id, "request": str(request_path.resolve()), "history": str(history_path.resolve()),
                "comfy_generated_filename": image.filename, "output": str(target.resolve()), "output_sha256": sha256(target), "duration_seconds": elapsed,
                "peak_gpu_used_mib": monitor.peak_gpu_used_mib(), "telemetry_samples": monitor.samples, "telemetry_before": before, "telemetry_after": memory_snapshot(),
                "technical_validation": validation, "warnings": [], "error": None,
            }
            write_json(RUN_ROOT / "manifests" / f"{scene_id}.json", record)
            manifest["results"].append(record)
            write_json(manifest_path, manifest); refresh_validation(manifest)
    except Exception as exc:
        manifest["status"] = "failed"; manifest["errors"].append({"at": utc_now(), "error": repr(exc)})
        write_json(manifest_path, manifest); refresh_validation(manifest)
        raise
    finally:
        try:
            free_models(client)
            manifest["telemetry"]["after_api_free"] = memory_snapshot()
        except Exception as exc:
            manifest["warnings"].append({"at": utc_now(), "warning": f"API model release failed: {exc!r}"})
        if len(manifest["results"]) == 3:
            manifest["status"] = "completed_api_free_sent"; manifest["finished_at"] = utc_now()
        write_json(manifest_path, manifest); refresh_validation(manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
