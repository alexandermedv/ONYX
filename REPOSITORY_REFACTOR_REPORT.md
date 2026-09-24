# ONYX Repository Refactor Report

**Date:** 2026-09-24
**Branch:** `main`
**Preflight HEAD:** `b283511f697cef5197dde2121563f32360723308`

## Outcome

The repository now has one declared authority for each active content domain. This pass removed top-level numbering collisions from the clean knowledge base and archived two early brand-cover explorations. Existing production WIP was preserved in place and classified as `DEFERRED_WIP`.

The structure is documented in [REPOSITORY_STRUCTURE.md](REPOSITORY_STRUCTURE.md).

## Preflight inventory

- Initial working tree: 575 entries.
- Existing WIP by root: 541 entries under `13 Production`, 31 under `02_Marketing`, and 3 under `engine`.
- External client storage: 772 files, approximately 2124.14 MB, under `D:\AI\ONYX_Clients`.
- Existing client migration verification: 766 source/destination SHA256 checks passed, zero failed.
- Clean tracked files remaining under legacy `13 Production`: 142.
- Dirty tracked files under legacy `13 Production`: 35.
- Untracked files reported under legacy `13 Production`: 541 status entries before this pass.

## Final architecture

| Domain | Canonical location |
| --- | --- |
| Synthetic characters and portfolio finals | `01_Characters/` |
| Shared advertising and channel exports | `02_Marketing/` |
| Brand, product, portfolio, marketing and client-experience standards | `03_Standards/` |
| Reusable templates | `04_Templates/` |
| R&D history | `09 Experiments/` |
| Execution code and workflows | `engine/`, `comfyui-workflows/` |
| ADRs and knowledge base | `docs/` |
| Real clients | `D:\AI\ONYX_Clients` |

## Old → new mapping implemented in this pass

| Old path | New path | Result |
| --- | --- | --- |
| `00 Home` | `docs/Knowledge_Base/Home` | moved |
| `01 Brand` | `docs/Knowledge_Base/Brand_Legacy` | moved; explicitly non-authoritative |
| `02 Business` | `docs/Knowledge_Base/Business` | moved |
| `03 Product` | `docs/Knowledge_Base/Product_Legacy` | moved; stable rules remain in `03_Standards/Product` |
| `04 Engineering` | `docs/Knowledge_Base/Engineering` | moved |
| `05 AI Pipeline` | `docs/Knowledge_Base/AI_Pipeline` | moved |
| `06 Research` | `docs/Knowledge_Base/Research` | moved |
| `07 Prompts` | `docs/Knowledge_Base/Prompts` | moved |
| `08 Workflows` | `docs/Knowledge_Base/Workflows` | moved |
| `10 Roadmap` | `docs/Knowledge_Base/Roadmap` | moved |
| `11 Library` | `docs/Knowledge_Base/Library` | moved |
| `12 Decisions` | `docs/Decisions` | moved |
| `assets/brand/cover` | `Archive/Legacy_Structure/Brand_Cover_Explorations` | archived as two different historical versions |

This pass moved 36 tracked files. It deleted no content files. Ten verified-empty legacy or duplicate directories were removed from the working filesystem after their contents were checked.

## Earlier completed migration already present at preflight

The 2026-09-23 content migration had already established the four canonical content roots and verified 296 legacy moves: 291 byte-identical moves and five intentional reference transformations. The 2026-09-24 protected client migration had already copied and verified 766 private files outside Git before removing tracked repository copies.

## Duplicate clusters

| Entity | Paths | Assessment | Authority / status |
| --- | --- | --- | --- |
| Brand | `03_Standards/Brand`, legacy `13 Production/Brand`, archived `assets/brand/cover` | Approved standards are canonical. Legacy Brand contains untracked Brandbook/Typography WIP. The two old covers had different SHA256 values and were archived. | `03_Standards/Brand`; legacy is `DEFERRED_WIP` |
| Characters | `01_Characters`, `09 Experiments/identity_benchmark_v1`, legacy `13 Production/Portfolio` | `01_Characters` contains promoted identity/session assets; experiment copies are R&D evidence. Legacy Portfolio contains active exports and delivery WIP. | `01_Characters`; others are evidence or `DEFERRED_WIP` |
| Portfolio | character sessions plus legacy `13 Production/Portfolio` | Portfolio is represented by approved finals inside the character package. Fifty clean legacy files were byte-identical to canonical files, but were retained because WIP manifests and derivative builders still reference the legacy package. | `01_Characters/<ID>/02_Sessions`; legacy `DEFERRED_WIP` |
| Marketing | `02_Marketing`, legacy marketing trees below `13 Production` | Shared Avito package is canonical. Current V3 and character `marketing_v2` trees are active WIP. | `02_Marketing`; legacy/current untracked work is `DEFERRED_WIP` |
| Product rules | `03_Standards/Product`, legacy `13 Production/Product_Standards`, archived `docs/Knowledge_Base/Product_Legacy` | Stable promoted rules are canonical. One generation-route policy and historical freeze material remain in the legacy root. | `03_Standards/Product`; legacy `DEFERRED_WIP`/history |
| Templates | `04_Templates`, legacy `13 Production/Templates` and Samples | Reusable canonical templates were promoted. Collection Book revisions remain active WIP. | `04_Templates`; legacy `DEFERRED_WIP` |
| Clients/orders | `D:\AI\ONYX_Clients`, ignored legacy client/order paths | External copies are verified. Active Valentina WIP remains in place under the preservation rule. | external root; repository leftovers `DEFERRED_WIP` |

## References

Active runtime/manifests pointing to the moved engineering runbook were updated to `docs/Knowledge_Base/Engineering/ComfyUI FLUX Windows Runbook.md`. Root README navigation and active ADR links were also updated.

Old paths still found inside commercial-freeze reports, saved Git status, saved diffs and experiment provenance are historical evidence rather than live links. They were intentionally not rewritten.

## Removed exact duplicates

No content file was deleted as an exact duplicate in this pass. Although 50 clean legacy files have canonical SHA256 matches, deleting them would break active modified or untracked manifests/build work in the same legacy packages. They remain `DEFERRED_WIP` until that work is closed.

## Ambiguous and deferred leftovers

- Entire `13 Production` legacy root: mixed clean content and 541 initial WIP entries.
- Brandbook v1.2, Manrope files and Brand build script under legacy Brand.
- P01/P02/P03 framed previews, client-delivery trees and `marketing_v2` exports.
- P02 Boudoir and Lifestyle Premium sessions.
- P02 Collection Book revisions and previews.
- Modified generation-route policy.
- Avito Carousel V3 under canonical Marketing, currently untracked WIP.
- Valentina order/runtime remnants already copied externally but still active locally.
- Three engine files with user WIP.

These items were not moved, deleted, renamed or edited by this pass.

## Client files remaining in the repository

No new client media was added or staged. Generic templates and safe policy documentation remain. Ignored or untracked active client WIP may still exist physically in legacy paths; its authoritative verified copy is external, and source cleanup is deferred until the active workflow is closed.

## Counts

- Files moved in this pass: 36.
- Files deleted as exact duplicates: 0.
- Files archived in this pass: 2.
- Empty legacy or duplicate directories removed: 10.
- Active references updated: 40 (15 references affected by the directory moves and 25 canonical cross-links repaired after the earlier content migration).
- Known broken links in canonical Markdown after the post-check: 0.

## Verification

- All changed JSON manifests parse successfully.
- `engine/production_pilot/runner.py` compiles successfully.
- Production-pilot unit suite: 5 tests passed.
- `git diff --check`: passed; only Windows line-ending notices were emitted.
- Canonical Markdown local-link scan: 0 broken links.
