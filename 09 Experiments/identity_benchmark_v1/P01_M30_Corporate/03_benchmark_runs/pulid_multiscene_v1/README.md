# P01 PuLID multiscene v1

This is a bounded four-scene technical set for PuLID as an identity method.
It reuses the successful BUS_01 v3 evidence without rerunning it, then adds
exactly one generation each for BUS_03, BUS_06 (DESK) and BUS_09 (FULL).
It contains no mini-LoRA invocation, comparison, QA, ranking, sweep,
postprocessing or Production Pilot change.

## Runtime contract

The server ran from `D:\AI\ComfyUI_Flux` using the canonical
[[ComfyUI FLUX Windows Runbook]] command flags:

```powershell
.\python_embeded\python.exe -s ComfyUI\main.py `
  --windows-standalone-build `
  --disable-async-offload `
  --disable-pinned-memory
```

DynamicVRAM remained enabled. The existing `ComfyUI-PuLID-Flux` and
`ComfyUI-GGUF` whitelist from the successful v3 run was retained. All requests
used the same P01 REF01–REF03 set, PuLID `0.9` from `0.0` through `1.0`, Flux
guidance `3.5`, 768x1024, 20 steps, Euler/simple and denoise `1.0`.

The new scene prompts resolve existing `business_scene_pack_v1` SceneSpec
records. `BUS_06 — At the Desk` is the requested DESK scene; `BUS_09 — Full
Body` is the requested FULL scene. Exact resolved prompts and seeds are in
[scene_specs.json](scene_specs.json). No new global SceneSpec was necessary.

## Technical set

| Scene | Seed | PuLID | Resolution | Time (s) | Peak VRAM (MiB) | Success | Output |
| --- | ---: | ---: | --- | ---: | ---: | --- | --- |
| BUS_01 | 748412438238144 | 0.9 | 768x1024 | 348.150 | 24150 | reused | [existing v3 PNG](../local_pulid_baseline_v3/outputs/P01_BUS_01_PULID_BASELINE_00001_.png) |
| BUS_03 | 748412438238145 | 0.9 | 768x1024 | 323.149 | 24091 | yes | [PNG](outputs/P01_BUS_03_PULID_00001_.png) |
| BUS_06 / DESK | 748412438238146 | 0.9 | 768x1024 | 145.331 | 24132 | yes | [PNG](outputs/P01_BUS_06_PULID_00001_.png) |
| BUS_09 / FULL | 748412438238147 | 0.9 | 768x1024 | 30.140 | 24027 | yes | [PNG](outputs/P01_BUS_09_PULID_00001_.png) |

BUS_01 is referenced in the manifests and was not physically copied. All four
PNGs decode as 768x1024 and their SHA-256 values match the individual or v3
source manifest. See [technical_validation.json](technical_validation.json),
[run_manifest.json](run_manifest.json), and
[aggregate_manifest.json](aggregate_manifest.json) for exact provenance,
per-request telemetry and hashes.

ComfyUI-Manager could not reach its registry at startup and used its local
list; no model-weight download occurred. There were no sampler, CUDA, OOM or
native access-violation errors. The temporary server was stopped after the
series. Its final GPU snapshot was 912 MiB used and 23,414 MiB free, with only
desktop C+G processes remaining.
