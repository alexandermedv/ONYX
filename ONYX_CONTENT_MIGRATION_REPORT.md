# ONYX content migration report

Date: 2026-09-23
Branch: `main`
HEAD at migration start: `e003c4e1364f01be5c9c5e0a9f6e811c2fb5d073`

## Completed

- Created `01_Characters`, `02_Marketing`, `03_Standards` and `04_Templates`.
- Promoted P01, P02 and P03 frozen identity assets by COPY; experiment originals remain unchanged.
- Promoted P01 Business v1, P02 Business v1 and P02 Lifestyle v1 production packages.
- Promoted P03 Executive v1 candidate source set only.
- Confirmed SHA256 integrity for the promoted identity and session source sets.
- Moved the clean, tracked Avito Launch Pack v1 into `02_Marketing/Avito/Current`; its v2.6 QA report records `APPROVED_FOR_AVITO_PUBLISH`.
- Moved stable, unmodified Brand/Product/Portfolio/Marketing/Client Experience documents and reusable template files.
- Added defensive ignore rules for in-repository client-like folders.
- Created the external client-storage skeleton at `D:\AI\ONYX_Clients` without copying current WIP.

## Deferred WIP

- P01/P02/P03 modified framed previews.
- Character `marketing_v2` and `client_delivery` trees.
- P02 Boudoir v1.
- P02 Lifestyle Premium v1, incomplete at 4/15 candidates.
- P02 Business Collection Book revisions and previews.
- Modified `ONYX_GENERATION_ROUTE_POLICY_v1.md`.
- New Brand Review/Typography/build artifacts.
- `val4.jpg`, Valentina order trees and engine WIP.

## Characters

- P01: frozen identity, Business v1 source/final/branded package migrated.
- P02: frozen identity with approved collage still missing; Business v1 and Lifestyle v1 migrated; Boudoir and Lifestyle Premium remain WIP.
- P03: frozen identity and Executive v1 candidate source migrated; status remains `candidate_set`, `owner_approval: PENDING`, with no canonical Final.

## Clients

The target external root is `D:\AI\ONYX_Clients`, with `CL-0001_Alexander` and `CL-0002_Valentina` skeleton folders. Existing client orders were not copied or moved because the current trees contain user-owned untracked WIP. Client migration remains a separate protected phase. No client binaries were staged or deleted.

## Marketing

The 250-file `ONYX_AVITO_LAUNCH_PACK_v1` is now under `02_Marketing/Avito/Current`. Character-specific v2 WIP remains in the legacy portfolio folders. No full portfolio was duplicated into Marketing.

## Standards and Templates

Stable files moved into `03_Standards/Brand`, `Product`, `Portfolio`, `Marketing` and `Client_Experience`. Reusable Collection Book, Client Intake and metadata templates moved into `04_Templates`. Modified or untracked WIP was left in place.

## Legacy folders

`13 Production` remains intact as a legacy source for deferred WIP, client orders and files not yet migrated. `09 Experiments` keeps its existing name. No legacy directory was deleted.

## Broken path scan

Legacy references remain intentionally in experiment history, deferred WIP and manifests whose source provenance points to the preserved originals. Production references requiring update are deferred until the corresponding WIP is migrated. Engine paths were not changed in this phase.

## Git

- The migration-only staging set is intentionally populated for the checkpoint commit; unrelated WIP remains unstaged.
- No commit or push was performed.
- Existing user WIP was preserved.

## Migration checkpoint verification

- Initial checkpoint before selective staging: 465 status lines, 39 modified, 297 deleted source paths, 129 untracked, staged empty.
- Current staged migration snapshot: 414 paths; Git detects 296 legacy renames, 115 additions and 3 root metadata modifications.
- Move verification: 296 legacy paths checked; 291 `IDENTICAL_MOVE`, 5 `INTENTIONAL_TRANSFORM`, 0 `MISSING_DESTINATION`, 0 `AMBIGUOUS`.
- The five intentional transforms update canonical provenance/template references to the new locations.
- Staged binary scan: 275 files, 291,433,965 bytes total. These are synthetic character assets, ONYX marketing assets, brand PDFs/PNG and template assets. No client binaries are staged.
- Client scan found only generic storage/WIP documentation references; no client intake, reference, delivery or order files are in the staged set.
- New canonical packages contain no unresolved references to the migrated `13 Production/Portfolio`, `13 Production/Marketing`, `13 Production/Samples`, `13 Production/Brand` or `13 Production/Product_Standards` paths.
- JSON parsing passed. A full YAML parser is unavailable in the base Python runtime; required-field and structural manifest checks were performed without installing dependencies.

## Verification snapshot

- Promoted identity/session hash checks: 58 PASS.
- Current Avito package files: 250 plus its launch requirements document.
- `01_Characters/P01`: 47 files; `P02`: 66 files; `P03`: 23 files.
- `03_Standards`: 29 files; `04_Templates`: 16 files.
- Working tree after migration: 465 status lines — 39 modified, 297 deleted source paths from safe content moves, 129 untracked paths; staged count 0.
- Client-like paths inside the repository are defensively ignored; external client folders are empty skeletons pending WIP-safe copy verification.
