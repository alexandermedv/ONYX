# Legacy Production semantic classification

Date: 2026-09-24
HEAD: `1e57d649877a8698a950b2eab6317a8847b61a16`
Mode: read-only analysis; no files in `13 Production` were moved, edited or deleted.

## Pre-flight

The working tree contains only the previously observed user WIP: modified P01/P02/P03 previews, modified intake and Product Standards files, modified delivery code, untracked Carousel V3, Brandbook, session, Collection Book, order and engine WIP. The index was empty before and after analysis. No stash, reset, restore, checkout, clean, staging, commit or push was performed.

## Complete inventory

The inventory covered every file recursively and calculated SHA256, byte size, tracked/untracked state, modification state, mtime, extension and top-level area. Aggregate result: **701 files / 5,544,166,067 bytes (5,287.33 MiB)**.

| Top-level area | Files | Tracked | Untracked | Bytes | Semantic result | Candidate canonical destination |
|---|---:|---:|---:|---:|---|---|
| Brand | 33 | 16 | 17 | 43,493,799 | BRAND_STANDARD + BRAND_WIP | `03_Standards/Brand` or `03_Standards/Brand/WIP`; generated examples need separate decision |
| Client_Delivery | 6 | 6 | 0 | 687,838 | TEMPLATE / ACTIVE_WIP | `03_Standards`, `04_Templates`, or protected session WIP |
| Client_Experience | 4 | 2 | 2 | 11,561 | CLIENT_EXPERIENCE_STANDARD / ACTIVE_WIP | `03_Standards/Client_Experience` and `04_Templates/Client_Intake` |
| Orders | 1 | 0 | 1 | 2,989 | NEEDS_OWNER_DECISION | No approved in-repo canonical order root |
| Portfolio | 442 | 106 | 336 | 5,351,482,294 | CHARACTER_SESSION_WIP + MARKETING_ASSET + EXACT_DUPLICATE | `01_Characters/<ID>/02_Sessions/<Session>/WIP` and `02_Marketing` |
| Product_Standards | 1 | 1 | 0 | 6,782 | PRODUCT_STANDARD / NEEDS_OWNER_DECISION | `03_Standards/Product` after semantic comparison |
| Samples | 213 | 3 | 210 | 148,477,498 | REFERENCE_SAMPLE + REPRODUCIBLE_BUILD + CHARACTER_COLLECTION_BOOK | `Archive/Reference_Samples`, `04_Templates/Collection_Book`, or character collection-book root |
| README.md | 1 | 1 | 0 | 3,306 | HISTORICAL / NEEDS_OWNER_DECISION | Root documentation review |

The generated per-file inventory used the fields `PATH`, `SIZE`, `TRACKED`, `MODIFIED`, `SHA256`, `MTIME`, `FILE_TYPE` and `TOP_LEVEL_AREA`. Likely entity/session and dependency fields remain package-level below where filenames alone cannot establish ownership safely.

## Logical packages

| Package | Current evidence | Classification | Status | Proposed destination | Action later |
|---|---|---|---|---|---|
| P01/P02 Business `final_source_resolution` | 20 SHA256-identical finals, plus builder/Brandbook references | EXACT_DUPLICATE | BLOCKED | Existing `01_Characters/P01|P02/.../02_Final` | Cut consumers, re-hash 20/20, then delete duplicates |
| P02 Boudoir_v1 | Untracked session tree with delivery, upscale and marketing outputs | CHARACTER_SESSION_WIP | ACTIVE_WIP | `01_Characters/P02/02_Sessions/Boudoir_v1/WIP` | Owner review; do not call Final |
| P02 Lifestyle_Premium_v1 | Untracked session tree; prior run incomplete | CHARACTER_SESSION_WIP | UNKNOWN / ACTIVE_WIP | `01_Characters/P02/02_Sessions/Lifestyle_Premium_v1/WIP` | Reconcile manifest and candidate count |
| P03 Lifestyle_v1 / Business WIP | Untracked session and delivery/marketing outputs; existing Executive candidate set remains pending | CHARACTER_SESSION_WIP | OWNER_DECISION_REQUIRED | `01_Characters/P03/02_Sessions/<Session>/WIP` | Preserve `candidate_set`, `owner_approval: PENDING` |
| Brandbook | PDF, review folder, fonts and `build_brandbook_v1_2.py` are untracked; script reads legacy P01/P02/P03 paths | BRAND_WIP | ACTIVE_WIP | Candidate `03_Standards/Brand/WIP` | Decide standard vs marketing deliverable, then cut paths |
| Collection Book | Revision notes, preview, source data and manifest under Samples | CHARACTER_COLLECTION_BOOK + REPRODUCIBLE_BUILD | ACTIVE_WIP | `01_Characters/P02/03_Collection_Books/<Session>` plus `04_Templates/Collection_Book` | Separate reusable template from character output |
| Client delivery | Modified previews are tracked; generated delivery packages are untracked | ACTIVE_WIP | PROTECTED | Canonical session WIP / external client storage for real client files | Owner review before any move |
| Client experience | Modified intake plus untracked Boudoir intake/schema | CLIENT_EXPERIENCE_STANDARD + TEMPLATE | ACTIVE_WIP | `03_Standards/Client_Experience` and `04_Templates/Client_Intake` | Semantic split |
| Samples | 213 files mix collection-book revisions, examples and generated output | NEEDS_OWNER_DECISION | MIXED | Archive, templates or character roots | Package-level review required |

## P02 Boudoir and Lifestyle Premium

Both packages are untracked working trees with delivery/upscale/marketing material and no verified approval manifest establishing canonical finals. They are `ACTIVE_WIP` or `UNKNOWN`, not `APPROVED`. Recommended action for both is `OWNER_DECISION` followed by `MOVE_TO_WIP`; no file is promoted or changed in this phase.

## P03

The existing P03 Executive state remains semantically contradictory: candidate-set and pending approval coexist with QA/export material. Classification is `CHARACTER_SESSION_WIP` and recommendation is `OWNER_DECISION_REQUIRED`; no Final status is inferred.

## Brandbook and Collection Book

The Brandbook package is still WIP. The PDF is a generated output, the Python builder is active source, fonts are source dependencies, and review material is provenance. The safest candidate root is `03_Standards/Brand/WIP` pending a decision whether the PDF is a standard or a marketing deliverable. Collection Book material must be split between reusable templates and the P02 character package; it cannot be treated as one production asset.

## Dependency scans

Active legacy references were found in the untracked marketing builder and Brandbook builder, and in untracked delivery manifests under the legacy portfolio tree. Historical migration reports also contain legacy references. Because consumers were not edited in this analysis phase, active legacy reference count is not zero. No runtime or manifest path was rewritten.

## Remaining duplicate and placeholder analysis

- 20 P01/P02 `final_source_resolution` images: `EXACT_DUPLICATE`, deletion blocked by active consumers.
- Four `.gitkeep` files: retained until their containing legacy directories receive a semantic destination.
- No additional deletion was authorized or performed.

## OWNER_DECISIONS_REQUIRED

1. Continue or archive P02 Boudoir_v1?
2. Continue or close P02 Lifestyle_Premium_v1?
3. Approve P03 Executive finals or keep candidate-only?
4. Is the Brandbook a reusable Brand Standard or a Marketing deliverable?
5. Which Samples are reference examples to retain in Archive?
6. Which Collection Book files are reusable templates versus P02 character output?
7. Where should the untracked order workspace live?
8. Should modified delivery previews remain protected until the current session completes?

## Proposed migration waves

1. Safe semantic moves after owner decisions: standards, templates and clearly identified character WIP.
2. Dependency cutover: marketing builder, Brandbook builder and manifests.
3. WIP promotion: P02 sessions, P03, Brandbook and Collection Book.
4. Duplicate deletion: 20 finals, `.gitkeep` and any newly verified duplicates.
5. Remove `13 Production` only after active references, useful WIP and unique files reach zero.

Analysis stopped here as requested. No cleanup commit was created.
