# Pipeline Architecture

## Статус архитектуры

ONYX разделяет текущий runtime и каноническую целевую архитектуру.

**Текущий runtime:** Job Engine, Ensemble Runner, Quality Gate, FaceFusion,
postprocessing и экспериментальные ComfyUI workflows продолжают работать в
своих существующих форматах.

**Canonical architecture:** Phase 1A реализует contract layer, Phase
1B.1 — machine-local configuration и чистую materialization в ExecutionPlan,
а Phase 1B.2 — CPU-only generation shell с fake provider и incremental
Manifest lifecycle. Real ONYX providers и legacy runtimes ещё не подключены.

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

## Canonical generation execution shell

```text
ExecutionPlan generation task
          ↓
orchestrator assigns stable GenerationResult ID
          ↓  persist running result + AttemptRecord
SceneGenerator invocation
          ↓
result/error + ArtifactRecord (SHA-256, size)
          ↓  atomic incremental persist
resumable Manifest
```

Оркестратор — единственный владелец Manifest, revisions, canonical
IDs и persistence. `SceneGenerator` получает immutable request с уже
назначенным result ID и детерминированным seed. Provider выполняет
работу и возвращает outcome, но не получает Manifest, не мутирует
canonical state и не назначает IDs.

Каждый provider invocation имеет отдельный `AttemptRecord`, но
`GenerationResult` ID остаётся стабильным при retry. Running state
атомарно сохраняется **до** provider invocation, чтобы crash не
оставался невидимым.

При resume:

- succeeded result с существующим artifact пропускается;
- failed result получает новую attempt при том же logical ID;
- stale running attempt сохраняется и помечается
  `INTERRUPTED_ATTEMPT`, после чего создаётся новая attempt;
- succeeded result с отсутствующим artifact перезапускается;
- исторические attempts и artifacts не удаляются.

Независимые sibling tasks продолжаются после failure по
умолчанию. Успешные artifacts регистрируются с фактическими
SHA-256 и byte size.

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

Phase 1A определяет provider references/configuration, Phase 1B.1
разрешает machine bindings, а Phase 1B.2 реализует `SceneGenerator`
boundary и canonical orchestrator. Выполняется только CPU-only
`FakeSceneGenerator`; real ComfyUI, FaceFusion, DreamO, LoRA, Ensemble Runner
и Job Engine adapters/registries не подключены. Identity-aware generators
отклоняются до реализации native passthrough `IdentityResult` lifecycle.

## Совместимость

Read-only adapters преобразуют существующие Job Engine и Ensemble job JSON в
JobSpec v1. Они не изменяют исторические файлы и не переносят machine-specific
пути в основные canonical fields.

## Связанные решения

- [[ADR-0002 Canonical Job and Manifest Contracts]]
- [[ADR-0003 Identity-Aware Generators and Identity Results]]
- [[ADR-0004 Quality Selection Postprocessing and Delivery]]
- [[ADR-0005 Orchestrator-Owned Manifest Lifecycle]]
