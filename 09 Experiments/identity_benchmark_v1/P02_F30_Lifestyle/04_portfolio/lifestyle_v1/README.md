# P02 LIFESTYLE V1

Ten saved lifestyle photographs packaged as a `finalized_candidate_set`.
Human review remains `PENDING`; the public graphics intentionally carry no workflow
labels. Clean presentation does not change internal approval state.

| Directory | Contents |
|---|---|
| `00_source` | 10 immutable byte-for-byte canonical copies |
| `01_prompts` | 10 verbatim supplied prompts, individual text files, session identity block |
| `02_review` | Empty human scores, PENDING decisions, technical QA, mapping, validation |
| `03_final` | 10 byte-identical staging copies |
| `04_web` | 10 JPEG + 10 WebP derivatives and provenance CSV |
| `05_marketing` | 18 clean layouts, four copy files, marketing provenance |

The ten original root-level PNGs remain unchanged. Mapping was checked visually
before copying. `10.png` is the outdoor evening-city replacement used for LIFE_10.
The earlier office-like attempt is non-canonical / superseded according to the
user-provided history, but no separate local file could be identified. No filename
or hash is invented and no reserve asset was deleted.

Pipeline: identity references → manually generated images → source preservation
→ technical QA → human review → repair/replacement if needed → final selection
→ web exports → public layouts. This phase starts from supplied images; it performs
no generation, repair, retouch or AI upscale. Sources are immutable.

Web exports cap the long edge at 1600 px without enlarging smaller sources. JPEG
uses quality 95 and no chroma subsampling; WebP uses quality 95 / method 6. Aspect
ratio is preserved. Layouts contain complete photographs without cropping.

See [session summary](SESSION_SUMMARY.md), [review rubric](02_review/README.md),
[QA notes](02_review/QA_NOTES.md), [manifest](lifestyle_manifest.yaml) and
[final report](FINAL_REPORT.md). Marketing input/output hashes are in
`05_marketing/marketing_manifest.yaml`.

## Reproduction

`build_pack.py --request <original request.txt>` uses existing Python/Pillow plus
the committed sibling business builder's font, wrapping and image-containment
helpers. It reads that module with `runpy` and never edits it or creates bytecode.
It also creates parallel business `_publish` exports. A different existing output
causes refusal rather than overwriting source files or human review history.
Windows Segoe UI and Georgia fonts are required; no automatic installation occurs.
All new YAML files use the JSON-compatible YAML 1.2 syntax.

`validate_pack.py` verifies files, manifests, public text and preservation against
the pre-work snapshot. No generation settings or exact replacement execution prompt
were available beyond the user-supplied prompt archive; unknown values remain null.

No commit or push in this phase. Review is still required.
