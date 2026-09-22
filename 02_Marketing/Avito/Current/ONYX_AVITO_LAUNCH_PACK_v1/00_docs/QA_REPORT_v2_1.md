# Avito Launch Pack — Final v2.1 QA Report

**Date:** 2026-09-21<br>
**Status:** `READY_FOR_AVITO_LAUNCH_APPROVAL`

This report covers the final micro-pass only. The v2 composition, typography system, imagery and text remain intact except for a modest increase in the visual weight of `от 1 000 ₽` on HERO.

## Before reference decision

- PASS — all five canonical P02 synthetic references were inspected at source resolution.
- PASS — `P02_REF03.png` remains the best ordinary/casual Before for card 02.
- PASS — `P02_REF02.png` is the nearest alternative, but is more styled and posed; it is not a clearly better replacement.
- PASS — card 02 remains byte-identical to v2 and the canonical REF03 source remains unchanged.

See `BEFORE_REFERENCE_REVIEW_v2_1.md` for the file-by-file assessment.

## Visual and mobile QA

- PASS — HERO entry price is slightly larger and remains subordinate to the headline and portrait.
- PASS — cards 02–10 are byte-identical to the reviewed v2 masters and exports.
- PASS — Pricing was inspected at an exact 390 px card width; `1 000 ₽`, `3 000 ₽`, `5 000 ₽`, `+1 фото — 500 ₽` and `Срочно — от +50%` remain readable without zoom.
- PASS — CTA was inspected at an exact 390 px card width; `Напишите «Хочу ONYX»` and both supporting bullets remain readable without zoom.
- PASS — no crop, layout, typography-system, image or copy defect requiring another change was found.

## Rights, privacy and commercial QA

- PASS — the carousel uses only approved synthetic P02 Business A01–A10 plus exact synthetic reference B01 / REF03.
- PASS — A01–A10 retain `approval_scope: AVITO_LAUNCH_V1`; B01 retains the narrower `approval_scope: AVITO_LAUNCH_V1_BEFORE_AFTER`.
- PASS — source and working-copy hashes match recorded provenance; canonical/source assets were not modified.
- PASS — no P01, P03, P02 Lifestyle collection, P02 Boudoir, Orders, client reference/candidate/final, client Collection Book or delivery asset is present.
- PASS — the Before → After card explicitly discloses a synthetic-persona demonstration.
- PASS — public pricing remains Portrait 1 photo / 1 000 ₽, Signature 10 photos / 3 000 ₽ and Premium 20 photos / 5 000 ₽; brief add-ons remain unchanged.
- PASS — no real-client claim, guarantee, unlimited-revision claim or automatic-publication action was introduced.

## Technical verification

- ten v2.1 master PNG files: 2560 × 1920, RGB;
- ten v2.1 export JPG files: 1280 × 960, RGB;
- final review contact sheet: `02_contact_sheets/AVITO_CAROUSEL_FINAL_REVIEW_v2_1.jpg`;
- exact-size mobile preview: `06_qa/v2_1/AVITO_MOBILE_QA_v2_1.jpg`;
- machine-readable inspection and validation: `render_inspection_v2_1.json` and `validation_result_v2_1.json`;
- prior v1 and v2 rendered outputs remain unchanged by recorded hashes.

Human approval is still required before publication. No commit, push or Avito publication was performed.
