# P01 PuLID baseline v2 — failed before sampling

Date: 2026-09-10 (Europe/Moscow). ONYX HEAD: `1999980a17f121e1f229675ce8fff1b43615aa0c`, branch `main`, initially clean. Exactly one request was submitted; no retry, sweep, mini-LoRA generation or Production Pilot change occurred.

## EVA finding

The installed Flux node uses `create_model_and_transforms('EVA02-CLIP-L-14-336', 'eva_clip', force_custom_clip=True)`. Its pretrained registry selects `QuanSun/EVA-CLIP/EVA02_CLIP_L_336_psz14_s6B.pt` through `hf_hub_download`, with no explicit cache directory. It does not look in ComfyUI's clip_vision directory. The node UI has no local-path input; the underlying factory does support a path as the pretrained argument.

The existing file is:

`D:\AI\Cache\huggingface\hub\models--QuanSun--EVA-CLIP\snapshots\11afd202f2ae80869d6cef18b1ec775e79bd8d12\EVA02_CLIP_L_336_psz14_s6B.pt`

- Size: 856,461,210 bytes.
- Modified: 2026-06-30 02:50:41.2412391 +03:00.
- SHA256: `84c3a17a228c567a155259b2245b0b59072bf7da510260a0a02ec54de6d50b05` (verified again after the attempt).
- `HF_HUB_CACHE` already points to `D:\AI\Cache\huggingface\hub`.
- `hf_hub_download(..., local_files_only=True)` successfully resolved this exact file. No copy, symlink, download or loader edit was needed.

The earlier search scope excluded this shared cache. No EVA filename candidate was found within either permitted ComfyUI installation, including hidden files. The user then explicitly authorized inspecting this specific cache repository. This explains the empty filename search; it does not prove EVA was the cause of the earlier stalled sampler.

## Runtime and dependencies

Used `D:\AI\ComfyUI_Flux`, ComfyUI commit `b1693ecba9f5b65f8c80ab36b195ab963ec92413`, version 0.30.0, existing Python 3.13.14 / PyTorch 2.13.0+cu130 on RTX 3090. No versions were changed.

PuLID Flux node commit: `a80912fc3435c358607bf4b43a58dbcbebdb09ff`. Its pre-existing `forward_orig(..., **kwargs)` change was preserved. The other installation contains SDXL `pulid_comfyui`, commit `135abed8da169e33ab0b86550e05e3ae55d6df8c`.

Confirmed local files: `models/pulid/pulid_flux_v0.9.1.safetensors`, all five ONNX files under `models/insightface/models/antelopev2`, `models/diffusion_models/flux1-dev.safetensors`, `models/text_encoders/{clip_l,t5xxl_fp8_e4m3fn}.safetensors`, `models/vae/ae.safetensors`. Facexlib's existing detection_Resnet50_Final, parsing_parsenet and parsing_bisenet weights were also found. Full paths and SHA256 for identity-related files are in the manifest. Presence/preflight is not evidence that these all loaded during the failed generation.

Both required custom node packages loaded; `BatchImagesNode` is built into this ComfyUI version. `/object_info` contained every class in the workflow. All three canonical references and staged inputs matched the frozen hashes.

## Isolated changes and attempt

The actual API JSON is in `outputs/workflow_api.json`. Relative to the existing P01 adapter, only SaveImage's prefix changed to `P01_BUS_01_PULID_BASELINE`; the source adapter remains unchanged. The disconnected GGUF loader was retained and does not feed generation.

Parameters: BUS_01 corporate portrait, seed `748412438238144`, 768x1024, batch 1, Euler/simple, 20 steps, denoise 1.0, guidance 3.5, PuLID weight 0.9 over 0.0–1.0. REF01–REF03 feed the native image batch; no identity master is used.

The run-local launcher enabled HF offline settings, a Python socket audit guard rejecting non-loopback connections, and a PuLID/GGUF custom-node whitelist. It disabled dynamic VRAM for this process because the previous attempt stalled during dynamic-VRAM model preparation. This was a diagnostic runtime choice, not a proven fix. Output was redirected here. No external source/configuration files were edited; normal runtime database initialization attempted a lock write and failed with WinError 5.

Prompt `2c9434ab-87bb-4416-a15b-9f478839fa0e` was accepted with no node validation errors. The runtime then logged **Windows fatal exception: access violation** while constructing a `torch.nn.Linear` inside the FLUX model under UNETLoader. No sampler step or output image was recorded. Reference identity conditioning was therefore not verified in execution. The cause of the native exception is undiagnosed; it must not be labelled an EVA failure or proven memory exhaustion.

No external model download was observed; EVA resolution used local-files-only and the server had HF offline enabled. There were no model copies or links. The created server process was stopped after recording the fatal exception. No second request was submitted.

Completed generation time: unavailable. GPU sampling continued through approximately 40.52 seconds after submission; this is not generation duration or a precise crash timestamp. Sampled peak total GPU memory was 1,092 MiB, including other GPU consumers. Logs also record optional backend/deprecation warnings and a database lock permission error; the latter did not prevent server startup.

## Evidence and next-stage readiness

[run_manifest.json](run_manifest.json) records parameters, provenance and failure status. Local ignored `outputs/` contains the exact request, submission response, launcher, controller, reference hashes, identity-weight hashes, system stats, VRAM samples and stdout/stderr. There is no output PNG and no completed ComfyUI history record.

EVA discovery is resolved. A successful P01 baseline is still required before direct comparison against accepted mini-LoRA `mini_5__1250`; the native FLUX initialization exception is the current technical blocker. Runtime diagnosis and another GPU attempt are separate follow-up work. No architecture change or ADR was introduced.


## Follow-up correction

V2's `--disable-dynamic-vram` contradicted [[ComfyUI FLUX Windows Runbook]]. This was an agent error. The separate [v3 canonical attempt](../local_pulid_baseline_v3/README.md) subsequently succeeded. The blocker assessment above describes the state before v3; the original failure evidence is preserved.
