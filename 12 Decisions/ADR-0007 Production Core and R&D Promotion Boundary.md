# ADR-0007 Production Core and R&D Promotion Boundary

## Status

Accepted — 2026-09-16

## Decision

`13 Production` is the production control plane for ONYX Brand, Product, Portfolio and Marketing standards. `09 Experiments` remains the immutable R&D evidence base for experiments, candidates, canonical sources and review history.

Production promotion uses a manifest that records canonical source paths, status and QA evidence. It may later reference approved copies or exports, but it must not silently alter the experimental evidence from which they derive.

## Consequences

- A production package can be created without reorganizing R&D history.
- An experimental asset is not production-approved merely because it exists.
- Missing QA, upscale or export work is recorded as `PENDING` or `MISSING`.
- Product-facing standards remain separate from internal implementation terms.
