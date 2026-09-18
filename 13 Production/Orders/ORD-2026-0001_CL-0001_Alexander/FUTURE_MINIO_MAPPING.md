# Future MinIO mapping — documentation only

No objects have been uploaded. The approved storage layout currently uses client-oriented prefixes (`onyx/clients/<CLIENT_ID>/...`), while this order folder keeps the dry-run order lifecycle locally.

For a future order-oriented mapping, the intended logical view is:

```text
onyx/orders/ORD-2026-0001/
├── intake/
├── references/
├── production/
├── candidates/
├── qa/
├── final/
├── collection_book/
└── delivery/
```

This is a future mapping only. It does not override `HomeLab/08 - ONYX Storage Layout.md`, does not create MinIO prefixes, and requires an owner-approved storage decision before use.
