# Avito Launch Pack — Headroom Fix v2.5

**Date:** 2026-09-21
**Status:** `APPROVED_FOR_AVITO_PUBLISH`

The image crops on slides 02–05 were anchored to the complete source top edge. The full head, hairline and hair contour are now visible in every photo on those slides.

## Visual QA

- PASS — slide 02: both Before and After portraits retain visible headroom.
- PASS — slide 03: Business and Lifestyle portraits show the complete head and hair contour.
- PASS — slide 04: both angles retain the complete head.
- PASS — slide 05: the main image and both supporting images retain the complete head.
- PASS — exact 390 px previews confirm the correction remains visible at mobile size.

## Change boundary

- Slides 02–05 changed only through crop positioning needed for headroom.
- Slides 01 and 06–10 are byte-identical to v2.4.
- Copy, pricing, rights, approved source selection and product scope are unchanged.
- Canonical/source images were not modified.

## Outputs

- final carousel: `02_contact_sheets/AVITO_CAROUSEL_FINAL_v2_5.jpg`;
- corrected masters: `04_master/v2_5/AVITO_V2_5_02.png` through `AVITO_V2_5_05.png`;
- corrected exports: `05_export/v2_5/AVITO_V2_5_02.jpg` through `AVITO_V2_5_05.jpg`;
- mobile QA: `06_qa/v2_5/AVITO_MOBILE_QA_v2_5.jpg`;
- validation: `06_qa/v2_5/validation_result_v2_5.json`.

No commit, push or Avito publication was performed.
