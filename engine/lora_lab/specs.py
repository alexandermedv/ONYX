from __future__ import annotations

from pathlib import Path

from .io import read_json
from .models import BenchmarkScene, BenchmarkSpec, BenchmarkStage, TrainingSpec


def load_training_spec(path: Path) -> TrainingSpec:
    raw = read_json(path)
    for key in ("resolution", "checkpoint_fractions"):
        raw[key] = tuple(raw[key])
    return TrainingSpec(**raw)


def load_benchmark_spec(path: Path) -> BenchmarkSpec:
    raw = read_json(path)
    scenes = tuple(BenchmarkScene(**scene) for scene in raw.pop("scenes"))
    stages = []
    for stage in raw.pop("stages"):
        for key in ("datasets", "scenes", "seeds", "weights", "checkpoints"):
            stage[key] = tuple(stage[key])
        stages.append(BenchmarkStage(**stage))
    return BenchmarkSpec(scenes=scenes, stages=tuple(stages), **raw)
