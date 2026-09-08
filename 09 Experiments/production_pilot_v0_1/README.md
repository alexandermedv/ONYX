# ONYX Production Pilot v0.1

Этот pilot — узкий последовательный запуск утверждённого `mini_5__1250` для
12 коммерческих business scenes. Он не является расширением LoRA Lab и не
изменяет training artifacts.

Runtime запускается только по canonical [[ComfyUI FLUX Windows Runbook]]:
DynamicVRAM включён; async offload и pinned memory выключены. Конфигурация
runtime намеренно не дублируется в коде.

`engine.production_pilot.runner` использует существующий API template
`comfyui-workflows/ONYX_Flux_Scene_Generator_0.3_fixed_lora_api.json` только в
памяти: подменяет native LoRA name, prompt, seed, fixed sampler parameters и
output prefix. Template на диске не изменяется. Raw stage не использует
FaceFusion, FaceDetailer, upscale или любую identity correction.

Перед каждым scene runner фиксирует RAM, Windows commit headroom и VRAM. При
critical RAM/commit threshold он останавливается. VRAM не является stop rule:
после успешного FLUX sample model-resident ~22 GiB — ожидаемое состояние.
CUDA/ComfyUI allocation failure будет записан как execution error без retry.
`/free` доступен только при soft system-memory pressure и только при явном
`--allow-free-on-pressure`, поэтому не вызывается после каждого image.

Raw outputs, immutable scene provenance и run manifest будут находиться в
`09 Experiments/production_pilot_v0_1/runs/<run_id>/raw` и
`runs/<run_id>/manifests`. Структура также резервирует
`qa`, `selected`, `repaired`, `upscaled` и `delivery`.

После raw stage команда `qa` запускает существующий Quality Gate v0.2 через
compatibility manifest; он измеряет identity, face detection/count/ratio.
Pilot дописывает blur/exposure/technical flags в его report как non-decisive
evidence. Автоматический rank — лишь recommendation: canonical
selection, postprocess и delivery требуют human review с `client_ready=true`.
После этого допускается selected-only `ONYX_Postprocessor v0.1` с approved
`4x_NMKD-Siax_200k.pth`; final delivery не создаётся автоматически.

Dry-run (без обращения к ComfyUI):

```powershell
python -m engine.production_pilot.runner --run-id production_pilot_v0_1 dry-run
```

For a bounded selected-scene matrix, each base seed is followed by consecutive
integer variants; this changes only seed, never inference settings:

```powershell
python -m engine.production_pilot.runner --run-id production_pilot_v0_1 dry-run --scenes 1,4,7 --seeds-per-scene 2
```

Canonical smoke payload (без обращения к ComfyUI) сохраняет текущие prompt и
seed workflow, меняя только LoRA и output prefix:

```powershell
python -m engine.production_pilot.runner --run-id production_pilot_v0_1 smoke
```

The only command that may submit this one canonical smoke is explicit; do not
use it without a separate GPU approval:

```powershell
python -m engine.production_pilot.runner --run-id production_pilot_v0_1_smoke smoke --execute
```

Raw generation требует отдельного preflight/human go-ahead:

```powershell
python -m engine.production_pilot.runner --run-id production_pilot_v0_1 raw --allow-free-on-pressure
```

После raw и без повторной генерации:

```powershell
python -m engine.production_pilot.runner --run-id production_pilot_v0_1 qa --reference-folder "D:\\AI\\Clients\\Alexander\\source"
```
