# Ideogram qualifier v1 — P01_M30_Corporate

## Purpose

Qualifier run for ONYX Model Arena using Ideogram with a single identity reference.

Test scenes:
- BUS_01
- BUS_06 / DESK
- BUS_09 / FULL

## Method

Model/service:
- Ideogram web app
- Character / identity-reference workflow
- 1 reference image used

Identity input:
- P01 canonical frontal reference
- single-reference mode
- no multi-reference input available in this workflow

Generation policy:
- one qualifier result per scene
- no manual retouching
- no post-processing
- no upscale
- no repair pass
- no selection based on visual quality

The Ideogram web UI generated multiple variants per prompt.
For Arena fairness, the first output from each scene batch was selected as the official qualifier result.
All raw variants are preserved under `outputs_raw/`.

## Scenes

### BUS_01
Professional chest-up business portrait.

Official output:
`P01_BUS_01_IDEOGRAM.jpg`

### BUS_06
Professional seated-at-desk business portrait.

Official output:
`P01_BUS_06_IDEOGRAM.jpg`

### BUS_09
Professional full-body executive portrait.

Official output:
`P01_BUS_09_IDEOGRAM.jpg`

## Output format

Original downloaded format:
- JPEG

No format conversion was performed.

## Known limitations

- Ideogram workflow used only one identity reference.
- The free web UI generated multiple outputs per request.
- Output count could not be reduced without upgrading the account.
- Qualifier uses the first output from each batch to avoid cherry-picking.
- No seed control was available in the web interface.
- Exact internal sampler / CFG / guidance values are not exposed.

## Arena status

Qualifier status: COMPLETE

Scenes completed:
- BUS_01
- BUS_06
- BUS_09

Ready for blind review.