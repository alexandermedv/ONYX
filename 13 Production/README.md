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
- `Templates/Collection_Book/` — local JSON-to-PDF reference renderer for 1/10/20-photo books; not yet a delivery default.
- `Samples/P02_Business_Collection_Book_v1/` — 15-page Signature reference, technical QA complete, owner design approval pending. Historical source-approval conflicts are documented in its README.

Collection Book requirements: [[Product_Standards/ONYX_COLLECTION_BOOK_STANDARD]]. Architectural decision: [[../12 Decisions/ADR-0008 Collection Book Reference Renderer]].

The production status of an asset is determined by its production manifest, not by the existence of a similarly named experimental file. `MISSING`, `PENDING`, and `REPAIR_REQUIRED` must not be replaced by placeholders.

See [[../12 Decisions/ADR-0007 Production Core and R&D Promotion Boundary|ADR-0007]].

## CURRENT commercial freeze — 2026-09-20

Commercial source of truth: [ONYX_COMMERCIAL_PRODUCT_SYSTEM_v1](Product_Standards/ONYX_PRODUCT_SYSTEM.md), **FROZEN_FOR_SOFT_LAUNCH**. Machine-readable mirror: [products_v1.yaml](Product_Standards/products_v1.yaml). Portrait 1000 RUB / 1 final; Signature 3000 RUB / 10; Premium 5000 RUB / 20. Premium has one main Collection and deeper Concepts, not multiple complete Collections by default.

[Launch readiness](Product_Standards/ONYX_LAUNCH_READINESS_CHECKLIST_v1.md) separates frozen scope from demonstrated operations. [History](Product_Standards/ONYX_COMMERCIAL_VERSION_HISTORY_v1.md) preserves superseded values. [KPI](Product_Standards/ONYX_LAUNCH_KPI_v1.md) defines manual measurement and the 10-paid-order review. Documentation/config updated; runtime generation, Book rendering and delivery code are unchanged.

## Soft-launch operations — 2026-09-21

[Data Retention & Deletion](Client_Experience/Intake/ONYX_DATA_RETENTION_AND_DELETION_v1.md) sets a 30-calendar-day maximum for client image assets after `CLOSED`, early deletion checks and a manual checklist. [Service Standard](Product_Standards/ONYX_SERVICE_STANDARD_v1.md) documents payment, cancellation, refund and compatible mapping to existing order states. The current readiness decision is **READY_FOR_AVITO_LAUNCH_PACK**. Exact public legal Terms can receive separate review; no automatic deletion or new runtime state machine is implemented.
