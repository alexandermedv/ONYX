# P01 GPT BUS_01 v1 — provisional run

This is the first GPT exploratory run for P01 v1.0 and `BUS_01 — Classic Business Headshot`. It contains three candidates, C01–C03.

The run is **provisional**. It was generated interactively in ChatGPT; canonical P01 references were present in the working conversation context, but strict proof that only REF01–REF03 were used as generation inputs is unavailable. It is retained for exploratory analysis and must not be used as final evidence that GPT is superior to another backend.

Machine QA uses the existing ONYX InsightFace `buffalo_l` evaluation logic against REF01–REF03. C01 has mean similarity `0.885309`; C02 `0.867965`; C03 `0.872464`. All three images are readable and have one detected face. No P01-calibrated threshold exists, so all machine decisions remain `REVIEW`; human review is pending in `human_review.csv`.

The Identity Master was not used as a generation input or QA reference. Candidate PNG are local generated artifacts; manifests, evaluation and review template provide their Git-tracked provenance.
