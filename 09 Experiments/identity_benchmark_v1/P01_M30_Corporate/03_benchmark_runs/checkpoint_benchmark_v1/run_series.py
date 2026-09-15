"""Execute one bounded P01 mini-LoRA checkpoint series through a running ComfyUI."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import sys
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
TEMPLATE = ROOT / "comfyui-workflows" / "ONYX_Flux_Scene_Generator_0.3_fixed_lora_api.json"
PLAN = RUN_ROOT / "run_plan.json"
EXTRA_LORA_ROOT = "D:\\AI\\AI-Toolkit\\output\\onyx_p01_lora_dataset_size_v1"


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


def free_models(client: ComfyUIClient) -> None:
    request = urllib.request.Request(
        client.endpoint + "/free",
        data=json.dumps({"unload_models": True, "free_memory": True}).encode("utf-8"),
        headers={"Content-Type": "application/json", "Connection": "close"},
    )
    client._open(request, operation="model release")


def render(template: dict[str, Any], plan: dict[str, Any], variant: dict[str, Any]) -> dict[str, Any]:
    workflow = copy.deepcopy(template)
    generation = plan["generation"]
    source = Path(variant["source_path"])
    workflow["56:59"]["inputs"].update({
        "lora_name": source.name,
        "strength_model": generation["lora_weight"],
    })
    workflow["56:51"]["inputs"]["text"] = plan["scene"]["prompt"]
    workflow["56:58"]["inputs"].update({
        "seed": generation["seed"], "steps": generation["steps"], "cfg": generation["cfg"],
        "sampler_name": generation["sampler_name"], "scheduler": generation["scheduler"],
        "denoise": generation["denoise"],
    })
    workflow["56:50"]["inputs"].update({"width": generation["width"], "height": generation["height"], "batch_size": 1})
    workflow["9"]["inputs"]["filename_prefix"] = f"P01_BUS_01_{variant['dataset_id']}__{variant['checkpoint']:04d}"
    return workflow


def validate_png(path: Path, width: int, height: int) -> dict[str, int]:
    with Image.open(path) as image:
        image.load()
        if image.format != "PNG" or image.size != (width, height):
            raise ValueError(f"unexpected PNG output: {path} ({image.format}, {image.size})")
        return {"width": image.width, "height": image.height}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", choices=("p01_mini_3", "p01_mini_5"), required=True)
    parser.add_argument("--endpoint", default="http://127.0.0.1:8188")
    args = parser.parse_args()

    plan = read_json(PLAN)
    template = read_json(TEMPLATE)
    variants = [item for item in plan["variants"] if item["dataset_id"] == args.dataset]
    if len(variants) != 3:
        raise ValueError(f"expected three variants for {args.dataset}, found {len(variants)}")

    manifest_path = RUN_ROOT / "manifests" / f"{args.dataset}_series_manifest.json"
    series = {
        "schema": "onyx.identity_benchmark.checkpoint_series",
        "schema_version": "1.0",
        "run_id": plan["run_id"], "dataset_id": args.dataset, "status": "running",
        "started_at": utc_now(), "plan_sha256": sha256(PLAN), "workflow_template": str(TEMPLATE),
        "workflow_template_sha256": sha256(TEMPLATE), "generation": plan["generation"], "scene": plan["scene"],
        "extra_lora_root": EXTRA_LORA_ROOT, "variants": [], "telemetry": {"before_series": memory_snapshot()},
    }
    write_json(manifest_path, series)
    client = ComfyUIClient(args.endpoint)
    for variant in variants:
        output_name = f"P01_BUS_01_{variant['dataset_id']}__{variant['checkpoint']:04d}_00001_.png"
        output_path = RUN_ROOT / "outputs" / output_name
        if output_path.exists():
            raise FileExistsError(f"refusing to overwrite existing output: {output_path}")
        workflow = render(template, plan, variant)
        request_path = RUN_ROOT / "requests" / f"{variant['dataset_id']}__{variant['checkpoint']:04d}.json"
        write_json(request_path, workflow)
        before = memory_snapshot(); started = time.monotonic()
        prompt_id = client.submit(workflow, uuid.uuid4().hex)
        history = client.wait_for_history(prompt_id, timeout_seconds=1800)
        elapsed = time.monotonic() - started
        write_json(RUN_ROOT / "history" / f"{variant['dataset_id']}__{variant['checkpoint']:04d}.json", history)
        image = client.one_image(history)
        if image.output_type != "output" or image.subfolder:
            raise ValueError(f"unexpected ComfyUI output location: {image}")
        actual_output = RUN_ROOT / "outputs" / image.filename
        if actual_output != output_path or not actual_output.is_file():
            raise FileNotFoundError(f"expected output {output_path}, got {actual_output}")
        dimensions = validate_png(actual_output, plan["generation"]["width"], plan["generation"]["height"])
        record = {
            "dataset_id": variant["dataset_id"], "checkpoint": variant["checkpoint"],
            "source_checkpoint": variant["source_path"], "source_checkpoint_sha256": sha256(Path(variant["source_path"])),
            "staged_filename": variant["staged_filename"], "prompt_id": prompt_id, "status": "completed",
            "request": str(request_path.resolve()), "history": str((RUN_ROOT / "history" / f"{variant['dataset_id']}__{variant['checkpoint']:04d}.json").resolve()),
            "output": str(actual_output.resolve()), "output_sha256": sha256(actual_output), "duration_seconds": elapsed,
            "telemetry_before": before, "telemetry_after": memory_snapshot(), "technical_validation": {"decodable": True, **dimensions},
        }
        write_json(RUN_ROOT / "manifests" / f"{variant['dataset_id']}__{variant['checkpoint']:04d}.json", record)
        series["variants"].append(record); write_json(manifest_path, series)
    free_models(client)
    series["telemetry"]["after_api_free"] = memory_snapshot()
    series["status"] = "completed_api_free_sent"; series["finished_at"] = utc_now()
    write_json(manifest_path, series)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
