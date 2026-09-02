from __future__ import annotations

import math
from dataclasses import asdict
from pathlib import Path

from .models import DatasetSpec, TrainingSpec


def resolve_steps(spec: TrainingSpec, dataset_size: int, mode: str) -> int:
    if mode == "fixed_steps":
        return spec.fixed_steps
    if mode == "fixed_exposure":
        samples = dataset_size * spec.fixed_exposure_epochs
        effective_batch = spec.batch_size * spec.gradient_accumulation
        return max(1, math.ceil(samples / effective_batch))
    raise ValueError(f"unsupported comparison mode: {mode}")


def checkpoint_steps(spec: TrainingSpec, steps: int, mode: str) -> list[int]:
    if mode == "fixed_steps":
        values = list(range(spec.save_interval, steps + 1, spec.save_interval))
        if not values or values[-1] != steps:
            values.append(steps)
        return values
    return sorted({max(1, round(steps * fraction)) for fraction in spec.checkpoint_fractions})


def plan_training(spec: TrainingSpec, datasets: list[DatasetSpec], mode: str) -> dict:
    runs = []
    effective_batch = spec.batch_size * spec.gradient_accumulation
    for dataset in datasets:
        steps = resolve_steps(spec, dataset.size, mode)
        samples_seen = steps * effective_batch
        runs.append(
            {
                "run_id": f"{dataset.dataset_id}_{mode}",
                "dataset_id": dataset.dataset_id,
                "dataset_size": dataset.size,
                "dataset_manifest": dataset.manifest_path,
                "mode": mode,
                "optimizer_steps": steps,
                "samples_seen": samples_seen,
                "effective_epochs": samples_seen / dataset.size,
                "checkpoint_steps": checkpoint_steps(spec, steps, mode),
                "output_directory": str(Path(spec.output_root) / f"{dataset.dataset_id}_{mode}"),
            }
        )
    return {
        "schema": "onyx.lora_lab.training_plan",
        "schema_version": "1.0",
        "experiment_id": spec.experiment_id,
        "comparison_mode": mode,
        "training_spec": asdict(spec),
        "runs": runs,
    }
