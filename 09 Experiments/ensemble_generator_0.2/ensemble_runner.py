#!/usr/bin/env python3
"""Sequential ONYX ensemble runner for ComfyUI.

Runs a series branch-by-branch to avoid keeping SDXL, FLUX and DreamO in
memory together. Optional identity post-processors are command/workflow based.
"""

from __future__ import annotations

import argparse
import copy
import json
import shutil
import subprocess
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path


BRANCHES = {
    "flux": {"workflow": "flux_api.json", "prompt": "60:51", "seed": "60:58", "save": "62"},
    "lora": {"workflow": "lora_api.json", "prompt": "76:74", "seed": "76:75", "save": "77"},
    "juggernautxl": {
        "workflow": "ONYX_JuggernautXL_Generator_v0.3_weighted.json",
        "prompt": "13",
        "negative": "14",
        "seed": "12",
        "save": "7",
        "latent": "9",
        "sampler": "12",
    },
    "dreamo": {
        "workflow": "dreamo_api.json",
        "prompt": "66:65",
        "seed": "66:31",
        "save": "67",
        "reference": "66:52",
    },
}


def http_json(url: str, payload: dict | None = None, timeout: int = 60) -> dict:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data)
    if payload is not None:
        request.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read()
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} from {url}: {body}") from exc
    return json.loads(raw) if raw else {}


def wait_for_prompt(server: str, prompt_id: str, poll_seconds: float) -> dict:
    while True:
        history = http_json(f"{server}/history/{prompt_id}")
        if prompt_id in history:
            record = history[prompt_id]
            status = record.get("status", {})
            if status.get("completed") is False or status.get("status_str") == "error":
                raise RuntimeError(f"ComfyUI failed: {json.dumps(status, ensure_ascii=False)}")
            return record
        time.sleep(poll_seconds)


def free_memory(server: str, settle_seconds: float) -> None:
    http_json(server + "/free", {"unload_models": True, "free_memory": True})
    time.sleep(settle_seconds)


def text(scene: dict, key: str, default: str = "") -> str:
    return str(scene.get(key, default)).strip()


def build_prompt(scene: dict, branch: str, job: dict) -> str:
    explicit = scene.get("prompts", {}).get(branch)
    if explicit:
        return explicit.strip()

    subject = text(scene, "subject", "one adult person")
    appearance = str(job.get("identity", {}).get("appearance", "")).strip()
    if appearance:
        subject = f"{subject}, {appearance}"
    clothing = text(scene, "clothing")
    pose = text(scene, "pose")
    hands = text(scene, "hands")
    location = text(scene, "location")
    lighting = text(scene, "lighting")
    composition = text(scene, "composition")
    camera = text(scene, "camera", "professional editorial photography, natural depth of field")
    details = text(scene, "details", "realistic skin texture, natural proportions, restrained retouching")

    if branch == "lora":
        trigger_word = str(job.get("trigger_word", "alexonyx")).strip()
        subject = (
            f"{trigger_word}, {subject}, preserving recognizable identity, "
            "facial proportions and real age"
        )
    elif branch == "dreamo":
        subject = (
            f"the same person from the reference image, {subject}, preserving recognizable "
            "identity, facial proportions and real age"
        )

    if branch == "juggernautxl":
        parts = [
            "professional editorial photograph",
            subject,
            f"({pose}:1.25)" if pose else "",
            f"({composition}:1.2)" if composition else "",
            f"({clothing}:1.3)" if clothing else "",
            f"({hands}:1.2)" if hands else "",
            location,
            lighting,
            camera,
            details,
        ]
    else:
        parts = [
            f"A photorealistic corporate editorial portrait of {subject}.",
            f"Clothing: {clothing}." if clothing else "",
            f"Pose: {pose}." if pose else "",
            f"Hands: {hands}." if hands else "",
            f"Location: {location}." if location else "",
            f"Lighting: {lighting}." if lighting else "",
            f"Composition: {composition}." if composition else "",
            f"Camera and finish: {camera}; {details}.",
        ]
    return "\n\n".join(part for part in parts if part)


def build_negative(scene: dict) -> str:
    explicit = scene.get("negative_prompt")
    if explicit:
        return explicit.strip()
    return (
        "sitting, seated, tie, necktie, no jacket, shirt only, beard, mustache, stubble, "
        "glasses, crossed arms, folded arms, hand in pocket, cropped hands, hidden hands, "
        "deformed hands, malformed hands, extra fingers, fused fingers, missing fingers, "
        "extra limbs, duplicate limbs, deformed anatomy, bad proportions, cgi, 3d render, "
        "illustration, doll, mannequin, waxy skin, plastic skin, airbrushed skin, blur, text, watermark, logo"
    )


def patch_workflow(template: dict, branch: str, scene: dict, job: dict, seed: int) -> tuple[dict, str]:
    cfg = BRANCHES[branch]
    workflow = copy.deepcopy(template)
    prompt = build_prompt(scene, branch, job)
    workflow[cfg["prompt"]]["inputs"]["text"] = prompt
    workflow[cfg["seed"]]["inputs"]["seed"] = seed
    if "negative" in cfg:
        workflow[cfg["negative"]]["inputs"]["text"] = build_negative(scene)
    if "reference" in cfg:
        workflow[cfg["reference"]]["inputs"]["image"] = job["identity"]["dreamo_reference"]

    # Native Juggernaut XL v9 production preset. Keep renderer-specific
    # inference settings separate from the shared scene specification.
    if branch == "juggernautxl":
        jcfg = job.get("renderer_settings", {}).get("juggernautxl", {})
        latent = workflow[cfg["latent"]]["inputs"]
        sampler = workflow[cfg["sampler"]]["inputs"]
        latent["width"] = int(jcfg.get("width", 832))
        latent["height"] = int(jcfg.get("height", 1216))
        sampler["steps"] = int(jcfg.get("steps", 35))
        sampler["cfg"] = float(jcfg.get("cfg", 5.0))
        sampler["sampler_name"] = jcfg.get("sampler_name", "dpmpp_2m_sde")
        sampler["scheduler"] = jcfg.get("scheduler", "karras")
        sampler["denoise"] = float(jcfg.get("denoise", 1.0))

    prefix = f"ONYX_Ensemble/{job['job_id']}/{scene['scene_id']}/{branch}/{branch}"
    workflow[cfg["save"]]["inputs"]["filename_prefix"] = prefix
    return workflow, prompt


def submit(server: str, workflow: dict, client_id: str) -> str:
    result = http_json(server + "/prompt", {"prompt": workflow, "client_id": client_id})
    if "prompt_id" not in result:
        raise RuntimeError(f"Unexpected /prompt response: {result}")
    return result["prompt_id"]


def run_command_variant(command: list[str], values: dict[str, str]) -> None:
    rendered = [part.format(**values) for part in command]
    subprocess.run(rendered, check=True)


def newest_image(folder: Path, started_at: float) -> Path | None:
    candidates = [
        path for path in folder.glob("**/*")
        if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
        and path.stat().st_mtime >= started_at - 2
    ]
    return max(candidates, key=lambda path: path.stat().st_mtime) if candidates else None


def image_files(folder: Path) -> list[Path]:
    if not folder.exists():
        return []
    return sorted(
        path for path in folder.rglob("*")
        if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
    )


def run_facefusion_batch(job: dict, branch: str, runs: list[dict], work_root: Path) -> None:
    cfg = job.get("identity", {}).get("facefusion", {})
    if not cfg.get("enabled"):
        return

    stage_root = work_root / job["job_id"] / "facefusion" / branch
    input_dir = stage_root / "input"
    output_dir = stage_root / "output"
    if stage_root.exists():
        shutil.rmtree(stage_root)
    input_dir.mkdir(parents=True)
    output_dir.mkdir(parents=True)

    staged: dict[str, dict] = {}
    for run in runs:
        source = run.get("output")
        if not source:
            continue
        source_path = Path(source)
        staged_name = f"{run['scene_id']}__{source_path.name}"
        shutil.copy2(source_path, input_dir / staged_name)
        staged[run["scene_id"]] = run

    if not staged:
        return

    values = {
        "python": cfg.get("launcher_python") or __import__("sys").executable,
        "source_dir": cfg["source_dir"],
        "input_dir": str(input_dir),
        "output_dir": str(output_dir),
    }
    rendered = [part.format_map(values) for part in cfg["command"]]
    subprocess.run(rendered, cwd=cfg.get("working_directory"), check=True)

    produced = image_files(output_dir)
    for scene_id, run in staged.items():
        matches = [path for path in produced if scene_id in path.name]
        if not matches:
            run["facefusion_status"] = "failed"
            run["facefusion_error"] = "No matching output image"
            continue
        source = matches[0]
        destination = Path(run["output"]).parent / "facefusion" / f"{scene_id}_facefusion{source.suffix}"
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        run["facefusion_status"] = "completed"
        run["facefusion_output"] = str(destination)


def patch_dreamo_img2img(template: dict, source_name: str, reference: str, prompt: str,
                          seed: int, prefix: str) -> dict:
    workflow = copy.deepcopy(template)
    workflow["60"]["inputs"]["image"] = source_name
    workflow["52"]["inputs"]["image"] = reference
    workflow["6"]["inputs"]["text"] = prompt
    workflow["31"]["inputs"]["seed"] = seed
    workflow["9"]["inputs"]["filename_prefix"] = prefix
    return workflow


def run_dreamo_img2img(server: str, client_id: str, job: dict, manifest: dict,
                       workflow_dir: Path, output_root: Path, poll_seconds: float) -> None:
    cfg = job.get("identity", {}).get("dreamo_img2img", {})
    if not cfg.get("enabled"):
        return
    comfy_input_root = Path(cfg["comfy_input_root"])
    template = json.loads((workflow_dir / cfg.get("workflow", "dreamo_img2img_api.json")).read_text(encoding="utf-8"))
    reference = job["identity"]["dreamo_reference"]

    candidates = [run for run in manifest["runs"]
                  if run.get("status") == "completed"
                  and run.get("branch") in {"flux", "juggernautxl"}
                  and run.get("output")]
    for index, run in enumerate(candidates):
        source = Path(run["output"])
        relative_input = Path("ONYX_Ensemble") / job["job_id"] / "img2img_inputs" / f"{run['branch']}__{run['scene_id']}{source.suffix}"
        local_input = comfy_input_root / relative_input
        local_input.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, local_input)

        scene = next(scene for scene in job["scenes"] if scene["scene_id"] == run["scene_id"])
        prompt = scene.get("prompts", {}).get("dreamo_img2img") or (
            "A photorealistic professional portrait of the same person from the identity reference, "
            "preserving the exact pose, head angle, body position, hands, clothing, composition, "
            "background and lighting of the source image. Natural facial proportions, realistic eyes, "
            "detailed natural skin texture, authentic high-end editorial photography."
        )
        prefix = f"ONYX_Ensemble/{job['job_id']}/{run['scene_id']}/{run['branch']}/dreamo_img2img/dreamo_img2img"
        workflow = patch_dreamo_img2img(
            template, relative_input.as_posix(), reference, prompt,
            int(run["seed"]) + int(cfg.get("seed_offset", 100000)), prefix,
        )
        try:
            prompt_id = submit(server, workflow, client_id)
            wait_for_prompt(server, prompt_id, poll_seconds)
            result_dir = output_root / "ONYX_Ensemble" / job["job_id"] / run["scene_id"] / run["branch"] / "dreamo_img2img"
            result = newest_image(result_dir, time.time() - 3600)
            run["dreamo_img2img_status"] = "completed"
            run["dreamo_img2img_prompt_id"] = prompt_id
            if result:
                run["dreamo_img2img_output"] = str(result)
        except Exception as exc:
            run["dreamo_img2img_status"] = "failed"
            run["dreamo_img2img_error"] = str(exc)
            print(f"DreamO img2img FAILED: {run['branch']}/{run['scene_id']}: {exc}", flush=True)



def find_workflow_node(workflow: dict, class_type: str, title_contains: str | None = None) -> str:
    """Find a node by class_type instead of relying on fragile ComfyUI node IDs."""
    matches: list[str] = []
    for node_id, node in workflow.items():
        if not isinstance(node, dict) or node.get("class_type") != class_type:
            continue
        if title_contains:
            title = str(node.get("_meta", {}).get("title", "")).lower()
            if title_contains.lower() not in title:
                continue
        matches.append(node_id)

    if not matches:
        raise KeyError(
            f"Workflow node not found: class_type={class_type!r}, "
            f"title_contains={title_contains!r}"
        )
    if len(matches) > 1:
        raise KeyError(
            f"Workflow node is ambiguous: class_type={class_type!r}, "
            f"title_contains={title_contains!r}, matches={matches}"
        )
    return matches[0]


def patch_postprocessor(template: dict, source_name: str, prefix: str, model_name: str | None = None) -> dict:
    """Patch ONYX_Postprocessor API workflow for one source image.

    Node IDs can change whenever the workflow is re-saved in ComfyUI, so find
    the required nodes by class_type instead of hard-coding IDs such as 67/64/66.
    """
    workflow = copy.deepcopy(template)

    load_id = find_workflow_node(workflow, "LoadImage")
    upscale_loader_id = find_workflow_node(workflow, "UpscaleModelLoader")
    save_id = find_workflow_node(workflow, "SaveImageAdvanced")

    workflow[load_id]["inputs"]["image"] = source_name
    workflow[save_id]["inputs"]["filename_prefix"] = prefix
    if model_name:
        workflow[upscale_loader_id]["inputs"]["model_name"] = model_name

    return workflow


def iter_identity_candidates(manifest: dict):
    """Yield (run, method, source_path_string) for identity-bearing outputs."""
    for run in manifest["runs"]:
        branch = run.get("branch")
        candidates: list[tuple[str, str | None]] = []

        if branch == "lora":
            candidates.append(("lora", run.get("output")))
        elif branch == "dreamo":
            candidates.append(("dreamo", run.get("output")))

        if branch in {"flux", "juggernautxl"}:
            candidates.append((f"facefusion_{branch}", run.get("facefusion_output")))
            candidates.append((f"dreamo_img2img_{branch}", run.get("dreamo_img2img_output")))

        for method, source_value in candidates:
            if source_value:
                yield run, method, source_value


def run_postprocessor(server: str, client_id: str, job: dict, manifest: dict,
                      workflow_dir: Path, output_root: Path, poll_seconds: float) -> None:
    """Upscale identity-bearing candidates with ONYX_Postprocessor v0.1.

    By default this stage is disabled. When enabled it runs after identity
    variants have been produced and before/alongside final delivery.

    Optional filters:
      postprocess.methods   -> list of methods to process
      postprocess.scene_ids -> list of scene IDs to process

    This lets the MVP upscale only manually selected finalists instead of
    spending GPU time and disk space on every generated candidate.
    """
    cfg = job.get("postprocess", {})
    if not cfg.get("enabled", False):
        return

    workflow_name = cfg.get("workflow", "ONYX_Postprocessor v0.1.json")
    template = json.loads((workflow_dir / workflow_name).read_text(encoding="utf-8"))

    comfy_input_root_value = cfg.get("comfy_input_root")
    if not comfy_input_root_value:
        raise ValueError("postprocess.comfy_input_root is required when postprocess.enabled=true")
    comfy_input_root = Path(comfy_input_root_value)

    allowed_methods = set(cfg.get("methods", []))
    allowed_scene_ids = set(cfg.get("scene_ids", []))
    model_name = cfg.get("model", "4x_NMKD-Siax_200k.pth")

    processed: list[dict] = []
    for run, method, source_value in iter_identity_candidates(manifest):
        if allowed_methods and method not in allowed_methods:
            continue
        if allowed_scene_ids and run["scene_id"] not in allowed_scene_ids:
            continue

        source = Path(source_value)
        if not source.is_file():
            continue

        # Stage source into ComfyUI/input so LoadImage can access it.
        relative_input = (
            Path("ONYX_Ensemble")
            / job["job_id"]
            / "postprocess_inputs"
            / method
            / f"{run['scene_id']}__{source.name}"
        )
        local_input = comfy_input_root / relative_input
        local_input.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, local_input)

        prefix = (
            f"ONYX_Ensemble/{job['job_id']}/postprocessed/"
            f"{method}/{run['scene_id']}__{method}__upscaled"
        )
        workflow = patch_postprocessor(
            template=template,
            source_name=relative_input.as_posix(),
            prefix=prefix,
            model_name=model_name,
        )

        started_at = time.time()
        try:
            prompt_id = submit(server, workflow, client_id)
            wait_for_prompt(server, prompt_id, poll_seconds)

            result_dir = (
                output_root / "ONYX_Ensemble" / job["job_id"]
                / "postprocessed" / method
            )
            result = newest_image(result_dir, started_at)

            record = {
                "scene_id": run["scene_id"],
                "method": method,
                "source": str(source),
                "status": "completed",
                "prompt_id": prompt_id,
                "elapsed_seconds": round(time.time() - started_at, 2),
            }
            if result:
                record["output"] = str(result)
                run["postprocess_status"] = "completed"
                run["postprocess_method"] = method
                run["postprocess_output"] = str(result)
            else:
                record["status"] = "failed"
                record["error"] = "No postprocessed output image found"
                run["postprocess_status"] = "failed"
                run["postprocess_error"] = record["error"]

            processed.append(record)

        except Exception as exc:
            run["postprocess_status"] = "failed"
            run["postprocess_error"] = str(exc)
            processed.append({
                "scene_id": run["scene_id"],
                "method": method,
                "source": str(source),
                "status": "failed",
                "error": str(exc),
                "elapsed_seconds": round(time.time() - started_at, 2),
            })
            print(f"Postprocess FAILED: {method}/{run['scene_id']}: {exc}", flush=True)

    manifest["postprocess"] = {
        "enabled": True,
        "workflow": workflow_name,
        "model": model_name,
        "count": sum(1 for item in processed if item["status"] == "completed"),
        "runs": processed,
    }

def collect_final_results(job: dict, manifest: dict, job_path: Path) -> Path:
    """Collect customer-facing results into one flat folder.

    Internal provenance (Flux/Juggernaut/DreamO/LoRA/identity method) remains
    in final_results_manifest.json, but the customer sees one photo set rather
    than implementation-specific subfolders.
    """
    configured = job.get("final_results_root")
    root = Path(configured) if configured else job_path.parent / "final_results"
    destination_root = root / job["job_id"]
    destination_root.mkdir(parents=True, exist_ok=True)

    # Avoid stale files from a previous run of the same job.
    for old_file in destination_root.iterdir():
        if old_file.is_file() and old_file.name != "final_results_manifest.json":
            old_file.unlink()

    collected: list[dict] = []
    used_names: set[str] = set()

    for run in manifest["runs"]:
        candidates: list[tuple[str, str | None]] = []
        branch = run.get("branch")
        if branch == "lora":
            candidates.append(("lora", run.get("output")))
        elif branch == "dreamo":
            candidates.append(("dreamo", run.get("output")))
        if branch in {"flux", "juggernautxl"}:
            candidates.append((f"facefusion_{branch}", run.get("facefusion_output")))
            candidates.append((f"dreamo_img2img_{branch}", run.get("dreamo_img2img_output")))

        for method, source_value in candidates:
            if not source_value:
                continue

            original_source = Path(source_value)
            if not original_source.is_file():
                continue

            postprocessed = (
                run.get("postprocess_output")
                if run.get("postprocess_method") == method
                else None
            )
            source = Path(postprocessed) if postprocessed else original_source
            if not source.is_file():
                source = original_source

            # Customer-facing filename intentionally hides the generation
            # method. Preserve scene_id when possible; add a numeric suffix
            # only if several accepted variants exist for the same scene.
            suffix = source.suffix.lower()
            base_name = run["scene_id"]
            filename = f"{base_name}{suffix}"
            counter = 2
            while filename.lower() in used_names or (destination_root / filename).exists():
                filename = f"{base_name}_{counter:02d}{suffix}"
                counter += 1
            used_names.add(filename.lower())

            destination = destination_root / filename
            shutil.copy2(source, destination)

            collected.append({
                "scene_id": run["scene_id"],
                "method": method,
                "branch": branch,
                "source": str(original_source),
                "postprocessed_source": str(source) if source != original_source else None,
                "customer_filename": filename,
                "output": str(destination),
            })

    index_path = destination_root / "final_results_manifest.json"
    index_path.write_text(json.dumps({
        "job_id": job["job_id"],
        "count": len(collected),
        "results": collected,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    manifest["final_results_root"] = str(destination_root)
    manifest["final_results_count"] = len(collected)
    return destination_root


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("job", type=Path)
    parser.add_argument("--server", default="http://127.0.0.1:8188")
    parser.add_argument("--workflows", type=Path, default=Path("workflows"))
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--poll-seconds", type=float, default=1.0)
    parser.add_argument("--free-settle-seconds", type=float, default=10.0)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--postprocess-only",
        action="store_true",
        help="Skip generation and identity stages; reuse the existing job manifest and run only postprocessing + final collection.",
    )
    args = parser.parse_args()

    job = json.loads(args.job.read_text(encoding="utf-8-sig"))
    service_tier = str(job.get("service_tier", "mass")).lower()
    branches = list(job.get("generators", ["flux", "juggernautxl", "dreamo"]))
    lora_enabled = bool(job.get("identity", {}).get("lora", {}).get("enabled", False))
    if "lora" in branches and (service_tier != "vip" or not lora_enabled):
        reason = "VIP tier required" if service_tier != "vip" else "identity.lora.enabled is false"
        print(f"[SKIP] lora: {reason}", flush=True)
        branches.remove("lora")
    templates = {
        branch: json.loads((args.workflows / BRANCHES[branch]["workflow"]).read_text(encoding="utf-8"))
        for branch in branches
    }
    client_id = str(uuid.uuid4())
    work_root = Path(job.get("work_root", args.job.parent / "runs"))

    if args.postprocess_only:
        if args.dry_run:
            raise ValueError("--postprocess-only cannot be combined with --dry-run")
        if not args.output_root:
            raise ValueError("--output-root is required with --postprocess-only")

        manifest_path = args.job.with_name(args.job.stem + ".manifest.json")
        if not manifest_path.is_file():
            raise FileNotFoundError(
                f"Existing manifest not found for --postprocess-only: {manifest_path}"
            )

        manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
        manifest.setdefault("job_id", job["job_id"])
        manifest.setdefault("service_tier", service_tier)
        manifest.setdefault("runs", [])

        http_json(args.server + "/system_stats")
        print("\n=== ONYX Postprocessor (postprocess-only) ===", flush=True)
        run_postprocessor(
            args.server, client_id, job, manifest, args.workflows,
            args.output_root, args.poll_seconds,
        )
        free_memory(args.server, args.free_settle_seconds)

        final_root = collect_final_results(job, manifest, args.job)
        manifest["finished_at"] = time.time()
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(
            f"Final results: {final_root} "
            f"({manifest.get('final_results_count', 0)} files)",
            flush=True,
        )
        print(f"Manifest: {manifest_path}", flush=True)
        return 0

    manifest = {
        "job_id": job["job_id"],
        "service_tier": service_tier,
        "started_at": time.time(),
        "runs": [],
    }

    if not args.dry_run:
        http_json(args.server + "/system_stats")

    for branch in branches:
        print(f"\n=== {branch} ===", flush=True)
        branch_runs: list[dict] = []
        for index, scene in enumerate(job["scenes"]):
            seed = int(scene.get("seed", int(job["base_seed"]) + index))
            workflow, prompt = patch_workflow(templates[branch], branch, scene, job, seed)
            run = {"branch": branch, "scene_id": scene["scene_id"], "seed": seed, "prompt": prompt}
            started_at = time.time()
            try:
                if args.dry_run:
                    print(f"DRY RUN {scene['scene_id']} seed={seed}")
                else:
                    prompt_id = submit(args.server, workflow, client_id)
                    run["prompt_id"] = prompt_id
                    wait_for_prompt(args.server, prompt_id, args.poll_seconds)
                run["status"] = "completed"
            except Exception as exc:
                run["status"] = "failed"
                run["error"] = str(exc)
                manifest["runs"].append(run)
                print(f"FAILED {scene['scene_id']}: {exc}", flush=True)
                if job.get("stop_on_error", False):
                    raise
                continue
            finally:
                run["elapsed_seconds"] = round(time.time() - started_at, 2)
            manifest["runs"].append(run)
            branch_runs.append(run)

            if args.output_root:
                scene_dir = args.output_root / "ONYX_Ensemble" / job["job_id"] / scene["scene_id"] / branch
                target = newest_image(scene_dir, started_at)
                if target:
                    run["output"] = str(target)

        if not args.dry_run:
            print(f"Freeing memory after {branch}...", flush=True)
            free_memory(args.server, args.free_settle_seconds)
            if branch in {"flux", "juggernautxl"}:
                try:
                    print(f"FaceFusion batch: {branch}", flush=True)
                    run_facefusion_batch(job, branch, branch_runs, work_root)
                except Exception as exc:
                    for run in branch_runs:
                        run["facefusion_status"] = "failed"
                        run["facefusion_error"] = str(exc)

    if not args.dry_run and args.output_root:
        print("\n=== DreamO img2img identity variants ===", flush=True)
        run_dreamo_img2img(args.server, client_id, job, manifest, args.workflows,
                           args.output_root, args.poll_seconds)
        free_memory(args.server, args.free_settle_seconds)

        try:
            print("\n=== ONYX Postprocessor ===", flush=True)
            run_postprocessor(
                args.server, client_id, job, manifest, args.workflows,
                args.output_root, args.poll_seconds,
            )
            free_memory(args.server, args.free_settle_seconds)
        except Exception as exc:
            manifest["postprocess_error"] = str(exc)
            print(f"Postprocessor FAILED: {exc}", flush=True)

        try:
            final_root = collect_final_results(job, manifest, args.job)
            print(f"Final results: {final_root} ({manifest['final_results_count']} files)", flush=True)
        except Exception as exc:
            manifest["final_results_error"] = str(exc)
            print(f"Final results collection FAILED: {exc}", flush=True)

    manifest["finished_at"] = time.time()
    manifest_path = args.job.with_name(args.job.stem + ".manifest.json")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nManifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
