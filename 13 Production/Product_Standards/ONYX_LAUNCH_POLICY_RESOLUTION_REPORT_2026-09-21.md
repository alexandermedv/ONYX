# Soft-launch policy resolution report — 2026-09-21

**Final go/no-go: `READY_FOR_AVITO_LAUNCH_PACK`.** Data-retention, operational payment and resolution policies now exist. The frozen commercial prices/product structure are unchanged. This status authorizes preparation of the Avito Pack; each order still has explicit reference, capacity, payment, QA, delivery and permission gates. Commit/push were not performed.

## 1. Pre-flight

- `pwd`: `D:\AI\ONYX`
- Branch: `main`
- HEAD: `885ffba9ea099778e228a89a92c91f90398e0045`
- Initial `git diff --stat`: as recorded on the worktree at task start below; the tracked summary is preserved in the prior freeze report.
- Initial working tree was already substantially modified by user work and the preceding product freeze. Files were checked inside `D:\AI\ONYX`; `%TEMP%` scripts were outside that repository and absent from Git. No user image/order/experiment assets were edited here.

## 2. Freeze report / actual worktree comparison

The 2026-09-20 freeze report says **27 modified + 21 created** files. Its file manifest contains exactly those counts. All 48 paths resolve inside this Git worktree; the 21 created outputs appear in `git status` as untracked files (some earlier output grouped them by directory). No listed path points into `C:\Users\ME\AppData\Local\Temp`.

The report's saved tracked diff is **65 files changed, 722 insertions, 270 deletions**, matching `git diff --stat` at this task's preflight. It also includes the same unrelated user edits that were present before the previous task; untracked files are excluded from `git diff --stat`. This comparison found no count/path mismatch, so the historical report was left intact.

The full preflight status and stat were saved during that freeze at:
[initial status](<D:/AI/ONYX/13 Production/Product_Standards/History/2026-09-20_commercial_freeze/final_git_status.txt>) and [diff stat](<D:/AI/ONYX/13 Production/Product_Standards/History/2026-09-20_commercial_freeze/final_git_diff_stat.txt>).

## 3. Created files

- [13 Production/Client_Experience/Intake/ONYX_DATA_RETENTION_AND_DELETION_v1.md](<D:/AI/ONYX/13 Production/Client_Experience/Intake/ONYX_DATA_RETENTION_AND_DELETION_v1.md>)
- [13 Production/Product_Standards/ONYX_LAUNCH_POLICY_RESOLUTION_REPORT_2026-09-21.md](<D:/AI/ONYX/13 Production/Product_Standards/ONYX_LAUNCH_POLICY_RESOLUTION_REPORT_2026-09-21.md>)

## 4. Modified files

- [13 Production/Client_Experience/Intake/ONYX_CONSENT_AND_PRIVACY_v1.md](<D:/AI/ONYX/13 Production/Client_Experience/Intake/ONYX_CONSENT_AND_PRIVACY_v1.md>)
- [13 Production/Client_Experience/Intake/schemas/intake_v1.schema.yaml](<D:/AI/ONYX/13 Production/Client_Experience/Intake/schemas/intake_v1.schema.yaml>)
- [13 Production/Client_Experience/Intake/README.md](<D:/AI/ONYX/13 Production/Client_Experience/Intake/README.md>)
- [13 Production/Product_Standards/ONYX_SERVICE_STANDARD_v1.md](<D:/AI/ONYX/13 Production/Product_Standards/ONYX_SERVICE_STANDARD_v1.md>)
- [13 Production/Product_Standards/products_v1.yaml](<D:/AI/ONYX/13 Production/Product_Standards/products_v1.yaml>)
- [13 Production/Product_Standards/ONYX_PRODUCT_SYSTEM.md](<D:/AI/ONYX/13 Production/Product_Standards/ONYX_PRODUCT_SYSTEM.md>)
- [13 Production/Product_Standards/ONYX_LAUNCH_READINESS_CHECKLIST_v1.md](<D:/AI/ONYX/13 Production/Product_Standards/ONYX_LAUNCH_READINESS_CHECKLIST_v1.md>)
- [13 Production/Product_Standards/ONYX_COMMERCIAL_VERSION_HISTORY_v1.md](<D:/AI/ONYX/13 Production/Product_Standards/ONYX_COMMERCIAL_VERSION_HISTORY_v1.md>)
- [13 Production/Marketing/Avito/ONYX_AVITO_LAUNCH_REQUIREMENTS_v1.md](<D:/AI/ONYX/13 Production/Marketing/Avito/ONYX_AVITO_LAUNCH_REQUIREMENTS_v1.md>)
- [13 Production/Orders/README.md](<D:/AI/ONYX/13 Production/Orders/README.md>)
- [10 Roadmap/Roadmap.md](<D:/AI/ONYX/10 Roadmap/Roadmap.md>)
- [13 Production/README.md](<D:/AI/ONYX/13 Production/README.md>)

## 5. Final retention rule

Client references, candidates, work/repair intermediates, production files and retained final copies are removed from active ONYX production storage **within 30 calendar days after `CLOSED`**. `order_closed_at` carries an offset/time zone; `retention_until` is 30 calendar days later in that zone. `CLOSED` follows actual delivery or completed cancellation/refund resolution. Eligible earlier client requests trigger manual deletion once no correction, delivery issue, complaint, dispute or incident needs the files. Specific holds apply only to necessary assets and require a reason, owner and review date.

Minimal transaction/order/consent evidence stays separate where needed. No accounting/payment retention term or legal retention claim was invented. External provider/backups may have separate deletion behavior; no universal/immediate erasure claim is made. Purchase alone never permits portfolio/Avito/site/social/advertising publication; the applicable separate permission is required and refusal changes neither price, service quality nor eligibility.

The manual checklist covers due/early requests, open holds, metadata minimization, active-storage deletion, Git image check, deletion status/date and separately permissioned marketing assets. No automated deletion was implemented.

## 6. Payment flow

**References submitted → Reference QA → feasibility confirmed → final scope/price/deadline confirmed → 100% prepayment received/recorded → production starts.** QA is free. Do not collect production payment until references, scope, feasibility, capacity and exact quote have been confirmed. For Priority/Express, capacity and deadline are confirmed before the surcharge quote; do not sell urgency without target capacity.

## 7. Refund/resolution matrix

| Case | Operational resolution |
|---|---|
| ONYX cannot complete accepted order to its minimum QA standard | Do not mark fulfilled; stop bounded retries. Refund payment for unfulfilled scope, or use a mutually accepted recorded alternative scope. |
| Individual frame fails QA | Regenerate, replace or repair within production; does not automatically cancel the complete order. |
| Genuine ONYX technical QA defect found after delivery | Correct free; does not consume a client correction round. |
| Output meets agreed brief; client asks for subjective changes | Signature 1 / Premium 2 included rounds, then the frozen correction/add-on policy. |
| Payment refunded | Log status, agreed amount/date/channel/reference and confirmation; close only when resolution/refund is complete. Do not promise an unverified processing SLA. |

## 8. Cancellation handling

For client cancellation before production starts, the soft-launch operational default is a full refund of the amount received. Do not deduct hypothetical expenses. If a verifiable unavoidable third-party charge has already been incurred, record it and obtain owner review before proposing any adjustment; do not apply an automatic penalty. Once production starts, record work performed, direct costs actually incurred, stage and applicable requirements. The owner proposes a case-specific resolution and agrees the amount with the client before processing. No fixed forfeiture or absolute no-refund-after-generation rule applies.

Exact public legal Terms for deductions and processing time can receive separate review before publishing those terms. This is a future client-Terms improvement, not a blocker to preparing the Pack or operating under the stated conservative internal process.

## 9. Order lifecycle

The existing persisted order-state list is unchanged. The Service Standard maps `INTAKE`, `REFERENCE_QA`, `READY_FOR_PAYMENT` and `PAID` to compatible existing states. `REFUNDED` and `CANCELLED` are recorded as resolution statuses; persist `CLOSED` only after the resolution completes, with `order_closed_at` starting the retention clock. The YAML marks these fields and canonical names as documentation-only; no runtime state-machine migration was made. Intake needs no new payment/retention fields. Existing marketing consent enums already support explicit permission.

## 10. Updated launch readiness

**Updated:** 2026-09-21. Commercial scope: **FROZEN_FOR_SOFT_LAUNCH**. Overall go/no-go status: **READY_FOR_AVITO_LAUNCH_PACK** — the product offer and minimum internal operating policies are now documented. This status permits preparation of the Pack; publication and accepting each order still require the per-order gates below.
| Block | Status | Readiness % | Blocker / Non-blocker | Existing evidence | Per-order action / next owner action |
| Product System | READY / FROZEN | 100 | Non-blocker | ONYX_COMMERCIAL_PRODUCT_SYSTEM_v1 and matching YAML | Keep prices/counts frozen; approve any later exception through versioned owner decision |
| Portrait | DEFINED / UNMEASURED | 80 | Non-blocker; acceptance gate | Frozen one-image scope | Confirm references and practical one-image delivery; measure real operator time |
| Signature | EVIDENCED | 95 | Non-blocker; order QA gate | Existing final human PASS, Book and delivery examples | Check exact current finals, accepted scope and clean package |
| Premium | DEFINED / PARTIAL EVIDENCE | 70 | Non-blocker to Pack; per-order capacity gate | Creative Profile and 20-image renderer planner | Confirm operator capacity and visually review each Extended Book before promise |
| Add-ons | DEFINED | 100 | Non-blocker | Frozen price/scope boundaries | Confirm exact final count and scope in each quote |
| Repair | CONDITIONAL | 85 | Non-blocker; per-image gate | Feasibility/quote rules | Inspect the submitted image and quote before payment |
| Upgrade rules | READY / CONTEXT GATED | 100 | Non-blocker | Frozen arithmetic and eligibility | Verify consent, available context and credit/round ledger |
| Price Book | READY | 100 | Non-blocker | Price Book and products_v1.yaml agree | Confirm total/deadline with client |
| Client Intake | READY | 95 | Non-blocker | PORTRAIT schema/example and consent records | Record per-order processing and any reuse consent |
| Reference Guide | READY | 100 | Non-blocker | Quality-based Reference Guide / Reference QA | Complete and record QA before requesting payment |
| Consent / marketing permission | READY | 100 | Non-blocker | Separate portfolio and marketing consent fields; default no-publication rule | Verify applicable explicit permission for each asset/channel; no permission means no publication |
| Privacy / image retention | READY / MANUAL | 95 | Non-blocker | 30 calendar days after CLOSED, early deletion checks, manual SOP | Set closure timestamp/deadline and complete checklist; explain external deletion limits |
| Order metadata separation | READY / MANUAL | 90 | Non-blocker | Minimal order/payment/consent/QA record fields defined | After image deletion retain only needed minimal business evidence; no unnecessary personal analytics |
| Payment | READY / PER-ORDER CHANNEL | 90 | Non-blocker to Pack; no production before gate | References → QA → feasibility/scope/price → 100% prepayment → production flow documented | Confirm an available approved payment channel, amount and receipt evidence for each order |
| Refund / failed production | READY / CASE-BASED | 90 | Non-blocker | Failed ONYX delivery resolves against unfulfilled scope; refund recording steps defined | Record client choice, amount, channel/reference and actual processing; no invented deadline |
| Client cancellation | OPERATIONAL RULE READY | 85 | Non-blocker; legal wording improvement remains | Full refund default before production; case assessment after start | Owner agrees actual amount with client; no automatic penalty/forfeiture |
| Human QA | READY / PER-OUTPUT | 95 | Non-blocker; delivery gate | ONYX_HUMAN_QA_STANDARD_v1 and existing human reviews | Approve exact current files before sending |
| Corrections | READY | 100 | Non-blocker | Defects are free; Signature 1 and Premium 2 client rounds | Separate QA defects from subjective requests |
| Collection Book | SIGNATURE EVIDENCED / PREMIUM CONDITIONAL | 80 | Non-blocker to Pack; Premium per-order gate | Signature PDFs and 1/10/20 renderer planner | Visually inspect each delivered Book; arbitrary add-on counts need a separate layout |
| Delivery | EVIDENCED / MANUAL FOR SOME TIERS | 80 | Non-blocker; per-order gate | Signature delivery examples and existing delivery SOP | Count 1/10/20 plus purchased finals; verify clean files, access and handover timestamp |
| Marketing assets | READY / RIGHTS GATED | 85 | Non-blocker | Marketing Standard, portfolio permissions and synthetic provenance process | Approve specific assets, copy and channel before use |
| Avito | READY_FOR_AVITO_LAUNCH_PACK | 80 | Non-blocker to Pack preparation | Commercial copy requirements and approved short policy text | Build Pack, review asset rights/copy/readability, then owner approves publication |
| Client communication | READY / SHORT COPY AVAILABLE | 95 | Non-blocker | Client-facing payment, corrections, refund and retention wording in data policy | Use product-specific rounds; explain agreed quote/exception before payment |
| KPI tracking | MANUAL READY | 90 | Non-blocker | Launch KPI framework/schema | Log leads, order, time, quality, expenses and resolution without unnecessary identity data |
| Post-delivery feedback | MANUAL READY | 85 | Non-blocker | Service Standard / KPI fields | Ask satisfaction/defects; do not infer marketing permission |
## TRUE SOFT-LAUNCH BLOCKERS

## 11. Remaining blockers

**None for Avito Launch Pack preparation or a limited internal operational soft launch under the documented gates.** Provider availability is checked per order; the repository does not prove any particular payment, external processor or delivery service is configured. No per-order payment may be taken until an available approved channel is confirmed.

## 12. Exact next action

Prepare **ONYX Avito Launch Pack v1** using the frozen price display, short policy wording and only permitted visual assets; have the owner approve the actual Pack before publication. Do not imply guaranteed service capacity or client-image publication permission.

## 13. Git state after this task

No commit or push. Existing user changes remain in the shared worktree. The full current status is recorded in the fenced block below. `git diff --stat` includes existing user work, not only this task; the file list above isolates the policy resolution.

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
 .../Intake/ONYX_CONSENT_AND_PRIVACY_v1.md          |  17 +-
 .../Intake/ONYX_PREMIUM_CREATIVE_PROFILE_v1.md     |   4 +
 .../Intake/ONYX_REFERENCE_QA_STANDARD_v1.md        |   4 +-
 .../Intake/ONYX_SIGNATURE_INTAKE_v1.md             |   2 +
 13 Production/Client_Experience/Intake/README.md   |  18 +-
 .../Intake/schemas/example_preview.yaml            |   1 +
 .../Intake/schemas/intake_v1.schema.yaml           | 145 +++++++-
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
 .../ONYX_GENERATION_ROUTE_POLICY_v1.md             |  19 +
 .../Product_Standards/ONYX_MARKETING_STANDARD.md   |  17 +-
 .../Product_Standards/ONYX_PORTFOLIO_STANDARD.md   |   6 +-
 .../ONYX_PREPAYMENT_PREVIEW_STANDARD.md            |   3 +-
 .../Product_Standards/ONYX_PRICE_BOOK_v1.md        |  62 ++--
 .../Product_Standards/ONYX_PRODUCT_SYSTEM.md       | 161 ++++-----
 .../Product_Standards/ONYX_SERVICE_STANDARD_v1.md  | 127 ++++---
 13 Production/Product_Standards/products_v1.yaml   | 401 +++++++++++++++++++--
 13 Production/README.md                            |  14 +
 .../COLLECTION_BOOK_PRODUCTION_GUIDE.md            |   4 +
 .../ONYX_COLLECTION_BOOK_TEMPLATE.md               |   4 +
 13 Production/Templates/Collection_Book/README.md  |   4 +
 engine/production/onyx_delivery.py                 |   7 +-
 65 files changed, 834 insertions(+), 267 deletions(-)
```

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
?? "13 Production/Client_Experience/Intake/ONYX_DATA_RETENTION_AND_DELETION_v1.md"
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
?? "13 Production/Product_Standards/ONYX_LAUNCH_POLICY_RESOLUTION_REPORT_2026-09-21.md"
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
