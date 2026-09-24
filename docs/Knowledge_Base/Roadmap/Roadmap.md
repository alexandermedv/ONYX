# Roadmap

## CURRENT commercial priority — 2026-09-20

[ONYX Commercial Product System v1](../13%20Production/Product_Standards/ONYX_PRODUCT_SYSTEM.md) is FROZEN_FOR_SOFT_LAUNCH. Until 10 unique paid orders: **80% SALES / CLIENT PRODUCTION / DELIVERY**, **20% R&D / AUTOMATION**. Existing technical milestones below remain historical/technical facts, not blockers or permission to change the frozen product. Model arenas, new LoRA, PuLID/FLUX tuning, complex automation and website infrastructure must not delay sales. Review prices/scope at **ONYX Product & Pricing Review v1.1** after 10 paid orders.

Next commercial step: prepare ONYX Avito Launch Pack v1 using the approved asset/consent gates and client payment/retention wording. Use the operational payment/refund process and the [manual 30-day data deletion policy](../13%20Production/Client_Experience/Intake/ONYX_DATA_RETENTION_AND_DELETION_v1.md). Public cancellation Terms can receive separate legal review before publication.


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

## ✅ Phase 1B.3 — Real FLUX SceneGenerator integration: COMPLETE

- [x] Минимальный ComfyUI HTTP client для `/prompt`, `/history`, `/view`.
- [x] Non-identity `FluxSceneGenerator` с workflow-hash и model checks.
- [x] LoRA Lab Phase 1: CPU/dry-run analysis, selection, planners, AI-Toolkit renderer, metrics and serialization.
- [ ] Alexander LoRA dataset-size Phase 2: approved materialization and controlled training.
- [x] Deterministic workflow patching и unchanged canonical seed.
- [x] Structured failures и untrusted output-descriptor validation.
- [x] Windows relative subfolder normalization без ослабления traversal checks.
- [x] Один successful real smoke и same-manifest resume без нового POST.
- [x] 93 passing canonical CPU tests.

Phase 1B.3 не подключает identity-aware generators, FaceFusion, legacy runners,
Quality Gate, review/selection, postprocessing или delivery.

Следующие отдельные шаги:

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
Phase 1A–1B.3 не переводят существующие runner-ы, Quality Gate, FaceFusion,
postprocessor и legacy ComfyUI workflows на canonical execution; подключён
только новый canonical FLUX API workflow Phase 1B.3.
