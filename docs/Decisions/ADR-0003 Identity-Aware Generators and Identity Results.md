# ADR-0003 Identity-Aware Generators and Identity Results

## Status

Accepted

## Context

Identity может применяться как преобразование готовой сцены либо участвовать
непосредственно в sampling. Model-specific manifest fields не позволяют
масштабировать providers и усложняют единый QA pipeline.

## Decision

- DreamO text-to-image и personal LoRA являются identity-aware
  SceneGenerators.
- FaceFusion и DreamO img2img являются IdentityProviders, принимающими
  GenerationResult.
- Один GenerationResult может иметь несколько независимых IdentityResult.
- Identity-aware SceneGenerator создаёт zero-copy `native_passthrough`
  IdentityResult, ссылающийся на generation artifact.
- IdentityResult является единой downstream unit для automatic evaluation,
  HumanReview и SelectionDecision.
- Personal LoRA разрешена только для service tier `vip` в canonical v1.

## Rationale

DreamO T2I и LoRA меняют сам процесс генерации и не могут корректно
представляться как post-generation identity transform. Native passthrough
сохраняет эту семантику и одновременно даёт downstream стадиям единый parent
type.

## Consequences

- Canonical Manifest не нуждается в `facefusion_output`,
  `dreamo_img2img_output` и аналогичных provider-specific top-level fields.
- Новый provider добавляется отдельным result record, а не новым полем run.
- Текущие Ensemble fields остаются частью его operational legacy format до
  runtime migration.

## Implementation

Решение реализовано contract models, compatibility importer и validation в
Phase 1A. Runtime providers пока не переведены на эти contracts.
