from __future__ import annotations

import platform
import subprocess
import sys
import time
from pathlib import Path


def environment_snapshot(repo_root: Path) -> dict:
    def command(*args: str) -> str | None:
        try:
            return subprocess.run(args, cwd=repo_root, check=True, capture_output=True, text=True).stdout.strip()
        except (OSError, subprocess.SubprocessError):
            return None
    return {
        "captured_at_unix": time.time(), "python": sys.version, "platform": platform.platform(),
        "git_commit": command("git", "rev-parse", "HEAD"),
        "gpu": command("nvidia-smi", "--query-gpu=name", "--format=csv,noheader"),
        "cuda_driver": command("nvidia-smi", "--query-gpu=driver_version", "--format=csv,noheader"),
    }


def checkpoint_telemetry(checkpoint: Path, optimizer_step: int, run_started_at: float,
                         dataset_size: int, effective_batch: int = 1) -> dict:
    saved_at = checkpoint.stat().st_mtime
    return {
        "checkpoint": str(checkpoint), "optimizer_step": optimizer_step,
        "saved_at_unix": saved_at, "training_elapsed_seconds": max(0.0, saved_at - run_started_at),
        "effective_epochs": optimizer_step * effective_batch / dataset_size,
        "checkpoint_size_bytes": checkpoint.stat().st_size,
    }
