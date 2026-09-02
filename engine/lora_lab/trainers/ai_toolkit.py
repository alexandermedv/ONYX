from __future__ import annotations

import json
from pathlib import Path

from ..models import TrainingSpec


def render_ai_toolkit_config(spec: TrainingSpec, run: dict, dataset_folder: str) -> dict:
    """Render AI-Toolkit's config structure without launching it."""
    checkpoint_steps = run["checkpoint_steps"]
    regular_interval = len(checkpoint_steps) > 1 and len(set(
        b - a for a, b in zip(checkpoint_steps, checkpoint_steps[1:])
    )) == 1
    save_every = checkpoint_steps[0] if regular_interval else min(checkpoint_steps)
    return {
        "job": "extension",
        "config": {
            "name": run["run_id"],
            "process": [{
                "type": "diffusion_trainer",
                "training_folder": spec.output_root,
                "sqlite_db_path": str(Path(spec.ai_toolkit_root) / "aitk_db.db"),
                "device": spec.device,
                "trigger_word": spec.trigger_word,
                "performance_log_every": 10,
                "network": {
                    "type": "lora", "linear": spec.rank, "linear_alpha": spec.alpha,
                    "conv": spec.conv_rank, "conv_alpha": spec.conv_alpha,
                    "lokr_full_rank": True, "lokr_factor": -1,
                    "network_kwargs": {"ignore_if_contains": []},
                },
                "save": {
                    "dtype": spec.precision, "save_every": save_every,
                    "max_step_saves_to_keep": len(checkpoint_steps),
                    "save_format": "diffusers", "push_to_hub": False,
                },
                "datasets": [{
                    "folder_path": dataset_folder, "mask_path": None,
                    "mask_min_value": 0.1, "default_caption": "", "caption_ext": "txt",
                    "caption_dropout_rate": spec.caption_dropout_rate,
                    "cache_latents_to_disk": False, "is_reg": False,
                    "network_weight": 1, "resolution": list(spec.resolution),
                    "controls": [], "shrink_video_to_frames": True, "num_frames": 1,
                    "flip_x": False, "flip_y": False, "num_repeats": 1,
                }],
                "train": {
                    "batch_size": spec.batch_size, "bypass_guidance_embedding": False,
                    "steps": run["optimizer_steps"],
                    "gradient_accumulation": spec.gradient_accumulation,
                    "train_unet": True, "train_text_encoder": False,
                    "gradient_checkpointing": True, "noise_scheduler": "flowmatch",
                    "optimizer": spec.optimizer, "timestep_type": "sigmoid",
                    "content_or_style": "balanced",
                    "optimizer_params": {"weight_decay": 0.0001},
                    "unload_text_encoder": False, "cache_text_embeddings": False,
                    "lr": spec.learning_rate, "ema_config": {"use_ema": False, "ema_decay": 0.99},
                    "skip_first_sample": True, "force_first_sample": False,
                    "disable_sampling": True, "dtype": spec.precision,
                    "diff_output_preservation": False,
                    "diff_output_preservation_multiplier": 1,
                    "diff_output_preservation_class": "person",
                    "switch_boundary_every": 1, "loss_type": "mse",
                },
                "logging": {"log_every": 1, "use_ui_logger": True},
                "model": {
                    "name_or_path": spec.base_model, "quantize": True, "qtype": "qfloat8",
                    "quantize_te": True, "qtype_te": "qfloat8", "arch": "flux",
                    "low_vram": False, "model_kwargs": {}, "compile": False,
                },
                "sample": {
                    "sampler": "flowmatch", "sample_every": spec.sample_interval,
                    "sample_start_step": 0, "width": 1024, "height": 1024,
                    "samples": [], "neg": "", "seed": spec.seed,
                    "walk_seed": False, "guidance_scale": 4, "sample_steps": 30,
                    "num_frames": 1, "fps": 1,
                },
            }],
        },
        "meta": {"name": run["run_id"], "version": "1.0", "dry_run_render": True},
    }


def config_as_yaml(config: dict) -> str:
    """Stable JSON is valid YAML 1.2 and avoids adding a runtime YAML dependency."""
    return json.dumps(config, indent=2, ensure_ascii=False) + "\n"
