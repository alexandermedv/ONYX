# ONYX Client Delivery SOP v1

## Source

Use only an approved production package. Never modify files under `09 Experiments`. The package must contain ten approved master PNGs after upscale and a completed visual QA record.

## Build

For a new package, run `engine/production/onyx_production_pipeline.py`. It first stages the approved source-resolution JPEGs, runs the configured ComfyUI postprocessor to create the full-resolution PNG masters, and then runs `onyx_delivery.py` to create the three client tiers. Re-running the delivery script alone is appropriate when the masters already exist.

Run `engine/production/onyx_delivery.py` with the package directory and the approved Cormorant font. The process creates four delivery folders:

- `full_resolution`: paid delivery containing the ten original upscale PNG masters at maximum resolution;
- `client_jpeg_2048`: paid client delivery, high-quality JPEG;
- `web_jpeg_1600`: paid lightweight delivery;
- `prepayment_preview`: reduced preview with `ONYX / PRIVATE PREVIEW / ORDER <ID>`.

The script writes `CLIENT_DELIVERY_MANIFEST_V1.json` with source master paths, copied full-resolution paths and SHA-256 values.

## Sending policy

Before payment, send only `prepayment_preview` and replace `<ID>` with the order number. After payment, the standard package contains `full_resolution`, `client_jpeg_2048` and `web_jpeg_1600`. Paid files contain no watermark. The client may use the lightweight set for messaging and social media, the 2048 px set for everyday use, and the full-resolution PNG set for print, retouching and archive storage.

## QA gate

Check that every delivery folder contains ten images, filenames and roles match the portfolio manifest, full-resolution checksums match their source masters, previews carry the correct order ID, paid files have no watermark, and the manifest is present. Do not publish or deliver while owner final approval is pending.

