# Local PuLID/FLUX baseline v1 — P01 adapter

## Purpose and scope

This is a narrow, reproducible local-adapter preparation for frozen `P01 v1.0`. It is not a production workflow and not a completed cross-model benchmark. The intended first task is one deterministic `BUS_01` smoke, followed only after validation by a separate baseline decision.

## Adapter contract

- Adapter workflow: `workflows/ONYX_P01_PuLID_FLUX_v0.1_api.json`
- Adapter SHA-256: `29542e811a0e61cfe14121d47dbf47391e69f11ba21d3903c97694279826d5fa`
- Preserved source template: `../../comfyui-workflows/ONYX_PuLID_FLUX_v0.1_api.json`
- Source-template SHA-256: `1768760d13336b4f1fc6baecb29dc336955699a60ff33fbccd60aff2306e5d55`

The adapter only replaces the external prompt, deterministic seed and `SaveImage` output prefix, and replaces the source identity images with P01 references. It preserves the original PuLID/FLUX model selections and sampler contract: `768x1024`, Euler, simple scheduler, 20 steps, denoise `1.0`, Flux guidance `3.5`, and PuLID weight `0.9` from start `0.0` through end `1.0`.

## Strict identity inputs

The native multi-reference graph uses `LoadImage` nodes `67` (REF01), `68` (REF02) and `54` (REF03), batches them at node `66`, then supplies the result to `ApplyPulidFlux` node `62`. The three runtime-staged PNGs have byte-identical SHA-256 values to the frozen canonical references. `P01 Identity Master` is neither referenced nor used.

This makes the graph capable of strict reference provenance, but a completed successful output is still required before it can become benchmark evidence.

## Runtime and dependencies

The canonical local runtime is ComfyUI on `http://127.0.0.1:8188`, started with:

```powershell
cd D:\AI\ComfyUI_Flux
.\python_embeded\python.exe -s ComfyUI\main.py --windows-standalone-build --disable-async-offload --disable-pinned-memory
```

The local adapter uses existing `flux1-dev.safetensors`, `t5xxl_fp8_e4m3fn.safetensors`, `clip_l.safetensors`, `ae.safetensors`, `pulid_flux_v0.9.1.safetensors`, local EVA-CLIP and InsightFace `antelopev2`. No package installation or model download is part of this baseline.

## Smoke status

The first permitted request, `local_adapter_smoke_v1`, was sent with seed `748412438238144`. It reached FLUX dynamic-VRAM preparation but did not execute a sampler step or write an image. It was deliberately interrupted after `569.91` seconds, with the server recording `execution_interrupted` at `SamplerCustomAdvanced`.

The adapter is graph-valid and three-reference capable, but **not smoke-validated or ready for a local benchmark series**. Do not retry or tune it under this baseline record. A separate runtime diagnosis and explicit authorization are required before another GPU attempt.

The full immutable record is [run_manifest.yaml](P01_M30_Corporate/03_benchmark_runs/local_adapter_smoke_v1/run_manifest.yaml).

## Authorized follow-up, 2026-09-10

The separate [v2 attempt](P01_M30_Corporate/03_benchmark_runs/local_pulid_baseline_v2/README.md) resolved EVA from the existing shared Hugging Face cache with no download or model relocation. Exactly one P01 request was submitted using a process-local offline launcher with dynamic VRAM disabled. It failed with a native access violation during FLUX initialization, before sampling or identity conditioning could be verified. No image was produced. The adapter remains unvalidated for a benchmark series; see the v2 manifest and logs for evidence. Production Pilot and mini-LoRA were unchanged.

## Current status: v3 technical baseline passed

After the user pointed back to [[ComfyUI FLUX Windows Runbook]], the [v3 attempt](P01_M30_Corporate/03_benchmark_runs/local_pulid_baseline_v3/README.md) restored its required configuration: DynamicVRAM enabled, async offload and pinned memory disabled. V2 incorrectly departed from the documented configuration and is not a canonical-runtime test.

One P01 BUS_01 image completed in **348.15 seconds**, with unchanged generation parameters and all three verified references. The technical baseline passed; identity quality and comparison against `mini_5__1250` remain separate work. No generation followed success.
