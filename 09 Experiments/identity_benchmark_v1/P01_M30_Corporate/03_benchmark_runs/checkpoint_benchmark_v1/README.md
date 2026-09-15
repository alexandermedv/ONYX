# P01 checkpoint benchmark v1

This completed the approved six-image technical checkpoint comparison for
`P01_M30_Corporate`. It is generation evidence only: no training, PuLID rerun,
quality assessment, identity ranking, seed sweep, postprocessing, or upscaling
was performed.

## Runtime and contract

ComfyUI was launched twice from `D:\AI\ComfyUI_Flux` with the canonical
[[ComfyUI FLUX Windows Runbook]] flags:

```powershell
.\python_embeded\python.exe -s ComfyUI\main.py `
  --windows-standalone-build `
  --disable-async-offload `
  --disable-pinned-memory
```

DynamicVRAM was left enabled. Each temporary server also received an ONYX-owned
`extra_model_paths.yaml`, output directory and user directory. The YAML was
loaded only for that process, so no checkpoint was copied, linked, moved or
written into the external ComfyUI installation. `mini-3` and `mini-5` used
separate servers; each was released through `/free` and then stopped.

The existing PuLID v3 result was reused only as a manifest-referenced baseline:
its output SHA-256 is `33e7089c50613c13796e66dc5edaba6ddce2dabd147e3a79e4ab11798b7a211c`.
It was not submitted again.

All six mini-LoRA requests used P01 / BUS_01, seed `748412438238144`,
768x1024, 20 steps, Euler/simple, denoise `1.0`, LoRA weight `1.0`, and
`photo of p01onyx man` followed by the canonical BUS_01 prompt. The mini-LoRA
workflow contract uses KSampler CFG `1.0`; no PuLID FluxGuidance `3.5` was
applied.

## Technical outputs

| Variant | PNG SHA-256 | Server seconds |
| --- | --- | ---: |
| mini-3 @ 750 | `6b0aa8c93274d7504cedc98f5a704f2b0924ea766e88359e48586bc0f744028c` | 314.008 |
| mini-3 @ 1000 | `6f68e8befa68461acbb1da4ddab2be0c3399b0e325afd9915a7765e685c55928` | 246.492 |
| mini-3 @ 1250 | `3ee2a42616617a8e8f9406e0a07738e83f8b8096339b9a69d068d04ce8f1b929` | 244.472 |
| mini-5 @ 750 | `930c55cc1d916da90223693c0068c539c0616152dfbbfc6acf27a73ce06d514d` | 300.876 |
| mini-5 @ 1000 | `141af3d27f263cfdaae2856cdf479755830757ea080af5bb56142a6554df9f5e` | 247.446 |
| mini-5 @ 1250 | `042c739da93362505183063a63ac9c29b8a6c5678be9fb18e27f75b297660255` | 245.559 |

All six PNGs decode successfully as `768x1024`. Per-request workflow JSON,
ComfyUI history, checkpoint SHA-256, timing and before/after RAM, commit and
VRAM snapshots are saved under `requests/`, `history/` and `manifests/`.
[run_manifest.json](run_manifest.json) is the aggregate record and
[technical_validation.json](technical_validation.json) contains the six-file
technical validation.

After the final server stop, no compute Python process remained on the GPU.
The final snapshot stored in the aggregate manifest reports 724 MiB used and
23,602 MiB free, attributable to desktop processes.
