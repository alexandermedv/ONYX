# AI Pipeline

## Каноническое направление

Phase 1A определяет общий контракт данных, но пока не заменяет существующие
runtime-пайплайны Job Engine и Ensemble Runner.

```text
JobSpec v1
  -> generation candidates
  -> identity results
  -> automatic evaluation + human review
  -> explicit selection
  -> postprocessing of selected results only
  -> delivery
```

Материализованное состояние, ошибки, provenance и результаты каждого этапа
хранятся в Manifest v1. Единицей оценки, ручной проверки и отбора является
`IdentityResult`, включая native passthrough для генераторов, уже сохраняющих
личность.

Подробности: [[JobSpec and Manifest v1]] и [[Pipeline Architecture]].

## Функциональные области

- [[Scene Generator]]

- [[Client Profiler]]

- [[Face Preservation]]

- [[Hand Repair]]

- [[Face Detailer]]

- [[QA]]

- [[Export]]

Текущие страницы модулей могут описывать работающие или экспериментальные
реализации. Они не являются отдельным источником истины для контрактов v1.
