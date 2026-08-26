# Pipeline Architecture

## Статус архитектуры

ONYX разделяет текущий runtime и каноническую целевую архитектуру.

**Текущий runtime:** Job Engine, Ensemble Runner, Quality Gate, FaceFusion,
postprocessing и экспериментальные ComfyUI workflows продолжают работать в
своих существующих форматах.

**Canonical target architecture:** Phase 1A реализует contract layer, а Phase
1B.1 — machine-local configuration и чистую materialization в ExecutionPlan.
Новый orchestrator, Manifest lifecycle и provider execution ещё не реализованы.

Подробный формат данных: [[JobSpec and Manifest v1]].

## Runtime materialization

```text
Machine-independent JobSpec v1
              +
Machine-local RuntimeConfig
              ↓
     immutable ExecutionPlan
```

RuntimeConfig не является вторым JobSpec: он содержит только roots, endpoints,
executables, provider locations, workflow/model mappings и machine metadata.
`config/runtime.local.json` локален и игнорируется Git;
`config/runtime.example.json` — sanitized tracked example. Альтернативный файл
выбирается через `ONYX_RUNTIME_CONFIG`.

Materialization разрешает `client://`, `workspace://`, `repo://` и `model://`,
отклоняя traversal, encoded separators, absolute-path и Windows-drive
injection. `model://` требует явного provider-local сопоставления model ID с
root alias и не угадывает filename.

ExecutionPlan содержит resolved execution description, identity references,
provider bindings, output locations и generation tasks. Он не является
Manifest и не содержит results, attempts или lifecycle state. JobSpec при
materialization не мутируется; providers и внешние runtimes не запускаются.

## Канонический поток

```text
Scene
  ↓
GenerationResult
  ↓
IdentityResult
  ├── Automatic Evaluation
  └── Human Review
          ↓
SelectionDecision
  ↓
PostProcessResult
  ↓
DeliveryResult
```

### Scene generation

Одна сцена может обрабатываться несколькими SceneGenerator providers, каждый
из которых может создать несколько GenerationResult candidates. Stable seed
выводится отдельно для job, scene, provider, candidate index и stage.

DreamO T2I и personal LoRA являются identity-aware SceneGenerators: identity
conditioning участвует непосредственно в генерации.

### Identity

FaceFusion и DreamO img2img являются IdentityProviders и создают производные
IdentityResult из GenerationResult. Один GenerationResult может иметь
несколько независимых IdentityResult.

Identity-aware generators создают zero-copy `native_passthrough`
IdentityResult, ссылающийся на тот же artifact. Поэтому дальнейшие стадии
всегда работают с IdentityResult независимо от способа получения личности.

Personal LoRA разрешена только для `vip` в каноническом v1.

### Quality and selection

IdentityResult — каноническая единица автоматической оценки, human review и
selection. Automatic Evaluation и HumanReview являются отдельными evidence
records.

Для `SelectionDecision(status="selected")` обязательны:

- все enabled required evaluators из materialized quality plan;
- успешный статус этих EvaluationResult;
- отсутствие `hard_fail=true` и `verdict="fail"`;
- успешный HumanReview того же IdentityResult;
- `ratings.client_ready=true` хотя бы в одном таком review.

### Postprocessing and delivery

Postprocessing разрешён только для selected IdentityResult. DeliveryResult
может ссылаться только на успешный PostProcessResult. `client_ready` является
решением quality/selection, а не свойством DeliveryResult.

Наличие файла в legacy `final_results/` само по себе не является каноническим
доказательством client readiness.

## Provider boundaries

Канонические роли:

- SceneGenerator;
- IdentityProvider;
- QualityEvaluator;
- Human reviewer;
- Candidate selector;
- PostProcessor;
- DeliveryProvider.

Phase 1A определяет provider references/configuration, а Phase 1B.1 разрешает
только machine bindings используемых providers. Runtime interfaces,
registries, execution adapters и orchestrator пока не реализованы.

## Совместимость

Read-only adapters преобразуют существующие Job Engine и Ensemble job JSON в
JobSpec v1. Они не изменяют исторические файлы и не переносят machine-specific
пути в основные canonical fields.

## Связанные решения

- [[ADR-0002 Canonical Job and Manifest Contracts]]
- [[ADR-0003 Identity-Aware Generators and Identity Results]]
- [[ADR-0004 Quality Selection Postprocessing and Delivery]]
