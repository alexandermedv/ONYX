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

Phase 1B.2 завершена: canonical execution shell потребляет
ExecutionPlan и выполняет generation tasks через `SceneGenerator`.
Оркестратор единолично владеет canonical IDs, Manifest state,
revisions и atomic persistence. Текущая реализация CPU-only и имеет
только `FakeSceneGenerator`.

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
- [[ADR-0005 Orchestrator-Owned Manifest Lifecycle]]

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

После Phase 1B.1 canonical unittest discovery выполнял 50 passing tests.

## Реализация Phase 1B.2

- `engine/runtime/providers.py` — `SceneGenerator` boundary, immutable request,
  structured provider outcome и CPU-only `FakeSceneGenerator`.
- `engine/runtime/orchestrator.py` — Manifest initialization, single-writer
  revisions, generation lifecycle, retries, resume и artifact provenance.
- `tests/runtime/test_orchestrator.py` — CPU-only lifecycle, crash/recovery,
  retry, sibling-failure и artifact tests.

Manifest сохраняется до provider invocation. Logical `GenerationResult`
сохраняет ID между retries, а каждый фактический вызов
получает отдельный `AttemptRecord`. При resume успешный result с
существующим artifact не перезапускается; failed result, stale
running attempt или пропавший artifact приводят к новой
attempt без удаления истории. ArtifactRecord получает фактические
SHA-256 и size. По умолчанию failure одной task не блокирует
независимые sibling tasks.

Полный canonical unittest discovery выполняет 70 passing tests.

## Не реализовано

Не реализованы real provider adapters и перевод текущих pipeline
на v1: ComfyUI/FaceFusion/DreamO/LoRA execution, Job Engine и Ensemble
integration, identity lifecycle, QA/review/selection, postprocessing и delivery.
Identity-aware generators в Phase 1B.2 явно отклоняются, пока не
реализован native passthrough `IdentityResult` lifecycle.
Также пока отсутствуют historical Manifest importer, Quality Gate CSV importer,
JSON Schema, event journal и concurrent-writer protection.
