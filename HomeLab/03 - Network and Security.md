# HomeLab — Network and Security

Related: [[02 - Services]] · [[05 - Runbook]] · [[07 - Change Log]]

LAN is 192.168.0.0/24; server 192.168.0.11 on wlp3s0. No global IPv6 is currently assigned.

## Service policy
- LAN: SSH 22, Airflow 8040, MinIO API 9000, MinIO Console 9001.
- localhost: PostgreSQL 5432, ClickHouse HTTP 8123, ClickHouse native 9002.

## Firewall
- UFW active; logging low; incoming deny, outgoing allow, routed deny.
- SSH is allowed from 192.168.0.0/24 on wlp3s0; IPv6 SSH is link-local fe80::/10 only.
- DOCKER-USER routes to HOMELAB-INGRESS: established/related return; LAN source via wlp3s0 return; other forwarded wlp3s0 traffic drop.

Docker-published Airflow/MinIO are LAN-only for current IPv4. Revisit policy if global IPv6, a new subnet, or a new published Docker service appears.

## SSH decision
PubkeyAuthentication yes; PasswordAuthentication yes; PermitRootLogin without-password; PermitEmptyPasswords no; X11Forwarding yes.

> [!warning]
> Keep PasswordAuthentication yes. ED25519 is preferred, but password login is the recovery fallback after a prior SSH lockout caused by excessive hardening. Do not disable it without a proven second recovery path or local/out-of-band console and explicit owner approval.

## Router checklist
- [ ] Port Forwarding / Virtual Server
- [ ] DMZ host
- [ ] UPnP / NAT-PMP mappings
- [ ] Remote WAN administration
- [ ] IPv6 firewall
