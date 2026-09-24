# Workflows

ComfyUI workflows — версионируемые определения внешнего runtime. ComfyUI,
модели и их installations находятся вне репозитория ONYX; в репозитории
хранятся JSON workflow, конфигурация и код вызова.

## Текущее использование

- Ensemble Runner использует API workflows из
  `09 Experiments/ensemble_generator_0.2/workflows/`.
- Другие workflow и их версии могут относиться к отдельным экспериментам или
  существующим runtime-пайплайнам.
- UI-format ComfyUI не равен API-format, принимаемому endpoint `/prompt`.

## Связь с контрактами v1

JobSpec v1 задаёт provider/model/workflow версии и логические входы. Manifest v1
записывает фактически использованные версии, параметры, runtime и артефакты.
Phase 1B.1 разрешает canonical `repo://` workflow references и provider-local
`model://` mappings через RuntimeConfig. Machine paths остаются вне JobSpec:
tracked `runtime.example.json` содержит только sanitized example, а локальный
`runtime.local.json` игнорируется.

Materialization создаёт только immutable ExecutionPlan. Она не читает и не
изменяет workflow JSON, не проверяет наличие моделей, не обращается к ComfyUI и
не подключена к существующим runner-ам.

Phase 1B.3 добавляет отдельную execution boundary после materialization.
`FluxSceneGenerator` использует canonical API workflow
`engine/flux_scene_generator/ONYX_Flux_Scene_Generator_0.3_API.json`, проверяет
его declared SHA-256 и детерминированно подставляет prompt, seed, dimensions,
sampler settings и output prefix. Затем adapter вызывает ComfyUI `/prompt`,
`/history` и `/view`. Workflow не мутируется на диске.

External ComfyUI installation и model files остаются вне ONYX. RuntimeConfig
задаёт endpoint и explicit provider-local model mapping. Для Windows FLUX
runtime canonical command сохраняет DynamicVRAM, но отключает async weight
offloading и pinned memory: `--disable-async-offload --disable-pinned-memory`.
Это workaround для нестабильного DynamicVRAM/comfy-aimdo host-buffer transfer
path; exact command, validation модели и troubleshooting находятся в
[[ComfyUI FLUX Windows Runbook]]. Cold model initialization может занимать
несколько минут.
Windows-style relative output subfolder
нормализуется, а traversal, absolute/rooted/drive/UNC и encoded separators
отклоняются. Канонический provenance продолжает использовать logical artifact
URI; Manifest и ArtifactRecord создаёт orchestrator, не ComfyUI provider.
Экспериментальные pread/custom-loader исследования rollback-нуты и не входят в
canonical runtime.

См. [[Pipeline Architecture]] и [[JobSpec and Manifest v1]].
