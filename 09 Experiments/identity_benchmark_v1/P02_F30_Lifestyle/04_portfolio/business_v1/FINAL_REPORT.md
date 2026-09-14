# P02 BUSINESS V1 — final packaging report

Technical package complete. Human approval and publication are pending. No commit created.

## Validation

| Check | Result |
|---|---|
| session_id | P02_BUSINESS_V1 |
| checked_on | 2026-09-15 |
| sources_present | 10 |
| sources_expected | 10 |
| unique_sha256 | 10 |
| prompts_present | 10 |
| manifest_entries | 10 |
| human_review_rows | 10 |
| human_decisions | PENDING |
| png_valid_and_readable | 10 |
| aspect_ratio_3_4 | 10 |
| technical_qa_rows | 10 |
| near_duplicate_detection | SKIPPED: existing repository tool requires unavailable cv2 |
| candidate_staging_copies_verified | 10 |
| web_derivatives_verified | 20 |
| marketing_derivatives_verified | 18 |
| marketing_traceability | PASS; two text-only cards have no image inputs |
| p02_identity_pngs_verified_unchanged | 6 |
| p01_files_verified_unchanged | 501 |
| preexisting_files_verified_unchanged | 533 |
| unrelated_tracked_diff_unchanged | True |
| source_pngs_overwritten | False |
| source_originals_and_reserve_preserved | True |
| technical_pack_status | PASS |
| human_approval | PENDING |
| publish_approved | False |
| commit_created | False |

## Source mapping and SHA256

All originals remain in the session root. Canonical paths are in `00_source`.

| ID | Original filename | Canonical filename | Dimensions | Bytes | SHA256 |
|---|---|---|---|---:|---|
| BUS_01 | P02_BUS_01_headshot_front.png | P02_BUS_01_headshot_front_v2.png | 1086 × 1448 | 2061575 | `cfa6328f56eb890c1faab43cac65f1b18873b1666a3a5e733a26c3209711c788` |
| BUS_02 | P02_BUS_02_window_3q.png | P02_BUS_02_window_3q_v2.png | 1086 × 1448 | 2047648 | `c6a4268bb90d2da603a37014e77d30af23723e2bb0edad84fa3fb9c034f58aaf` |
| BUS_03 | P02_BUS_03_executive_desk.png | P02_BUS_03_executive_desk_v2.png | 1086 × 1448 | 2009085 | `5e68469f0789097b6007f8bfdba03bfdb910e1ddd4a0e6487b13d93c6bf0cf99` |
| BUS_04 | P02_BUS_04_office_walk.png | P02_BUS_04_office_walk_v2.png | 1086 × 1448 | 1961761 | `8dede4976b623d0393cbb19ba74c8e7048008be0652160431213da297b5a9e71` |
| BUS_05 | P02_BUS_05_boardroom.png | P02_BUS_05_boardroom_v2.png | 1086 × 1448 | 1838406 | `8195b49a07d65e2bbe8d65236da62b4b5bea05e8243d08f90e282eb925d45a4a` |
| BUS_06 | P02_BUS_06_lobby_fullbody.png | P02_BUS_06_lobby_fullbody_v2.png | 1086 × 1448 | 2018688 | `f9109dd9f9ba2c29d3a35fe1a7b46f58f74d9f58807a46a808183213607d4cd6` |
| BUS_07 | P02_BUS_07_private_office.png | P02_BUS_07_private_office_v2.png | 1086 × 1448 | 1835251 | `51f12dad939278d3f3b214312c9588c8ee95111810534d53ab1f25d252f19339` |
| BUS_08 | P02_BUS_08_laptop_workspace.png | P02_BUS_08_laptop_workspace_v2.png | 1086 × 1448 | 1790449 | `87a5f20554bcc4dac8e577b62b15dd511d78bf5a37f87e8f0da5ff5a82e3f51a` |
| BUS_09 | P02_BUS_09_window_crossed_arms.png | P02_BUS_09_window_crossed_arms_v2.png | 1086 × 1448 | 1821932 | `e83ac1012236713fe5b83529372a9b24ed2abf6bdd08e45b2d4c45ee869ac40b` |
| BUS_10 | P02_BUS_10_editorial_fullbody.png | P02_BUS_10_editorial_fullbody_v2.png | 1086 × 1448 | 1987689 | `3cd3547b3dc8f6bcac4dd6776f1505ffffb9413e1da09e35c08493cfc8c4f312` |

## Prompt manifest

10/10 verbatim prompts, BUS_01–BUS_10; session identity rule preserved. Model, seed and settings unknown. Each prompt has its own text SHA256. `scene`, `pose_type`, `gaze`, `expression`, `framing` and `wardrobe` in the image manifest are observed descriptions.

## Technical QA

10/10 PNGs verified and decoded; exact 3:4 aspect ratio; unique SHA256. No human scores or automated identity scores assigned. Near-duplicate detection skipped due to missing cv2. EXIF presence is recorded per image in technical_qa.csv.

## Marketing assets

| File | Dimensions | Source IDs | Status |
|---|---|---|---|
| 05_marketing/01_contact_sheet/P02_business_v1_contact_sheet.jpg | 2400 × 1590 | BUS_01, BUS_02, BUS_03, BUS_04, BUS_05, BUS_06, BUS_07, BUS_08, BUS_09, BUS_10 | candidate |
| 05_marketing/01_contact_sheet/P02_business_v1_contact_sheet_clean.jpg | 2400 × 1590 | BUS_01, BUS_02, BUS_03, BUS_04, BUS_05, BUS_06, BUS_07, BUS_08, BUS_09, BUS_10 | candidate |
| 05_marketing/02_avito_carousel/P02_business_card_01.jpg | 1600 × 2000 | BUS_01, BUS_06 | candidate |
| 05_marketing/02_avito_carousel/P02_business_card_02.jpg | 1600 × 2000 | BUS_01, BUS_03, BUS_09 | candidate |
| 05_marketing/02_avito_carousel/P02_business_card_03.jpg | 1600 × 2000 | BUS_01, BUS_04, BUS_05, BUS_06 | candidate |
| 05_marketing/02_avito_carousel/P02_business_card_04.jpg | 1600 × 2000 | BUS_08, BUS_04, BUS_09 | candidate |
| 05_marketing/02_avito_carousel/P02_business_card_05.jpg | 1600 × 2000 | BUS_02, BUS_07 | candidate |
| 05_marketing/02_avito_carousel/P02_business_card_06.jpg | 1600 × 2000 | Text only | candidate |
| 05_marketing/02_avito_carousel/P02_business_card_07.jpg | 1600 × 2000 | Text only | candidate |
| 05_marketing/02_avito_carousel/P02_business_card_08.jpg | 1600 × 2000 | BUS_01, BUS_03, BUS_04, BUS_06, BUS_08, BUS_09 | candidate |
| 05_marketing/02_avito_carousel/P02_business_card_09.jpg | 1600 × 2000 | BUS_01, BUS_09 | candidate |
| 05_marketing/02_avito_carousel/P02_business_card_10.jpg | 1600 × 2000 | BUS_06, BUS_08 | candidate |
| 05_marketing/03_before_after/P02_reference_to_business_demo.jpg | 2100 × 1400 | BUS_01, BUS_06, MASTER, REF03 | candidate |
| 05_marketing/04_social/P02_business_square_selection.jpg | 1600 × 1600 | BUS_01, BUS_03, BUS_06, BUS_09 | candidate |
| 05_marketing/04_social/P02_business_story_cover.jpg | 1080 × 1920 | BUS_06 | candidate |
| 05_marketing/04_social/P02_business_portrait_showcase.jpg | 1600 × 2000 | BUS_01, BUS_08, BUS_09 | candidate |
| 05_marketing/04_social/P02_business_clean_grid_4.jpg | 1800 × 2440 | BUS_01, BUS_04, BUS_06, BUS_09 | candidate |
| 05_marketing/04_social/P02_business_clean_grid_6.jpg | 2100 × 2020 | BUS_01, BUS_03, BUS_04, BUS_06, BUS_08, BUS_09 | candidate |

## business_v1 tree

```text
business_v1/
  00_source/
    P02_BUS_01_headshot_front_v2.png
    P02_BUS_02_window_3q_v2.png
    P02_BUS_03_executive_desk_v2.png
    P02_BUS_04_office_walk_v2.png
    P02_BUS_05_boardroom_v2.png
    P02_BUS_06_lobby_fullbody_v2.png
    P02_BUS_07_private_office_v2.png
    P02_BUS_08_laptop_workspace_v2.png
    P02_BUS_09_window_crossed_arms_v2.png
    P02_BUS_10_editorial_fullbody_v2.png
  01_prompts/
    BUS_01.txt
    BUS_02.txt
    BUS_03.txt
    BUS_04.txt
    BUS_05.txt
    BUS_06.txt
    BUS_07.txt
    BUS_08.txt
    BUS_09.txt
    BUS_10.txt
    P02_business_v1_prompts.md
    P02_business_v1_prompts.yaml
    session_identity_block.md
  02_review/
    P02_business_v1_review.csv
    QA_NOTES.md
    README.md
    source_mapping.csv
    technical_qa.csv
    validation.json
  03_final/
    P02_BUS_01_headshot_front_v2.png
    P02_BUS_02_window_3q_v2.png
    P02_BUS_03_executive_desk_v2.png
    P02_BUS_04_office_walk_v2.png
    P02_BUS_05_boardroom_v2.png
    P02_BUS_06_lobby_fullbody_v2.png
    P02_BUS_07_private_office_v2.png
    P02_BUS_08_laptop_workspace_v2.png
    P02_BUS_09_window_crossed_arms_v2.png
    P02_BUS_10_editorial_fullbody_v2.png
    README.md
  04_web/
    jpg/
      P02_BUS_01_headshot_front_v2_web.jpg
      P02_BUS_02_window_3q_v2_web.jpg
      P02_BUS_03_executive_desk_v2_web.jpg
      P02_BUS_04_office_walk_v2_web.jpg
      P02_BUS_05_boardroom_v2_web.jpg
      P02_BUS_06_lobby_fullbody_v2_web.jpg
      P02_BUS_07_private_office_v2_web.jpg
      P02_BUS_08_laptop_workspace_v2_web.jpg
      P02_BUS_09_window_crossed_arms_v2_web.jpg
      P02_BUS_10_editorial_fullbody_v2_web.jpg
    webp/
      P02_BUS_01_headshot_front_v2_web.webp
      P02_BUS_02_window_3q_v2_web.webp
      P02_BUS_03_executive_desk_v2_web.webp
      P02_BUS_04_office_walk_v2_web.webp
      P02_BUS_05_boardroom_v2_web.webp
      P02_BUS_06_lobby_fullbody_v2_web.webp
      P02_BUS_07_private_office_v2_web.webp
      P02_BUS_08_laptop_workspace_v2_web.webp
      P02_BUS_09_window_crossed_arms_v2_web.webp
      P02_BUS_10_editorial_fullbody_v2_web.webp
    README.md
    web_manifest.csv
  05_marketing/
    01_contact_sheet/
      P02_business_v1_contact_sheet.jpg
      P02_business_v1_contact_sheet_clean.jpg
    02_avito_carousel/
      P02_business_card_01.jpg
      P02_business_card_02.jpg
      P02_business_card_03.jpg
      P02_business_card_04.jpg
      P02_business_card_05.jpg
      P02_business_card_06.jpg
      P02_business_card_07.jpg
      P02_business_card_08.jpg
      P02_business_card_09.jpg
      P02_business_card_10.jpg
    03_before_after/
      P02_reference_to_business_demo.jpg
      before_after_concept.md
    04_social/
      P02_business_clean_grid_4.jpg
      P02_business_clean_grid_6.jpg
      P02_business_portrait_showcase.jpg
      P02_business_square_selection.jpg
      P02_business_story_cover.jpg
    05_copy/
      avito_description_v1.md
      portfolio_caption_v1.md
      short_social_caption_v1.md
      website_business_collection_v1.md
    README.md
    marketing_manifest.yaml
  reserve/
    P02_BUS_01_headshot_front.png
    P02_BUS_02_window_3q.png
    P02_BUS_03_executive_desk.png
    P02_BUS_04_office_walk.png
    P02_BUS_05_boardroom.png
    P02_BUS_06_lobby_fullbody.png
  ADR-001-identity-and-pose.md
  P02_BUS_01_headshot_front.png
  P02_BUS_02_window_3q.png
  P02_BUS_03_executive_desk.png
  P02_BUS_04_office_walk.png
  P02_BUS_05_boardroom.png
  P02_BUS_06_lobby_fullbody.png
  P02_BUS_07_private_office.png
  P02_BUS_08_laptop_workspace.png
  P02_BUS_09_window_crossed_arms.png
  P02_BUS_10_editorial_fullbody.png
  README.md
  SESSION_SUMMARY.md
  build_pack.py
  business_manifest.yaml
  validate_pack.py
  FINAL_REPORT.md
```

## git status --short

```text
 M "09 Experiments/identity_benchmark_v1/LOCAL_PULID_BASELINE_V1.md"
 M "09 Experiments/identity_benchmark_v1/P01_M30_Corporate/01_references/references.yaml"
 M "09 Experiments/identity_benchmark_v1/README.md"
 M engine/lora_lab/materialize.py
?? "09 Experiments/identity_benchmark_v1/P01_M30_Corporate/01_references/P01_REF04_right_soft.png"
?? "09 Experiments/identity_benchmark_v1/P01_M30_Corporate/01_references/P01_REF05_left_soft.png"
?? "09 Experiments/identity_benchmark_v1/P01_M30_Corporate/03_benchmark_runs/checkpoint_benchmark_v1/"
?? "09 Experiments/identity_benchmark_v1/P01_M30_Corporate/03_benchmark_runs/flux_kontext_qualifier_v1/"
?? "09 Experiments/identity_benchmark_v1/P01_M30_Corporate/03_benchmark_runs/flux_kontext_repair_v1/"
?? "09 Experiments/identity_benchmark_v1/P01_M30_Corporate/03_benchmark_runs/ideogram_qualifier_v1/"
?? "09 Experiments/identity_benchmark_v1/P01_M30_Corporate/03_benchmark_runs/kandinsky_qualifier_v1/"
?? "09 Experiments/identity_benchmark_v1/P01_M30_Corporate/03_benchmark_runs/local_pulid_baseline_v2/"
?? "09 Experiments/identity_benchmark_v1/P01_M30_Corporate/03_benchmark_runs/local_pulid_baseline_v3/"
?? "09 Experiments/identity_benchmark_v1/P01_M30_Corporate/03_benchmark_runs/local_qualifier_tail_v1/"
?? "09 Experiments/identity_benchmark_v1/P01_M30_Corporate/03_benchmark_runs/pulid_multiscene_v1/"
?? "09 Experiments/identity_benchmark_v1/P01_M30_Corporate/04_lora_training_v1/"
?? "09 Experiments/identity_benchmark_v1/P01_M30_Corporate/04_portfolio/gpt_portfolio_v1/"
?? "09 Experiments/identity_benchmark_v1/P01_M30_Corporate/05_blind_review_v1/"
?? "09 Experiments/identity_benchmark_v1/P01_M30_Corporate/06_final_round_v1/"
?? "09 Experiments/identity_benchmark_v1/P02_F30_Lifestyle/"
```

## git diff --stat

```text
 .../identity_benchmark_v1/LOCAL_PULID_BASELINE_V1.md  | 10 ++++++++++
 .../P01_M30_Corporate/01_references/references.yaml   | 19 +++++++++++++++++++
 09 Experiments/identity_benchmark_v1/README.md        |  5 +++++
 engine/lora_lab/materialize.py                        | 17 +++++++++++++----
 4 files changed, 47 insertions(+), 4 deletions(-)
```

The tracked diff above predates this phase. P02 is untracked, so these new files are absent from ordinary git diff --stat. No staging or commit was performed. Existing P01 changes are not part of this work.

## Suggested commit message — not executed

`feat(onyx): add P02 business portfolio session v1`
