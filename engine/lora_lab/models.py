from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


SCHEMA_VERSION = "1.0"


class SpecError(ValueError):
    pass


@dataclass(frozen=True)
class DatasetSpec:
    dataset_id: str
    size: int
    manifest_path: str

    def __post_init__(self) -> None:
        if not self.dataset_id or self.size < 1 or not self.manifest_path:
            raise SpecError("dataset_id, positive size and manifest_path are required")


@dataclass(frozen=True)
class TrainingSpec:
    experiment_id: str
    base_model: str
    trigger_word: str
    resolution: tuple[int, ...]
    batch_size: int
    gradient_accumulation: int
    rank: int
    alpha: int
    conv_rank: int
    conv_alpha: int
    optimizer: str
    learning_rate: float
    scheduler: str
    fixed_steps: int
    fixed_exposure_epochs: float
    seed: int
    save_interval: int
    sample_interval: int
    precision: str
    device: str
    output_root: str
    ai_toolkit_root: str
    caption_dropout_rate: float = 0.0
    checkpoint_fractions: tuple[float, ...] = (0.2, 0.4, 0.6, 0.8, 1.0)

    def __post_init__(self) -> None:
        positive = {
            "batch_size": self.batch_size,
            "gradient_accumulation": self.gradient_accumulation,
            "rank": self.rank,
            "alpha": self.alpha,
            "fixed_steps": self.fixed_steps,
            "seed": self.seed,
        }
        invalid = [name for name, value in positive.items() if value < 1]
        if invalid:
            raise SpecError(f"positive values required: {', '.join(invalid)}")
        if not self.trigger_word.strip() or any(r < 64 for r in self.resolution):
            raise SpecError("trigger_word and valid resolutions are required")
        if not 0 <= self.caption_dropout_rate <= 1:
            raise SpecError("caption_dropout_rate must be between 0 and 1")


@dataclass(frozen=True)
class BenchmarkScene:
    scene_id: str
    prompt: str
    width: int
    height: int
    diagnostic: bool = False


@dataclass(frozen=True)
class BenchmarkStage:
    stage_id: str
    datasets: tuple[str, ...]
    scenes: tuple[str, ...]
    seeds: tuple[int, ...]
    weights: tuple[float, ...]
    checkpoints: tuple[int | str, ...]
    checkpoint_mode: str
    include_historical_control: bool = False

    def __post_init__(self) -> None:
        if self.checkpoint_mode not in {"explicit", "best"}:
            raise SpecError("checkpoint_mode must be explicit or best")
        if not all((self.datasets, self.scenes, self.seeds, self.weights, self.checkpoints)):
            raise SpecError("benchmark matrix axes must not be empty")


@dataclass(frozen=True)
class BenchmarkSpec:
    benchmark_id: str
    scenes: tuple[BenchmarkScene, ...]
    stages: tuple[BenchmarkStage, ...]
    inference_steps: int
    guidance: float
    sampler: str
    scheduler: str


@dataclass
class SourceRecord:
    source_id: str
    source_path: str
    sha256: str
    width: int
    height: int
    face_detected: bool
    face_count: int
    face_area_ratio: float | None
    yaw: float | None
    pitch: float | None
    roll: float | None
    pose_bucket: str
    sharpness: float
    exposure_mean: float
    exposure_low_fraction: float
    exposure_high_fraction: float
    identity_similarity: float | None
    quality_flags: list[str] = field(default_factory=list)
    historical_full_21: bool = False
    selected_memberships: list[str] = field(default_factory=list)
    selection_rank: int | None = None
    diversity_contribution: float | None = None
    selection_reason: str = ""
    caption: str = ""
    perceptual_hash: str = ""
    perceptual_distance: float | None = None
    capture_group: str = ""
    expression_bucket: str = "unknown"
    lighting_bucket: str = "unknown"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CheckpointMetrics:
    checkpoint: str
    optimizer_step: int
    effective_epochs: float
    training_elapsed_seconds: float | None
    identity_mean: float | None
    identity_median: float | None
    identity_p10: float | None
    identity_min: float | None
    identity_max: float | None
    identity_std: float | None
    identity_pass_rate: float | None
    quality_pass_rate: float | None
    yield_rate: float | None


@dataclass(frozen=True)
class HistoricalControl:
    control_id: str
    checkpoint_path: str
    notes: str = ""
