# ONYX Commercial Freeze — final report, 2026-09-20

**Completed documentation/config phase:** ONYX_COMMERCIAL_PRODUCT_SYSTEM_v1 — CURRENT / FROZEN_FOR_SOFT_LAUNCH.
Operational readiness remains conditional; this is not a declaration that policy blockers or every product's production certification are complete.

## A. Pre-flight summary

- Working directory: `D:\AI\ONYX`.
- Branch: `main`.
- HEAD: `885ffba9ea099778e228a89a92c91f90398e0045` — unchanged.
- Initial working tree: 168 status entries, including user-owned code, intake/consent/brand edits and generated assets. No staging, commit or push.
- [Pre-flight inventory/conflict table](History/2026-09-20_commercial_freeze/PREFLIGHT.md).
- [Full initial git status](History/2026-09-20_commercial_freeze/initial_git_status.txt).

## B. Created files — 21

- [12 Decisions/ADR-0009 Commercial Product Freeze v1.md](<D:/AI/ONYX/12 Decisions/ADR-0009 Commercial Product Freeze v1.md>)
- [13 Production/Client_Experience/Intake/schemas/example_portrait.yaml](<D:/AI/ONYX/13 Production/Client_Experience/Intake/schemas/example_portrait.yaml>)
- [13 Production/Marketing/Avito/ONYX_AVITO_LAUNCH_REQUIREMENTS_v1.md](<D:/AI/ONYX/13 Production/Marketing/Avito/ONYX_AVITO_LAUNCH_REQUIREMENTS_v1.md>)
- [13 Production/Product_Standards/History/2026-09-20_commercial_freeze/PREFLIGHT.md](<D:/AI/ONYX/13 Production/Product_Standards/History/2026-09-20_commercial_freeze/PREFLIGHT.md>)
- [13 Production/Product_Standards/History/2026-09-20_commercial_freeze/baseline_text_sha256.json](<D:/AI/ONYX/13 Production/Product_Standards/History/2026-09-20_commercial_freeze/baseline_text_sha256.json>)
- [13 Production/Product_Standards/History/2026-09-20_commercial_freeze/consistency_scan.json](<D:/AI/ONYX/13 Production/Product_Standards/History/2026-09-20_commercial_freeze/consistency_scan.json>)
- [13 Production/Product_Standards/History/2026-09-20_commercial_freeze/final_git_diff_stat.txt](<D:/AI/ONYX/13 Production/Product_Standards/History/2026-09-20_commercial_freeze/final_git_diff_stat.txt>)
- [13 Production/Product_Standards/History/2026-09-20_commercial_freeze/final_git_status.txt](<D:/AI/ONYX/13 Production/Product_Standards/History/2026-09-20_commercial_freeze/final_git_status.txt>)
- [13 Production/Product_Standards/History/2026-09-20_commercial_freeze/initial_git_status.txt](<D:/AI/ONYX/13 Production/Product_Standards/History/2026-09-20_commercial_freeze/initial_git_status.txt>)
- [13 Production/Product_Standards/History/2026-09-20_commercial_freeze/superseded_documents.md](<D:/AI/ONYX/13 Production/Product_Standards/History/2026-09-20_commercial_freeze/superseded_documents.md>)
- [13 Production/Product_Standards/History/2026-09-20_commercial_freeze/task_files.json](<D:/AI/ONYX/13 Production/Product_Standards/History/2026-09-20_commercial_freeze/task_files.json>)
- [13 Production/Product_Standards/History/2026-09-20_commercial_freeze/task_only.diff](<D:/AI/ONYX/13 Production/Product_Standards/History/2026-09-20_commercial_freeze/task_only.diff>)
- [13 Production/Product_Standards/History/2026-09-20_commercial_freeze/validate_freeze.py](<D:/AI/ONYX/13 Production/Product_Standards/History/2026-09-20_commercial_freeze/validate_freeze.py>)
- [13 Production/Product_Standards/History/2026-09-20_commercial_freeze/validation_results.json](<D:/AI/ONYX/13 Production/Product_Standards/History/2026-09-20_commercial_freeze/validation_results.json>)
- [13 Production/Product_Standards/ONYX_COMMERCIAL_FREEZE_REPORT_2026-09-20.md](<D:/AI/ONYX/13 Production/Product_Standards/ONYX_COMMERCIAL_FREEZE_REPORT_2026-09-20.md>)
- [13 Production/Product_Standards/ONYX_COMMERCIAL_VERSION_HISTORY_v1.md](<D:/AI/ONYX/13 Production/Product_Standards/ONYX_COMMERCIAL_VERSION_HISTORY_v1.md>)
- [13 Production/Product_Standards/ONYX_CORRECTION_POLICY_v1.md](<D:/AI/ONYX/13 Production/Product_Standards/ONYX_CORRECTION_POLICY_v1.md>)
- [13 Production/Product_Standards/ONYX_HUMAN_QA_STANDARD_v1.md](<D:/AI/ONYX/13 Production/Product_Standards/ONYX_HUMAN_QA_STANDARD_v1.md>)
- [13 Production/Product_Standards/ONYX_LAUNCH_KPI_v1.md](<D:/AI/ONYX/13 Production/Product_Standards/ONYX_LAUNCH_KPI_v1.md>)
- [13 Production/Product_Standards/ONYX_LAUNCH_READINESS_CHECKLIST_v1.md](<D:/AI/ONYX/13 Production/Product_Standards/ONYX_LAUNCH_READINESS_CHECKLIST_v1.md>)
- [13 Production/Product_Standards/launch_kpi_v1.yaml](<D:/AI/ONYX/13 Production/Product_Standards/launch_kpi_v1.yaml>)

## C. Modified files — 27

These are task-touched files only. The full repository diff also contains unrelated pre-existing user work.

- [03 Product/Collections.md](<D:/AI/ONYX/03 Product/Collections.md>)
- [03 Product/Product.md](<D:/AI/ONYX/03 Product/Product.md>)
- [10 Roadmap/Roadmap.md](<D:/AI/ONYX/10 Roadmap/Roadmap.md>)
- [13 Production/Brand/CLIENT_PREVIEW_PROOF_STANDARD_V1.md](<D:/AI/ONYX/13 Production/Brand/CLIENT_PREVIEW_PROOF_STANDARD_V1.md>)
- [13 Production/Brand/Logo/EDITORIAL_WORDMARK_V1.md](<D:/AI/ONYX/13 Production/Brand/Logo/EDITORIAL_WORDMARK_V1.md>)
- [13 Production/Brand/ONYX_BRANDBOOK_CONTENT_V1.md](<D:/AI/ONYX/13 Production/Brand/ONYX_BRANDBOOK_CONTENT_V1.md>)
- [13 Production/Brand/ONYX_BRAND_SYSTEM.md](<D:/AI/ONYX/13 Production/Brand/ONYX_BRAND_SYSTEM.md>)
- [13 Production/Client_Delivery/ONYX_CLIENT_DELIVERY_SOP_V1.md](<D:/AI/ONYX/13 Production/Client_Delivery/ONYX_CLIENT_DELIVERY_SOP_V1.md>)
- [13 Production/Client_Delivery/Templates/README.md](<D:/AI/ONYX/13 Production/Client_Delivery/Templates/README.md>)
- [13 Production/Client_Experience/Intake/ONYX_PREMIUM_CREATIVE_PROFILE_v1.md](<D:/AI/ONYX/13 Production/Client_Experience/Intake/ONYX_PREMIUM_CREATIVE_PROFILE_v1.md>)
- [13 Production/Client_Experience/Intake/ONYX_REFERENCE_QA_STANDARD_v1.md](<D:/AI/ONYX/13 Production/Client_Experience/Intake/ONYX_REFERENCE_QA_STANDARD_v1.md>)
- [13 Production/Client_Experience/Intake/README.md](<D:/AI/ONYX/13 Production/Client_Experience/Intake/README.md>)
- [13 Production/Client_Experience/Intake/schemas/example_preview.yaml](<D:/AI/ONYX/13 Production/Client_Experience/Intake/schemas/example_preview.yaml>)
- [13 Production/Client_Experience/Intake/schemas/intake_v1.schema.yaml](<D:/AI/ONYX/13 Production/Client_Experience/Intake/schemas/intake_v1.schema.yaml>)
- [13 Production/Product_Standards/ONYX_COLLECTION_BOOK_STANDARD.md](<D:/AI/ONYX/13 Production/Product_Standards/ONYX_COLLECTION_BOOK_STANDARD.md>)
- [13 Production/Product_Standards/ONYX_COLLECTION_CATALOG.md](<D:/AI/ONYX/13 Production/Product_Standards/ONYX_COLLECTION_CATALOG.md>)
- [13 Production/Product_Standards/ONYX_MARKETING_STANDARD.md](<D:/AI/ONYX/13 Production/Product_Standards/ONYX_MARKETING_STANDARD.md>)
- [13 Production/Product_Standards/ONYX_PORTFOLIO_STANDARD.md](<D:/AI/ONYX/13 Production/Product_Standards/ONYX_PORTFOLIO_STANDARD.md>)
- [13 Production/Product_Standards/ONYX_PREPAYMENT_PREVIEW_STANDARD.md](<D:/AI/ONYX/13 Production/Product_Standards/ONYX_PREPAYMENT_PREVIEW_STANDARD.md>)
- [13 Production/Product_Standards/ONYX_PRICE_BOOK_v1.md](<D:/AI/ONYX/13 Production/Product_Standards/ONYX_PRICE_BOOK_v1.md>)
- [13 Production/Product_Standards/ONYX_PRODUCT_SYSTEM.md](<D:/AI/ONYX/13 Production/Product_Standards/ONYX_PRODUCT_SYSTEM.md>)
- [13 Production/Product_Standards/ONYX_SERVICE_STANDARD_v1.md](<D:/AI/ONYX/13 Production/Product_Standards/ONYX_SERVICE_STANDARD_v1.md>)
- [13 Production/Product_Standards/products_v1.yaml](<D:/AI/ONYX/13 Production/Product_Standards/products_v1.yaml>)
- [13 Production/README.md](<D:/AI/ONYX/13 Production/README.md>)
- [13 Production/Templates/Collection_Book/COLLECTION_BOOK_PRODUCTION_GUIDE.md](<D:/AI/ONYX/13 Production/Templates/Collection_Book/COLLECTION_BOOK_PRODUCTION_GUIDE.md>)
- [13 Production/Templates/Collection_Book/ONYX_COLLECTION_BOOK_TEMPLATE.md](<D:/AI/ONYX/13 Production/Templates/Collection_Book/ONYX_COLLECTION_BOOK_TEMPLATE.md>)
- [13 Production/Templates/Collection_Book/README.md](<D:/AI/ONYX/13 Production/Templates/Collection_Book/README.md>)

## D. Superseded values

| Old value| New value | Document | Reason |
|---|---|---|---|
| Preview 900 RUB, personal test frame | Portrait 1000 RUB, complete standalone service | Product System / Price Book / YAML / intake | Explicit frozen commercial request |
| Preview → Signature 2100; Preview → Premium 4100 | Portrait → Signature +2000; Signature → Premium +2000, 7 calendar days | Product System / Price Book / YAML | New upgrade ladder; legacy orders retain agreed terms |
| Premium 4–5 looks; unclear Collection limit | Usually 4–6 Concepts, one main Collection | Product System / YAML / Premium profile | Creative depth without bundling full Collections |
| Premium Motion and specialized social exports included | Future separate scope, not frozen mandatory deliverables | Product System / YAML / Book Standard | Align frozen deliverable list; no new Motion production |
| Payment before intake/QA; payment model TBD | 100% prepayment after QA/feasibility/capacity | Service / Price Book / delivery / proof docs | Requested soft-launch payment order |
| Broad outfit/scene correction language | Free QA defects versus bounded subjective rounds and scope add-ons | Service / Correction Policy | Prevent charging for defects or unlimited creative resets |
| Preview Book technical support presented in delivery model | Portrait no Book; renderer legacy support retained | Book Standard / renderer docs | Separate implementation capability from entitlement |
| Universal ten-image delivery wording | 1/10/20 plus extras; existing automated builder stays Signature-specific | Delivery / Portfolio standards | Preserve runtime while making purchased scope correct |
| Product → Collection → Scenes; Essential/Executive/etc. as tiers | Collection → Concept → Scene → Final Image; three commercial tiers | 03 Product (marked SUPERSEDED) / Product System | Preserve historical vocabulary without competing authority |
| Signature-only marketing carousel entry | Portrait entry, Signature recommended, Premium extended | Marketing / Avito requirements | Public headline starts at 1000 RUB |
| No prices for scope extras/urgency | Final 500, Concept 1000, round 700, Repair from 500/1000; Priority +50%, Express +100% | Product System / Price Book / YAML | Explicit commercial freeze |
| No global SLA, no approved retention period | Standard deadline per order; conditional urgent targets; retention unresolved | Service / readiness | No invented universal SLA/privacy duration |
| Intake YAML description contained an unquoted colon | Same text quoted as a YAML string | intake_v1.schema.yaml | Restore actual YAML parseability; preserve all existing fields and consent values |

Complete pre-task working-tree texts are retained in the historical snapshot; pre-existing edits in the touched files were not replaced with HEAD versions. Existing consent/privacy, generation route, runtime code, orders, images and experiment history were not edited by this task.

## E. Final product matrix

| Product / stable ID | Price, RUB | Final images | Collection scope | Concepts | Client correction rounds | Collection Book |
|---|---:|---:|---|---|---:|---|
| ONYX Portrait / ONYX_PORTRAIT_V1 | 1000 | 1 | Single agreed direction | 1 | 0 | No |
| ONYX Signature / ONYX_SIGNATURE_V1 | 3000 | 10 | 1 main Collection | Usually 2–3 | 1 | Standard PDF |
| ONYX Premium / ONYX_PREMIUM_V1 | 5000 | 20 | 1 main Collection | Usually 4–6 | 2 | Extended PDF |

## F. Add-on matrix

| Service / stable ID | Price, RUB | Applies to | Boundary |
|---|---:|---|---|
| Additional Final Image / ADD_FINAL_IMAGE | 500 | 1 extra accepted final within agreed Collection/Concept or close Scene direction | Extra angle/pose/portrait in existing look; substantial new wardrobe, location, style or Concept is separately scoped |
| Additional Concept / Look / ADD_CONCEPT | 1000 | New creative idea/look/location type within existing or compatible Collection architecture | Not automatically a separate Collection; final count stays the ordered count unless extra finals are purchased |
| Additional Correction Round / ADD_CORRECTION_ROUND | 700 | One subjective round after included rounds are used; Portrait has zero included | No new session, full creative reset, new Collection or unlimited regeneration |
| ONYX Repair / ONYX_REPAIR | from 500 simple; from 1000 complex | External image or new scope outside ONYX obligations | Price and feasibility only after inspection; no guarantee of technically impossible repair |
| ONYX Priority / ONYX_PRIORITY | +50% | Confirmed capacity; target within 24 hours | Queue change only; unchanged identity and QA standard |
| ONYX Express / ONYX_EXPRESS | +100% | Explicitly confirmed capacity; same-day target | Not always available; unchanged identity and QA standard |

Additional Collection remains PLANNED / price TBD, not included automatically in Premium. Additional Concept buys scope, not an unspecified number of extra finals. Urgency is quoted against the production subtotal and does not reduce QA.

## G. Upgrade matrix

| Upgrade | Window | Credited base payment, RUB | Additional base payment, RUB | Target total, RUB |
|---|---|---:|---:|---:|
| Portrait → Signature | 7 calendar days | 1000 | 2000 | 3000 |
| Signature → Premium | 7 calendar days | 3000 | 2000 | 5000 |

Window starts at source delivery. Context/references/consent/metadata must remain lawfully available; Signature → Premium continues the original Collection. Target final counts and rounds are cumulative, no double charging. Upgrade eligibility does not establish a retention period.

## H. Commercial source of truth

[D:/AI/ONYX/13 Production/Product_Standards/ONYX_PRODUCT_SYSTEM.md](<D:/AI/ONYX/13 Production/Product_Standards/ONYX_PRODUCT_SYSTEM.md>)

Logical ID: `ONYX_COMMERCIAL_PRODUCT_SYSTEM_v1`; status `CURRENT` / `FROZEN_FOR_SOFT_LAUNCH`; freeze date `2026-09-20`. The existing path remains authoritative; no second commercial authority was created.

## I. Machine-readable source of truth

[D:/AI/ONYX/13 Production/Product_Standards/products_v1.yaml](<D:/AI/ONYX/13 Production/Product_Standards/products_v1.yaml>)

Stable IDs, product/add-on prices, scope, final counts, rounds, Books, recommended Concept ranges, urgent conditions, upgrade rules, reference/payment/privacy gates and freeze review are documented. `saleable_product_keys` excludes legacy Preview. No executable consumer was found; no external consumer compatibility is claimed. Runtime manifests are not migrated; additive taxonomy fields are documented guidance only.

## J. Launch readiness matrix

| Block| Status | Readiness % | Blocker / Non-blocker | Existing evidence | Owner / missing next action |
|---|---|---:|---|---|---|
| Product System | READY | 100 | Non-blocker | ONYX_PRODUCT_SYSTEM.md | Frozen authority and change control recorded |
| Portrait | DEFINED / UNMEASURED | 80 | Non-blocker; per-order gate | Product System; existing portrait workflow | Measure first-order effort; confirm one-image manual delivery |
| Signature | EVIDENCED | 95 | Non-blocker; per-order gate | ORD-2026-0002 human review PASS; existing delivery/Book artifacts | Check current order acceptance and clean package; samples do not prove paid sales |
| Premium | DEFINED / PARTIAL EVIDENCE | 70 | Non-blocker for limited soft launch; gate Premium acceptance | Creative Profile; renderer planner supports 20 | Confirm operator capacity and Extended Book visual QA before accepting Premium promise |
| Add-ons | DEFINED | 100 | Non-blocker | Product System / YAML | Quote exact scope and extra final count |
| Repair | CONDITIONAL | 85 | Non-blocker; per-image gate | Pricing/feasibility rules | Inspect image and quote; do not guarantee repair |
| Upgrade rules | READY / CONDITIONAL | 100 | Non-blocker; depends on privacy | Product System / Service Standard | Verify available context, consent and credit ledger |
| Price Book | READY | 100 | Non-blocker | Price Book / YAML | Use frozen quote values |
| Client Intake | READY / POLICY GATED | 90 | Non-blocker itself | Intake schema 1.3 and Portrait example | Use PORTRAIT for new orders; privacy gate first |
| Reference Guide | READY | 100 | Non-blocker | Existing quality-based Guide / Reference QA | No hard 4–8 limit; QA before payment |
| Consent | DOCUMENTED | 95 | Non-blocker itself | Existing Consent & Privacy | Capture per-order/reuse and separate publication choices |
| Privacy | BLOCKED | 50 | TRUE BLOCKER before new client data | Consent has no duration; Service Standard previously owner-decision | Owner approves retention duration and actionable deletion procedure |
| Payment | PARTIAL | 75 | TRUE BLOCKER before accepting payment | 100% prepayment after QA now defined; payment channel absent from inspected standards | Owner confirms working payment/refund channel and client terms |
| Refund | PARTIAL | 60 | TRUE BLOCKER before accepting payment | Resolution principles defined; prior framework had no final terms | Owner confirms cancellation/partial refund rules and processing timing |
| Human QA | READY | 95 | Non-blocker; per-output gate | New Human QA Standard + existing order human PASS | Record acceptance of exact current files |
| Corrections | READY | 100 | Non-blocker | Correction Policy | Log defects separately from subjective rounds |
| Collection Book | SIGNATURE EVIDENCED / PREMIUM CONDITIONAL | 80 | Non-blocker for Portrait/Signature; Premium gate | Signature PDFs/reviews; 20-image planner only | Visual QA of each Extended Book; no new Book in this task |
| Delivery | SIGNATURE EVIDENCED / MANUAL OTHER TIERS | 80 | Non-blocker; per-order gate | Existing ten-frame SOP and delivery artifacts | Manually verify 1/20 plus extras, clean files and access |
| Portfolio | AVAILABLE / RIGHTS GATED | 85 | Non-blocker; per-asset gate | Portfolio Standard and synthetic character packages | Verify exact asset approval and publication permission |
| Marketing | REQUIREMENTS READY | 85 | Non-blocker | Marketing Standard | Export current offer only in next Launch Pack |
| Avito | PACK NOT CREATED | 40 | Channel publication gate; not general soft-launch blocker | Requirements; folder previously only .gitkeep | Owner/operator creates and approves Avito Launch Pack v1 |
| Client communication | DOCUMENTED / TEMPLATES PENDING | 80 | Non-blocker | Public copy, Service/Correction rules | Use consultation checklist; create channel responses with Launch Pack |
| KPI tracking | MANUAL READY | 90 | Non-blocker | KPI framework / schema | Operator logs each lead/order; no automation claim |
| Post-delivery feedback | MANUAL READY | 85 | Non-blocker | Service Standard / KPI fields | Ask satisfaction/defects and record resolution |

Readiness percentages are checklist estimates, not empirical delivery probabilities. Signature has existing human PASS/Book/delivery evidence; Portrait economics and Premium/extra-final Book packaging need order-specific confirmation. Renderer tests prove planning/privacy checks only, not visual certification.

## K. True blockers

1. **Privacy lifecycle:** no approved storage duration or actionable deletion procedure in current policy. Owner must define and communicate these before accepting new client materials. Existing consent language is preserved; no arbitrary retention period added.
2. **Payment/refund execution and terms:** prepayment timing is frozen, but inspected standards do not establish a working payment/refund channel, cancellation/partial-refund rules or processing timing. Owner must confirm them before collecting money. Failed production cannot be marked successfully fulfilled.

No image generation, legal-policy invention or new external account setup is required in this documentation task. This report records missing evidence rather than asserting that a payment channel cannot exist outside the repository.

Premium capacity/Extended Book and urgent capacity are product-specific acceptance gates, not reasons to postpone a limited Portrait/Signature launch once shared blockers are closed. Avito Pack approval gates Avito publication only. Do not advertise unconditional Premium/urgent availability before confirming capacity.

The Book renderer supports exactly 1/10/20 images; extra-final orders need a separately prepared/checked layout. This is an add-on packaging gate, not a claim of existing arbitrary-count automation.

Full Imagegen/OpenAI API automation, FLUX improvements, PuLID, LoRA, physical books, website, ONYX Private, perfect CRM and full automation are **not launch blockers**.

## L. Recommended next action

Owner resolves retention/deletion and payment/refund operating terms in one launch-policy review. Then prepare **ONYX Avito Launch Pack v1**. No final Avito Pack, image generation, new Book, upload or publication was performed here.

## Verification and scope limits

- 32 documentation/config checks PASS: eight YAML files parsed with duplicate-key rejection; product/add-on table parity; unique IDs; upgrade arithmetic; freeze metadata; new links; snapshot integrity; preserved intake fields/consent values; unchanged HEAD; every initial status entry retained; whitespace check.
- Three existing Collection Book renderer tests PASS (1/10/20 planning and privacy vocabulary). No PDF generated.
- Fixed one pre-existing intake YAML parse error by quoting a description containing a colon; no semantic change to that field.
- Kept mature quality-based reference sufficiency; 4–8 is guidance, not a hard limit.
- Existing Book renderer rejects arbitrary counts such as 11/21; additional-final orders need separate layout preparation/QA. Runtime code was not changed.
- Global production text scan performed for all requested terms. [Scan/classification](History/2026-09-20_commercial_freeze/consistency_scan.json). Remaining 900/Preview entries are historical, non-saleable legacy config or proof/renderer terminology; negative trial/multi-Collection statements are explicit exclusions.
- [Machine-readable verification results](History/2026-09-20_commercial_freeze/validation_results.json); [re-runnable audit script](History/2026-09-20_commercial_freeze/validate_freeze.py); [task-only text diff against initial working tree](History/2026-09-20_commercial_freeze/task_only.diff).
- Validation used existing local Python/PyYAML and the bundled Book dependencies. No installation, dependency upgrade, ComfyUI process, GPU job or external call was needed.

## M. Git state

Full `git diff --stat` includes pre-existing image/code/user edits and excludes untracked new files. Use sections B/C and the task-only diff to isolate this task.

```text
 03 Product/Collections.md                          |   8 +-
 03 Product/Product.md                              |   8 +-
 10 Roadmap/Roadmap.md                              |   7 +
 .../Brand/CLIENT_PREVIEW_PROOF_STANDARD_V1.md      |   4 +
 13 Production/Brand/Logo/EDITORIAL_WORDMARK_V1.md  |   8 +
 13 Production/Brand/ONYX_BRANDBOOK_CONTENT_V1.md   |  10 +-
 13 Production/Brand/ONYX_BRAND_SYSTEM.md           |  14 +
 .../ONYX_P01_BUSINESS_PREPAYMENT_PREVIEW.jpg       | Bin 276514 -> 126239 bytes
 .../ONYX_P02_BUSINESS_PREPAYMENT_PREVIEW.jpg       | Bin 294057 -> 133764 bytes
 .../ONYX_P03_BUSINESS_PREPAYMENT_PREVIEW.jpg       | Bin 289525 -> 135437 bytes
 .../Client_Delivery/ONYX_CLIENT_DELIVERY_SOP_V1.md |   7 +-
 13 Production/Client_Delivery/Templates/README.md  |   2 +-
 .../Intake/ONYX_CONSENT_AND_PRIVACY_v1.md          |  11 +
 .../Intake/ONYX_PREMIUM_CREATIVE_PROFILE_v1.md     |   4 +
 .../Intake/ONYX_REFERENCE_QA_STANDARD_v1.md        |   4 +-
 .../Intake/ONYX_SIGNATURE_INTAKE_v1.md             |   2 +
 13 Production/Client_Experience/Intake/README.md   |  17 +-
 .../Intake/schemas/example_preview.yaml            |   1 +
 .../Intake/schemas/intake_v1.schema.yaml           | 143 ++++++++-
 .../08_collection_book/.gitkeep                    |   1 -
 .../ONYX_P01_BUSINESS_01_HERO.jpg                  | Bin 285171 -> 249458 bytes
 .../ONYX_P01_BUSINESS_02_CLOSE.jpg                 | Bin 293451 -> 257169 bytes
 .../ONYX_P01_BUSINESS_03_WAIST.jpg                 | Bin 274622 -> 239157 bytes
 .../ONYX_P01_BUSINESS_04_SEATED.jpg                | Bin 273199 -> 237697 bytes
 .../ONYX_P01_BUSINESS_05_ENVIRONMENT.jpg           | Bin 302462 -> 264954 bytes
 .../ONYX_P01_BUSINESS_06_ACTION.jpg                | Bin 260221 -> 228323 bytes
 .../ONYX_P01_BUSINESS_07_3Q_BODY.jpg               | Bin 266432 -> 233467 bytes
 .../ONYX_P01_BUSINESS_08_FULL_BODY.jpg             | Bin 263484 -> 232219 bytes
 .../ONYX_P01_BUSINESS_09_MOOD.jpg                  | Bin 293686 -> 255947 bytes
 .../ONYX_P01_BUSINESS_10_EDITORIAL.jpg             | Bin 284800 -> 249139 bytes
 .../ONYX_P02_BUSINESS_01_HERO.jpg                  | Bin 304996 -> 266288 bytes
 .../ONYX_P02_BUSINESS_02_CLOSE.jpg                 | Bin 265801 -> 232496 bytes
 .../ONYX_P02_BUSINESS_03_WAIST.jpg                 | Bin 309233 -> 270689 bytes
 .../ONYX_P02_BUSINESS_04_SEATED.jpg                | Bin 332007 -> 290532 bytes
 .../ONYX_P02_BUSINESS_05_ENVIRONMENT.jpg           | Bin 263828 -> 230408 bytes
 .../ONYX_P02_BUSINESS_06_ACTION.jpg                | Bin 299472 -> 262716 bytes
 .../ONYX_P02_BUSINESS_07_3Q_BODY.jpg               | Bin 272901 -> 237926 bytes
 .../ONYX_P02_BUSINESS_08_FULL_BODY.jpg             | Bin 311533 -> 273940 bytes
 .../ONYX_P02_BUSINESS_09_MOOD.jpg                  | Bin 281917 -> 246873 bytes
 .../ONYX_P02_BUSINESS_10_EDITORIAL.jpg             | Bin 290822 -> 255921 bytes
 .../ONYX_P03_BUSINESS_01_HERO.jpg                  | Bin 299585 -> 263751 bytes
 .../ONYX_P03_BUSINESS_02_CLOSE.jpg                 | Bin 292106 -> 256075 bytes
 .../ONYX_P03_BUSINESS_03_WAIST.jpg                 | Bin 307214 -> 269399 bytes
 .../ONYX_P03_BUSINESS_04_SEATED.jpg                | Bin 341052 -> 298724 bytes
 .../ONYX_P03_BUSINESS_05_ENVIRONMENT.jpg           | Bin 271484 -> 237776 bytes
 .../ONYX_P03_BUSINESS_06_ACTION.jpg                | Bin 277760 -> 244531 bytes
 .../ONYX_P03_BUSINESS_07_3Q_BODY.jpg               | Bin 290997 -> 255154 bytes
 .../ONYX_P03_BUSINESS_08_FULL_BODY.jpg             | Bin 296526 -> 261090 bytes
 .../ONYX_P03_BUSINESS_09_MOOD.jpg                  | Bin 308072 -> 270072 bytes
 .../ONYX_P03_BUSINESS_10_EDITORIAL.jpg             | Bin 271980 -> 238574 bytes
 .../ONYX_COLLECTION_BOOK_STANDARD.md               |  10 +-
 .../Product_Standards/ONYX_COLLECTION_CATALOG.md   |   2 +-
 .../ONYX_GENERATION_ROUTE_POLICY_v1.md             |  19 ++
 .../Product_Standards/ONYX_MARKETING_STANDARD.md   |  17 +-
 .../Product_Standards/ONYX_PORTFOLIO_STANDARD.md   |   6 +-
 .../ONYX_PREPAYMENT_PREVIEW_STANDARD.md            |   3 +-
 .../Product_Standards/ONYX_PRICE_BOOK_v1.md        |  62 ++--
 .../Product_Standards/ONYX_PRODUCT_SYSTEM.md       | 161 +++++-----
 .../Product_Standards/ONYX_SERVICE_STANDARD_v1.md  | 107 +++----
 13 Production/Product_Standards/products_v1.yaml   | 325 ++++++++++++++++++---
 13 Production/README.md                            |  10 +
 .../COLLECTION_BOOK_PRODUCTION_GUIDE.md            |   4 +
 .../ONYX_COLLECTION_BOOK_TEMPLATE.md               |   4 +
 13 Production/Templates/Collection_Book/README.md  |   4 +
 engine/production/onyx_delivery.py                 |   7 +-
 65 files changed, 722 insertions(+), 270 deletions(-)
```

Full `git status --short`:

```text
 M "03 Product/Collections.md"
 M "03 Product/Product.md"
 M "10 Roadmap/Roadmap.md"
 M "13 Production/Brand/CLIENT_PREVIEW_PROOF_STANDARD_V1.md"
 M "13 Production/Brand/Logo/EDITORIAL_WORDMARK_V1.md"
 M "13 Production/Brand/ONYX_BRANDBOOK_CONTENT_V1.md"
 M "13 Production/Brand/ONYX_BRAND_SYSTEM.md"
 M "13 Production/Client_Delivery/Examples/Prepayment/ONYX_P01_BUSINESS_PREPAYMENT_PREVIEW.jpg"
 M "13 Production/Client_Delivery/Examples/Prepayment/ONYX_P02_BUSINESS_PREPAYMENT_PREVIEW.jpg"
 M "13 Production/Client_Delivery/Examples/Prepayment/ONYX_P03_BUSINESS_PREPAYMENT_PREVIEW.jpg"
 M "13 Production/Client_Delivery/ONYX_CLIENT_DELIVERY_SOP_V1.md"
 M "13 Production/Client_Delivery/Templates/README.md"
 M "13 Production/Client_Experience/Intake/ONYX_CONSENT_AND_PRIVACY_v1.md"
 M "13 Production/Client_Experience/Intake/ONYX_PREMIUM_CREATIVE_PROFILE_v1.md"
 M "13 Production/Client_Experience/Intake/ONYX_REFERENCE_QA_STANDARD_v1.md"
 M "13 Production/Client_Experience/Intake/ONYX_SIGNATURE_INTAKE_v1.md"
 M "13 Production/Client_Experience/Intake/README.md"
 M "13 Production/Client_Experience/Intake/schemas/example_preview.yaml"
 M "13 Production/Client_Experience/Intake/schemas/intake_v1.schema.yaml"
 D "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/08_collection_book/.gitkeep"
 M "13 Production/Portfolio/P01/Business_V1/portfolio_framed_preview/ONYX_P01_BUSINESS_01_HERO.jpg"
 M "13 Production/Portfolio/P01/Business_V1/portfolio_framed_preview/ONYX_P01_BUSINESS_02_CLOSE.jpg"
 M "13 Production/Portfolio/P01/Business_V1/portfolio_framed_preview/ONYX_P01_BUSINESS_03_WAIST.jpg"
 M "13 Production/Portfolio/P01/Business_V1/portfolio_framed_preview/ONYX_P01_BUSINESS_04_SEATED.jpg"
 M "13 Production/Portfolio/P01/Business_V1/portfolio_framed_preview/ONYX_P01_BUSINESS_05_ENVIRONMENT.jpg"
 M "13 Production/Portfolio/P01/Business_V1/portfolio_framed_preview/ONYX_P01_BUSINESS_06_ACTION.jpg"
 M "13 Production/Portfolio/P01/Business_V1/portfolio_framed_preview/ONYX_P01_BUSINESS_07_3Q_BODY.jpg"
 M "13 Production/Portfolio/P01/Business_V1/portfolio_framed_preview/ONYX_P01_BUSINESS_08_FULL_BODY.jpg"
 M "13 Production/Portfolio/P01/Business_V1/portfolio_framed_preview/ONYX_P01_BUSINESS_09_MOOD.jpg"
 M "13 Production/Portfolio/P01/Business_V1/portfolio_framed_preview/ONYX_P01_BUSINESS_10_EDITORIAL.jpg"
 M "13 Production/Portfolio/P02/Business_V1/portfolio_framed_preview/ONYX_P02_BUSINESS_01_HERO.jpg"
 M "13 Production/Portfolio/P02/Business_V1/portfolio_framed_preview/ONYX_P02_BUSINESS_02_CLOSE.jpg"
 M "13 Production/Portfolio/P02/Business_V1/portfolio_framed_preview/ONYX_P02_BUSINESS_03_WAIST.jpg"
 M "13 Production/Portfolio/P02/Business_V1/portfolio_framed_preview/ONYX_P02_BUSINESS_04_SEATED.jpg"
 M "13 Production/Portfolio/P02/Business_V1/portfolio_framed_preview/ONYX_P02_BUSINESS_05_ENVIRONMENT.jpg"
 M "13 Production/Portfolio/P02/Business_V1/portfolio_framed_preview/ONYX_P02_BUSINESS_06_ACTION.jpg"
 M "13 Production/Portfolio/P02/Business_V1/portfolio_framed_preview/ONYX_P02_BUSINESS_07_3Q_BODY.jpg"
 M "13 Production/Portfolio/P02/Business_V1/portfolio_framed_preview/ONYX_P02_BUSINESS_08_FULL_BODY.jpg"
 M "13 Production/Portfolio/P02/Business_V1/portfolio_framed_preview/ONYX_P02_BUSINESS_09_MOOD.jpg"
 M "13 Production/Portfolio/P02/Business_V1/portfolio_framed_preview/ONYX_P02_BUSINESS_10_EDITORIAL.jpg"
 M "13 Production/Portfolio/P03/Business_V1/portfolio_framed_preview/ONYX_P03_BUSINESS_01_HERO.jpg"
 M "13 Production/Portfolio/P03/Business_V1/portfolio_framed_preview/ONYX_P03_BUSINESS_02_CLOSE.jpg"
 M "13 Production/Portfolio/P03/Business_V1/portfolio_framed_preview/ONYX_P03_BUSINESS_03_WAIST.jpg"
 M "13 Production/Portfolio/P03/Business_V1/portfolio_framed_preview/ONYX_P03_BUSINESS_04_SEATED.jpg"
 M "13 Production/Portfolio/P03/Business_V1/portfolio_framed_preview/ONYX_P03_BUSINESS_05_ENVIRONMENT.jpg"
 M "13 Production/Portfolio/P03/Business_V1/portfolio_framed_preview/ONYX_P03_BUSINESS_06_ACTION.jpg"
 M "13 Production/Portfolio/P03/Business_V1/portfolio_framed_preview/ONYX_P03_BUSINESS_07_3Q_BODY.jpg"
 M "13 Production/Portfolio/P03/Business_V1/portfolio_framed_preview/ONYX_P03_BUSINESS_08_FULL_BODY.jpg"
 M "13 Production/Portfolio/P03/Business_V1/portfolio_framed_preview/ONYX_P03_BUSINESS_09_MOOD.jpg"
 M "13 Production/Portfolio/P03/Business_V1/portfolio_framed_preview/ONYX_P03_BUSINESS_10_EDITORIAL.jpg"
 M "13 Production/Product_Standards/ONYX_COLLECTION_BOOK_STANDARD.md"
 M "13 Production/Product_Standards/ONYX_COLLECTION_CATALOG.md"
 M "13 Production/Product_Standards/ONYX_GENERATION_ROUTE_POLICY_v1.md"
 M "13 Production/Product_Standards/ONYX_MARKETING_STANDARD.md"
 M "13 Production/Product_Standards/ONYX_PORTFOLIO_STANDARD.md"
 M "13 Production/Product_Standards/ONYX_PREPAYMENT_PREVIEW_STANDARD.md"
 M "13 Production/Product_Standards/ONYX_PRICE_BOOK_v1.md"
 M "13 Production/Product_Standards/ONYX_PRODUCT_SYSTEM.md"
 M "13 Production/Product_Standards/ONYX_SERVICE_STANDARD_v1.md"
 M "13 Production/Product_Standards/products_v1.yaml"
 M "13 Production/README.md"
 M "13 Production/Templates/Collection_Book/COLLECTION_BOOK_PRODUCTION_GUIDE.md"
 M "13 Production/Templates/Collection_Book/ONYX_COLLECTION_BOOK_TEMPLATE.md"
 M "13 Production/Templates/Collection_Book/README.md"
 M engine/production/onyx_delivery.py
?? "12 Decisions/ADR-0009 Commercial Product Freeze v1.md"
?? "13 Production/Brand/ONYX_BRANDBOOK_V1_2.pdf"
?? "13 Production/Brand/Review/"
?? "13 Production/Brand/Typography/Manrope-OFL.txt"
?? "13 Production/Brand/Typography/Manrope-Variable.ttf"
?? "13 Production/Brand/build_brandbook_v1_2.py"
?? "13 Production/Client_Experience/Intake/ONYX_BOUDOIR_SIGNATURE_INTAKE_v1.md"
?? "13 Production/Client_Experience/Intake/schemas/example_portrait.yaml"
?? "13 Production/Client_Experience/Intake/schemas/example_signature_boudoir.yaml"
?? "13 Production/Marketing/Avito/ONYX_AVITO_LAUNCH_REQUIREMENTS_v1.md"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/01_references/REF_01.jpg"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/01_references/REF_02.jpg"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/01_references/REF_03.jpg"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/01_references/REF_04.jpg"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/01_references/REF_05.jpg"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/01_references/REF_06.jpg"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/05_candidates/BUSINESS_01/"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/05_candidates/BUSINESS_02/"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/05_candidates/BUSINESS_03/"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/05_candidates/BUSINESS_04/"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/05_candidates/BUSINESS_05/"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/05_candidates/BUSINESS_06/"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/05_candidates/BUSINESS_07/"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/05_candidates/BUSINESS_08/"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/05_candidates/BUSINESS_09/"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/05_candidates/BUSINESS_10/"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/06_qa/BUSINESS_01/.gitkeep"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/06_qa/BUSINESS_02/.gitkeep"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/06_qa/BUSINESS_03/.gitkeep"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/06_qa/BUSINESS_04/.gitkeep"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/06_qa/BUSINESS_05/.gitkeep"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/06_qa/BUSINESS_06/.gitkeep"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/06_qa/BUSINESS_07/.gitkeep"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/06_qa/BUSINESS_08/.gitkeep"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/06_qa/BUSINESS_09/.gitkeep"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/06_qa/BUSINESS_10/.gitkeep"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/06_qa/human_review/contact_sheet.jpg"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/07_final/ONYX_BUSINESS_01.png"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/07_final/ONYX_BUSINESS_02.png"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/07_final/ONYX_BUSINESS_03.png"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/07_final/ONYX_BUSINESS_04.png"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/07_final/ONYX_BUSINESS_05.png"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/07_final/ONYX_BUSINESS_06.png"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/07_final/ONYX_BUSINESS_07.png"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/07_final/ONYX_BUSINESS_08.png"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/07_final/ONYX_BUSINESS_09.png"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/07_final/ONYX_BUSINESS_10.png"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/07_final/superseded/"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/08_collection_book/ORD-2026-0001_ALEXANDER_BUSINESS_COLLECTION_BOOK_v1.pdf"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/08_collection_book/ORD-2026-0001_ALEXANDER_BUSINESS_COLLECTION_BOOK_v1_manifest.yaml"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/08_collection_book/ORD-2026-0001_ALEXANDER_BUSINESS_COLLECTION_BOOK_v2.pdf"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/08_collection_book/QA.md"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/08_collection_book/preview/"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/08_collection_book/preview_v2/"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/08_collection_book/source_data.json"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/09_delivery/ONYX_Alexander_Business.zip"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/09_delivery/ONYX_Alexander_Business/"
?? "13 Production/Orders/ORD-2026-0001_CL-0001_Alexander/09_delivery/delivery_manifest.json"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/00_intake/"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/01_references/"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/02_reference_qa/"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/03_scene_plan/"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/04_production/BODY_TYPE_GUIDANCE.md"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/04_production/FEMALE_BUSINESS_STYLING_GUIDANCE.md"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/04_production/prompts/"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/04_production/replacement_prompts/"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/05_candidates/"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/06_qa/BUSINESS_01/"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/06_qa/BUSINESS_02/"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/06_qa/BUSINESS_03/"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/06_qa/BUSINESS_04/"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/06_qa/BUSINESS_05/"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/06_qa/BUSINESS_06/"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/06_qa/BUSINESS_07/"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/06_qa/BUSINESS_08/"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/06_qa/BUSINESS_09/"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/06_qa/BUSINESS_10/"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/06_qa/BUSINESS_11/"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/06_qa/BUSINESS_12/"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/06_qa/REPL_A_BODYTYPE_qa.yaml"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/06_qa/REPL_B_PROFILE_qa.yaml"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/06_qa/REPL_C_FORMAL_qa.yaml"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/06_qa/REPL_D_WARM_qa.yaml"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/06_qa/REPL_E_MANICURE_DESK_qa.yaml"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/06_qa/REPL_F_FORMAL_WATCH_qa.yaml"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/06_qa/REPL_G_WARM_MANICURE_qa.yaml"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/06_qa/candidate_contact_sheet.jpg"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/06_qa/human_review/contact_sheet.jpg"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/06_qa/human_review/contact_sheet_before_manicure_watch_round.jpg"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/06_qa/replacement_round_2_summary.yaml"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/07_final/"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/08_collection_book/ORD-2026-0002_VALENTINA_BUSINESS_COLLECTION_BOOK_v1.pdf"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/08_collection_book/ORD-2026-0002_VALENTINA_BUSINESS_COLLECTION_BOOK_v1_manifest.yaml"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/08_collection_book/ORD-2026-0002_VALENTINA_BUSINESS_COLLECTION_BOOK_v2.pdf"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/08_collection_book/QA_v1.md"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/08_collection_book/preview_v1/"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/08_collection_book/preview_v2/"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/08_collection_book/source_data_v1.json"
?? "13 Production/Orders/ORD-2026-0002_CL-0002_Valentina/09_delivery/"
?? "13 Production/Orders/ORD-2026-0003_CL-0002_Valentina/"
?? "13 Production/Orders/README.md"
?? "13 Production/Portfolio/P01/Business_V1/client_delivery/"
?? "13 Production/Portfolio/P01/Business_V1/marketing_v2/"
?? "13 Production/Portfolio/P02/Boudoir_V1/"
?? "13 Production/Portfolio/P02/Business_V1/client_delivery/"
?? "13 Production/Portfolio/P02/Business_V1/marketing_v2/"
?? "13 Production/Portfolio/P03/Business_V1/client_delivery/"
?? "13 Production/Portfolio/P03/Business_V1/marketing_v2/"
?? "13 Production/Portfolio/P03/Lifestyle_V1/"
?? "13 Production/Product_Standards/History/"
?? "13 Production/Product_Standards/ONYX_COMMERCIAL_FREEZE_REPORT_2026-09-20.md"
?? "13 Production/Product_Standards/ONYX_COMMERCIAL_VERSION_HISTORY_v1.md"
?? "13 Production/Product_Standards/ONYX_CORRECTION_POLICY_v1.md"
?? "13 Production/Product_Standards/ONYX_HUMAN_QA_STANDARD_v1.md"
?? "13 Production/Product_Standards/ONYX_LAUNCH_KPI_v1.md"
?? "13 Production/Product_Standards/ONYX_LAUNCH_READINESS_CHECKLIST_v1.md"
?? "13 Production/Product_Standards/launch_kpi_v1.yaml"
?? "13 Production/Samples/P02_Business_Collection_Book_v1/GIT_REPORT.txt"
?? "13 Production/Samples/P02_Business_Collection_Book_v1/NEW_FILES.txt"
?? "13 Production/Samples/P02_Business_Collection_Book_v1/P02_BUSINESS_COLLECTION_BOOK_v1_manifest.yaml"
?? "13 Production/Samples/P02_Business_Collection_Book_v1/PREFLIGHT.md"
?? "13 Production/Samples/P02_Business_Collection_Book_v1/REVISION_05_CONTACT_SHEET.jpg"
?? "13 Production/Samples/P02_Business_Collection_Book_v1/STYLE_REVIEW_REVISION_04.md"
?? "13 Production/Samples/P02_Business_Collection_Book_v1/STYLE_REVIEW_REVISION_05.md"
?? "13 Production/Samples/P02_Business_Collection_Book_v1/STYLE_REVIEW_REVISION_06.md"
?? "13 Production/Samples/P02_Business_Collection_Book_v1/STYLE_REVIEW_REVISION_07.md"
?? "13 Production/Samples/P02_Business_Collection_Book_v1/STYLE_REVIEW_REVISION_09.md"
?? "13 Production/Samples/P02_Business_Collection_Book_v1/STYLE_REVIEW_REVISION_10.md"
?? "13 Production/Samples/P02_Business_Collection_Book_v1/preflight_git_status.txt"
?? "13 Production/Samples/P02_Business_Collection_Book_v1/preview/"
?? "13 Production/Samples/P02_Business_Collection_Book_v1/revisions/"
?? "13 Production/Samples/P02_Business_Collection_Book_v1/source_data.json"
?? engine/production/onyx_marketing_builder.py
?? engine/production/onyx_pulid_collection.py
?? val4.jpg
```

No commit. No push. No unrelated files staged.
