# ADR-001 — Separate public layouts from internal review state

Status: accepted for P02 portfolio packaging only.

Public images and copy carry branding and collection descriptions without internal
workflow labels. Machine-readable session/review records remain the authority for
approval. Business clean exports use `_publish` filenames and a separate publishing
manifest, preserving all historical outputs and their provenance byte-for-byte.
Lifestyle uses the same separation from its initial finalized candidate set.

This is an export decision, not production integration or an identity-provider change.
No global pipeline, generation settings or canonical identity assets were changed.
Every public derivative is traceable to input hashes, so later review decisions can
identify which exports need replacement without overwriting source photographs.
