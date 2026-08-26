# ADR-0002 Canonical Job and Manifest Contracts

## Status

Accepted

## Context

Job Engine и Ensemble Runner используют разные job/manifest formats. Их
runtime configuration, result provenance и lifecycle представлены
несовместимо, а исторические jobs должны оставаться воспроизводимыми и
неизменными.

## Decision

ONYX использует два отдельных canonical contracts:

- JobSpec v1 описывает declarative execution intent и рассматривается как
  immutable после начала исполнения;
- Manifest v1 хранит materialized execution state, resolved provider/model/
  workflow/runtime information, results, attempts и artifacts.

Logical results получают стабильные UUIDv5 IDs из canonical dimensions.
Retry не меняет logical result ID и хранится отдельным AttemptRecord.

Artifacts используют logical `client://`, `workspace://`, `repo://` и
`model://` URIs с provenance. Absolute runtime paths допустимы только в
resolved Manifest information.

Manifest сохраняется атомарно через temporary file, flush, `fsync` и
`os.replace`, с integer revision. Event journal и writer locking не входят в
v1.

Legacy Job Engine и Ensemble jobs читаются compatibility adapters. Source
files не переписываются.

Machine bindings отделены от JobSpec в RuntimeConfig. Materialization разрешает
logical URI через local roots/provider mappings и создаёт immutable
ExecutionPlan, не изменяя JobSpec. ExecutionPlan описывает будущее исполнение,
но не содержит Manifest lifecycle state.

`model://` разрешается только через explicit provider-local model ID/root
mapping. Runtime не угадывает model filenames. В Manifest в дальнейшем должен
копироваться JSON-serializable resolved runtime snapshot только для providers,
фактически используемых job.

## Consequences

- Новый runtime сможет работать с единым contract независимо от provider.
- Исторические runtimes остаются operational compatibility runtimes до
  последующей интеграции.
- Caller отвечает за monotonic revision и concurrent writers.
- Provider execution, Manifest runtime lifecycle и automatic workflow/model
  hashing ещё необходимы.

## Implementation

Phase 1A реализована в `engine/contracts/`; Phase 1B.1 RuntimeConfig и
materialization — в `engine/runtime/`. Подробнее: [[JobSpec and Manifest v1]].
