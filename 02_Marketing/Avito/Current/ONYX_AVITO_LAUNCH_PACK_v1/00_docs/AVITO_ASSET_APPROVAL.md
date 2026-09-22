# Avito Asset Approval — P02 Business A01–A10

**Recorded:** 2026-09-21<br>
**Approver:** ONYX owner via explicit user authorization<br>
**Scope:** `AVITO_LAUNCH_V1`

The ten exact JPEG files `ONYX_P02_BUSINESS_01_HERO.jpg` through `ONYX_P02_BUSINESS_10_EDITORIAL.jpg` in `01_Characters/P02/02_Sessions/Business_v1/02_Final` are approved synthetic marketing assets for:

- Avito advertisement;
- Avito carousel;
- ONYX layouts directly related to Avito Launch Pack v1;
- crop, resize, typography and branding overlays required for the advertisement;
- contact sheets and QA previews for preparing this advertisement.

For every listed file:

```yaml
synthetic_persona: true
marketing_approved: true
avito_publication_approved: true
publish_approved: true
approval_scope: AVITO_LAUNCH_V1
```

Canonical and source images must remain unchanged. Exact source paths and SHA-256 values are preserved in `01_asset_candidates/PROVENANCE.json` and the source portfolio manifest.

This decision does not apply to P01, P03, P02 Lifestyle, P02 Boudoir, private Orders, client references, client candidates, client finals, client Collection Books, delivery packages, or marketing channels outside `AVITO_LAUNCH_V1`.

This approval permits the assets and layouts; final advertisement publication remains a separate human action.

## Revision v2 Before → After reference

The owner additionally authorized exactly:

`09 Experiments/identity_benchmark_v1/P02_F30_Lifestyle/01_references/P02_REF03.png`

SHA-256: `23fb0883218085354fe2de85d92d2641916501ac41e754735892babb10a004c2`

This is a canonical reference for the same frozen synthetic P02 identity v1. It may appear only as the Before/reference side of the Avito Launch Pack revision v2 comparison with:

```yaml
synthetic_persona: true
marketing_approved: true
avito_publication_approved: true
publish_approved: true
approval_scope: AVITO_LAUNCH_V1_BEFORE_AFTER
```

The approved After asset is A10, `ONYX_P02_BUSINESS_10_EDITORIAL.jpg`. The layout states that it is a synthetic-persona demonstration and does not present the pair as a real-client transformation.
