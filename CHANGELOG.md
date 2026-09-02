## Unreleased

### Phase 1B.3 — real non-identity FLUX adapter

- Добавлены минимальный ComfyUI HTTP client и `FluxSceneGenerator` для
  canonical `/prompt` → `/history` → `/view` execution.
- Adapter проверяет workflow SHA-256, детерминированно патчит API graph и
  передаёт canonical seed без изменения.
- Добавлены structured provider failures, output descriptor validation и
  provenance для endpoint, prompt ID, workflow hash, submitted seed и ComfyUI
  output metadata.
- Windows-style relative output subfolder нормализуется в POSIX form перед
  строгой проверкой; traversal, absolute/rooted/drive/UNC paths и encoded
  separators остаются запрещены.
- Controlled real smoke на clean external ComfyUI `b1693ecb` выполнил ровно
  один POST и создал canonical PNG 896×1152 с совпадающими size/SHA-256.
- Same-manifest resume не создал нового POST или AttemptRecord и сохранил все
  canonical IDs и artifact hash.
- Canonical unittest discovery выполняет 93 passing tests.

Phase 1B.3 не реализует identity-aware generation, FaceFusion,
QA/review/selection, postprocessing, delivery или legacy runner integration.

### Phase 1B.2 — canonical generation execution shell

- Добавлен `SceneGenerator` provider boundary и CPU-only
  `FakeSceneGenerator`.
- Добавлен canonical orchestrator, который единолично владеет
  Manifest state, revisions, canonical IDs и atomic incremental persistence.
- Running `GenerationResult` и `AttemptRecord` сохраняются до
  provider invocation; каждый retry сохраняет logical result ID и
  создаёт новую attempt.
- Добавлены resume, stale running/crash recovery, missing-artifact rerun
  и сохранение полной attempt/artifact истории.
- ArtifactRecord записывает фактические SHA-256 и byte size;
  independent sibling tasks по умолчанию продолжаются после failure.
- Canonical unittest discovery выполняет 70 passing tests.

Phase 1B.2 не подключает ComfyUI, FaceFusion, DreamO, LoRA,
Ensemble Runner или Job Engine. Identity-aware generators отклоняются
до реализации native passthrough IdentityResult lifecycle.

### Phase 1B.1 — runtime configuration and materialization

- Добавлены RuntimeConfig и ProviderRuntimeConfig для machine-only bindings.
- Добавлены tracked sanitized `config/runtime.example.json`, ignored
  `config/runtime.local.json` и выбор через `ONYX_RUNTIME_CONFIG`.
- Добавлено безопасное resolution `client://`, `workspace://`, `repo://` и
  provider-local `model://` без filename guessing.
- Добавлен immutable ExecutionPlan и side-effect-free JobSpec materialization.
- Generation tasks используют canonical `sha256-derived-v1` seeds отдельно для
  provider и candidate; VIP-only LoRA повторно проверяется.
- `resolved_runtime_snapshot()` включает только используемые providers и
  является JSON-serializable.
- Canonical unittest discovery выполняет 50 passing tests.

Phase 1B.1 не выполняет providers и не реализует orchestrator, Manifest
lifecycle, retries, ComfyUI/FaceFusion, QA/review/selection, postprocessing или
delivery execution.

### Phase 1A — canonical contracts

- Добавлены JobSpec v1 и Manifest v1 как независимые канонические модели.
- Добавлены нормализованные generation, identity, evaluation, human review,
  selection, postprocessing и delivery results с provenance и ошибками.
- Добавлены stable logical ID helpers и детерминированный seed algorithm
  `sha256-derived-v1`.
- Добавлены правила обязательной automatic QA, human review с
  `client_ready=true`, selected-only postprocessing и delivery после успешного
  postprocessing.
- Добавлено атомарное incremental сохранение Manifest и read-only importers для
  Job Engine и Ensemble legacy formats.
- Phase 1A покрыта 28 автоматическими тестами.

Phase 1A не изменяет и не подключает существующие runtime-пайплайны.

## v1.0.0 — 2026-08-05

### Добавлено

- ONYX Flux Scene Generator v1.0.0.
- Генерация сцен на базе FLUX через ComfyUI API.
- Поддержка Client Profile v2.
- Режимы `client` и `portfolio`.
- Управление параметрами `fixed/random`.
- Библиотека из 12 Executive-пресетов.
- Diversity-контроль без повторов сцен.
- Рандомизация одежды и выражения лица.
- Уникальный `seed` для каждого изображения.
- Сохранение metadata для сгенерированных сцен.
- Контроль возраста клиента через prompt.
- Валидация Client Profile и Session Spec.

### Улучшено

- Соблюдение возраста клиента при генерации.
- Разнообразие сцен в рамках одной серии.
- Размещение персонажа относительно стола в `conference_table`.

### Известные ограничения

- FLUX может генерировать растительность на лице для мужского профиля даже при `clean-shaven`.
- Точное положение рук может отличаться от заданного в scene preset.
- Геометрия взаимодействия человека с мебелью в отдельных случаях может содержать артефакты.
# Unreleased

### LoRA Lab Phase 1 — CPU/dry-run infrastructure

- Добавлены versioned specs и deterministic planners для Alexander dataset-size experiment.
- Historical `full_21` зафиксирован как control; mini datasets требуют human approval.
- Добавлены staged benchmark plans, AI-Toolkit dry-run renderer, telemetry,
  `time_to_best_checkpoint`, metrics aggregation и machine-readable reports.
- Training, GPU benchmark и production integration не выполнялись.

### LoRA Lab Phase 1.5 — candidate-pool proposal

- Protocol расширен: frozen `full_21` остаётся baseline, а nested mini datasets
  выбираются из полного доступного client pool.
- Добавлены explicit capture groups, session-aware selection и derived caption
  overrides без изменения historical captions.
