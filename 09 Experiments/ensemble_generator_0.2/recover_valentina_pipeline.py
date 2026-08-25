import json
import time
import uuid
from pathlib import Path

import ensemble_runner as er


JOB_PATH = Path("job.20scenes.valentina.json")
MANIFEST_PATH = Path("job.20scenes.valentina.manifest.json")

WORKFLOWS = Path("workflows")

OUTPUT_ROOT = Path(
    r"D:\AI\ComfyUI_Flux\ComfyUI\output"
)


def save_manifest(manifest):
    MANIFEST_PATH.write_text(
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


job = json.loads(
    JOB_PATH.read_text(encoding="utf-8-sig")
)

manifest = json.loads(
    MANIFEST_PATH.read_text(encoding="utf-8-sig")
)

client_id = str(uuid.uuid4())

print("=" * 78)
print("ONYX RECOVERY — VALENTINA")
print("=" * 78)
print("Job :", job["job_id"])
print("Runs:", len(manifest["runs"]))
print()


# ------------------------------------------------------------------
# 1. Restore source output paths for the already generated 80 images
# ------------------------------------------------------------------

print("=== Restoring generated outputs ===")

restored = 0
missing = []

for run in manifest["runs"]:

    if run.get("status") != "completed":
        continue

    scene_id = run["scene_id"]
    branch = run["branch"]

    scene_dir = (
        OUTPUT_ROOT
        / "ONYX_Ensemble"
        / job["job_id"]
        / scene_id
        / branch
    )

    images = er.image_files(scene_dir)

    # Do not accidentally pick identity derivatives if recovery is re-run.
    originals = [
        p for p in images
        if "facefusion" not in p.parts
        and "dreamo_img2img" not in p.parts
    ]

    if not originals:
        missing.append(
            f"{branch}/{scene_id}"
        )
        continue

    source = max(
        originals,
        key=lambda p: p.stat().st_mtime,
    )

    run["output"] = str(source)

    # Remove stale recovery state if this script is re-run.
    run.pop("facefusion_status", None)
    run.pop("facefusion_error", None)
    run.pop("facefusion_output", None)

    run.pop("dreamo_img2img_status", None)
    run.pop("dreamo_img2img_error", None)
    run.pop("dreamo_img2img_output", None)
    run.pop("dreamo_img2img_prompt_id", None)

    run.pop("postprocess_status", None)
    run.pop("postprocess_method", None)
    run.pop("postprocess_output", None)

    restored += 1


print("Restored:", restored)
print("Missing :", len(missing))

if missing:
    print()
    print("Missing source images:")
    for item in missing:
        print("  ", item)

    raise RuntimeError(
        "Recovery stopped because some generated "
        "source images could not be found."
    )

if restored != 80:
    raise RuntimeError(
        f"Expected 80 completed sources, restored {restored}"
    )

save_manifest(manifest)


# ------------------------------------------------------------------
# 2. FaceFusion
# ------------------------------------------------------------------

for branch in ("flux", "juggernautxl"):

    runs = [
        run
        for run in manifest["runs"]
        if run["branch"] == branch
        and run["status"] == "completed"
    ]

    print()
    print(
        f"=== FaceFusion recovery: {branch} "
        f"({len(runs)} images) ==="
    )

    er.free_memory(
        "http://127.0.0.1:8188",
        10.0,
    )

    er.run_facefusion_batch(
        job,
        branch,
        runs,
        Path(job["work_root"]),
    )

    completed = sum(
        run.get("facefusion_status") == "completed"
        for run in runs
    )

    failed = sum(
        run.get("facefusion_status") == "failed"
        for run in runs
    )

    print(
        f"FaceFusion {branch}: "
        f"{completed} completed / {failed} failed"
    )

    save_manifest(manifest)


# ------------------------------------------------------------------
# 3. DreamO img2img
# ------------------------------------------------------------------

print()
print("=== DreamO img2img identity variants ===")

er.free_memory(
    "http://127.0.0.1:8188",
    10.0,
)

er.run_dreamo_img2img(
    "http://127.0.0.1:8188",
    client_id,
    job,
    manifest,
    WORKFLOWS,
    OUTPUT_ROOT,
    1.0,
)

save_manifest(manifest)


# ------------------------------------------------------------------
# 4. Postprocessor
# ------------------------------------------------------------------

print()
print("=== ONYX Postprocessor ===")

er.free_memory(
    "http://127.0.0.1:8188",
    10.0,
)

er.run_postprocessor(
    "http://127.0.0.1:8188",
    client_id,
    job,
    manifest,
    WORKFLOWS,
    OUTPUT_ROOT,
    1.0,
)

save_manifest(manifest)


# ------------------------------------------------------------------
# 5. Flat customer-facing results
# ------------------------------------------------------------------

print()
print("=== Final results ===")

final_root = er.collect_final_results(
    job,
    manifest,
    JOB_PATH,
)

manifest["finished_at"] = time.time()

save_manifest(manifest)

print()
print("=" * 78)
print("RECOVERY COMPLETED")
print("=" * 78)
print("Final :", final_root)
print(
    "Count :",
    manifest.get("final_results_count"),
)