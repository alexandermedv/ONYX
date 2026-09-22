# Avito Launch Pack — Revision v2 QA Report

**Date:** 2026-09-21<br>
**Status:** `READY_FOR_HUMAN_AVITO_REVIEW_V2`

V1 remains preserved. This report covers the parallel mobile-first v2 outputs.

## Rights and provenance

- PASS — P02 Business A01–A10 remain approved synthetic assets for `AVITO_LAUNCH_V1`.
- PASS — Before asset B01 is exact canonical synthetic reference `P02_REF03.png`, approved only for `AVITO_LAUNCH_V1_BEFORE_AFTER`.
- PASS — `identity_manifest.yaml` and `references_metadata.yaml` identify B01 as part of the same frozen synthetic P02 identity v1.
- PASS — B01 canonical and working-copy SHA-256 are `23fb0883218085354fe2de85d92d2641916501ac41e754735892babb10a004c2`.
- PASS — After asset A10 retains SHA-256 `d918c5e894d5a6f8a0b191e1d78db72f03d3a30e4be98db4797e60c99261f6f5`.
- PASS — canonical/source assets were not modified.
- PASS — no P01, P03, real-client, Orders, client Collection Book or delivery asset is referenced or copied.

## Carousel structure

1. Hero — A01.
2. Before → After — B01 / REF03 → A10.
3. Diversity — A03, A04, A06, A10.
4. Portrait / personality — A02, A03.
5. Work / context — A04, A09, A05.
6. Process.
7. Quality control.
8. Pricing.
9. Collection Book PDF.
10. CTA.

Ten cards are retained. Series and Range are combined on slide 03 to preserve all required conversion messages within the existing format.

## Commercial and product QA

- PASS — Portrait remains 1 photo / 1 000 ₽.
- PASS — Signature remains 10 photos / 3 000 ₽ and is visually recommended.
- PASS — Premium remains 20 photos / 5 000 ₽.
- PASS — only brief add-ons `+1 фото — 500 ₽` and `Срочно — от +50%` appear on pricing.
- PASS — Premium is not presented as multiple complete Collections.
- PASS — no guarantee, unlimited revision or all-candidates claim is shown.
- PASS — Before/After is explicitly disclosed as a synthetic-persona demonstration, not a real-client case.

## Visual and mobile QA

- PASS — hero photograph occupies the dominant area; headline and entry price read immediately.
- PASS — Before and After are balanced, honestly labeled and visually distinct.
- PASS — portrait, work, movement and full-body variety appears by slide 03.
- PASS — process is reduced to five stages; quality is reduced to six large criteria.
- PASS — Signature is the dominant pricing block.
- PASS — Book benefit states both the PDF format and included products.
- PASS — CTA combines the action, free photo check and product-format guidance with a large portrait.
- PASS — all ten 1280 × 960 exports were visually reviewed in the 350 × 263 mobile sheet.
- PASS — no key card uses A08 or its prominent synthetic lobby signage.
- PASS — no face is obscured by typography or branding.

## Technical validation

- ten v2 master PNG files: 2560 × 1920, RGB;
- ten v2 export JPG files: 1280 × 960, RGB;
- all generated files decode successfully;
- `06_qa/v2/render_inspection_v2.json` records dimensions, format, bytes and SHA-256;
- `06_qa/v2/validation_result_v2.json` records the reproducible validation result.

## Human review gate

Review the exact Before → After comparison, carousel order, copy hierarchy and crop choices. Verify the current Avito Services form immediately before any manual publication.

No automated publication, commit or push was performed.
