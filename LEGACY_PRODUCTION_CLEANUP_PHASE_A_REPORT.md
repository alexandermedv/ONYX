# Legacy Production Cleanup — Phase A Report

**Date:** 2026-09-24
**Baseline HEAD:** `5898c183f2f254162691b6faf25ffb852e36ebf9`
**Scope:** path cutover, verified duplicate removal, obsolete-container cleanup, WIP preservation

## Protected pre-existing WIP

The following paths were recorded before Phase A and were not overwritten. The untracked list follows Git status directory collapsing; ignored physical files were inventoried separately.

### Modified at pre-flight

- `13 Production/Client_Delivery/Examples/Prepayment/ONYX_P01_BUSINESS_PREPAYMENT_PREVIEW.jpg`
- `13 Production/Client_Delivery/Examples/Prepayment/ONYX_P02_BUSINESS_PREPAYMENT_PREVIEW.jpg`
- `13 Production/Client_Delivery/Examples/Prepayment/ONYX_P03_BUSINESS_PREPAYMENT_PREVIEW.jpg`
- `13 Production/Client_Experience/Intake/ONYX_SIGNATURE_INTAKE_v1.md`
- `13 Production/Portfolio/P01/Business_V1/portfolio_framed_preview/ONYX_P01_BUSINESS_01_HERO.jpg`
- `13 Production/Portfolio/P01/Business_V1/portfolio_framed_preview/ONYX_P01_BUSINESS_02_CLOSE.jpg`
- `13 Production/Portfolio/P01/Business_V1/portfolio_framed_preview/ONYX_P01_BUSINESS_03_WAIST.jpg`
- `13 Production/Portfolio/P01/Business_V1/portfolio_framed_preview/ONYX_P01_BUSINESS_04_SEATED.jpg`
- `13 Production/Portfolio/P01/Business_V1/portfolio_framed_preview/ONYX_P01_BUSINESS_05_ENVIRONMENT.jpg`
- `13 Production/Portfolio/P01/Business_V1/portfolio_framed_preview/ONYX_P01_BUSINESS_06_ACTION.jpg`
- `13 Production/Portfolio/P01/Business_V1/portfolio_framed_preview/ONYX_P01_BUSINESS_07_3Q_BODY.jpg`
- `13 Production/Portfolio/P01/Business_V1/portfolio_framed_preview/ONYX_P01_BUSINESS_08_FULL_BODY.jpg`
- `13 Production/Portfolio/P01/Business_V1/portfolio_framed_preview/ONYX_P01_BUSINESS_09_MOOD.jpg`
- `13 Production/Portfolio/P01/Business_V1/portfolio_framed_preview/ONYX_P01_BUSINESS_10_EDITORIAL.jpg`
- `13 Production/Portfolio/P02/Business_V1/portfolio_framed_preview/ONYX_P02_BUSINESS_01_HERO.jpg`
- `13 Production/Portfolio/P02/Business_V1/portfolio_framed_preview/ONYX_P02_BUSINESS_02_CLOSE.jpg`
- `13 Production/Portfolio/P02/Business_V1/portfolio_framed_preview/ONYX_P02_BUSINESS_03_WAIST.jpg`
- `13 Production/Portfolio/P02/Business_V1/portfolio_framed_preview/ONYX_P02_BUSINESS_04_SEATED.jpg`
- `13 Production/Portfolio/P02/Business_V1/portfolio_framed_preview/ONYX_P02_BUSINESS_05_ENVIRONMENT.jpg`
- `13 Production/Portfolio/P02/Business_V1/portfolio_framed_preview/ONYX_P02_BUSINESS_06_ACTION.jpg`
- `13 Production/Portfolio/P02/Business_V1/portfolio_framed_preview/ONYX_P02_BUSINESS_07_3Q_BODY.jpg`
- `13 Production/Portfolio/P02/Business_V1/portfolio_framed_preview/ONYX_P02_BUSINESS_08_FULL_BODY.jpg`
- `13 Production/Portfolio/P02/Business_V1/portfolio_framed_preview/ONYX_P02_BUSINESS_09_MOOD.jpg`
- `13 Production/Portfolio/P02/Business_V1/portfolio_framed_preview/ONYX_P02_BUSINESS_10_EDITORIAL.jpg`
- `13 Production/Portfolio/P03/Business_V1/portfolio_framed_preview/ONYX_P03_BUSINESS_01_HERO.jpg`
- `13 Production/Portfolio/P03/Business_V1/portfolio_framed_preview/ONYX_P03_BUSINESS_02_CLOSE.jpg`
- `13 Production/Portfolio/P03/Business_V1/portfolio_framed_preview/ONYX_P03_BUSINESS_03_WAIST.jpg`
- `13 Production/Portfolio/P03/Business_V1/portfolio_framed_preview/ONYX_P03_BUSINESS_04_SEATED.jpg`
- `13 Production/Portfolio/P03/Business_V1/portfolio_framed_preview/ONYX_P03_BUSINESS_05_ENVIRONMENT.jpg`
- `13 Production/Portfolio/P03/Business_V1/portfolio_framed_preview/ONYX_P03_BUSINESS_06_ACTION.jpg`
- `13 Production/Portfolio/P03/Business_V1/portfolio_framed_preview/ONYX_P03_BUSINESS_07_3Q_BODY.jpg`
- `13 Production/Portfolio/P03/Business_V1/portfolio_framed_preview/ONYX_P03_BUSINESS_08_FULL_BODY.jpg`
- `13 Production/Portfolio/P03/Business_V1/portfolio_framed_preview/ONYX_P03_BUSINESS_09_MOOD.jpg`
- `13 Production/Portfolio/P03/Business_V1/portfolio_framed_preview/ONYX_P03_BUSINESS_10_EDITORIAL.jpg`
- `13 Production/Product_Standards/ONYX_GENERATION_ROUTE_POLICY_v1.md`
- `engine/production/onyx_delivery.py`

### Untracked at pre-flight

- `02_Marketing/Avito/Current/ONYX_AVITO_CAROUSEL_V3/`
- `13 Production/Brand/ONYX_BRANDBOOK_V1_2.pdf`
- `13 Production/Brand/Review/`
- `13 Production/Brand/Typography/Manrope-OFL.txt`
- `13 Production/Brand/Typography/Manrope-Variable.ttf`
- `13 Production/Brand/build_brandbook_v1_2.py`
- `13 Production/Client_Experience/Intake/ONYX_BOUDOIR_SIGNATURE_INTAKE_v1.md`
- `13 Production/Client_Experience/Intake/schemas/`
- `13 Production/Orders/ORD-2026-0003_CL-0002_Valentina/`
- `13 Production/Portfolio/P01/Business_V1/client_delivery/`
- `13 Production/Portfolio/P01/Business_V1/marketing_v2/`
- `13 Production/Portfolio/P02/Boudoir_V1/`
- `13 Production/Portfolio/P02/Business_V1/client_delivery/`
- `13 Production/Portfolio/P02/Business_V1/marketing_v2/`
- `13 Production/Portfolio/P02/Lifestyle_Premium_v1/`
- `13 Production/Portfolio/P03/Business_V1/client_delivery/`
- `13 Production/Portfolio/P03/Business_V1/marketing_v2/`
- `13 Production/Portfolio/P03/Lifestyle_V1/`
- `13 Production/Samples/P02_Business_Collection_Book_v1/GIT_REPORT.txt`
- `13 Production/Samples/P02_Business_Collection_Book_v1/NEW_FILES.txt`
- `13 Production/Samples/P02_Business_Collection_Book_v1/P02_BUSINESS_COLLECTION_BOOK_v1_manifest.yaml`
- `13 Production/Samples/P02_Business_Collection_Book_v1/PREFLIGHT.md`
- `13 Production/Samples/P02_Business_Collection_Book_v1/REVISION_05_CONTACT_SHEET.jpg`
- `13 Production/Samples/P02_Business_Collection_Book_v1/STYLE_REVIEW_REVISION_04.md`
- `13 Production/Samples/P02_Business_Collection_Book_v1/STYLE_REVIEW_REVISION_05.md`
- `13 Production/Samples/P02_Business_Collection_Book_v1/STYLE_REVIEW_REVISION_06.md`
- `13 Production/Samples/P02_Business_Collection_Book_v1/STYLE_REVIEW_REVISION_07.md`
- `13 Production/Samples/P02_Business_Collection_Book_v1/STYLE_REVIEW_REVISION_09.md`
- `13 Production/Samples/P02_Business_Collection_Book_v1/STYLE_REVIEW_REVISION_10.md`
- `13 Production/Samples/P02_Business_Collection_Book_v1/preflight_git_status.txt`
- `13 Production/Samples/P02_Business_Collection_Book_v1/preview/`
- `13 Production/Samples/P02_Business_Collection_Book_v1/revisions/`
- `13 Production/Samples/P02_Business_Collection_Book_v1/source_data.json`
- `engine/production/onyx_marketing_builder.py`
- `engine/production/onyx_pulid_collection.py`

## Dependency map

| Consumer/reference group | Classification | Phase A result |
|---|---|---|
| P01/P02 `PORTFOLIO_EXPORT_MANIFEST.json` | `ACTIVE_MANIFEST_DEPENDENCY` | Final and duplicate-cover paths changed to `01_Characters/<ID>/02_Sessions/Business_v1/02_Final`. Remaining unique previews and modified framed previews stay legacy. |
| P02 approval inventory and persona record | `ACTIVE_MANIFEST_DEPENDENCY` / `DOCUMENTATION_DEPENDENCY` | Approval scope now names canonical P02 finals. |
| Avito review validators | `ACTIVE_RUNTIME_DEPENDENCY` | Source and expected paths now resolve to canonical P02 finals; both validators pass. |
| Collection Book renderer and docs | `ACTIVE_RUNTIME_DEPENDENCY` | Reusable style/example data moved to `04_Templates`; renderer root fixed for canonical depth; test output goes to `tmp`, client output to `ONYX_CLIENT_ROOT`. |
| `engine/production/onyx_marketing_builder.py` | `DEFERRED_WIP_DEPENDENCY` | Untracked user WIP still expects `final_source_resolution` and legacy Brand fonts/assets; file was not edited. |
| Brandbook v1.2 builder | `DEFERRED_WIP_DEPENDENCY` | Untracked build reads P01/P02 finals plus P03 candidate assets; file and inputs retained. |
| P02 Collection Book revisions and sample data | `DEFERRED_WIP_DEPENDENCY` | Current untracked revisions retain legacy paths and were not edited. |
| Commercial-freeze snapshots, saved status/diffs and migration reports | `HISTORICAL_REFERENCE` | Preserved verbatim; clean Product Standards evidence moved to Archive. |
| Canonical docs linking the explicit P02 deferred sample | `DOCUMENTATION_DEPENDENCY` | Kept because the target WIP still exists. |
| Modified delivery, intake, route-policy and framed-preview files | `DEFERRED_WIP_DEPENDENCY` | Not edited or staged by Phase A. |

Post-cutover classification: `BROKEN_ACTIVE_DEPENDENCY = 0`.

## Portfolio cutover

| Session | Canonical session | Legacy source | Consumers | Status |
|---|---|---|---|---|
| P01 Business | `01_Characters/P01/02_Sessions/Business_v1` | `13 Production/Portfolio/P01/Business_V1` | Manifest cut over; untracked marketing builder and Brandbook WIP still consume legacy layout | `DEFERRED_WIP_DEPENDENCY` |
| P02 Business | `01_Characters/P02/02_Sessions/Business_v1` | `13 Production/Portfolio/P02/Business_V1` | Manifest, inventory and Avito validators cut over; untracked builders remain | `DEFERRED_WIP_DEPENDENCY` |
| P02 Lifestyle | `01_Characters/P02/02_Sessions/Lifestyle_v1` | No matching legacy session directory | Canonical package is complete | `CANONICAL` |
| P02 Boudoir | Not promoted | `13 Production/Portfolio/P02/Boudoir_V1` | Untracked session/delivery WIP | `DEFERRED_WIP_DEPENDENCY` |
| P02 Lifestyle Premium | Not promoted | `13 Production/Portfolio/P02/Lifestyle_Premium_v1` | Untracked run and manifests | `DEFERRED_WIP_DEPENDENCY` |
| P03 Executive | `01_Characters/P03/02_Sessions/Executive_v1` | `13 Production/Portfolio/P03/Business_V1` | Modified previews and untracked delivery/marketing WIP | `candidate_set`; `owner_approval: PENDING` |

## Verified duplicate deletion ledger

| LEGACY_PATH | CANONICAL_PATH | SHA256 | CONSUMERS_UPDATED | DELETED |
|---|---|---|---|---|
| `13 Production/Portfolio/P01/Business_V1/marketing_preview/ONYX_P01_BUSINESS_01_HERO.jpg` | `01_Characters/P01/02_Sessions/Business_v1/02_Final/ONYX_P01_BUSINESS_01_HERO.jpg` | `ad975499622405780a509cc9c174e08ebf5c88be9de7dd3c7c2f2f0fcc80226a` | YES | YES |
| `13 Production/Portfolio/P01/Business_V1/marketing_preview/ONYX_P01_BUSINESS_02_CLOSE.jpg` | `01_Characters/P01/02_Sessions/Business_v1/02_Final/ONYX_P01_BUSINESS_02_CLOSE.jpg` | `c43dfb71dd57e6814cdd19378e7e4a06e53eba8bc198e489676afa75c6fa9582` | YES | YES |
| `13 Production/Portfolio/P01/Business_V1/marketing_preview/ONYX_P01_BUSINESS_03_WAIST.jpg` | `01_Characters/P01/02_Sessions/Business_v1/02_Final/ONYX_P01_BUSINESS_03_WAIST.jpg` | `cd6d2f688c5dbe454734049c45f25d0abdaf17b4eb102c42e9a828babdff8ee0` | YES | YES |
| `13 Production/Portfolio/P01/Business_V1/marketing_preview/ONYX_P01_BUSINESS_04_SEATED.jpg` | `01_Characters/P01/02_Sessions/Business_v1/02_Final/ONYX_P01_BUSINESS_04_SEATED.jpg` | `e0996e725e1ba886fa680c7277d7635794ea633a0b1aecdfab101e2223b9712b` | YES | YES |
| `13 Production/Portfolio/P01/Business_V1/marketing_preview/ONYX_P01_BUSINESS_05_ENVIRONMENT.jpg` | `01_Characters/P01/02_Sessions/Business_v1/02_Final/ONYX_P01_BUSINESS_05_ENVIRONMENT.jpg` | `dc02696283a2560e2d29bb47db0727e8c6644a6ba85710c15574cc7d83434582` | YES | YES |
| `13 Production/Portfolio/P01/Business_V1/marketing_preview/ONYX_P01_BUSINESS_06_ACTION.jpg` | `01_Characters/P01/02_Sessions/Business_v1/02_Final/ONYX_P01_BUSINESS_06_ACTION.jpg` | `a44948d6ca7e947254b0186eb5a71c8e1598a3853ad301bfb54e4c64bb14ad48` | YES | YES |
| `13 Production/Portfolio/P01/Business_V1/marketing_preview/ONYX_P01_BUSINESS_07_3Q_BODY.jpg` | `01_Characters/P01/02_Sessions/Business_v1/02_Final/ONYX_P01_BUSINESS_07_3Q_BODY.jpg` | `f9de896c710f8c827e0fd1294f0cefac2335134b6e337bb2896c3cd2aa887337` | YES | YES |
| `13 Production/Portfolio/P01/Business_V1/marketing_preview/ONYX_P01_BUSINESS_08_FULL_BODY.jpg` | `01_Characters/P01/02_Sessions/Business_v1/02_Final/ONYX_P01_BUSINESS_08_FULL_BODY.jpg` | `1bbaf834c2d4656e78d4847a3f4e3309c1b353a54468c1f4a6d436cd45500b91` | YES | YES |
| `13 Production/Portfolio/P01/Business_V1/marketing_preview/ONYX_P01_BUSINESS_09_MOOD.jpg` | `01_Characters/P01/02_Sessions/Business_v1/02_Final/ONYX_P01_BUSINESS_09_MOOD.jpg` | `00a2d4fbf221fa15a55f4b73035303a8c4d304c7670c297b046c7675a2d0455d` | YES | YES |
| `13 Production/Portfolio/P01/Business_V1/marketing_preview/ONYX_P01_BUSINESS_10_EDITORIAL.jpg` | `01_Characters/P01/02_Sessions/Business_v1/02_Final/ONYX_P01_BUSINESS_10_EDITORIAL.jpg` | `8d3354de525ff6d8ec9fd6cf8812918d484b1ce91a0e43457b5f79132ff575ca` | YES | YES |
| `13 Production/Portfolio/P01/Business_V1/marketing_preview/ONYX_P01_BUSINESS_COVER.jpg` | `01_Characters/P01/02_Sessions/Business_v1/02_Final/ONYX_P01_BUSINESS_01_HERO.jpg` | `ad975499622405780a509cc9c174e08ebf5c88be9de7dd3c7c2f2f0fcc80226a` | YES | YES |
| `13 Production/Portfolio/P02/Business_V1/marketing_preview/ONYX_P02_BUSINESS_01_HERO.jpg` | `01_Characters/P02/02_Sessions/Business_v1/02_Final/ONYX_P02_BUSINESS_01_HERO.jpg` | `ffcd2a6e021d4edc4e1fd31159ae314ecde6097ea8610267ea86b7fe24c05162` | YES | YES |
| `13 Production/Portfolio/P02/Business_V1/marketing_preview/ONYX_P02_BUSINESS_02_CLOSE.jpg` | `01_Characters/P02/02_Sessions/Business_v1/02_Final/ONYX_P02_BUSINESS_02_CLOSE.jpg` | `a8c54ee3f73541d513f19e89c84beb05e319f33e0c40edbc636e11c335387582` | YES | YES |
| `13 Production/Portfolio/P02/Business_V1/marketing_preview/ONYX_P02_BUSINESS_03_WAIST.jpg` | `01_Characters/P02/02_Sessions/Business_v1/02_Final/ONYX_P02_BUSINESS_03_WAIST.jpg` | `0e984d2851d5e3d99f4ff97906dbcfe748d27482eec4aa1280bf251738e23479` | YES | YES |
| `13 Production/Portfolio/P02/Business_V1/marketing_preview/ONYX_P02_BUSINESS_04_SEATED.jpg` | `01_Characters/P02/02_Sessions/Business_v1/02_Final/ONYX_P02_BUSINESS_04_SEATED.jpg` | `c51335f9dd689e77d0169be643b7d721fd443c23487b51c8d8bbb06ff1c0ddc3` | YES | YES |
| `13 Production/Portfolio/P02/Business_V1/marketing_preview/ONYX_P02_BUSINESS_05_ENVIRONMENT.jpg` | `01_Characters/P02/02_Sessions/Business_v1/02_Final/ONYX_P02_BUSINESS_05_ENVIRONMENT.jpg` | `e5fc685dd0d6859f7afeaa31f85dab2659535dd7ac58f7aea6c368ecb68157c0` | YES | YES |
| `13 Production/Portfolio/P02/Business_V1/marketing_preview/ONYX_P02_BUSINESS_06_ACTION.jpg` | `01_Characters/P02/02_Sessions/Business_v1/02_Final/ONYX_P02_BUSINESS_06_ACTION.jpg` | `f6c071d10147c4187192b2cf6274f5366f53b15fc07cbf6b3953b8d748f3a1c8` | YES | YES |
| `13 Production/Portfolio/P02/Business_V1/marketing_preview/ONYX_P02_BUSINESS_07_3Q_BODY.jpg` | `01_Characters/P02/02_Sessions/Business_v1/02_Final/ONYX_P02_BUSINESS_07_3Q_BODY.jpg` | `ced65a4bab43cdeadd2406321eb2c1fd8a63971081f58288c39663d35c6ace58` | YES | YES |
| `13 Production/Portfolio/P02/Business_V1/marketing_preview/ONYX_P02_BUSINESS_08_FULL_BODY.jpg` | `01_Characters/P02/02_Sessions/Business_v1/02_Final/ONYX_P02_BUSINESS_08_FULL_BODY.jpg` | `6cc8ec0317a48b54fd5c48d9d7a515f29f1b8fcfc0ee5cd53ba005f87732a425` | YES | YES |
| `13 Production/Portfolio/P02/Business_V1/marketing_preview/ONYX_P02_BUSINESS_09_MOOD.jpg` | `01_Characters/P02/02_Sessions/Business_v1/02_Final/ONYX_P02_BUSINESS_09_MOOD.jpg` | `aa84f1f2f61e125cd6b91fbbb8095a529a1408ead5b4dd830298be8a91c746fd` | YES | YES |
| `13 Production/Portfolio/P02/Business_V1/marketing_preview/ONYX_P02_BUSINESS_10_EDITORIAL.jpg` | `01_Characters/P02/02_Sessions/Business_v1/02_Final/ONYX_P02_BUSINESS_10_EDITORIAL.jpg` | `d918c5e894d5a6f8a0b191e1d78db72f03d3a30e4be98db4797e60c99261f6f5` | YES | YES |
| `13 Production/Portfolio/P02/Business_V1/marketing_preview/ONYX_P02_BUSINESS_COVER.jpg` | `01_Characters/P02/02_Sessions/Business_v1/02_Final/ONYX_P02_BUSINESS_01_HERO.jpg` | `ffcd2a6e021d4edc4e1fd31159ae314ecde6097ea8610267ea86b7fe24c05162` | YES | YES |
| `13 Production/Brand/Colors/.gitkeep` | Empty legacy container removed | `01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b` | N/A | YES |
| `13 Production/Brand/Templates/.gitkeep` | Empty legacy container removed | `01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b` | N/A | YES |
| `13 Production/Brand/Watermark/.gitkeep` | Empty legacy container removed | `01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b` | N/A | YES |
| `13 Production/Marketing/Avito/.gitkeep` | Empty legacy container removed | `01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b` | N/A | YES |

Exact duplicate bytes removed: **9588273**.

## Other cleanup

- Moved `13 Production/Templates/Collection_Book/example_data` and `template/style.json` into `04_Templates/Collection_Book`.
- Archived 13 clean commercial-freeze/history files under `Archive/Legacy_Structure/Product_Standards` without rewriting their contents.
- Migrated generic client/order rules into `docs/client_storage.md`, then removed the obsolete Clients and Orders README files.
- Removed two reproducible legacy `.pyc` files and the now-empty legacy Templates and Marketing containers.
- Kept the empty `13 Production/Clients/CL-0002_Valentina` directory untouched under client-data safeguards.

## Remaining exact duplicates

- 20 P01/P02 `final_source_resolution` images remain SHA256-identical to canonical finals. Deletion is blocked by the protected untracked marketing builder and Brandbook v1.2 build.
- Four `.gitkeep` files remain in nonempty or active legacy directories: Brand Logo, Brand Typography, Portfolio P01 and Portfolio P02.

## Verification

- Production pilot: 5 tests passed.
- Collection Book unit tests: 3 tests passed.
- Collection Book end-to-end dry-run: 15-page PDF, 18 output files; temporary output removed.
- Marketing builder dry-run from canonical P01 finals: 35 files; temporary output removed.
- Avito review validators: PASS and PASS.
- Changed JSON parsed: 3 files.
- YAML parsed: 2 manifests.
- Manifest path existence: 166 checked, 0 missing.
- P03 remains `candidate_set`, `owner_approval: PENDING`, `final_count: 0`.
- Final Markdown links, active legacy-reference classification and diff checks are recorded before commit.

## Phase B blockers

- Merge or otherwise resolve the protected `onyx_marketing_builder.py` WIP against canonical session layout.
- Finish or close Brandbook v1.2, P01/P02/P03 delivery and marketing builds, P02 Boudoir/Lifestyle Premium, and the Collection Book revisions.
- Reconcile P03 upscale evidence and obtain owner approval before declaring canonical finals.
- Re-run SHA256 and remove the remaining 20 duplicate finals only after all WIP consumers use canonical paths.
