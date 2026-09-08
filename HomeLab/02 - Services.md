# HomeLab — Services

Related: [[03 - Network and Security]] · [[04 - Backup and Recovery]] · [[05 - Runbook]] · [[08 - ONYX Storage Layout]]

## MinIO
- Container minio; image minio/minio:RELEASE.2025-09-07T16-13-09Z.
- Digest sha256:14cea493d9a34af32f524e538b8346cf79f3321eff8e708c1e2960462bd8936e.
- Compose: /home/alexander/services/minio/compose.yaml; data: /mnt/data/minio/data.
- Root/admin credentials: /home/alexander/services/minio/.env, mode 600; restart unless-stopped; healthy.
- LAN API 9000 and Console 9001. Functional and persistence tests passed.

### MinIO credentials
- Root/admin credentials: `/home/alexander/services/minio/.env`.
- Daily user `alexander` credentials: `/home/alexander/services/minio/users/alexander.env` (mode 600).
- Private bucket: `alexander`.
- Policy: `alexander-bucket-rw`; it permits list/read/write/delete and multipart-compatible object operations only in bucket `alexander`.
- The daily user has no MinIO administrative rights and no access to other buckets.

> [!danger]
> Do not store plaintext passwords or secret keys in Obsidian. This vault records credential-file paths only. Use root credentials only for MinIO administration.

### ONYX internal storage
- Private bucket: `onyx`; it is the internal source of truth for ONYX application artifacts and client delivery material.
- Logical layout and client conventions: [[08 - ONYX Storage Layout]].
- User `alexander` has additional policy `onyx-bucket-rw`, scoped only to the `onyx` bucket; it has no MinIO administrative rights.
- Delivery source path: `onyx/clients/<CLIENT_ID>/06_delivery/`.
- Delivery remote: `rclone` at `/usr/bin/rclone`, Ubuntu package `1.53.3-4ubuntu1.22.04.5` (reports `rclone v1.53.3-DEV`).
- rclone config: `/home/alexander/.config/rclone/rclone.conf`, mode 600; remotes `minio-onyx` and `yandex-onyx`. The MinIO remote uses `http://127.0.0.1:9000` and ordinary user credentials only.
- Delivery boundary: copy only `onyx/clients/<CLIENT_ID>/06_delivery/` to `yandex-onyx:ONYX/Clients/<CLIENT_ID>/`; never export raw/work/QA material.
- A synthetic `CL-2026-TEST` transfer, repeat copy, and size check passed; test objects were removed from both sides.

## ClickHouse
- yandex/clickhouse-server, version 22.1.3.7; data /mnt/data/clickhouse.
- Localhost only: 127.0.0.1:8123 and 127.0.0.1:9002.
- Auth XML: /home/alexander/services/clickhouse/users.d/onyx-local-auth.xml, mode 644; plaintext credential .env, mode 600.
- SQL without credentials is rejected; authenticated HTTP/native works.

## PostgreSQL my-postgres
- Data /mnt/data/postgres; mae_db ~589 MiB; SCRAM HBA; restart unless-stopped.
- Localhost only: 127.0.0.1:5432.

### PostgreSQL access from Windows / pgAdmin
PostgreSQL is intentionally not published to the LAN. Its host bind is `127.0.0.1:5432`. From Windows, use a pgAdmin SSH Tunnel.

**Connection tab**
- Host name/address: `127.0.0.1`
- Port: `5432`
- Maintenance database: `postgres`
- Username: `postgres` or the required PostgreSQL DB user

**SSH Tunnel tab**
- Use SSH tunneling: enabled
- Tunnel host: `192.168.0.11`
- Tunnel port: `22`
- Username: `alexander`
- Authentication: Identity file
- Identity file: `C:\Users\ME\.ssh\id_ed25519`

Critical distinction: SSH user = `alexander`; PostgreSQL DB user = `postgres`. These are separate accounts. Store their credentials in Bitwarden (`HomeLab – Ubuntu Server` and `HomeLab – PostgreSQL postgres`), never in Obsidian.

```yaml
pgAdmin on Windows
    |
    | SSH tunnel
    | user: alexander
    v
192.168.0.11:22
    |
    | localhost on Ubuntu
    v
127.0.0.1:5432
    |
    | PostgreSQL auth
    | user: postgres
    v
my-postgres
```

## Airflow
- 2.10.5; FabAuthManager; login required; alexandermed is Admin.
- LAN UI: 192.168.0.11:8040.
- Paths: /home/alexander/install/airflow/pgdata, logs, plugins; /home/alexander/git/airflow.

## Nextcloud
No active installation. Preserve /mnt/data/recovered-nextcloud-2026-08-30 until an explicit decision.

> [!note]
> Initial ClickHouse hardening failed because XML was 600 alexander:alexander and container user clickhouse could not read it. Validated XML is 644 because it contains only a hash; .env remains 600.
