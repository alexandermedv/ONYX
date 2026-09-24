# ADR-0005 Orchestrator-Owned Manifest Lifecycle

## Status

Accepted

## Context

Provider invocation может завершиться failure или process crash. Resume
должен сохранять provenance, не дублировать уже завершённую работу и
не передавать provider-ам ownership канонического state.

## Decision

- Canonical orchestrator — единственный writer и владелец Manifest,
  revisions и canonical result/attempt IDs.
- Providers получают immutable execution request и возвращают outcome.
  Они не получают Manifest и не могут назначать canonical IDs.
- Logical `GenerationResult` ID стабилен между retries. Каждый
  фактический provider invocation имеет отдельный `AttemptRecord`.
- Running result и attempt атомарно сохраняются до provider
  invocation (`persist-before-invoke`).
- Resume пропускает succeeded result только если его artifact
  существует. Failed result повторяется с тем же logical ID.
  Stale running attempt сохраняется и помечается interrupted.
  Отсутствующий artifact форсирует новую attempt.
- Recovery не удаляет исторические attempts и ArtifactRecord.

## Consequences

- Manifest содержит наблюдаемый durable lifecycle даже при crash.
- Provider adapters остаются заменяемыми и не зависят от persistence.
- Retry не ломает внешние ссылки на logical result, а attempt history
  сохраняет provenance.
- Single-writer — ограничение Phase 1B.2. Multi-process locking и event
  journal не входят в это решение.

## Implementation

Phase 1B.2 реализует решение в `engine/runtime/orchestrator.py` и
проверяет CPU-only tests в `tests/runtime/test_orchestrator.py`.
Текущий executable provider — только `FakeSceneGenerator`; real ONYX
provider integration не является частью этого ADR.
