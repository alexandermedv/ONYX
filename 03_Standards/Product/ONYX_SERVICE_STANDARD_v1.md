# ONYX Service Standard v1

CURRENT, revised 2026-09-21. [Commercial source of truth](ONYX_PRODUCT_SYSTEM.md) governs frozen prices, deliverables, rounds and upgrades. This is an operational business policy, not a new legal contract.

## Customer journey and payment

Lead → product selection → references submitted → Reference QA → feasibility and capacity confirmed → final scope, price and deadline confirmed → 100% prepayment → Premium Concept Card approval where applicable → production → technical and human QA → client review/corrections → final QA → Book where included → delivery → resolution recorded → `CLOSED` → retention/deletion under [Data Retention & Deletion](../Client_Experience/Intake/ONYX_DATA_RETENTION_AND_DELETION_v1.md).

Reference QA must be PASS or PASS_WITH_NOTES with limitations resolved/agreed before payment and final acceptance. NEEDS_MORE_REFERENCES/REJECT cannot proceed to payment. No generation is promised before prepayment. Reference Guide uses quality-based sufficiency; 4–8 useful images is an orientation, not a hard limit.

| State | Meaning / gate | Next states |
|---|---|---|
| LEAD | Product interest | WAITING_FOR_REFERENCES, CLOSED |
| WAITING_FOR_REFERENCES | Intake, per-order processing consent and usable inputs | REFERENCE_REVIEW, CLOSED |
| REFERENCE_REVIEW | Assess reference suitability and scope feasibility | WAITING_FOR_PAYMENT, WAITING_FOR_REFERENCES, CLOSED |
| WAITING_FOR_PAYMENT | Accepted references, final quote and confirmed capacity | READY_FOR_PRODUCTION, WAITING_FOR_CLIENT, CLOSED |
| WAITING_FOR_CLIENT | Premium direction approval, cancellation choice or consolidated feedback | READY_FOR_PRODUCTION, IN_REVISION, FINAL_QA, CLOSED |
| READY_FOR_PRODUCTION | Full payment received and logged; inputs, consent, capacity and creative approval complete | IN_PRODUCTION |
| IN_PRODUCTION | Bounded configured attempts | IN_QA, CLOSED through resolution |
| IN_QA | Technical/human review and collection diversity | WAITING_FOR_CLIENT, FINAL_QA, IN_PRODUCTION |
| IN_REVISION | Agreed subjective scope | IN_QA |
| FINAL_QA | All ordered finals accepted; Book/package checked | READY_FOR_DELIVERY, IN_PRODUCTION |
| READY_FOR_DELIVERY | Approved clean package | DELIVERED |
| DELIVERED | Actual handover recorded | CLOSED |
| CLOSED | Delivery or cancellation/refund resolution complete; `order_closed_at` recorded. Starts 30-calendar-day image-retention clock. | — |

These are documentation/config states, not a newly implemented runtime state machine. Record resolution outcome separately from state: fulfilled, cancelled, refunded or otherwise explicitly agreed; CLOSED alone does not prove success.

### Legacy order-state mapping

Keep the existing persisted states in `products_v1.yaml` and current order records. This mapping supplies the requested operational names without renaming records or changing runtime consumers:

| Operational stage | Existing persisted state / record |
|---|---|
| `INTAKE` | `LEAD` or initial order record |
| `WAITING_FOR_REFERENCES` | `WAITING_FOR_REFERENCES` |
| `REFERENCE_QA` | `REFERENCE_REVIEW` |
| `READY_FOR_PAYMENT` | `WAITING_FOR_PAYMENT` after PASS/PASS_WITH_NOTES and confirmed quote/capacity |
| `PAID` | `READY_FOR_PRODUCTION` only when `payment_status: PAID` is recorded |
| `IN_PRODUCTION` | `IN_PRODUCTION` |
| `IN_QA` | `IN_QA` / `FINAL_QA` |
| `WAITING_FOR_CLIENT_CORRECTION` | `WAITING_FOR_CLIENT` / `IN_REVISION` |
| `READY_FOR_DELIVERY` | `READY_FOR_DELIVERY` after final acceptance |
| `DELIVERED` | `DELIVERED` with handover timestamp |
| `CLOSED` | `CLOSED` after delivery or agreed cancellation/refund resolution |
| `REFUNDED` | Keep as `resolution_status: REFUNDED`; persisted state becomes `CLOSED` after refund completion |
| `CANCELLED` | Keep as `resolution_status: CANCELLED`; persisted state becomes `CLOSED` after cancellation resolution |

Do not transition to `CLOSED` while a refund remains unresolved. `CLOSED` plus `order_closed_at` starts image-retention countdown; storing resolution as metadata preserves existing status consumers.

## Service levels and correction boundaries

Portrait: one direction, one final, no Book or included subjective round. Signature: one main Collection, usually 2–3 Concepts, ten finals, one round, Standard Book. Premium: one main Collection, usually 4–6 Concepts, twenty finals, two rounds, Extended Book and deeper direction. Compatible adjacent Concepts are possible; full second Collection is separate scope.

[Correction Policy](ONYX_CORRECTION_POLICY_v1.md) distinguishes free QA defects from subjective changes. New major wardrobe/location/Concept is scope expansion, not automatically a correction. No unlimited retries or rounds.

## Deadlines and upgrades

Standard deadline is agreed per order; no unsupported global SLA. Priority targets within 24 hours and Express same day only after explicit capacity confirmation and all inputs/payment/approvals. Record timezone, start and deadline; QA remains unchanged. Prices and surcharge basis are in [Price Book](ONYX_PRICE_BOOK_v1.md).

Portrait → Signature and Signature → Premium each cost an additional 2000 RUB within 7 calendar days of source delivery, subject to source policy eligibility. Target totals remain 3000/5000 RUB. Target finals/rounds are cumulative, not two sessions; prior used rounds count toward the target allowance. Verify consent, reference availability and continuing context; never extend retention automatically. If context is unavailable after closure, transparently offer a new order rather than a technical upgrade. Never charge the credited base price twice.

## Payment, capacity and urgent orders

The soft-launch flow is **References submitted → Reference QA → feasibility confirmed → final scope/price/deadline confirmed → 100% prepayment → production starts**. Reference QA is free and precedes payment. Do not collect production prepayment until references are usable, the selected product and scope are feasible, the total is confirmed and capacity is available. Record the quote and the client's confirmation. Start only after the full agreed amount is received, verified and logged. Use the existing approved payment channel; this policy assumes no new provider, credential or fee.

For Priority/Express, confirm available capacity and target first; confirm surcharge and exact total second; collect payment after the client agrees; then start urgent production. If the target cannot be met, do not sell or collect its surcharge. If an accepted urgent target later becomes impossible, promptly agree a revised deadline or refund the undelivered urgency surcharge as applicable.

## Failed production, cancellation and refunds

Use the bounded reasonable effort allowed by the job configuration. Regenerate/replace isolated failures; do not automatically cancel the whole session for a rejected frame. If ONYX cannot deliver an accepted result meeting its minimum production/QA standard, stop retries, preserve diagnostics, notify the client, and record the order as unresolved/failed rather than successfully delivered. The base resolution is refund of payment for the unfulfilled order. If a mutually accepted alternative scope resolves the issue, record the choice and delivered scope; rejected images or an unwanted credit are not fulfillment.

The operator records paid amount, delivered/accepted scope, reason, resolution offered, client decision and refund completion. If part of a multi-part order is accepted and the remainder cannot be completed, agree a refund for the unfulfilled part based on the confirmed line-item quote. If no separable line value was quoted, the owner agrees the proposed amount with the client before processing. Record amount and processing evidence. Do not invent a fixed deduction or require store credit.

For client cancellation before production starts, the soft-launch operational default is a full refund of the amount received. Do not deduct hypothetical expenses. If a verifiable unavoidable third-party charge has already been incurred, record it and obtain owner review before proposing any adjustment; do not apply an automatic penalty. Once production starts, record work performed, direct costs actually incurred, stage and applicable requirements. The owner proposes a case-specific resolution and agrees the amount with the client before processing. No fixed forfeiture or absolute no-refund-after-generation rule applies.

Process refunds through the original payment channel when available; otherwise agree a documented method with the client. Record `refund_status`, amount, date, channel/reference and confirmation. Do not promise an unsupported processing-time SLA; share only timing confirmed by the actual provider for that transaction. Keep minimal payment/refund records separate from image files. Exact public cancellation Terms may receive separate legal review; this does not block the internal operational workflow or Avito Pack preparation.

## Privacy and delivery

[Consent & Privacy](../Client_Experience/Intake/ONYX_CONSENT_AND_PRIVACY_v1.md) remains authoritative. Per-order processing consent is required; reuse for a new order needs explicit reuse consent. Portfolio and marketing consent are separate and not implied by purchase. Apply the relevant permission to Avito, social, website and advertising; denied/not asked never permits publication.

Retain client image assets no later than 30 calendar days after `CLOSED`, with earlier deletion on an eligible request when no correction/dispute needs the assets. Closure starts the clock. Separate minimal order/transaction/consent records; this policy asserts no fixed legal retention term for them. Follow the manual checklist in [Data Retention & Deletion v1](../Client_Experience/Intake/ONYX_DATA_RETENTION_AND_DELETION_v1.md). No automated purge or third-party erasure is claimed.

Only accepted clean finals, the included Book and approved client readme belong in delivery. No sources, rejected candidates, prompts, internal paths or manifests. `onyx` is internal project storage; never use personal `alexander` or expose direct MinIO access. Use the approved delivery layer and verify its access/expiry for each order.

Delivery counts are 1/10/20 plus purchased additional finals; a legacy ten-frame builder is not a universal product rule. Portrait/Premium may be manually packaged with recorded human QA until their automation is adapted. Record final IDs, acceptance, source integrity, Book QA and actual handover.

Ask for post-delivery satisfaction, remaining defects, intended-use suitability and optional repeat/Collection interest; record complaints and resolution without inferring marketing consent. Feedback collection may be manual at soft launch.
