# ONYX Launch Readiness Checklist v1

**Updated:** 2026-09-21. Commercial scope: **FROZEN_FOR_SOFT_LAUNCH**. Overall go/no-go status: **READY_FOR_AVITO_LAUNCH_PACK** — the product offer and minimum internal operating policies are now documented. This status permits preparation of the Pack; publication and accepting each order still require the per-order gates below.

Percentages are evidence-based checklist estimates, not measured probabilities or certification. They describe policy/documentation and available evidence; they do not assert paid-order volume or universal automation. Owner: product/policy decisions and Pack approval. Operator: order records, QA and manual deletion.

| Block | Status | Readiness % | Blocker / Non-blocker | Existing evidence | Per-order action / next owner action |
|---|---|---:|---|---|---|
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

**None for preparing ONYX Avito Launch Pack v1 or conducting a limited internal soft launch under these operational rules.** The policies do not certify that a particular payment provider, storage processor, or delivery link is currently configured. Confirm the channel actually available for each order before accepting payment or sending data through it. Do not claim deletion from systems outside the verified ONYX process.

## Non-blocking future legal/process improvement

Have exact customer-facing cancellation/refund Terms reviewed separately before adopting detailed deductions or quoting a processing deadline. This checklist uses a full-refund operational default before production and a documented, agreed case resolution after production; it does not invent legal forfeitures, accounting retention terms or a universal refund SLA. This review does not block Pack preparation/internal operation under those conservative rules.

## Per-order and per-channel gates

- Reference QA PASS or agreed PASS_WITH_NOTES; confirmed technical feasibility, final scope, price, deadline and full prepayment before production.
- Priority/Express capacity and delivery target confirmed before charging urgency.
- Human and technical QA passed for current final files; every ordered final accepted.
- Book visually checked; extra-final layouts prepared separately where the renderer's fixed 1/10/20 counts do not apply.
- Client delivery access and actual handover recorded.
- Portfolio/Avito/site/social/advertising asset scope has the correct explicit permission or is a separately approved synthetic asset.
- At closure, set `order_closed_at`, calculate `retention_until` at 30 calendar days in order timezone, segregate any necessary specific hold and assign the manual deletion task.

## Excluded from blockers

Website, CRM, automated deletion, API automation, FLUX/PuLID/LoRA improvements, Physical Book, ONYX Private and full automation.

## Next action

Prepare **ONYX Avito Launch Pack v1** using the frozen price table, approved client reply copy and only publication-approved visual assets. Pack preparation is authorized by this readiness state; owner approval remains the publication gate.
