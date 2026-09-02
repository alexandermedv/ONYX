"""Deterministic, sequential Stage 1 benchmark adapter for ComfyUI."""
from __future__ import annotations

import hashlib
import json
import os
import time
import uuid
import shutil
from pathlib import Path
from typing import Any

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    try:
        from ..runtime.comfyui_client import ComfyUIClient
    except ImportError:  # pragma: no cover
        from engine.runtime.comfyui_client import ComfyUIClient


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_stage1_plan(plan: dict[str, Any]) -> None:
    if plan.get("schema") != "onyx.lora_lab.benchmark_plan":
        raise ValueError("invalid benchmark plan schema")
    if plan.get("stage_id") != "stage_1_screening" or plan.get("task_count") != 80:
        raise ValueError("Stage 1 plan must contain exactly 80 tasks")
    if len(plan.get("tasks", [])) != 80:
        raise ValueError("Stage 1 task list must contain exactly 80 tasks")


def checkpoint_mapping(source_manifest: dict[str, Any]) -> dict[tuple[str, int], dict[str, Any]]:
    mapping: dict[tuple[str, int], dict[str, Any]] = {}
    for dataset_id, dataset in source_manifest.get("datasets", {}).items():
        for item in dataset.get("checkpoints", []):
            step = int(item["step"])
            key = (dataset_id, step)
            if key in mapping:
                raise ValueError(f"duplicate checkpoint mapping: {key}")
            mapping[key] = dict(item)
    if len(mapping) != 20:
        raise ValueError(f"expected 20 logical checkpoints, got {len(mapping)}")
    return mapping


def stage_checkpoints(source_manifest: dict[str, Any], staging_root: Path, *, comfy_lora_prefix: str = "") -> dict[str, Any]:
    """Copy the immutable inventory into an experiment-only ComfyUI LoRA namespace."""
    mapping = checkpoint_mapping(source_manifest)
    rows = []
    for (dataset, step), item in sorted(mapping.items()):
        source = Path(item["source_path"])
        if not source.is_file():
            raise FileNotFoundError(source)
        staged_name = f"{dataset}__{step:04d}.safetensors"
        target = staging_root / staged_name
        source_hash = item.get("sha256") or sha256_file(source)
        if target.exists():
            if sha256_file(target) != source_hash:
                raise FileExistsError(f"conflicting staged checkpoint: {target}")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        staged_hash = sha256_file(target)
        if staged_hash != source_hash:
            raise RuntimeError(f"staged checkpoint hash mismatch: {target}")
        comfy_lora_name = f"{comfy_lora_prefix}\\{staged_name}" if comfy_lora_prefix else staged_name
        rows.append({"dataset": dataset, "step": step, "source_path": str(source), "staged_path": str(target), "staged_filename": staged_name, "comfy_lora_name": comfy_lora_name, "size": target.stat().st_size, "sha256": source_hash, "staged_sha256": staged_hash})
    return {"schema": "onyx.lora_lab.benchmark_staging_manifest", "schema_version": "1.0", "status": "immutable", "checkpoints": rows}


def build_checkpoint_inventory(night_plan: dict[str, Any]) -> dict[str, Any]:
    datasets: dict[str, dict[str, Any]] = {}
    for run in night_plan.get("runs", []):
        dataset = run["run_id"].removesuffix("_fixed_steps")
        root = Path(run["output_directory"])
        rows = []
        for step in run["checkpoint_steps"]:
            numbered = root / f"{run['run_id']}_{int(step):09d}.safetensors"
            final = root / f"{run['run_id']}.safetensors"
            source = final if int(step) == max(run["checkpoint_steps"]) and final.is_file() else numbered
            if not source.is_file():
                raise FileNotFoundError(source)
            rows.append({"step": int(step), "source_path": str(source), "size": source.stat().st_size, "sha256": sha256_file(source)})
        datasets[dataset] = {"checkpoints": rows}
    return {"schema": "onyx.lora_lab.checkpoint_inventory", "schema_version": "1.0", "datasets": datasets}


def substitute_workflow(template: dict[str, Any], task: dict[str, Any], checkpoint: dict[str, Any]) -> dict[str, Any]:
    workflow = json.loads(json.dumps(template))
    workflow["4"]["inputs"].update({"lora_name": checkpoint.get("comfy_lora_name", checkpoint["staged_filename"]), "strength_model": task["lora_weight"]})
    workflow["5"]["inputs"]["text"] = task["prompt"]
    workflow["7"]["inputs"].update({"width": task["width"], "height": task["height"], "batch_size": 1})
    workflow["8"]["inputs"].update({"seed": task["seed"], "steps": 30, "cfg": 4.0, "sampler_name": "euler", "scheduler": "simple", "denoise": 1.0})
    workflow["10"]["inputs"]["filename_prefix"] = f"onyx_benchmark/{task['task_id']}"
    return workflow


def output_path(root: Path, task: dict[str, Any]) -> Path:
    return root / "images" / task["dataset_id"] / str(task["checkpoint"]) / f"{task['scene_id']}__seed_{task['seed']}.png"


def run_task(client: Any, template: dict[str, Any], task: dict[str, Any], checkpoint: dict[str, Any], root: Path, *, client_id: str | None = None, timeout_seconds: float = 1800) -> dict[str, Any]:
    destination = output_path(root, task)
    if destination.exists():
        raise FileExistsError(f"conflicting existing benchmark output: {destination}")
    started = time.monotonic()
    prompt_id = client.submit(substitute_workflow(template, task, checkpoint), client_id or uuid.uuid4().hex)
    history = client.wait_for_history(prompt_id, timeout_seconds)
    image = client.one_image(history)
    payload = client.download(image)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".writing")
    try:
        temporary.write_bytes(payload)
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)
    return {"task_id": task["task_id"], "prompt_id": prompt_id, "source_output": image.__dict__, "canonical_output": str(destination), "image_sha256": sha256_file(destination), "duration_seconds": time.monotonic() - started, "status": "completed"}


def execute_plan(plan: dict[str, Any], template: dict[str, Any], checkpoints: dict[tuple[str, int], dict[str, Any]], client: Any, output_root: Path, *, limit: int | None = None) -> dict[str, Any]:
    validate_stage1_plan(plan)
    results = []
    for task in plan["tasks"][:limit]:
        checkpoint = checkpoints.get((task["dataset_id"], int(task["checkpoint"])))
        if checkpoint is None:
            raise FileNotFoundError(f"missing checkpoint mapping: {task['dataset_id']}@{task['checkpoint']}")
        results.append(run_task(client, template, task, checkpoint, output_root))
    return {"schema": "onyx.lora_lab.stage1_generation_manifest", "schema_version": "1.0", "status": "completed", "task_count": len(results), "tasks": results}
