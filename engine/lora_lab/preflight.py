from __future__ import annotations

from copy import deepcopy
from pathlib import Path


def render_smoke_config(production_config: dict, dataset_path: Path, output_root: Path,
                        name: str = "smoke_mini_3_10steps", steps: int = 10) -> dict:
    if not 5 <= steps <= 10:
        raise ValueError("smoke test must use 5-10 optimizer steps")
    config = deepcopy(production_config)
    config["config"]["name"] = name
    process = config["config"]["process"][0]
    process["training_folder"] = str(output_root)
    process["datasets"][0]["folder_path"] = str(dataset_path)
    process["train"]["steps"] = steps
    process["save"]["save_every"] = steps
    process["save"]["max_step_saves_to_keep"] = 1
    process["train"]["disable_sampling"] = True
    config["meta"] = {"name": name, "version": "1.0", "artifact_role": "technical_smoke_not_experimental_evidence"}
    return config


def build_night_plan(training_plan: dict, configs_root: Path, dataset_root: Path,
                     runtime_root: Path, toolkit_root: Path, python: Path,
                     base_model: Path, checkpoint_size_bytes: int,
                     output_root: Path, required_free_vram_mib: int = 20_000) -> dict:
    runs = []
    for run in training_plan["runs"]:
        runs.append({
            "run_id": run["run_id"], "dataset_size": run["dataset_size"],
            "dataset": str(dataset_root / run["dataset_id"]),
            "config": str((configs_root / f"{run['run_id']}.yaml").resolve()),
            "output_directory": run["output_directory"],
            "checkpoint_steps": run["checkpoint_steps"],
        })
    checkpoint_count = sum(len(run["checkpoint_steps"]) + 1 for run in runs)
    checkpoint_bytes = checkpoint_count * checkpoint_size_bytes
    log_telemetry_allowance = 512 * 1024**2
    temporary_allowance = 8 * 1024**3
    required = checkpoint_bytes + log_telemetry_allowance + temporary_allowance
    return {
        "schema": "onyx.lora_lab.night_run_plan", "schema_version": "1.0",
        "experiment_id": training_plan["experiment_id"], "mode": "fixed_steps",
        "ai_toolkit_root": str(toolkit_root), "python": str(python), "base_model": str(base_model),
        "output_root": str(output_root), "runtime_root": str(runtime_root),
        "log_root": str(runtime_root / "night_run" / "logs"),
        "state_file": str(runtime_root / "night_run" / "night_run_state.json"),
        "checkpoint_size_bytes": checkpoint_size_bytes, "checkpoint_count_including_finals": checkpoint_count,
        "checkpoint_bytes": checkpoint_bytes, "log_telemetry_allowance_bytes": log_telemetry_allowance,
        "temporary_allowance_bytes": temporary_allowance, "required_free_bytes": required,
        "required_free_vram_mib": required_free_vram_mib,
        "runs": runs, "benchmark_after_training": False,
    }
