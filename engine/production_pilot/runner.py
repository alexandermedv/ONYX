"""Sequential ONYX Production Pilot v0.1 runner.

This is deliberately a small compatibility runner, not a new orchestration
architecture.  It patches the existing FLUX LoRA API workflow in memory and
records provenance for a human-reviewed business-portrait pilot.
"""
from __future__ import annotations

import argparse
import copy
import csv
import ctypes
import hashlib
import json
import shutil
import subprocess
import time
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from engine.runtime.comfyui_client import ComfyUIClient

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
# Node IDs of ONYX_Flux_Scene_Generator_0.3_fixed_lora_api.json.
MODEL_NODE = "56:48"
LORA_NODE = "56:59"
PROMPT_NODE = "56:51"
SAMPLER_NODE = "56:58"
LATENT_NODE = "56:50"
SAVE_NODE = "9"


def read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8-sig") as stream:
        return json.load(stream)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def windows_memory_status() -> dict[str, int]:
    """Read physical and commit headroom without adding a runtime dependency."""
    class MEMORYSTATUSEX(ctypes.Structure):
        _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
    status = MEMORYSTATUSEX()
    status.dwLength = ctypes.sizeof(status)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
        raise OSError("GlobalMemoryStatusEx failed")
    return {"ram_free_mib": int(status.ullAvailPhys // (1024 * 1024)),
            "commit_free_mib": int(status.ullAvailPageFile // (1024 * 1024))}


def gpu_snapshot() -> dict[str, int]:
    completed = subprocess.run(
        ["nvidia-smi", "--query-gpu=memory.total,memory.used,memory.free", "--format=csv,noheader,nounits"],
        check=True, capture_output=True, text=True,
    )
    total, used, free = (int(value.strip()) for value in completed.stdout.splitlines()[0].split(","))
    return {"total_mib": total, "used_mib": used, "free_mib": free}


def memory_snapshot() -> dict[str, Any]:
    return {"timestamp": datetime.now(timezone.utc).isoformat(), **windows_memory_status(), "gpu": gpu_snapshot()}


def validate_spec(spec: dict[str, Any], root: Path) -> None:
    if spec.get("schema") != "onyx.production_pilot":
        raise ValueError("invalid pilot schema")
    if spec.get("schema_version") != "0.1":
        raise ValueError("unsupported pilot schema version")
    scenes = spec.get("scenes", [])
    if not 10 <= len(scenes) <= 12:
        raise ValueError("pilot must contain 10–12 scenes")
    ids = [scene.get("scene_id") for scene in scenes]
    if len(set(ids)) != len(ids) or not all(isinstance(value, str) and value for value in ids):
        raise ValueError("scene_id values must be unique non-empty strings")
    required = ("workflow", "workflow_sha256", "lora_name", "generation", "memory_guard")
    if any(key not in spec for key in required):
        raise ValueError("pilot spec misses required configuration")
    workflow_path = root / spec["workflow"]
    if not workflow_path.is_file():
        raise FileNotFoundError(workflow_path)
    if sha256_file(workflow_path).lower() != str(spec["workflow_sha256"]).lower():
        raise ValueError("workflow SHA-256 differs from the approved manual-comparison template")
    generation = spec["generation"]
    if generation.get("trigger") != "photo of alexonyx man" or generation.get("lora_weight") != 1.0:
        raise ValueError("pilot identity contract requires photo of alexonyx man at weight 1.0")
    if generation.get("width") != 896 or generation.get("height") != 1152:
        raise ValueError("pilot dimensions must match the canonical API defaults")
    if (generation.get("steps"), generation.get("cfg"), generation.get("sampler_name"),
            generation.get("scheduler"), generation.get("denoise")) != (20, 1.0, "euler", "simple", 1.0):
        raise ValueError("pilot sampler settings must match the canonical API defaults")


def render_workflow(template: dict[str, Any], spec: dict[str, Any], scene: dict[str, Any], run_id: str) -> tuple[dict[str, Any], str]:
    workflow = copy.deepcopy(template)
    generation = spec["generation"]
    # Scene-pack prompts already contain the immutable identity block exactly once.
    prompt = scene["prompt"]
    workflow[LORA_NODE]["inputs"].update({"lora_name": spec["lora_name"], "strength_model": generation["lora_weight"]})
    workflow[PROMPT_NODE]["inputs"]["text"] = prompt
    workflow[SAMPLER_NODE]["inputs"].update({"seed": scene["seed"], "steps": generation["steps"], "cfg": generation["cfg"], "sampler_name": generation["sampler_name"], "scheduler": generation["scheduler"], "denoise": generation["denoise"]})
    workflow[LATENT_NODE]["inputs"].update({"width": generation["width"], "height": generation["height"], "batch_size": 1})
    workflow[SAVE_NODE]["inputs"]["filename_prefix"] = f"ONYX_ProductionPilot/{run_id}/raw/{scene['scene_id']}__seed_{scene['seed']}"
    return workflow, prompt


def resolve_scene_variants(spec: dict[str, Any], scene_indexes: str | None, seeds_per_scene: int) -> list[dict[str, Any]]:
    """Return deterministic scene/seed variants without changing sampler settings."""
    if seeds_per_scene < 1:
        raise ValueError("--seeds-per-scene must be positive")
    scenes = spec["scenes"]
    indexes = list(range(1, len(scenes) + 1)) if scene_indexes is None else [int(value.strip()) for value in scene_indexes.split(",") if value.strip()]
    if not indexes or len(indexes) != len(set(indexes)) or any(not 1 <= index <= len(scenes) for index in indexes):
        raise ValueError(f"--scenes must be unique indexes between 1 and {len(scenes)}")
    variants = []
    for index in indexes:
        scene = dict(scenes[index - 1])
        for offset in range(seeds_per_scene):
            variant = dict(scene)
            variant["seed"] = int(scene["seed"]) + offset
            variant["seed_variant"] = offset + 1
            variants.append(variant)
    return variants


def render_canonical_smoke_workflow(template: dict[str, Any], spec: dict[str, Any], run_id: str) -> dict[str, Any]:
    """Keep canonical prompt and seed byte-for-byte; replace only LoRA and output prefix."""
    workflow = copy.deepcopy(template)
    workflow[LORA_NODE]["inputs"].update({"lora_name": spec["lora_name"], "strength_model": spec["generation"]["lora_weight"]})
    workflow[SAVE_NODE]["inputs"]["filename_prefix"] = f"ONYX_ProductionPilot/{run_id}/raw/00_canonical_smoke"
    return workflow


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".writing")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def prepare_run(spec: dict[str, Any], root: Path, run_id: str) -> dict[str, Any]:
    run_root = root / "09 Experiments" / "production_pilot_v0_1" / "runs" / run_id
    if run_root.exists():
        raise FileExistsError(f"run directory already exists: {run_root}")
    for name in ("raw", "qa", "selected", "repaired", "upscaled", "delivery", "manifests"):
        (run_root / name).mkdir(parents=True)
    template_path = root / spec["workflow"]
    manifest = {"schema": "onyx.production_pilot.run", "schema_version": "0.1", "run_id": run_id,
                "status": "prepared", "created_at": datetime.now(timezone.utc).isoformat(),
                "spec_path": str((root / "09 Experiments/production_pilot_v0_1/pilot_spec.json").resolve()),
                "workflow_path": str(template_path.resolve()), "workflow_sha256": sha256_file(template_path),
                "lora_name": spec["lora_name"], "generation": spec["generation"], "runtime_runbook": "04 Engineering/ComfyUI FLUX Windows Runbook.md", "scenes": []}
    _write_json(run_root / "manifests" / "run_manifest.json", manifest)
    return manifest


def should_free(snapshot: dict[str, Any], guard: dict[str, int]) -> bool:
    """Optional recovery only for system-memory pressure, never loaded-FLUX VRAM."""
    return (snapshot["ram_free_mib"] < guard["soft_ram_free_mib"]
            or snapshot["commit_free_mib"] < guard["soft_commit_free_mib"])


def critically_low(snapshot: dict[str, Any], guard: dict[str, int]) -> bool:
    """Only system RAM/commit headroom stops a run before prompt submission.

    FLUX retains roughly 22 GiB after a successful sample.  Low *free* VRAM is
    therefore telemetry, not a capacity verdict.  Real CUDA allocation/OOM is
    surfaced by ComfyUI as an execution error and recorded without retry.
    """
    return (snapshot["ram_free_mib"] < guard["critical_ram_free_mib"]
            or snapshot["commit_free_mib"] < guard["critical_commit_free_mib"])


def free_models(endpoint: str) -> None:
    data = json.dumps({"unload_models": True, "free_memory": True}).encode()
    request = urllib.request.Request(endpoint.rstrip("/") + "/free", data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=30) as response:
        response.read()


def execute_raw(spec: dict[str, Any], root: Path, run_id: str, *, allow_free: bool, scene_indexes: str | None = None, seeds_per_scene: int = 1) -> Path:
    run_root = root / "09 Experiments" / "production_pilot_v0_1" / "runs" / run_id
    manifest_path = run_root / "manifests" / "run_manifest.json"
    manifest = read_json(manifest_path)
    template = read_json(root / spec["workflow"])
    client = ComfyUIClient(spec.get("endpoint", "http://127.0.0.1:8188"))
    guard = spec["memory_guard"]
    for scene in resolve_scene_variants(spec, scene_indexes, seeds_per_scene):
        before = memory_snapshot()
        if critically_low(before, guard):
            manifest["status"] = "stopped_low_memory"; manifest["stop_snapshot"] = before; _write_json(manifest_path, manifest); break
        freed = False
        if allow_free and should_free(before, guard):
            free_models(client.endpoint); freed = True; before = memory_snapshot()
            if critically_low(before, guard):
                manifest["status"] = "stopped_low_memory"; manifest["stop_snapshot"] = before; _write_json(manifest_path, manifest); break
        workflow, prompt = render_workflow(template, spec, scene, run_id)
        started = time.monotonic(); prompt_id = client.submit(workflow, uuid.uuid4().hex)
        history = client.wait_for_history(prompt_id, spec.get("timeout_seconds", 1800)); image = client.one_image(history); payload = client.download(image)
        suffix = "" if seeds_per_scene == 1 else f"__seed_{scene['seed']}"
        destination = run_root / "raw" / f"{scene['scene_id']}{suffix}.png"; destination.write_bytes(payload)
        record = {"scene_id": scene["scene_id"], "prompt": prompt, "seed": scene["seed"], "prompt_id": prompt_id,
                  "seed_variant": scene["seed_variant"], "status": "completed", "output": str(destination.resolve()), "sha256": sha256_file(destination),
                  "duration_seconds": time.monotonic() - started, "memory_before": before, "memory_after": memory_snapshot(), "free_invoked": freed}
        manifest["scenes"].append(record); _write_json(run_root / "manifests" / f"{scene['scene_id']}.json", record); _write_json(manifest_path, manifest)
    else:
        manifest["status"] = "raw_completed"; _write_json(manifest_path, manifest)
    return manifest_path


def dry_run(spec: dict[str, Any], root: Path, run_id: str, scene_indexes: str | None = None, seeds_per_scene: int = 1) -> dict[str, Any]:
    template = read_json(root / spec["workflow"])
    rendered = []
    for scene in resolve_scene_variants(spec, scene_indexes, seeds_per_scene):
        workflow, prompt = render_workflow(template, spec, scene, run_id)
        rendered.append({"scene_id": scene["scene_id"], "seed": scene["seed"], "prompt": prompt,
                         "lora_name": workflow[LORA_NODE]["inputs"]["lora_name"], "output_prefix": workflow[SAVE_NODE]["inputs"]["filename_prefix"]})
    return {"run_id": run_id, "scene_count": len(rendered), "workflow_path": spec["workflow"], "workflow_sha256": sha256_file(root / spec["workflow"]), "generation": spec["generation"], "scenes": rendered}


def smoke_payload(spec: dict[str, Any], root: Path, run_id: str) -> dict[str, Any]:
    workflow = render_canonical_smoke_workflow(read_json(root / spec["workflow"]), spec, run_id)
    sampler = workflow[SAMPLER_NODE]["inputs"]
    return {"mode": "canonical_smoke_payload_only", "workflow_path": spec["workflow"],
            "workflow_sha256": sha256_file(root / spec["workflow"]), "model": workflow[MODEL_NODE]["inputs"]["unet_name"],
            "lora": {"node": LORA_NODE, "name": workflow[LORA_NODE]["inputs"]["lora_name"], "weight": workflow[LORA_NODE]["inputs"]["strength_model"]},
            "prompt": workflow[PROMPT_NODE]["inputs"]["text"], "seed": sampler["seed"],
            "sampler": {key: sampler[key] for key in ("steps", "cfg", "sampler_name", "scheduler", "denoise")},
            "latent": workflow[LATENT_NODE]["inputs"], "output_prefix": workflow[SAVE_NODE]["inputs"]["filename_prefix"]}


def execute_canonical_smoke(spec: dict[str, Any], root: Path, run_id: str, *, allow_free: bool) -> Path:
    """Submit exactly one canonical-prompt smoke only when explicitly requested."""
    run_root = root / "09 Experiments" / "production_pilot_v0_1" / "runs" / run_id
    manifest = prepare_run(spec, root, run_id)
    manifest_path = run_root / "manifests" / "run_manifest.json"; guard = spec["memory_guard"]
    before = memory_snapshot()
    if critically_low(before, guard):
        manifest.update({"status": "stopped_low_memory", "stop_snapshot": before}); _write_json(manifest_path, manifest); return manifest_path
    freed = False
    client = ComfyUIClient(spec.get("endpoint", "http://127.0.0.1:8188"))
    if allow_free and should_free(before, guard):
        free_models(client.endpoint); freed = True; before = memory_snapshot()
        if critically_low(before, guard):
            manifest.update({"status": "stopped_low_memory", "stop_snapshot": before}); _write_json(manifest_path, manifest); return manifest_path
    workflow = render_canonical_smoke_workflow(read_json(root / spec["workflow"]), spec, run_id)
    started = time.monotonic(); prompt_id = client.submit(workflow, uuid.uuid4().hex)
    history = client.wait_for_history(prompt_id, spec.get("timeout_seconds", 1800)); image = client.one_image(history); payload = client.download(image)
    destination = run_root / "raw" / "00_canonical_smoke.png"; destination.write_bytes(payload)
    record = {"scene_id": "00_canonical_smoke", "prompt": workflow[PROMPT_NODE]["inputs"]["text"],
              "seed": workflow[SAMPLER_NODE]["inputs"]["seed"], "prompt_id": prompt_id, "status": "completed",
              "output": str(destination.resolve()), "sha256": sha256_file(destination), "duration_seconds": time.monotonic() - started,
              "memory_before": before, "memory_after": memory_snapshot(), "free_invoked": freed}
    manifest["scenes"].append(record); manifest["status"] = "smoke_completed"
    _write_json(run_root / "manifests" / "00_canonical_smoke.json", record); _write_json(manifest_path, manifest)
    return manifest_path


def quality_gate_manifest(run_root: Path, run_manifest: dict[str, Any]) -> Path:
    """Create the read-only legacy shape consumed by the existing QG CLI."""
    rows = [{"scene_id": item["scene_id"], "method": "lora_mini_5__1250",
             "source": item["output"], "status": "completed"}
            for item in run_manifest.get("scenes", []) if item.get("status") == "completed"]
    if not rows:
        raise RuntimeError("raw run contains no completed images")
    path = run_root / "qa" / "quality_gate_input_manifest.json"
    _write_json(path, {"job_id": run_manifest["run_id"], "postprocess": {"runs": rows}})
    return path


def annotate_technical_flags(report_path: Path, ranking_path: Path) -> None:
    """Add deterministic OpenCV technical evidence without altering Quality Gate scores."""
    import cv2
    import numpy as np
    with report_path.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    for row in rows:
        image = cv2.imdecode(np.fromfile(row["source"], dtype=np.uint8), cv2.IMREAD_COLOR)
        if image is None:
            row.update({"sharpness": "", "exposure_mean": "", "technical_flags": "cannot_read"})
            continue
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sharpness = float(cv2.Laplacian(gray, cv2.CV_64F).var()); exposure = float(gray.mean())
        low = float(np.mean(gray <= 20)); high = float(np.mean(gray >= 235))
        flags = (["low_sharpness"] if sharpness < 45 else []) + (["underexposed"] if low > .35 else []) + (["overexposed"] if high > .20 else [])
        row.update({"sharpness": f"{sharpness:.6f}", "exposure_mean": f"{exposure:.6f}", "technical_flags": "|".join(flags)})
    rows.sort(key=lambda row: (str(row.get("face_detected", "")).lower() != "true", -float(row.get("sim_mean") or -1), len([x for x in row.get("technical_flags", "").split("|") if x]), row["scene_id"]))
    for rank, row in enumerate(rows, start=1):
        row["rank"] = str(rank); row["recommendation"] = "review"  # never a final automatic selection
    fields = list(rows[0]) if rows else []
    with report_path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields); writer.writeheader(); writer.writerows(rows)
    _write_json(ranking_path, {"schema": "onyx.production_pilot.qa_ranking", "status": "review_required", "rows": rows})


def run_qa(run_root: Path, reference_folder: Path) -> Path:
    if not reference_folder.is_dir():
        raise FileNotFoundError(reference_folder)
    run_manifest = read_json(run_root / "manifests" / "run_manifest.json")
    input_manifest = quality_gate_manifest(run_root, run_manifest)
    report = run_root / "qa" / "quality_report.csv"; summary = run_root / "qa" / "identity_summary.csv"
    subprocess.run(["python", "-m", "engine.quality_gate.identity", "analyze-job", str(reference_folder), str(input_manifest), "--output", str(report), "--summary", str(summary)], check=True)
    ranking = run_root / "qa" / "ranking.json"; annotate_technical_flags(report, ranking)
    return ranking


def main() -> int:
    parser = argparse.ArgumentParser(description="ONYX Production Pilot v0.1")
    parser.add_argument("--spec", type=Path, default=Path("09 Experiments/production_pilot_v0_1/pilot_spec.json"))
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--run-id", default=datetime.now().strftime("production_pilot_%Y%m%d_%H%M%S"))
    sub = parser.add_subparsers(dest="command", required=True)
    dry = sub.add_parser("dry-run")
    dry.add_argument("--scenes", help="comma-separated one-based scene indexes")
    dry.add_argument("--seeds-per-scene", type=int, default=1)
    smoke = sub.add_parser("smoke", help="canonical one-scene smoke; payload only unless --execute is explicit")
    smoke.add_argument("--execute", action="store_true")
    smoke.add_argument("--allow-free-on-pressure", action="store_true")
    raw = sub.add_parser("raw"); raw.add_argument("--allow-free-on-pressure", action="store_true")
    raw.add_argument("--scenes", help="comma-separated one-based scene indexes")
    raw.add_argument("--seeds-per-scene", type=int, default=1)
    qa = sub.add_parser("qa"); qa.add_argument("--reference-folder", type=Path, required=True)
    args = parser.parse_args(); root = args.root.resolve(); spec = read_json(args.spec); validate_spec(spec, root)
    if args.command == "dry-run": print(json.dumps(dry_run(spec, root, args.run_id, args.scenes, args.seeds_per_scene), ensure_ascii=False, indent=2)); return 0
    if args.command == "smoke":
        if args.execute: print(execute_canonical_smoke(spec, root, args.run_id, allow_free=args.allow_free_on_pressure)); return 0
        print(json.dumps(smoke_payload(spec, root, args.run_id), ensure_ascii=False, indent=2)); return 0
    if args.command == "qa": print(run_qa(root / "09 Experiments" / "production_pilot_v0_1" / "runs" / args.run_id, args.reference_folder)); return 0
    prepare_run(spec, root, args.run_id); print(execute_raw(spec, root, args.run_id, allow_free=args.allow_free_on_pressure, scene_indexes=args.scenes, seeds_per_scene=args.seeds_per_scene)); return 0


if __name__ == "__main__":
    raise SystemExit(main())
