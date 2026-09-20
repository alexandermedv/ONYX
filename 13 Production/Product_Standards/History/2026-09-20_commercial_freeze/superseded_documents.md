# Superseded working-tree texts — before commercial freeze

Status: SUPERSEDED commercial values, captured 2026-09-20 before this task's edits.
These are exact decoded text snapshots, including pre-existing user edits. They are historical evidence, not current client terms. Relative links inside quoted snapshots retain their original context and are not navigation links for this archive.

## 13 Production/Product_Standards/ONYX_PRODUCT_SYSTEM.md

````text
# ONYX Product System v1

**Status:** production launch standard.
**Scope:** product architecture and customer value; implementation, prices and service operations are defined by the linked standards.

## Positioning

ONYX is not a service for generating isolated AI images. Its core product is a **personal virtual photoshoot**, designed, selected, refined and delivered as a finished visual collection.

Technology is not the customer value proposition. The value is identity consistency, creative direction, diversity of the series, selection, quality control, regeneration and repair, retouch and enhancement, upscale, curator-style selection, Collection Book and a convenient delivery package.

## Launch product matrix

| Product | Customer outcome | Price, RUB | Final photographs | Creative model | Collection Book | Motion | Revisions |
| --- | --- | ---: | ---: | --- | --- | --- | --- |
| ONYX Preview | Personal test frame: proof of identity and collection quality before a full photoshoot | 900 | 1 | One chosen collection and primary look | No | No | Technical correction only |
| ONYX Signature | Personal photoshoot in a chosen collection | 3,000 | 10 | Standardized ONYX collection, adapted to the person | Standard | No | One launch-policy round, limited scope |
| ONYX Premium | Personalized visual story designed around the person’s goals and desired image | 5,000 | 20 | Personal Creative Profile, creative direction and scene plan | Extended | ONYX Motion | Two launch-policy rounds, broader scope |

**Preview proves. Signature standardizes. Premium personalizes.** Premium is not simply a 20-image Signature package.

Client-facing launch prices and Preview upgrade arithmetic are authoritative in [ONYX Price Book v1](ONYX_PRICE_BOOK_v1.md). The structured source for future automation is [products_v1.yaml](products_v1.yaml).

## ONYX Preview

### Purpose

Preview is a low-risk first purchase. It lets a client check identity preservation, see the style of a selected collection, understand ONYX quality and decide whether to purchase a full photoshoot.

Use customer language such as **«персональный тестовый кадр ONYX»**. Do not describe it as a sale of one AI image.

### Included

- one final high-resolution photograph;
- one chosen production-approved collection and one primary look;
- production QA;
- repair or regeneration when required for technical quality;
- final processing and high-resolution delivery.

Preview has no Concept Card, personal creative profile or client-directed creative cycle. A full Preview payment is credited when the client upgrades to Signature or Premium; it is a product price credit, not a discount on the listed total price.

## ONYX Signature

### Purpose

**Персональная фотосессия в выбранной коллекции.** Signature is the standard mass-market ONYX product.

Signature is standardized by creative framework. The client chooses a ready ONYX Collection, such as Business, Executive, Lifestyle or another production-approved collection. ONYX adapts the collection to the individual; it does not design a wholly new visual concept from zero.

### Included

- 10 final photographs;
- usually 2–3 looks and 4–6 visually distinct scenes, adjusted when quality requires it;
- one coherent collection visual language;
- identity consistency and diversity control;
- production QA, repair or regeneration, retouch or enhancement and upscale;
- ONYX Selection;
- standard ONYX Collection Book;
- high-resolution originals and delivery package.

The P02 Business Collection Book is the approved Signature reference implementation. See [Collection Book Standard](ONYX_COLLECTION_BOOK_STANDARD.md) and [production guide](../Templates/Collection_Book/COLLECTION_BOOK_PRODUCTION_GUIDE.md).

## ONYX Premium

### Purpose

Premium is a **photoshoot developed around the client’s personality, goals and desired image**. It is a personalized visual story with more creative variety, not a larger standard collection.

### Included

- 20 final photographs;
- Personal Creative Profile and Premium Creative Brief;
- individual creative direction and scene plan;
- usually 4–5 looks, 8–12 scenes and several visual chapters or moods, adjusted when quality requires it;
- increased variety and identity consistency;
- production QA, repair or regeneration, retouch or enhancement and upscale;
- extended ONYX Collection Book;
- ONYX Selection and, where useful, additional curator selections;
- Personal Style Recommendation and Recommended Use guidance;
- ONYX Motion;
- social-ready export formats in addition to high-resolution originals;
- expanded client revision scope.

The 5,000 RUB launch price is a hypothesis. Reassess it after the first real orders using measured unit economics; it is not a promise of a permanent price.

### Personal Creative Profile

Premium production begins only after collecting: purpose of the photoshoot; profession or field; intended uses; desired impression; preferred style; Natural / Polished / Glamour level; clothing; preferred environments; elements to avoid; permitted facial and body correction; and other wishes.

These inputs become the internal **Premium Creative Brief**. They guide production but do not authorize unsupported changes to identity or appearance.

### Concept Card and approval

Premium includes a brief operational concept approval before batch production. It is a bounded direction check, not an open-ended bespoke design engagement.

```text
ONYX PREMIUM CONCEPT

Client:
Collection / concept:
Visual direction:
Mood:
Primary use:
Looks:
Scenes:
Key priorities:
Avoid:
```

The client approves or corrects this card once before mass generation. The service standard defines the state transition.

### Visual chapters

Premium should be organized as logical visual chapters so it reads as a complete story rather than 20 variations of one scene. For a Business or Executive direction, chapters may be Portrait, At Work, Personal Brand and Editorial. This is an example, not a mandatory universal list; chapters come from the Creative Profile.

### ONYX Motion

ONYX Motion is a Premium deliverable: a short cinematic motion portrait based on a key collection frame. Target: about four seconds, natural motion and expression, minimal artefacts, a premium look and vertical/social-friendly format. The underlying model is not part of the product definition and may change.

### Premium Collection Book and use guidance

Premium Book requirements extend the Signature standard with Personal Creative Direction, visual chapters, ONYX Selection, optional additional curator selections, Personal Style Recommendation, Recommended Use, personal closing note and next collections. No Premium Book PDF is defined by this document.

Recommended Use is personalized after final selection and may cover a professional profile, avatar, corporate site, speaker bio, CV, social media or editorial/personal-brand use when relevant. It does not promise particular platforms.

Social-ready exports are optional optimized copies such as avatar/profile, portrait post or story/reel cover. High-resolution originals remain the main deliverable; no social assets are generated by this standard.

## What is outside the launch line

The following are future scope, not launch products: ONYX Private; fully bespoke products above Premium; subscriptions; corporate packages; website self-service; automated SaaS; unlimited generation; and Model Arena as a customer feature.

## Related standards

- [Price Book](ONYX_PRICE_BOOK_v1.md): prices, Preview credit and unit-economics placeholders.
- [Service Standard](ONYX_SERVICE_STANDARD_v1.md): journey, corrections, privacy, retention and delivery rules.
- [Portfolio Standard](ONYX_PORTFOLIO_STANDARD.md): asset roles and portfolio QA.
- [Marketing Standard](ONYX_MARKETING_STANDARD.md): marketing collateral only.
- [Collection Book Standard](ONYX_COLLECTION_BOOK_STANDARD.md): Signature and Premium Book requirements.

````

## 13 Production/Product_Standards/ONYX_PRICE_BOOK_v1.md

````text
# ONYX Price Book v1

**Status:** launch pricing framework. Client-facing prices are active launch prices; internal cost fields are intentionally unfilled until real orders are measured.

## Client-facing launch prices

| Product | Total product price, RUB | Customer wording |
| --- | ---: | --- |
| ONYX Preview | 900 | Personal test frame ONYX |
| ONYX Signature | 3,000 | Personal photoshoot in a chosen collection |
| ONYX Premium | 5,000 | Personalized visual story |

## Preview upgrade pricing

Preview payment is credited in full toward one subsequent Signature or Premium purchase.

| Upgrade | Total product price, RUB | Preview credit, RUB | Remaining amount after Preview upgrade, RUB |
| --- | ---: | ---: | ---: |
| Preview → Signature | 3,000 | 900 | 2,100 |
| Preview → Premium | 5,000 | 900 | 4,100 |

Always show both the total product price and the remaining amount after Preview upgrade. Do not call the remaining amount the price of Signature or Premium.

## Internal pricing fields — TBD after production tests

| Field | Definition | Status |
| --- | --- | --- |
| `inference_cost` | Direct generation cost per order | TBD |
| `manual_minutes` | Measured human production time | TBD |
| `repair_cost` | Cost of repair/regeneration work | TBD |
| `motion_cost` | Direct Motion cost for Premium | TBD |
| `delivery_cost` | Packaging, storage and delivery cost | TBD |
| `total_variable_cost` | Sum of variable costs | TBD |
| `effective_hourly_margin` | Margin after measured manual time | TBD |
| `gross_margin` | Revenue less variable cost | TBD |

## Payment policy — OWNER DECISION REQUIRED

The following are framework fields only and are not customer terms until approved by the owner:

- payment model and timing of prepayment;
- cancellation treatment;
- refund conditions;
- outcome when production cannot pass quality requirements;
- expiry or transferability of a Preview credit.

````

## 13 Production/Product_Standards/ONYX_SERVICE_STANDARD_v1.md

````text
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

````

## 13 Production/Product_Standards/products_v1.yaml

````text
version: 1
status: launch_product_definition
currency: RUB
pricing_note: "Launch prices; Premium price requires unit-economics review after real orders."
common:
  identity_consistency: true
  production_qa: true
  technical_correction_included: true
  high_resolution_originals: true
  delivery_layer_required: true
  direct_minio_access: false
products:
  preview:
    client_name: "ONYX Preview"
    positioning: "Personal test frame ONYX"
    price_rub: 900
    final_photos: 1
    collection_selection: single_approved_collection
    primary_look: 1
    creative_profile: false
    concept_approval: false
    collection_book: none
    motion: false
    social_ready_exports: false
    client_revision_policy: technical_only
    upgrade_credit_rub: 900
  signature:
    client_name: "ONYX Signature"
    positioning: "Personal photoshoot in a chosen collection"
    price_rub: 3000
    final_photos: 10
    expected_looks: "2-3"
    expected_visual_scenes: "4-6; quality-adjusted, not contractual"
    creative_model: standardized_collection
    creative_profile: false
    concept_approval: false
    collection_book: standard
    motion: false
    social_ready_exports: false
    onyx_selection: true
    client_revision_policy: "1 launch-policy round; limited scope"
    preview_upgrade_remaining_rub: 2100
  premium:
    client_name: "ONYX Premium"
    positioning: "Personalized visual story"
    price_rub: 5000
    final_photos: 20
    expected_looks: "4-5"
    expected_visual_scenes: "8-12; quality-adjusted, not contractual"
    creative_model: personalized_visual_story
    creative_profile: true
    concept_approval: true
    premium_creative_brief: true
    visual_chapters: true
    collection_book: extended
    motion: true
    social_ready_exports: true
    onyx_selection: true
    personal_style_recommendation: true
    recommended_use_guidance: true
    client_revision_policy: "2 launch-policy rounds; broader scope"
    preview_upgrade_remaining_rub: 4100
automation_fields:
  order_statuses:
    - LEAD
    - WAITING_FOR_PAYMENT
    - WAITING_FOR_REFERENCES
    - REFERENCE_REVIEW
    - READY_FOR_PRODUCTION
    - IN_PRODUCTION
    - IN_QA
    - WAITING_FOR_CLIENT
    - IN_REVISION
    - FINAL_QA
    - READY_FOR_DELIVERY
    - DELIVERED
    - CLOSED
  internal_pricing_fields:
    - inference_cost
    - manual_minutes
    - repair_cost
    - motion_cost
    - delivery_cost
    - total_variable_cost
    - effective_hourly_margin
    - gross_margin

````

## 13 Production/Product_Standards/ONYX_MARKETING_STANDARD.md

````text
# ONYX Marketing Standard

**Version:** 1.0  
**Date:** 2026-09-16  
**Status:** ACTIVE / Production Standard

## Standard layouts

| Type | Purpose |
| --- | --- |
| A — Hero | Primary visual promise |
| B — Gallery | Series and visual range |
| C — Before/After | Original/reference to ONYX result |
| D — Contact Sheet | Full ten-photo session |
| E — Text/Benefits | Product value and process |
| F — CTA | Direct next action |

## Avito carousel v1

| Slide | Message |
| --- | --- |
| 1 | Hero — professional photoshoot without studio |
| 2 | 10 final photographs |
| 3 | original/reference → ONYX result |
| 4 | full 10-photo contact sheet |
| 5 | more than generation: QA / repair / retouch / upscale |
| 6 | five-step workflow |
| 7 | collections |
| 8 | multiple characters / identities |
| 9 | ONYX quality control |
| 10 | CTA |

Customer-facing material must not expose LoRA, Flux, PuLID, ComfyUI, seed, checkpoint, face swap or prompt engineering. These may remain in internal technical documentation.

````

## 13 Production/Product_Standards/ONYX_PORTFOLIO_STANDARD.md

````text
# ONYX Portfolio Standard

**Version:** 1.0  
**Date:** 2026-09-16  
**Status:** ACTIVE / Production Standard

## Standard session

A standard session contains ten images. Roles are standardized, while their specific scenes depend on the collection.

| No. | Role |
| --- | --- |
| 01 | HERO |
| 02 | CLOSE |
| 03 | WAIST |
| 04 | SEATED |
| 05 | ENVIRONMENT |
| 06 | ACTION |
| 07 | 3Q_BODY |
| 08 | FULL_BODY |
| 09 | MOOD |
| 10 | EDITORIAL |

## Names

Final portfolio files use `ONYX_<CHARACTER>_<COLLECTION>_01_HERO.jpg` through `ONYX_<CHARACTER>_<COLLECTION>_10_EDITORIAL.jpg`.

```text
ONYX_<CHARACTER>_<COLLECTION>_COVER.jpg
ONYX_<CHARACTER>_<COLLECTION>_BEFORE_AFTER.jpg
ONYX_<CHARACTER>_<COLLECTION>_COLLAGE_4.jpg
ONYX_<CHARACTER>_<COLLECTION>_COLLAGE_6.jpg
ONYX_<CHARACTER>_<COLLECTION>_CONTACT_SHEET.jpg
```

Client delivery uses `ONYX_01.jpg` through `ONYX_10.jpg`.

## Portfolio Ready criteria

- identity master exists;
- canonical references exist;
- 10/10 final scenes exist;
- all 10 passed QA;
- no critical identity or anatomy defects;
- upscale is complete;
- standard exports are complete;
- portfolio-watermark version exists;
- cover, before/after, collage and contact sheet exist.

Canonical experimental images are referenced by promotion manifest. They are not renamed or overwritten to conform to this naming standard.

## Footer placement rule (v1.1)

- Footer is a contained lower field, 230 px in a 1080x1350 portfolio frame (about 17% of height).
- The source portrait is fitted with 	humbnail inside the upper field; never use cover/crop when it can remove a head or face.
- Keep the complete head and hair visible with safe space above; side margins are acceptable.
- Footer may overlap only the lower image boundary through a controlled transition; it must not move the portrait upward or crop the subject.
- Reject any export where a face, head, or critical body area is clipped by the footer.


### Эталонная геометрия framed preview

- Canvas: 1080 x 1350 px, portrait 4:5.
- Photo field: y=0..1120 px; fit with contain/thumbnail and preserve full head.
- Footer field: y=1120..1350 px; height 230 px, full canvas width.
- Stone footer texture is anchored to the lower field and does not resize the photo field.
- Logo lockup stays within the footer safe area; never stretch the monogram vertically.


### Footer lockup alignment

- The top of the monogram ring aligns with the horizontal rule above the copy.
- The bottom of the ONYX wordmark aligns with the bottom of the PORTFOLIO PREVIEW line.
- Logo and copy share one fixed footer alignment zone; do not stretch or independently offset either element.


````

## 13 Production/Product_Standards/ONYX_COLLECTION_BOOK_STANDARD.md

````text
# ONYX Collection Book Standard v1

Date: 2026-09-17. Status: approved reference layout; client-specific copy and asset approval remain required.

## Purpose

Collection Book is the personal editorial presentation of an ONYX photoshoot. It accompanies, never replaces, separate high-resolution photographs. It is not a technical report or evidence of publication approval.

## Delivery model

- Preview: one photograph; template supports a compact seven-page book, no sample produced.
- Signature: ten photographs; 14–18 pages, reference implementation 15.
- Premium: twenty photographs; reference layout 16 pages through paired compositions; optional Motion delivered separately with an explicit HTTPS link in the book.
- All orders retain their separate clean high-resolution photographs. Existing product delivery sets and pricing are unchanged. These tier names describe this template contract, not a pricing revision.

## Required sections

Cover with selected photo, approved logo, collection title and short subtitle; opening note from ONYX; collection purpose and use cases; personal note; complete photo story; ONYX Selection with a justified choice; final next-collections page.

Photo story must cover every ordered photograph exactly once. Cover and Selection may intentionally reuse photographs; every reuse must be recorded. Existing hero metadata takes precedence over subjective re-selection. No invented review scores.

## Optional sections

Client display name; captions; additional context when it is specific and brief; verified collection links; separately delivered Premium Motion link. QR URLs are reserved in v1 and rejected when nonempty until a QR renderer is implemented. Do not show inactive placeholder buttons or invented URLs.

Cross-sell copy and Business/Executive differentiation must follow [ONYX Collection Catalog](ONYX_COLLECTION_CATALOG.md).

## Copy standard

Opening note: explain ONYX’s mission, how the collection is assembled around a client’s task, and thank the client for the request; it must not address the client by name. Description: purpose, then practical uses. Selection: one or two sentences grounded in the chosen image and selection metadata. Closing: one to three restrained, series-specific sentences that address the client and draw on the approved persona or client brief, distinct from the collection description; a specific, supportable compliment is welcome. Cross-sell: only documented products; show “Скоро” unless launch availability is verified. Never imply a human photographer personally wrote the text.

Body copy is Russian in v1; established collection names and ONYX Selection may remain English. No client identity is invented for a demo. Sample display name may be empty.

## Visual standard

Authority: [Brand System](../Brand/ONYX_BRAND_SYSTEM.md), [Brandbook content](../Brand/ONYX_BRANDBOOK_CONTENT_V1.md), [Editorial Wordmark](../Brand/Logo/EDITORIAL_WORDMARK_V1.md).

Digital portrait canvas 1080 × 1350 logical units, 4:5. Manrope for body, Cormorant Garamond for short editorial headlines; approved champagne wordmark on an Onyx field. Preserve logo proportions and clear space. Warm White #F6F4EF, Onyx #111111, Champagne #B5A079; no gradients or invented identity.

Collection-specific proposals pending design approval: 72-unit safe margin, body 29–36 units, headline 72–91 units, 1.4 line spacing, and high-contrast section labels in Champagne with a short rule. Full-height 3:4 portraits retain narrow side fields on the 4:5 page. Never crop to achieve full bleed. Alternate full-height, inset, caption, asymmetric negative-space and paired layouts. No photo filters, stretching, decorative face overlays or frames on source files.

The v1 reference footer mirrors the approved 1080×230 Brandbook portfolio footer on every page: a stone field, centred monogram at x=170, the gold rule from x=330, collection lockup and page number aligned beneath it. Dark and full-photo pages use the Onyx stone field; Warm White pages use a quiet light-stone treatment in the same geometry and with the same lockup. Photo pages reserve this field below the image rather than overlay it. Cover use of Stone Signature must be symmetrical, stay inside the central layout grid, and keep each approved logo element intact.

Phone viewing budget: PDF ≤15 MiB; internal JPEG derivatives max edge 2048, quality 92, no chroma subsampling. This is a screen presentation, not a print master. Originals remain byte-identical. Main copy should be checked at phone scale; zoom remains useful for paired photographs and folios.

## Personalization requirements

Client display name, collection name/subtitle, ONYX mission note, cover/hero, description/use cases, Selection image/note, closing note/heading and next collections must be checked for the correct order. A fictional sample persona must be explicitly labelled internally, with boundaries that prevent it being treated as client biography. Never carry sample copy into a real delivery without editorial review.

## Privacy

External PDF excludes order IDs, internal identifiers, filenames, paths, prompts, hashes, workflow metadata and model information. Machine-readable manifest, source_data and review files are internal only. Do not distribute the entire sample folder as a client package. Text scan is a guard, not a substitute for human privacy review or inspection of text already present in a photograph.

## QA checklist

- PDF exists, nonempty, reopens, all pages render, expected 4:5 page count.
- Previews are rasterized from that exact PDF, not independent layout approximations.
- All ordered photos present; no accidental duplicates; only logged hero reuse.
- All references readable; source hashes match before and after; separate originals unchanged.
- Text boxes fit; glyph coverage and embedded fonts checked; no clipping or missing images.
- No internal paths, technical IDs or model vocabulary in visible text or document metadata.
- Original photo aspect ratios preserved; faces and hair not cropped by the layout.
- Logo/monogram and footer correct; page hierarchy and main copy readable on phone; PDF within size budget.
- Copy belongs to correct client; availability/links verified; no unsupported claims of approval.
- Visual review completed and owner approves design before delivery.

Automated PASS covers only measured technical checks. It never grants source approval, identity QA or publication rights.

````

## 13 Production/Product_Standards/ONYX_COLLECTION_CATALOG.md

````text
# ONYX Collection Catalog v1

**Status:** Product reference for Collection Book copy. Availability must be confirmed per order; entries below do not imply a launched public offer.

## How the catalog works

An ONYX product defines the use case; a collection defines a visual world and scene set. A Collection Book may recommend another collection only when it differs clearly from the book already delivered and its availability is verified. Otherwise use `Скоро` and no URL.

## Business

For professional presence where trust, clarity, and versatility matter. Typical uses: professional profile, company website, expert publication, presentation announcement, and social presence. Visual language: modern office, natural light, calm posture, direct but approachable portraiture.

The P02 sample belongs here.

## Executive

For founders, executives, and public experts whose work calls for a more formal status signal. It is distinct from Business through high-status environments and more formal editorial direction: CEO office, private library, financial district, premium lounge, executive meeting, and black interior. It should be recommended after Business only where that elevated positioning is a deliberate next need, not as a duplicate default.

## Lifestyle

For life outside the office: city walks, café, travel, weekend, sport, and hobbies. It creates a personal-brand extension rather than another business portrait series.

## Dating

For warm, natural images in social settings: coffee shop, restaurant, sunset walk, city evening, park, rooftop, and weekend trip. It has a different intent and visual energy from Business.

## Other documented directions

Family centers on shared home and leisure scenes. Fantasy is for deliberately fictional cinematic worlds. Both are separate from professional collections and require a collection-specific brief.

## Collection Book rule

Never imply that a listed collection is currently available because it appears in this catalog. For P02 Business, the current sample may show Lifestyle and Dating as `Скоро`; it must not recommend Executive by default.

````

## 13 Production/Product_Standards/ONYX_PREPAYMENT_PREVIEW_STANDARD.md

````text
# ONYX Prepayment Preview Standard v1

До оплаты клиент получает фирменный preview, а не технический черновик.

- Canvas: 1080 × 1350 px, full width photo, без боковых полей.
- Нижний footer: 230 px, каменная onyx-текстура и утверждённый lockup `BUSINESS COLLECTION / CLIENT PREVIEW`.
- Фото сохраняет голову и лицо; нижняя часть может уходить под footer.
- Поверх фото размещается небольшой полупрозрачный watermark `ONYX / PRIVATE PREVIEW / ORDER <ID>` без чёрной плашки и без перекрытия лица.
- В footer или рядом с watermark указывается ID заказа.
- Preview экспортируется в уменьшенном размере; paid delivery содержит clean JPEG и master без watermark.
- Нельзя отправлять preview без watermark и нельзя использовать watermark, который можно легко обрезать.
- Подпись `PORTFOLIO PREVIEW` используется только для портфолио и запрещена в клиентской выдаче.
- Папка `00_PREPAYMENT_PREVIEW` располагается рядом с тремя оплаченными наборами, но не включается в оплачиваемые ZIP-архивы.

### Approved watermark treatment v1.1

- Use five repeated transparent lockups per image.
- Each lockup contains the monogram incision, ONYX, and PRIVATE PREVIEW with the order ID handled by the delivery manifest.
- One lockup may lightly cross the face so the mark cannot be removed by a simple crop.
- No opaque panel, black badge, or high-contrast central banner is allowed.


````

## 13 Production/Client_Delivery/ONYX_CLIENT_DELIVERY_SOP_V1.md

````text
# ONYX Client Delivery SOP v1

## Source

Use only an approved production package. Never modify files under `09 Experiments`. The package must contain ten approved master PNGs after upscale and a completed visual QA record.

## Build

For a new package, run `engine/production/onyx_production_pipeline.py`. It first stages the approved source-resolution JPEGs, runs the configured ComfyUI postprocessor to create the full-resolution PNG masters, and then runs `onyx_delivery.py` to create the client package. Re-running the delivery script alone is appropriate when the masters already exist.

Run `engine/production/onyx_delivery.py` with the package directory and the approved Cormorant font. The process creates four delivery folders:

- `00_PREPAYMENT_PREVIEW`: reduced proofs used only before payment;
- `01_LIGHT_JPEG`: paid lightweight delivery;
- `02_HIGH_QUALITY_JPEG`: paid high-quality JPEG delivery;
- `03_FULL_RESOLUTION_PNG`: paid delivery containing the ten original upscale PNG masters at maximum resolution.

Client-facing files are named `ONYX_01` through `ONYX_10`; internal character identifiers are not exposed in filenames. The script also creates `README.txt`, `ONYX_<ORDER>_LIGHT.zip`, `ONYX_<ORDER>_FULL.zip`, and `CLIENT_DELIVERY_MANIFEST_V1.json` with source master paths, copied full-resolution paths and SHA-256 values.

The prepayment footer uses `BUSINESS COLLECTION / CLIENT PREVIEW`. `PORTFOLIO PREVIEW` is reserved for public portfolio assets and must never appear in client proof files.

## Sending policy

Before payment, send only `00_PREPAYMENT_PREVIEW`. After payment, send either the compact LIGHT archive or the complete FULL archive. Paid files contain no watermark. The client may use the lightweight set for messaging and social media, the high-quality JPEG set for everyday use, and the full-resolution PNG set for print, retouching and archive storage.

## QA gate

Check that every delivery folder contains ten images, filenames and roles match the portfolio manifest, full-resolution checksums match their source masters, previews carry the correct order ID, paid files have no watermark, and the manifest is present. Do not publish or deliver while owner final approval is pending.


````

## 13 Production/Client_Delivery/Templates/README.md

````text
# Client Delivery Template

For an approved paid order, prepare only the ten final files named `ONYX_01.jpg` through `ONYX_10.jpg`. Final paid delivery contains no watermark. Source, intermediate, rejected, repaired and preview assets stay outside the delivery package and retain their manifest provenance.

````

## 13 Production/Client_Experience/Intake/README.md

````text
# ONYX Client Intake Pack v1

Этот пакет помогает собрать только ту информацию, которая влияет на результат съёмки. Его можно отправить клиенту как набор документов или перенести поля в форму.

## Состав

```text
Intake/
├── README.md
├── ONYX_REFERENCE_GUIDE_v1.md
├── ONYX_SIGNATURE_INTAKE_v1.md
├── ONYX_BOUDOIR_SIGNATURE_INTAKE_v1.md
├── ONYX_PREMIUM_CREATIVE_PROFILE_v1.md
├── ONYX_CONSENT_AND_PRIVACY_v1.md
├── ONYX_REFERENCE_QA_STANDARD_v1.md
└── schemas/
    ├── intake_v1.schema.yaml
    ├── example_preview.yaml
    ├── example_signature.yaml
    └── example_premium.yaml
```

## Как использовать

1. Отправьте каждому клиенту [руководство по фотографиям](ONYX_REFERENCE_GUIDE_v1.md) и [согласия](ONYX_CONSENT_AND_PRIVACY_v1.md).
2. Для **Preview** соберите только короткий набор полей из схемы: имя для отображения, номер заказа или контакт, выбранную коллекцию, назначение, стиль, референсы, пожелания и согласия.
3. Для **Signature** заполните [короткую анкету](ONYX_SIGNATURE_INTAKE_v1.md). Для **Boudoir** дополнительно заполните [Boudoir Signature intake](ONYX_BOUDOIR_SIGNATURE_INTAKE_v1.md); все Boudoir-specific поля и согласия обязательны.
   Для коллекции **Boudoir** дополнительно обязательны поля из [Boudoir Signature intake](ONYX_BOUDOIR_SIGNATURE_INTAKE_v1.md), включая границы образа, возраст и отдельные согласия.
4. Для **Premium** заполните [Creative Profile](ONYX_PREMIUM_CREATIVE_PROFILE_v1.md), затем перенесите согласованный профиль в Concept Card. До массового производства концепция должна быть одобрена.
5. Внутренний специалист проверяет референсы по [стандарту QA](ONYX_REFERENCE_QA_STANDARD_v1.md) и фиксирует результат в поле `reference_qa_status`.

## Signature и Premium

| Уровень | Что заполняет клиент | Зачем |
|---|---|---|
| Signature | Короткая анкета: цель, стиль, важные особенности внешности, одежда и то, чего следует избегать. | Получить точный и естественный результат без длинного брифа. |
| Premium | Creative Profile: образ, приоритеты, среда, гардероб, настроение и индивидуальные пожелания. | Согласовать творческое направление до подготовки Concept Card. |

Вопросы должны касаться только результата. Не просите клиента описывать себя сверх того, что поможет создать его образ.

## Язык и границы

Клиентские документы написаны простым, спокойным языком: без технических терминов, медицинских оценок и обещаний, которых нет в сервисе. Примеры в `schemas/` демонстрационные и не содержат реальных данных.

## Машиночитаемый формат

[Схема intake_v1.2](schemas/intake_v1.schema.yaml) описывает канонические поля, подписи, типы, обязательность и контролируемые значения. Boudoir-specific поля обязательны для `collection: BOUDOIR`; они являются источником для формы, ручного заполнения и передачи данных в производство. Примеры показывают минимально достаточное заполнение для каждого продукта.

````

## 13 Production/Client_Experience/Intake/schemas/intake_v1.schema.yaml

````text
schema_version: "1.2"
schema_id: onyx_client_intake_v1_1
title: ONYX Client Intake v1.2
description: >-
  Каноническая машиночитаемая структура для Preview, Signature и Premium.
  Boudoir-specific поля обязательны только для коллекции BOUDOIR.
  Это описательная YAML-схема для форм и производства, а не JSON Schema.
controlled_values:
  product: [PREVIEW, SIGNATURE, PREMIUM]
  style_intensity: [NATURAL, POLISHED, GLAMOUR]
  portfolio_consent: [GRANTED, DENIED, NOT_ASKED]
  marketing_consent: [GRANTED, DENIED, NOT_ASKED]
  service_processing_consent: [GRANTED, DENIED]
  reference_reuse_consent: [GRANTED, DENIED]
  adult_confirmation: [CONFIRMED_18_PLUS, NOT_CONFIRMED]
  portfolio_use_consent: [GRANTED, NOT_GRANTED, NOT_ASKED]
  sensuality_level: [NATURAL, SUBTLE, ELEVATED, MAX_NON_EXPLICIT]
  clothing_level: [FULL_COVERAGE, MODERATE, MINIMAL]
  preferred_coverage: [FULL_COVERAGE, IMPLIED_TASTEFUL, OTHER]
  reference_qa_status: [PASS, PASS_WITH_NOTES, NEEDS_MORE_REFERENCES, REJECT]
  reference_check: [PASS, WARN, FAIL, N_A]
  clothing_style: [BUSINESS_FORMAL, SMART_CASUAL, CASUAL, FASHION, OTHER]
  body_adjustment_intent: [NO_INTENTIONAL_ADJUSTMENT, LIGHT_FLATTERING_CORRECTION, POLISHED_SILHOUETTE, INDIVIDUAL_REQUEST]
  personal_image_trait: [confident, approachable, elegant, modern, creative, authoritative, relaxed, sophisticated, energetic, minimal, editorial, other]
  environment: [modern_office, architecture, hotel_lounge, city, studio, home_lifestyle, travel, nature, editorial, other]
  production_priority: [MAX_LIKENESS, PROFESSIONAL, ATTRACTIVENESS, REALISM, DIVERSITY, SOCIAL_PRESENCE]
fields:
  order:
    - canonical: order_id
      label_ru: Идентификатор заказа
      description_ru: Внутренний стабильный идентификатор заказа.
      type: string
      required: true
    - canonical: product
      label_ru: Продукт
      description_ru: Выбранный уровень ONYX.
      type: enum
      allowed_values_ref: product
      required: true
    - canonical: client_display_name
      label_ru: Имя для отображения
      description_ru: Как обращаться к клиенту в материалах заказа.
      type: string
      required: true
    - canonical: order_reference
      label_ru: Номер заказа или контакт
      description_ru: Ссылка на заказ или канал связи.
      type: string
      required: true
    - canonical: selected_collection
      label_ru: Выбранная коллекция
      description_ru: Название согласованной коллекции.
      type: string
      required: true
  references:
    - canonical: reference_items
      label_ru: Референсы
      description_ru: Идентификаторы приложенных кадров и краткая роль каждого.
      type: array_of_objects
      item_fields: [reference_id, role, notes]
      required: true
    - canonical: reference_qa_status
      label_ru: Статус проверки референсов
      description_ru: Итог внутренней проверки до производства; null до получения референсов и запуска QA.
      type: enum
      allowed_values_ref: reference_qa_status
      required: true
      nullable: true
    - canonical: reference_qa_checks
      label_ru: Проверки референсов
      description_ru: Результаты контрольного списка внутренней проверки.
      type: object
      allowed_values_ref: reference_check
      required: false
    - canonical: reference_qa_notes
      label_ru: Заметки по референсам
      description_ru: Ограничения или запрос недостающих кадров.
      type: string
      required: false
  appearance:
    - canonical: must_keep
      label_ru: Что важно сохранить
      description_ru: Важные элементы внешности и привычного образа.
      type: array_of_strings
      required_for_products: [PREVIEW, SIGNATURE, PREMIUM]
    - canonical: glasses_status
      label_ru: Очки
      description_ru: Нужно ли учитывать очки как часть образа.
      type: string
      required: false
    - canonical: body_type
      label_ru: Предпочтения по телосложению
      description_ru: Нейтральное описание естественного телосложения клиента для сохранения узнаваемости и пропорций.
      type: string
      required: false
    - canonical: body_adjustment_intent
      label_ru: Подход к силуэту
      description_ru: Нейтральное пожелание о работе с силуэтом.
      type: enum
      allowed_values_ref: body_adjustment_intent
      required_for_products: [PREMIUM]
    - canonical: body_adjustment_note
      label_ru: Индивидуальное пожелание о силуэте
      description_ru: Заполняется только при необходимости.
      type: string
      required: false
  preferences:
    - canonical: primary_use
      label_ru: Цель фотосессии
      description_ru: Назначение и случаи использования фотографий в одном ответе.
      type: string
      required: true
    - canonical: use_places
      label_ru: Места использования (Premium)
      description_ru: Дополнительный контекст о каналах и площадках только для Premium Creative Profile.
      type: array_of_strings
      required_for_products: [PREMIUM]
    - canonical: desired_style
      label_ru: Желаемый стиль
      description_ru: Короткое описание образа словами клиента.
      type: string
      required_for_products: [PREVIEW, SIGNATURE, PREMIUM]
    - canonical: style_intensity
      label_ru: Выразительность стиля
      description_ru: Выбранная степень стилизации.
      type: enum
      allowed_values_ref: style_intensity
      required_for_products: [SIGNATURE, PREMIUM]
    - canonical: clothing_style
      label_ru: Стиль одежды
      description_ru: Общая формальность одежды.
      type: enum
      allowed_values_ref: clothing_style
      required: false
    - canonical: wardrobe_preferences
      label_ru: Предпочтения по одежде
      description_ru: Одежда, фактуры, цвета и детали.
      type: array_of_strings
      required_for_products: [PREMIUM]
    - canonical: must_avoid
      label_ru: Чего избегать
      description_ru: Нежелательные вещи, цвета, степень формальности, ретушь или места.
      type: array_of_strings
      required_for_products: [PREVIEW, SIGNATURE, PREMIUM]
      required_for_collections: [BOUDOIR]
    - canonical: client_note
      label_ru: Заметка клиента
      description_ru: Короткий дополнительный контекст.
      type: string
      required: false
  premium:
    - canonical: personal_image_traits
      label_ru: Качества желаемого образа
      description_ru: Слова, описывающие впечатление от образа.
      type: array_of_enums
      allowed_values_ref: personal_image_trait
      required_for_products: [PREMIUM]
    - canonical: environment_preferences
      label_ru: Предпочтительные среды
      description_ru: Места и типы окружения.
      type: array_of_enums
      allowed_values_ref: environment
      required_for_products: [PREMIUM]
    - canonical: production_priorities
      label_ru: Приоритеты результата
      description_ru: Что важнее всего для клиента.
      type: array_of_enums
      allowed_values_ref: production_priority
      required_for_products: [PREMIUM]
    - canonical: inspirations
      label_ru: Вдохновение
      description_ru: Необязательное словесное описание настроения или примеров.
      type: array_of_strings
      required: false
    - canonical: concept_card_status
      label_ru: Статус Concept Card
      description_ru: Для Premium: DRAFT, PENDING_APPROVAL или APPROVED до массового производства.
      type: enum
      allowed_values: [DRAFT, PENDING_APPROVAL, APPROVED]
      required_for_products: [PREMIUM]
  boudoir:
    - canonical: sensuality_level
      label_ru: Уровень чувственности
      description_ru: Желаемая выразительность чувственного образа; Boudoir only.
      type: enum
      allowed_values_ref: sensuality_level
      required_for_collections: [BOUDOIR]
    - canonical: preferred_wardrobe_types
      label_ru: Предпочтительные варианты одежды
      description_ru: Выберите подходящие варианты гардероба для Boudoir.
      type: array_of_strings
      required_for_collections: [BOUDOIR]
    - canonical: preferred_coverage
      label_ru: Желаемая степень закрытости
      description_ru: Границы открытости образа; explicit nudity is not produced.
      type: enum
      allowed_values_ref: preferred_coverage
      required_for_collections: [BOUDOIR]
    - canonical: clothing_level
      label_ru: Уровень закрытости одежды
      description_ru: Предпочитаемое количество одежды в рамках non-explicit границ.
      type: enum
      allowed_values_ref: clothing_level
      required_for_collections: [BOUDOIR]
    - canonical: lingerie_allowed
      label_ru: Допустимо бельё
      description_ru: Разрешение на бельевые образы в согласованных non-explicit сценах.
      type: boolean
      required_for_collections: [BOUDOIR]
    - canonical: bodysuit_allowed
      label_ru: Допустимо боди
      type: boolean
      required_for_collections: [BOUDOIR]
    - canonical: silk_robe_allowed
      label_ru: Допустим шёлковый халат
      type: boolean
      required_for_collections: [BOUDOIR]
    - canonical: sheer_layers_allowed
      label_ru: Допустимы прозрачные слои
      description_ru: Только как слой с обязательным стратегическим прикрытием.
      type: boolean
      required_for_collections: [BOUDOIR]
    - canonical: implied_nudity_allowed
      label_ru: Допустима имитация наготы
      description_ru: Только implied framing со стратегическим прикрытием; фактической наготы нет.
      type: boolean
      required_for_collections: [BOUDOIR]
    - canonical: strategic_coverage_required
      label_ru: Требуется стратегическое прикрытие
      type: boolean
      required_for_collections: [BOUDOIR]
    - canonical: explicit_nudity
      label_ru: Разрешена явная нагота
      description_ru: ONYX Boudoir production boundary; должно быть false.
      type: boolean
      allowed_values: [false]
      required_for_collections: [BOUDOIR]
    - canonical: sexual_activity
      label_ru: Разрешена сексуальная активность
      description_ru: ONYX Boudoir production boundary; должно быть false.
      type: boolean
      allowed_values: [false]
      required_for_collections: [BOUDOIR]
    - canonical: oversized_shirt_limit
      label_ru: Ограничение образа с объёмной рубашкой
      description_ru: Для этого заказа — не более одной сцены и не доминирующее направление гардероба.
      type: string
      required_for_collections: [BOUDOIR]
    - canonical: mood
      label_ru: Настроение коллекции
      description_ru: Желаемое эмоциональное впечатление.
      type: array_of_strings
      required_for_collections: [BOUDOIR]
    - canonical: lighting_preference
      label_ru: Предпочтительный свет
      description_ru: Тип света и атмосферы.
      type: array_of_strings
      required_for_collections: [BOUDOIR]
    - canonical: intended_use
      label_ru: Назначение коллекции
      description_ru: Где и как клиент планирует использовать изображения.
      type: string
      required_for_collections: [BOUDOIR]
    - canonical: adult_confirmation
      label_ru: Подтверждение возраста 18+
      description_ru: Required for Boudoir; production only after CONFIRMED_18_PLUS.
      type: enum
      allowed_values_ref: adult_confirmation
      required_for_collections: [BOUDOIR]
    - canonical: reference_reuse_consent
      label_ru: Согласие на повторное использование референсов
      description_ru: Separate consent for reusing references from another order.
      type: enum
      allowed_values_ref: reference_reuse_consent
      required_for_collections: [BOUDOIR]
    - canonical: portfolio_use_consent
      label_ru: Согласие на использование в портфолио
      description_ru: Separate optional consent; NOT_GRANTED is the privacy-preserving default.
      type: enum
      allowed_values_ref: portfolio_use_consent
      default: NOT_GRANTED
      required_for_collections: [BOUDOIR]
  consent:
    - canonical: service_processing_consent
      label_ru: Согласие на выполнение заказа
      description_ru: Право передать материалы и обработать их для выполнения заказа.
      type: enum
      allowed_values_ref: service_processing_consent
      required: true
      nullable: true
    - canonical: portfolio_consent
      label_ru: Согласие на портфолио
      description_ru: Публикация возможна только при GRANTED; значение по умолчанию DENIED.
      type: enum
      allowed_values_ref: portfolio_consent
      default: DENIED
      required: true
      nullable: true
    - canonical: marketing_consent
      label_ru: Согласие на маркетинговые материалы
      description_ru: Независимо от согласия на портфолио.
      type: enum
      allowed_values_ref: marketing_consent
      default: NOT_ASKED
      required: true
      nullable: true
  metadata:
    - canonical: intake_version
      label_ru: Версия intake
      description_ru: Версия структуры заполнения.
      type: string
      required: true
    - canonical: submitted_at
      label_ru: Время заполнения
      description_ru: ISO 8601 timestamp.
      type: datetime
      required: true
    - canonical: intake_owner
      label_ru: Ответственный за intake
      description_ru: Внутренний идентификатор сотрудника или роли.
      type: string
      required: true

````

## 13 Production/Client_Experience/Intake/schemas/example_preview.yaml

````text
intake_version: "1.0"
order:
  order_id: DEMO-PREVIEW-001
  product: PREVIEW
  client_display_name: Демо-клиент
  order_reference: DEMO-CONTACT-001
  selected_collection: Business
references:
  reference_items:
    - reference_id: DEMO_REF_01
      role: front
      notes: Недавний портрет при мягком дневном свете.
    - reference_id: DEMO_REF_02
      role: three_quarter
      notes: Ракурс три четверти.
  reference_qa_status: PASS
  reference_qa_checks:
    face_visibility: PASS
    identity_consistency: PASS
    currentness: PASS
    angle_variety: PASS
    filter_status: PASS
    image_quality: PASS
    facial_hair_status: N_A
    hairstyle_status: PASS
    glasses_status: PASS
    body_information: N_A
    preference_conflicts: PASS
appearance:
  must_keep: [Короткая стрижка, Очки]
  glasses_status: Очки оставить частью образа.
preferences:
  primary_use: Профессиональный профиль
  use_places: [Сайт компании, Социальные сети]
  desired_style: Современно и спокойно.
  must_avoid: [Яркие принты, Слишком формальный костюм]
consent:
  service_processing_consent: GRANTED
  portfolio_consent: DENIED
  marketing_consent: NOT_ASKED
metadata:
  intake_version: "1.0"
  submitted_at: "2026-09-18T10:00:00+03:00"
  intake_owner: DEMO_INTAKE_OWNER

````

## 13 Production/Client_Experience/Intake/ONYX_PREMIUM_CREATIVE_PROFILE_v1.md

````text
# ONYX Premium — Creative Profile

Этот профиль помогает собрать ваш образ в одну ясную творческую идею. Отвечайте только на те вопросы, которые помогут получить желаемый результат.

## 1. Цель и образ

- **Цель и места использования:** `primary_use`, `use_places`
- **Каким вы хотите выглядеть:** `personal_image_traits`

Выберите подходящие слова или добавьте свой вариант: `confident`, `approachable`, `elegant`, `modern`, `creative`, `authoritative`, `relaxed`, `sophisticated`, `energetic`, `minimal`, `editorial`, `other`.

- **Насколько выразительным должен быть стиль:** `style_intensity`
  - `NATURAL` — естественно и спокойно;
  - `POLISHED` — собранно и выразительно;
  - `GLAMOUR` — заметно и стилизованно.

## 2. Одежда и среда

- **Одежда, фактуры, цвета, формальность:** `wardrobe_preferences`
- **Подходящие места:** `environment_preferences`

Варианты среды: `modern_office`, `architecture`, `hotel_lounge`, `city`, `studio`, `home_lifestyle`, `travel`, `nature`, `editorial`, `other`.

## 3. Пропорции и естественность

Выберите, как работать с силуэтом: `body_adjustment_intent`.

| Вариант | Описание |
|---|---|
| `NO_INTENTIONAL_ADJUSTMENT` | Сохранять привычное восприятие фигуры. |
| `LIGHT_FLATTERING_CORRECTION` | Деликатно выбирать позу, свет и ракурс. |
| `POLISHED_SILHOUETTE` | Стремиться к более собранному визуальному силуэту. |
| `INDIVIDUAL_REQUEST` | Учесть ваше описание ниже. |

- **Индивидуальное пожелание, если есть:** `body_adjustment_note`

## 4. Приоритеты и ограничения

Выберите главное: `production_priorities` — `MAX_LIKENESS`, `PROFESSIONAL`, `ATTRACTIVENESS`, `REALISM`, `DIVERSITY`, `SOCIAL_PRESENCE`.

- **Чего избегать:** `must_avoid`
- **Вдохновение или примеры настроения:** `inspirations` — можно описать словами, ссылку добавлять не обязательно.
- **Свободная заметка:** `client_note`

## Что происходит дальше

Команда переносит согласованный профиль в Concept Card: цель — в назначение, качества образа и стиль — в визуальное направление, одежду — в образы, среду — в сцены, а приоритеты и ограничения — в правила производства. Concept Card согласуется до начала массового производства.

````

## 13 Production/Client_Experience/Intake/ONYX_REFERENCE_QA_STANDARD_v1.md

````text
# ONYX Reference QA Standard v1

Внутренний стандарт проверки референсов до передачи заказа в производство. Не является клиентским документом.

## Итоговые статусы

| Статус | Когда ставить | Следующее действие |
|---|---|---|
| `PASS` | Референсы дают достаточное и непротиворечивое представление о внешности для выбранного заказа. | Передать в производство. |
| `PASS_WITH_NOTES` | Материала достаточно, но есть ограничения или детали, которые нужно явно учесть. | Передать в производство вместе с заметками. |
| `NEEDS_MORE_REFERENCES` | Главных данных не хватает, но запрос можно закрыть дополнительными фото. | Попросить конкретные недостающие кадры. |
| `REJECT` | Материалы нельзя использовать: нет права на передачу, данные противоречивы или качество не позволяет установить внешность. | Остановить intake и объяснить, что нужно заменить. |

## Чек-лист

Для каждого пункта укажите одно из значений: `PASS`, `WARN`, `FAIL`, `N_A`.

| Проверка | Что проверяется |
|---|---|
| `face_visibility` | Лицо хорошо видно хотя бы на части кадров. |
| `identity_consistency` | На фотографиях один и тот же человек, без существенных противоречий. |
| `currentness` | Внешность соответствует текущему образу клиента. |
| `angle_variety` | Есть анфас и полезные разные ракурсы. |
| `filter_status` | Нет фильтров или ретуши, скрывающих важные черты. |
| `image_quality` | Кадры достаточно резкие и светлые для проверки. |
| `facial_hair_status` | Понятно наличие или отсутствие бороды и усов, если это применимо. |
| `hairstyle_status` | Понятны причёска, длина и цвет волос. |
| `glasses_status` | Понятно, являются ли очки частью желаемого образа. |
| `body_information` | Есть информация о фигуре, когда она нужна для выбранной коллекции. |
| `preference_conflicts` | Нет конфликтов между референсами, `must_keep`, `must_avoid` и стилем. |

## Правило решения

- `REJECT`: есть критическое нарушение права на передачу материалов или `FAIL` в `identity_consistency`.
- `NEEDS_MORE_REFERENCES`: есть `FAIL` в видимости лица, актуальности, качестве или необходимой информации о фигуре; либо отсутствуют необходимые ракурсы.
- `PASS_WITH_NOTES`: нет блокирующих `FAIL`, но есть `WARN` или ограничения, важные для производства.
- `PASS`: все применимые проверки имеют `PASS`.

Фиксируйте итог, дату проверки, идентификатор проверяющего, список использованных референсов и конкретные заметки. Не записывайте лишние личные сведения.

````

## 03 Product/Product.md

````text
# Product

## Назначение

ONYX — это бренд премиальных AI-фотосессий.

Мы не продаем генерацию изображений или работу с нейросетями. Мы предлагаем готовые продукты, каждый из которых решает конкретную задачу клиента.

Каждый продукт создается по единому стандарту качества ONYX и использует ONYX Method.

Главное отличие продуктов заключается не в технологии генерации, а в сценарии использования, художественной концепции и составе коллекций.

---

# Продуктовая линейка

## ONYX Essential

Базовый продукт.

Предназначен для быстрого получения качественных персональных портретов.

Подходит для:

- аватаров;
- социальных сетей;
- резюме;
- первых профессиональных фотографий.

---

## ONYX Signature

Флагманский продукт ONYX.

Универсальная персональная фотосессия, подходящая большинству клиентов.

Включает разнообразные деловые, городские и повседневные образы.

Используется для:

- личного бренда;
- социальных сетей;
- профессионального позиционирования;
- повседневного использования.

---

## ONYX Executive

Премиальный продукт для руководителей, предпринимателей и публичных экспертов.

Особенности:

- статусные интерьеры;
- дорогие материалы;
- премиальная атмосфера;
- уверенный деловой стиль.

Главная задача — подчеркнуть профессиональный статус клиента.

---

## ONYX Lifestyle

Продукт, отражающий образ жизни человека.

Используется для создания естественных фотографий вне рабочего контекста.

Основные направления:

- путешествия;
- отдых;
- городская жизнь;
- спорт;
- хобби.

---

## ONYX Dating

Продукт для сервисов знакомств.

Главная цель — показать человека максимально естественным, привлекательным и открытым.

Особое внимание уделяется эмоциям, разнообразию ситуаций и живым фотографиям.

---

## ONYX Family

Семейные фотосессии.

Позволяет создавать теплые семейные изображения без организации традиционной съемки.

---

## ONYX Fantasy

Творческие художественные проекты.

Позволяет создавать необычные образы, вдохновленные кино, историей, фэнтези и научной фантастикой.

---

## ONYX Custom

Индивидуальный продукт.

Создается специально под нестандартную задачу клиента и может объединять элементы нескольких продуктов.

---

# Общие принципы

Каждый продукт ONYX:

- сохраняет личность клиента;
- использует единый стандарт качества;
- включает несколько тематических коллекций;
- формирует полноценную фотосессию, а не набор случайных изображений;
- может расширяться новыми коллекциями без изменения своей концепции.

---

## Связанные документы

- [[Mission]]
- [[Vision]]
- [[ONYX Method]]
- [[Collections]]
````

## 03 Product/Collections.md

````text
# Collections

## Назначение

Каждый продукт ONYX состоит из набора тематических коллекций.

Коллекция — это группа сцен, объединенных общей идеей, стилем, атмосферой и назначением.

Коллекции позволяют постоянно расширять возможности продукта, не создавая новые продукты для каждой новой идеи.

---

# Структура

Архитектура ONYX имеет три уровня.

```
Продукт
    ↓
Коллекция
    ↓
Сцены
```

Например:

```
ONYX Signature
    ↓
Modern Office
    ↓
Office 01
Office 02
Office 03
...
```

---

# Коллекции ONYX Signature

Деловые пространства

- Modern Office
- Executive Office
- Glass Business Center
- Conference Room
- Boardroom
- Creative Workspace
- Coffee Meeting
- Corporate Portrait

---

# Коллекции ONYX Executive

Премиальные пространства

- CEO Office
- Luxury Office
- Skyline Office
- Private Library
- Financial District
- Premium Lounge
- Executive Meeting
- Black Interior

---

# Коллекции ONYX Lifestyle

Образ жизни

- City Walk
- Café
- Mountains
- Beach
- Yacht
- Resort
- Travel
- Weekend
- Gym
- Running

---

# Коллекции ONYX Dating

Естественные жизненные ситуации

- First Date
- Restaurant
- Sunset Walk
- City Evening
- Coffee Shop
- Weekend Trip
- Park
- Rooftop

---

# Коллекции ONYX Family

Семейная жизнь

- Home
- Park
- Picnic
- Holiday
- Christmas
- Vacation
- Children's Playground

---

# Коллекции ONYX Fantasy

Художественные проекты

- Cyberpunk
- Medieval
- Viking
- Samurai
- Space Explorer
- Film Noir
- Ancient Empire
- Magic Forest

---

# Сцены

Каждая коллекция включает множество отдельных сцен.

Например:

```
Modern Office

├── Office 01
├── Office 02
├── Office 03
├── Office 04
├── Office 05
└── ...
```

Все сцены одной коллекции сохраняют единый художественный стиль и могут свободно комбинироваться в рамках одной фотосессии.

---

# Принципы развития

При добавлении новой коллекции необходимо соблюдать следующие правила:

- коллекция должна соответствовать одному из существующих продуктов;
- иметь четкую художественную концепцию;
- содержать достаточное разнообразие сцен;
- расширять возможности продукта, а не дублировать существующие коллекции.

---

## Связанные документы

- [[Product]]
- [[ONYX Method]]
````

## 13 Production/Templates/Collection_Book/README.md

````text
# ONYX Collection Book renderer

Local ReportLab + Pillow + pypdf + Poppler. No service, model, GPU, network, global installation or existing delivery-pipeline changes.

From repository root, with those dependencies installed:

```powershell
python "13 Production/Templates/Collection_Book/render_collection_book.py" --data "13 Production/Templates/Collection_Book/example_data/P02_BUSINESS_COLLECTION_BOOK_v1.json" --output "13 Production/Samples/P02_Business_Collection_Book_v1_rebuild"
```

On this workstation replace `python` with `& 'C:/Users/ME/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'`. `pdftoppm` is on PATH; otherwise pass `--poppler` with its executable path. No extra dependencies were installed.

```powershell
python "13 Production/Templates/Collection_Book/test_renderer.py"
```

Planner/privacy unit checks cover 1, 10 and 20 photos. The actual P02 Signature book additionally passes end-to-end PDF rendering checks. Previews are 1350 px JPEGs rendered directly from the PDF. Premium/Preview PDF output has not been visually certified.

See [data contract](ONYX_COLLECTION_BOOK_TEMPLATE.md), [production guide](COLLECTION_BOOK_PRODUCTION_GUIDE.md), [standard](../../Product_Standards/ONYX_COLLECTION_BOOK_STANDARD.md), and [sample](../../Samples/P02_Business_Collection_Book_v1/README.md). Do not send internal manifests, source_data or reports to clients.

````

## 13 Production/Templates/Collection_Book/ONYX_COLLECTION_BOOK_TEMPLATE.md

````text
# Collection Book template specification v1

Status: approved RU editorial reference template. Client-specific copy and asset approval remain required.

JSON data is separate from `template/style.json` and Python layout. Paths resolve against repository root (override `--root`). No P02 identifier is embedded in the renderer.

| Field | Contract |
| --- | --- |
| order_id | Internal manifest only |
| client_display_name | Cover name; empty allowed for sample |
| collection_name, collection_subtitle | Public cover copy |
| cover_image, hero_image | Paths belonging to photos; hero must be first photo |
| photos | Ordered array implementing photo_01 … photo_N; entries path, sha256, caption |
| product_tier | Preview=1, Signature=10, Premium=20 |
| onyx_mission_heading, onyx_mission_text | Opening note from ONYX: mission, approach and thanks; no personal greeting |
| collection_description, collection_use_cases | Short paragraph and up to three short use-case lines |
| onyx_selection_image, onyx_selection_note | Collection image path and public rationale |
| personal_closing_note, closing_heading | Personalized closing copy, grounded in approved persona or client brief |
| next_collections | One or two objects implementing next_collection_01 … next_collection_N |
| next_collections[].name, description | Verified product copy |
| next_collections[].status | available or coming_soon |
| next_collections[].collection_url | Explicit HTTPS URL or null; alias for next_collection_01_url |
| next_collections[].qr_url | Reserved next_collection_01_qr_url; must be null in v1 |
| next_collections[].cta_label | Link label when available; coming_soon renders “Скоро” |
| brand_logo | Approved PNG master; placed on dark cover without distortion |
| brand_variant, language | v1 accepts editorial_v1 and ru; other values fail |
| book_version, created_at | Internal version and date |
| output_stem | Internal safe filename stem |
| sample | Shows ONYX SAMPLE COLLECTION instead of client name |
| motion_asset | null or Premium object {url, cta_label}; HTTPS link, no video embedding |

## Layout and constraints

Six structural pages plus story: Preview 7 pages; Signature 15; Premium 16. Signature uses nine story pages, one pair. Premium uses ten pairs. No extra Preview/Premium PDF is supplied with this reference implementation.

All photographs use contain geometry; no crop or filter. Body and heading wrapping checks reject overflow rather than silently truncate or shrink. Long translations and names may require editorial shortening. Maximum two next collections. QR rendering is deliberately unsupported, not silently ignored. External links are neither fetched nor invented.

## Outputs

PDF, internal YAML 1.2 manifest serialized as JSON, copied structured source_data, and one PNG per page rendered by Poppler. Manifest records exact input paths/SHA256, PDF and preview hashes, placements/reuse and renderer/style/font/logo hashes. Source images are never copied to the sample. Only in-memory JPEG derivatives enter the PDF.

Output must not already contain generated book files. Rebuild to a new version directory, preventing accidental overwrite. A failed run may leave diagnostics/partial outputs; use a fresh directory after fixing the input.

## Reproducibility limits

Deterministic PDF metadata via ReportLab invariant mode. Exact bytes also depend on ReportLab/Pillow/font/Poppler versions; preserve those with the QA report. Source approval is external to this template. Historical stale manifests are preserved and reported, not repaired by the renderer.

## Semantic caption contract

Each `photos[]` entry keeps its editable caption with the approved source image. The optional `page_caption` object records the rendered text, scene semantics and editability:

```json
"page_caption": {"text": "Рабочие детали", "source_scene": "work-detail portrait", "editable": true}
```

Captions must describe the actual image and scene role rather than a page-number slot. QA must include `caption matches actual image content` and must be repeated whenever a photo is replaced.

````

## 13 Production/Templates/Collection_Book/COLLECTION_BOOK_PRODUCTION_GUIDE.md

````text
# Collection Book production guide

This guide is the repeatable workflow for producing an ONYX Collection Book from an approved photoshoot. The reference result is the approved P02 Business sample. Keep the renderer and `template/style.json` unchanged unless a new approved design revision is required.

## 1. Prepare a new data file

Copy `example_data/P02_BUSINESS_COLLECTION_BOOK_v1.json` to a new client/order-specific JSON file. Do not edit the P02 sample data.

Fill these items from approved internal records only:

- `client_display_name`, collection name and short cover subtitle;
- product tier and the exact ordered number of unique photographs: Preview 1, Signature 10, Premium 20;
- each photo path and SHA256; preserve the approved story order;
- the cover/hero image, which must be the first story image; and the selected ONYX Selection image;
- ONYX mission note, collection description and practical use cases;
- personal note, based only on the approved client brief or persona boundaries;
- documented next collections, their status and verified HTTPS URLs when available.

Do not add client source photographs to the book folder. The data file references their existing delivery paths and the renderer confirms their hashes before and after the build.

## 2. Write copy for the fixed sequence

The Signature reference has 15 pages in this order:

1. Cover: compact ONYX monogram/wordmark, collection title, concise subtitle and one portrait inside the central Onyx field.
2. `Обращение от ONYX`: a non-personal message about the desired image and self-expression, ending with a thank-you.
3. `О коллекции`: purpose, visual language and use cases.
4. `Личная нота`: name appears in the body, with specific observations and a supportable compliment; it must not repeat page 3.
5–13. Photo story: every ordered photograph exactly once. Cover and Selection may reuse the hero only when logged by the manifest.
14. `ONYX Selection`: one selected image and a concise, image-grounded rationale.
15. `Следующие коллекции` / `Продолжение вашей истории`: verified current or coming-soon collections only.

Use Russian body copy. Collection names and ONYX Selection may remain English. Never invent employment, achievements, review scores, availability, URLs, client biography or photographer attribution. For a fictional sample, label the persona internally and never reuse that copy for a client.

## 3. Page passport: Signature, 10 photographs

All dimensions below are logical units on a 1080 × 1350 canvas. Coordinates use the page’s top-left corner. The footer starts at `y=1120`, is always 230 units high, and is never overlaid on a photograph.

| Page | Fixed structure and geometry | Individual content to fill |
| --- | --- | --- |
| 01 Cover | Stone fields `250 × 1120` at the left and right edges; central Onyx field is 580 wide. Monogram centred at `x=540`, compact wordmark and a 350-unit Champagne rule. Collection title is centred; subtitle is `x=300, y=250, w=480`, 24 pt. Hero portrait is contained, never cropped: `x=262, y=360, w=556, h=740`. | `collection_name`, `collection_subtitle`, `cover_image`. The subtitle should state the collection benefit in one or two short lines. |
| 02 Opening | Light page. Champagne label `Обращение от ONYX`; editorial heading at `x=72, y=210, w=940`, 83 pt; body at `x=76, y=590, w=870`, 35 pt. | `onyx_mission_heading`, `onyx_mission_text`. This page has no personal greeting or biography. |
| 03 Collection | Dark page. Label `О коллекции`; collection name at `x=72, y=210`, 76 pt; description at `x=76, y=380, w=890`, 30 pt. Six use cases form three rows in two columns; body entries are 27 pt with Champagne circular bullets. | `collection_name`, `collection_description`, six `collection_use_cases`. Explain the product and practical uses, never the client’s character. |
| 04 Personal note | Light page. Label `Личная нота`; heading at `x=72, y=230`, 82 pt; body at `x=76, y=580, w=865`, 36 pt. | `closing_heading`, `personal_closing_note`. Name appears in the body. Use approved observations from the client brief; do not duplicate page 3. |
| 05, 09, 13 Hero | Dark/full-photo story page. The photo fills `1080 × 1120` above the footer with contain geometry. | Photos 01, 06 and 10 in the Signature story order. |
| 06, 11 Inset | Light story page. Portrait is `x=150, y=90, w=780, h=930`. | Photos 02 and 08. No extra copy. |
| 07, 12 Caption | Light story page. Portrait is `x=355, y=135, w=653, h=850`; Champagne Cormorant caption is in the left negative space at `x=76, y=480, w=270`, 43 pt. | Photos 03 and 09 plus their short `caption` values. |
| 08 Pair | Light story page. Champagne Cormorant `В рабочем ритме` at `x=72, y=160`, 43 pt. Two images: `x=72` and `x=552`, each `456 × 720` at `y=300`. | Photos 04 and 05. Do not add an underline or extra body copy. |
| 10 Space | Light story page. Uses the same image and caption geometry as a Caption page. | Photo 07 and its `caption`. |
| 14 ONYX Selection | Dark page. Label `ONYX Selection`; image `x=230, y=145, w=780, h=760`; note `x=76, y=945, w=925`, 28 pt. | `onyx_selection_image`, `onyx_selection_note`. The note must explain a visible, practical strength of the image. |
| 15 Continuation | Dark page. Label `Следующие коллекции`; one-line Cormorant title `Продолжение вашей истории` at `x=72, y=185, w=940`, 56 pt. Collection blocks begin at `y=420` and `y=700`; names 54 pt, descriptions 29 pt, status 22 pt. | One or two `next_collections`. Use only a documented collection and verified availability. Do not add imagery unless it belongs to that exact collection and is approved. |

The Preview tier contains page 01, pages 02–04, one hero story page, ONYX Selection and continuation. Premium uses the same structural pages and ten paired story pages; photo planning is generated by `plan()` rather than manually changing the page order.

## 4. What stays fixed and what changes per client

| Fixed across every book | Filled for each client/order |
| --- | --- |
| Page order, page count rule, margins, headline/body fonts, colours, stone treatment, footer geometry and photo-layout sequence for each tier | Client display name, copy, collection, tier, approved photo paths/hashes/order, hero, Selection, captions, personal note and permitted next collections |
| `Обращение от ONYX`, `О коллекции`, `Личная нота`, `ONYX Selection`, `Следующие коллекции`, footer labels and continuation title | The two heading/body fields of page 02, collection description/use cases on page 03, and every field in the data JSON listed in the data contract |
| All source images are placed with contain geometry and pass through unchanged | The brief must confirm that each referenced image is an accepted delivery asset and that personal copy is supported by the brief |

Do not change fixed values merely to accommodate long copy. Edit the copy first. If a genuine design change is needed, version the renderer and record a new approved reference before using it for a client.

## 5. Preserve the approved visual rules

- Canvas is 1080 × 1350, 4:5. Never crop, filter, stretch or overwrite a source image.
- The cover uses symmetrical dark stone side fields and a central Onyx field. The portrait must fit within the central field.
- Light and dark pages use the same 230-unit footer geometry: monogram, Champagne rule, collection lockup, Champagne `ONYX COLLECTION BOOK` and folio. Light pages use the subtle light-stone variation.
- Captions use Champagne Cormorant. The paired-page title `В рабочем ритме` follows the same treatment.
- The continuation title is one Cormorant line; keep the collection blocks directly beneath it. Add collection imagery only when approved images genuinely belong to those collections.

## 6. Build

Run from the repository root into a new output folder:

```powershell
& 'C:/Users/ME/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' '13 Production/Templates/Collection_Book/render_collection_book.py' --data 'path/to/client_book.json' --output '13 Production/Samples/CLIENT_COLLECTION_BOOK_v1'
```

Do not use the sample folder as an output target. The renderer rejects a nonempty output directory to prevent accidental overwrite.

## 7. Verify before delivery

Run the renderer tests, then inspect the PDF and its generated previews:

```powershell
& 'C:/Users/ME/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -m unittest '13 Production/Templates/Collection_Book/test_renderer.py'
```

Confirm all ordered images appear, text is readable at phone scale, pages have the expected count, the PDF is under 15 MiB, captions do not collide with footers, all source hashes remain unchanged and no internal identifiers are visible. Deliver only the PDF. Keep `source_data.json`, manifest, preview and review files internal.

## 7. Semantic photo captions

Photo captions are editorial data, not fixed labels tied only to page numbers or layout slots. Each photo entry should include `caption` and, when traceability is useful, a `page_caption` object:

```json
"page_caption": {
  "text": "Другой ракурс",
  "source_scene": "side-angle portrait",
  "editable": true
}
```

Before every final render, verify `caption matches actual image content` using the approved photograph, scene role, pose, environment and intended use. If a scene is replaced, revisit its caption before rendering; a new image inherits no caption automatically.

````

## 13 Production/Brand/ONYX_BRANDBOOK_CONTENT_V1.md

````text
# ONYX Brandbook Content v1

## Brand promise

ONYX creates a finished personal virtual photoshoot from the client's photographs: a coherent series, professional direction and final processing.

Primary message: **Не одна AI-картинка, а законченная фотосессия.**

## Typography hierarchy

Use Manrope for navigation, descriptions, prices, metadata, buttons and all functional text. Use Cormorant Garamond for one short editorial headline or wordmark accent per composition. Keep body copy in Manrope; never set a full paragraph in the editorial face.

Recommended hierarchy:

- Display: Cormorant Garamond, large, sentence case;
- Section title: Manrope Semibold, uppercase or title case;
- Body: Manrope Regular;
- Metadata and CTA: Manrope Medium, compact tracking.

## Composition

Photography occupies the visual lead. Use generous Warm White or Onyx fields, quiet Stone dividers and Champagne only for restrained emphasis. Leave clear space around the wordmark. A composition should have one dominant photograph, one message and one action.

## Signature stone application

`ONYX Stone Signature` is the approved premium presentation mode: black onyx stone and silk with the luminous metallic-gold monogram and wordmark. Use it on covers, title slides, presentations, premium dark banners and selected collage fields. Keep body copy in a separate field. Use flat logo masters for small sizes, watermarks, functional layouts and light backgrounds.

## Watermark applications

Portfolio cards use the approved editorial wordmark in a dedicated lower field. Prepayment proofs use the five repeated transparent `ONYX / PRIVATE PREVIEW / ORDER <ID>` marks, including one light overlap with the face. Paid files are always clean. Never place a plain white `ONYX` caption directly on a photograph.

## Product communication

Say “персональная виртуальная фотосессия”, “10 фотографий”, “сохранение внешности”, “профессиональная постановка” and “финальная обработка”. Avoid “AI art”, “генерация картинок” and claims of guaranteed perfection.

## Delivery tiers

Before payment: `00_PREPAYMENT_PREVIEW` with the approved `CLIENT PREVIEW` footer and five protective marks. After payment: `01_LIGHT_JPEG`, `02_HIGH_QUALITY_JPEG` and `03_FULL_RESOLUTION_PNG`. Paid files are clean and contain no watermark.


````

## 13 Production/Brand/ONYX_BRAND_SYSTEM.md

````text
# ONYX Brand System

**Version:** 1.0  
**Date:** 2026-09-16  
**Status:** ACTIVE / Production Standard

## Brand

- **Name:** ONYX
- **Category descriptor:** Virtual Photography
- **RU descriptor:** Персональные виртуальные фотосессии

## Positioning

ONYX создаёт персональные виртуальные фотосессии по фотографиям клиента с сохранением внешности, профессиональной постановкой серии и финальной обработкой.

**Core product message:** Не одна AI-картинка, а законченная фотосессия.

## Visual system

| Token | Value | Intended use |
| --- | --- | --- |
| Onyx | `#111111` | Primary text and dark field |
| Carbon | `#242424` | Secondary dark field |
| Warm White | `#F6F4EF` | Primary light field |
| Stone | `#D8D3CA` | Dividers and quiet surfaces |
| Graphite | `#77736D` | Supporting text |
| Champagne | `#B5A079` | Restrained accent |

- **Primary typeface:** Manrope
- **Editorial accent:** Cormorant Garamond
- **Style:** premium photography / editorial; minimal; photography-first.
- Do not use AI-purple gradients, neural-network motifs, robots, magic wands or camera-cliché icons.

## ONYX Stone Signature

The approved premium presentation treatment combines the black ONYX stone-and-silk background with a luminous metallic-gold monogram and wordmark. This is a controlled signature application, not a replacement for the flat logo masters.

- Controlled artwork: `Brand/Logo/Presentations/ONYX_MONOGRAM_ONYX_SILK_PRESENTATION_V1.png`.
- Use on brandbook covers, title slides, presentations, premium dark banners and selected collage fields.
- Keep the gold warm and restrained; the glow supports the metallic form and must not become a neon effect.
- Preserve the original artwork proportions and crop only through dark background areas. Never crop the monogram or wordmark.
- Do not use the luminous treatment in watermarks, small functional captions, paid client photographs or on light backgrounds. Use the flat approved SVG/PNG artwork in those cases.

## Watermarks

| Use | Mark | Rule |
| --- | --- | --- |
| Portfolio preview | `ONYX Editorial Wordmark v1` | In a dedicated lower editorial field; never over the photograph |
| Client pre-payment proof | `ONYX` + `PRIVATE PREVIEW / ORDER <ID>` | Five restrained transparent overlays across the image body |
| Paid final client delivery | none | No watermark or frame |

Controlled artwork: `Brand/Logo/ONYX_WORDMARK_EDITORIAL_V1_CHAMPAGNE.png`. The approved portfolio application is a branded frame, not an overlaid caption. Client proof overlays are only for pre-payment previews. This standard does not authorize changing canonical experimental images.


````

## 13 Production/Brand/Logo/EDITORIAL_WORDMARK_V1.md

````text
# ONYX Editorial Wordmark v1

**Status:** APPROVED DIRECTION — 2026-09-16

Selected direction: `01 Editorial`. The lockup uses Cormorant Garamond for `ONYX` and a restrained Sans-serif descriptor. Champagne is an accent on Onyx; use the inverse version only on dark fields.

## Approved applications

- Portfolio previews use the lockup in a dedicated lower editorial field. Do not put it over a face or other focal detail.
- Covers, title slides, presentations and selected collage fields may use the controlled `ONYX Stone Signature` artwork: black stone-and-silk background with a luminous metallic-gold logo.
- Portfolio master images remain clean and unwatermarked.
- Customer previews before payment use a separate proof layout with an order identifier and five repeated transparent overlays. A bottom lockup by itself is not proof protection because it is easily cropped.

The luminous presentation treatment must not be recreated ad hoc. Do not add glow to the flat SVG masters. For small, functional, light-background or watermark applications, use the approved flat logo artwork.

## Files

- `ONYX_WORDMARK_EDITORIAL_V1_CHAMPAGNE.png` — transparent master for dark applications.
- `ONYX_WORDMARK_EDITORIAL_V1_INVERSE.png` — lockup on an Onyx field.
- `Presentations/ONYX_MONOGRAM_ONYX_SILK_PRESENTATION_V1.png` — controlled ONYX Stone Signature artwork.
- `Portfolio/*/Business_V1/portfolio_framed_preview/` — applied portfolio use.

The Cormorant Garamond variable font is bundled under SIL Open Font License 1.1. See `../Typography/CormorantGaramond-OFL.txt`.


````

## 13 Production/Brand/CLIENT_PREVIEW_PROOF_STANDARD_V1.md

````text
# ONYX Client Preview Proof Standard v1

Pre-payment previews are proof files, not marketing layouts. Every proof file has five repeated transparent lockups in restrained Champagne: `ONYX` plus `PRIVATE PREVIEW / ORDER <ID>`. The overlay crosses the image body, so removing it means removing a material part of the photograph.

Use a unique order identifier for each customer. Proofs stay outside public portfolio folders. Never add a proof overlay to paid delivery, public portfolio framing or canonical R&D sources.

`ONYX_PREPAYMENT_PROOF_LAYOUT_V1.png` is a visual sample only; `SAMPLE-0001` is not a customer identifier.


````

## 10 Roadmap/Roadmap.md

````text
# Roadmap

## ✅ Phase 1A — Canonical contracts: COMPLETE

- [x] JobSpec v1 и Manifest v1 contract layer.
- [x] Stable logical IDs и deterministic `sha256-derived-v1` seeds.
- [x] Валидация quality → human review → selection → postprocessing → delivery.
- [x] Atomic Manifest persistence и read-only compatibility importers.

Phase 1A не включает runtime integration.

---

## ✅ Phase 1B.1 — Runtime Configuration and Materialization: COMPLETE

- [x] RuntimeConfig и ProviderRuntimeConfig.
- [x] Local/ignored runtime config и tracked sanitized example.
- [x] Безопасное resolution `client://`, `workspace://`, `repo://`, `model://`.
- [x] Immutable ExecutionPlan без execution state.
- [x] Canonical per-provider/per-candidate `sha256-derived-v1` seeds.
- [x] Side-effect-free JobSpec materialization и 50 passing tests.

Phase 1B.1 не выполняет providers и не создаёт Manifest lifecycle.

---

## ✅ Phase 1B.2 — Canonical Generation Execution Shell: COMPLETE

- [x] `SceneGenerator` boundary и CPU-only `FakeSceneGenerator`.
- [x] Orchestrator-owned incremental Manifest lifecycle и single writer.
- [x] Stable `GenerationResult` и distinct `AttemptRecord` per invocation.
- [x] Atomic persist-before-invoke, structured failures и artifact provenance.
- [x] Retry, resume, stale-attempt/crash recovery и missing-artifact rerun.
- [x] Independent sibling failure handling и 70 passing tests.

Phase 1B.2 не подключает real providers. Identity-aware generation ещё
не executable без native passthrough IdentityResult lifecycle.

---

## ✅ Phase 1B.3 — Real FLUX SceneGenerator integration: COMPLETE

- [x] Минимальный ComfyUI HTTP client для `/prompt`, `/history`, `/view`.
- [x] Non-identity `FluxSceneGenerator` с workflow-hash и model checks.
- [x] LoRA Lab Phase 1: CPU/dry-run analysis, selection, planners, AI-Toolkit renderer, metrics and serialization.
- [ ] Alexander LoRA dataset-size Phase 2: approved materialization and controlled training.
- [x] Deterministic workflow patching и unchanged canonical seed.
- [x] Structured failures и untrusted output-descriptor validation.
- [x] Windows relative subfolder normalization без ослабления traversal checks.
- [x] Один successful real smoke и same-manifest resume без нового POST.
- [x] 93 passing canonical CPU tests.

Phase 1B.3 не подключает identity-aware generators, FaceFusion, legacy runners,
Quality Gate, review/selection, postprocessing или delivery.

Следующие отдельные шаги:

- Проверить восстановление личности через FaceFusion после FLUX.
- Проверить устранение растительности на лице через FaceFusion.
- Подключить существующие Job Engine и Ensemble runtime через compatibility
  adapters без переписывания исторических jobs.
- Подключить QualityEvaluator и human-review evidence к каноническому Manifest.
- Перевести postprocessing на selected-only execution.

---

## 💡 В будущем

- Автоматический Hand Repair.
- Автоматический отбор лучших изображений.
- Расширение библиотеки scene presets.
- Добавление новых коллекций сцен помимо Executive.
- Автоматическая генерация полного клиентского сета ONYX.

---

## ✅ Завершено

- [x] Client Profile v2.
- [x] ONYX Flux Scene Generator v1.0.0.
- [x] 12 Executive scene presets.
- [x] Управление параметрами `fixed/random`.
- [x] Diversity-контроль сцен без повторов.
- [x] Интеграция Flux Scene Generator с ComfyUI API.
Phase 1A–1B.3 не переводят существующие runner-ы, Quality Gate, FaceFusion,
postprocessor и legacy ComfyUI workflows на canonical execution; подключён
только новый canonical FLUX API workflow Phase 1B.3.

````

## 13 Production/README.md

````text
# ONYX Production Core

**Status:** ACTIVE  
**Established:** 2026-09-16

`13 Production` is the canonical product, brand, portfolio and marketing control plane for ONYX. It contains standards, promotion manifests and delivery templates; it does not replace research evidence or silently mutate it.

`09 Experiments` remains the R&D evidence base. An asset may be promoted only through an explicit production manifest after required QA and approval. Promotion records canonical source paths and integrity data. It never changes an experimental source, candidate, review record or historical export in place.

## Structure

- `Brand/` — visual-system specification and future Brand Board template.
- `Product_Standards/` — customer product, portfolio and marketing standards.
- `Portfolio/` — promotion manifests and migration assessments; no copied canonical experiment images.
- `Marketing/` — channel-level production specifications.
- `Client_Delivery/Templates/` — delivery package requirements.
- `Templates/Collection_Book/` — local JSON-to-PDF reference renderer for 1/10/20-photo books; not yet a delivery default.
- `Samples/P02_Business_Collection_Book_v1/` — 15-page Signature reference, technical QA complete, owner design approval pending. Historical source-approval conflicts are documented in its README.

Collection Book requirements: [[Product_Standards/ONYX_COLLECTION_BOOK_STANDARD]]. Architectural decision: [[../12 Decisions/ADR-0008 Collection Book Reference Renderer]].

The production status of an asset is determined by its production manifest, not by the existence of a similarly named experimental file. `MISSING`, `PENDING`, and `REPAIR_REQUIRED` must not be replaced by placeholders.

See [[../12 Decisions/ADR-0007 Production Core and R&D Promotion Boundary|ADR-0007]].

````

