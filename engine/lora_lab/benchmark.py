from __future__ import annotations

import hashlib

from .models import BenchmarkSpec


def plan_benchmark(spec: BenchmarkSpec, stage_id: str, best_checkpoints: dict[str, int] | None = None,
                   historical_control: dict | None = None) -> dict:
    stage = next((item for item in spec.stages if item.stage_id == stage_id), None)
    if stage is None:
        raise ValueError(f"unknown benchmark stage: {stage_id}")
    scene_by_id = {scene.scene_id: scene for scene in spec.scenes}
    tasks = []
    for dataset in stage.datasets:
        checkpoints = stage.checkpoints
        if stage.checkpoint_mode == "best":
            if not best_checkpoints or dataset not in best_checkpoints:
                checkpoints = ("BEST_CHECKPOINT_PENDING_STAGE_1",)
            else:
                checkpoints = (best_checkpoints[dataset],)
        for checkpoint in checkpoints:
            for scene_id in stage.scenes:
                scene = scene_by_id[scene_id]
                for seed in stage.seeds:
                    for weight in stage.weights:
                        task_key = f"{stage_id}|{dataset}|{checkpoint}|{scene_id}|{seed}|{weight:.3f}"
                        tasks.append({
                            "task_id": hashlib.sha256(task_key.encode()).hexdigest()[:16],
                            "dataset_id": dataset, "checkpoint": checkpoint, "scene_id": scene_id,
                            "prompt": scene.prompt, "width": scene.width, "height": scene.height,
                            "seed": seed, "lora_weight": weight,
                        })
    controls = []
    if stage.include_historical_control and historical_control:
        controls.append(historical_control)
    return {
        "schema": "onyx.lora_lab.benchmark_plan", "schema_version": "1.0",
        "benchmark_id": spec.benchmark_id, "stage_id": stage_id,
        "inference": {"steps": spec.inference_steps, "guidance": spec.guidance,
                      "sampler": spec.sampler, "scheduler": spec.scheduler},
        "task_count": len(tasks), "tasks": tasks, "external_controls": controls,
    }
