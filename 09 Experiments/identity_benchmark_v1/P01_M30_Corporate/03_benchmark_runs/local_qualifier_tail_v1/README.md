# P01 local qualifier tail v1

This bounded run closes the local mini-LoRA portion of `identity_benchmark_v1` for the ONYX Model Arena. It creates only the 12 missing points: BUS_06 and BUS_09 for the six existing P01 mini-LoRA checkpoints. Existing BUS_01 checkpoint outputs and the completed three-scene PuLID qualifier are reused, not rerun.

The runner reads the resolved canonical prompts and fixed seeds from the completed sibling `pulid_multiscene_v1/scene_specs.json`. It applies the established mini-LoRA prompt policy: `photo of p01onyx man, ` followed by that canonical prompt.

Runtime follows [ComfyUI FLUX Windows Runbook](../../../../../04%20Engineering/ComfyUI%20FLUX%20Windows%20Runbook.md): DynamicVRAM remains enabled, while async offload and pinned memory are disabled. The mini-LoRA workflow contract is KSampler CFG 1.0, 20 steps, Euler/simple, denoise 1.0 and LoRA weight 1.0. Flux guidance is not applicable because this approved workflow has no FluxGuidance node.

`run_tail.py --check-only` validates the fixed contract and checkpoint hashes without contacting ComfyUI. A normal invocation processes exactly one three-checkpoint dataset group and each group produces six PNGs sequentially. Every completed point has its request, Comfy history, per-point manifest, output SHA256, PNG decode/dimension validation, timing and sampled GPU-memory telemetry. `run_manifest.json` combines both groups and `technical_validation.json` summarizes all twelve outputs.

## Completed execution

The controlled run completed on 2026-09-10 with exactly 12 PNG outputs: BUS_06 and BUS_09 for mini-3 and mini-5 at 750, 1000 and 1250. `technical_validation.json` records all 12 as decodable 768×1024 PNGs and includes their SHA-256 values. The runner sent `/free` after each dataset group; ComfyUI was then stopped. No PuLID run, LoRA training, BUS_01 rerun, QA/ranking, external-model run, postprocess or Production Pilot action was performed.
