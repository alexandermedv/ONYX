# HomeLab — Runbook

Related: [[02 - Services]] · [[03 - Network and Security]] · [[04 - Backup and Recovery]]

## After reboot
Run: lsblk; findmnt /mnt/data; df -hT; docker ps; systemctl --failed.

Check MinIO and open http://192.168.0.11:9001. Check Airflow at http://192.168.0.11:8040. Confirm ClickHouse is localhost-only and PostgreSQL is on 127.0.0.1:5432.

## MinIO does not start
1. Confirm /mnt/data is mounted.
2. Confirm /mnt/data/minio/data and permissions.
3. Check .env, Compose config, logs, and 9000/9001 conflicts.

> [!danger]
> Do not start or restart MinIO, PostgreSQL, or ClickHouse when /mnt/data is missing. Docker could create empty root-filesystem paths instead of using persistent data.

## SSH unavailable
Check VPN bypass route, server IP, UFW, then physical console. Historical Windows route: destination 192.168.0.11/32; gateway 192.168.1.1; Tenda Wi-Fi historical ifIndex 9.

> [!note]
> Verify ifIndex after Windows or driver changes; it can change.
