# P01 PuLID baseline v3 — successful canonical runtime

2026-09-10, ONYX `main` at `1999980a17f121e1f229675ce8fff1b43615aa0c`.

One BUS_01 image completed successfully with the runtime prescribed by [[ComfyUI FLUX Windows Runbook]]. DynamicVRAM remained enabled; async offload and pinned memory were disabled. The preceding v2 attempt incorrectly added `--disable-dynamic-vram`, contrary to that runbook. V2 is not evidence of failure under the canonical configuration. The successful v3 result does not establish the exact native cause of v2's access violation.

## Exact runtime

Working directory: `D:\AI\ComfyUI_Flux`. Direct executable: `python_embeded\python.exe -s ComfyUI\main.py` with `--windows-standalone-build --disable-async-offload --disable-pinned-memory`. Neither `--disable-dynamic-vram` nor `--disable-mmap` was used; `comfy/utils.py` has no Git diff. Existing ComfyUI, PyTorch, CUDA and custom node versions were preserved.

Additional operational arguments only whitelist `ComfyUI-PuLID-Flux` and `ComfyUI-GGUF` and redirect output/user directories into this run. Full arguments are saved in `outputs/argv.json`. HF_HUB_OFFLINE=1, TRANSFORMERS_OFFLINE=1 and HF_HUB_DISABLE_TELEMETRY=1 were inherited by the process. There is no runpy launcher or socket audit hook in v3. No model download was observed, and all required weights already existed. No model copy, symlink or external source/config edit was performed.

EVA was loaded from the existing shared cache:

`D:\AI\Cache\huggingface\hub\models--QuanSun--EVA-CLIP\snapshots\11afd202f2ae80869d6cef18b1ec775e79bd8d12\EVA02_CLIP_L_336_psz14_s6B.pt`

SHA256: `84c3a17a228c567a155259b2245b0b59072bf7da510260a0a02ec54de6d50b05`. Size: 856,461,210 bytes. Full identity-related model paths/hashes are in [run_manifest.json](run_manifest.json).

## Workflow and result

The existing P01 API adapter was retained, changing only SaveImage's prefix. Parameters: seed `748412438238144`, 768x1024, batch 1, 20 steps, Euler/simple, denoise 1.0, guidance 3.5, PuLID weight 0.9 from 0.0 through 1.0. FLUX.1-dev, PuLID v0.9.1, antelopev2, EVA and existing facexlib weights were used. All three canonical P01 references and staged inputs passed their frozen SHA256 checks. Identity Master and mini-LoRA were not inputs.

Prompt ID: `bb2980b3-8221-4d49-af30-43555c1f0aa4`. ComfyUI history reports `success`, `completed: true`, with no cached nodes. Logs confirm EVA/PuLID/InsightFace loading, completion of model initialization, 20/20 sampler steps and saving. The inspected ApplyPulidFlux implementation uses the reference batch and warns if it returns an unmodified model; no no-face/unmodified-model warning appeared. This verifies the execution path, not a quantitative identity quality threshold. No identity similarity score or cross-provider comparison was performed.

Output: [P01_BUS_01_PULID_BASELINE_00001_.png](outputs/P01_BUS_01_PULID_BASELINE_00001_.png).

- PNG: 768x1024, 750,711 bytes; visually inspected as a frontal corporate portrait.
- Output SHA256: `33e7089c50613c13796e66dc5edaba6ddce2dabd147e3a79e4ab11798b7a211c`.
- Server execution time: **348.15 seconds**, including cold model initialization (about four minutes).
- Sampled peak total GPU memory: **24,150 MiB**, including other GPU consumers.
- Minimum sampled free RAM: **18,529 MiB**; minimum free Windows commit: **10,206 MiB**.

RAM/commit snapshots use the existing read-only `memory_snapshot()` helper; no Production Pilot behavior was modified. The server created for this run was stopped after success. Exactly one v3 request was submitted. No sweep, second scene or mini-LoRA run followed.

## Warnings and evidence

Nonfatal messages: external default database lock permission error (the user-directory argument did not relocate its default DB URL), CLIP `text_projection.weight`, EVA rotary-buffer missing keys, package deprecations and optional backend notices. No fatal CUDA, node or missing-model error occurred in v3. These warnings remain recorded rather than being silently repaired.

Ignored local `outputs/` retains exact API workflow/request, submission, ComfyUI history, stdout/stderr, system stats, references, identity weights, argv, timing and RAM/commit/VRAM samples. `run_manifest.json` preserves the compact provenance. PNG metadata and API graph were checked; the only change from the source adapter is the output prefix.

This completes the one-image technical baseline. It does not establish commercial quality or superiority to `mini_5__1250`. No blocker from this execution prevents planning a separately authorized direct comparison. The canonical runbook remains authoritative; no architectural change or new ADR was needed.
