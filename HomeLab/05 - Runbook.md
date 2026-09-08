# HomeLab — Runbook

Related: [[02 - Services]] · [[03 - Network and Security]] · [[04 - Backup and Recovery]] · [[08 - ONYX Storage Layout]]

## After reboot
Run: lsblk; findmnt /mnt/data; df -hT; docker ps; systemctl --failed.

Check MinIO and open http://192.168.0.11:9001. Check Airflow at http://192.168.0.11:8040. Confirm ClickHouse is localhost-only and PostgreSQL is on 127.0.0.1:5432.

## MinIO does not start
1. Confirm /mnt/data is mounted.
2. Confirm /mnt/data/minio/data and permissions.
3. Check .env, Compose config, logs, and 9000/9001 conflicts.

## Where to find MinIO credentials
- Root/admin: `/home/alexander/services/minio/.env`
- Daily user: `/home/alexander/services/minio/users/alexander.env`

On the server, view only when necessary:

```bash
cat /home/alexander/services/minio/.env
cat /home/alexander/services/minio/users/alexander.env
```

> [!danger]
> Never copy credential-file contents into Obsidian, chat logs, or git.

## Create an ONYX client prefix
1. Allocate the next immutable client ID in the form `CL-YYYY-NNNN`; do not use a client name as the storage identifier.
2. Create `onyx/clients/<CLIENT_ID>/metadata.json` from the minimal schema in [[08 - ONYX Storage Layout]].
3. Create the defined client-stage prefixes as the pipeline first writes to them. If empty-prefix visibility is required, create a minimal `.keep` object through the approved S3 client.
4. Write final client files only to `onyx/clients/<CLIENT_ID>/06_delivery/`, named `ONYX_<CLIENT_ID>_<SERIES>_<NN>.jpg`.
5. Do not copy `00_intake`, `01_references`, `02_raw`, `03_work`, `04_qa`, or `05_selected` to Yandex Disk.

### Check ONYX MinIO policy
The user `alexander` must have `onyx-bucket-rw` in addition to the pre-existing `alexander-bucket-rw`. The policy allows list/read/write/delete and multipart-compatible object operations only in the `onyx` bucket; it does not allow MinIO administration.

### ONYX delivery to Yandex Disk
Before copying, confirm the client ID, that only `06_delivery/` is selected, and that neither test nor real source data is missing:

```bash
rclone lsf minio-onyx:onyx/clients/<CLIENT_ID>/06_delivery/
```

Copy a finished delivery prefix with:

```bash
rclone copy \
  minio-onyx:onyx/clients/<CLIENT_ID>/06_delivery/ \
  yandex-onyx:ONYX/Clients/<CLIENT_ID>/ \
  --progress
```

Verify the result without changing either side:

```bash
rclone check \
  minio-onyx:onyx/clients/<CLIENT_ID>/06_delivery/ \
  yandex-onyx:ONYX/Clients/<CLIENT_ID>/ \
  --size-only
```

Use `rclone copy` as the standard safe delivery command: it does not delete destination-only files. Do **not** run `rclone sync` automatically; it can delete destination files that are absent from MinIO.

The configured remotes are `minio-onyx` and `yandex-onyx`; their credentials remain only in `/home/alexander/.config/rclone/rclone.conf` (mode 600), never in this vault or git. On this rclone version, `minio-onyx` is configured with `no_check_bucket=true` because the older client otherwise performs an unnecessary bucket check against the already-existing private bucket.

If an upload returns `AccessDenied`, do not expand MinIO policy or use root credentials first. Confirm that the command uses `minio-onyx`, the destination starts with `onyx/`, and the remote retains `no_check_bucket=true`.

> [!danger]
> Do not start or restart MinIO, PostgreSQL, or ClickHouse when /mnt/data is missing. Docker could create empty root-filesystem paths instead of using persistent data.

## pgAdmin cannot connect to PostgreSQL
If the PostgreSQL connection times out:

1. Do not re-open PostgreSQL on `0.0.0.0`.
2. Confirm that pgAdmin uses an SSH Tunnel.
3. In **Connection**, use host `127.0.0.1` and port `5432`.
4. In **SSH Tunnel**, use host `192.168.0.11`, SSH username `alexander`, and key `C:\Users\ME\.ssh\id_ed25519`.
5. Set the PostgreSQL username separately in **Connection**.

Incident record: pgAdmin could not establish the SSH Tunnel when its SSH username was incorrectly set to `postgres`. Changing the SSH Tunnel username to `alexander` made the ED25519-key connection work.

> [!warning]
> Do not open PostgreSQL port `5432` back to the LAN solely for pgAdmin. Use the SSH Tunnel.

> [!danger]
> Store credentials in Bitwarden (`HomeLab – Ubuntu Server`, `HomeLab – PostgreSQL postgres`). Never copy passwords or a private key into Obsidian or git.

## SSH unavailable
Check VPN bypass route, server IP, UFW, then physical console. Historical Windows route: destination 192.168.0.11/32; gateway 192.168.1.1; Tenda Wi-Fi historical ifIndex 9.

> [!note]
> Verify ifIndex after Windows or driver changes; it can change.
