# Avito Launch Pack — Slide 09 Headroom Fix v2.6

**Date:** 2026-09-21
**Status:** `APPROVED_FOR_AVITO_PUBLISH`

The four image crops on slide 09 were anchored to the complete source top edge. The full head, hairline and hair contour are now visible in every image on the card.

## Visual QA

- PASS — left portrait retains the complete head and hair contour.
- PASS — both centre portraits retain visible headroom.
- PASS — right full-length portrait retains the complete head.
- PASS — exact 390 px preview confirms all four corrected crops remain clear at mobile size.

## Change boundary

- Only slide 09 changed from v2.5.
- Slides 01–08 and 10 are byte-identical to v2.5.
- Copy, typography, composition, pricing, rights and approved source selection are unchanged.
- Canonical/source images were not modified.

## Outputs

- final carousel: `02_contact_sheets/AVITO_CAROUSEL_FINAL_v2_6.jpg`;
- corrected master: `04_master/v2_6/AVITO_V2_6_09.png`;
- corrected export: `05_export/v2_6/AVITO_V2_6_09.jpg`;
- mobile QA: `06_qa/v2_6/AVITO_MOBILE_QA_v2_6.jpg`;
- validation: `06_qa/v2_6/validation_result_v2_6.json`.

No commit, push or Avito publication was performed.
