# ONYX — Codex Instructions

## Content layout rules

- Production assets for a synthetic character belong under `01_Characters/<ID>`.
- Shared ONYX advertising deliverables belong under `02_Marketing`; canonical character photographs remain in the character package.
- Stable rules belong under `03_Standards`; reusable templates belong under `04_Templates`.
- `09 Experiments` remains R&D history and keeps its existing name.
- Real client data belongs physically outside the repository under `D:\AI\ONYX_Clients`. Never stage client files. The in-repository `/_Clients/`, `/Clients/` and `/clients/` paths are defensive-only ignore locations.
- During incremental migration, preserve user WIP. If a modified or untracked file is encountered, mark it `DEFERRED_WIP` and leave it in place.

## Project

ONYX is an AI portrait generation and image-production pipeline.

The goal is to build a scalable, highly automated system that generates commercially usable AI photographs while preserving client identity and photorealism.

The system is experimental and under active development. Do not assume that every experiment is part of the production architecture.

## Core priorities

In descending order:

1. Identity fidelity to the client.
2. Photorealism and natural human appearance.
3. Absence of visible AI artifacts.
4. Correct anatomy, especially face, hands, eyes, teeth, and hair.
5. Prompt and scene adherence.
6. Automation and reproducibility.
7. Generation speed and compute efficiency.

Do not sacrifice identity fidelity merely to improve aesthetics.

## Architecture principles

ONYX should evolve toward modular providers rather than hard-coded model-specific pipelines.

Prefer interfaces such as:

- SceneGenerator
- IdentityProvider
- QualityEvaluator
- PostProcessor
- Upscaler
- DeliveryProvider

New models should be replaceable without rewriting the entire pipeline.

Prefer configuration-driven behavior over hard-coded paths or parameters.

Experiments should be reproducible using:
- fixed seeds;
- explicit model/config versions;
- manifests;
- saved parameters;
- machine-readable evaluation results.

## Identity strategy

Mass-market client processing should preferably work without per-client training.

Personal LoRA is allowed but is primarily intended for VIP/premium workflows unless explicitly requested otherwise.

Existing or previously investigated identity technologies include:

- FaceFusion
- InstantID
- PuLID / PuLID-FLUX
- DreamO
- InfiniteYou
- IP-Adapter / FaceID
- personal LoRA

Do not present these as unexplored technologies.

New identity methods should be benchmarked against the strongest existing baseline rather than evaluated in isolation.

## Quality evaluation

Identity similarity should be measurable where possible.

ONYX has an automatic quality-control direction using InsightFace embeddings.

Do not rely only on subjective visual judgment.

A future benchmark system should support comparison across:

- identity provider;
- generator;
- seed;
- scene;
- reference image;
- identity score;
- quality score;
- artifact score;
- generation time;
- VRAM usage.

## Existing implementation

Before modifying anything, inspect the repository and determine the current structure.

Important known areas include:

- ensemble generator / runner
- engine/quality_gate
- ComfyUI workflows
- postprocessing
- experiment runs
- job manifests

Do not assume these paths or implementations are still current. Inspect them first.

## ComfyUI

ComfyUI installations and model repositories exist outside the ONYX repository.

Treat them as external runtime dependencies.

Do NOT:

- upgrade ComfyUI automatically;
- upgrade PyTorch automatically;
- change CUDA automatically;
- install or upgrade global dependencies automatically;
- modify external ComfyUI installations without explicit approval.

When a ComfyUI workflow must be changed, prefer creating a new version rather than destroying a known-working workflow.

## Models

Model weights are large external assets.

Never:

- commit model weights to Git;
- duplicate large models unnecessarily;
- delete models;
- move models;
- automatically download multi-GB models.

Before downloading a model larger than 1 GB, report:

- exact model;
- source;
- expected size;
- destination;
- why it is needed;

and wait for explicit approval.

Prefer reusing models already present on disk.

## Client data

Client photographs and datasets are sensitive production assets.

Never:

- delete client photographs;
- overwrite source datasets;
- rename or reorganize client folders without approval;
- commit client photographs to Git;
- upload client photographs anywhere unless explicitly requested.

Generated synthetic images must remain distinguishable from original client photographs.

## Experiments

Experiments should not silently change production behavior.

Prefer:

experiment -> benchmark -> decision -> integration

rather than directly integrating an untested model.

When testing a new identity technology, start with the smallest useful benchmark before performing large GPU runs.

Prefer:
1. one subject;
2. one reference;
3. simple portrait;
4. fixed seed;
5. compare against baseline.

Only expand the experiment if the method passes the initial test.

## GPU jobs

Long GPU generations are expensive.

Do not automatically start long-running generation jobs.

Before a substantial GPU run, state:

- number of images;
- resolution;
- model;
- approximate workload;
- expected output directory.

Wait for approval unless the user explicitly requested the run.

Dry-run functionality should be preferred when available.

## Git

Keep commits focused and reversible.

Do not commit:

- model weights;
- generated runs;
- client data;
- caches;
- temporary files;
- secrets.

Before large refactors, inspect Git status.

Do not discard uncommitted user changes.

Do not force push.

Do not rewrite Git history unless explicitly requested.

## Documentation

Documentation is part of the implementation.

When architecture or behavior changes materially, identify which documentation should also change.

Prefer Markdown documentation suitable for Obsidian and Git.

Do not update documentation merely to make it look complete. It must describe the actual implementation.

## Coding behavior

Before implementing a task:

1. Inspect relevant code and documentation.
2. Check Git status.
3. Explain the proposed change briefly.
4. Prefer the smallest safe change.
5. Preserve existing behavior unless change is required.
6. Add or update tests when practical.
7. Run relevant tests or dry-runs.
8. Review the diff.
9. Report exactly what changed.

Do not perform unrelated refactoring while solving a focused task.

## When uncertain

Do not guess about:

- model compatibility;
- paths;
- workflow node IDs;
- model filenames;
- client dataset structure;
- production configuration.

Inspect the repository or ask.

If an operation could destroy data, break a working environment, trigger a large download, or consume significant GPU time, stop and request approval.

## Working style

Act as an engineering collaborator, not an autonomous product owner.

You may proactively identify:

- bugs;
- technical debt;
- architectural problems;
- missing tests;
- opportunities for automation.

But separate observations from requested changes.

Do not implement unrelated suggestions without approval.

## Documentation synchronization

The Obsidian vault at `D:\AI\ONYX` is part of the ONYX repository and is
the authoritative human-readable project documentation.

For every completed implementation phase:

1. Implement the requested change.
2. Run and verify relevant tests.
3. Update affected Obsidian documentation to match the actual implementation.
4. Update or create ADRs for architectural decisions.
5. Update project/status documentation when capabilities or pipeline state changed.
6. Verify that documentation describes implemented behavior, not planned behavior.
7. Only then propose the final commit.

Do not update documentation after every intermediate edit.
Update it once the implementation phase is stable and tests pass.

Documentation and code should normally be committed together when they
describe the same completed change.

## Remote and unattended execution

ONYX may be operated remotely and may run long-lived jobs while the user is away from the computer.

Remote operation does not imply unrestricted autonomy.

For unattended or remote jobs:

- prefer deterministic scripts and existing pipeline commands over repeated agent reasoning;
- prefer API/CLI execution over GUI automation when both are available;
- do not rely on an unlocked interactive Windows desktop unless the task explicitly requires GUI automation;
- do not modify Windows security, networking, firewall, user accounts, power settings, VPN, SSH, RDP, startup configuration, or scheduled tasks unless explicitly requested;
- do not expose new network ports or services to the public Internet;
- do not install remote-access software unless explicitly requested;
- do not disable security controls merely to make automation easier;
- if a task cannot continue safely without elevated permissions or interactive access, stop and report the blocker.

For a long-running job, write enough state to disk that the run can be inspected after completion or failure.

Prefer resumable/idempotent execution where practical.

## Cost and usage control

Treat external AI generation, cloud APIs, Codex reasoning, and repeated retries as metered resources.

Prefer, in order where technically appropriate:

1. deterministic local Python/code;
2. existing local ONYX tools;
3. local GPU processing / ComfyUI;
4. inexpensive external/model calls;
5. expensive model reasoning or generation only when necessary.

Do not use a more expensive Codex model or higher reasoning effort merely because an image generation failed.

Image-generation retry policy must be defined by the job/session configuration where possible.

Never create an unbounded retry loop.

When retry limits are exhausted:
- preserve the failed result and diagnostics;
- mark the scene/job appropriately;
- continue with independent work when safe;
- report the failure rather than repeatedly consuming quota.

Batch routine filesystem, manifest, QA, metadata, and upload operations in deterministic scripts rather than performing them through repeated conversational reasoning.

## Image production workflow

For automated ONYX photo sessions, prefer a configuration-driven pipeline such as:

session specification
-> generation
-> source preservation
-> automatic QA
-> PASS / REPAIR / REGENERATE decision
-> post-processing
-> upscale
-> final QA
-> manifest/report update
-> delivery

Never overwrite the original generated image during repair or post-processing.

Keep source, intermediate, rejected, repaired, and final assets distinguishable.

A final delivery set should contain only explicitly accepted images.

Where practical, record for every generated asset:

- session/job ID;
- scene ID;
- provider/model;
- model/config version;
- prompt or prompt reference;
- reference-image identifiers;
- seed when applicable;
- generation timestamp;
- generation duration;
- resolution;
- QA results;
- identity score when available;
- retry/repair history;
- final disposition.

Prefer structured machine-readable manifests over information stored only in chat text.

## Quality gates

Automated QA should use deterministic/local checks whenever practical.

Examples include:

- file readability;
- expected resolution and aspect ratio;
- face count;
- identity similarity;
- blur/sharpness;
- duplicate or near-duplicate detection;
- missing outputs.

Visual-model evaluation should complement deterministic QA rather than replace it.

Do not automatically PASS an image solely because generation completed successfully.

Session-level QA should also consider collection diversity, including scene, framing, pose, expression, clothing, and background diversity when relevant.

## Storage and delivery

ONYX project assets and personal user assets must remain separated.

Known storage distinction:

- `onyx` is the ONYX project/work bucket;
- `alexander` is personal storage.

Never upload ONYX project assets to `alexander`.

Before adding a new storage destination, inspect the existing project configuration rather than hard-coding credentials or endpoints.

Never write secrets, access keys, passwords, tokens, or private URLs into:

- AGENTS.md;
- source code;
- committed configuration;
- manifests;
- Markdown documentation.

Prefer environment variables or existing secret/config mechanisms.

For production delivery, upload only the assets intended by the session/job configuration.

Source client photograph uploads remain subject to the Client data rules and require explicit approval.

## Git safety for automated work

Because remote and unattended tasks may run while the repository contains unrelated work:

Before modifying tracked project files:
1. run `git status --short`;
2. identify pre-existing changes;
3. treat all pre-existing changes as user-owned unless clearly produced by the current task.

Never:
- stage unrelated files;
- include unrelated changes in a commit;
- use `git add .` or `git add -A` when unrelated changes exist;
- run destructive cleanup commands to obtain a clean tree.

Prefer explicitly staging only the files produced by the current task.

Do not push unless the user explicitly requests push.

A request to commit does not imply permission to push.

A request to push does not imply permission to force-push.

## Escalation and approvals

Stop and request explicit approval before:

- destructive filesystem operations;
- overwriting canonical references;
- changing production credentials;
- changing system configuration;
- exposing network services;
- rewriting Git history (the existing prohibition on force-push still applies).

The existing Models, GPU jobs, and Client data sections govern approvals for large model downloads, substantial GPU runs, and source/client uploads. Other large external downloads and sensitive source-data uploads also require explicit approval.

Routine execution already explicitly requested by the user does not require asking for approval again at every individual scene or file.
