# HomeLab — Change Log

## 2026-09-05
- SSH restored while VPN was active through a static Windows route; route documented in [[05 - Runbook]].
- Disk/SMART audit completed; RAID retirement decision recorded in [[01 - Storage and Disks]].
- Independent external backup created; see [[04 - Backup and Recovery]].
- ClickHouse host port moved 9000 to 9002 to reserve MinIO API port.
- MinIO deployed on 9000/9001; functional and persistence tests passed.
- ClickHouse auth hardening initially failed due permissions, was rolled back, isolated-validated, then deployed successfully with rollback retained.
- PostgreSQL hardened: LAN exposure removed and global trust rules removed; rollback retained.
- Airflow auth/network audited; owner LAN UI retained.
- PasswordAuthentication yes deliberately retained as SSH recovery fallback.
