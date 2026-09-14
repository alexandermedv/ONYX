# Candidate staging — not approved final delivery

`portfolio_status: candidate` for these ten byte-for-byte staging copies.
Session-level `portfolio_status: review` remains in `business_manifest.yaml`.
Each staging PNG must have the same SHA256 as its `00_source` counterpart.

- PASS → confirm or copy the reviewed file to final and record approval explicitly.
- REPAIR → separate repaired derivative only after approval; preserve source PNG.
- REGENERATE → replacement required; no generation is authorized by this staging step.
- REJECT → never publish; exclude from final delivery and subsequent marketing exports.

No current file is approved merely because it is inside `03_final`.
