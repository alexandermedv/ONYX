# ONYX Signature Business — Scene Plan v1

**Order:** `ORD-2026-0001`
**Product:** `SIGNATURE`
**Collection:** `BUSINESS`
**Target:** 10 final photographs
**Style intensity:** `GLAMOUR`

## Direction

Create a polished, flattering and elevated Business collection for CV and social use. `GLAMOUR` means premium light, clean styling and confident presence; it does not mean fashion makeup or an artificial result.

**Identity guidance:** adult man; closely cropped light hair around a balding top; light complexion; light eyebrows and eyes; clean-shaven appearance; no beard; no glasses. Preserve the identity evident across the current five-reference set.

## Outfit strategy

Use 2–3 compatible looks without brands: a navy or blue suit with white shirt; a smart business jacket without a tie; and a slightly relaxed executive business-casual look. Keep the appearance clean-shaven and corporate.

## Scenes

| Scene ID | Purpose | Framing | Outfit | Environment |
|---|---|---|---|---|
| BUSINESS_01 | CV, profile, corporate page | Head-and-shoulders | Navy suit, white shirt | Clean studio or refined office wall |
| BUSINESS_02 | Soft premium profile | Soft three-quarter portrait | Smart jacket, open collar | Window-lit modern office |
| BUSINESS_03 | Working credibility | Upper-body at desk | Navy suit | Executive desk with restrained details |
| BUSINESS_04 | Professional movement | Three-quarter walking portrait | Smart jacket | Bright office corridor |
| BUSINESS_05 | Leadership image | Waist-up, meeting-ready | Suit, open collar | Boardroom |
| BUSINESS_06 | Scale and posture | Near full-body | Suit | Minimal office architecture |
| BUSINESS_07 | Informal professional use | Upper-body seated | Relaxed business-casual | Lounge or collaboration space |
| BUSINESS_08 | Digital work | Three-quarter at laptop | Smart jacket | Modern workspace |
| BUSINESS_09 | Editorial personal brand | Head-and-shoulders or waist-up | Deep-blue business look | Architectural office environment |
| BUSINESS_10 | Closing hero / ONYX Selection candidate | Strong three-quarter portrait | Best-fitting suit look | Premium restrained studio or office |

## Future candidate strategy — DRY RUN HYPOTHESIS

- Generate `2–4` candidates per scene.
- Regenerate only after a QA failure.
- Repair only promising candidates whose issue can be corrected without compromising identity.

## Future generation strategy — not executed

- **Default route:** ChatGPT Imagegen with the six order-approved references and an order-specific single-scene technical qualifier before batch work.
- **Fallback route:** ChatGPT Imagegen targeted retry or controlled correction of a promising candidate; keep the same reference set and identity constraints.
- **Target output:** 1536×2048, `3:4` portrait; use a conservative crop for landscape-friendly scenes only when needed.
- **Entry gate:** technical qualifier must pass likeness, clean-shaven requirement, anatomy and realism before batch production.

PuLID and FLUX are never default routes for this order. The local PuLID/FLUX baselines are documented as technically unvalidated and are not selected automatically.

The default is governed by [ONYX Generation Route Policy v1](../../Product_Standards/ONYX_GENERATION_ROUTE_POLICY_v1.md).
