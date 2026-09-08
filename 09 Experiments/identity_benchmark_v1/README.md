# ONYX Identity Benchmark v1

`identity_benchmark_v1` defines reproducible synthetic-identity comparisons for ONYX. It records benchmark metadata and immutable assets; it does not itself run generation or modify a production pipeline.

## P01 v1.0

P01_M30_Corporate is the first frozen synthetic identity. Its canonical assets are immutable within version 1.0:

- `00_master/P01_identity_master_v1.png` is the **Identity Master**. It is used only for internal evaluation and must never be a generation input.
- `01_references/P01_REF01_frontal.png`, `P01_REF02_right_3q.png`, and `P01_REF03_left_3q_smile.png` are the three canonical generation inputs.

Model comparisons must use the same reference set and the same SceneSpecs. Replacing a canonical reference requires a new benchmark identity version rather than an unrecorded edit to P01 v1.0.

The four canonical assets are tracked as immutable benchmark provenance. Pre-canonical source generations, contact sheets and future benchmark-run outputs remain local generated artifacts; they are not benchmark ground truth.

## Layout

```text
P01_M30_Corporate/
├── 00_master/              identity master and frozen metadata
├── 01_references/          generation-input references and hashes
├── 02_source_generations/  local pre-canonical provenance
├── 03_benchmark_runs/      local future execution outputs
└── 04_portfolio/           local review/portfolio outputs
```

See `benchmark_spec.yaml` for the comparison schema and `business_scene_pack_v1.yaml` for the model-neutral Business Scene Pack.

## Registered runs

- [P01 GPT BUS_01 v1](P01_M30_Corporate/03_benchmark_runs/gpt_BUS_01_v1/README.md) — provisional exploratory run; strict provenance is not verified.
- [P01 GPT BUS_03 v1](P01_M30_Corporate/03_benchmark_runs/gpt_BUS_03_v1/README.md) — provisional exploratory run; strict provenance is not verified.
- [P01 GPT BUS_05 v1](P01_M30_Corporate/03_benchmark_runs/gpt_BUS_05_v1/README.md) — provisional exploratory run; strict provenance is not verified.
