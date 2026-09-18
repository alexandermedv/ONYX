# Collection Book template specification v1

Status: approved RU editorial reference template. Client-specific copy and asset approval remain required.

JSON data is separate from `template/style.json` and Python layout. Paths resolve against repository root (override `--root`). No P02 identifier is embedded in the renderer.

| Field | Contract |
| --- | --- |
| order_id | Internal manifest only |
| client_display_name | Cover name; empty allowed for sample |
| collection_name, collection_subtitle | Public cover copy |
| cover_image, hero_image | Paths belonging to photos; hero must be first photo |
| photos | Ordered array implementing photo_01 … photo_N; entries path, sha256, caption |
| product_tier | Preview=1, Signature=10, Premium=20 |
| onyx_mission_heading, onyx_mission_text | Opening note from ONYX: mission, approach and thanks; no personal greeting |
| collection_description, collection_use_cases | Short paragraph and up to three short use-case lines |
| onyx_selection_image, onyx_selection_note | Collection image path and public rationale |
| personal_closing_note, closing_heading | Personalized closing copy, grounded in approved persona or client brief |
| next_collections | One or two objects implementing next_collection_01 … next_collection_N |
| next_collections[].name, description | Verified product copy |
| next_collections[].status | available or coming_soon |
| next_collections[].collection_url | Explicit HTTPS URL or null; alias for next_collection_01_url |
| next_collections[].qr_url | Reserved next_collection_01_qr_url; must be null in v1 |
| next_collections[].cta_label | Link label when available; coming_soon renders “Скоро” |
| brand_logo | Approved PNG master; placed on dark cover without distortion |
| brand_variant, language | v1 accepts editorial_v1 and ru; other values fail |
| book_version, created_at | Internal version and date |
| output_stem | Internal safe filename stem |
| sample | Shows ONYX SAMPLE COLLECTION instead of client name |
| motion_asset | null or Premium object {url, cta_label}; HTTPS link, no video embedding |

## Layout and constraints

Six structural pages plus story: Preview 7 pages; Signature 15; Premium 16. Signature uses nine story pages, one pair. Premium uses ten pairs. No extra Preview/Premium PDF is supplied with this reference implementation.

All photographs use contain geometry; no crop or filter. Body and heading wrapping checks reject overflow rather than silently truncate or shrink. Long translations and names may require editorial shortening. Maximum two next collections. QR rendering is deliberately unsupported, not silently ignored. External links are neither fetched nor invented.

## Outputs

PDF, internal YAML 1.2 manifest serialized as JSON, copied structured source_data, and one PNG per page rendered by Poppler. Manifest records exact input paths/SHA256, PDF and preview hashes, placements/reuse and renderer/style/font/logo hashes. Source images are never copied to the sample. Only in-memory JPEG derivatives enter the PDF.

Output must not already contain generated book files. Rebuild to a new version directory, preventing accidental overwrite. A failed run may leave diagnostics/partial outputs; use a fresh directory after fixing the input.

## Reproducibility limits

Deterministic PDF metadata via ReportLab invariant mode. Exact bytes also depend on ReportLab/Pillow/font/Poppler versions; preserve those with the QA report. Source approval is external to this template. Historical stale manifests are preserved and reported, not repaired by the renderer.

## Semantic caption contract

Each `photos[]` entry keeps its editable caption with the approved source image. The optional `page_caption` object records the rendered text, scene semantics and editability:

```json
"page_caption": {"text": "Рабочие детали", "source_scene": "work-detail portrait", "editable": true}
```

Captions must describe the actual image and scene role rather than a page-number slot. QA must include `caption matches actual image content` and must be repeated whenever a photo is replaced.
