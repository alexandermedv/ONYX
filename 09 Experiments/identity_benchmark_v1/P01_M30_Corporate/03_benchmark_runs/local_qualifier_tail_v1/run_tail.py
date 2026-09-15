"""Run only the missing BUS_06/BUS_09 local P01 mini-LoRA qualifier points."""
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
TEMPLATE_PATH = ROOT / "comfyui-workflows" / "ONYX_Flux_Scene_Generator_0.3_fixed_lora_api.json"
SCENES_PATH = RUN_ROOT.parent / "pulid_multiscene_v1" / "scene_specs.json"
REFERENCES_PATH = RUN_ROOT.parent.parent / "01_references" / "references.yaml"


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


def validate_contract(plan: dict[str, Any], template: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    generation = plan["generation"]
    if template["56:58"]["inputs"]["cfg"] != generation["cfg"]:
        raise ValueError("template cfg differs from the approved mini-LoRA contract")
    if any(key not in template for key in ("56:48", "56:59", "56:51", "56:58", "56:50", "9")):
        raise ValueError("fixed mini-LoRA template is missing a required node")
    if "FluxGuidance" in {node.get("class_type") for node in template.values()}:
        raise ValueError("mini-LoRA template unexpectedly includes FluxGuidance")
    selected = {scene["scene_id"]: scene for scene in scenes if scene["scene_id"] in plan["required_scene_ids"]}
    if set(selected) != set(plan["required_scene_ids"]):
        raise ValueError("canonical source does not contain exactly BUS_06 and BUS_09")
    for scene_id, scene in selected.items():
        if scene["seed"] != plan["scenes"][scene_id]["seed"]:
            raise ValueError(f"seed drift for {scene_id}")
    for variant in plan["variants"]:
        source = Path(variant["source_path"])
        if not source.is_file():
            raise FileNotFoundError(source)
        actual_hash = sha256(source).upper()
        if actual_hash != variant["source_checkpoint_sha256"]:
            raise ValueError(f"checkpoint hash mismatch: {source}")
    if not REFERENCES_PATH.is_file():
        raise FileNotFoundError(REFERENCES_PATH)
    return selected


def render(template: dict[str, Any], plan: dict[str, Any], variant: dict[str, Any], scene: dict[str, Any]) -> dict[str, Any]:
    generation = plan["generation"]
    workflow = copy.deepcopy(template)
    workflow["56:59"]["inputs"].update({"lora_name": Path(variant["source_path"]).name, "strength_model": generation["lora_weight"]})
    workflow["56:51"]["inputs"]["text"] = f"photo of {generation['trigger']} man, {scene['prompt']}"
    workflow["56:58"]["inputs"].update({"seed": scene["seed"], "steps": generation["steps"], "cfg": generation["cfg"], "sampler_name": generation["sampler_name"], "scheduler": generation["scheduler"], "denoise": generation["denoise"]})
    workflow["56:50"]["inputs"].update({"width": generation["width"], "height": generation["height"], "batch_size": 1})
    workflow["9"]["inputs"]["filename_prefix"] = f"P01_{scene['scene_id']}_{variant['variant_id']}"
    return workflow


def validate_png(path: Path, width: int, height: int) -> dict[str, Any]:
    with Image.open(path) as image:
        image.load()
        if image.format != "PNG" or image.size != (width, height):
            raise ValueError(f"unexpected PNG output: {path} ({image.format}, {image.size})")
        return {"exists": True, "decodable": True, "format": image.format, "width": image.width, "height": image.height}


def refresh_technical_validation(manifest: dict[str, Any]) -> None:
    results = manifest["results"]
    write_json(RUN_ROOT / "technical_validation.json", {
        "schema": "onyx.identity_benchmark.technical_validation", "schema_version": "1.0",
        "run_id": manifest["run_id"], "generated_at": utc_now(), "expected_png_count": 12,
        "validated_png_count": len(results), "all_expected_outputs_present": len(results) == 12,
        "results": [{"variant_id": item["variant_id"], "scene_id": item["scene_id"], "output": item["output"], "output_sha256": item["output_sha256"], "technical_validation": item["technical_validation"]} for item in results],
    })


def initial_manifest(plan: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "onyx.identity_benchmark.local_qualifier_tail_run", "schema_version": "1.0",
        "run_id": plan["run_id"], "status": "running", "started_at": utc_now(),
        "plan": str(PLAN_PATH.resolve()), "plan_sha256": sha256(PLAN_PATH),
        "workflow_template": str(TEMPLATE_PATH.resolve()), "workflow_template_sha256": sha256(TEMPLATE_PATH),
        "canonical_scene_specs": str(SCENES_PATH.resolve()), "canonical_scene_specs_sha256": sha256(SCENES_PATH),
        "canonical_references": str(REFERENCES_PATH.resolve()), "canonical_references_sha256": sha256(REFERENCES_PATH),
        "generation": plan["generation"], "runtime_flags": ["--windows-standalone-build", "--disable-async-offload", "--disable-pinned-memory"],
        "results": [], "warnings": [], "errors": [], "telemetry": {"before_first_series": memory_snapshot()},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", choices=("p01_mini_3", "p01_mini_5"), required=True)
    parser.add_argument("--endpoint", default="http://127.0.0.1:8188")
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()

    plan, template = read_json(PLAN_PATH), read_json(TEMPLATE_PATH)
    selected_scenes = validate_contract(plan, template, read_json(SCENES_PATH)["scenes"])
    variants = [item for item in plan["variants"] if item["dataset_id"] == args.dataset]
    if len(variants) != 3:
        raise ValueError(f"expected three variants for {args.dataset}, found {len(variants)}")
    if args.check_only:
        print(json.dumps({"status": "contract_valid", "dataset": args.dataset, "scenes": list(selected_scenes), "workflow_template_sha256": sha256(TEMPLATE_PATH)}))
        return 0

    manifest_path = RUN_ROOT / "run_manifest.json"
    manifest = read_json(manifest_path) if manifest_path.is_file() else initial_manifest(plan)
    existing = {(item["variant_id"], item["scene_id"]) for item in manifest["results"]}
    client = ComfyUIClient(args.endpoint)
    try:
        for variant in variants:
            for scene_id in plan["required_scene_ids"]:
                scene = selected_scenes[scene_id]
                key = (variant["variant_id"], scene_id)
                if key in existing:
                    raise ValueError(f"refusing to repeat an existing qualifier point: {key}")
                expected_name = f"P01_{scene_id}_{variant['variant_id']}_00001_.png"
                expected_output = RUN_ROOT / "outputs" / expected_name
                if expected_output.exists():
                    raise FileExistsError(f"refusing to overwrite existing output: {expected_output}")
                workflow = render(template, plan, variant, scene)
                stem = f"{variant['variant_id']}__{scene_id}"
                request_path = RUN_ROOT / "requests" / f"{stem}.json"
                history_path = RUN_ROOT / "history" / f"{stem}.json"
                write_json(request_path, workflow)
                before, started = memory_snapshot(), time.monotonic()
                with GpuMonitor() as monitor:
                    prompt_id = client.submit(workflow, uuid.uuid4().hex)
                    history = client.wait_for_history(prompt_id, timeout_seconds=1800)
                elapsed = time.monotonic() - started
                write_json(history_path, history)
                image = client.one_image(history)
                if image.output_type != "output" or image.subfolder:
                    raise ValueError(f"unexpected ComfyUI output location: {image}")
                actual_output = RUN_ROOT / "outputs" / image.filename
                if actual_output != expected_output or not actual_output.is_file():
                    raise FileNotFoundError(f"expected {expected_output}, got {actual_output}")
                record = {
                    "variant_id": variant["variant_id"], "dataset_id": variant["dataset_id"], "checkpoint": variant["checkpoint"],
                    "scene_id": scene_id, "scene_label": plan["scenes"][scene_id]["label"], "canonical_scene_prompt": scene["prompt"],
                    "prompt": workflow["56:51"]["inputs"]["text"], "seed": scene["seed"], "status": "completed", "prompt_id": prompt_id,
                    "source_checkpoint": variant["source_path"], "source_checkpoint_sha256": sha256(Path(variant["source_path"])).upper(),
                    "request": str(request_path.resolve()), "history": str(history_path.resolve()), "output": str(actual_output.resolve()),
                    "output_sha256": sha256(actual_output), "duration_seconds": elapsed, "peak_gpu_used_mib": monitor.peak_gpu_used_mib(),
                    "telemetry_samples": monitor.samples, "telemetry_before": before, "telemetry_after": memory_snapshot(),
                    "technical_validation": validate_png(actual_output, plan["generation"]["width"], plan["generation"]["height"]), "warnings": [], "error": None,
                }
                write_json(RUN_ROOT / "manifests" / f"{stem}.json", record)
                manifest["results"].append(record)
                write_json(manifest_path, manifest)
                refresh_technical_validation(manifest)
    except Exception as exc:
        manifest["status"] = "failed"; manifest["errors"].append({"at": utc_now(), "dataset": args.dataset, "error": repr(exc)})
        write_json(manifest_path, manifest); refresh_technical_validation(manifest)
        raise
    finally:
        try:
            free_models(client)
            manifest["telemetry"][f"after_{args.dataset}_api_free"] = memory_snapshot()
        except Exception as exc:
            manifest["warnings"].append({"at": utc_now(), "dataset": args.dataset, "warning": f"API memory release failed: {exc!r}"})
        if len(manifest["results"]) == 12:
            manifest["status"] = "completed_api_free_sent"; manifest["finished_at"] = utc_now()
        write_json(manifest_path, manifest); refresh_technical_validation(manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
