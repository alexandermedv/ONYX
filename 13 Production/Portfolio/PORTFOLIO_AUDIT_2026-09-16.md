# Portfolio Standard v1 — evidence audit

Date: 2026-09-16. No image generation, source modification, visual approval, upscale or production export was performed. Inventories record exact paths, SHA256, full image decode and dimensions. They are candidate mappings, not promotion approvals.

| Session | Photos | Human review | 3:4 source photos | Existing derived images |
| --- | --- | --- | --- | --- |
| P01 gpt_portfolio_v1 | 10 | 6 selected + 4 reserve; no 10-image approval | 10/10 | 59 |
| P02 business_v1 | 10 | 10/10 PENDING | 10/10 | 56 |
| P02 lifestyle_v1 | 10 | 10/10 PENDING | 10/10 | 38 |
| P02 boudoir_v1 | 10 | 10/10 PENDING | 10/10 | 36 |
| P03 executive_v1 | 10 | 10/10 PENDING | 0/10 | 38 |

## Actual blockers

- P01: four additional final selections are required, not necessarily four new generations. Existing reserves overlap desk/standing scenes. CLOSE, HERO, SEATED, ENVIRONMENT and FULL_BODY have named candidates; WAIST, ACTION, 3Q_BODY, MOOD and EDITORIAL require visual role selection across the full candidate pool. A ten-photo session contact sheet must follow that decision; existing six-photo marketing does not establish a ten-photo session.
- P02 business/lifestyle/boudoir: all 30 review decisions remain PENDING. Ten files per collection exist; no missing source generation is established. Collection-specific final QA, critical-defect clearance, standard role assignment and approval remain required. Boudoir remains a private collection; no public Avito promotion is implied.
- P03: all ten source photos exist; all ten human reviews remain PENDING. EXEC_02 (waist-up) cannot be asserted to satisfy CLOSE and EXEC_08 (medium) cannot be asserted to satisfy 3Q_BODY. The existing mapping is provisional. The source images are 5:6, while the package specifies 3:4; composition must be reviewed before cropping.
- All sessions: no verified upscale lineage/output; no approved standard-named ten-image exports or verified portfolio-watermark set. A larger web or layout canvas is not evidence of upscale.
- Existing covers, before/after, grids of 4/6, contact sheets, carousel and web files are inventoried as reusable candidates. P03 cover/grid_4/grid_6 were incorrectly called physically missing in the previous checklist; corrected to SOURCE_EXISTS_PENDING_PROMOTION.
- P03 portfolio card is still missing as a separately specified approved production deliverable. Existing Avito cards are not automatically equivalent. Watermark artwork/application and marketing layouts need approval and final exports.
- Marketing Standard v1 carousel is semantic: P03 current carousel repeats one portrait per slide and does not implement slide 3 comparison, slide 4 full contact sheet, slide 6 five-step workflow or slide 8 multiple identities. Preserve it as R&D marketing; a compliant production carousel needs a separate layout pass after selection.

## Safe next actions

Use the per-session SOURCE_INVENTORY.json files to select roles and approve QA. Then map role order 01 HERO, 02 CLOSE, 03 WAIST, 04 SEATED, 05 ENVIRONMENT, 06 ACTION, 07 3Q_BODY, 08 FULL_BODY, 09 MOOD, 10 EDITORIAL; export approved derivatives with source hashes and processing provenance. Do not promote a reserve, infer QA from filenames or count resizing as upscale. No new generation is proven necessary until visual selection/repair decisions are recorded.

## Preservation and Git

PREFLIGHT_2026-09-16.json records the fetched remote state and all twelve pre-existing user file hashes. The user-authored finalize_pack.py was syntax-checked without execution; its eleven changed JPEGs were fully decoded. Its experimental outputs remain experimental, not production-approved. All twelve bytes are checked unchanged after this audit. The original production standards and ADR were reviewed; only the P03 checklist/mapping metadata and migration audit links were updated.
