# Engineering

## Текущий статус

Phase 1A завершена: в `engine/contracts/` реализован канонический слой
контрактов ONYX — JobSpec v1, Manifest v1, нормализованные result entities,
валидация, стабильные IDs, детерминированные seeds, атомарное сохранение и
read-only compatibility adapters.

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

## Не реализовано

Phase 1A не включает новый orchestrator, runtime provider interfaces/adapters,
перевод текущих pipeline на v1, historical Manifest importer, Quality Gate CSV
importer, JSON Schema, event journal или concurrent-writer protection.
