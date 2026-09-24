# ADR-0004 Quality Selection Postprocessing and Delivery

## Status

Accepted

## Context

Identity fidelity должна измеряться автоматически, но commercial readiness
не может определяться только одной метрикой. Expensive postprocessing должен
применяться после отбора, а delivery не должен молча использовать
unprocessed fallback.

## Decision

Automatic Evaluation и HumanReview являются отдельными evidence records для
одного IdentityResult.

В ONYX v1 `SelectionDecision(status="selected")` требует:

- всех enabled required evaluators из materialized Manifest quality plan;
- succeeded EvaluationResult для того же IdentityResult;
- отсутствия `hard_fail=true` и `verdict="fail"`;
- succeeded HumanReview того же IdentityResult;
- минимум одного HumanReview с `ratings.client_ready=true`.

Только selected IdentityResult может поступить в postprocessing. DeliveryResult
может быть создан только после succeeded PostProcessResult. `client_ready`
принадлежит quality/selection evidence и не записывается в DeliveryResult.

Supervisor override не входит в v1.

## Consequences

- Automatic metrics и human judgment сохраняются независимо и проверяемо.
- Дорогая обработка не является prerequisite для canonical QA.
- Ошибка обязательного postprocessing блокирует delivery.
- Текущий Quality Gate CSV workflow и Ensemble final collector остаются
  operational runtime behavior до интеграции с contracts v1.

## Implementation

Инварианты реализованы в `engine/contracts/validation.py` и покрыты Phase 1A
tests. Runtime Quality Gate и postprocessing не изменялись.
