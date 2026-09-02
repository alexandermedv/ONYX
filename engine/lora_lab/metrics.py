from __future__ import annotations

import math
import statistics


def percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * fraction
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)


def aggregate_metrics(rows: list[dict], identity_threshold: float) -> dict:
    scores = [float(row["identity_similarity"]) for row in rows if row.get("identity_similarity") is not None]
    total = len(rows)
    identity_passes = sum(row.get("identity_similarity") is not None and float(row["identity_similarity"]) >= identity_threshold for row in rows)
    quality_passes = sum(bool(row.get("quality_pass")) for row in rows)
    combined = sum(bool(row.get("quality_pass")) and row.get("identity_similarity") is not None and float(row["identity_similarity"]) >= identity_threshold for row in rows)
    return {
        "count": total, "identity_count": len(scores),
        "identity_mean": statistics.fmean(scores) if scores else None,
        "identity_median": statistics.median(scores) if scores else None,
        "identity_p10": percentile(scores, 0.10) if scores else None,
        "identity_min": min(scores) if scores else None, "identity_max": max(scores) if scores else None,
        "identity_std": statistics.pstdev(scores) if scores else None,
        "identity_pass_rate": identity_passes / total if total else None,
        "quality_pass_rate": quality_passes / total if total else None,
        "yield_rate": combined / total if total else None,
    }


def choose_best_checkpoint(rows: list[dict]) -> dict:
    if not rows:
        raise ValueError("checkpoint rows are required")
    def key(row: dict) -> tuple:
        return (row.get("yield_rate") if row.get("yield_rate") is not None else -1,
                row.get("identity_p10") if row.get("identity_p10") is not None else -1,
                row.get("identity_mean") if row.get("identity_mean") is not None else -1,
                -int(row["optimizer_step"]))
    best = max(rows, key=key)
    return {
        "best_checkpoint": best["checkpoint"], "optimizer_step": best["optimizer_step"],
        "effective_epochs": best["effective_epochs"],
        "time_to_best_checkpoint_seconds": best.get("training_elapsed_seconds"),
        "identity_metrics": {key: value for key, value in best.items() if key.startswith("identity_")},
        "quality_pass_rate": best.get("quality_pass_rate"), "yield_rate": best.get("yield_rate"),
    }
