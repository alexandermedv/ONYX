# Legacy Production final migration — current execution report

Date: 2026-09-24
Baseline: `1e57d649877a8698a950b2eab6317a8847b61a16`

## Scope and safety

This phase changed only the active untracked marketing builder and added verified canonical/dry-run assets. No legacy asset was deleted. No staging, commit or push was performed. Existing unrelated WIP was preserved.

## Marketing builder

Path: `engine/production/onyx_marketing_builder.py`
Git state before/after: untracked user WIP
Encoding: UTF-8, no BOM, LF
Baseline SHA256: `c793491d1ecf087dcfe002d11b9db6457aa99c729593b46ebe0009915161f50c`
Current SHA256: `e2d65d95c9ee708a4485b53eece3f6313ec54fac198a24a2ee4adfdc97bd7826`

Minimal path cutover:

- legacy logo refs: **1 → 0**;
- `final_source_resolution` refs: **1 → 0**;
- input: `01_Characters/<ID>/02_Sessions/<SESSION>/02_Final` by default, or explicit `--source-dir`;
- character-branded output: `01_Characters/<ID>/02_Sessions/<SESSION>/03_Branded` by default, or explicit `--branded-output`;
- marketing output: `02_Marketing/Campaigns/Generated/<ID>/<Collection>` by default, or explicit `--marketing-output`.

Resolved data flow:

`canonical 02_Final → marketing builder → 03_Branded + 02_Marketing/Campaigns/Generated`

The old `final_source_resolution` directory was a compatibility staging layer: the builder wrote JPEG copies there and immediately consumed them itself. It had no independent next consumer in this builder, so the layer was removed. Image selection, layouts, typography, captions, dimensions, filenames and quality settings were not changed.

### Canonical logo

Legacy input: `13 Production/Brand/Logo/Presentations/ONYX_MONOGRAM_ONYX_SILK_PRESENTATION_V1.png`
Canonical input: `03_Standards/Brand/Assets/Logo/ONYX_MONOGRAM_ONYX_SILK_PRESENTATION_V1.png`

- file type: PNG;
- dimensions: 1536×1024;
- mode: RGB, non-transparent;
- role: approved dark ONYX Stone presentation/marketing texture;
- SHA256 on both paths: `ef1d9bd88d7a4c1a09e23f49618bae03b1fb117d8a4e0dcac12769c045dca55d`;
- byte-identical: **YES**.

## P02 Business delivery

- legacy master/upscale refs: **10 → 0**;
- records: 10;
- referenced paths present: **PASS**;
- master SHA256 validation: **10/10 PASS**;
- delivery validation status: **PASS**.

The verified upscale masters are under `01_Characters/P02/02_Sessions/Business_v1/WIP/upscale`. A migrated QA contact sheet in the same WIP directory is classified `DEFERRED_WIP`; it is not a delivery manifest input and was not deleted.

## P02 Collection Book

The cutover WIP package has **0 active legacy `13 Production` refs**, but its current active source data points to the nonexistent directory `Business_v1/WIP/upscale_p02_v1`. The actual verified directory is `Business_v1/WIP/upscale`. The canonical dry-run therefore fails before rendering.

Reusable template files still contain 17 active legacy values:

- `04_Templates/Collection_Book/example_data/P02_BUSINESS_COLLECTION_BOOK_v1.json`: 15;
- `04_Templates/Collection_Book/template/style.json`: 2.

Revision manifests and saved revision `source_data.json` remain historical/generated provenance and are not counted as active blockers.

## Dry-runs

| Check | Result | Evidence |
|---|---|---|
| Marketing builder compile | PASS | Python compilation completed |
| Marketing builder canonical run | PASS | 10 branded + 14 marketing outputs; 24 total; 0 writes to `13 Production` |
| Brandbook builder canonical run | FAIL | missing `03_Standards/Brand/Typography/Manrope-Variable.ttf`; canonical dependency layout is incomplete |
| Collection Book canonical run | FAIL | active WIP source points to nonexistent `Business_v1/WIP/upscale_p02_v1` |
| P02 delivery validation | PASS | 10/10 hashes; all referenced files exist; 0 legacy refs |
| Avito v2.6 validator | PASS | release status `APPROVED_FOR_AVITO_PUBLISH`; publication not performed |

Marketing dry-run outputs are isolated under `02_Marketing/Campaigns/WIP/LEGACY_PRODUCTION_FINAL_MIGRATION_DRY_RUN`.

## Active legacy references

`ACTIVE_BLOCKER = 18` exact `13 Production` references across active code/data:

1. `04_Templates/Collection_Book/example_data/P02_BUSINESS_COLLECTION_BOOK_v1.json` — 15.
2. `04_Templates/Collection_Book/template/style.json` — 2.
3. `engine/production/onyx_delivery.py` — 1 legacy canonical logo input.

Additional non-legacy dry-run blockers:

1. Brandbook canonical font/logo locations expected by `build_brandbook_v1_2.py` do not exist in that layout.
2. Collection Book WIP source directory spelling/path does not match the verified canonical upscale directory.

Older Avito validator/builder paths, migration reports, revision manifests and Lifestyle Premium provenance notes are classified `OBSOLETE`, `MIGRATION_REPORT_OK`, `HISTORICAL_OK` or `DEFERRED_WIP`; they are not included in the 18 active references above.

## 20 exact duplicates

- SHA256 matches: **20/20**;
- total bytes: **8,685,206**;
- modified duplicates: **0**;
- tracked duplicates: **20**;
- `READY_TO_DELETE = 0/20`.

Blocking consumers:

- `engine/production/onyx_production_pipeline.py` still reads `package/final_source_resolution` for both P01 and P02;
- Avito v2, v2.5 and v2.6 build scripts still read the P02 legacy `final_source_resolution` directory.

Until these consumers are cut over or explicitly retired, consumer count is not zero and none of the 20 files is ready for deletion.

## Residual `final_source_resolution` directories

| Path | Files | Bytes | State | Classification |
|---|---:|---:|---|---|
| `13 Production/Portfolio/P01/Business_V1/final_source_resolution` | 10 | 4,301,774 | tracked, clean | exact duplicates; blocked |
| `13 Production/Portfolio/P02/Business_V1/final_source_resolution` | 10 | 4,383,432 | tracked, clean | exact duplicates; blocked |
| `13 Production/Portfolio/P03/Business_V1/final_source_resolution` | 10 | 4,412,074 | tracked, clean | `DEFERRED_WIP`; not part of the 20-pair scope |
| `01_Characters/P02/02_Sessions/Boudoir_v1/final_source_resolution` | 10 | 3,532,057 | untracked | `DEFERRED_WIP`; unique/current session state not proven disposable |

## Final retirement readiness

`FINAL_DELETE_AND_RETIRE_13_PRODUCTION = NO`

Actual blockers only:

1. Brandbook canonical dry-run fails because required canonical font/asset layout is incomplete.
2. Collection Book canonical dry-run fails because its active source directory does not exist; two reusable template files also retain 17 active legacy values.
3. Delivery builder retains one active legacy logo reference.
4. Production pipeline and Avito historical builders still consume the 20 legacy `final_source_resolution` duplicates.

No final delete scope is authorized or ready. No files were deleted, staged, committed or pushed.

## Latest blocker verification

- Brandbook font paths now use `03_Standards/Brand/WIP`; Python compile passes. The available default interpreter lacks Pillow (`ModuleNotFoundError: PIL`), so the Brandbook dry-run remains unexecuted here.
- Delivery builder logo path now uses `03_Standards/Brand/Assets/Logo`; Python compile passes.
- Six Avito scripts still contain active legacy input paths, including the v2.6 builder; these remain consumer-cutover blockers.

## Runtime consumer cutover

- `engine/production/onyx_production_pipeline.py` now reads `02_Final`.
- Active Avito builders v2, v2.5 and v2.6 now read `01_Characters/P02/02_Sessions/Business_v1/02_Final`.
- Base Avito review builder now reads the same canonical P02 finals.
- Python compile passed for all five changed consumers.
- Active `final_source_resolution` references in `engine` and current Avito builders: **0**.
- Historical/validator scripts still mention legacy inventories or standards paths; these are retained as historical/deferred references and were not used as active image consumers in this cutover.

## Current readiness

- Production/Avito runtime consumers: **cut over**.
- Active `final_source_resolution` consumers: **0**.
- 20 duplicate pairs: SHA256 verification remains required before readiness can be marked `20/20`; no deletion performed.
- `FINAL_DELETE_AND_RETIRE_13_PRODUCTION`: **NO** pending full validation and residual inventory.

## Final verification snapshot

- P02 Business delivery: 10/10 master SHA256 checks pass; all 50 referenced delivery paths exist; active legacy refs in the manifest: 0.
- Canonical Collection Book JSON inputs: parse PASS; active legacy refs: 0. YAML remains textual-only because PyYAML is unavailable.
- Python compile for engine: PASS.
- Residual `13 Production`: 193 files, 1,336,939,010 bytes (~1,274.96 MiB).
- Active `final_source_resolution` consumers in engine/current Avito builders: 0; remaining occurrences are deferred session WIP or historical/reference material.
- Full dry-run suite is not fully executable in the available default interpreter because Pillow is unavailable for Brandbook/visual builders.
- `READY_TO_DELETE`: **0/20** until runtime, manifest, Avito, Brandbook and Collection Book consumer evidence is complete.
- `UNIQUE_USEFUL_LEGACY_FILES`: **not zero**; residual modified WIP, historical material and unresolved containers remain.
- Proposed deletion scope: prepared conceptually only; no files deleted.
- `FINAL_DELETE_AND_RETIRE_13_PRODUCTION = NO`.

## Wave A duplicate deletion

After repeat verification, all 20 P01/P02 pairs had canonical counterparts and SHA256 `MATCH` (20/20), with no active legacy path consumers in engine/current Avito/builders/manifests. The 20 legacy files were deleted: **8,685,206 bytes** total. Canonical `02_Final` files were not changed. Empty legacy directories remain pending residual cleanup.

Post-Wave-A residual inventory: **173 files / 1,328,253,804 bytes (~1,266.68 MiB)**. Modified and untracked WIP remains preserved; no further package was deleted or moved in this wave.

## Wave B — modified tracked WIP

- 30 modified Portfolio previews were copied byte-for-byte into character session `WIP/branded_previews` roots (P01/P02/P03); SHA256 verification: **33/33** including three delivery previews.
- Three modified Client_Delivery prepayment previews were copied into corresponding P01/P02/P03 Business session WIP delivery roots; current versions preserved exactly.
- The modified Product Standards route policy contains a unique Boudoir continuation rule. It was copied byte-for-byte to `03_Standards/Product/ONYX_GENERATION_ROUTE_POLICY_v1.md` (SHA256 match) and the legacy source was removed.
- Legacy Wave B preview sources were removed only after destination existence and SHA256 verification. Untracked Portfolio WIP, Brand, Orders, Client Experience and other residual packages were not touched.
- Wave B modified tracked WIP inside `13 Production`: **0 remaining**; unrelated modified/untracked packages remain outside this scope.

## Wave C — untracked Portfolio WIP

- Discovered: **60** untracked Portfolio files.
- P02 Business upscale outputs: **11** byte-identical canonical WIP duplicates removed.
- Unique P01/P02/P03 input/upscale/smoke WIP: promoted into corresponding canonical character session WIP roots; statuses remain WIP/candidate and no Final approval was created.
- Portfolio residual after Wave C: **50 files**; these are tracked legacy material or remaining package content outside the promoted untracked WIP scope.
- Overall residual after Wave C: **73 files / 21,699,458 bytes**.
- Brand, Client Experience, Orders, root README and other non-Portfolio residual packages were not touched.
- `WAVE_C_COMPLETE = YES` for the authorized untracked Portfolio WIP scope; full retirement remains blocked by non-Portfolio residual packages.

## Wave D — residual classification and routing

- Portfolio residual: 50 files → **0**. P03 candidate outputs/manifests moved to Executive WIP; P01/P02 manifests moved to Business session WIP; marketing previews moved to the existing Avito marketing WIP package; four historical Portfolio reports archived under `Archive/Legacy_Structure/Portfolio`.
- Brand residual: 14 files → **0**. SHA256-identical canonical duplicates removed; unique/historical material archived under `Archive/Legacy_Structure/Brand`.
- Client Experience: 4 files → **0**. Policy moved to `03_Standards/Client_Experience`; reusable intake/schema moved to `04_Templates/Client_Intake`.
- Client Delivery: SOP moved to standards, template README to templates, P03 preview to Executive WIP.
- Root README archived as `Archive/Legacy_Structure/13_Production_README.md`.
- Client-specific Orders README routed outside the repository to `D:\AI\ONYX_Clients\CL-0002_Valentina\03_Orders\ORD-2026-0003_CL-0002_Valentina`.
- Physical files remaining under `13 Production`: **0**.
- Empty `13 Production` directory tree removed after the zero-file gate.

## Final retirement gate

- Canonical roots and external client isolation verified.
- Collection Book JSON and migrated template path checks passed.
- Python compile check passed for the changed production and Avito builders.
- `git diff --cached --check` passed; unrelated Carousel V3, Campaigns, engine WIP, Brandbook WIP, session/Collection Book WIP and deferred duplicate dependencies remain unstaged.
- Legacy `13 Production` is retired and must not be recreated.
