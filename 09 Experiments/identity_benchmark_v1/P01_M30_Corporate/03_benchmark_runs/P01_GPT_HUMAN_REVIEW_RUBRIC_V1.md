# P01 GPT Human Review Rubric v1

Review each candidate beside canonical `REF01`–`REF03`. The Identity Master may be viewed for human benchmark context, but it was not a production generation input. Score the 1–5 fields independently; do not infer a score from the machine metric.

| Score | General meaning |
|---:|---|
| 5 | Strongly meets the stated criterion without material concern. |
| 4 | Meets the criterion; only small, acceptable drift or flaws. |
| 3 | Borderline; visible issue that requires careful delivery judgment. |
| 2 | Material weakness; not acceptable without substantial change. |
| 1 | Severe failure of the criterion. |

## Dimensions

- **identity_fidelity_human** — 5: unmistakably the same person; facial proportions and distinctive traits preserved. 4: clearly the same person with small acceptable drift. 3: recognizable but visibly drifted; borderline for delivery. 2: weak resemblance; likely a different interpretation. 1: effectively a different identity.
- **appearance_fidelity_human** — score preservation of apparent age, hair/hairline, facial hair, facial proportions, natural asymmetry and general appearance. A 5 preserves all materially; a 3 has noticeable drift; a 1 materially changes the person.
- **beautification_drift_human** — 5: no inappropriate beautification; natural appearance preserved. 4: mild polish. 3: noticeable but potentially acceptable polish. 2: strong beautification/modelization. 1: identity materially replaced by an idealized or model-like face.
- **photorealism_human** — 5: convincing professional photograph. 4: minor non-material synthetic cues. 3: noticeable artifacts but possibly usable after review. 2: clear synthetic appearance. 1: obvious synthetic artifact.
- **face_integrity_human** — 5: no visible facial defects. 4: small non-material defect. 3: noticeable defect requiring review. 2: material defect. 1: severe facial defect.
- **hands_integrity_human** — use `N/A` when hands are not materially visible. Otherwise 5: anatomically natural; 3: noticeable issue; 1: severe anatomy/interaction failure.
- **body_pose_human** — use `N/A` only when body/pose is not materially visible. Otherwise 5: plausible, natural posture; 3: awkward or borderline; 1: materially implausible anatomy or pose.
- **scene_compliance_human** — 5: meets the applicable SceneSpec; 3: notable deviation; 1: scene concept materially missed.
- **naturalness_human** — 5: relaxed, plausible expression and body language; 3: mildly staged or artificial; 1: materially unnatural.

## Delivery and decision

`delivery_eligible_human` is a Boolean `yes`/`no` judgment of actual ONYX client-delivery suitability.

Allowed `human_decision` values:

- `PASS` — deliverable without repair.
- `REPAIR` — core image and identity are acceptable, but local repair is needed.
- `REGENERATE` — scene concept is usable, but this candidate should be regenerated.
- `REJECT` — not worth repair or regeneration as a candidate.

Identity is a hard-gate calibration dimension. Premium scene, photorealism, outfit or background quality cannot alone justify `PASS`. If `identity_fidelity_human` is 1 or 2, `PASS` is prohibited. If it is 3, mark the candidate borderline and explicitly justify any `PASS` in `notes`. This is a calibration policy, not a production threshold.
