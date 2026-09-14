# Lifestyle human review

All ten rows start with `decision=PENDING`; all scores, repair notes and comments
are blank. The assistant does not supply human scores. Review each full-size source
against MASTER and REF01–REF05; use REF03 as the primary body-proportion reference.

| Score | Meaning |
|---|---|
| 1 | Major failure |
| 2 | Clear problem requiring significant work |
| 3 | Usable only with reservations or targeted repair |
| 4 | Strong with minor reservations |
| 5 | Excellent for the intended use |

| Field | Assess |
|---|---|
| identity | Facial identity, age, shape, eyes, nose, lips, hairline |
| realism | Photographic plausibility, skin and material texture, lighting |
| anatomy | Proportions, joints and face/limb structure |
| hands | Fingers, grips and contact with props |
| pose_naturalness | Balance, motion and relaxed body position |
| expression | Natural emotion and appropriateness to the scene |
| scene_quality | Environment, reflections, props, lettering |
| portfolio_value | Usefulness of the individual image |
| diversity | Distinct contribution to the ten-image series |

Identity fidelity has priority over aesthetics. A high aggregate score must not hide
identity drift or an anatomical defect.

Completed decisions: PASS, REPAIR, REGENERATE, REJECT. PENDING is an initial state.
PASS may enter a reviewed delivery set; REPAIR needs a separately approved derivative;
REGENERATE needs a replacement; REJECT must not be published. Keep originals unchanged
and retain review history. Public layout readiness does not grant human approval.

Technical QA records PNG validity, full decode, dimensions, ratio, exact hash duplicate
check and EXIF presence. It does not measure identity or approve anatomy.
