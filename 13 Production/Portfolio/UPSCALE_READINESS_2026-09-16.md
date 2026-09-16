# Upscale readiness — 2026-09-16

The configured postprocessing workflow is `comfyui-workflows/Portrait_PostProcessor_1.0_API.json`; it specifies the local model `4x_NMKD-Siax_200k.pth`, which is present at the configured ComfyUI installation.

The endpoint `http://127.0.0.1:8188` refused connection during readiness verification. No external ComfyUI process was started, no source was copied into its input directory, and no upscale was attempted.

The 30 final portfolio exports for P01 Business, P02 Business and P03 Business are source-resolution JPEG derivatives. They have passed editorial visual QA and standard 3:4 packaging, but cannot be labelled `UPSCALED` or delivered as paid finals.

When the existing ComfyUI service is available, run a single P03 HERO postprocessing smoke test through the configured workflow. Inspect identity and anatomy against the source before applying it to the three ten-photo packages. Record the workflow hash, model filename, source/output SHA256, dimensions and visual QA decision in each package manifest.
