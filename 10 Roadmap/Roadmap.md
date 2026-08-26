# Roadmap

## ✅ Phase 1A — Canonical contracts: COMPLETE

- [x] JobSpec v1 и Manifest v1 contract layer.
- [x] Stable logical IDs и deterministic `sha256-derived-v1` seeds.
- [x] Валидация quality → human review → selection → postprocessing → delivery.
- [x] Atomic Manifest persistence и read-only compatibility importers.

Phase 1A не включает runtime integration.

---

## ✅ Phase 1B.1 — Runtime Configuration and Materialization: COMPLETE

- [x] RuntimeConfig и ProviderRuntimeConfig.
- [x] Local/ignored runtime config и tracked sanitized example.
- [x] Безопасное resolution `client://`, `workspace://`, `repo://`, `model://`.
- [x] Immutable ExecutionPlan без execution state.
- [x] Canonical per-provider/per-candidate `sha256-derived-v1` seeds.
- [x] Side-effect-free JobSpec materialization и 50 passing tests.

Phase 1B.1 не выполняет providers и не создаёт Manifest lifecycle.

---

## ✅ Phase 1B.2 — Canonical Generation Execution Shell: COMPLETE

- [x] `SceneGenerator` boundary и CPU-only `FakeSceneGenerator`.
- [x] Orchestrator-owned incremental Manifest lifecycle и single writer.
- [x] Stable `GenerationResult` и distinct `AttemptRecord` per invocation.
- [x] Atomic persist-before-invoke, structured failures и artifact provenance.
- [x] Retry, resume, stale-attempt/crash recovery и missing-artifact rerun.
- [x] Independent sibling failure handling и 70 passing tests.

Phase 1B.2 не подключает real providers. Identity-aware generation ещё
не executable без native passthrough IdentityResult lifecycle.

---

## ⏸ Phase 1B.3 — Real generation adapter integration: PROPOSED / NOT STARTED

Точный implementation scope ещё не утверждён. Предполагаемое
направление — подключение первого real SceneGenerator adapter к
canonical execution shell без переноса ownership Manifest в provider.

Отдельные будущие шаги, не входящие в Phase 1B.2:

- Проверить восстановление личности через FaceFusion после FLUX.
- Проверить устранение растительности на лице через FaceFusion.
- Подключить существующие Job Engine и Ensemble runtime через compatibility
  adapters без переписывания исторических jobs.
- Подключить QualityEvaluator и human-review evidence к каноническому Manifest.
- Перевести postprocessing на selected-only execution.

---

## 💡 В будущем

- Автоматический Hand Repair.
- Автоматический отбор лучших изображений.
- Расширение библиотеки scene presets.
- Добавление новых коллекций сцен помимо Executive.
- Автоматическая генерация полного клиентского сета ONYX.

---

## ✅ Завершено

- [x] Client Profile v2.
- [x] ONYX Flux Scene Generator v1.0.0.
- [x] 12 Executive scene presets.
- [x] Управление параметрами `fixed/random`.
- [x] Diversity-контроль сцен без повторов.
- [x] Интеграция Flux Scene Generator с ComfyUI API.
Phase 1A–1B.2 не переводят существующие runner-ы, Quality Gate,
FaceFusion, postprocessor и ComfyUI workflows на canonical execution.
