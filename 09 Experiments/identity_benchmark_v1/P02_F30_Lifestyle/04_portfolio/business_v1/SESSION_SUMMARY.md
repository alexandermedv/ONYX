# P02 BUSINESS V1 — session summary

- Character: `P02_F30_Lifestyle`; identity version 1.
- Session: `P02_BUSINESS_V1`; collection: business.
- Images: 10 saved source candidates, 10 unique SHA256 values.
- Source status: frozen; portfolio status: review; final staging: candidate.
- Packaging date: 2026-09-15. Generation date/model/seed were not supplied.

Scene diversity: frontal headshot; 3/4 executive; seated desk; walking; boardroom;
lobby full-body; seated private office; candid laptop; window profile; editorial
full-body. Manifest descriptions reflect saved images, not idealized prompt results.

Per the supplied session history, initial P02 business generations showed excessive
pose/expression repetition. The prompt strategy was changed to separate identity
preservation from pose preservation, explicitly forbid copying reference pose and
expression, and intentionally vary gaze, expression, body orientation, camera distance
and activity. This lesson is preserved in the verbatim session identity block and
[local decision record](ADR-001-identity-and-pose.md).

Completed locally: immutable source copies, prompt archive, technical QA, empty human
review sheet, candidate staging, 20 web derivatives, 18 marketing layouts and four
copy drafts. No generation, repair, retouch, AI upscale or human scoring was performed.

Review attention: BUS_07 and BUS_10 visibly deviate from several prompt details.
See `02_review/QA_NOTES.md`. Near-duplicate detection was skipped because the existing
repository detector requires unavailable OpenCV. No dependencies were installed.

The available source collage is a JPEG with misleading embedded “REAL PHOTOS” text.
It remains unchanged and is used only as concept provenance. The demo layout instead
uses canonical references with explicit synthetic-character labeling. Canonical
identity PNGs and P01 remain unchanged; no identity version was advanced.

No commit, upload or publication performed. Human review remains the next required step.
