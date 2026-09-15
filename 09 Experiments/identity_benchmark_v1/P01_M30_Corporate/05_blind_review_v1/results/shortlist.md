# P01 final 10-scene round shortlist

## Core finalists

1. **GPT Images 2.5** — best overall score and the only finalist with PASS on all three scenes.
2. **mini-3 @ 1250** — best local LoRA, strongest local full-body result, and the narrowest three-scene score range.
3. **mini-5 @ 1000** — the most stable mini-5 checkpoint; its full-body result is REPAIR rather than a reject.

## Diagnostic finalists

4. **FLUX Kontext** — top identity score across all three scenes, but its BUS_09 realism and commercial result require a robustness check.
5. **Ideogram** — excellent BUS_01 and BUS_06 commercial quality, but BUS_09 identity failed; retain only to test whether this failure persists over a larger scene set.

The shortlist intentionally excludes higher-average variants with a rejected full-body frame when a more stable alternative is available. No final-round generation is started by this analysis.

## Ranked evidence

| Overall rank | Model | Identity | Overall | PASS+REPAIR |
| --- | --- | --- | --- | --- |
| 1 | GPT Images 2.5 | 5.0 | 4.5667 | 1.0 |
| 3 | mini-3 @ 1250 | 3.3333 | 3.6667 | 1.0 |
| 6 | mini-5 @ 1000 | 2.6667 | 3.4 | 1.0 |
| 4 | FLUX Kontext | 5.0 | 3.6 | 0.6667 |
| 2 | Ideogram | 3.6667 | 4.0167 | 0.6667 |
