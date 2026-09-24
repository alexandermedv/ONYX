# ADR-0008: Local Collection Book reference renderer

Date: 2026-09-17. Status: implemented for internal reference; visual design pending approval.

## Context

ONYX needs a reusable editorial PDF accompanying separate photographs, without changing generation, existing sources or delivery manifests. The workspace contains unrelated uncommitted brand and delivery work.

## Decision

Use a standalone ReportLab renderer under `13 Production/Templates/Collection_Book`, structured JSON order data, existing brand fonts/logo and Poppler page previews. Contain every photograph, preserve input SHA256, record placements and deliberate hero reuse. Support 1/10/20-photo layout planning. Do not integrate automatically into paid delivery yet.

## Consequences

No new heavyweight dependencies or GPU work. Source approval is an external prerequisite; PDF technical QA cannot promote an asset. QR field is reserved and rejects nonempty values. Premium Motion is a separate HTTPS link. Signature reference is visually reviewed; other tier layouts are planner-tested only. The P02 sample uses latest manifest-listed upscale masters while explicitly retaining historical approval conflicts. Owner must approve design before this becomes a delivery default.

See [[../13 Production/Product_Standards/ONYX_COLLECTION_BOOK_STANDARD|Collection Book Standard]] and [[../13 Production/Templates/Collection_Book/README|Renderer]].
