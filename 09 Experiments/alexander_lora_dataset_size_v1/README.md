# Alexander LoRA Dataset Size v1

Статус: Phase 1 CPU/dry-run infrastructure implemented; dataset selection awaits human approval.

Исторически вручную отобранные 21 фотографии являются неизменяемым baseline
`full_21`. Начиная с Phase 1.5, детерминированные `mini_3`, `mini_5` и `mini_10`
выбираются из расширенного доступного client pool и образуют строгую вложенную
иерархию между собой. `full_21` остаётся отдельным frozen baseline и не обязан
содержать mini datasets. Анализ historical pool и новых candidates сохраняется
раздельно и не меняет source data.

Selector учитывает pose, framing, lighting, expression metadata, perceptual и
capture-group diversity. В `mini_3` допускается не более двух изображений из
одного явно заданного `capture_group`.

## Benchmark

- Stage 1: 4 datasets × 5 checkpoints × 4 diagnostic scenes × 1 seed × weight 0.9 = 80 images.
- Stage 2: best checkpoint каждого dataset × 12 scenes × 2 seeds × weight 0.9 = 96 images.
- Stage 3: optional weight sweep 0.7/0.9/1.0; автоматически не запускается.

`historical_control` регистрируется отдельно как внешний sanity check и не
участвует в выводах о dataset size.

CLI не materializes proposed dataset. Training configs являются dry-run
artifacts. До materialization требуется явное human approval, а до Phase 2
запрещены training и GPU benchmark.

Runtime artifacts исключены из Git, поскольку содержат абсолютные client paths.
