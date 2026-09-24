# ONYX

## Current content model

Production content is organized around a single package per synthetic character:

```text
01_Characters   character identity, sessions, branded derivatives and history
02_Marketing    shared ONYX campaign deliverables
03_Standards    stable brand, product, portfolio and client-experience rules
04_Templates    reusable templates only
09 Experiments  R&D history, benchmarks and model experiments
D:\AI\ONYX_Clients  real client data outside the Git repository
```

The legacy `13 Production` content migration is complete; that root is retired and must not be recreated. Technical roots such as `engine`, `scripts`, `tests`, `config` and model/workflow directories remain in place.

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
- [ONYX Product Vision](ONYX_PRODUCT_VISION.md)
- [ONYX MVP v0.1 Definition of Done](ONYX_MVP_V0_1.md)

## Repository structure

- `01_Characters/` — authoritative synthetic identities and their sessions.
- `02_Marketing/` — shared ONYX campaigns and channel exports.
- `03_Standards/` — stable Brand, Product, Portfolio, Marketing and Client Experience rules.
- `04_Templates/` — reusable generic templates.
- `09 Experiments/` — preserved R&D evidence.
- `engine/` — production runtime and execution code.
- `docs/` — architecture decisions and historical knowledge base.
- `D:\AI\ONYX_Clients` — real client assets and orders outside Git.

See [Repository Structure](REPOSITORY_STRUCTURE.md).

## Roadmap

See [Roadmap](docs/Knowledge_Base/Roadmap/Roadmap.md).

## License

MIT
