# ONYX Client Delivery SOP v1

## Source

Use only an approved production package. Never modify files under `09 Experiments`. The package must contain ten approved master PNGs after upscale and a completed visual QA record.

## Build

Run `engine/production/onyx_delivery.py` with the package directory and the approved Cormorant font. The process creates three derived folders:

- `client_jpeg_2048`: paid client delivery, high-quality JPEG;
- `web_jpeg_1600`: paid lightweight delivery;
- `prepayment_preview`: reduced preview with `ONYX / PRIVATE PREVIEW / ORDER <ID>`.

The script writes `CLIENT_DELIVERY_MANIFEST_V1.json` with master paths and SHA-256 values.

## Sending policy

Before payment, send only `prepayment_preview` and replace `<ID>` with the order number. After payment, send both `client_jpeg_2048` and `web_jpeg_1600`; provide the full-resolution PNG masters when the client requests maximum quality or an archive package. Paid files contain no watermark.

## QA gate

Check that the package contains ten images, filenames and roles match the portfolio manifest, previews carry the correct order ID, paid JPEGs have no watermark, and the manifest is present. Do not publish or deliver while owner final approval is pending.
