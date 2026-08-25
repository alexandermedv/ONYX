# Roadmap

## ✅ Phase 1A — Canonical contracts: COMPLETE

- [x] JobSpec v1 и Manifest v1 contract layer.
- [x] Stable logical IDs и deterministic `sha256-derived-v1` seeds.
- [x] Валидация quality → human review → selection → postprocessing → delivery.
- [x] Atomic Manifest persistence и read-only compatibility importers.

Phase 1A не включает runtime integration.

---

## ⏸ Next architectural phase — runtime/orchestrator integration: NOT STARTED

Следующие задачи являются **proposed**, а не утверждённым implementation scope:

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
Phase 1A является только contract layer: существующие runner-ы, Quality Gate,
FaceFusion, postprocessor и ComfyUI workflows ещё не переведены на эти контракты.
