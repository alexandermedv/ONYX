# Client migration report

Date: 2026-09-24

Checkpoint: `f74915e907fdf53de303187c816696cd7c6e6aeb`

## Result

Private client material was copied to the external client root and verified before source cleanup.

- verified files: 766
- verified SHA256 checks: 766
- failed verifications: 0
- Alexander verified files: 286
- Valentina verified files: 480
- external root: `D:\\AI\\ONYX_Clients`

The detailed source-to-destination verification table is kept outside Git with the client storage operator and is not committed here.

## Cleanup

- Alexander private order data, client metadata, experiment datasets, and training material were verified and removed from the repository working tree.
- `val4.jpg` was verified and moved to the Valentina external references area.
- Tracked Valentina order metadata and client-specific helper files were verified and removed from the repository index.
- Active Valentina WIP source trees remain in place after copy and verification. They are deferred as `COPIED_WIP_PENDING_SOURCE_CLEANUP` to preserve the active workflow.

## Deferred WIP

Deferred source material is limited to active Valentina WIP under the legacy order tree, Valentina generation results, quality-gate output, temporary Collection Book review output, and the pre-cleanup review image. No unrelated character, portfolio, engine, or marketing WIP was changed.

## Privacy checks

The repository was scanned for active client-specific tracked paths and client-like binaries after staging. Generic templates and historical technical references remain where they do not contain client payloads. The next cleanup pass can remove the deferred Valentina WIP after its workflow is closed.

Known historical experiment references to legacy client labels and example source paths remain in generic benchmark documentation/configuration. They contain no client payloads and were left unchanged to avoid changing experiment behavior; converting these configs to `ONYX_CLIENT_ROOT` is recorded as `DEFERRED_CODE_UPDATE`.
