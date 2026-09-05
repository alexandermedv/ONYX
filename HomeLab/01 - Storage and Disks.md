# HomeLab — Storage and Disks

Related: [[00 - Server Overview]] · [[04 - Backup and Recovery]] · [[06 - SSD Migration Plan]]

## Disks
- /dev/sdd, Seagate 18 TB: system plus /mnt/data (/dev/sdd3, ext4, ~16.3 TiB). SMART: 0 reallocated/pending/offline-uncorrectable/reported-uncorrectable, 36°C, error log empty. UDMA CRC 1595 and Command Timeout 59: check SATA cable, power and port during physical service.
- /dev/sda, Seagate SSHD 1 TB: sole active /dev/md127 member; formally healthy, 29,150 h, no bad sectors; not needed in target architecture.
- /dev/sdb, Toshiba 1 TB: failed former RAID member — 5,784 pending, 255 offline-uncorrectable, 27,433 reported-uncorrectable, 27,588 ATA errors. Never return to RAID or use for new data.
- /dev/sdc, Seagate 250 GB: active swap; 3 reallocated, 653 reported-uncorrectable, 1,555 ATA errors. Retire only after swap moves to SSD.

## RAID
/dev/md127 is degraded RAID1 [U_]. Rebuild is not planned. After system/swap migration, stop it safely and disconnect /dev/sda and /dev/sdb.

> [!danger]
> Never rebuild with /dev/sdb, format /dev/sdd3, or move/resize partitions without an approved backup and plan.
