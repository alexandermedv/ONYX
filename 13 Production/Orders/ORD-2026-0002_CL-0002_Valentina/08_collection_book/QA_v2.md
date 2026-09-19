# Collection Book v2 — QA

Order: `ORD-2026-0002_CL-0002_Valentina`
Artifact: `ORD-2026-0002_VALENTINA_BUSINESS_COLLECTION_BOOK_v2.pdf`
State: **QA PASS; owner/design review PASS; approved for delivery**

## Build and technical checks

- Rendered with the approved Collection Book renderer and unchanged approved style configuration.
- PDF opens successfully and contains exactly 15 pages at 1080 × 1350 pt.
- All 10 selected current final-image hashes match the order files recorded by the renderer manifest.
- All 15 JPEG previews exist and decode; preview index runs page-01 through page-15.
- No source image was cropped by the renderer; approved image placement geometry is preserved.
- Renderer privacy-text guard and text-overflow guard passed.
- PDF size is below 15 MiB.
- Existing v1 PDF is unchanged; only its manifest marks it superseded.

## Editorial and visual checks

- Cover: BUSINESS_09; ONYX Selection: BUSINESS_01.
- Repeat owner-approved choices and revised story order are reflected.
- Personal note is individualized to Valentina’s photographed professional range and does not restate the collection description.
- ONYX Selection note reflects BUSINESS_01’s professional headshot role.
- Captions were checked against actual image content, including the desk, walking, full-body, profile, and warm-smile scenes.
- All 15 pages were reviewed in the contact sheet; cover, personal note, paired-image spread, full-body, profile, warm-smile, Selection, and closing pages were also inspected individually at full preview scale.
- No visible text overflow or layout shift found. Text and key page elements remain legible at mobile preview scale.

## Approval gate

Automated and visual QA: **PASS**.
Owner/design review of the rendered v2 book: **PASS**.
The book is approved for delivery. Order status is `READY_FOR_DELIVERY`; delivery itself is pending.

## File integrity

- Bytes: `4,928,959`
- SHA256: `3db1d94859e6819cc6aa3df98377c709073dce35f8d52039d9390a6cefc3d7e0`
