# Future candidate QA plan

Run this plan only after production candidates exist. It does not authorize generation.

Assess every candidate for:

- likeness and identity consistency;
- anatomy, eyes, hands and proportions;
- realism and visible artifacts;
- clean-shaven requirement and clothing quality;
- scene intent and background quality;
- collection consistency and diversity across selected scenes.

Use exactly one disposition: `PASS`, `REPAIR`, `REGENERATE`, `REJECT`.

- `PASS`: candidate is suitable for selection.
- `REPAIR`: a promising image has a bounded fix.
- `REGENERATE`: scene objective is valid but the candidate misses a quality gate.
- `REJECT`: do not continue work on the candidate.
