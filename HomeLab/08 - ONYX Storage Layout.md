# HomeLab — ONYX Storage Layout

Related: [[00 - Server Overview]] · [[02 - Services]] · [[05 - Runbook]]

## Purpose and boundary
MinIO bucket `onyx` is ONYX's private internal source of truth. It is not public and clients do not receive direct S3 access. The delivery boundary is only `clients/<CLIENT_ID>/06_delivery/` to Yandex Disk through the configured `rclone` remotes.

S3 has object prefixes, not real directories. To make the common shared layout visible in MinIO Console, the bucket contains minimal `.keep` marker objects. Client-stage prefixes should appear as the pipeline writes real content; do not create client records or personal data merely to pre-populate empty folders.

## Bucket prefixes

```text
onyx/
├── clients/
│   └── CL-YYYY-NNNN/
│       ├── 00_intake/
│       ├── 01_references/
│       ├── 02_raw/
│       ├── 03_work/
│       ├── 04_qa/
│       ├── 05_selected/
│       ├── 06_delivery/
│       ├── 90_exports/
│       ├── 99_archive/
│       └── metadata.json
├── portfolio/{characters,business,dating,family,fantasy,before-after}/
├── templates/{prompts,scenes,delivery,metadata}/
├── shared/{brand,logos,backgrounds,overlays,reference-assets}/
├── exports/{yandex,manual,temporary}/
└── system/{manifests,reports,qa,logs}/
```

- `00_intake`: client inputs and briefs; `01_references`: approved identity/style references.
- `02_raw`: model output; `03_work`: retouch and intermediate variants; `04_qa`: QA and review artifacts; `05_selected`: finalists.
- `06_delivery`: final customer-ready files only.
- `90_exports`: temporary packages and external-publication preparation; `99_archive`: closed-order archive.
- `system/` contains only ONYX application manifests, reports, QA artifacts, and application-level logs. Never put Linux logs, `.env` files, passwords, or tokens in S3.

## Client and delivery conventions
- Client ID: `CL-YYYY-NNNN`, for example `CL-2026-0001`. Client name/PII belongs in approved metadata or a database, not the primary S3 path.
- Delivery filename: `ONYX_<CLIENT_ID>_<SERIES>_<NN>.jpg`, for example `ONYX_CL-2026-0001_EXECUTIVE_01.jpg`.
- Do not rename or move existing content automatically.

## Minimal client metadata

```json
{
  "client_id": "CL-2026-0001",
  "created_at": "2026-09-06T00:00:00Z",
  "service_type": "executive_portraits",
  "status": "active",
  "source_count": 0,
  "selected_count": 0,
  "delivery_count": 0,
  "delivery_target": "yandex_disk",
  "retention_policy": "pending",
  "notes": ""
}
```

Keep this metadata operational and minimize personal data. Never store credentials, tokens, passwords, or secret keys.

## Access and delivery export
- User `alexander` has `onyx-bucket-rw`, which is limited to list/read/write/delete and multipart-compatible object operations in `onyx` only. It has no MinIO admin or IAM-management rights.
- Bucket `alexander` and its existing `alexander-bucket-rw` policy remain separate.
- Only final delivery files may cross this boundary:

```text
onyx/clients/<CLIENT_ID>/06_delivery/
        ↓
    rclone copy
        ↓
Yandex Disk / ONYX / Clients / <CLIENT_ID>/
```

- Use `rclone copy minio-onyx:onyx/clients/<CLIENT_ID>/06_delivery/ yandex-onyx:ONYX/Clients/<CLIENT_ID>/ --progress`; run `rclone check --size-only` after a delivery.
- Never use `rclone sync` as the default delivery command because it can delete destination-only files.
- rclone and Yandex credentials are configured only in the mode-600 server-side config. They must never be placed in this vault, git, a script, or a chat.
