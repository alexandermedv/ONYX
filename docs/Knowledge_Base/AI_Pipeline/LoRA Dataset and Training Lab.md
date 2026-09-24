# LoRA Dataset and Training Lab

`engine/lora_lab` реализует CPU/dry-run слой для personal-LoRA экспериментов:
source analysis, nested selection, caption validation, training planning,
AI-Toolkit config rendering, staged benchmark planning, telemetry, aggregation и
result serialization.

Phase 1 не обучает модели и не интегрирует LoRA в production runtime. Для
Alexander baseline dataset — исторический `full_21`; analyzer не меняет его
состав. Mini datasets могут использовать новые read-only candidates из
расширенного pool, имеют session-aware diversity constraints и требуют human
approval.

## ComfyUI benchmark runtime

LoRA benchmark generation использует тот же canonical Windows FLUX runtime,
что и existing Alexander LoRA, а не отдельный profile для новых checkpoints.
На Windows + RTX 3090 + ComfyUI `b1693ec` + comfy-aimdo `0.4.11` запускать
ComfyUI с `--disable-async-offload --disable-pinned-memory`, оставляя
DynamicVRAM включённым. `mini_3__1250` успешно прошёл generation в этом
runtime. Не восстанавливать diagnostic pread patch и не включать async offload
или pinned memory без нового controlled smoke. См. [[ComfyUI FLUX Windows
Runbook]].

Selection report сохраняет source hash, лицо, pragmatic pose, sharpness,
exposure, identity similarity, diversity contribution, причины выбора и contact
sheet. Best checkpoint включает optimizer step, effective epochs, elapsed time,
identity/quality/yield metrics и `time_to_best_checkpoint`.
