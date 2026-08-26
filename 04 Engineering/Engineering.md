# Engineering

## Текущий статус

Phase 1A завершена: в `engine/contracts/` реализован канонический слой
контрактов ONYX — JobSpec v1, Manifest v1, нормализованные result entities,
валидация, стабильные IDs, детерминированные seeds, атомарное сохранение и
read-only compatibility adapters.

Phase 1B.1 также завершена: `engine/runtime/` загружает machine-local
RuntimeConfig, безопасно разрешает logical URI и materializes неизменяемый
ExecutionPlan с canonical per-provider/per-candidate seeds. Materialization не
изменяет JobSpec и не запускает providers.

Текущие Job Engine, Ensemble Runner, Quality Gate, FaceFusion и postprocessing
остаются рабочими runtime-контурами совместимости. Они пока не переведены на
JobSpec/Manifest v1 и не заменены новым orchestrator.

## Основные документы

- [[Pipeline Architecture]] — концептуальная архитектура и границы стадий.
- [[JobSpec and Manifest v1]] — техническая спецификация реализованных контрактов.
- [[AI Pipeline]] — обзор стадий обработки изображений.
- [[Workflows]] — роль ComfyUI workflows.
- [[Roadmap]] — состояние и следующие архитектурные шаги.

## Архитектурные решения

- [[ADR-0001 Repository Structure]]
- [[ADR-0002 Canonical Job and Manifest Contracts]]
- [[ADR-0003 Identity-Aware Generators and Identity Results]]
- [[ADR-0004 Quality Selection Postprocessing and Delivery]]

## Реализация Phase 1A

- `engine/contracts/models.py` — dataclass-модели.
- `engine/contracts/ids.py` — stable IDs и `sha256-derived-v1`.
- `engine/contracts/validation.py` — инварианты JobSpec и Manifest.
- `engine/contracts/persistence.py` — атомарное сохранение Manifest.
- `engine/contracts/compatibility/` — импорт Job Engine и Ensemble jobs.
- `tests/contracts/`, `tests/compatibility/` — 28 passing tests.

## Реализация Phase 1B.1

- `engine/runtime/config.py` — RuntimeConfig, ProviderRuntimeConfig и выбор
  файла через `ONYX_RUNTIME_CONFIG`.
- `engine/runtime/materialize.py` — безопасное URI resolution и
  JobSpec → ExecutionPlan.
- `engine/runtime/execution_plan.py` — immutable execution description и
  `resolved_runtime_snapshot()`.
- `config/runtime.example.json` — tracked sanitized example.
- `config/runtime.local.json` — ignored machine-local configuration.
- `tests/runtime/` — CPU-only runtime/materialization tests.

Полный canonical unittest discovery выполняет 50 passing tests.

## Не реализовано

Phase 1B.1 не включает orchestrator, provider execution/interfaces/adapters,
Manifest runtime lifecycle, retries, перевод текущих pipeline на v1,
ComfyUI/FaceFusion execution, QA/review/selection, postprocessing или delivery.
Также пока отсутствуют historical Manifest importer, Quality Gate CSV importer,
JSON Schema, event journal и concurrent-writer protection.
