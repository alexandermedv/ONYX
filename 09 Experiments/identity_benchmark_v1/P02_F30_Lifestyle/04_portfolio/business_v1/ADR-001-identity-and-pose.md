# ADR-001 — Separate identity from pose in the P02 prompt archive

Status: accepted for this experiment's archived prompts, not production integration.
Date: 2026-09-15.

## Context

The user reports excessive repetition in initial P02 business generations. A reference
image supplies both identity and a specific pose; copying both limits series diversity.

## Decision

Archive the supplied rule and all ten prompts verbatim: MASTER / REF01–REF05 govern
identity, while gaze, expression, head angle, hands, hairstyle arrangement, distance
and composition are explicitly allowed to vary. Do not infer that every saved image
perfectly follows its prompt. Store observed scene descriptions separately.

## Consequences

The prompt block is reusable for future experiments. No generation provider or global
prompt template has been changed. The current session is a qualitative example, not
a measured proof of improved identity or diversity. New use still needs benchmarking.
Immutable source copies, pending human review and traceable candidate derivatives keep
visual approval separate from technical file validation.
