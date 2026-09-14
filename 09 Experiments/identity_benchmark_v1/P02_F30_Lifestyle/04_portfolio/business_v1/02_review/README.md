# Human review — P02 BUSINESS V1

Status: **PENDING, 10 candidates**. Technical QA does not grant portfolio approval.
Open the labeled contact sheet, then inspect each source at 100% alongside MASTER
and REF01–REF05. Use REF03 for body proportions and the full reference set for identity.

The CSV contains no assigned human scores. Score each criterion from 1 to 5:

| Score | Meaning |
|---|---|
| 1 | Major failure; unsuitable in its current form |
| 2 | Obvious problems requiring substantial correction |
| 3 | Usable only with reservations or targeted repair |
| 4 | Strong candidate with minor reservations |
| 5 | Excellent for the intended portfolio use |

| Criterion | Inspect |
|---|---|
| identity | Face shape, proportions, age, eyes, nose, lips, hairline against canonical references |
| realism | Skin texture, lighting, materials and photographic plausibility |
| anatomy | Face, neck, limbs, joints and body proportions |
| hands | Fingers, grips, contact with props and occlusion |
| pose naturalness | Balance, motion and believable body position |
| expression | Natural expression and appropriateness for the scene |
| scene quality | Environment, props, reflections, typography and artifacts |
| portfolio value | Value as an individual business portrait |
| diversity | Added value relative to the other nine frames |

`PENDING` is the initial workflow state, not a completed decision. Completed decisions:

- `PASS`: eligible for final approval; keep the source unchanged.
- `REPAIR`: specify exact defects and review a separate repaired derivative before approval.
- `REGENERATE`: replacement required; this packaging phase does not generate it.
- `REJECT`: never publish this frame.

Identity is the highest priority. Do not average away an identity or anatomy failure
with attractive lighting. Record the reason in `repair_notes` / `comments`.
Qualitative assistant observations live in [QA_NOTES.md](QA_NOTES.md), separate from
your scores. No InsightFace score or human likeness verdict is claimed for this phase.

The initial `03_final` files are candidates, not approved selections. After review,
update the business manifest, selection decisions and derivative manifests consistently;
do not publish stale derivatives containing a rejected or superseded image.
