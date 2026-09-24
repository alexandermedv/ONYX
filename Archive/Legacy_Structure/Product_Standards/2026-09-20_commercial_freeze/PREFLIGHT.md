# Commercial freeze pre-flight — 2026-09-20

Working directory: D:\AI\ONYX
Branch: main
HEAD: 885ffba9ea099778e228a89a92c91f90398e0045
Initial status: **168 entries**, dirty; all pre-existing work treated as user-owned. Full output: [initial_git_status.txt](initial_git_status.txt).

Structure: Brand, Client_Delivery, Client_Experience, Clients, Marketing, Orders, Portfolio, Product_Standards, Samples, Templates.

| Document | Current value before task | Conflict / no conflict | Proposed action |
|---|---|---|---|
| Product System / Price Book / products_v1.yaml | Preview 900; credits 2100/4100; Premium Motion | Conflict | Frozen three-tier line, stable IDs, explicit history |
| Service Standard | Payment → Intake → QA; payment/refund TBD | Conflict | QA first, prepayment and resolution rules |
| Reference Guide / QA | Quality-based references; QA handoff straight to production | Partial | Keep flexible reference rule; payment gate after QA |
| Consent & Privacy | Separate consents; no retention duration | No product conflict; blocker | Preserve policy; owner decision flagged |
| Intake schema/examples | PREVIEW, SIGNATURE, PREMIUM | Conflict | PORTRAIT mapping/example; legacy retained |
| Marketing / Avito | Ten-photo focus; Avito folder only .gitkeep | Conflict | Public line and requirements, no final Pack |
| Collection Book / renderer | Preview capability; 10/20 layouts | Partial | Entitlements distinct from renderer; no new PDF |
| Portfolio / Delivery | Ten-frame Signature path | Partial | Explicit tier scope and manual packaging boundary |
| Human QA | Existing order PASS and local quality_gate | No conflict; no unified commercial standard | Add final human checklist, preserve evidence |
| 03 Product | Older tiers / multiple Collections | Conflict | Mark SUPERSEDED, keep content |
| Roadmap | Technical milestones | Partial | Add 80/20 commercial priority |
| Readiness / KPI / Corrections | No unified files found | Missing | Add documentation/schema |

Executable consumers of products_v1.yaml: none found in repository search. Existing Signature/Premium keys and legacy Preview are retained. No external consumer compatibility is asserted.
