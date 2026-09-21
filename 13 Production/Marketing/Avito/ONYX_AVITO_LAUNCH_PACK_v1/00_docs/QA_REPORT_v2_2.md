# Avito Launch Pack — Final v2.2 QA Report

**Date:** 2026-09-21<br>
**Status:** `READY_FOR_AVITO_PUBLISH_REVIEW`

## Commercial QA

- PASS — Portrait remains 1 final / 1 000 ₽.
- PASS — Signature remains 10 finals / 3 000 ₽ and is the visual center of Pricing.
- PASS — Premium remains 20 finals / 5 000 ₽.
- PASS — Portrait → Signature credits the full 1 000 ₽ and requires a 2 000 ₽ additional payment within 7 calendar days under the active eligibility rules.
- PASS — Signature → Premium requires a 2 000 ₽ additional payment within 7 calendar days when lawful references, consent, production context and order metadata remain available and the original Collection continues.
- PASS — Premium is described as one main Collection, not a bundle of complete Collections.
- PASS — add-ons remain in the full listing copy and do not crowd the Pricing card.

## Collection availability QA

- PASS — Business is the only Collection represented as available on the current soft launch.
- PASS — other catalog directions are not named as current public offers; their availability is confirmed individually before payment.
- PASS — card 03 labels the approved P02 Business image only as a Business visual example.
- PASS — no Business image is presented as Lifestyle, Executive, Dating, Fashion, Glamour, Boudoir or another Collection.

The availability decision is recorded in `COLLECTION_AVAILABILITY_DECISION_v2_2.md`.

## Visual and mobile QA

- PASS — exact 390 px preview confirms that `Business` is readable without zoom.
- PASS — exact 390 px preview confirms that `1 000 ₽`, `3 000 ₽` and `5 000 ₽` are readable without zoom.
- PASS — the Portrait → Signature path and `ДОПЛАТА 2 000 ₽` are readable and understandable without zoom.
- PASS — Signature remains larger and darker than Portrait and Premium.
- PASS — slides 04 and 05 preserve approved imagery while making range and scene diversity explicit.
- PASS — the rendered star beside Signature is a vector-drawn mark; no missing-glyph artifact remains.
- PASS — no face is obscured by text or branding.

## Rights and privacy QA

- PASS — visual assets are limited to approved synthetic P02 Business A01–A10 plus approved synthetic B01 / REF03.
- PASS — the Before → After pair remains REF03 → A10 with its existing disclosure.
- PASS — no P01, P03, P02 Lifestyle, P02 Boudoir, Orders, client reference/candidate/final, client Book or delivery asset is used.
- PASS — canonical/source assets and v2.1 outputs remain unchanged by recorded hash.
- PASS — listing copy states that client photographs are not published without separate permission.

## Carousel order

1. HERO.
2. BEFORE → AFTER.
3. COLLECTIONS.
4. IDENTITY / RANGE.
5. SCENES / DIVERSITY.
6. PROCESS.
7. QUALITY.
8. PRICING + PORTRAIT → SIGNATURE UPGRADE.
9. COLLECTION BOOK.
10. CTA.

## Technical verification

- ten v2.2 master PNG files: 2560 × 1920, RGB;
- ten v2.2 export JPG files: 1280 × 960, RGB;
- slides 01, 02, 06, 07, 09 and 10 are byte-identical to v2.1;
- only slides 03, 04, 05 and 08 differ from v2.1;
- final contact sheet: `02_contact_sheets/AVITO_CAROUSEL_FINAL_REVIEW_v2_2.jpg`;
- mobile QA: `06_qa/v2_2/AVITO_MOBILE_QA_v2_2.jpg`;
- machine-readable results: `render_inspection_v2_2.json` and `validation_result_v2_2.json`.

No Avito publication, commit or push was performed. Final human approval remains required.
