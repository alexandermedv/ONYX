# Business public export layer

The preferred publishing files are the **18 JPEGs ending `_publish.jpg` and four
copy files ending `_publish.md`**, explicitly listed in `publishing_manifest.yaml`.
Use that list instead of globbing all files in the marketing directories.

Updated public categories: labeled and clean contact sheets; ten Avito carousel cards;
neutral reference-to-business graphic; square selection, story cover, portrait showcase,
clean four-photo and six-photo grids; Avito, website, social and portfolio copy.

These new parallel versions remove visible test/demo/candidate/review labels and the
internal warning footer. Text uses ONYX / Virtual Photo Studio and neutral descriptions.
The comparison uses “Исходный образ персонажа” and “Деловая серия ONYX”; it does not
claim a real client. No repair, retouch or upscale result is invented. No prices or
delivery timelines are asserted.

All existing business files were intentionally left byte-for-byte unchanged, including:

- `business_manifest.yaml` and historical `05_marketing/marketing_manifest.yaml`;
- human review CSV, technical QA CSV and prior validation JSON;
- `SESSION_SUMMARY.md` and historical `FINAL_REPORT.md`;
- original/source/staging PNGs, web derivatives and old marketing layouts/copy.

Files without `_publish` remain historical/internal variants. Internal statuses are
unchanged; public-layout readiness does not auto-approve the session. The new manifest
records input paths/hashes, new output hashes, dimensions and exact rendered public
text. Its approval note is internal and is not drawn onto images.

Built by `../../lifestyle_v1/build_pack.py`, which reads the existing business layout
helpers without changing them. Nothing was uploaded; no commit or push was performed.
