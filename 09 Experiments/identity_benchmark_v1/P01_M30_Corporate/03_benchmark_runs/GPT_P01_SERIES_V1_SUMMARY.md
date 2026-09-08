# GPT P01 Series v1 — exploratory summary

This is the first GPT/P01 exploratory series: BUS_01, BUS_03, BUS_05, BUS_09 and BUS_10. Every run lacks strict generation provenance, so it is not final cross-model benchmark evidence. Human review is pending and no calibrated P01 identity threshold exists.

The machine series is complete for its currently saved artifacts; human identity calibration is now pending. Among completed scenes, BUS_10 has the lowest machine identity similarity. No delivery-yield conclusion may be made until the human review is complete.

| Scene | Run status | Saved / target | Identity mean | Candidate min–max |
|---|---|---:|---:|---:|
| BUS_01 | provisional | 3 / 3 | 0.875246 | 0.867965–0.885309 |
| BUS_03 | provisional | 3 / 3 | 0.859053 | 0.843049–0.880694 |
| BUS_05 | provisional | 3 / 3 | 0.812501 | 0.797974–0.839156 |
| BUS_09 | **incomplete** | 1 / 3 | 0.760114 | n=1; non-equivalent |
| BUS_10 | provisional | 3 / 3 | 0.520274 | 0.502434–0.542918 |

There were 15 planned candidates and 13 actually saved: 12 from completed scenes and one from incomplete BUS_09. The two absent BUS_09 candidates are not asserted to be verified backend failures; no reliability rate or delivery-yield estimate is calculated.

Across all 13 saved candidates, the descriptive mean identity similarity is `0.766257`. The observed minimum is BUS_10/C01 (`0.502434`); the maximum is BUS_01/C01 (`0.885309`). These figures do not establish that GPT is better or worse than any other backend, nor that identity decline proves model degradation. Scene complexity, face scale, pose, lighting and interactive generation variability differ.

Face-area ratios are recorded in the companion YAML. Their exploratory Pearson correlation with identity similarity is `0.668888` across heterogeneous samples; this is not a causal or controlled result. BUS_09 has a particularly small detected face and only one candidate, so it is non-equivalent to the completed scenes.
