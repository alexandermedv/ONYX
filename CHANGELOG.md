## Unreleased

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
