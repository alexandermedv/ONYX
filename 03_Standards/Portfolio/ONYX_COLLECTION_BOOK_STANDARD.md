# ONYX Collection Book Standard v1

Date: 2026-09-17. Status: approved reference layout; client-specific copy and asset approval remain required.

## Purpose

Collection Book is the personal editorial presentation of an ONYX photoshoot. It accompanies, never replaces, separate high-resolution photographs. It is not a technical report or evidence of publication approval.

## Delivery model

- Portrait: no Collection Book. The renderer’s legacy Preview tier is a technical capability only, not a saleable frozen entitlement.
- Signature: ten photographs; 14–18 pages, reference implementation 15.
- Premium: twenty photographs; Extended Collection Book PDF, a clearer narrative and Concept chapters when useful. The legacy 16-page paired layout is a technical starting point, not proof of visual certification. Motion is outside the frozen package.
- All orders retain their separate clean high-resolution photographs. Commercial inclusions follow [Product System](../Product/ONYX_PRODUCT_SYSTEM.md); renderer capabilities do not expand them.

## Required sections

Cover with selected photo, approved logo, collection title and short subtitle; opening note from ONYX; collection purpose and use cases; personal note; complete photo story; ONYX Selection with a justified choice; final next-collections page.

Photo story must cover every ordered photograph exactly once. Cover and Selection may intentionally reuse photographs; every reuse must be recorded. Existing hero metadata takes precedence over subjective re-selection. No invented review scores.

The current renderer accepts exactly 1/10/20 photographs. A Signature/Premium order with extra finals needs a separately prepared and visually checked Book layout covering the complete ordered set; the existing renderer does not automatically support 11/21 or arbitrary counts. Confirm that packaging capacity before selling extra finals for a Book-bearing order. No renderer change is included in this freeze.

## Optional sections

Client display name; captions; additional context when it is specific and brief; verified collection links; separately approved future Motion link, never a frozen Premium obligation. QR URLs are reserved in v1 and rejected when nonempty until a QR renderer is implemented. Do not show inactive placeholder buttons or invented URLs.

Cross-sell copy and Business/Executive differentiation must follow [ONYX Collection Catalog](ONYX_COLLECTION_CATALOG.md).

## Copy standard

Opening note: explain ONYX’s mission, how the collection is assembled around a client’s task, and thank the client for the request; it must not address the client by name. Description: purpose, then practical uses. Selection: one or two sentences grounded in the chosen image and selection metadata. Closing: one to three restrained, series-specific sentences that address the client and draw on the approved persona or client brief, distinct from the collection description; a specific, supportable compliment is welcome. Cross-sell: only documented products; show “Скоро” unless launch availability is verified. Never imply a human photographer personally wrote the text.

Body copy is Russian in v1; established collection names and ONYX Selection may remain English. No client identity is invented for a demo. Sample display name may be empty.

## Visual standard

Authority: [Brand System](../Brand/ONYX_BRAND_SYSTEM.md), [Brandbook content](../Brand/ONYX_BRANDBOOK_CONTENT_V1.md), [Editorial Wordmark](../../13%20Production/Brand/Logo/EDITORIAL_WORDMARK_V1.md).

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
