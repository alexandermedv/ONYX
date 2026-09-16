# Upscale readiness and P03 qualification — 2026-09-16

The active ComfyUI installation is `D:\AI\ComfyUI_Flux\ComfyUI`, served locally at `http://127.0.0.1:8188` (ComfyUI 0.30.0). The prior validation failure came from staging an image into an obsolete ComfyUI input folder. The postprocessor now normalizes staged inputs to valid RGB PNG files in the active input root and preserves ComfyUI's HTTP validation response.

P03 Business was qualified with `comfyui-workflows/Portrait_PostProcessor_1.0_API.json` (SHA-256 `FD8D686120908FF3B2BE60F0F4CDC73F9A9440118227F4911172A083AD4C842E`): 4x `4x_NMKD-Siax_200k.pth`, followed by FaceDetailer using `Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors` at denoise 0.15. The HERO smoke test and all ten P03 frames passed visual QA for identity, face, skin, hair, hands, anatomy and visible artefacts. Full lineage is recorded in `P03/P03_UPSCALE_MANIFEST_V1.json`; compact contact and anatomy sheets accompany the local outputs.

P01 Business and P02 Business retain source-resolution exports only. Their full batches have not been submitted, so they remain blocked on the same validated upscale workflow and per-frame QA.

P03 still requires owner final approval before publication or paid delivery. Full-resolution PNG outputs remain local-only; Git contains the manifest and QA evidence rather than the approximately 400 MB render set.
