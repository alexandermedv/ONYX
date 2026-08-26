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
не подключена к существующим runner-ам. Канонический provenance продолжает
использовать logical artifact URI.

См. [[Pipeline Architecture]] и [[JobSpec and Manifest v1]].
