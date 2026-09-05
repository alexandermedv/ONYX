# HomeLab — Services

Related: [[03 - Network and Security]] · [[04 - Backup and Recovery]] · [[05 - Runbook]]

## MinIO
- Container minio; image minio/minio:RELEASE.2025-09-07T16-13-09Z.
- Digest sha256:14cea493d9a34af32f524e538b8346cf79f3321eff8e708c1e2960462bd8936e.
- Compose: /home/alexander/services/minio/compose.yaml; data: /mnt/data/minio/data.
- Credentials: /home/alexander/services/minio/.env, mode 600; restart unless-stopped; healthy.
- LAN API 9000 and Console 9001. Functional and persistence tests passed.

## ClickHouse
- yandex/clickhouse-server, version 22.1.3.7; data /mnt/data/clickhouse.
- Localhost only: 127.0.0.1:8123 and 127.0.0.1:9002.
- Auth XML: /home/alexander/services/clickhouse/users.d/onyx-local-auth.xml, mode 644; plaintext credential .env, mode 600.
- SQL without credentials is rejected; authenticated HTTP/native works.

## PostgreSQL my-postgres
- Data /mnt/data/postgres; mae_db ~589 MiB; SCRAM HBA; restart unless-stopped.
- Localhost only: 127.0.0.1:5432.

## Airflow
- 2.10.5; FabAuthManager; login required; alexandermed is Admin.
- LAN UI: 192.168.0.11:8040.
- Paths: /home/alexander/install/airflow/pgdata, logs, plugins; /home/alexander/git/airflow.

## Nextcloud
No active installation. Preserve /mnt/data/recovered-nextcloud-2026-08-30 until an explicit decision.

> [!note]
> Initial ClickHouse hardening failed because XML was 600 alexander:alexander and container user clickhouse could not read it. Validated XML is 644 because it contains only a hash; .env remains 600.
