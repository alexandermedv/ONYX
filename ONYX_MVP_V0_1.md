# ONYX — MVP v0.1 Definition of Done

This document defines readiness for first test sales. It is a product and production target, not a claim that every capability is already implemented.

## 1. MVP scope

Product: **ONYX Business v1**.

- Input: 3–5 reference photos of one adult identity.
- Output: 10 delivery-grade business photographs.

## 2. Reference Intake v1

Recommended references: frontal, slight right, slight left, ideally one smile, different days/lighting, clearly visible face, no strong filters and preferably no sunglasses. Professional studio photos are not required; ordinary smartphone photos are a normal supported input.

## 3. Reference QA v1

Check face detection, sufficient visible face area, usable resolution, useful angle coverage, identity consistency, material blur/occlusion and material sunglasses/filters.

Result is **GOOD**, **ACCEPTABLE** or **INSUFFICIENT**. For INSUFFICIENT, ONYX must say which additional reference would improve the set.

## 4. Business Scene Pack v1

The ten canonical scenes are:

| ID | Scene |
|---|---|
| BUS_01 | Classic Business Headshot |
| BUS_02 | Friendly Headshot |
| BUS_03 | Executive 3/4 |
| BUS_04 | By the Window |
| BUS_05 | Meeting Room |
| BUS_06 | At the Desk |
| BUS_07 | Standing in Office |
| BUS_08 | Relaxed Business |
| BUS_09 | Full Body |
| BUS_10 | Premium Hero Portrait |

Each future SceneSpec must describe `scene_id`, name, framing, body pose, head pose, gaze, expression, wardrobe, environment, lighting, difficulty and mandatory constraints. This document fixes the specification; it does not require a SceneSpec code implementation.

## 5. Candidate strategy

Generate multiple candidates per scene. Up to four candidates per scene is a starting baseline, not an immutable requirement of 40 generations. Measure actual Delivery Yield and evolve adaptively only with evidence.

## 6. Candidate statuses

Each candidate conceptually receives one of:

- PASS;
- REPAIR;
- REGENERATE;
- REJECT.

Reasons are logged, for example: `identity_failure`, `wrong_age`, `beautification_drift`, `hand_failure`, `eye_failure`, `skin_artifact`, `blur`, `prompt_failure`, `composition_failure`, `duplicate`, `uncanny` or `other`.

## 7. QA gates

MVP evaluates:

- identity — is it the same person;
- appearance fidelity — age, face, hair, skin and body characteristics;
- face integrity and visible-hand integrity;
- technical quality — blur, obvious artifacts and broken image;
- SceneSpec compliance;
- naturalness;
- diversity of selected finals.

## 8. Decision logic

```text
candidate → QA → PASS / REPAIR / REGENERATE / REJECT
```

Use REPAIR when an image is strong, identity is good and a local defect is plausibly correctable. Use REGENERATE when the scene is needed but its candidate is unsuitable. Use REJECT when it is not worth repairing.

## 9. Human review

MVP allows a human-in-the-loop flow:

```text
candidate pool → machine-assisted shortlist → human review → 10 selected finals
```

Full automation is not a Definition of Done requirement.

## 10. Delivery definition

Final delivery contains 10 images:

```text
WEB/   optimized copies
FULL/  maximum-quality final copies
```

Files must be human-readable and exclude internal technical IDs. Recommended convention: `ONYX_<Client>_01_Headshot.jpg` through `ONYX_<Client>_10_Hero.jpg`. This is a recommended MVP convention, not a final API contract.

## 11. Definition of Done

ONYX MVP v0.1 is ready for test sales when all of the following are true:

- 3–5 reference photos successfully work as input;
- the 10 canonical Business scenes are a fixed specification;
- a full dry-run produces 10 delivery images;
- 0/10 obvious identity failures;
- 0/10 critical face artifacts;
- 0/10 critical hand artifacts where hands are visible;
- at least one full-body image;
- at least three visibly different outfits;
- at least four different environments;
- no more than one excessively similar final pair;
- WEB and FULL delivery are built;
- generation count, applicable cloud cost/local GPU time, operator time, repairs and regenerations are recorded;
- the dry-run finishes without manual chaos, lost files or lost provenance.

Human operator time target is ≤30 minutes. It is a target, not a hard failure for the first engineering dry-run.

## 12. Production metrics

Record at minimum:

- `order_id`, `references_count`, `generated_candidates`;
- `pass_count`, `repair_count`, `regenerate_count`, `reject_count`;
- `final_images`, `cloud_cost`, `local_gpu_minutes`;
- `operator_generation_minutes`, `operator_review_minutes`, `operator_retouch_minutes`, `total_operator_minutes`.

Derived metrics:

- **First Pass Yield** = PASS without repair / generated candidates;
- **Delivery Yield** = delivery-grade images / generated candidates;
- **Cost per Delivery Image** = all measurable generation costs / final delivery images.

## 13. P01 benchmark

The first canonical synthetic benchmark is **P01**. It has one Identity Master, three canonical reference photos and an immutable accepted benchmark identity. The Identity Master is not used as generation input; it is internal benchmark/ground-truth-style evaluation material. Accepted P01 references must not change silently between model comparisons.

## 14. Benchmark strategies

Compare production strategies, not only isolated models:

1. Cloud-only;
2. Local-only;
3. Hybrid cloud master → local/edit variants;
4. LoRA-based.

Compare identity, image quality, Delivery Yield, First Pass Yield, cost, speed, operator time, repair rate and reproducibility.

## 15. Test-sales gate

Test sales may start after a successful P01 full dry-run, an initial portfolio, known production cost/time and a usable delivery process. Do not block them on unfinished mini-LoRA or Kandinsky R&D, an ideal website, a fully automated router/QA, a customer portal or a production DB.

See also: [ONYX Product Vision](ONYX_PRODUCT_VISION.md).
