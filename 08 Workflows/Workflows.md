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
Контракты Phase 1A не запускают ComfyUI и пока не подключены к существующим
runner-ам. Физические пути остаются деталями compatibility runtime/provider;
канонический provenance использует логические artifact URI.

См. [[Pipeline Architecture]] и [[JobSpec and Manifest v1]].
