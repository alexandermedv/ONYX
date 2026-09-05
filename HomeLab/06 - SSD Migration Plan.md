# HomeLab — SSD Migration Plan

Related: [[00 - Server Overview]] · [[01 - Storage and Disks]] · [[04 - Backup and Recovery]]

## Goal
Clean Ubuntu installation on new 250–500 GB SSD. Keep /dev/sdd3 intact and mount it as /mnt/data.

> [!danger]
> Prefer a clean install, not cloning. Make a fresh backup and preferably disconnect the 18 TB disk during installation so the installer cannot select it.

## Sequence
1. Install Ubuntu on SSD.
2. Reconnect 18 TB disk and identify /dev/sdd3 UUID.
3. Mount as /mnt/data; add correct fstab entry; verify findmnt.
4. Only then install Docker/Compose and restore services.
5. Create swap on SSD; only then retire /dev/sdc.

## Restore
- MinIO: restore /home/alexander/services/minio/, same .env, compatible fixed image, unchanged /mnt/data/minio/data; verify buckets/objects.
- PostgreSQL: retain /mnt/data/postgres; keep logical dumps as independent recovery.
- ClickHouse: retain /mnt/data/clickhouse; restore auth config/.env and localhost-only ports.
- Airflow: restore config, DAGs, plugins and retained pgdata or logical dump.

After validation, remove mdadm/fstab dependencies safely, stop old RAID, then disconnect /dev/sda, /dev/sdb, /dev/sdc.
