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

## Consequences

- Новый runtime сможет работать с единым contract независимо от provider.
- Исторические runtimes остаются operational compatibility runtimes до
  последующей интеграции.
- Caller отвечает за monotonic revision и concurrent writers.
- Runtime materialization и automatic workflow/model hashing ещё необходимы.

## Implementation

Phase 1A реализована в `engine/contracts/`. Подробнее: [[JobSpec and Manifest v1]].
