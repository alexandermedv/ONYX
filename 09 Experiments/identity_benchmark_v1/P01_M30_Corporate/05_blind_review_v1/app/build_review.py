"""Build and verify the immutable input package for P01 blind review v1."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
BENCHMARK = ROOT.parent
RUNS = BENCHMARK / "03_benchmark_runs"
SCENES = ("BUS_01", "BUS_06", "BUS_09")
SEED = 20260912
LETTERS = tuple("ABCDEFGHIJKL")
SCORE_COLUMNS = (
    "review_id", "scene", "candidate_id", "identity_score", "realism_score",
    "scene_score", "commercial_score", "verdict", "comment", "reviewed_at",
)


def path(*parts: str) -> str:
    return str(RUNS.joinpath(*parts).resolve())


PARTICIPANTS = {
    "gpt_images_25": {
        "model_name": "GPT Images 2.5",
        "sources": {scene: path("gpt_images_25_qualifier_v1", f"P01_{scene}_GPT_IMAGES_25.png") for scene in SCENES},
    },
    "qwen": {
        "model_name": "Qwen",
        "sources": {scene: path("qwen_qualifier_v1", f"P01_{scene}_QWEN.png") for scene in SCENES},
    },
    "kandinsky": {
        "model_name": "Kandinsky",
        "sources": {scene: path("kandinsky_qualifier_v1", f"P01_{scene}_KANDINSKY.jpeg") for scene in SCENES},
    },
    "ideogram": {
        "model_name": "Ideogram",
        "sources": {scene: path("ideogram_qualifier_v1", f"P01_{scene}_IDEOGRAM.jpg") for scene in SCENES},
    },
    "pulid": {
        "model_name": "PuLID",
        "sources": {
            "BUS_01": path("local_pulid_baseline_v3", "outputs", "P01_BUS_01_PULID_BASELINE_00001_.png"),
            "BUS_06": path("pulid_multiscene_v1", "outputs", "P01_BUS_06_PULID_00001_.png"),
            "BUS_09": path("pulid_multiscene_v1", "outputs", "P01_BUS_09_PULID_00001_.png"),
        },
    },
    "flux_kontext": {
        "model_name": "FLUX Kontext",
        "sources": {
            "BUS_01": path("flux_kontext_qualifier_v1", "outputs", "P01_BUS_01_KONTEXT.png"),
            "BUS_06": path("flux_kontext_repair_v1", "outputs", "P01_BUS_06_KONTEXT_REPAIR.png"),
            "BUS_09": path("flux_kontext_repair_v1", "outputs", "P01_BUS_09_KONTEXT_REPAIR.png"),
        },
    },
    **{
        f"mini{dataset}_{checkpoint}": {
            "model_name": f"mini-{dataset} @ {checkpoint}",
            "sources": {
                "BUS_01": path("checkpoint_benchmark_v1", "outputs", f"P01_BUS_01_p01_mini_{dataset}__{checkpoint}_00001_.png"),
                "BUS_06": path("local_qualifier_tail_v1", "outputs", f"P01_BUS_06_MINI{dataset}_{checkpoint}_00001_.png"),
                "BUS_09": path("local_qualifier_tail_v1", "outputs", f"P01_BUS_09_MINI{dataset}_{checkpoint}_00001_.png"),
            },
        }
        for dataset in (3, 5) for checkpoint in ("0750", "1000", "1250")
    },
}

REFERENCES = {
    "master": str((BENCHMARK / "00_master" / "P01_identity_master_v1.png").resolve()),
    "references": [
        str((BENCHMARK / "01_references" / name).resolve())
        for name in ("P01_REF01_frontal.png", "P01_REF02_right_3q.png", "P01_REF03_left_3q_smile.png")
    ],
}


def sha256(image: Path) -> str:
    digest = hashlib.sha256()
    with image.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def decode_image(image: Path) -> dict[str, int | str]:
    with Image.open(image) as opened:
        opened.verify()
    with Image.open(image) as opened:
        return {"format": opened.format or "", "width": opened.width, "height": opened.height}


def atomic_json(destination: Path, value: object) -> None:
    temporary = destination.with_suffix(destination.suffix + ".writing")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(destination)


def write_empty_scores(destination: Path, order: list[dict[str, str]]) -> None:
    temporary = destination.with_suffix(".writing.csv")
    with temporary.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=SCORE_COLUMNS)
        writer.writeheader()
        for item in order:
            writer.writerow({"review_id": "P01_blind_review_v1", "scene": item["scene"], "candidate_id": item["candidate_id"]})
    temporary.replace(destination)


def build_mapping() -> tuple[dict[str, object], list[dict[str, str]]]:
    participant_ids = sorted(PARTICIPANTS)
    mapping: dict[str, dict[str, str]] = {}
    order: list[dict[str, str]] = []
    for offset, scene in enumerate(SCENES):
        shuffled = participant_ids.copy()
        random.Random(SEED + offset).shuffle(shuffled)
        mapping[scene] = dict(zip(LETTERS, shuffled, strict=True))
        order.extend({"scene": scene, "candidate_id": f"{scene}-{letter}"} for letter in LETTERS)
    secret_participants = {
        participant_id: {
            "source": participant["sources"],
            "model_name": participant["model_name"],
        }
        for participant_id, participant in PARTICIPANTS.items()
    }
    return {
        "schema": "onyx.identity_benchmark.blind_mapping",
        "schema_version": "1.0",
        "blind_review_seed": SEED,
        "mapping": mapping,
        "participants": secret_participants,
    }, order


def verify(root: Path) -> dict[str, object]:
    mapping_path, config_path, scores_path = root / "blind_mapping.json", root / "review_config.json", root / "blind_review_scores.csv"
    mapping = json.loads(mapping_path.read_text(encoding="utf-8-sig"))
    config = json.loads(config_path.read_text(encoding="utf-8-sig"))
    errors: list[str] = []
    if mapping.get("blind_review_seed") != SEED:
        errors.append("blind mapping seed differs")
    candidate_ids = [item["candidate_id"] for item in config.get("review_order", [])]
    if len(candidate_ids) != 36 or len(set(candidate_ids)) != 36:
        errors.append("review order must contain 36 unique candidates")
    for scene in SCENES:
        labels = mapping.get("mapping", {}).get(scene, {})
        if set(labels) != set(LETTERS) or len(set(labels.values())) != 12:
            errors.append(f"{scene} mapping is incomplete or duplicated")
    images = [Path(REFERENCES["master"]), *(Path(item) for item in REFERENCES["references"])]
    images += [Path(source) for participant in mapping.get("participants", {}).values() for source in participant.get("source", {}).values()]
    if len(images) != 40 or len({str(item) for item in images}) != 40:
        errors.append("expected 36 candidates plus 4 canonical references")
    decoded: list[dict[str, object]] = []
    for image in images:
        if not image.is_file():
            errors.append(f"missing: {image}")
            continue
        try:
            decoded.append({"path": str(image), "sha256": sha256(image), **decode_image(image)})
        except Exception as exc:  # pragma: no cover - diagnostic path
            errors.append(f"not decodable: {image}: {exc}")
    with scores_path.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    if [row.get("candidate_id") for row in rows] != candidate_ids:
        errors.append("score rows do not match the immutable review order")
    return {"ok": not errors, "errors": errors, "candidate_count": 36, "scene_counts": {scene: sum(item["scene"] == scene for item in config["review_order"]) for scene in SCENES}, "decoded_images": decoded}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    ROOT.mkdir(parents=True, exist_ok=True)
    mapping_path, config_path, scores_path = ROOT / "blind_mapping.json", ROOT / "review_config.json", ROOT / "blind_review_scores.csv"
    if args.verify:
        result = verify(ROOT)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["ok"] else 1
    if any(path.exists() for path in (mapping_path, config_path, scores_path)):
        raise FileExistsError("blind review package already exists; use --verify rather than regenerating its mapping")
    mapping, order = build_mapping()
    config = {
        "schema": "onyx.identity_benchmark.blind_review_config",
        "schema_version": "1.0",
        "review_id": "P01_blind_review_v1",
        "references": REFERENCES,
        "review_order": order,
        "score_weights": {"identity": 0.40, "realism": 0.20, "scene": 0.15, "commercial": 0.25},
        "verdicts": ["PASS", "REPAIR", "REGENERATE", "REJECT"],
    }
    atomic_json(mapping_path, mapping)
    atomic_json(config_path, config)
    write_empty_scores(scores_path, order)
    result = verify(ROOT)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
