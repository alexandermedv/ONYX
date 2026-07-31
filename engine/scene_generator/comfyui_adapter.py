#!/usr/bin/env python3
"""Run the saved Scene Generator and Portrait PostProcessor through ComfyUI API."""

from __future__ import annotations

import argparse
import copy
import json
import random
import re
import shutil
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from typing import Any


IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}


def profile_value(profile: dict[str, Any], name: str, default: str = "unknown") -> str:
    value = profile.get(name, default)
    if isinstance(value, dict):
        value = value.get("value", default)
    return str(value).strip().lower()


def target_age(value: str) -> int:
    numbers = [int(number) for number in re.findall(r"\d+", value)]
    if len(numbers) >= 2:
        return round((numbers[0] + numbers[1]) / 2)
    if numbers:
        return numbers[0]
    raise ValueError(f"Cannot determine target age from profile value: {value!r}")


def profile_settings(profile: dict[str, Any]) -> tuple[dict[str, str], str, str, str]:
    gender_raw = profile_value(profile, "gender")
    gender = "woman" if gender_raw in {"female", "woman"} else "man"
    age = target_age(profile_value(profile, "age_range"))
    body = profile_value(profile, "body_type", "average build")
    hair = profile_value(profile, "hair")
    facial_hair = profile_value(profile, "facial_hair", "unknown")

    hair_parts: list[str] = []
    if hair in {"bald", "shaved", "shaved head", "completely bald"}:
        hair_positive = (
            "(completely bald head:1.35), fully shaved clean scalp, clearly visible bare scalp, "
            "no visible hair on top or sides, natural realistic scalp texture"
        )
        hair_negative = (
            "head hair, full head of hair, thick hair, medium hair, long hair, hairstyle, "
            "styled hair, side-parted hair, pompadour, quiff, visible hairline, wig, toupee"
        )
        hair_parts.append(hair_positive)
    elif hair in {"buzz_cut_3_6mm", "buzz cut 3-6mm", "buzz cut 3–6 mm", "3-6 mm", "3–6 mm"}:
        hair_positive = (
            "(extremely short 3-6 mm buzz cut:1.3), uniform close-cropped hair, "
            "clearly visible scalp, no styled hairstyle"
        )
        hair_negative = (
            "bald head, shaved head, full head of hair, thick hair, medium hair, long hair, "
            "styled hair, side-parted hair, pompadour, quiff, wig, toupee"
        )
        hair_parts.append(hair_positive)
    elif hair not in {"unknown", "none", ""}:
        hair_positive = hair
        hair_negative = ""
        hair_parts.append(hair_positive)
    else:
        hair_positive = ""
        hair_negative = ""
        hair_parts.append("random")

    clean_shaven = facial_hair in {"none", "no", "clean-shaven", "clean shaven", "without facial hair"}
    if clean_shaven:
        hair_parts.append("clean-shaven face, no beard, no mustache")
    elif facial_hair not in {"unknown", ""}:
        hair_parts.append(facial_hair)

    appearance = (
        f"{body}, well-groomed professional appearance, natural {gender} facial features, "
        "healthy realistic skin, youthful mature appearance, subtle natural age lines"
    )
    settings = {
        "gender_setting": gender,
        "age_setting": f"{age}-year-old",
        "appearance_setting": appearance,
        "hair_setting": ", ".join(hair_parts),
    }
    negative = (
        "elderly, old person, senior citizen, aged face, prematurely aged, deep wrinkles, "
        "heavy wrinkles, sagging skin, teenager, very young person, baby face"
    )
    if clean_shaven:
        negative += ", beard, mustache, stubble, gray beard, white beard, gray facial hair"
    if hair_negative:
        negative += ", " + hair_negative
    post_positive = hair_positive
    if clean_shaven:
        post_positive += ", clean-shaven face, no beard, no mustache"
    return settings, negative, post_positive.strip(" ,"), hair_negative


def replace_jinja_setting(text: str, name: str, value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    pattern = rf'({{%\s*set\s+{re.escape(name)}\s*=\s*")[^"]*("\s*%}})'
    updated, count = re.subn(pattern, rf'\g<1>{escaped}\g<2>', text, count=1)
    if count != 1:
        raise ValueError(f"Workflow does not contain Jinja setting {name}")
    return updated


def apply_profile(workflow: dict[str, Any], profile_path: Path, prompt_node: str, negative_node: str) -> None:
    profile = read_json(profile_path)
    settings, negative, _, _ = profile_settings(profile)
    text = workflow[prompt_node]["inputs"]["text"]
    for name, value in settings.items():
        text = replace_jinja_setting(text, name, value)
    # Avoid the ambiguous age word "senior" in the fixed subject description.
    text = text.replace("successful businesswoman, senior corporate executive", "successful businesswoman, corporate executive")
    text = text.replace("successful businessman, senior corporate executive", "successful businessman, corporate executive")
    workflow[prompt_node]["inputs"]["text"] = text
    base_negative = workflow[negative_node]["inputs"]["text"].rstrip(" ,\n")
    workflow[negative_node]["inputs"]["text"] = f"{base_negative},\n\n{negative}"
    print("Applied client profile: " + ", ".join(f"{key}={value}" for key, value in settings.items()))


def append_prompt_text(workflow: dict[str, Any], node_id: str, addition: str) -> None:
    if not addition:
        return
    base = workflow[node_id]["inputs"]["text"].rstrip(" ,\n")
    workflow[node_id]["inputs"]["text"] = f"{base},\n{addition}"


def apply_postprocess_profile(
    workflow: dict[str, Any], profile_path: Path, prompt_node: str, negative_node: str
) -> None:
    profile = read_json(profile_path)
    settings, profile_negative, post_positive, _ = profile_settings(profile)
    append_prompt_text(workflow, prompt_node, post_positive)
    append_prompt_text(workflow, negative_node, profile_negative)
    print(
        "Applied client profile to PostProcessor: "
        + ", ".join(f"{key}={value}" for key, value in settings.items())
    )


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def request_json(url: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data)
    if data is not None:
        request.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def queue_prompt(server: str, workflow: dict[str, Any], client_id: str) -> str:
    response = request_json(f"{server}/prompt", {"prompt": workflow, "client_id": client_id})
    if "prompt_id" not in response:
        raise RuntimeError(f"ComfyUI rejected workflow: {response}")
    return str(response["prompt_id"])


def wait_for_history(server: str, prompt_id: str, timeout: int) -> dict[str, Any]:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        history = request_json(f"{server}/history/{prompt_id}")
        if prompt_id in history:
            record = history[prompt_id]
            status = record.get("status", {})
            if status.get("status_str") == "error":
                raise RuntimeError(f"ComfyUI execution failed: {status.get('messages', status)}")
            return record
        time.sleep(1)
    raise TimeoutError(f"ComfyUI did not finish prompt {prompt_id} in {timeout} seconds")


def convert_saver(workflow: dict[str, Any], node_id: str, prefix: str) -> None:
    node = workflow[node_id]
    image_link = node["inputs"]["images"]
    workflow[node_id] = {
        "inputs": {"filename_prefix": prefix, "images": image_link},
        "class_type": "SaveImage",
        "_meta": {"title": "Job Engine Save Image"},
    }


def collect_outputs(record: dict[str, Any], comfy_output: Path, destination: Path) -> int:
    destination.mkdir(parents=True, exist_ok=True)
    copied = 0
    for node_output in record.get("outputs", {}).values():
        for image in node_output.get("images", []):
            if image.get("type") != "output":
                continue
            source = comfy_output / image.get("subfolder", "") / image["filename"]
            if not source.exists():
                raise FileNotFoundError(f"ComfyUI reported an output that does not exist: {source}")
            target = destination / source.name
            if target.exists():
                target = destination / f"{target.stem}_{uuid.uuid4().hex[:8]}{target.suffix}"
            shutil.copy2(source, target)
            copied += 1
    return copied


def run_one(server: str, workflow: dict[str, Any], comfy_output: Path, destination: Path, timeout: int) -> int:
    client_id = uuid.uuid4().hex
    prompt_id = queue_prompt(server, workflow, client_id)
    record = wait_for_history(server, prompt_id, timeout)
    return collect_outputs(record, comfy_output, destination)


def run_scenes(args: argparse.Namespace) -> int:
    base = read_json(args.workflow)
    if args.profile:
        apply_profile(base, args.profile, args.prompt_node, args.negative_node)
    produced = 0
    for index in range(1, args.count + 1):
        workflow = copy.deepcopy(base)
        workflow[args.seed_node]["inputs"]["seed"] = random.randrange(0, 2**63)
        convert_saver(workflow, args.save_node, f"JobEngine/scenes/scene_{index:03d}")
        count = run_one(args.server, workflow, args.comfy_output, args.output_dir, args.timeout)
        if count < 1:
            raise RuntimeError(f"Scene {index} completed without an output image")
        produced += count
        print(f"[{index}/{args.count}] Scene generated")
    print(f"Generated {produced} scene(s) in {args.output_dir}")
    return 0


def images_in(folder: Path) -> list[Path]:
    return sorted(path for path in folder.iterdir() if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES)


def run_postprocess(args: argparse.Namespace) -> int:
    base = read_json(args.workflow)
    if args.profile:
        apply_postprocess_profile(base, args.profile, args.prompt_node, args.negative_node)
    sources = images_in(args.input_dir)
    if not sources:
        raise RuntimeError(f"No images found in {args.input_dir}")
    args.comfy_input.mkdir(parents=True, exist_ok=True)
    produced = 0
    for index, source in enumerate(sources, 1):
        workflow = copy.deepcopy(base)
        uploaded_name = f"job_engine_{uuid.uuid4().hex}_{source.name}"
        comfy_source = args.comfy_input / uploaded_name
        shutil.copy2(source, comfy_source)
        try:
            workflow[args.load_node]["inputs"]["image"] = uploaded_name
            if args.seed_node in workflow:
                workflow[args.seed_node]["inputs"]["seed"] = random.randrange(0, 2**63)
            convert_saver(workflow, args.save_node, f"JobEngine/final/{source.stem}")
            count = run_one(args.server, workflow, args.comfy_output, args.output_dir, args.timeout)
            if count < 1:
                raise RuntimeError(f"PostProcessor completed without output for {source.name}")
            produced += count
            print(f"[{index}/{len(sources)}] Processed {source.name}")
        finally:
            comfy_source.unlink(missing_ok=True)
    print(f"Postprocessed {produced} image(s) in {args.output_dir}")
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="ComfyUI API adapter for Job Engine v1.3")
    root.add_argument("--server", default="http://127.0.0.1:8188")
    root.add_argument("--comfy-output", type=Path, required=True)
    root.add_argument("--timeout", type=int, default=1800)
    commands = root.add_subparsers(dest="mode", required=True)

    scenes = commands.add_parser("scenes")
    scenes.add_argument("--workflow", type=Path, required=True)
    scenes.add_argument("--output-dir", type=Path, required=True)
    scenes.add_argument("--count", type=int, default=1)
    scenes.add_argument("--profile", type=Path)
    scenes.add_argument("--prompt-node", default="13")
    scenes.add_argument("--negative-node", default="3")
    scenes.add_argument("--seed-node", default="5")
    scenes.add_argument("--save-node", default="12")
    scenes.set_defaults(handler=run_scenes)

    post = commands.add_parser("postprocess")
    post.add_argument("--workflow", type=Path, required=True)
    post.add_argument("--input-dir", type=Path, required=True)
    post.add_argument("--output-dir", type=Path, required=True)
    post.add_argument("--comfy-input", type=Path, required=True)
    post.add_argument("--profile", type=Path)
    post.add_argument("--prompt-node", default="9")
    post.add_argument("--negative-node", default="10")
    post.add_argument("--load-node", default="1")
    post.add_argument("--seed-node", default="6")
    post.add_argument("--save-node", default="5")
    post.set_defaults(handler=run_postprocess)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        return args.handler(args)
    except urllib.error.URLError as exc:
        print(f"Cannot connect to ComfyUI at {args.server}: {exc}")
        return 1
    except Exception as exc:
        print(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
