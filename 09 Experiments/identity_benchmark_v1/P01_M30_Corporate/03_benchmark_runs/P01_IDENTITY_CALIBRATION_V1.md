# P01 Identity Calibration v1 — first GPT human review

## Dataset and method

This exploratory calibration covers 13 saved candidates from the P01 v1.0 GPT series: BUS_01 (3), BUS_03 (3), BUS_05 (3), BUS_09 (1, incomplete) and BUS_10 (3). The machine metric is InsightFace `buffalo_l` cosine similarity on `CPUExecutionProvider`, compared independently with canonical REF01–REF03; the Identity Master was not used in the aggregate.

Human evaluation follows [P01 GPT Human Review Rubric v1](P01_GPT_HUMAN_REVIEW_RUBRIC_V1.md). Only dimensions explicitly reviewed by the human reviewer are populated in the CSV; all other human fields remain blank.

## Candidate review record

| Scene | Candidate | Machine mean | Face area | Human identity | Decision |
|---|---|---:|---:|---:|---|
| BUS_01 | C01 | 0.885309 | 0.211538 | 5 | PASS |
| BUS_01 | C02 | 0.867965 | 0.154447 | 5 | PASS |
| BUS_01 | C03 | 0.872464 | 0.160004 | 5 | PASS |
| BUS_03 | C01 | 0.880694 | 0.112802 | 5 | PASS |
| BUS_03 | C02 | 0.853416 | 0.110879 | 4 | PASS |
| BUS_03 | C03 | 0.843049 | 0.109038 | 4 | PASS |
| BUS_05 | C01 | 0.839156 | 0.074509 | 4 | PASS |
| BUS_05 | C02 | 0.800374 | 0.066262 | 4 | PASS |
| BUS_05 | C03 | 0.797974 | 0.061275 | 3 | REPAIR |
| BUS_09 | C01 | 0.760114 | 0.010887 | 4 | PASS |
| BUS_10 | C01 | 0.502434 | 0.050161 | 2 | REGENERATE |
| BUS_10 | C02 | 0.515471 | 0.040115 | 2 | REGENERATE |
| BUS_10 | C03 | 0.542918 | 0.035256 | 2 | REGENERATE |

## Human delivery outcome

`PASS`: 9/13 (69.23%); `REPAIR`: 1/13 (7.69%); `REGENERATE`: 3/13 (23.08%); `REJECT`: 0/13. Usable after repair (`PASS + REPAIR`) is 10/13 (76.92%). This is an exploratory count, not an established GPT delivery-yield rate: there is one synthetic identity, non-strict provenance and incomplete BUS_09.

## Score and human-label observations

Human identity 5 examples span `0.867965–0.885309` (n=4). Human identity 4 examples span `0.760114–0.853416` (n=5). The single identity-3 case is `0.797974` and was marked `REPAIR`. The three identity-2 failures span `0.502434–0.542918` and were all marked `REGENERATE`.

Current PASS examples span `0.760114–0.885309` (n=9); the REPAIR example is `0.797974`; REGENERATE examples span `0.502434–0.542918` (n=3). This shows separation in this sample, but does not establish a universal threshold.

## BUS_09 scale exception and BUS_10 drift case

BUS_09/C01 is a PASS with human identity 4 at machine score `0.760114`, but its face occupies only `0.010887` of image area. BUS_10 candidates have materially larger detected faces (`0.035256–0.050161`) yet machine scores `0.502434–0.542918` and human identity 2. The series therefore suggests machine similarity is affected by more than one factor; face scale may confound comparisons, but does not by itself explain BUS_09.

The descriptive Pearson correlation between face-area ratio and machine score is `0.668888` across 13 heterogeneous candidates. It is tiny-sample, non-causal and does not control scene, pose, light or interactive generation variation.

## Why no official threshold is set

The calibration confirms the metric is useful evidence for this P01 sample, but does not justify an official production threshold. The sample has one synthetic identity, 13 candidates, non-strict GPT provenance and one incomplete scene. Identity remains a human hard-gate dimension.

## Data needed next

Collect strict-provenance runs across multiple identities, repeated seeds and controlled face-scale/scene conditions; complete independent human reviews; then measure false-accept and false-reject behavior before proposing any production threshold.
