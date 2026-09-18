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

## 3. Preserve the approved visual rules

- Canvas is 1080 × 1350, 4:5. Never crop, filter, stretch or overwrite a source image.
- The cover uses symmetrical dark stone side fields and a central Onyx field. The portrait must fit within the central field.
- Light and dark pages use the same 230-unit footer geometry: monogram, Champagne rule, collection lockup, Champagne `ONYX COLLECTION BOOK` and folio. Light pages use the subtle light-stone variation.
- Captions use Champagne Cormorant. The paired-page title `В рабочем ритме` follows the same treatment.
- The continuation title is one Cormorant line; keep the collection blocks directly beneath it. Add collection imagery only when approved images genuinely belong to those collections.

## 4. Build

Run from the repository root into a new output folder:

```powershell
& 'C:/Users/ME/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' '13 Production/Templates/Collection_Book/render_collection_book.py' --data 'path/to/client_book.json' --output '13 Production/Samples/CLIENT_COLLECTION_BOOK_v1'
```

Do not use the sample folder as an output target. The renderer rejects a nonempty output directory to prevent accidental overwrite.

## 5. Verify before delivery

Run the renderer tests, then inspect the PDF and its generated previews:

```powershell
& 'C:/Users/ME/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -m unittest '13 Production/Templates/Collection_Book/test_renderer.py'
```

Confirm all ordered images appear, text is readable at phone scale, pages have the expected count, the PDF is under 15 MiB, captions do not collide with footers, all source hashes remain unchanged and no internal identifiers are visible. Deliver only the PDF. Keep `source_data.json`, manifest, preview and review files internal.
