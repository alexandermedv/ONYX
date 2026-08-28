# ONYX

Helping people look the way they want to look.

------------------------------------------------

ONYX is an AI portrait generation and image-production platform focused on
identity fidelity, photorealism, reproducibility, and commercial quality.

Key features

• Identity preservation
• Automated generation pipeline
• Modular architecture
• Commercial-quality portraits
• Knowledge base
• Workflow automation

## Architecture status

Phase 1A implements the canonical contract layer: JobSpec v1, Manifest v1,
normalized result entities, validation, atomic persistence, and read-only
compatibility importers. Phase 1B.1 adds machine-local RuntimeConfig and
side-effect-free JobSpec → immutable ExecutionPlan materialization. Phase
1B.2 adds the canonical generation shell, orchestrator-owned incremental
Manifest persistence, retries, and resume. Phase 1B.3 connects the first real,
non-identity-aware `SceneGenerator`: a FLUX adapter using the ComfyUI HTTP API.
A controlled Windows smoke and same-manifest resume completed successfully.
Existing Job Engine, Ensemble Runner, Quality Gate, FaceFusion, identity,
postprocessing, and delivery runtimes remain outside the canonical shell.

- [[Pipeline Architecture]]
- [[JobSpec and Manifest v1]]
- [[Engineering]]

## Repository structure

01 Brand
02 Business
03 Product
04 Engineering
05 AI Pipeline
...

## Roadmap

See 10 Roadmap/

## License

MIT
