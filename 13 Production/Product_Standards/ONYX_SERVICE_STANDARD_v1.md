# ONYX Service Standard v1

**Status:** production service framework. It establishes operating states and boundaries; it does not promise an unmeasured SLA or approve legal payment terms.

## Customer journey

```text
Lead
→ Product selection
→ Preview or direct purchase
→ Payment
→ Intake
→ Reference QA
→ Production
→ Internal QA
→ Client review where applicable
→ Corrections
→ Final QA
→ Collection Book
→ Delivery
→ Feedback
→ Retention / deletion
```

## Order states for future automation

| State | Meaning | Typical next states |
| --- | --- | --- |
| `LEAD` | Product interest recorded | `WAITING_FOR_PAYMENT`, `WAITING_FOR_REFERENCES` |
| `WAITING_FOR_PAYMENT` | Payment step pending | `WAITING_FOR_REFERENCES`, `CLOSED` |
| `WAITING_FOR_REFERENCES` | Intake or usable references pending | `REFERENCE_REVIEW`, `CLOSED` |
| `REFERENCE_REVIEW` | References are assessed for identity input quality | `READY_FOR_PRODUCTION`, `WAITING_FOR_REFERENCES` |
| `READY_FOR_PRODUCTION` | Inputs and, for Premium, Concept Card approval are complete | `IN_PRODUCTION` |
| `IN_PRODUCTION` | Generation, repair and post-processing underway | `IN_QA` |
| `IN_QA` | Internal quality gate and diversity review | `WAITING_FOR_CLIENT`, `FINAL_QA`, `IN_PRODUCTION` |
| `WAITING_FOR_CLIENT` | Preview decision, Premium Concept Card approval or client revision input pending | `IN_REVISION`, `FINAL_QA`, `CLOSED` |
| `IN_REVISION` | Approved subjective correction scope underway | `IN_QA` |
| `FINAL_QA` | Final assets and delivery package checked | `READY_FOR_DELIVERY` |
| `READY_FOR_DELIVERY` | Delivery package prepared | `DELIVERED` |
| `DELIVERED` | Client delivery completed | `CLOSED` |
| `CLOSED` | Service completed, cancelled or retained/deleted under policy | — |

These states complement, rather than replace, existing production-asset statuses in the Product System.

## Service levels

| Area | Preview | Signature | Premium |
| --- | --- | --- | --- |
| Customer role | Minimal choice: collection and primary look | Chooses existing collection; limited creative participation | Completes Creative Profile and approves a Concept Card |
| Creative direction | No concept approval | Standard collection framework | Individual direction and scene plan |
| Delivery | One final high-resolution image | 10 images, standard Collection Book and delivery package | 20 images, extended Book, Motion, use guidance and optional social-ready copies |
| Revisions | Technical correction only | One launch-policy subjective correction round with limited scope | Two launch-policy subjective correction rounds with broader scope |

No turnaround-time SLA is set until production measurements exist. Use `TBD` rather than promising hours or days.

## Correction policy

### Technical correction — included

Technical correction covers visible artefacts; hands, eyes or anatomy errors; extra objects; image defects; and unexpected identity failure. These are internal quality obligations, not subjective client revisions.

### Client revision — launch policy

Client revision covers a different outfit, pose, scene, expression or additional stylistic request. Signature includes one correction round with a limited number of images; Premium includes two rounds with a higher replacement/correction scope. Do not publish a fixed image-count limit until first-order data is reviewed.

This is a launch policy to validate after the first paid orders. A request beyond the agreed scope may require a new product decision or separate quote; no automatic entitlement is created.

## Reference quality policy

A usable reference set has clear, recent images of the client, adequate face visibility, varied angles or expressions where available, and no severe blur, obstruction or conflicting identity information. The needed number varies by identity method and available source material; do not impose an unsupported universal minimum.

Ask for new references when identity cannot be evaluated reliably, the face is consistently obscured/blurred, the supplied images conflict materially, or quality gates identify poor identity input. Do not start production with knowingly inadequate references unless the client has been informed of the limitation and the responsible production decision is recorded.

## Premium intake and Concept Card

Collect purpose, professional field, intended uses, desired impression, preferred style, Natural/Polished/Glamour level, clothing, environments, elements to avoid, permitted facial/body correction and additional wishes. Convert them into a Premium Creative Brief and one bounded Concept Card.

Concept approval happens before `READY_FOR_PRODUCTION`. Keep it to one concise direction check; it does not initiate unlimited custom design work.

## Delivery

High-resolution originals are the primary deliverable. Signature includes the standard Collection Book; Premium includes the extended Book requirement and, when feasible, Motion and social-ready copies. The client receives delivery through the approved delivery layer, not direct MinIO access.

## Privacy, consent and retention

- Client photos are private production data.
- MinIO `onyx` is internal production storage; clients do not receive direct MinIO access.
- Source references and production artefacts are never published or used in a portfolio without separate client consent.
- Retention duration and the deletion procedure are **OWNER DECISION REQUIRED**. Until approved, record the intended lifecycle and do not imply a retention period to clients.
- A deletion request/process must be tracked as an operational event without exposing storage credentials or private locations.

## Payment and failed-production framework — OWNER DECISION REQUIRED

Do not publish final rules for prepayment, cancellation, refunds, Preview-credit expiry or failed-production outcomes until owner approval. During launch, record each exceptional case and use it to form the final policy.
