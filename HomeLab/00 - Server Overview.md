# HomeLab — Server Overview

## Quick links
- [[01 - Storage and Disks]]
- [[02 - Services]]
- [[03 - Network and Security]]
- [[04 - Backup and Recovery]]
- [[05 - Runbook]]
- [[06 - SSD Migration Plan]]
- [[07 - Change Log]]

## Current server
- Hostname: alexander-server
- Hardware: Dell Precision WorkStation T3500
- CPU: Xeon E5645, 6C/12T; RAM ~27 GiB
- Ubuntu Server 22.04.5 LTS; kernel 6.8.0-138-generic
- LAN: 192.168.0.11 on wlp3s0; gateway 192.168.0.1

## Architecture
### Current
- System partitions and /mnt/data are on the 18 TB /dev/sdd.
- /dev/sdd3 is ext4 mounted at /mnt/data; MinIO is live.
- Old RAID1 exists but is not part of the target architecture; /dev/sdc provides active swap.

### Target
New 250–500 GB SSD: Ubuntu, EFI/boot, swap, Docker/Compose, /etc, /home/alexander/services, Airflow config/code.

18 TB Seagate: persistent data only — archives, MinIO, PostgreSQL/ClickHouse data.

> [!danger]
> Do not format /dev/sdd3, resize/move partitions, or run fsck while it is mounted.
