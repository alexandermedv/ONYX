# JobSpec and Manifest v1

## Implementation status

Статус: **Phase 1A contracts, Phase 1B.1 materialization и Phase 1B.2
canonical generation shell implemented**.

Контракты находятся в `engine/contracts/`, materialization — в
`engine/runtime/`. Canonical discovery выполняет 70 contract, compatibility и
runtime tests. Phase 1B.2 выполняет generation tasks только через
CPU-only fake provider; текущие ONYX runtime pipelines не подключены.

## JobSpec v1

JobSpec описывает намерение задания:

- job/client identity и service tier;
- base seed;
- несколько SceneSpec;
- несколько SceneGenerator configurations;
- identity profiles и logical references;
- IdentityProvider configurations;
- QualityPlan и SelectionPolicy;
- postprocessing и delivery intent;
- compatibility metadata.

JobSpec использует schema `onyx.job_spec`, version `1.0`. После начала
исполнения JobSpec должен рассматриваться как immutable input. Технической
защиты файла от изменения Phase 1A не реализует.

JobSpec является machine-independent. Canonical references используют stable
provider IDs и logical URIs. Resolved endpoints, executable paths и локальные
runtime paths не записываются обратно в JobSpec. Phase 1B.1 подтверждает
тестами, что JobSpec остаётся равным исходному после materialization.

## RuntimeConfig и ExecutionPlan

RuntimeConfig — отдельная machine-local модель, содержащая только:

- `machine_id`, repository/workspace/client roots;
- provider endpoints и installation/executable/input/output roots;
- workflow roots;
- provider-local model roots и explicit model mappings;
- runtime capabilities/location metadata.

Он не содержит scenes, prompts, service tier, seeds, candidate counts или
quality/review/selection/delivery policy. `config/runtime.example.json`
является sanitized tracked example, а `config/runtime.local.json` игнорируется.
Другой файл выбирается одной переменной `ONYX_RUNTIME_CONFIG`.

`materialize_job(JobSpec, RuntimeConfig)` возвращает immutable ExecutionPlan:

- resolved workspace и intended output locations;
- resolved client profiles и identity references;
- только используемые provider runtime bindings;
- materialized generation tasks и canonical scene/provider inputs;
- отдельный deterministic seed для каждого scene/provider/candidate;
- JSON-serializable `resolved_runtime_snapshot()` для будущего Manifest.

ExecutionPlan является описанием будущего исполнения, не runtime state. В нём
нет Manifest, results, attempts или retries. Materialization не создаёт
каталоги, не проверяет существование runtime assets и не выполняет subprocess,
network, ComfyUI, FaceFusion или GPU operations.

### Logical URI resolution

- `client://` разрешается относительно `RuntimeConfig.client_root`;
- `workspace://` — относительно `workspace_root`;
- `repo://` — относительно `repo_root`;
- `model://<root-alias>/<path>` — через model roots конкретного provider.

Для `ProviderRef.model_id` runtime configuration должна явно задать
`models[model_id] → model://...`. Filename guessing отсутствует. URI без
authority, traversal (`..`), percent-encoded traversal/separators, absolute
path и Windows drive injection отклоняются.

## Manifest v1

Manifest использует schema `onyx.manifest`, version `1.0` и представляет
materialized execution state. Он содержит integer `revision`, JobSpec
reference/hash, resolved runtime snapshot и отдельные collections:

- GenerationResult;
- IdentityResult;
- EvaluationResult;
- HumanReview;
- SelectionDecision;
- PostProcessResult;
- DeliveryResult;
- ArtifactRecord;
- AttemptRecord.

`quality_plan` materialized в Manifest, чтобы selection validation могла
детерминированно проверить required evaluators без обращения к изменяемому
внешнему состоянию.

## Result and provenance model

```text
Scene 1 ── N GenerationResult
GenerationResult 1 ── N IdentityResult
IdentityResult 1 ── N EvaluationResult
IdentityResult 1 ── N HumanReview
IdentityResult 1 ── N SelectionDecision
SelectionDecision 1 ── N PostProcessResult
PostProcessResult 1 ── N DeliveryResult
```

Parent references валидируются. Один generation candidate может иметь
несколько независимых identity variants без полей вроде
`facefusion_output` или `dreamo_img2img_output`.

Каждый runtime result содержит provider snapshot, inputs, outputs, status,
attempt IDs, timestamps/runtime fields и optional ErrorRecord. Часть
provider-specific inputs/outputs пока остаётся loosely typed dictionaries.

## Status and error model

Runtime statuses v1:

- `planned`;
- `running`;
- `succeeded`;
- `failed`;
- `skipped`;
- `cancelled`.

Selection statuses:

- `pending`;
- `selected`;
- `rejected`.

Минимальная consistency validation:

- `failed` runtime result требует ErrorRecord;
- `succeeded` runtime result не может содержать error.

Полная state machine и обязательность timestamps пока не реализованы.

## Stable logical IDs and attempts

`stable_id()` использует фиксированный ONYX UUID namespace, canonical sorted
JSON стабильных dimensions и UUIDv5. Entity-specific helpers фиксируют
нормативные dimensions для GenerationResult, IdentityResult,
EvaluationResult, PostProcessResult и DeliveryResult.

Logical result ID остаётся стабильным при retry. Retry хранится отдельным
AttemptRecord с собственным attempt ID.

## Deterministic seed contract

Алгоритм `sha256-derived-v1`:

1. canonical UTF-8 JSON;
2. dimensions: algorithm, base seed, job, scene, provider, candidate index, stage;
3. SHA-256;
4. первые 8 bytes;
5. big-endian integer;
6. очистка high bit для signed-64-bit-safe неотрицательного значения.

Golden vector закреплён automated test.

Phase 1B.1 использует этот же `derive_seed()` при materialization с dimensions
job, scene, provider, candidate index и stage=`generation`. Legacy shared-branch
seed behavior не переносится в canonical ExecutionPlan.

## Identity model

- DreamO T2I и personal LoRA — identity-aware SceneGenerators.
- FaceFusion и DreamO img2img — IdentityProviders.
- Identity-aware generator получает `native_passthrough` IdentityResult без
  повторной обработки изображения.
- IdentityResult является downstream unit для QA, review и selection.
- Personal LoRA в canonical v1 разрешена только для `vip`.

## Quality, human review, and selection

Automatic Evaluation и HumanReview сохраняются раздельно.

Selected decision требует:

- всех enabled required evaluator provider IDs из Manifest quality plan;
- succeeded EvaluationResult для того же IdentityResult;
- отсутствие technical `hard_fail` и `verdict="fail"`;
- succeeded HumanReview того же IdentityResult;
- минимум один review с `ratings.client_ready=true`.

Optional evaluator может отсутствовать.

## Artifacts

ArtifactRecord хранит logical URI, provenance creator, optional SHA-256,
размер, MIME type и image dimensions. Поддерживаемые URI schemes:

- `client://`;
- `workspace://`;
- `repo://`;
- `model://`.

Artifact IDs, указанные в result outputs через `artifact_id` или
`artifact_ids`, должны существовать в `Manifest.artifacts`.

## Postprocessing and delivery

PostProcessResult допускается только для `SelectionDecision(status="selected")`.
DeliveryResult требует succeeded PostProcessResult. Unprocessed fallback не
является частью canonical v1. `client_ready` не хранится в DeliveryResult.

## Atomic persistence

`save_manifest_atomic()` выполняет:

1. contract validation;
2. запись в `<manifest>.writing` рядом с целевым файлом;
3. flush;
4. `os.fsync`;
5. `os.replace`;
6. cleanup оставшегося temporary file.

Event journal, locking и concurrent-writer protection не реализованы.
Persistence primitive сам по себе не владеет revision lifecycle;
Phase 1B.2 `ManifestWriter` единолично управляет monotonic revisions
внутри одного orchestrator process и отклоняет неожиданное внешнее
изменение revision.

## Phase 1B.2 generation lifecycle

`run_generation_plan()` инициализирует Manifest до provider execution.
Оркестратор назначает stable `GenerationResult` ID и `AttemptRecord`
для каждого фактического invocation. Running result и attempt атомарно
сохраняются до вызова provider. Provider не получает Manifest,
не меняет canonical state и не выбирает canonical IDs.

Resume основан на сохранённом Manifest:

- succeeded result с доступным artifact не вызывает provider;
- failed result повторяется с тем же logical result ID и новым
  attempt ID;
- stale running attempt остаётся в истории, помечается failed
  с `INTERRUPTED_ATTEMPT`, затем создаётся новая attempt;
- succeeded result с пропавшим artifact перезапускается;
- предыдущие attempts и ArtifactRecord не удаляются.

Каждый успешный returned artifact проверяется и получает
ArtifactRecord с фактическими SHA-256 и byte size. Failure одной
независимой task по умолчанию не останавливает siblings.

## Compatibility imports

Read-only importers поддерживают representative:

- Job Engine v1 job JSON;
- Ensemble v0.2/v0.3 job JSON.

Они создают JobSpec v1, не изменяют source files и исключают machine-specific
runtime paths из canonical fields. Job Engine scenes восстанавливаются как
placeholder scenes из `minimum_output_images`, поскольку legacy job не хранит
явную scene specification.

Historical Manifest importer и Quality Gate CSV importer пока отсутствуют.

## Known limitations after Phase 1B.2

- есть только CPU-only `FakeSceneGenerator`; нет real provider adapters или
  registry;
- legacy Job Engine и Ensemble runtimes не читают JobSpec/Manifest v1;
- нет ComfyUI, FaceFusion, QA/review/selection, postprocessing или delivery execution;
- identity-aware SceneGenerators отклоняются до native passthrough
  IdentityResult lifecycle;
- нет historical Manifest и Quality Gate CSV importers;
- нет JSON Schema files;
- нет event journal и concurrent-writer protection;
- revision monotonicity не проверяется persistence layer;
- workflow/model hashes не materialized автоматически, существование resolved paths не проверяется;
- provider-specific inputs/outputs частично loosely typed;
- Manifest quality plan пока не сверяется с JobSpec hash;
- timestamps и полный lifecycle не обязательны валидатором.

## Related documents

- [[Pipeline Architecture]]
- [[ADR-0002 Canonical Job and Manifest Contracts]]
- [[ADR-0003 Identity-Aware Generators and Identity Results]]
- [[ADR-0004 Quality Selection Postprocessing and Delivery]]
- [[ADR-0005 Orchestrator-Owned Manifest Lifecycle]]
