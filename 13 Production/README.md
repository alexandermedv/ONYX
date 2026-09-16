# ONYX Production Core

**Status:** ACTIVE  
**Established:** 2026-09-16

`13 Production` is the canonical product, brand, portfolio and marketing control plane for ONYX. It contains standards, promotion manifests and delivery templates; it does not replace research evidence or silently mutate it.

`09 Experiments` remains the R&D evidence base. An asset may be promoted only through an explicit production manifest after required QA and approval. Promotion records canonical source paths and integrity data. It never changes an experimental source, candidate, review record or historical export in place.

## Structure

- `Brand/` — visual-system specification and future Brand Board template.
- `Product_Standards/` — customer product, portfolio and marketing standards.
- `Portfolio/` — promotion manifests and migration assessments; no copied canonical experiment images.
- `Marketing/` — channel-level production specifications.
- `Client_Delivery/Templates/` — delivery package requirements.

The production status of an asset is determined by its production manifest, not by the existence of a similarly named experimental file. `MISSING`, `PENDING`, and `REPAIR_REQUIRED` must not be replaced by placeholders.

See [[../12 Decisions/ADR-0007 Production Core and R&D Promotion Boundary|ADR-0007]].
