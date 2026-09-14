# P02 Lifestyle V1 + business public exports — final report

Package prepared without commit or push. Public presentation is clean; internal review remains PENDING.

## Validation

| Check | Result |
|---|---|
| lifestyle_sources | 10/10 |
| unique_sha256 | 10/10 |
| prompts | 10/10 verbatim |
| manifest_entries | 10/10 |
| review_rows | 10/10 PENDING; all scores blank |
| technical_qa | 10/10 valid PNG, full decode OK, 3:4; EXIF recorded |
| staging_copies | 10/10 byte-identical |
| web_derivatives | 20/20 verified |
| lifestyle_marketing | 18 images + 4 copy files verified |
| replacement_LIFE_10 | 10.png visually confirmed as outdoor evening city; source/staging hashes verified |
| old_office_LIFE_10 | Excluded; superseded history recorded; separate local file not identified |
| business_public_exports | 18 images + 4 copy files verified; _publish preferred |
| business_historical_files | All pre-existing business files byte-identical, including reports/review/QA/manifests |
| public_labels | PASS: rendered text and copy denylist + visual layout inspection; no OCR claim |
| P02_identity | MASTER, REF01–05 and Collage.jpg unchanged; identity metadata unchanged |
| P01 | 501 files unchanged; same inventory |
| unrelated_tracked_changes | Byte-identical to before phase |
| source_PNG_overwritten | False |
| human_review_status | PENDING |
| near_duplicate_detection | SKIPPED: existing detector requires unavailable cv2 |
| commit_created | False |
| push_performed | False |

## Source mapping / SHA256

Root originals → 00_source canonical copies; all originals preserved.

| ID | Original | Canonical | Dimensions | Bytes | SHA256 |
|---|---|---|---|---:|---|
| LIFE_01 | P02_LIFE_01_cafe_window.png | P02_LIFE_01_cafe_window.png | 1086 × 1448 | 2004967 | `bcfc627f4b79a8121fe63e23da8beaf94863443919b4f84cbf66f375a4c5dbb0` |
| LIFE_02 | 2.png | P02_LIFE_02_city_walk.png | 1086 × 1448 | 2215475 | `32c62bb3d78d487cc99116a32be0016d4cb4fff1a1a2625f6653f80d8159615f` |
| LIFE_03 | 3.png | P02_LIFE_03_home_morning.png | 1086 × 1448 | 2104831 | `4418e5052aa0da402f681283afc772c9217b554b610f792c3704a156a413ddc1` |
| LIFE_04 | 4.png | P02_LIFE_04_book_cafe.png | 1086 × 1448 | 2150335 | `99e498e8fb7dc52f5de1283662e31073e7a0d3c9964ab2671c0d370cc571896b` |
| LIFE_05 | 5.png | P02_LIFE_05_rooftop_sunset.png | 1086 × 1448 | 1925488 | `95d6428075a4a5dae69d3d7a3f5ad725235c673d39ce4c5c229626356ac41829` |
| LIFE_06 | 6.png | P02_LIFE_06_weekend_street.png | 1086 × 1448 | 2236512 | `ce833d64a5848dbd99d65f3461a4eece52adaff0aa6eca5a173f72ad079e90a5` |
| LIFE_07 | 7.png | P02_LIFE_07_balcony_profile.png | 1086 × 1448 | 1949554 | `eb66169c9bf98fb30b3bd658a67fe7ec2dee7042d88542975b5d866e2dc81285` |
| LIFE_08 | 8.png | P02_LIFE_08_cozy_sofa.png | 1086 × 1448 | 2346267 | `32985e058fdedb32a2312cce5290844fd05aa99759197bdc70ce97e93156f87e` |
| LIFE_09 | 9.png | P02_LIFE_09_travel_lobby.png | 1086 × 1448 | 2032116 | `c8ef167ddcbf00407611a02fb760a67be47eb3781204e288e605db78b2137b7c` |
| LIFE_10 | 10.png | P02_LIFE_10_evening_city.png | 1086 × 1448 | 1890629 | `dff2f12e84565b150fa999441eb68945eaaaa7ce4ed78621506b179c9899ce2d` |

## LIFE_10 replacement

10.png is the true evening-city image, selected by visual scene inspection and copied without edits. The earlier office-like attempt is superseded according to user history; no local path was identified. It is not in the canonical ten.

## Prompts and technical QA

Ten verbatim supplied prompts plus session identity rule, saved in Markdown/YAML and individual text files. Exact replacement execution prompt, generation model/seed remain unknown. PNG CRC and full decoding pass; exact hashes are unique, dimensions/EXIF recorded in technical_qa.csv. No human scores assigned.

## lifestyle_v1 public assets

| File | Dimensions | Source IDs |
|---|---|---|
| 05_marketing/01_contact_sheet/P02_lifestyle_v1_contact_sheet.jpg | 2400 × 1590 | LIFE_01, LIFE_02, LIFE_03, LIFE_04, LIFE_05, LIFE_06, LIFE_07, LIFE_08, LIFE_09, LIFE_10 |
| 05_marketing/01_contact_sheet/P02_lifestyle_v1_contact_sheet_clean.jpg | 2400 × 1590 | LIFE_01, LIFE_02, LIFE_03, LIFE_04, LIFE_05, LIFE_06, LIFE_07, LIFE_08, LIFE_09, LIFE_10 |
| 05_marketing/02_avito_carousel/P02_lifestyle_card_01.jpg | 1600 × 2000 | LIFE_01, LIFE_05 |
| 05_marketing/02_avito_carousel/P02_lifestyle_card_02.jpg | 1600 × 2000 | LIFE_03, LIFE_06, LIFE_07 |
| 05_marketing/02_avito_carousel/P02_lifestyle_card_03.jpg | 1600 × 2000 | LIFE_01, LIFE_02, LIFE_03, LIFE_05, LIFE_09, LIFE_10 |
| 05_marketing/02_avito_carousel/P02_lifestyle_card_04.jpg | 1600 × 2000 | LIFE_06, LIFE_04, LIFE_08 |
| 05_marketing/02_avito_carousel/P02_lifestyle_card_05.jpg | 1600 × 2000 | LIFE_02, LIFE_08 |
| 05_marketing/02_avito_carousel/P02_lifestyle_card_06.jpg | 1600 × 2000 | Text only |
| 05_marketing/02_avito_carousel/P02_lifestyle_card_07.jpg | 1600 × 2000 | Text only |
| 05_marketing/02_avito_carousel/P02_lifestyle_card_08.jpg | 1600 × 2000 | LIFE_01, LIFE_03, LIFE_05, LIFE_06, LIFE_09, LIFE_10 |
| 05_marketing/02_avito_carousel/P02_lifestyle_card_09.jpg | 1600 × 2000 | LIFE_03, LIFE_10 |
| 05_marketing/02_avito_carousel/P02_lifestyle_card_10.jpg | 1600 × 2000 | LIFE_07, LIFE_09 |
| 05_marketing/03_before_after/P02_reference_to_lifestyle.jpg | 2100 × 1400 | LIFE_03, LIFE_10, MASTER, REF03 |
| 05_marketing/04_social/P02_lifestyle_square_selection.jpg | 1600 × 1600 | LIFE_01, LIFE_03, LIFE_05, LIFE_06 |
| 05_marketing/04_social/P02_lifestyle_story_cover.jpg | 1080 × 1920 | LIFE_05 |
| 05_marketing/04_social/P02_lifestyle_portrait_showcase.jpg | 1600 × 2000 | LIFE_01, LIFE_06, LIFE_09 |
| 05_marketing/04_social/P02_lifestyle_clean_grid_4.jpg | 1800 × 2440 | LIFE_01, LIFE_05, LIFE_06, LIFE_07 |
| 05_marketing/04_social/P02_lifestyle_clean_grid_6.jpg | 2100 × 2020 | LIFE_01, LIFE_03, LIFE_05, LIFE_06, LIFE_07, LIFE_09 |

Copy files:

- 05_marketing/05_copy/avito_description_v1.md
- 05_marketing/05_copy/website_lifestyle_collection_v1.md
- 05_marketing/05_copy/short_social_caption_v1.md
- 05_marketing/05_copy/portfolio_caption_v1.md

## business_v1 public assets

| File | Dimensions | Source IDs |
|---|---|---|
| 05_marketing/01_contact_sheet/P02_business_v1_contact_sheet_publish.jpg | 2400 × 1590 | BUS_01, BUS_02, BUS_03, BUS_04, BUS_05, BUS_06, BUS_07, BUS_08, BUS_09, BUS_10 |
| 05_marketing/01_contact_sheet/P02_business_v1_contact_sheet_clean_publish.jpg | 2400 × 1590 | BUS_01, BUS_02, BUS_03, BUS_04, BUS_05, BUS_06, BUS_07, BUS_08, BUS_09, BUS_10 |
| 05_marketing/02_avito_carousel/P02_business_card_01_publish.jpg | 1600 × 2000 | BUS_01, BUS_06 |
| 05_marketing/02_avito_carousel/P02_business_card_02_publish.jpg | 1600 × 2000 | BUS_01, BUS_03, BUS_09 |
| 05_marketing/02_avito_carousel/P02_business_card_03_publish.jpg | 1600 × 2000 | BUS_01, BUS_04, BUS_05, BUS_06 |
| 05_marketing/02_avito_carousel/P02_business_card_04_publish.jpg | 1600 × 2000 | BUS_08, BUS_04, BUS_09 |
| 05_marketing/02_avito_carousel/P02_business_card_05_publish.jpg | 1600 × 2000 | BUS_02, BUS_07 |
| 05_marketing/02_avito_carousel/P02_business_card_06_publish.jpg | 1600 × 2000 | Text only |
| 05_marketing/02_avito_carousel/P02_business_card_07_publish.jpg | 1600 × 2000 | Text only |
| 05_marketing/02_avito_carousel/P02_business_card_08_publish.jpg | 1600 × 2000 | BUS_01, BUS_03, BUS_04, BUS_06, BUS_08, BUS_09 |
| 05_marketing/02_avito_carousel/P02_business_card_09_publish.jpg | 1600 × 2000 | BUS_01, BUS_09 |
| 05_marketing/02_avito_carousel/P02_business_card_10_publish.jpg | 1600 × 2000 | BUS_06, BUS_08 |
| 05_marketing/03_before_after/P02_reference_to_business_publish.jpg | 2100 × 1400 | BUS_01, BUS_06, MASTER, REF03 |
| 05_marketing/04_social/P02_business_square_selection_publish.jpg | 1600 × 1600 | BUS_01, BUS_03, BUS_04, BUS_06 |
| 05_marketing/04_social/P02_business_story_cover_publish.jpg | 1080 × 1920 | BUS_06 |
| 05_marketing/04_social/P02_business_portrait_showcase_publish.jpg | 1600 × 2000 | BUS_01, BUS_08, BUS_09 |
| 05_marketing/04_social/P02_business_clean_grid_4_publish.jpg | 1800 × 2440 | BUS_01, BUS_04, BUS_06, BUS_08 |
| 05_marketing/04_social/P02_business_clean_grid_6_publish.jpg | 2100 × 2020 | BUS_01, BUS_03, BUS_04, BUS_06, BUS_08, BUS_09 |

Copy files:

- 05_marketing/05_copy/avito_description_v1_publish.md
- 05_marketing/05_copy/website_business_collection_v1_publish.md
- 05_marketing/05_copy/short_social_caption_v1_publish.md
- 05_marketing/05_copy/portfolio_caption_v1_publish.md

## lifestyle_v1 tree

```text
lifestyle_v1/
  00_source/
    P02_LIFE_01_cafe_window.png
    P02_LIFE_02_city_walk.png
    P02_LIFE_03_home_morning.png
    P02_LIFE_04_book_cafe.png
    P02_LIFE_05_rooftop_sunset.png
    P02_LIFE_06_weekend_street.png
    P02_LIFE_07_balcony_profile.png
    P02_LIFE_08_cozy_sofa.png
    P02_LIFE_09_travel_lobby.png
    P02_LIFE_10_evening_city.png
  01_prompts/
    LIFE_01.txt
    LIFE_02.txt
    LIFE_03.txt
    LIFE_04.txt
    LIFE_05.txt
    LIFE_06.txt
    LIFE_07.txt
    LIFE_08.txt
    LIFE_09.txt
    LIFE_10.txt
    P02_lifestyle_v1_prompts.md
    P02_lifestyle_v1_prompts.yaml
    session_identity_block.md
  02_review/
    P02_lifestyle_v1_review.csv
    QA_NOTES.md
    README.md
    source_mapping.csv
    technical_qa.csv
    validation.json
  03_final/
    P02_LIFE_01_cafe_window.png
    P02_LIFE_02_city_walk.png
    P02_LIFE_03_home_morning.png
    P02_LIFE_04_book_cafe.png
    P02_LIFE_05_rooftop_sunset.png
    P02_LIFE_06_weekend_street.png
    P02_LIFE_07_balcony_profile.png
    P02_LIFE_08_cozy_sofa.png
    P02_LIFE_09_travel_lobby.png
    P02_LIFE_10_evening_city.png
    README.md
  04_web/
    jpg/
      P02_LIFE_01_cafe_window_web.jpg
      P02_LIFE_02_city_walk_web.jpg
      P02_LIFE_03_home_morning_web.jpg
      P02_LIFE_04_book_cafe_web.jpg
      P02_LIFE_05_rooftop_sunset_web.jpg
      P02_LIFE_06_weekend_street_web.jpg
      P02_LIFE_07_balcony_profile_web.jpg
      P02_LIFE_08_cozy_sofa_web.jpg
      P02_LIFE_09_travel_lobby_web.jpg
      P02_LIFE_10_evening_city_web.jpg
    webp/
      P02_LIFE_01_cafe_window_web.webp
      P02_LIFE_02_city_walk_web.webp
      P02_LIFE_03_home_morning_web.webp
      P02_LIFE_04_book_cafe_web.webp
      P02_LIFE_05_rooftop_sunset_web.webp
      P02_LIFE_06_weekend_street_web.webp
      P02_LIFE_07_balcony_profile_web.webp
      P02_LIFE_08_cozy_sofa_web.webp
      P02_LIFE_09_travel_lobby_web.webp
      P02_LIFE_10_evening_city_web.webp
    README.md
    web_manifest.csv
  05_marketing/
    01_contact_sheet/
      P02_lifestyle_v1_contact_sheet.jpg
      P02_lifestyle_v1_contact_sheet_clean.jpg
    02_avito_carousel/
      P02_lifestyle_card_01.jpg
      P02_lifestyle_card_02.jpg
      P02_lifestyle_card_03.jpg
      P02_lifestyle_card_04.jpg
      P02_lifestyle_card_05.jpg
      P02_lifestyle_card_06.jpg
      P02_lifestyle_card_07.jpg
      P02_lifestyle_card_08.jpg
      P02_lifestyle_card_09.jpg
      P02_lifestyle_card_10.jpg
    03_before_after/
      P02_reference_to_lifestyle.jpg
      before_after_concept.md
    04_social/
      P02_lifestyle_clean_grid_4.jpg
      P02_lifestyle_clean_grid_6.jpg
      P02_lifestyle_portrait_showcase.jpg
      P02_lifestyle_square_selection.jpg
      P02_lifestyle_story_cover.jpg
    05_copy/
      avito_description_v1.md
      portfolio_caption_v1.md
      short_social_caption_v1.md
      website_lifestyle_collection_v1.md
    README.md
    marketing_manifest.yaml
  10.png
  2.png
  3.png
  4.png
  5.png
  6.png
  7.png
  8.png
  9.png
  ADR-001-public-layout-and-review-state.md
  P02_LIFE_01_cafe_window.png
  README.md
  SESSION_SUMMARY.md
  build_pack.py
  lifestyle_manifest.yaml
  validate_pack.py
  FINAL_REPORT.md
```

## git status --short

```text
 M "09 Experiments/identity_benchmark_v1/LOCAL_PULID_BASELINE_V1.md"
 M "09 Experiments/identity_benchmark_v1/P01_M30_Corporate/01_references/references.yaml"
 M "09 Experiments/identity_benchmark_v1/P02_F30_Lifestyle/README.md"
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
?? "09 Experiments/identity_benchmark_v1/P02_F30_Lifestyle/04_portfolio/business_v1/05_marketing/01_contact_sheet/P02_business_v1_contact_sheet_clean_publish.jpg"
?? "09 Experiments/identity_benchmark_v1/P02_F30_Lifestyle/04_portfolio/business_v1/05_marketing/01_contact_sheet/P02_business_v1_contact_sheet_publish.jpg"
?? "09 Experiments/identity_benchmark_v1/P02_F30_Lifestyle/04_portfolio/business_v1/05_marketing/02_avito_carousel/P02_business_card_01_publish.jpg"
?? "09 Experiments/identity_benchmark_v1/P02_F30_Lifestyle/04_portfolio/business_v1/05_marketing/02_avito_carousel/P02_business_card_02_publish.jpg"
?? "09 Experiments/identity_benchmark_v1/P02_F30_Lifestyle/04_portfolio/business_v1/05_marketing/02_avito_carousel/P02_business_card_03_publish.jpg"
?? "09 Experiments/identity_benchmark_v1/P02_F30_Lifestyle/04_portfolio/business_v1/05_marketing/02_avito_carousel/P02_business_card_04_publish.jpg"
?? "09 Experiments/identity_benchmark_v1/P02_F30_Lifestyle/04_portfolio/business_v1/05_marketing/02_avito_carousel/P02_business_card_05_publish.jpg"
?? "09 Experiments/identity_benchmark_v1/P02_F30_Lifestyle/04_portfolio/business_v1/05_marketing/02_avito_carousel/P02_business_card_06_publish.jpg"
?? "09 Experiments/identity_benchmark_v1/P02_F30_Lifestyle/04_portfolio/business_v1/05_marketing/02_avito_carousel/P02_business_card_07_publish.jpg"
?? "09 Experiments/identity_benchmark_v1/P02_F30_Lifestyle/04_portfolio/business_v1/05_marketing/02_avito_carousel/P02_business_card_08_publish.jpg"
?? "09 Experiments/identity_benchmark_v1/P02_F30_Lifestyle/04_portfolio/business_v1/05_marketing/02_avito_carousel/P02_business_card_09_publish.jpg"
?? "09 Experiments/identity_benchmark_v1/P02_F30_Lifestyle/04_portfolio/business_v1/05_marketing/02_avito_carousel/P02_business_card_10_publish.jpg"
?? "09 Experiments/identity_benchmark_v1/P02_F30_Lifestyle/04_portfolio/business_v1/05_marketing/03_before_after/P02_reference_to_business_publish.jpg"
?? "09 Experiments/identity_benchmark_v1/P02_F30_Lifestyle/04_portfolio/business_v1/05_marketing/04_social/P02_business_clean_grid_4_publish.jpg"
?? "09 Experiments/identity_benchmark_v1/P02_F30_Lifestyle/04_portfolio/business_v1/05_marketing/04_social/P02_business_clean_grid_6_publish.jpg"
?? "09 Experiments/identity_benchmark_v1/P02_F30_Lifestyle/04_portfolio/business_v1/05_marketing/04_social/P02_business_portrait_showcase_publish.jpg"
?? "09 Experiments/identity_benchmark_v1/P02_F30_Lifestyle/04_portfolio/business_v1/05_marketing/04_social/P02_business_square_selection_publish.jpg"
?? "09 Experiments/identity_benchmark_v1/P02_F30_Lifestyle/04_portfolio/business_v1/05_marketing/04_social/P02_business_story_cover_publish.jpg"
?? "09 Experiments/identity_benchmark_v1/P02_F30_Lifestyle/04_portfolio/business_v1/05_marketing/05_copy/avito_description_v1_publish.md"
?? "09 Experiments/identity_benchmark_v1/P02_F30_Lifestyle/04_portfolio/business_v1/05_marketing/05_copy/portfolio_caption_v1_publish.md"
?? "09 Experiments/identity_benchmark_v1/P02_F30_Lifestyle/04_portfolio/business_v1/05_marketing/05_copy/short_social_caption_v1_publish.md"
?? "09 Experiments/identity_benchmark_v1/P02_F30_Lifestyle/04_portfolio/business_v1/05_marketing/05_copy/website_business_collection_v1_publish.md"
?? "09 Experiments/identity_benchmark_v1/P02_F30_Lifestyle/04_portfolio/business_v1/05_marketing/PUBLISHING_NOTES.md"
?? "09 Experiments/identity_benchmark_v1/P02_F30_Lifestyle/04_portfolio/business_v1/05_marketing/publishing_manifest.yaml"
?? "09 Experiments/identity_benchmark_v1/P02_F30_Lifestyle/04_portfolio/lifestyle_v1/"
```

## git diff --stat

```text
 .../identity_benchmark_v1/LOCAL_PULID_BASELINE_V1.md  | 10 ++++++++++
 .../P01_M30_Corporate/01_references/references.yaml   | 19 +++++++++++++++++++
 .../identity_benchmark_v1/P02_F30_Lifestyle/README.md |  6 ++++++
 09 Experiments/identity_benchmark_v1/README.md        |  5 +++++
 engine/lora_lab/materialize.py                        | 17 +++++++++++++----
 5 files changed, 53 insertions(+), 4 deletions(-)
```

New lifestyle/public exports are untracked, so ordinary git diff --stat does not include them. The only changed existing P02 file is its README, updated to link the new packages. Existing business records remain byte-identical.

## Suggested commit message — not executed

`feat(onyx): add P02 lifestyle portfolio session v1 and publish-ready business materials`
