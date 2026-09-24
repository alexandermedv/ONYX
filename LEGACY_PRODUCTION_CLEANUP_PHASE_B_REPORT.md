# Legacy Production Cleanup — Phase B assessment

Date: 2026-09-24  
Baseline commit: `5c3a25011fd22f67764faa7d9ae8864ab3341e2e`

## Result

Phase B cannot safely remove `13 Production` yet. The pre-flight inventory found 701 files (about 5,287 MiB) and active, user-owned WIP whose canonical destination or lifecycle is not unambiguous. Per the task stop condition, the legacy tree remains as a residual and no destructive cleanup was performed.

## Inventory

| Block | Files | Size (MiB) | Current classification | Residual reason |
|---|---:|---:|---|---|
| Brand | 33 | 41.48 | ACTIVE_WIP / NEEDS_DECISION | Brandbook source, generated PDF, review material, fonts and builder are untracked; semantic split is unresolved. |
| Client_Delivery | 6 | 0.66 | ACTIVE_WIP / NEEDS_DECISION | Modified previews and untracked delivery packages contain legacy paths and must be reconciled with the protected delivery WIP. |
| Client_Experience | 4 | 0.01 | ACTIVE_WIP | Modified intake and untracked schema/Boudoir intake are user WIP. |
| Orders | 1 | negligible | ACTIVE_WIP | Untracked order workspace; no approved canonical order destination was identified. |
| Portfolio | 442 | 5,103.57 | ACTIVE_WIP / EXACT_DUPLICATE_BLOCKED | P01/P02 final duplicates are blocked by active marketing-builder and Brandbook references; P02/P03 session WIP and modified previews remain. |
| Product_Standards | 1 | 0.01 | NEEDS_DECISION | Modified route policy needs comparison with canonical Product standards before promotion or archival. |
| Samples | 213 | 141.60 | NEEDS_DECISION / ACTIVE_WIP | Collection Book revisions and generated sample sets mix reusable templates, character output and reproducible builds. |

## Blocking dependencies

- 20 SHA256-identical P01/P02 `final_source_resolution` files still have active consumers in the untracked marketing builder and Brandbook WIP. They were not deleted.
- Active untracked `engine/production/onyx_marketing_builder.py` still contains legacy Brand and `final_source_resolution` paths. It was not overwritten.
- Active manifests under legacy WIP still contain `13 Production` paths; therefore the active manifest reference count is not zero.
- User-modified previews, intake, delivery code and route policy were preserved in place.
- P02 Boudoir, P02 Lifestyle Premium, P03 Lifestyle and Collection Book revisions require an explicit semantic destination before movement.

## Safety decision

No whole-tree deletion, broad move, reset, stash, clean, checkout, or push was performed. Phase B remains open with the minimum residual needed to preserve user WIP and unresolved dependencies.

