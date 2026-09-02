from __future__ import annotations

import csv
import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path

from .captions import CaptionPolicy, validate_caption
from .io import read_json, read_jsonl, write_json


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def build_approved_manifest(selection_path: Path, caption_proposal_path: Path,
                            membership_path: Path, historical_manifest_path: Path,
                            historical_caption_root: Path) -> dict:
    selection = read_jsonl(selection_path)
    by_name = {Path(row["source_path"]).name: row for row in selection}
    membership = read_json(membership_path)
    captions = {row["filename"]: row["caption"] for row in read_json(caption_proposal_path)["captions"]}
    with historical_manifest_path.open("r", encoding="utf-8-sig", newline="") as stream:
        historical_rows = list(csv.DictReader(stream))
    historical_names = [row["OriginalName"] for row in historical_rows]
    historical_dataset_names = {row["OriginalName"]: row["DatasetName"] for row in historical_rows}
    datasets: dict[str, dict] = {}
    for dataset_id in ("mini_3", "mini_5", "mini_10"):
        names = membership[dataset_id]
        items = []
        for name in names:
            record = by_name[name]
            caption = captions[name]
            items.append({"filename": name, "source_path": record["source_path"], "sha256": record["sha256"],
                          "caption": caption, "caption_sha256": hashlib.sha256(caption.encode("utf-8")).hexdigest()})
        datasets[dataset_id] = {"size": len(items), "items": items}
    full_items = []
    for name in historical_names:
        record = by_name[name]
        caption_file = historical_caption_root / Path(historical_dataset_names[name]).with_suffix(".txt")
        caption = caption_file.read_text(encoding="utf-8").lstrip("\ufeff").strip()
        full_items.append({"filename": name, "source_path": record["source_path"], "sha256": record["sha256"],
                           "caption": caption, "caption_sha256": hashlib.sha256(caption.encode("utf-8")).hexdigest()})
    datasets["full_21"] = {"size": 21, "items": full_items}
    mini3 = {item["sha256"] for item in datasets["mini_3"]["items"]}
    mini5 = {item["sha256"] for item in datasets["mini_5"]["items"]}
    mini10 = {item["sha256"] for item in datasets["mini_10"]["items"]}
    if not mini3 < mini5 < mini10:
        raise ValueError("approved mini memberships are not strictly nested")
    return {
        "schema": "onyx.lora_lab.approved_dataset_manifest", "schema_version": "1.0",
        "experiment_id": "alexander_lora_dataset_size_v1", "status": "approved",
        "approval": membership, "automatic_proposal_preserved_at": membership["automatic_proposal"],
        "datasets": datasets,
    }


def materialize_approved(manifest: dict, target_root: Path) -> dict:
    if target_root.exists():
        raise FileExistsError(f"immutable target already exists: {target_root}")
    target_root.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{target_root.name}.staging-", dir=target_root.parent))
    try:
        verification = {}
        for dataset_id, dataset in manifest["datasets"].items():
            folder = staging / "datasets" / dataset_id
            folder.mkdir(parents=True)
            rows = []
            for index, item in enumerate(dataset["items"], start=1):
                source = Path(item["source_path"])
                image_name = f"alexonyx_{index:03d}{source.suffix.lower()}"
                image_target = folder / image_name
                caption_target = folder / f"alexonyx_{index:03d}.txt"
                shutil.copy2(source, image_target)
                caption_target.write_text(item["caption"] + "\n", encoding="utf-8", newline="\n")
                actual_hash = file_hash(image_target)
                if actual_hash != item["sha256"]:
                    raise RuntimeError(f"hash mismatch after copy: {source}")
                rows.append({**item, "materialized_image": str(target_root / "datasets" / dataset_id / image_name),
                             "materialized_caption": str(target_root / "datasets" / dataset_id / caption_target.name)})
            verification[dataset_id] = {"images": len(list(folder.glob("*.jpg"))) + len(list(folder.glob("*.png"))) + len(list(folder.glob("*.webp"))),
                                        "captions": len(list(folder.glob("*.txt"))), "items": rows}
        resolved = {**manifest, "runtime_root": str(target_root), "materialization": verification}
        write_json(staging / "approved_immutable_manifest.json", resolved)
        os.replace(staging, target_root)
        return resolved
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise


def verify_materialized(root: Path) -> dict:
    manifest = read_json(root / "approved_immutable_manifest.json")
    results = {}
    for dataset_id, dataset in manifest["materialization"].items():
        mismatches = []
        for item in dataset["items"]:
            path = Path(item["materialized_image"])
            if not path.exists() or file_hash(path) != item["sha256"]:
                mismatches.append(str(path))
        results[dataset_id] = {"images": dataset["images"], "captions": dataset["captions"],
                               "hash_mismatches": mismatches, "valid": not mismatches and dataset["images"] == dataset["captions"]}
    results["valid"] = all(row["valid"] for row in results.values())
    return results
