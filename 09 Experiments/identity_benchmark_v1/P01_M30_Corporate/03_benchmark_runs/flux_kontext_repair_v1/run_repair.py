"""Run exactly two prompt-only FLUX Kontext anatomy repair points."""
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
SCENES_PATH = RUN_ROOT.parent / "pulid_multiscene_v1" / "scene_specs.json"
REF_PATH = RUN_ROOT.parent.parent / "01_references" / "P01_REF01_frontal.png"
OFFICIAL_ROOT = RUN_ROOT.parent / "flux_kontext_qualifier_v1"


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
        self.stop = threading.Event(); self.samples: list[dict[str, Any]] = []
        self.thread = threading.Thread(target=self._run, daemon=True)

    def _run(self) -> None:
        while not self.stop.is_set():
            try: self.samples.append(memory_snapshot())
            except Exception as exc: self.samples.append({"timestamp": utc_now(), "telemetry_error": repr(exc)})
            self.stop.wait(2)

    def __enter__(self) -> "GpuMonitor": self.thread.start(); return self
    def __exit__(self, *_: object) -> None: self.stop.set(); self.thread.join(timeout=5)
    def peak_gpu_used_mib(self) -> int | None:
        values = [sample.get("gpu", {}).get("used_mib") for sample in self.samples]
        values = [value for value in values if isinstance(value, int)]
        return max(values) if values else None


def free_models(client: ComfyUIClient) -> None:
    request = urllib.request.Request(client.endpoint + "/free", data=json.dumps({"unload_models": True, "free_memory": True}).encode("utf-8"), headers={"Content-Type": "application/json", "Connection": "close"})
    client._open(request, operation="model release")


def verify_official_artifacts(plan: dict[str, Any]) -> dict[str, str]:
    expected = plan["source_qualifier"]
    paths = {
        "run_manifest_sha256_preflight": OFFICIAL_ROOT / "run_manifest.json",
        "technical_validation_sha256_preflight": OFFICIAL_ROOT / "technical_validation.json",
        "workflow_template_sha256_preflight": OFFICIAL_ROOT / "workflow_template_api.json",
        "bus_06_output_sha256_preflight": OFFICIAL_ROOT / "outputs" / "P01_BUS_06_KONTEXT.png",
        "bus_09_output_sha256_preflight": OFFICIAL_ROOT / "outputs" / "P01_BUS_09_KONTEXT.png",
    }
    actual = {key: sha256(path).upper() for key, path in paths.items()}
    mismatches = [key for key, value in actual.items() if value != expected[key]]
    if mismatches: raise ValueError(f"official qualifier artifact drift: {mismatches}")
    return actual


def validate_contract(plan: dict[str, Any], template: dict[str, Any]) -> dict[str, dict[str, Any]]:
    if not REF_PATH.is_file() or sha256(REF_PATH).lower() != plan["identity"]["primary_reference_sha256"]:
        raise ValueError("canonical REF01 unavailable or hash-mismatched")
    if not Path(plan["model"]["unet_path"]).is_file(): raise FileNotFoundError(plan["model"]["unet_path"])
    generation, sampler = plan["generation"], template["12"]["inputs"]
    if (sampler["steps"], sampler["cfg"], sampler["sampler_name"], sampler["scheduler"], sampler["denoise"], template["10"]["inputs"]["guidance"]) != (generation["steps"], generation["cfg"], generation["sampler_name"], generation["scheduler"], generation["denoise"], generation["guidance"]):
        raise ValueError("repair template diverges from controlled Kontext parameters")
    original_template = OFFICIAL_ROOT / "workflow_template_api.json"
    if sha256(TEMPLATE_PATH) != sha256(original_template): raise ValueError("repair topology differs from official template")
    scenes = {item["scene_id"]: item for item in read_json(SCENES_PATH)["scenes"]}
    expected = {item["scene_id"]: item["seed"] for item in plan["scenes"]}
    if set(expected) != {"BUS_06", "BUS_09"} or any(scenes[key]["seed"] != expected[key] for key in expected): raise ValueError("scene seed drift")
    return {key: scenes[key] for key in expected}


def render(template: dict[str, Any], plan: dict[str, Any], scene: dict[str, Any], seed: int) -> dict[str, Any]:
    workflow = copy.deepcopy(template); scene_id = scene["scene_id"]
    changes = plan["prompt_changes"]
    prompt = f"Place the same adult man in this scene: {scene['prompt']} Preserve his facial features, apparent age, bald head, natural skin texture, identity, and photorealistic quality. {changes['common']} {changes[scene_id]} Do not add other people."
    workflow["1"]["inputs"]["image"] = plan["identity"]["comfy_input"]
    workflow["8"]["inputs"]["text"] = prompt; workflow["12"]["inputs"]["seed"] = seed
    workflow["14"]["inputs"]["filename_prefix"] = f"P01_{scene_id}_KONTEXT_REPAIR"
    return workflow


def validate_png(path: Path) -> dict[str, Any]:
    with Image.open(path) as image:
        image.load()
        if image.format != "PNG": raise ValueError(f"unexpected format: {image.format}")
        return {"exists": True, "decodable": True, "format": image.format, "width": image.width, "height": image.height}


def refresh_validation(manifest: dict[str, Any]) -> None:
    write_json(RUN_ROOT / "technical_validation.json", {"schema": "onyx.identity_benchmark.technical_validation", "schema_version": "1.0", "run_id": manifest["run_id"], "generated_at": utc_now(), "expected_output_count": 2, "validated_output_count": len(manifest["results"]), "all_expected_outputs_present": len(manifest["results"]) == 2, "results": [{key: item[key] for key in ("scene_id", "seed", "output", "output_sha256", "technical_validation")} for item in manifest["results"]]})


def recover_saved_output(manifest: dict[str, Any], plan: dict[str, Any], scenes: dict[str, dict[str, Any]], client: ComfyUIClient) -> None:
    """Recover a completed Comfy save after an interrupted artifact hand-off; never submit work."""
    completed = {item["scene_id"] for item in manifest["results"]}
    for item in plan["scenes"]:
        scene_id, seed = item["scene_id"], item["seed"]
        if scene_id in completed:
            continue
        history_path = RUN_ROOT / "history" / f"{scene_id}.json"
        if not history_path.is_file():
            continue
        history = read_json(history_path)
        image = client.one_image(history)
        generated = RUN_ROOT / "output" / image.filename
        target = RUN_ROOT / "outputs" / f"P01_{scene_id}_KONTEXT_REPAIR.png"
        target.parent.mkdir(parents=True, exist_ok=True)
        if not generated.is_file() or target.exists():
            continue
        os.replace(generated, target)
        messages = history.get("status", {}).get("messages", [])
        timestamps = [event[1].get("timestamp") for event in messages if isinstance(event, list) and len(event) > 1 and isinstance(event[1], dict) and isinstance(event[1].get("timestamp"), int)]
        duration = (max(timestamps) - min(timestamps)) / 1000 if len(timestamps) >= 2 else None
        workflow = read_json(RUN_ROOT / "requests" / f"{scene_id}.json")
        record = {"scene_id": scene_id, "source_name": scenes[scene_id]["source_name"], "canonical_scene_prompt": scenes[scene_id]["prompt"], "prompt": workflow["8"]["inputs"]["text"], "seed": seed, "status": "completed_recovered_saved_output", "prompt_id": history["prompt"][1], "request": str((RUN_ROOT / "requests" / f"{scene_id}.json").resolve()), "history": str(history_path.resolve()), "comfy_generated_filename": image.filename, "output": str(target.resolve()), "output_sha256": sha256(target), "duration_seconds": duration, "peak_gpu_used_mib": None, "telemetry_samples": [], "telemetry_before": manifest["telemetry"]["before_series"], "telemetry_after": memory_snapshot(), "technical_validation": validate_png(target), "warnings": ["Recovered an already-completed ComfyUI output after an artifact-directory mismatch; no second submission was made."], "error": None}
        write_json(RUN_ROOT / "manifests" / f"{scene_id}.json", record)
        manifest["results"].append(record)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--check-only", action="store_true"); parser.add_argument("--continue-after-artifact-recovery", action="store_true"); parser.add_argument("--endpoint", default="http://127.0.0.1:8188"); args = parser.parse_args()
    plan, template = read_json(PLAN_PATH), read_json(TEMPLATE_PATH)
    official_hashes, scenes = verify_official_artifacts(plan), validate_contract(plan, template)
    if args.check_only:
        print(json.dumps({"status": "contract_valid", "scenes": list(scenes), "official_artifacts_verified": official_hashes, "template_sha256": sha256(TEMPLATE_PATH)})); return 0
    manifest_path = RUN_ROOT / "run_manifest.json"
    client = ComfyUIClient(args.endpoint)
    if manifest_path.exists():
        if not args.continue_after_artifact_recovery: raise FileExistsError(f"refusing to overwrite repair manifest: {manifest_path}")
        manifest = read_json(manifest_path)
        if manifest.get("status") != "failed": raise ValueError("continuation is permitted only after a failed artifact hand-off")
        recover_saved_output(manifest, plan, scenes, client)
        manifest["status"] = "running"; manifest["resumed_at"] = utc_now()
        manifest["warnings"].append({"at": utc_now(), "warning": "Resumed after recovering an existing completed output; only unresolved scenes may be submitted."})
        write_json(manifest_path, manifest); refresh_validation(manifest)
    else:
        manifest = {"schema": "onyx.identity_benchmark.flux_kontext_repair_run", "schema_version": "1.0", "run_id": plan["run_id"], "status": "running", "started_at": utc_now(), "plan": str(PLAN_PATH.resolve()), "plan_sha256": sha256(PLAN_PATH), "workflow_template": str(TEMPLATE_PATH.resolve()), "workflow_template_sha256": sha256(TEMPLATE_PATH), "official_artifacts_verified_before_run": official_hashes, "identity": {**plan["identity"], "source_path": str(REF_PATH.resolve()), "source_sha256_verified": sha256(REF_PATH)}, "model": plan["model"], "generation": plan["generation"], "prompt_changes": plan["prompt_changes"], "runtime_flags": ["--windows-standalone-build", "--disable-async-offload", "--disable-pinned-memory"], "results": [], "warnings": [], "errors": [], "telemetry": {"before_series": memory_snapshot()}}
    try:
        for item in plan["scenes"]:
            scene_id, seed = item["scene_id"], item["seed"]; scene = scenes[scene_id]; target = RUN_ROOT / "outputs" / f"P01_{scene_id}_KONTEXT_REPAIR.png"
            target.parent.mkdir(parents=True, exist_ok=True)
            if scene_id in {result["scene_id"] for result in manifest["results"]}: continue
            if target.exists(): raise FileExistsError(target)
            workflow = render(template, plan, scene, seed); request_path = RUN_ROOT / "requests" / f"{scene_id}.json"; history_path = RUN_ROOT / "history" / f"{scene_id}.json"; write_json(request_path, workflow)
            before, started = memory_snapshot(), time.monotonic()
            with GpuMonitor() as monitor:
                prompt_id = client.submit(workflow, uuid.uuid4().hex); history = client.wait_for_history(prompt_id, timeout_seconds=1800)
            elapsed = time.monotonic() - started; write_json(history_path, history); image = client.one_image(history)
            if image.output_type != "output" or image.subfolder: raise ValueError(f"unexpected Comfy output: {image}")
            generated = RUN_ROOT / "output" / image.filename
            if not generated.is_file(): raise FileNotFoundError(generated)
            os.replace(generated, target); validation = validate_png(target)
            record = {"scene_id": scene_id, "source_name": scene["source_name"], "canonical_scene_prompt": scene["prompt"], "prompt": workflow["8"]["inputs"]["text"], "seed": seed, "status": "completed", "prompt_id": prompt_id, "request": str(request_path.resolve()), "history": str(history_path.resolve()), "comfy_generated_filename": image.filename, "output": str(target.resolve()), "output_sha256": sha256(target), "duration_seconds": elapsed, "peak_gpu_used_mib": monitor.peak_gpu_used_mib(), "telemetry_samples": monitor.samples, "telemetry_before": before, "telemetry_after": memory_snapshot(), "technical_validation": validation, "warnings": [], "error": None}
            write_json(RUN_ROOT / "manifests" / f"{scene_id}.json", record); manifest["results"].append(record); write_json(manifest_path, manifest); refresh_validation(manifest)
    except Exception as exc:
        manifest["status"] = "failed"; manifest["errors"].append({"at": utc_now(), "error": repr(exc)}); write_json(manifest_path, manifest); refresh_validation(manifest); raise
    finally:
        try: free_models(client); manifest["telemetry"]["after_api_free"] = memory_snapshot()
        except Exception as exc: manifest["warnings"].append({"at": utc_now(), "warning": f"API model release failed: {exc!r}"})
        if len(manifest["results"]) == 2: manifest["status"] = "completed_api_free_sent"; manifest["finished_at"] = utc_now()
        write_json(manifest_path, manifest); refresh_validation(manifest)
    return 0


if __name__ == "__main__": raise SystemExit(main())
