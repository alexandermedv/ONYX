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
compatibility importers. Existing Job Engine, Ensemble Runner, Quality Gate,
FaceFusion, and postprocessing runtimes remain operational and do not yet
consume the v1 contracts.

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
