"""Reveal completed blind scores and write reproducible P01 benchmark summaries."""
from __future__ import annotations

import csv
import json
import os
import statistics
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
SCENES = ("BUS_01", "BUS_06", "BUS_09")
SCORE_FIELDS = ("identity_score", "realism_score", "scene_score", "commercial_score")
WEIGHTS = {"identity_score": 0.40, "realism_score": 0.20, "scene_score": 0.15, "commercial_score": 0.25}
PRODUCT = {
    "mini3_0750": ("Local training", "Yes", "3", "Local", "Not recorded", "LoRA training + local ComfyUI"),
    "mini3_1000": ("Local training", "Yes", "3", "Local", "Not recorded", "LoRA training + local ComfyUI"),
    "mini3_1250": ("Local training", "Yes", "3", "Local", "Not recorded", "LoRA training + local ComfyUI"),
    "mini5_0750": ("Local training", "Yes", "5", "Local", "Not recorded", "LoRA training + local ComfyUI"),
    "mini5_1000": ("Local training", "Yes", "5", "Local", "Not recorded", "LoRA training + local ComfyUI"),
    "mini5_1250": ("Local training", "Yes", "5", "Local", "Not recorded", "LoRA training + local ComfyUI"),
    "pulid": ("Local reference-based", "No", "3", "Local", "348.15 s recorded for BUS_01 baseline", "ComfyUI + PuLID custom node and weights"),
    "flux_kontext": ("Local reference-based", "No", "1", "Local", "~58 s recorded for each repair scene", "Native FLUX Kontext ComfyUI graph"),
    "gpt_images_25": ("External/cloud", "No", "Not recorded", "Cloud", "Not recorded", "External image service"),
    "qwen": ("External/cloud", "No", "Not recorded", "Cloud", "Not recorded", "External image service"),
    "kandinsky": ("External/cloud", "No", "Not recorded", "Cloud", "Not recorded", "External image service"),
    "ideogram": ("External/cloud", "No", "1", "Cloud", "Not recorded", "Web UI; first official batch output"),
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def mean(rows: Iterable[dict[str, Any]], key: str) -> float:
    values = [float(row[key]) for row in rows]
    return statistics.fmean(values)


def median(rows: Iterable[dict[str, Any]], key: str) -> float:
    return statistics.median(float(row[key]) for row in rows)


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str]) -> None:
    temporary = path.with_suffix(".writing.csv")
    with temporary.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def fmt(value: float) -> str:
    return f"{value:.2f}"


def summary(rows: list[dict[str, Any]], participant_id: str, model: str, scene: str = "ALL") -> dict[str, Any]:
    counts = {verdict: sum(row["verdict"] == verdict for row in rows) for verdict in ("PASS", "REPAIR", "REGENERATE", "REJECT")}
    size = len(rows)
    return {
        "participant_id": participant_id, "model": model, "scene": scene, "n": size,
        "mean_identity": round(mean(rows, "identity_score"), 4), "median_identity": round(median(rows, "identity_score"), 4),
        "mean_realism": round(mean(rows, "realism_score"), 4), "mean_scene_anatomy": round(mean(rows, "scene_score"), 4),
        "mean_commercial": round(mean(rows, "commercial_score"), 4), "mean_overall_score": round(mean(rows, "overall_score"), 4),
        "median_overall_score": round(median(rows, "overall_score"), 4),
        **{f"{verdict.lower()}_count": counts[verdict] for verdict in counts},
        **{f"{verdict.lower()}_rate": round(counts[verdict] / size, 4) for verdict in counts},
        "pass_repair_rate": round((counts["PASS"] + counts["REPAIR"]) / size, 4),
    }


def rank(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ordered = sorted(rows, key=lambda row: (-row["mean_overall_score"], -row["mean_identity"], -row["mean_commercial"], -row["pass_repair_rate"], row["model"]))
    for index, row in enumerate(ordered, 1):
        row["rank"] = index
    return ordered


def markdown_table(rows: list[dict[str, Any]], columns: list[tuple[str, str]]) -> str:
    header = "| " + " | ".join(label for _, label in columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(str(row[key]) for key, _ in columns) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def main() -> int:
    config = read_json(ROOT / "review_config.json")
    mapping = read_json(ROOT / "blind_mapping.json")
    state = read_json(ROOT / "review_state.json")
    if not state.get("finished_at"):
        raise ValueError("blind review is not marked complete")
    with (ROOT / "blind_review_scores.csv").open(encoding="utf-8-sig", newline="") as stream:
        scores = list(csv.DictReader(stream))
    expected_ids = [item["candidate_id"] for item in config["review_order"]]
    if len(scores) != 36 or [row["candidate_id"] for row in scores] != expected_ids or len(set(expected_ids)) != 36:
        raise ValueError("scores must be exactly the 36 immutable review candidates")
    revealed: list[dict[str, Any]] = []
    for row in scores:
        if any(not row.get(field, "").strip() for field in (*SCORE_FIELDS, "verdict", "reviewed_at")):
            raise ValueError(f"incomplete score: {row['candidate_id']}")
        scene, letter = row["scene"], row["candidate_id"].rsplit("-", 1)[1]
        if scene not in SCENES or letter not in mapping["mapping"][scene]:
            raise ValueError(f"invalid candidate mapping: {row['candidate_id']}")
        participant_id = mapping["mapping"][scene][letter]
        participant = mapping["participants"][participant_id]
        values = {field: int(row[field]) for field in SCORE_FIELDS}
        if any(value not in {1, 2, 3, 4, 5} for value in values.values()):
            raise ValueError(f"invalid score: {row['candidate_id']}")
        overall = sum(values[field] * WEIGHTS[field] for field in SCORE_FIELDS)
        revealed.append({**row, **values, "participant_id": participant_id, "model": participant["model_name"].replace("0750", "750"), "source_path": participant["source"][scene], "overall_score": round(overall, 4)})
    participant_scenes = defaultdict(set)
    for row in revealed:
        participant_scenes[row["participant_id"]].add(row["scene"])
    if len(participant_scenes) != 12 or any(scenes != set(SCENES) for scenes in participant_scenes.values()):
        raise ValueError("each of the 12 participants must have each of the 3 scenes exactly once")
    RESULTS.mkdir(exist_ok=True)
    revealed_columns = ["review_id", "scene", "candidate_id", "participant_id", "model", "identity_score", "realism_score", "scene_score", "commercial_score", "overall_score", "verdict", "comment", "reviewed_at", "source_path"]
    write_csv(RESULTS / "revealed_scores.csv", revealed, revealed_columns)
    by_participant = defaultdict(list)
    by_scene = defaultdict(list)
    for row in revealed:
        by_participant[row["participant_id"]].append(row)
        by_scene[row["scene"]].append(row)
    model_rows = rank([summary(rows, participant_id, rows[0]["model"]) for participant_id, rows in by_participant.items()])
    model_columns = ["rank", "participant_id", "model", "n", "mean_identity", "median_identity", "mean_realism", "mean_scene_anatomy", "mean_commercial", "mean_overall_score", "median_overall_score", "pass_count", "pass_rate", "repair_count", "repair_rate", "regenerate_count", "regenerate_rate", "reject_count", "reject_rate", "pass_repair_rate"]
    write_csv(RESULTS / "model_summary.csv", model_rows, model_columns)
    scene_rows: list[dict[str, Any]] = []
    for scene in SCENES:
        rows = [summary([row], row["participant_id"], row["model"], scene) for row in by_scene[scene]]
        scene_rows.extend(rank(rows))
    write_csv(RESULTS / "scene_summary.csv", scene_rows, model_columns)
    mini = [row for row in revealed if row["participant_id"].startswith("mini")]
    def mini_key(row: dict[str, Any]) -> tuple[str, str]:
        identifier = row["participant_id"]
        return ("mini-" + identifier[4], str(int(identifier.rsplit("_", 1)[1])))
    mini_rows: list[dict[str, Any]] = []
    groups: dict[tuple[str, str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in mini:
        dataset, checkpoint = mini_key(row)
        groups[("interaction", dataset, checkpoint, "ALL")].append(row)
        groups[("dataset_size", dataset, "ALL", "ALL")].append(row)
        groups[("checkpoint", "ALL", checkpoint, "ALL")].append(row)
        groups[("dataset_size_by_scene", dataset, "ALL", row["scene"])].append(row)
    for (scope, dataset, checkpoint, scene), rows in sorted(groups.items()):
        item = summary(rows, "", f"{dataset} @ {checkpoint}" if checkpoint != "ALL" else dataset, scene)
        item.update({"scope": scope, "dataset_size": dataset, "checkpoint": checkpoint})
        mini_rows.append(item)
    mini_columns = ["scope", "dataset_size", "checkpoint", "scene", "n", "mean_identity", "mean_realism", "mean_scene_anatomy", "mean_commercial", "mean_overall_score", "median_overall_score", "pass_repair_rate"]
    write_csv(RESULTS / "mini_lora_analysis.csv", mini_rows, mini_columns)
    by_model = {row["participant_id"]: row for row in model_rows}
    shortlist_ids = ("gpt_images_25", "mini3_1250", "mini5_1000", "flux_kontext", "ideogram")
    shortlist = [by_model[item] for item in shortlist_ids]
    ranking_md = ["# P01 blind review v1 — revealed ranking", "", f"Review completion: 36 / 36. Mapping was revealed after `{state['finished_at']}`. Overall score = 40% Identity + 20% Realism + 15% Scene/Anatomy + 25% Commercial.", "", "## Overall ranking", "", markdown_table(model_rows, [("rank", "Rank"), ("model", "Model"), ("mean_identity", "Identity"), ("mean_realism", "Realism"), ("mean_scene_anatomy", "Scene"), ("mean_commercial", "Commercial"), ("mean_overall_score", "Overall"), ("pass_repair_rate", "PASS+REPAIR")]), "", "## Scene rankings"]
    for scene in SCENES:
        scene_ranked = [row for row in scene_rows if row["scene"] == scene]
        ranking_md.extend(["", f"### {scene}", "", markdown_table(scene_ranked, [("rank", "Rank"), ("model", "Model"), ("mean_identity", "Identity"), ("mean_realism", "Realism"), ("mean_scene_anatomy", "Scene"), ("mean_commercial", "Commercial"), ("mean_overall_score", "Overall"), ("pass_repair_rate", "PASS+REPAIR")])])
    ranking_md.extend(["", "## Scene interpretation", "", "- **BUS_01 close-up:** GPT Images 2.5 and Ideogram tie at 4.85. FLUX Kontext keeps identity at 5.0 but trails them on scene and commercial score.", "- **BUS_06 desk:** GPT Images 2.5 (4.65) and Ideogram (4.60) lead. mini-5 @ 1250 reaches 4.00, while mini-3 @ 1250 and mini-5 @ 1000 receive the strongest Scene/Anatomy score of 5.0 among local LoRAs.", "- **BUS_09 full body:** GPT Images 2.5 leads at 4.20. mini-3 @ 1250 (3.70) and mini-5 @ 1000 (3.55) are the only local LoRAs without a rejection. FLUX Kontext retains Identity 5.0 but has Realism and Commercial scores of 1.0, so it is not delivery-ready for this scene.", "", "## mini-LoRA findings", "", "- mini-5 averages 3.37 versus mini-3 at 3.27: a small +0.09 overall difference across nine reviewed images. The gain is concentrated in BUS_06 (+0.32); BUS_01 and BUS_09 are each about 0.02 lower for mini-5.", "- Across both dataset sizes, checkpoint 1250 has the highest aggregate score (3.43), ahead of 750 (3.35) and 1000 (3.18). The interaction matters: mini-3 @ 1250 is the best and most stable local variant (3.67; no reject), while mini-5 peaks at 750 (3.52) and mini-5 @ 1000 is the only mini-5 variant with PASS+REPAIR on all three scenes.", "- The mini-5 decline at 1250 is driven by full-body identity and commercial scores of 1.0 despite Realism and Scene scores of 5.0. That is evidence consistent with overtraining or identity/style decoupling in this small sample, not proof of its cause.", "", "## Method comparison", "", "- **Local training:** mini-3 @ 1250 is the strongest local trained result. The review does not justify requiring five photos for this character; three photos at 1250 outperform every mini-5 checkpoint.", "- **Local reference-based:** FLUX Kontext is highly competitive on identity but not robust enough for full-body delivery. PuLID scores 1.48 overall with three REJECT outcomes and should remain only as an archived baseline.", "- **External/cloud:** GPT Images 2.5 is the clear quality and identity leader. Ideogram is strong for close-up and desk scenes but fails full-body identity. Kandinsky is mid-pack; Qwen is not competitive in this qualifier.", "", "## Product metadata", "", markdown_table([{"model": row["model"], "quality": fmt(row["mean_overall_score"]), "identity": fmt(row["mean_identity"]), "training": PRODUCT[row["participant_id"]][1], "refs": PRODUCT[row["participant_id"]][2], "location": PRODUCT[row["participant_id"]][3], "speed": PRODUCT[row["participant_id"]][4], "complexity": PRODUCT[row["participant_id"]][5]} for row in model_rows], [("model", "Model"), ("quality", "Quality"), ("identity", "Identity"), ("training", "Training needed"), ("refs", "Ref count"), ("location", "Local/Cloud"), ("speed", "Speed"), ("complexity", "Complexity")])])
    (RESULTS / "final_ranking.md").write_text("\n".join(ranking_md) + "\n", encoding="utf-8")
    shortlist_md = ["# P01 final 10-scene round shortlist", "", "## Core finalists", "", "1. **GPT Images 2.5** — best overall score and the only finalist with PASS on all three scenes.", "2. **mini-3 @ 1250** — best local LoRA, strongest local full-body result, and the narrowest three-scene score range.", "3. **mini-5 @ 1000** — the most stable mini-5 checkpoint; its full-body result is REPAIR rather than a reject.", "", "## Diagnostic finalists", "", "4. **FLUX Kontext** — top identity score across all three scenes, but its BUS_09 realism and commercial result require a robustness check.", "5. **Ideogram** — excellent BUS_01 and BUS_06 commercial quality, but BUS_09 identity failed; retain only to test whether this failure persists over a larger scene set.", "", "The shortlist intentionally excludes higher-average variants with a rejected full-body frame when a more stable alternative is available. No final-round generation is started by this analysis.", "", "## Ranked evidence", "", markdown_table(shortlist, [("rank", "Overall rank"), ("model", "Model"), ("mean_identity", "Identity"), ("mean_overall_score", "Overall"), ("pass_repair_rate", "PASS+REPAIR")])]
    (RESULTS / "shortlist.md").write_text("\n".join(shortlist_md) + "\n", encoding="utf-8")
    print(json.dumps({"completed": len(revealed), "models": len(model_rows), "top_model": model_rows[0]["model"], "top_overall": model_rows[0]["mean_overall_score"], "results": str(RESULTS)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
