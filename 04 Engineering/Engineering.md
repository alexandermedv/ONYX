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
revisions и atomic persistence.

Phase 1B.3 завершена: добавлен первый real non-identity-aware provider —
`FluxSceneGenerator`, который выполняет API-format FLUX workflow через
ComfyUI HTTP API. Контролируемый Windows smoke создал canonical artifact,
а повторная передача того же job/Manifest подтвердила resume без нового POST.

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

## Реализация Phase 1B.3

- `engine/runtime/comfyui_client.py` — минимальный `/prompt`, `/history` и
  `/view` HTTP client без владения canonical state.
- `engine/runtime/flux_scene_generator.py` — загрузка и проверка workflow,
  deterministic patching prompt/seed/parameters/output prefix, polling и
  structured provider outcome.
- `engine/flux_scene_generator/ONYX_Flux_Scene_Generator_0.3_API.json` —
  canonical API workflow, адресуемый через `repo://`.
- `tests/runtime/test_flux_scene_generator.py` — CPU-only transport,
  workflow, provenance, failure и output-safety tests.

ComfyUI может вернуть Windows-style relative `subfolder`. Adapter нормализует
separator `\\` в `/` до строгой проверки, но продолжает отклонять traversal,
absolute/rooted/drive/UNC paths и percent-encoded separators. Provider
возвращает bytes и provenance оркестратору; canonical ID, Manifest и
ArtifactRecord остаются собственностью orchestrator.

Контролируемый smoke на clean external ComfyUI revision `b1693ecb`, endpoint
`127.0.0.1:8190`, FLUX `flux1-dev` и workflow hash
`bdd790a35b5f6e360273d50a91710559411e52a7c60bcf001345bf4bc583df18`
успешно создал один PNG 896×1152. Cold run занял 421.6 секунды, включая
333.9 секунды model initialization; resume занял 0.004 секунды и не создал
новый POST или AttemptRecord. Последующий Windows runtime investigation показал
нестабильность DynamicVRAM/comfy-aimdo host-buffer transfers при включённых async
weight offloading и pinned memory. Canonical запуск сохраняет DynamicVRAM, но
использует `--disable-async-offload --disable-pinned-memory`; подробности и
exact command — в [[ComfyUI FLUX Windows Runbook]]. ComfyUI и модели остаются
внешними и не модифицируются ONYX. Исследовательские pread/custom-loader
прототипы rollback-нуты и не входят в runtime architecture.

Полный canonical unittest discovery выполняет 93 passing tests.

## Не реализовано

Кроме non-identity FLUX adapter, не реализованы другие real providers и перевод
текущих pipeline на v1: FaceFusion/DreamO/LoRA execution, Job Engine и Ensemble
integration, identity lifecycle, QA/review/selection, postprocessing и delivery.
Identity-aware generators явно отклоняются, пока не
реализован native passthrough `IdentityResult` lifecycle.
Также пока отсутствуют historical Manifest importer, Quality Gate CSV importer,
JSON Schema, event journal и concurrent-writer protection.
