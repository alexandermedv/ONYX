# ONYX residual decision pack

Read-only inventory at HEAD `1e57d649877a8698a950b2eab6317a8847b61a16`.

## Inventory

All **193/193** residual files under `13 Production` were hashed and classified at package level. Total: **1,336,939,010 bytes (~1,274.96 MiB)**.

| Package | Files | Bytes | Modified | Untracked | Classification | Canonical destination |
|---|---:|---:|---:|---:|---|---|
| Brand | 14 | 5,953,167 | 0 | 0 | MOVE_CANONICAL / HISTORICAL_REFERENCE | `03_Standards/Brand`, `Archive/Legacy_Structure` |
| Client_Delivery | 6 | 687,838 | 3 | 0 | KEEP_WIP_TEMPORARILY | `03_Standards`, `04_Templates`, canonical session WIP |
| Client_Experience | 4 | 11,561 | 1 | 2 | MOVE_CANONICAL / KEEP_WIP_TEMPORARILY | `03_Standards/Client_Experience`, `04_Templates/Client_Intake` |
| Orders | 1 | 2,989 | 0 | 1 | NEEDS_OWNER_DECISION | External client storage, standards, template or docs |
| Portfolio | 166 | 1,330,273,367 | 30 | 60 | EXACT_DUPLICATE_DELETE / KEEP_WIP_TEMPORARILY / MOVE_CANONICAL | `01_Characters`, `02_Marketing`, Archive |
| Product_Standards | 1 | 6,782 | 1 | 0 | KEEP_WIP_TEMPORARILY | `03_Standards/Product` or Archive after review |
| root README | 1 | 3,306 | 0 | 0 | HISTORICAL_REFERENCE | `Archive/Legacy_Structure` or documentation review |

The per-file inventory captured relative path, byte size, SHA256, tracked/untracked state, modified state, extension, package and filesystem mtime. No file was modified by this analysis.

## Unique useful legacy files

The non-duplicate useful set is not zero. The exact groups requiring later action are:

- 30 modified Portfolio preview files: protected user WIP; keep temporarily until owner review confirms promotion/obsolescence.
- 60 untracked Portfolio files: active session/delivery/marketing WIP already partly promoted; remaining files need package-level verification before deletion.
- 3 modified Client_Delivery previews: keep temporarily; byte similarity to canonical derivatives is insufficient because user modifications exist.
- 1 modified Product Standards document: compare with canonical Product standards before promotion.
- 1 untracked Orders file: `NEEDS_OWNER_DECISION`; no permanent in-repo Orders root is allowed.

## Duplicate readiness audit

The 20 P01/P02 pairs remain SHA256-identical to canonical finals. Their individual status is:

| Pair | SHA256 | Runtime consumers | Manifest consumers | Builder/Avito consumers | Brandbook/Collection Book | READY_TO_DELETE |
|---|---|---:|---:|---:|---:|---|
| P01 Business 01–10 | MATCH (10/10) | 0 after pipeline cutover | 0 in active canonical manifests | 0 in current builders; historical scripts remain | no active canonical refs found | NO — final visual/dry-run evidence and residual WIP gate pending |
| P02 Business 01–10 | MATCH (10/10) | 0 after pipeline cutover | 0 after delivery/Collection Book cutover | 0 in current builders; historical scripts remain | no active canonical refs found | NO — final visual/dry-run evidence and residual WIP gate pending |

The remaining `NO` reason is `VALIDATION_PENDING`, not an active path dependency: the Brandbook visual environment is unavailable (`Pillow` missing), residual modified/untracked WIP is still present, and the final deletion gate has not been approved. This is separate from SHA256/path safety.

## Projected actions (no execution)

| Class | Files | Approx. bytes | Proposed action |
|---|---:|---:|---|
| EXACT_DUPLICATE_DELETE | 20 | ~8.69 MiB | Delete only after final gate |
| REPRODUCIBLE_DELETE | 0 confirmed | 0 confirmed | Requires builder proof |
| MOVE_CANONICAL | package-dependent | not safely aggregated | Promote only after WIP review |
| MOVE_ARCHIVE | package-dependent | not safely aggregated | Archive historical/reference material |
| KEEP_WIP_TEMPORARILY | 95+ | majority of residual bytes | Preserve modified/untracked WIP |
| NEEDS_OWNER_DECISION | 1 logical package | 2,989 bytes | Orders file destination |

Projected residual cannot be reduced safely to zero in this phase because useful Portfolio WIP and modified delivery/Product Standards files remain unresolved.

## Decision pack

| # | Package | Files | Recommendation |
|---:|---|---:|---|
| 1 | Portfolio modified previews | 30 | Keep until owner confirms promotion or abandonment |
| 2 | Portfolio untracked WIP | 60 | Verify package-by-package; promote useful WIP, delete only proven reproducible output |
| 3 | Client_Delivery previews | 3 modified | Preserve current user edits; later compare with canonical derivatives |
| 4 | Product_Standards | 1 modified | Owner review against `03_Standards/Product` |
| 5 | Orders | 1 untracked | Owner decision: client storage, standards, template, docs or archive |

## Final gate

- Classified: **193/193**.
- Unique useful legacy files: **not zero**.
- Delete-ready duplicates: **0/20** under the conservative gate above.
- `FINAL_DELETE_AND_RETIRE_13_PRODUCTION = NO`.

No deletes, moves, staging, commit or push were performed.
