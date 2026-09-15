"""Bounded P01 PuLID multi-scene execution against the canonical v3 graph."""
from __future__ import annotations

import copy
import argparse
import hashlib
import json
import os
import subprocess
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
SCENES_PATH = RUN_ROOT / "scene_specs.json"
TEMPLATE_PATH = RUN_ROOT.parent / "local_pulid_baseline_v3" / "outputs" / "workflow_api.json"


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
            except Exception as exc:  # telemetry must never change a generation result
                self.samples.append({"timestamp": utc_now(), "telemetry_error": repr(exc)})
            self.stop.wait(2)

    def __enter__(self) -> "GpuMonitor":
        self.thread.start()
        return self

    def __exit__(self, *_: object) -> None:
        self.stop.set()
        self.thread.join(timeout=5)

    def peak_gpu_used_mib(self) -> int | None:
        values = [item.get("gpu", {}).get("used_mib") for item in self.samples]
        return max(value for value in values if isinstance(value, int)) if any(isinstance(value, int) for value in values) else None


def render(template: dict[str, Any], plan: dict[str, Any], scene: dict[str, Any]) -> dict[str, Any]:
    workflow = copy.deepcopy(template)
    generation = plan["generation"]
    workflow["6"]["inputs"]["text"] = scene["prompt"]
    workflow["25"]["inputs"]["noise_seed"] = scene["seed"]
    workflow["26"]["inputs"]["guidance"] = generation["guidance"]
    workflow["62"]["inputs"].update({"weight": generation["pulid_weight"], "start_at": generation["pulid_start"], "end_at": generation["pulid_end"]})
    workflow["27"]["inputs"].update({"width": generation["width"], "height": generation["height"], "batch_size": 1})
    workflow["50"]["inputs"]["filename_prefix"] = f"P01_{scene['scene_id']}_PULID"
    return workflow


def validate_png(path: Path) -> dict[str, int]:
    with Image.open(path) as image:
        image.load()
        if image.format != "PNG" or image.size != (768, 1024):
            raise ValueError(f"unexpected output: {path} ({image.format}, {image.size})")
        return {"width": image.width, "height": image.height}


def free_models(client: ComfyUIClient) -> None:
    request = urllib.request.Request(
        client.endpoint + "/free", data=json.dumps({"unload_models": True, "free_memory": True}).encode("utf-8"),
        headers={"Content-Type": "application/json", "Connection": "close"},
    )
    client._open(request, operation="model release")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the bounded P01 PuLID multi-scene set")
    parser.add_argument("--check-only", action="store_true", help="validate immutable workflow settings without contacting ComfyUI")
    args = parser.parse_args()
    plan, scenes, template = read_json(PLAN_PATH), read_json(SCENES_PATH)["scenes"], read_json(TEMPLATE_PATH)
    if len(scenes) != 3 or {item["scene_id"] for item in scenes} != {"BUS_03", "BUS_06", "BUS_09"}:
        raise ValueError("expected the exact BUS_03/BUS_06/BUS_09 controlled set")
    if template["16"]["inputs"]["sampler_name"] != plan["generation"]["sampler"]:
        raise ValueError("workflow sampler differs from the PuLID plan")
    scheduler = template["17"]["inputs"]
    if (scheduler["scheduler"], scheduler["steps"], scheduler["denoise"]) != (plan["generation"]["scheduler"], plan["generation"]["steps"], 1.0):
        raise ValueError("workflow scheduler settings differ from the PuLID plan")
    if template["26"]["inputs"]["guidance"] != plan["generation"]["guidance"]:
        raise ValueError("workflow FluxGuidance differs from the PuLID plan")
    if template["62"]["inputs"]["weight"] != plan["generation"]["pulid_weight"]:
        raise ValueError("workflow PuLID weight differs from the PuLID plan")
    if args.check_only:
        print(json.dumps({"status": "contract_valid", "workflow_template_sha256": sha256(TEMPLATE_PATH), "scenes": [item["scene_id"] for item in scenes]}))
        return 0
    manifest_path = RUN_ROOT / "run_manifest.json"
    manifest = {
        "schema": "onyx.identity_benchmark.pulid_multiscene_run", "schema_version": "1.0",
        "run_id": plan["run_id"], "status": "running", "started_at": utc_now(),
        "plan_sha256": sha256(PLAN_PATH), "scene_specs_sha256": sha256(SCENES_PATH),
        "workflow_template": str(TEMPLATE_PATH.resolve()), "workflow_template_sha256": sha256(TEMPLATE_PATH),
        "generation": plan["generation"], "scenes": [], "telemetry": {"before_series": memory_snapshot()},
    }
    write_json(manifest_path, manifest)
    client = ComfyUIClient("http://127.0.0.1:8188")
    for scene in scenes:
        workflow = render(template, plan, scene)
        request_path = RUN_ROOT / "requests" / f"{scene['scene_id']}.json"
        write_json(request_path, workflow)
        before, started = memory_snapshot(), time.monotonic()
        with GpuMonitor() as monitor:
            prompt_id = client.submit(workflow, uuid.uuid4().hex)
            history = client.wait_for_history(prompt_id, timeout_seconds=1800)
        elapsed = time.monotonic() - started
        history_path = RUN_ROOT / "history" / f"{scene['scene_id']}.json"; write_json(history_path, history)
        image = client.one_image(history)
        if image.output_type != "output" or image.subfolder:
            raise ValueError(f"unexpected ComfyUI output location: {image}")
        output_path = RUN_ROOT / "outputs" / image.filename
        if not output_path.is_file():
            raise FileNotFoundError(output_path)
        record = {
            "scene_id": scene["scene_id"], "source_name": scene["source_name"], "prompt": scene["prompt"], "seed": scene["seed"],
            "prompt_id": prompt_id, "status": "completed", "request": str(request_path.resolve()), "history": str(history_path.resolve()),
            "output": str(output_path.resolve()), "output_sha256": sha256(output_path), "duration_seconds": elapsed,
            "peak_gpu_used_mib": monitor.peak_gpu_used_mib(), "telemetry_samples": monitor.samples,
            "telemetry_before": before, "telemetry_after": memory_snapshot(), "technical_validation": {"decodable": True, **validate_png(output_path)},
            "warnings": [], "error": None,
        }
        write_json(RUN_ROOT / "manifests" / f"{scene['scene_id']}.json", record)
        manifest["scenes"].append(record); write_json(manifest_path, manifest)
    free_models(client)
    manifest["telemetry"]["after_api_free"] = memory_snapshot(); manifest["status"] = "completed_api_free_sent"; manifest["finished_at"] = utc_now()
    write_json(manifest_path, manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
