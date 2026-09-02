from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

from .io import read_json, write_json


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def gpu_snapshot() -> dict:
    result = subprocess.run([
        "nvidia-smi", "--query-gpu=name,memory.total,memory.used,memory.free,driver_version",
        "--format=csv,noheader,nounits",
    ], check=True, capture_output=True, text=True)
    name, total, used, free, driver = [value.strip() for value in result.stdout.strip().split(",")]
    return {"name": name, "memory_total_mib": int(total), "memory_used_mib": int(used),
            "memory_free_mib": int(free), "driver": driver}


def expected_output_contract(run: dict) -> dict:
    output = Path(run["output_directory"])
    name = run["run_id"]
    steps = sorted({int(step) for step in run["checkpoint_steps"]})
    if not steps:
        raise ValueError(f"run has no checkpoint steps: {name}")
    final_step = int(run.get("optimizer_steps", steps[-1]))
    intermediate = [
        output / f"{name}_{step:09d}.safetensors"
        for step in steps if step != final_step
    ]
    final_numbered = output / f"{name}_{final_step:09d}.safetensors"
    final_unnumbered = output / f"{name}.safetensors"
    return {
        "intermediate": intermediate,
        "final_step": final_step,
        "final_alternatives": [final_numbered, final_unnumbered],
    }


def missing_expected_outputs(run: dict) -> list[str]:
    contract = expected_output_contract(run)
    missing = [str(path) for path in contract["intermediate"] if not path.is_file()]
    final_alternatives = contract["final_alternatives"]
    if not any(path.is_file() for path in final_alternatives):
        missing.append("one_of: " + " | ".join(str(path) for path in final_alternatives))
    return missing


def validate_dataset(path: Path, expected: int) -> dict:
    images = [item for item in path.iterdir() if item.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}]
    captions = list(path.glob("*.txt"))
    if len(images) != expected or len(captions) != expected:
        raise RuntimeError(f"dataset count mismatch at {path}: images={len(images)} captions={len(captions)} expected={expected}")
    return {"path": str(path), "images": len(images), "captions": len(captions)}


def preflight(plan: dict, allow_completed: bool = False, resume_run_id: str | None = None) -> dict:
    toolkit_root = Path(plan["ai_toolkit_root"])
    python = Path(plan["python"])
    model = Path(plan["base_model"])
    if not python.is_file() or not (toolkit_root / "run.py").is_file() or not model.exists():
        raise RuntimeError("AI-Toolkit python/run.py or base model is missing")
    gpu = gpu_snapshot()
    required_free_vram = int(plan.get("required_free_vram_mib", 0))
    if gpu["memory_free_mib"] < required_free_vram:
        raise RuntimeError(
            f"insufficient free VRAM: free={gpu['memory_free_mib']} MiB "
            f"required={required_free_vram} MiB; stop other GPU workloads before launch"
        )
    datasets = []
    outputs = []
    for run in plan["runs"]:
        config = Path(run["config"])
        if not config.is_file():
            raise RuntimeError(f"missing config: {config}")
        datasets.append(validate_dataset(Path(run["dataset"]), int(run["dataset_size"])))
        output = Path(run["output_directory"])
        exists = output.exists()
        if exists and not allow_completed and run["run_id"] != resume_run_id:
            raise FileExistsError(f"output collision: {output}")
        outputs.append({"run_id": run["run_id"], "path": str(output), "exists": exists})
    usage = shutil.disk_usage(Path(plan["output_root"]).anchor)
    required = int(plan["required_free_bytes"])
    if usage.free < required:
        raise RuntimeError(f"insufficient disk: free={usage.free} required={required}")
    return {"checked_at": utc_now(), "gpu": gpu, "datasets": datasets, "outputs": outputs,
            "disk": {"free_bytes": usage.free, "required_free_bytes": required}}


def load_state(plan: dict) -> dict:
    path = Path(plan["state_file"])
    return read_json(path) if path.exists() else {"schema": "onyx.lora_lab.night_run_state", "runs": {}}


def save_state(plan: dict, state: dict) -> None:
    write_json(Path(plan["state_file"]), state)


def run_one(plan: dict, run: dict, state: dict) -> int:
    logs = Path(plan["log_root"])
    logs.mkdir(parents=True, exist_ok=True)
    stdout_path = logs / f"{run['run_id']}.stdout.log"
    stderr_path = logs / f"{run['run_id']}.stderr.log"
    started = time.time()
    record = {"status": "running", "started_at": utc_now(), "started_at_unix": started,
              "config": run["config"], "output_directory": run["output_directory"], "peak_vram_mib": 0}
    state["runs"][run["run_id"]] = record
    save_state(plan, state)
    command = [plan["python"], str(Path(plan["ai_toolkit_root"]) / "run.py"), run["config"]]
    with stdout_path.open("w", encoding="utf-8") as stdout, stderr_path.open("w", encoding="utf-8") as stderr:
        process = subprocess.Popen(command, cwd=plan["ai_toolkit_root"], stdout=stdout, stderr=stderr)
        while process.poll() is None:
            try:
                record["peak_vram_mib"] = max(record["peak_vram_mib"], gpu_snapshot()["memory_used_mib"])
            except Exception:
                pass
            time.sleep(2)
    ended = time.time()
    missing = missing_expected_outputs(run)
    record.update({"status": "completed" if process.returncode == 0 and not missing else "failed",
                   "ended_at": utc_now(), "ended_at_unix": ended, "duration_seconds": ended - started,
                   "exit_code": process.returncode, "stdout_log": str(stdout_path), "stderr_log": str(stderr_path),
                   "missing_expected_outputs": missing})
    save_state(plan, state)
    return 0 if record["status"] == "completed" else (process.returncode or 1)


def start(plan: dict, resume_run_id: str | None = None, acknowledge_existing: bool = False) -> int:
    state = load_state(plan)
    if resume_run_id:
        if not acknowledge_existing:
            raise RuntimeError("resume requires --acknowledge-existing-output")
        ids = [run["run_id"] for run in plan["runs"]]
        if resume_run_id not in ids:
            raise ValueError(f"unknown resume run: {resume_run_id}")
        runs = plan["runs"][ids.index(resume_run_id):]
        preflight(plan, allow_completed=True, resume_run_id=resume_run_id)
    else:
        runs = plan["runs"]
        preflight(plan)
    for run in runs:
        prior = state["runs"].get(run["run_id"], {})
        if prior.get("status") == "completed":
            continue
        if prior and not resume_run_id:
            raise RuntimeError(f"run has prior state and needs explicit resume: {run['run_id']}")
        exit_code = run_one(plan, run, state)
        if exit_code:
            return exit_code
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="ONYX sequential LoRA night-run launcher")
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("preflight", "status", "start", "resume"):
        command = commands.add_parser(name)
        command.add_argument("--plan", required=True, type=Path)
        if name == "resume":
            command.add_argument("--run-id", required=True)
            command.add_argument("--acknowledge-existing-output", action="store_true")
    args = parser.parse_args()
    plan = read_json(args.plan)
    if args.command == "preflight":
        print(json.dumps(preflight(plan), indent=2, ensure_ascii=False))
        return 0
    if args.command == "status":
        print(json.dumps(load_state(plan), indent=2, ensure_ascii=False))
        return 0
    if args.command == "start":
        return start(plan)
    return start(plan, args.run_id, args.acknowledge_existing_output)


if __name__ == "__main__":
    raise SystemExit(main())
