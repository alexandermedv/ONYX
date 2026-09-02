# ComfyUI FLUX Windows Runbook

## Canonical runtime

Для текущего ONYX FLUX runtime на Windows с RTX 3090 запускать ComfyUI_Flux
следующей командой:

```powershell
cd D:\AI\ComfyUI_Flux

.\python_embeded\python.exe -s ComfyUI\main.py `
  --windows-standalone-build `
  --disable-async-offload `
  --disable-pinned-memory
```

DynamicVRAM остаётся включённым. Не добавлять в canonical command
`--disable-dynamic-vram` или `--disable-mmap`.

## Known issue and classification

На Windows стандартный DynamicVRAM/comfy-aimdo host-buffer transfer path
периодически падал во время FLUX sampling с ошибками:

```text
RuntimeError: hostbuf_file_reader_read failed
HostBuffer.read_file_slice failed
```

Падение происходило в `comfy_aimdo.host_buffer.read_file_to_device` при
file-backed transfer весов в GPU. Это классифицировано как нестабильность
Windows DynamicVRAM/aimdo host-buffer path, а не как ошибка LoRA, ONYX workflow
или training artifacts.

Рабочий workaround: сохранить DynamicVRAM, но отключить async weight offload и
pinned memory через canonical flags выше. Для Windows + RTX 3090 + ComfyUI
`b1693ec` + comfy-aimdo `0.4.11` не убирать
`--disable-async-offload` и `--disable-pinned-memory` без нового controlled
smoke.

## Verification performed

- `flux1-dev.safetensors` расположен в
  `D:\AI\ComfyUI_Flux\ComfyUI\models\diffusion_models\flux1-dev.safetensors`.
- Его размер `23,802,932,552` bytes и SHA-256
  `4610115BB0C89560703C892C59AC2742FA821E60EF5871B33493BA544683ABD7`
  совпадают с authoritative metadata exact FLUX.1-dev artifact.
- Последовательное чтение, beginning/middle/end read probes и safetensors header
  parse прошли; storage corruption не подтверждена.
- Windows Event Log фиксировал virtual-memory/resource exhaustion и native
  `torch_cpu.dll` access violations. Это отдельный system-level risk, который
  следует проверять при повторении runtime failures.
- В новом canonical runtime `mini_3__1250` успешно сгенерирован. Старые и новые
  Alexander LoRA используют один и тот же рабочий ComfyUI runtime; LoRA не
  требует отдельного runtime profile.

## Explicit non-solutions

- Не восстанавливать diagnostic `pread` patch в `comfy/utils.py`: он был
  rollback-нут.
- Не использовать `--disable-mmap` как canonical workaround.
- Не обновлять ComfyUI, PyTorch, CUDA, safetensors или comfy-aimdo автоматически.
- Не менять models, LoRA или training artifacts для устранения этой ошибки.

## If the error returns

1. Сохранить server-side ComfyUI log, exact argv, RAM/VRAM и pagefile/commit
   snapshot.
2. Не повторять benchmark matrix автоматически.
3. Проверить, что canonical command содержит оба disable flags, а
   `comfy/utils.py` остаётся original file.
4. Классифицировать failure до изменения runtime packages или model files.
