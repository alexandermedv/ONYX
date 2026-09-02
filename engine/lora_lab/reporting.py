from __future__ import annotations

from pathlib import Path

from .io import write_csv, write_json


RESULT_COLUMNS = (
    "model", "photos", "train_time_seconds", "best_checkpoint", "optimizer_step",
    "effective_epochs", "time_to_best_checkpoint_seconds", "identity_mean", "identity_p10",
    "identity_min", "quality_pass_rate", "yield_rate", "human_score",
)


def serialize_results(output_dir: Path, results: list[dict]) -> None:
    write_json(output_dir / "experiment_results.json", {"schema": "onyx.lora_lab.results", "schema_version": "1.0", "results": results})
    write_csv(output_dir / "experiment_results.csv", [{key: row.get(key) for key in RESULT_COLUMNS} for row in results])
