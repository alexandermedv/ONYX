# ONYX Orders

Orders are separate production entities and reference their client through `client_id`.

- Canonical order ID: `ORD-{year}-{number}`.
- Human-readable folder: `ORD-{year}-{number}_{client_id}_{client_slug}`.
- The folder name assists people; `order.yaml` remains the machine-readable source of truth.

For new soft-launch orders, record reference-QA/scope/quote confirmation before the payment step, then `payment_status` and receipt evidence before production. On final resolution set `resolution_status`, an offset-aware `order_closed_at`, and `retention_until` (30 calendar days later); update `refund_status` and deletion status/date where applicable. These are documentation-level metadata fields described in [Product configuration](../Product_Standards/products_v1.yaml); existing order records and runtime contracts are not migrated automatically.

Follow [Data Retention & Deletion](../Client_Experience/Intake/ONYX_DATA_RETENTION_AND_DELETION_v1.md) for manual asset deletion. After image deletion, retain only necessary minimal order/payment/consent evidence and approved anonymized metrics. Do not copy client images into Git or marketing without separate permission.
