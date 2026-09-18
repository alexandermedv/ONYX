# P02 Business Collection Book v1

This is an internal reference implementation of ONYX Collection Book v1.

Status: DESIGN_APPROVED_REFERENCE. Revision 11: 15 pages, 1080 × 1350 logical units (4:5), 8,903,521 bytes (8.49 MiB). Russian Signature sample, 10 unique photographs.

Revision 11 changes the cover subtitle to “Деловая фотосессия для уверенного профессионального образа”. Page 02 is labelled “Обращение от ONYX”. On the final slide, Lifestyle and Dating move 115 logical units closer to the one-line continuation title. This approved reference supersedes the earlier design drafts.

Anna is the approved fictional display persona for this demo only. Her internal profile and writing boundaries are in [ANNA_P02_SYNTHETIC_PERSONA.md](../../Portfolio/P02/ANNA_P02_SYNTHETIC_PERSONA.md). Collection differences and recommendation rules are in [ONYX Collection Catalog](../../Product_Standards/ONYX_COLLECTION_CATALOG.md).

The latest layout assessment is in [Style review revision 11](STYLE_REVIEW_REVISION_11.md).

## Source decision

Used the ten existing upscale masters listed in `13 Production/Portfolio/P02/Business_V1/client_delivery/CLIENT_DELIVERY_MANIFEST_V1.json`. All ten actual SHA256 values match that manifest. These are later delivery assets, not experimental candidates or watermarked marketing composites. No high-resolution images copied here; originals remain unchanged.

Important provenance limitation: historical PORTFOLIO_EXPORT_MANIFEST.json still says portfolio_ready=false and blocks upscale/delivery; experimental review has ten PENDING decisions. New delivery records establish asset lineage, not explicit human final approval. This sample does not resolve or overwrite those records and must not be described as publication-approved.

Cover and ONYX Selection both use ONYX_P02_BUSINESS_01_HERO_00001_.png: existing production role HERO and corresponding marketing cover select the same scene. No numerical best-image score was invented. The hero is deliberately reused on cover, story and Selection; every other image appears once. Cover branding uses the approved `ONYX_MONOGRAM_ONYX_SILK_PRESENTATION_V1.png` without alteration.

## Sources

- `13 Production/Portfolio/P02/Business_V1/upscale_p02_v1/ONYX_P02_BUSINESS_01_HERO_00001_.png` — SHA256 `87d60ba2aa6b7a945dfff026deeb2edceae55dcd83ccfd226a87dc52c23f6de5`
- `13 Production/Portfolio/P02/Business_V1/upscale_p02_v1/ONYX_P02_BUSINESS_02_CLOSE_00001_.png` — SHA256 `378d9b4765d424109dc31313b12b5c57210bf8ee51d2d80b3d88c807d8274f64`
- `13 Production/Portfolio/P02/Business_V1/upscale_p02_v1/ONYX_P02_BUSINESS_03_WAIST_00001_.png` — SHA256 `604ec0f11536878ebb3918ba6082d62b1a5e5ed6e2101d15d8be74d606f090ab`
- `13 Production/Portfolio/P02/Business_V1/upscale_p02_v1/ONYX_P02_BUSINESS_04_SEATED_00001_.png` — SHA256 `22cb1099114606567744c539a6ba64ce90b0353a70529428acbc43406d7025d3`
- `13 Production/Portfolio/P02/Business_V1/upscale_p02_v1/ONYX_P02_BUSINESS_05_ENVIRONMENT_00001_.png` — SHA256 `15415ded6e8ed38410f4febd055fb254439b991c728f1d997d6afb558a46a86f`
- `13 Production/Portfolio/P02/Business_V1/upscale_p02_v1/ONYX_P02_BUSINESS_06_ACTION_00001_.png` — SHA256 `629792d14515181552ce7dd8baff31e579766799860cf4bc2f4a44db257cb309`
- `13 Production/Portfolio/P02/Business_V1/upscale_p02_v1/ONYX_P02_BUSINESS_07_3Q_BODY_00001_.png` — SHA256 `c2921f002ad69122e3d79d293f37bf06521ef045c8a5e5d544cc9f678b69be41`
- `13 Production/Portfolio/P02/Business_V1/upscale_p02_v1/ONYX_P02_BUSINESS_08_FULL_BODY_00001_.png` — SHA256 `6d12a1579b0aed24b30cfeb06cc7c4e1a2d4880de3f03be5551f81b29d5f2c7b`
- `13 Production/Portfolio/P02/Business_V1/upscale_p02_v1/ONYX_P02_BUSINESS_09_MOOD_00001_.png` — SHA256 `1e6add2717d2c0b5fce67db77b6d1d6ab9cd0830e951d9f1f160737cecd9aa99`
- `13 Production/Portfolio/P02/Business_V1/upscale_p02_v1/ONYX_P02_BUSINESS_10_EDITORIAL_00001_.png` — SHA256 `0b3e04685cd5523e751fba7dc0154c80e4dc9080d5c7ad80fb995e3ab5ee1c3d`

## Build and QA

Renderer: local ReportLab; Pillow in-memory JPEG copies (2048 px maximum edge, quality 92); pypdf extraction; Poppler JPEG previews. Exact source, font, logo, renderer, style, PDF and page hashes are in the manifest. JSON serialization in the .yaml file is valid YAML 1.2.

Run from repository root:

```powershell
& 'C:/Users/ME/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' '13 Production/Templates/Collection_Book/render_collection_book.py' --data '13 Production/Templates/Collection_Book/example_data/P02_BUSINESS_COLLECTION_BOOK_v1.json' --output '13 Production/Samples/P02_Business_Collection_Book_v1_rebuild'
```

Use a new output directory. Tests: 3 passing; unique planner coverage for 1/10/20, unsupported counts, privacy tokens. Only Signature has an end-to-end visual sample. All 15 JPEG previews were rendered from this PDF and decoded. Embedded custom fonts, text bounds/glyph coverage, privacy scan, image geometry, expected page count and unchanged source hashes passed. Pages 01, 02, 03, 06, 07, 13 and 14 were inspected at full size. No layout clipping or broken photographs observed. Phone-scale dense paired photos may need zoom. Font weight uses the bundled variable-font default; final typography is subject to design approval.

Next products are documented Lifestyle/Executive, conservatively labelled “Скоро”. No destination URLs invented. QR rendering is reserved; optional Premium Motion supports a separate HTTPS link only.

The PDF alone is client-facing. Anna is a fictional sample persona; replace all sample copy with an approved client brief before any client-facing delivery. Do not distribute source_data, manifests, preflight or QA reports: they intentionally contain internal identifiers and paths. No identity re-evaluation or image repair occurred. Commit/push not performed.
