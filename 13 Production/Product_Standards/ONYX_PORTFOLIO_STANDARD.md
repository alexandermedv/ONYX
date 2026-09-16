# ONYX Portfolio Standard

**Version:** 1.0  
**Date:** 2026-09-16  
**Status:** ACTIVE / Production Standard

## Standard session

A standard session contains ten images. Roles are standardized, while their specific scenes depend on the collection.

| No. | Role |
| --- | --- |
| 01 | HERO |
| 02 | CLOSE |
| 03 | WAIST |
| 04 | SEATED |
| 05 | ENVIRONMENT |
| 06 | ACTION |
| 07 | 3Q_BODY |
| 08 | FULL_BODY |
| 09 | MOOD |
| 10 | EDITORIAL |

## Names

Final portfolio files use `ONYX_<CHARACTER>_<COLLECTION>_01_HERO.jpg` through `ONYX_<CHARACTER>_<COLLECTION>_10_EDITORIAL.jpg`.

```text
ONYX_<CHARACTER>_<COLLECTION>_COVER.jpg
ONYX_<CHARACTER>_<COLLECTION>_BEFORE_AFTER.jpg
ONYX_<CHARACTER>_<COLLECTION>_COLLAGE_4.jpg
ONYX_<CHARACTER>_<COLLECTION>_COLLAGE_6.jpg
ONYX_<CHARACTER>_<COLLECTION>_CONTACT_SHEET.jpg
```

Client delivery uses `ONYX_01.jpg` through `ONYX_10.jpg`.

## Portfolio Ready criteria

- identity master exists;
- canonical references exist;
- 10/10 final scenes exist;
- all 10 passed QA;
- no critical identity or anatomy defects;
- upscale is complete;
- standard exports are complete;
- portfolio-watermark version exists;
- cover, before/after, collage and contact sheet exist.

Canonical experimental images are referenced by promotion manifest. They are not renamed or overwritten to conform to this naming standard.

## Footer placement rule (v1.1)

- Footer is a contained lower field, 230 px in a 1080x1350 portfolio frame (about 17% of height).
- The source portrait is fitted with 	humbnail inside the upper field; never use cover/crop when it can remove a head or face.
- Keep the complete head and hair visible with safe space above; side margins are acceptable.
- Footer may overlap only the lower image boundary through a controlled transition; it must not move the portrait upward or crop the subject.
- Reject any export where a face, head, or critical body area is clipped by the footer.


### Эталонная геометрия framed preview

- Canvas: 1080 x 1350 px, portrait 4:5.
- Photo field: y=0..1120 px; fit with contain/thumbnail and preserve full head.
- Footer field: y=1120..1350 px; height 230 px, full canvas width.
- Stone footer texture is anchored to the lower field and does not resize the photo field.
- Logo lockup stays within the footer safe area; never stretch the monogram vertically.


### Footer lockup alignment

- The top of the monogram ring aligns with the horizontal rule above the copy.
- The bottom of the ONYX wordmark aligns with the bottom of the PORTFOLIO PREVIEW line.
- Logo and copy share one fixed footer alignment zone; do not stretch or independently offset either element.

