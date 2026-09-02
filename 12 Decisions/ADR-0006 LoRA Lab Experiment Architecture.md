# ADR-0006 LoRA Lab Experiment Architecture

## Status

Accepted for Phase 1 CPU/dry-run infrastructure.

## Decision

LoRA experiments используют reusable `engine/lora_lab`, но не подключаются к
production orchestrator до прохождения experiment → benchmark → decision.
AI-Toolkit остаётся training backend и получает декларативно отрендеренные
конфигурации; новый training stack не создаётся.

Alexander dataset-size experiment фиксирует historical manual `full_21` как
отдельный baseline. С Phase 1.5 mini datasets выбираются из расширенного client
pool, поэтому обязаны быть вложены только друг в друга, но не в `full_21`.
Selection учитывает explicit capture groups и ограничивает mini_3 максимум двумя
фотографиями одной session. Все proposed memberships требуют human approval.

Benchmark задаётся произвольной matrix specification и выполняется staged.
Best checkpoint выбирается по yield, затем identity p10 и mean; вместе с ним
сохраняется `time_to_best_checkpoint`. `historical_control` является внешним
sanity check и исключён из dataset-size comparison.

Phase 1 использует существующие InsightFace/OpenCV/Pillow assets и CPU provider.
Новые ML weights или тяжёлые dependencies не добавляются.

## Consequences

Production runtime и legacy Quality Gate CLI остаются неизменными. Generated
artifacts с client paths не коммитятся.
