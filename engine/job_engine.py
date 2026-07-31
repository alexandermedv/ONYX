#!/usr/bin/env python3
"""Minimal sequential orchestrator for the commercial AI portrait pipeline."""

from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGES = ("scene_generator", "facefusion", "postprocessor")
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, data: dict[str, Any]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
    temporary.replace(path)


def image_count(folder: Path) -> int:
    if not folder.exists():
        return 0
    return sum(p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS for p in folder.iterdir())


def format_command(template: list[str], values: dict[str, str]) -> list[str]:
    try:
        return [part.format_map(values) for part in template]
    except KeyError as exc:
        raise ValueError(f"Unknown placeholder in command: {exc.args[0]}") from exc


def initial_state(job: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "job_id": job["job_id"],
        "status": "pending",
        "created_at": utc_now(),
        "updated_at": utc_now(),
        "stages": {name: {"status": "pending"} for name in STAGES},
    }


def validate_job(job: dict[str, Any]) -> None:
    required = ("schema_version", "job_id", "paths", "pipeline")
    missing = [key for key in required if key not in job]
    if missing:
        raise ValueError(f"Missing job fields: {', '.join(missing)}")
    if job["schema_version"] != "1.0":
        raise ValueError("Only schema_version 1.0 is supported")
    for stage in STAGES:
        if stage not in job["pipeline"]:
            raise ValueError(f"Missing pipeline stage: {stage}")
        cfg = job["pipeline"][stage]
        if cfg.get("enabled", True) and not isinstance(cfg.get("command"), list):
            raise ValueError(f"pipeline.{stage}.command must be a JSON array")


def resolve_job_path(job_dir: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else (job_dir / path).resolve()


def stage_paths(job_dir: Path) -> dict[str, Path]:
    return {
        "source": job_dir / "01_source",
        "scenes": job_dir / "02_scenes",
        "face_swapped": job_dir / "03_face_swapped",
        "final": job_dir / "04_final",
        "logs": job_dir / "logs",
    }


def clear_generated_outputs(paths: dict[str, Path]) -> None:
    """Remove generated outputs without touching client source photos."""
    for key in ("scenes", "face_swapped", "final", "logs"):
        folder = paths[key]
        if folder.exists():
            shutil.rmtree(folder)
        folder.mkdir(parents=True, exist_ok=True)


def run_job(
    job_file: Path,
    restart: bool = False,
    dry_run: bool = False,
    stop_after: str | None = None,
) -> int:
    job_file = job_file.resolve()
    job_dir = job_file.parent
    job = read_json(job_file)
    validate_job(job)
    paths = stage_paths(job_dir)
    if restart and not dry_run:
        clear_generated_outputs(paths)
    for folder in paths.values():
        folder.mkdir(parents=True, exist_ok=True)

    state_path = job_dir / "state.json"
    state = initial_state(job) if restart or not state_path.exists() else read_json(state_path)
    state["status"] = "running"
    state["updated_at"] = utc_now()
    write_json(state_path, state)

    stage_io = {
        "scene_generator": (paths["source"], paths["scenes"]),
        "facefusion": (paths["scenes"], paths["face_swapped"]),
        "postprocessor": (paths["face_swapped"], paths["final"]),
    }
    values = {
        "python": sys.executable,
        "job_dir": str(job_dir),
        "job_file": str(job_file),
        **{f"{key}_dir": str(value) for key, value in paths.items()},
    }
    for key, value in job.get("paths", {}).items():
        if isinstance(value, str):
            values[key] = str(resolve_job_path(job_dir, value))

    try:
        for stage in STAGES:
            cfg = job["pipeline"][stage]
            stage_state = state["stages"].setdefault(stage, {"status": "pending"})
            if not cfg.get("enabled", True):
                stage_state.update(status="skipped", finished_at=utc_now())
                write_json(state_path, state)
                continue
            if stage_state.get("status") == "completed" and not restart:
                print(f"[SKIP] {stage}: already completed")
                continue

            input_dir, output_dir = stage_io[stage]
            values.update(input_dir=str(input_dir), output_dir=str(output_dir), stage=stage)
            command = format_command(cfg["command"], values)
            stage_state.update(status="running", started_at=utc_now(), command=command)
            write_json(state_path, state)
            print(f"[RUN ] {stage}: {shlex.join(command)}")

            if dry_run:
                stage_state.update(status="dry_run", finished_at=utc_now())
                write_json(state_path, state)
                continue

            started = time.monotonic()
            log_path = paths["logs"] / f"{stage}.log"
            environment = os.environ.copy()
            environment.update({str(k): str(v) for k, v in cfg.get("environment", {}).items()})
            with log_path.open("w", encoding="utf-8") as log:
                result = subprocess.run(
                    command,
                    cwd=cfg.get("working_directory") or str(job_dir),
                    env=environment,
                    stdout=log,
                    stderr=subprocess.STDOUT,
                    text=True,
                    check=False,
                )
            produced = image_count(output_dir)
            minimum = int(cfg.get("minimum_output_images", 1))
            if result.returncode != 0 or produced < minimum:
                reason = f"exit_code={result.returncode}, output_images={produced}, required={minimum}"
                stage_state.update(
                    status="failed", finished_at=utc_now(), duration_seconds=round(time.monotonic() - started, 2),
                    exit_code=result.returncode, output_images=produced, error=reason, log=str(log_path),
                )
                raise RuntimeError(f"{stage} failed: {reason}. See {log_path}")
            stage_state.update(
                status="completed", finished_at=utc_now(), duration_seconds=round(time.monotonic() - started, 2),
                exit_code=0, output_images=produced, log=str(log_path),
            )
            state["updated_at"] = utc_now()
            write_json(state_path, state)
            print(f"[ OK ] {stage}: {produced} image(s)")

            if stage == stop_after:
                state["status"] = "awaiting_review"
                state["updated_at"] = utc_now()
                state["review_folder"] = str(output_dir)
                write_json(state_path, state)
                print(f"Job {job['job_id']}: awaiting_review")
                print(f"Review folder: {output_dir}")
                print("Delete rejected images, then continue with: python job_engine.py <job.json>")
                print("Do not use --restart when continuing: it deletes reviewed scenes.")
                return 0

        state["status"] = "dry_run" if dry_run else "completed"
        state["updated_at"] = utc_now()
        state["finished_at"] = utc_now()
        write_json(state_path, state)
        print(f"Job {job['job_id']}: {state['status']}")
        return 0
    except Exception as exc:
        state["status"] = "failed"
        state["updated_at"] = utc_now()
        state["error"] = str(exc)
        write_json(state_path, state)
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Commercial AI Portrait Job Engine v1.3")
    parser.add_argument("job_file", type=Path, help="Path to job.json")
    parser.add_argument(
        "--restart",
        action="store_true",
        help="Clear generated outputs (02-04 and logs) and run all stages again",
    )
    parser.add_argument("--dry-run", action="store_true", help="Validate and print commands only")
    parser.add_argument(
        "--stop-after",
        choices=STAGES,
        help="Stop successfully after a stage so its output can be reviewed",
    )
    args = parser.parse_args()
    return run_job(
        args.job_file,
        restart=args.restart,
        dry_run=args.dry_run,
        stop_after=args.stop_after,
    )


if __name__ == "__main__":
    raise SystemExit(main())
