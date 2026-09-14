# P02_F30_Lifestyle — canonical identity v1

Synthetic ONYX portfolio character. `identity_version: 1`, `status: frozen`.
Structure follows P01_M30_Corporate; P02 has its own five-reference semantics.

## Current state

Canonical asset inventory is **incomplete: 6/7 present**. The expected canonical collage
PNG is missing; an existing `02_source_generations/Collage.jpg` is separate source context.
Frozen status records the selected identity and does not imply complete provenance.
The user supplied ten business portfolio candidates. The [P02 BUSINESS V1 package](04_portfolio/business_v1/README.md)
preserves them, archives prompts and includes technical QA, candidate staging, web
exports and internal marketing drafts. Human review is pending. This packaging phase
did not run generation, training, repair or identity scoring and did not change canonical PNGs.

The [P02 LIFESTYLE V1 package](04_portfolio/lifestyle_v1/README.md) now preserves ten
lifestyle candidates, including the evening-city LIFE_10 replacement, with prompts,
technical QA, staging, web exports and clean public layouts. Human review remains pending.
Business has parallel [preferred publishing exports](04_portfolio/business_v1/05_marketing/PUBLISHING_NOTES.md);
its historical manifests, review/QA and reports are unchanged.

## Metadata

- [Identity manifest](identity_manifest.yaml): canonical paths, roles, SHA256 and validation.
- [Master metadata](00_master/master_metadata.yaml).
- [Reference metadata](01_references/references_metadata.yaml).
- [Source provenance](02_source_generations/README.md).

All asset paths in YAML are relative to this character directory.
`00_master/Master.png` was copied byte-for-byte to the canonical MASTER filename.
The source was preserved at preparation but disappeared before final review without an
agent deletion or move. The canonical MASTER still matches its recorded source hash.
Existing REF01–REF05 were preserved unchanged.

## Identity semantics

- **MASTER**: Primary canonical identity anchor.
- **REF01**: Frontal phone-style portrait, face-focused, no hand on face.
- **REF02**: 3/4 facial reference with different head angle.
- **REF03**: Lighter clothing, more distant framing, primary body-proportion reference.
- **REF04**: Dark outfit, more distant lifestyle/body reference.
- **REF05**: Seated pose, beige/light outfit, different styling and pose, diversity reference.
- **APPROVED_COLLAGE**: Original approved collage: visual source from which the character identity was established.

## Canonical policy

All earlier P02 reference attempts are **non-canonical**. Do not use them as identity
anchors, canonical benchmark inputs or substitutes for this frozen set. No separate
historical attempt files were identified during preparation; no filenames are invented.
The exact paths and hashes in the manifest define the present canonical assets.
Do not modify or replace canonical PNGs. Identity changes require a new identity version.
The missing approved collage must be supplied as the original approved file; do not
reconstruct or regenerate it. Then calculate its SHA256 and refresh manifest validation.

## Layout

```text
P02_F30_Lifestyle/
  00_master/
  01_references/
  02_source_generations/
  03_benchmark_runs/
  04_lora_training_v1/
  04_portfolio/
  05_blind_review_v1/
  06_final_round_v1/
  identity_manifest.yaml
  README.md
```

Empty work directories contain `.gitkeep` so the structure can be preserved in Git.
This preparation changes only P02 files; it does not register a production pipeline.
