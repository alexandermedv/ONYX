# Web derivatives

Twenty local candidate exports: ten JPEG and ten WebP, linked in `web_manifest.csv`.
Inputs are byte-identical `03_final` candidates. Publication is pending human review.

- Long edge is capped at 1600 px; smaller inputs are not enlarged.
- Original aspect ratio is preserved, using Lanczos if downsampling is required.
- JPEG quality 95, chroma subsampling disabled; WebP quality 95, method 6.
- Exported as RGB; source metadata is not copied into delivery files.
- No source PNG is overwritten. No retouch, repair or AI upscale was performed.

After a candidate changes or is rejected, regenerate its derivatives through a new
reviewed export step and update manifests. Do not publish stale candidate derivatives.
