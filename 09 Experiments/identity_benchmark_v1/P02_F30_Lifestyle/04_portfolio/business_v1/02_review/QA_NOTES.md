# Technical and visual notes

The ten supplied root-level files were mapped by scene ID and visual inspection.
Their names omit `_v2`; the requested canonical packaging names add `_v2`.
This suffix does not establish which generation settings or model were used.
The six `reserve` images are separate earlier alternatives and are not selected.

Technical checks: PNG signature and Pillow verification (including PNG CRC), full
decode, dimensions, exact 3:4 ratio, SHA256 uniqueness and EXIF presence. See
[technical_qa.csv](technical_qa.csv). No images were repaired during these checks.
Near-duplicate detection is **SKIPPED**: the existing repository implementation
`engine/lora_lab/analyzer.py::difference_hash` imports `cv2`, unavailable in the
selected runtime. No replacement detector or dependency was installed.
Exact SHA256 uniqueness does not demonstrate perceptual diversity or identity fidelity.

These are assistant observations for review, not human scores or decisions:

| Scene | Observation / attention point |
|---|---|
| BUS_01 | Near-frontal; confirm head angle and hair arrangement against the stricter frontal prompt. |
| BUS_02 | Three-quarter window portrait; inspect hands at cuff. |
| BUS_03 | Pen and notebook desk scene; inspect pen grip and generated lettering. |
| BUS_04 | Corridor movement; inspect stride and folder-hand contact, background typography. |
| BUS_05 | Forest-green boardroom suit; inspect fingers on chair and background lettering. |
| BUS_06 | Full-body lobby frame; inspect bag handle, fingers and heels. |
| BUS_07 | Hand at chin and soft smile differ from requested armrest position and serious/no-smile expression. |
| BUS_08 | Laptop activity; inspect fingers, screen contact and book/background typography. |
| BUS_09 | Profile and window gaze clearly differentiate this frame. Inspect crossed-arm anatomy. |
| BUS_10 | Dark suit, hands in pockets and slight smile differ from requested ivory/stone suit, leather portfolio and no smile. |

Prompts remain verbatim; observed wardrobe and pose in the manifest describe the
saved image rather than claiming perfect prompt adherence. Reserve files were not
used to silently replace any of these candidates.

The provisional social edit favors BUS_01, 03, 04, 06, 08 and 09 for a mix of face,
activity, full-body, walking and profile. This editorial choice does not approve them.
BUS_07 and BUS_10 remain available in the full contact sheet and staging.

All 18 marketing exports were decoded and inspected in layout previews. Text uses
reserved regions outside photographs; the builder checks text-box overflow. Images
are contained without cropping. Clean sheets deliberately omit the draft footer and
must remain internal until the candidate series is approved.
