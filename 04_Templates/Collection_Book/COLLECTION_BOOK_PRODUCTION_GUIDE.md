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
& 'C:/Users/ME/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' '04_Templates/Collection_Book/render_collection_book.py' --data 'path/to/client_book.json' --output '13 Production/Samples/CLIENT_COLLECTION_BOOK_v1'
```

Do not use the sample folder as an output target. The renderer rejects a nonempty output directory to prevent accidental overwrite.

## 7. Verify before delivery

Run the renderer tests, then inspect the PDF and its generated previews:

```powershell
& 'C:/Users/ME/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -m unittest '04_Templates/Collection_Book/test_renderer.py'
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

## Commercial scope override — CURRENT, 2026-09-20

[Product System](../../Product_Standards/ONYX_PRODUCT_SYSTEM.md) controls inclusions: Portrait has no Book; Signature Standard PDF; Premium Extended PDF with deeper narrative and Concept grouping when useful. `Preview` below names a retained legacy renderer tier, not a current product entitlement. Motion support is a technical capability outside frozen scope. Existing renderer input contracts and examples remain unchanged. Premium visual certification remains per-output work, not implied by planner tests.
