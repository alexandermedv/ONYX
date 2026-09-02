# Experiments

Эксперименты проверяют генераторы, identity-методы и способы orchestration, но
не становятся production-архитектурой автоматически.

## Активные и исторические направления

- [[ensemble_generator_0.2/README|Ensemble Runner 0.3]] — работающий
  экспериментальный orchestration runtime с собственными legacy job/manifest.
- Каталоги отдельных запусков и сравнений — воспроизводимые исследовательские
  материалы, а не канонические контракты ONYX.

Путь интеграции: experiment → benchmark → decision → runtime integration.

## Alexander LoRA Dataset Size v1

Phase 1 CPU/dry-run infrastructure находится в
`alexander_lora_dataset_size_v1`. Исторический `full_21` зафиксирован как
control; mini datasets предложены детерминированно и ожидают human approval.
Training и GPU benchmark ещё не запускались.
Канонические контракты Phase 1A описаны в [[JobSpec and Manifest v1]].
