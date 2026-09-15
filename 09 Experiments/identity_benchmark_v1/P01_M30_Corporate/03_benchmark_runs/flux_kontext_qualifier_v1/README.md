# P01 FLUX Kontext qualifier v1

This local qualifier runs exactly three FLUX.1 Kontext Dev points: BUS_01, BUS_06/DESK and BUS_09/FULL. It reuses the existing working ComfyUI workflow `KontextDev_beard_removal_success_best_pre_identity.json`, specifically its `Image Edit (Flux.1 Kontext Dev)` subgraph, as a compact API graph.

The graph is a single reference-conditioned edit pass: `LoadImage → ImageStitch (one connected primary input) → FluxKontextImageScale → VAEEncode → ReferenceLatent → FluxGuidance → KSampler → VAEDecode`. The reference latent is also the sampler latent, exactly as in the reused working graph. It has no LoRA, PuLID node, hidden second pass, reroll, postprocessing or selection stage.

REF01 is the connected primary identity input because this established graph has one connected primary input. Its staged ComfyUI copy is SHA256-verified against the canonical P01 REF01. REF02 and REF03 are not connected; this method limitation is recorded in `run_plan.json` and `run_manifest.json`.

The reused Context settings are Flux guidance 2.5; KSampler 20 steps, CFG 1.0, Euler/simple and denoise 1.0. `FluxKontextImageScale` selects the model's native closest preferred vertical resolution from REF01; this is recorded from each actual decoded PNG rather than resizing the output to force 768×1024.

Runtime follows [ComfyUI FLUX Windows Runbook](../../../../../04%20Engineering/ComfyUI%20FLUX%20Windows%20Runbook.md): DynamicVRAM remains enabled and ComfyUI starts with `--disable-async-offload` and `--disable-pinned-memory`.

## Completed execution

The bounded run completed on 2026-09-10 with exactly three outputs, one each for BUS_01, BUS_06 and BUS_09. All three decoded as PNG at the native `880×1184` selected by `FluxKontextImageScale`; no output was resized after generation. The manifest records exact prompts, seeds, source identity input, source workflow provenance, workflow/API JSON, timing, peak VRAM and output hashes. No visual QA, ranking, reroll, external model, LoRA, PuLID, postprocessing or Production Pilot action was performed.
