# P02 BUSINESS V1

**10 candidates preserved; portfolio review pending. Nothing is approved for publication.**

Pipeline:

identity refs → generation → source preservation → technical QA → human review
→ repair/regenerate if needed → final selection → web derivatives → marketing materials

The user supplied the generated images. This phase packages them; it does not run
generation, repairs, retouch or AI upscale. **Source images are immutable.**

| Directory | Current content |
|---|---|
| `00_source` | Ten byte-for-byte copies under requested `_v2` names |
| `01_prompts` | Exact supplied prompts, individual text files and session identity block |
| `02_review` | Empty human scores / PENDING decisions, technical QA, mapping and notes |
| `03_final` | Ten byte-identical candidate staging copies; not approved |
| `04_web` | Ten JPEG + ten WebP candidate derivatives and manifest |
| `05_marketing` | 18 internal JPEG layouts, input/output provenance and four copy drafts |
| `reserve` | Six pre-existing alternatives preserved untouched; not selected |

The ten original root-level PNGs remain untouched. The root → `00_source` mappings
are in `02_review/source_mapping.csv`. `_v2` is the requested package filename suffix,
not independently verified generation history. Do not deduplicate or remove originals.

`business_manifest.yaml` contains session metadata, observed scene descriptions,
source SHA256, dimensions, byte sizes, prompt IDs and explicit candidate status.
All generated `.yaml` files use JSON-compatible YAML 1.2; they can be read with either
a YAML 1.2 parser or Python's `json` module. Unknown generation settings remain null.

See [session summary](SESSION_SUMMARY.md), [QA notes](02_review/QA_NOTES.md),
[review rubric](02_review/README.md), and [final report](FINAL_REPORT.md).

## Reproduction and review

`build_pack.py` uses Python + Pillow with JPEG/WebP support and Windows Segoe UI /
Georgia fonts. On first build use `--request <original request.txt>`; after the prompt
manifest exists, it can be read without the attachment. Different existing output bytes
cause a refusal; source PNGs are never overwritten. The builder does not consume human
decisions or auto-promote candidates. It will refuse to reset an edited review CSV.

`validate_pack.py` checks the package without modifying images. Its optional baseline
argument also verifies P01 and pre-existing P02 files from this preparation phase.
Documentation and copy drafts are maintained independently of the image builder.

The current identity manifest still expects a canonical collage PNG; the available
`../../02_source_generations/Collage.jpg` is preserved as separate concept context.
No JPEG-to-PNG substitution or canonical identity edit occurred in this phase.

Do not commit or publish until user review. Suggested commit message, not executed:
`feat(onyx): add P02 business portfolio session v1`.
