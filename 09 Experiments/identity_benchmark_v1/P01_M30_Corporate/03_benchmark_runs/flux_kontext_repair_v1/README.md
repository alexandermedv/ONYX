# P01 FLUX Kontext repair v1

This is a separate two-image repair run, not a replacement for `flux_kontext_qualifier_v1`. The official qualifier and its two source outputs are SHA256-verified before the repair starts and are never written by this run.

The native FLUX.1 Kontext Dev graph, model, REF01 identity input, seeds, 20 steps, CFG 1.0, Flux guidance 2.5, Euler/simple, denoise 1.0 and `FluxKontextImageScale` behavior are identical to qualifier v1. The only generation change is positive-prompt wording for adult body scale and anatomy on BUS_06 and BUS_09.

The reused graph keeps `ConditioningZeroOut`; it has no editable text-negative input. Therefore no negative-prompt branch was added and no pipeline topology was changed. Context-specific anatomy requests appear only in the two positive prompts, saved exactly in the per-scene requests and manifests.

No PuLID, LoRA, reroll, sweep, postprocess, external model, QA/ranking, blind package or Production Pilot action is part of this repair.

## Completed technical record

The two requested repair outputs were completed on 2026-09-10 and decode as native `880×1184` PNGs. `FluxKontextImageScale` selected that size; no crop, resize, upscale or retouch was applied.

| Scene | Seed | Duration | SHA256 |
| --- | ---: | ---: | --- |
| BUS_06 | 748412438238146 | 58.295 s | `DAFEAD933A0411DD39EDAFE5918A987C0B76227BA1F7D4C29FE95AFBB43DC858` |
| BUS_09 | 748412438238147 | 58.312 s | `DDECAE6D5D1A2E511CC88B3C9003B1760F5695EDE29DF242569F84A6D153F173` |

BUS_06 was rendered once and its saved PNG was recovered after a local artifact-directory hand-off mismatch; the recovery submitted no second prompt. BUS_09 was submitted once. The run manifest, per-scene requests, ComfyUI histories, hashes and telemetry are retained beside the outputs. The official qualifier's manifest, validation, workflow and BUS_06/BUS_09 source PNG hashes were rechecked after the repair and remain unchanged.
