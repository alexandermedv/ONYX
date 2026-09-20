# ONYX Client Delivery SOP v1

## Commercial scope — 2026-09-20

[Product System](../Product_Standards/ONYX_PRODUCT_SYSTEM.md) governs 1/10/20 accepted finals plus purchased extras; Portrait has no Book, Signature Standard PDF, Premium Extended PDF. The existing builder described below is the legacy ten-image Signature path. Portrait/Premium require manually verified packaging until a compatible builder is confirmed; do not claim universal automation.

## Source

Use only an approved production package. Never modify files under `09 Experiments`. The package must contain ten approved master PNGs after upscale and a completed visual QA record.

## Build

For a new package, run `engine/production/onyx_production_pipeline.py`. It first stages the approved source-resolution JPEGs, runs the configured ComfyUI postprocessor to create the full-resolution PNG masters, and then runs `onyx_delivery.py` to create the client package. Re-running the delivery script alone is appropriate when the masters already exist.

Run `engine/production/onyx_delivery.py` with the package directory and the approved Cormorant font. The process creates four delivery folders:

- `00_PREPAYMENT_PREVIEW`: reduced proofs used only before payment;
- `01_LIGHT_JPEG`: paid lightweight delivery;
- `02_HIGH_QUALITY_JPEG`: paid high-quality JPEG delivery;
- `03_FULL_RESOLUTION_PNG`: paid delivery containing the ten original upscale PNG masters at maximum resolution.

Client-facing files are named `ONYX_01` through `ONYX_10`; internal character identifiers are not exposed in filenames. The script also creates `README.txt`, `ONYX_<ORDER>_LIGHT.zip`, `ONYX_<ORDER>_FULL.zip`, and `CLIENT_DELIVERY_MANIFEST_V1.json` with source master paths, copied full-resolution paths and SHA-256 values.

The prepayment footer uses `BUSINESS COLLECTION / CLIENT PREVIEW`. `PORTFOLIO PREVIEW` is reserved for public portfolio assets and must never appear in client proof files.

## Sending policy

New frozen orders require Reference QA and 100% prepayment before production. Legacy `00_PREPAYMENT_PREVIEW` proofs are not a free included prepayment generation step. After payment and final acceptance, send either the compact LIGHT archive or the complete FULL archive. Paid files contain no watermark. The client may use the lightweight set for messaging and social media, the high-quality JPEG set for everyday use, and the full-resolution PNG set for print, retouching and archive storage.

## QA gate

Check that every delivery folder contains ten images, filenames and roles match the portfolio manifest, full-resolution checksums match their source masters, previews carry the correct order ID, paid files have no watermark, and the manifest is present. Do not publish or deliver while owner final approval is pending.
