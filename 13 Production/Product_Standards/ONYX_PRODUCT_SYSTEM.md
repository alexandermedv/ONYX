# ONYX Commercial Product System v1

Commercial source of truth: **ONYX_COMMERCIAL_PRODUCT_SYSTEM_v1**.
Version status: **CURRENT**. Commercial status: **FROZEN_FOR_SOFT_LAUNCH**.
Freeze date: **2026-09-20**. Owner: ONYX owner.

This file governs product names, prices, deliverables, corrections, add-ons and upgrades.
[Price Book](ONYX_PRICE_BOOK_v1.md) and [products_v1.yaml](products_v1.yaml) are synchronized views of this document, not independent authorities.
Operational readiness is tracked separately in [Launch readiness](ONYX_LAUNCH_READINESS_CHECKLIST_v1.md); frozen commercial scope does not certify every production route or Collection.
Earlier values are SUPERSEDED; see [version history](ONYX_COMMERCIAL_VERSION_HISTORY_v1.md).

## Product taxonomy

**Collection → Concept → Scene → Final Image**

- Collection: a broad visual direction, such as Business, Executive, Lifestyle, Fashion, Glamour, Travel or Evening. The [Collection Catalog](ONYX_COLLECTION_CATALOG.md) describes existing directions; listing does not grant launch availability.
- Concept: a distinct creative idea within a Collection, e.g. Corporate Headshot, Formal Executive, Boardroom, Smart Casual, Workspace, Office Walk or Window Portrait in Business.
- Scene: a concrete composition within a Concept. Boardroom may contain seated at table, standing by presentation screen, close executive portrait and walking into boardroom.
- Final Image: an individually accepted client deliverable after final QA, not a candidate or generation attempt.

New scene plans and commercial manifest extensions record collection_id, concept_id, scene_id and final_image_id, with links to candidate provenance and acceptance. Existing asset IDs and canonical runtime contracts are not rewritten. The YAML documents an additive future manifest contract; runtime enforcement is not implemented by this freeze.

## Frozen product matrix

| Product / stable ID | Price, RUB | Final images | Collection scope | Concepts | Client correction rounds | Collection Book |
|---|---:|---:|---|---|---:|---|
| ONYX Portrait / ONYX_PORTRAIT_V1 | 1000 | 1 | Single agreed direction | 1 | 0 | No |
| ONYX Signature / ONYX_SIGNATURE_V1 | 3000 | 10 | 1 main Collection | Usually 2–3 | 1 | Standard PDF |
| ONYX Premium / ONYX_PREMIUM_V1 | 5000 | 20 | 1 main Collection | Usually 4–6 | 2 | Extended PDF |

Concept ranges are production guidance, never a hard customer deliverable count. Internal candidate budgets and retry limits are job configuration, never a promised number of generations. Only approved final images count toward delivery.

## ONYX Portrait

A complete standalone professional portrait service: CV/resume, business or corporate profile, messenger/avatar, social media, personal website, dating/profile photo and other single-portrait uses. Customer wording: «Один готовый профессиональный портрет». Do not position it as trial, demo, пробное фото or тестовая генерация.

Includes reference suitability review, one agreed Concept/Scene direction, internal candidates, identity preservation, technical/face/eyes/anatomy/realism QA, selection of one final, standard final preparation and correction of ONYX technical defects before delivery (and defects missed at delivery).

No multi-scene session, independent additional Concepts, Collection Book, separate client correction round, requested wardrobe/location variants, all intermediate generations or unlimited revisions are included.

## ONYX Signature — CORE / RECOMMENDED PRODUCT

A compact complete virtual photoshoot in one main Collection: usually 2–3 Concepts, multiple Scenes and 10 curated finals. Includes Client Intake, Reference QA, creative direction, scene planning, candidate production, identity preservation, diversity, human and technical QA, regeneration/replacement of unacceptable frames, repair as needed, curation, final QA, one client correction round, Standard Collection Book PDF and delivery package.

The client buys 10 finished images. Candidate counts such as 12 or 20 remain internal production parameters. The approved Signature Book reference and current layout rules remain in [Collection Book Standard](ONYX_COLLECTION_BOOK_STANDARD.md).

## ONYX Premium

An extended editorial photoshoot with deeper creative direction and a richer coherent visual story: 20 finals, one main Collection, usually 4–6 Concepts and multiple Scenes. Greater range of wardrobe, viewpoints, expressions, compositions, scene types and mood must preserve identity, realism and coherence.

Includes Signature production quality obligations, Personal Creative Profile, Premium Creative Brief, one bounded pre-production Concept Card approval, curation, replacement/regeneration, repair as needed, final QA, two client correction rounds, Extended Collection Book PDF and delivery package. The extended Book contains all 20 images, clearer narrative structure and Concept chapters when useful, with personalized selection/use guidance.

Compatible adjacent Concepts are allowed when they form one session. Business / Executive can be coherent; **Business + Lifestyle included** or two full Collections is not the default. A full second Collection is separately scoped and quoted; no frozen Additional Collection price exists.

ONYX Motion and specialized social export sets from the previous model are not mandatory frozen deliverables. They remain future separately approved scope; no video or Book is produced by this documentation change.

## Add-ons and independent Repair

| Service / stable ID | Price, RUB | Applies to | Boundary |
|---|---:|---|---|
| Additional Final Image / ADD_FINAL_IMAGE | 500 | 1 extra accepted final within agreed Collection/Concept or close Scene direction | Extra angle/pose/portrait in existing look; substantial new wardrobe, location, style or Concept is separately scoped |
| Additional Concept / Look / ADD_CONCEPT | 1000 | New creative idea/look/location type within existing or compatible Collection architecture | Not automatically a separate Collection; final count stays the ordered count unless extra finals are purchased |
| Additional Correction Round / ADD_CORRECTION_ROUND | 700 | One subjective round after included rounds are used; Portrait has zero included | No new session, full creative reset, new Collection or unlimited regeneration |
| ONYX Repair / ONYX_REPAIR | from 500 simple; from 1000 complex | External image or new scope outside ONYX obligations | Price and feasibility only after inspection; no guarantee of technically impossible repair |
| ONYX Priority / ONYX_PRIORITY | +50% | Confirmed capacity; target within 24 hours | Queue change only; unchanged identity and QA standard |
| ONYX Express / ONYX_EXPRESS | +100% | Explicitly confirmed capacity; same-day target | Not always available; unchanged identity and QA standard |

Additional Concept fee pays for creative scope, not an unspecified bonus image bundle. Confirm its final count in the quote before payment; Additional Final Image supplies extra finals when needed. ONYX classifies substantial creative changes as Concept/Collection/new order rather than a simple extra final, explains the scope and confirms the price first.

Repair may cover hands/anatomy, clothing, background, object removal/replacement, local composition, realism or restoration. A defect in ONYX's own final delivery is corrected free, never sold as paid Repair.

Urgency quote records the surcharge base explicitly: approved production subtotal (base product plus applicable production add-ons), excluding any urgency fee itself; Priority and Express are alternatives, not cumulative. The accepted quote records the exact total and delivery deadline before payment. Timing starts only when usable references, consent, agreed scope, required approvals and payment are complete. Express requires an explicit local same-day deadline; if that cannot be met, do not sell it. Standard delivery time is agreed per order; there is no measured universal standard SLA yet.

## Corrections

ONYX QA defects are corrected free and never consume a client round: extra/missing fingers, malformed hands/eyes, anatomy/body-proportion errors, severe face artifacts, damaged clothing, obvious AI artifacts, unusable technical output, identity failure or violation of an explicitly recorded requirement.

Client correction means a subjective change to an otherwise compliant image: smile intensity, small look change, preference for another version or local style adjustment. One round is one consolidated feedback list and the agreed bounded response; record affected finals and scope before work. Portrait includes zero, Signature one, Premium two. Further same-scope rounds cost 700 RUB. Full wardrobe/location/creative changes may be Additional Concept, Additional Collection or a new order. There is no unlimited regeneration entitlement or invented per-round image limit. See [Correction Policy](ONYX_CORRECTION_POLICY_v1.md).

## Upgrade rules

| Upgrade | Window | Credited base payment, RUB | Additional base payment, RUB | Target total, RUB |
|---|---|---:|---:|---:|
| Portrait → Signature | 7 calendar days | 1000 | 2000 | 3000 |
| Signature → Premium | 7 calendar days | 3000 | 2000 | 5000 |

Operational window: from recorded delivery of the source product, through delivery date + 7 calendar days in the order timezone; record request timestamp and eligibility. The result is the target package (10 or 20 total finals), not two separately charged packages. Prior accepted finals may count when they meet the continuing brief. Target tier's included correction allowance is cumulative: subtract rounds already used on the continuing order. Any outstanding QA defect stays free.

Upgrade requires available references, production context, consent and order metadata under the actual privacy policy; Signature → Premium also requires continuation of the original Collection. Never extend retention or reuse rights automatically to support an upgrade. If context is unavailable, explain that a new order is necessary; do not silently call it an upgrade. Additional services are separately itemized, not credited twice. Track prior credits to prevent double charging. Legacy Preview orders retain their recorded agreed terms; no automatic relabeling/repricing.

## References, payment, failed production and privacy

Reference QA and feasibility/capacity confirmation precede final acceptance and **100% prepayment**. For all three tiers 4–8 useful references is an orientation only: the mature [Reference Guide](../Client_Experience/Intake/ONYX_REFERENCE_GUIDE_v1.md) quality-based rule prevails; no universal hard minimum or maximum.

Failed candidates are regenerated/replaced within bounded job effort; one bad frame does not cancel a session. If reasonable effort cannot produce an acceptable order, it is not successfully fulfilled: stop retries, record evidence and use the [Service Standard resolution process](ONYX_SERVICE_STANDARD_v1.md). Never mark a rejected set delivered.

[Consent & Privacy](../Client_Experience/Intake/ONYX_CONSENT_AND_PRIVACY_v1.md) remains authoritative for processing, reference reuse and separate publication permissions. Purchase never grants portfolio, Avito, social, website or advertising permission. Default is no publication; require the relevant explicit consent. Synthetic portfolio characters follow existing asset/provenance approval rules. Client image assets follow [Data Retention & Deletion v1](../Client_Experience/Intake/ONYX_DATA_RETENTION_AND_DELETION_v1.md): up to 30 calendar days after CLOSED, with eligible early deletion; minimum order/payment/consent records are segregated and have no invented legal retention term. The upgrade window does not establish retention.

## Scope boundaries and future products

Default v1 excludes personal LoRA training, unlimited revisions, all candidates, internal prompts/workflows/seeds/config/model settings, complex manual Photoshop compositing, exact branded-object reproduction guarantees, physical books, multiple complete Collections inside Premium, explicit adult content, ONYX Private and unapproved scope.

PLANNED / FUTURE, not mandatory soft-launch scope: Additional Collection (price TBD), Physical Collection Book, Couple session, Family session, Corporate packages, printed products, advanced retouch, VIP LoRA, Motion and specialized social exports. Catalog presence does not make these saleable today.

## Pricing communication and internal rationale

Public headline: **Профессиональные AI-фото по вашим обычным снимкам — от 1 000 ₽.**

Public display: Portrait — 1 фото — 1 000 ₽; Signature ⭐ — 10 фото — 3 000 ₽; Premium — 20 фото — 5 000 ₽. Brief add-ons: +1 фото — 500 ₽; срочное выполнение — от +50%; исправление фото — от 500 ₽. Detailed correction/complex Repair fees belong in consultation, Price Book and Service Standard, not the first slide.

Portrait lowers purchase friction, serves real single-image needs and may lead to Signature. Signature is the core value package for most clients. Premium increases creative depth and average order value, not the number of full Collections. Extra finals monetize existing scope; Concepts monetize creative expansion; Repair is an independent acquisition/revenue channel; urgency compensates queue disruption.

## Freeze and review

Until **10 PAID ORDERS**, do not change base prices, final counts, Portrait/Signature/Premium structure or upgrade pricing except documented critical product issues, unsustainable economics, serious client confusion, legal/compliance issues or inability to deliver reliably. Record an owner decision, reason and synchronized Markdown/YAML revision before any exception. R&D never silently changes the freeze.

At 10 paid orders run **ONYX Product & Pricing Review v1.1**. Track unique paid order IDs; upgrade/add-on payments do not inflate this count. Record refunds separately. Portrait economics require operator minutes, attempts, generation cost when measurable, correction frequency and Portrait → Signature upgrade rate; do not change its price before evidence.

Soft-launch allocation: **80% SALES / CLIENT PRODUCTION / DELIVERY**, **20% R&D / AUTOMATION**. Model arenas, LoRA/PuLID/FLUX tuning, complex automation and website infrastructure must not delay sales. See [KPI framework](ONYX_LAUNCH_KPI_v1.md) and [readiness](ONYX_LAUNCH_READINESS_CHECKLIST_v1.md).
