from __future__ import annotations

import json
from pathlib import Path


def create_job(client: str, job_name: str) -> Path:
    root = Path(r"D:\AI\Clients")

    job_dir = root / client / "jobs" / job_name

    for folder in (
        # "01_source",
        "02_scenes",
        "03_face_swapped",
        "04_final",
        "logs",
    ):
        (job_dir / folder).mkdir(parents=True, exist_ok=True)

    job = {
        "schema_version": "1.0",
        "job_id": job_name,
        "client_id": client,
        "paths": {
            "client_profile": str(root / client / "profile" / "client_profile.json")
        },
        "pipeline": {
            "scene_generator": {
                "enabled": True,
                "command": [
                    "{python}",
                    r"D:\AI\ONYX\engine\scene_generator\generator.py",
                    "--server", "http://127.0.0.1:8188",
                    "--comfy-output", r"D:\AI\ComfyUI\ComfyUI_windows_portable\ComfyUI\output",
                    "scenes",
                    "--workflow", r"D:\AI\ONYX\comfyui-workflows\Scene_Generator_Random_API.json",
                    "--profile", "{client_profile}",
                    "--output-dir", "{output_dir}",
                    "--count", "8"
                ],
                "minimum_output_images": 8
            },
            "facefusion": {
                "enabled": True,
                "command": [
                    "{python}",
                    r"D:\AI\ONYX\engine\facefusion\runner.py",
                    "--facefusion-folder", r"D:\AI\facefusion",
                    "--python", r"C:\Users\ME\miniconda3\envs\facefusion\python.exe",
                    "--source-dir", "{source_dir}",
                    "--target-dir", "{input_dir}",
                    "--output-dir", "{output_dir}"
                ],
                "minimum_output_images": 1
            },
            "postprocessor": {
                "enabled": True,
                "command": [
                    "{python}",
                    r"D:\AI\ONYX\engine\scene_generator\generator.py",
                    "--server", "http://127.0.0.1:8188",
                    "--comfy-output", r"D:\AI\ComfyUI\ComfyUI_windows_portable\ComfyUI\output",
                    "postprocess",
                    "--workflow", r"D:\AI\ONYX\comfyui-workflows\Portrait_PostProcessor_1.0_API.json",
                    "--profile", "{client_profile}",
                    "--input-dir", "{input_dir}",
                    "--output-dir", "{output_dir}",
                    "--comfy-input", r"D:\AI\ComfyUI\ComfyUI_windows_portable\ComfyUI\input"
                ],
                "minimum_output_images": 1
            }
        }
    }

    with (job_dir / "job.json").open("w", encoding="utf-8") as f:
        json.dump(job, f, indent=2, ensure_ascii=False)

    return job_dir