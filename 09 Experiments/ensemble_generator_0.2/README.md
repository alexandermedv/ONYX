# ONYX Ensemble Runner 0.3

ONYX Ensemble Runner — экспериментальный orchestration layer для генерации коммерческих AI-портретов через несколько независимых генераторов, способов переноса личности и единый postprocessing pipeline.

Основная задача Ensemble Runner — получить несколько вариантов одной сцены разными методами, сохранить техническое происхождение каждого результата и собрать готовые изображения в единую клиентскую папку.

## Архитектура

```text
Scene specification
        │
        ├── FLUX ─────────────┐
        │                     ├── FaceFusion ───────┐
        ├── JuggernautXL ─────┤                     │
        │                     └── DreamO img2img ───┤
        │                                           │
        ├── DreamO ─────────────────────────────────┤
        │                                           │
        └── FLUX + LoRA [VIP only] ─────────────────┤
                                                    │
                                                    ▼
                                           ONYX Postprocessor
                                           Siax 4× upscale
                                                    │
                                                    ▼
                                               final_results/
                                                    │
                                                    ▼
                                              Client delivery
```

Runner последовательно запускает четыре основные генеративные ветки:

1. FLUX
2. FLUX + LoRA
3. JuggernautXL
4. DreamO

Для FLUX и JuggernautXL дополнительно могут создаваться identity-варианты через FaceFusion и DreamO img2img.

После identity stage результаты могут автоматически передаваться в ONYX Postprocessor.

---

## Service tiers и LoRA

LoRA предназначена только для VIP-заказов и не является основой массового production pipeline.

Она запускается только при одновременном выполнении двух условий:

```json
{
  "service_tier": "vip",
  "identity": {
    "lora": {
      "enabled": true
    }
  }
}
```

Для `mass`, `signature`, `premium` или при `enabled: false` runner автоматически пропускает LoRA, даже если она случайно указана в `generators`.

---

## Управление памятью

Внутри одной генеративной ветки модель остаётся загруженной, а prompt и seed меняются для каждой сцены.

Между тяжёлыми этапами runner вызывает ComfyUI `/free`, чтобы освобождать модели и снижать риск переполнения RAM/VRAM.

Отказ одной ветки не должен останавливать весь ensemble job: runner сохраняет ошибку в manifest и продолжает обработку остальных доступных веток.

---

## Workflows

API workflows хранятся в:

```text
workflows/
```

Основные файлы:

```text
flux_api.json
lora_api.json
dreamo_api.json
dreamo_img2img_api.json
ONYX_JuggernautXL_Generator_v0.3_weighted.json
ONYX_Postprocessor v0.1.json
```

`juggernautxl_api.json` сохранён как предыдущий workflow JuggernautXL.

Все workflows, используемые runner, должны быть экспортированы из ComfyUI в API format.

UI workflow вида:

```json
{
  "nodes": [...]
}
```

не подходит для отправки через ComfyUI `/prompt`.

API workflow содержит узлы вида:

```json
{
  "67": {
    "inputs": {},
    "class_type": "LoadImage"
  }
}
```

---

## JuggernautXL production preset

JuggernautXL использует отдельные native SDXL settings и не должен наследовать разрешение FLUX.

Текущий preset:

```text
Resolution: 832 × 1216
Steps:      35
CFG:        5.0
Sampler:    DPM++ 2M SDE
Scheduler:  Karras
Denoise:    1.0
```

Runner принудительно задаёт эти параметры при запуске JuggernautXL.

Это защищает production pipeline от случайного изменения параметров при сохранении workflow в ComfyUI.

---

## Матрица переноса личности

Текущая схема:

| Источник | Варианты |
|---|---|
| FLUX | original, FaceFusion, DreamO img2img |
| JuggernautXL | original, FaceFusion, DreamO img2img |
| DreamO text-to-image | original |
| FLUX + LoRA | original |

FaceFusion подключён через:

```text
D:\AI\ONYX\engine\facefusion\runner.py
```

После генерации ветки FLUX или JuggernautXL ComfyUI освобождает память, после чего FaceFusion обрабатывает подготовленную папку изображений.

DreamO img2img работает через отдельный API workflow.

Runner копирует исходную сцену в `ComfyUI/input`, подставляет исходное изображение и reference identity, меняет prompt, seed и output prefix.

---

# ONYX Postprocessor

После генерации и переноса личности изображения могут автоматически передаваться в:

```text
ONYX_Postprocessor v0.1
```

Текущий production upscaler:

```text
4x_NMKD-Siax_200k.pth
```

Pipeline:

```text
LoadImage
    ↓
UpscaleModelLoader
    ↓
ImageUpscaleWithModel
    ↓
SaveImageAdvanced
```

Runner определяет необходимые узлы postprocessor по `class_type`, а не по конкретным ComfyUI node IDs.

Это позволяет повторно сохранять workflow без необходимости изменять ID узлов в Python-коде.

Пример конфигурации:

```json
{
  "postprocess": {
    "enabled": true,
    "workflow": "ONYX_Postprocessor v0.1.json",
    "comfy_input_root": "D:\\AI\\ComfyUI_Flux\\ComfyUI\\input",
    "model": "4x_NMKD-Siax_200k.pth",
    "methods": [],
    "scene_ids": []
  }
}
```

Пустые:

```json
"methods": [],
"scene_ids": []
```

означают обработку всех доступных подходящих результатов.

Позже эти параметры могут использоваться для upscale только вручную или автоматически отобранных финалистов.

---

## Postprocess-only

Postprocessor можно запускать отдельно, не выполняя повторную генерацию FLUX, JuggernautXL, DreamO и LoRA.

Runner использует существующий job manifest и уже созданные identity results.

Пример:

```powershell
python .\ensemble_runner.py `
  .\job_postprocess_test.json `
  --workflows .\workflows `
  --output-root "D:\AI\ComfyUI_Flux\ComfyUI\output" `
  --postprocess-only
```

Pipeline в этом режиме:

```text
Existing identity results
        ↓
ONYX Postprocessor
        ↓
Siax 4×
        ↓
final_results
```

Это позволяет отделить дорогой upscale от генерации и в дальнейшем применять postprocessing только к отобранным изображениям.

---

# Final results

Технические результаты генераторов продолжают храниться раздельно, чтобы можно было анализировать происхождение изображения и качество отдельных методов.

Клиентский output при этом собирается в одну плоскую папку:

```text
final_results/
└── <job_id>/
    ├── scene_01.png
    ├── scene_01_02.png
    ├── scene_02.png
    ├── scene_03.png
    └── final_results_manifest.json
```

В клиентской структуре отсутствуют каталоги:

```text
flux/
juggernautxl/
dreamo/
lora/
facefusion/
```

Клиент получает единый фотосет независимо от того, какой метод создал конкретное изображение.

При наличии нескольких финальных вариантов одной сцены runner автоматически добавляет числовой suffix:

```text
executive_desk_01.png
executive_desk_01_02.png
executive_desk_01_03.png
```

---

## Provenance

Скрытие модели от клиентской структуры не означает потерю технической информации.

`final_results_manifest.json` сохраняет:

- `scene_id`;
- исходную branch;
- identity method;
- original source;
- postprocessed source;
- customer filename;
- final output path.

Таким образом ONYX может в дальнейшем анализировать:

- долю коммерчески пригодных кадров каждого генератора;
- эффективность FaceFusion и DreamO;
- влияние postprocessing;
- причины брака;
- оптимальную маршрутизацию сцен между моделями.

---

## Dry run

Проверка job без генерации:

```powershell
python .\ensemble_runner.py .\job.example.json --dry-run
```

---

## Обычный запуск

```powershell
python .\ensemble_runner.py `
  .\job.example.json `
  --workflows .\workflows `
  --output-root "D:\AI\ComfyUI_Flux\ComfyUI\output"
```

ComfyUI должен быть доступен по умолчанию на:

```text
http://127.0.0.1:8188
```

---

## Runtime artifacts

Следующие данные являются runtime artifacts и не должны попадать в Git:

```text
runs/
final_results/
*.manifest.json
*.zip
Архив/
```

Они исключены через `.gitignore`.

---

## Текущие ограничения

### FLUX stability

На текущей конфигурации периодически наблюдается ошибка ComfyUI:

```text
RuntimeError: hostbuf_file_reader_read failed
```

Ошибка возникает при загрузке/offload весов FLUX и относится к runtime/memory/storage layer ComfyUI.

Runner должен изолировать такой сбой и продолжить остальные доступные ветки.

### Автоматический Quality Control

Автоматическая оценка качества изображения, likeness, рук, глаз и других дефектов пока не входит в Ensemble Runner.

На текущем этапе финальный отбор выполняется вручную.

Следующий архитектурный этап — ONYX Quality Gate между identity stage и дорогим postprocessing.

---

## Целевая production architecture

```text
Scene Generator
      ↓
Generator Ensemble
      ↓
Identity Transfer
      ↓
ONYX Quality Gate
      ↓
Candidate Selection
      ↓
ONYX Postprocessor
      ↓
Final Results
      ↓
Client Delivery / Nextcloud
```

Основной принцип: генерировать достаточно кандидатов, автоматически или вручную отбирать коммерчески пригодные изображения и применять дорогую финальную обработку только к выбранным результатам.