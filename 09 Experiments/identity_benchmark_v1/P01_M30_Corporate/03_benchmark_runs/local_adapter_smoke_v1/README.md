# P01 local PuLID/FLUX adapter smoke v1

This directory records the single permitted minimal local PuLID/FLUX smoke for `P01 v1.0`, scene `BUS_01`. It did not produce an image.

The request used the dedicated adapter workflow and all three canonical references through the workflow's native `BatchImagesNode`. The identity master was not used. ComfyUI loaded the FLUX/PuLID components but remained at `Model Initializing`; after `569.91` seconds the job was interrupted at `SamplerCustomAdvanced` before its first sampler step.

No parameter tuning, retry, benchmark-series generation, or production-pipeline change was performed. Consequently there are no image QA or identity metrics, and this run is not local benchmark evidence.

See `run_manifest.yaml` for hashes, model identifiers, exact parameters, runtime argv and the server prompt ID.
