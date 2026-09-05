# HomeLab — Backup and Recovery

Related: [[01 - Storage and Disks]] · [[05 - Runbook]] · [[06 - SSD Migration Plan]]

## External backup
- Windows external HDD My Passport, NTFS, ~1 TB, Healthy/Online.
- Path: E:\\alexander-server-backup\\2026-09-05.
- Current payload: ~28.8 GB.
- Includes user data, from_pgk, recovered Nextcloud, PostgreSQL dumps, Airflow config/plugins/DAGs, Docker/ClickHouse snapshots, MinIO config, .env, migration README.

> [!warning]
> .env files contain secrets. Treat the external disk and backup directory as confidential.

## PostgreSQL dumps
- mae_db.dump: ~56 MiB; custom format; pg_restore -l valid; SHA-256 a1096950c7bce299f17f08ca660c12c1b084ca1fc98add9a26b34eda34faac17.
- airflow.dump: ~15 MiB; custom format; pg_restore -l valid; SHA-256 2aa7b5bbbfec4ae0fd88f8f913bae8d38f7a261c23dd43c1ca1f81636753bd09.

Verify after copy with Get-FileHash and the recorded SHA-256 values.

## Rollback inventory
- ClickHouse: clickhouse-server.rollback-pre-auth-2026-09-05, clickhouse-server.failed-auth-2026-09-05, clickhouse-server.pre-minio-2026-09-05, isolated diagnostics.
- PostgreSQL: my-postgres.rollback-pre-hardening-2026-09-05.
- Snapshots: /home/alexander/backups/pre-minio-2026-09-05/{clickhouse,postgres-hardening,security}/.

Do not remove rollback artifacts before separately approved cleanup after sustained stable operation.
