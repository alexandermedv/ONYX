from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from .analyzer import analyze_pool
from .benchmark import plan_benchmark
from .benchmark_executor import build_checkpoint_inventory, checkpoint_mapping, execute_plan, stage_checkpoints
from .captions import CaptionPolicy, validate_caption
from .io import read_json, read_jsonl, write_csv, write_json, write_jsonl
from .materialize import build_approved_manifest, materialize_approved, verify_materialized
from .models import DatasetSpec, SourceRecord
from .preflight import build_night_plan, render_smoke_config
from .review import create_comparison_sheet, create_selection_report, selection_rows
from .selector import select_nested
from .specs import load_benchmark_spec, load_training_spec
from .training import plan_training
from .trainers.ai_toolkit import config_as_yaml, render_ai_toolkit_config


def records_from_jsonl(path: Path) -> list[SourceRecord]:
    return [SourceRecord(**row) for row in read_jsonl(path)]


def apply_metadata_overrides(records: list[SourceRecord], path: Path | None) -> list[SourceRecord]:
    if path is None:
        return records
    from dataclasses import replace
    overrides = read_json(path)
    allowed = {"capture_group", "expression_bucket", "lighting_bucket", "caption"}
    result = []
    for record in records:
        values = overrides.get(Path(record.source_path).name, {})
        unknown = set(values) - allowed
        if unknown:
            raise ValueError(f"unsupported metadata override fields: {sorted(unknown)}")
        result.append(replace(record, **values) if values else record)
    return result


def command_analyze(args: argparse.Namespace) -> None:
    refs = [path for path in args.references.iterdir() if path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}]
    records = analyze_pool(args.source, args.historical_manifest, refs, capture_group=args.capture_group)
    write_jsonl(args.output / f"source_analysis_{len(records)}.jsonl", records)
    write_json(args.output / "source_analysis_summary.json", {
        "pool_size": len(records), "historical_full_21_count": sum(row.historical_full_21 for row in records),
        "reference_directory": str(args.references), "provider": "InsightFace buffalo_l CPUExecutionProvider",
        "capture_group": args.capture_group,
    })


def command_select(args: argparse.Namespace) -> None:
    input_records = []
    for analysis in args.analysis:
        input_records.extend(records_from_jsonl(analysis))
    input_records = apply_metadata_overrides(input_records, args.metadata_overrides)
    hashes = [record.sha256 for record in input_records]
    if len(hashes) != len(set(hashes)):
        raise ValueError("analysis inputs contain duplicate source hashes")
    records, memberships = select_nested(input_records)
    write_jsonl(args.output / "selection_analysis.jsonl", records)
    selected = {row.sha256: row for row in records}
    manifest = {
        "schema": "onyx.lora_lab.dataset_manifest", "schema_version": "1.0",
        "status": "proposed_requires_human_approval", "source_analysis": [str(path) for path in args.analysis],
        "control_policy": "full_21 is the immutable historical baseline; minis are selected from the expanded client pool and need not be subsets of full_21",
        "datasets": {},
    }
    for dataset_id, hashes in memberships.items():
        manifest["datasets"][dataset_id] = {
            "size": len(hashes), "sha256": hashes,
            "sources": [selected[value].source_path for value in hashes],
        }
    write_json(args.output / "dataset_manifest.proposed.json", manifest)
    write_csv(args.output / "selection_report.csv", selection_rows(records))
    create_selection_report(records, args.output / "selection_contact_sheet.jpg")
    if args.comparison_old:
        create_comparison_sheet(records, args.comparison_old, args.output / "old_vs_new_mini3.jpg")


def command_captions(args: argparse.Namespace) -> None:
    import csv
    records = records_from_jsonl(args.selection)
    with args.historical_manifest.open("r", encoding="utf-8-sig", newline="") as stream:
        historical_map = {row["OriginalName"]: row["DatasetName"] for row in csv.DictReader(stream)}
    overrides = read_json(args.overrides)
    policy_raw = read_json(args.policy)
    policy_raw["forbidden_terms"] = tuple(policy_raw.get("forbidden_terms", []))
    policy = CaptionPolicy(**policy_raw)
    rows = []
    for record in sorted((row for row in records if row.selection_rank and row.selection_rank <= 10),
                         key=lambda row: row.selection_rank or 999):
        filename = Path(record.source_path).name
        caption = overrides.get(filename, {}).get("caption", "")
        provenance = "derived_override"
        if not caption and filename in historical_map:
            caption_name = Path(historical_map[filename]).with_suffix(".txt")
            caption = (args.historical_caption_root / caption_name).read_text(encoding="utf-8").lstrip("\ufeff").strip()
            provenance = "historical_copy"
        if not caption:
            raise ValueError(f"no caption draft for selected image: {filename}")
        errors = validate_caption(caption, policy)
        rows.append({"rank": record.selection_rank, "filename": filename, "sha256": record.sha256,
                     "caption": caption, "provenance": provenance, "validation_errors": errors})
    write_json(args.output, {"schema": "onyx.lora_lab.caption_proposal", "schema_version": "1.0",
                             "status": "proposed_requires_human_approval", "captions": rows})


def command_plan(args: argparse.Namespace) -> None:
    training_spec = load_training_spec(args.training_spec)
    manifest = read_json(args.dataset_manifest)
    datasets = [DatasetSpec(key, value["size"], str(args.dataset_manifest)) for key, value in manifest["datasets"].items()]
    training_plan = plan_training(training_spec, datasets, args.mode)
    write_json(args.output / f"training_plan.{args.mode}.json", training_plan)
    configs = args.output / "ai_toolkit_configs"
    for run in training_plan["runs"]:
        dataset_folder = str(args.runtime_dataset_root / run["dataset_id"])
        rendered = render_ai_toolkit_config(training_spec, run, dataset_folder)
        target = configs / f"{run['run_id']}.yaml"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(config_as_yaml(rendered), encoding="utf-8")
    benchmark_spec = load_benchmark_spec(args.benchmark_spec)
    historical = read_json(args.historical_control) if args.historical_control else None
    for stage in benchmark_spec.stages:
        plan = plan_benchmark(benchmark_spec, stage.stage_id, historical_control=historical)
        write_json(args.output / f"benchmark_plan.{stage.stage_id}.json", plan)
    write_json(args.output / "dry_run_summary.json", {
        "training_run_count": len(training_plan["runs"]),
        "training_optimizer_steps": sum(run["optimizer_steps"] for run in training_plan["runs"]),
        "benchmark_tasks": {stage.stage_id: len(plan_benchmark(benchmark_spec, stage.stage_id)["tasks"]) for stage in benchmark_spec.stages},
        "materialization_allowed": manifest.get("status") == "approved",
        "blocker": "" if manifest.get("status") == "approved" else "dataset_manifest status requires explicit human approval",
    })


def command_approve(args: argparse.Namespace) -> None:
    manifest = build_approved_manifest(
        args.selection, args.captions, args.membership,
        args.historical_manifest, args.historical_caption_root,
    )
    write_json(args.output, manifest)


def command_materialize(args: argparse.Namespace) -> None:
    materialize_approved(read_json(args.manifest), args.target)


def command_verify(args: argparse.Namespace) -> None:
    print(json.dumps(verify_materialized(args.root), indent=2, ensure_ascii=False))


def command_smoke_config(args: argparse.Namespace) -> None:
    config = render_smoke_config(read_json(args.production_config), args.dataset, args.output_root,
                                 steps=args.steps)
    write_json(args.output, config)


def command_night_plan(args: argparse.Namespace) -> None:
    plan = build_night_plan(read_json(args.training_plan), args.configs_root, args.dataset_root,
                            args.runtime_root, args.ai_toolkit_root, args.python,
                            args.base_model, args.checkpoint_size_bytes, args.output_root)
    write_json(args.output, plan)


def command_benchmark_inventory(args: argparse.Namespace) -> None:
    write_json(args.output, build_checkpoint_inventory(read_json(args.night_plan)))


def command_benchmark_stage(args: argparse.Namespace) -> None:
    write_json(args.output, stage_checkpoints(read_json(args.inventory), args.staging_root,
                                               comfy_lora_prefix=args.comfy_lora_prefix))


def command_benchmark_run(args: argparse.Namespace) -> None:
    from engine.runtime.comfyui_client import ComfyUIClient
    plan = read_json(args.plan)
    staging = read_json(args.staging_manifest)
    checkpoints = {(row["dataset"], int(row["step"])): row for row in staging["checkpoints"]}
    client = ComfyUIClient(args.endpoint, poll_interval_seconds=args.poll_interval)
    result = execute_plan(plan, read_json(args.workflow), checkpoints, client, args.output_root, limit=args.limit)
    write_json(args.output, result)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ONYX LoRA Lab CPU/dry-run CLI")
    commands = parser.add_subparsers(dest="command", required=True)
    analyze = commands.add_parser("analyze")
    analyze.add_argument("--source", required=True, type=Path)
    analyze.add_argument("--historical-manifest", required=True, type=Path)
    analyze.add_argument("--references", required=True, type=Path)
    analyze.add_argument("--output", required=True, type=Path)
    analyze.add_argument("--capture-group", default="")
    analyze.set_defaults(func=command_analyze)
    select = commands.add_parser("select")
    select.add_argument("--analysis", required=True, type=Path, nargs="+")
    select.add_argument("--output", required=True, type=Path)
    select.add_argument("--metadata-overrides", type=Path)
    select.add_argument("--comparison-old", nargs=3)
    select.set_defaults(func=command_select)
    captions = commands.add_parser("captions")
    captions.add_argument("--selection", required=True, type=Path)
    captions.add_argument("--historical-manifest", required=True, type=Path)
    captions.add_argument("--historical-caption-root", required=True, type=Path)
    captions.add_argument("--overrides", required=True, type=Path)
    captions.add_argument("--policy", required=True, type=Path)
    captions.add_argument("--output", required=True, type=Path)
    captions.set_defaults(func=command_captions)
    plan = commands.add_parser("plan")
    plan.add_argument("--training-spec", required=True, type=Path)
    plan.add_argument("--benchmark-spec", required=True, type=Path)
    plan.add_argument("--dataset-manifest", required=True, type=Path)
    plan.add_argument("--historical-control", type=Path)
    plan.add_argument("--runtime-dataset-root", required=True, type=Path)
    plan.add_argument("--mode", choices=("fixed_steps", "fixed_exposure"), default="fixed_steps")
    plan.add_argument("--output", required=True, type=Path)
    plan.set_defaults(func=command_plan)
    approve = commands.add_parser("approve")
    approve.add_argument("--selection", required=True, type=Path)
    approve.add_argument("--captions", required=True, type=Path)
    approve.add_argument("--membership", required=True, type=Path)
    approve.add_argument("--historical-manifest", required=True, type=Path)
    approve.add_argument("--historical-caption-root", required=True, type=Path)
    approve.add_argument("--output", required=True, type=Path)
    approve.set_defaults(func=command_approve)
    materialize = commands.add_parser("materialize")
    materialize.add_argument("--manifest", required=True, type=Path)
    materialize.add_argument("--target", required=True, type=Path)
    materialize.set_defaults(func=command_materialize)
    verify = commands.add_parser("verify")
    verify.add_argument("--root", required=True, type=Path)
    verify.set_defaults(func=command_verify)
    smoke = commands.add_parser("smoke-config")
    smoke.add_argument("--production-config", required=True, type=Path)
    smoke.add_argument("--dataset", required=True, type=Path)
    smoke.add_argument("--output-root", required=True, type=Path)
    smoke.add_argument("--steps", type=int, default=10)
    smoke.add_argument("--output", required=True, type=Path)
    smoke.set_defaults(func=command_smoke_config)
    night = commands.add_parser("night-plan")
    night.add_argument("--training-plan", required=True, type=Path)
    night.add_argument("--configs-root", required=True, type=Path)
    night.add_argument("--dataset-root", required=True, type=Path)
    night.add_argument("--runtime-root", required=True, type=Path)
    night.add_argument("--ai-toolkit-root", required=True, type=Path)
    night.add_argument("--python", required=True, type=Path)
    night.add_argument("--base-model", required=True, type=Path)
    night.add_argument("--checkpoint-size-bytes", required=True, type=int)
    night.add_argument("--output-root", required=True, type=Path)
    night.add_argument("--output", required=True, type=Path)
    night.set_defaults(func=command_night_plan)
    inventory = commands.add_parser("benchmark-inventory")
    inventory.add_argument("--night-plan", required=True, type=Path)
    inventory.add_argument("--output", required=True, type=Path)
    inventory.set_defaults(func=command_benchmark_inventory)
    stage = commands.add_parser("benchmark-stage")
    stage.add_argument("--inventory", required=True, type=Path)
    stage.add_argument("--staging-root", required=True, type=Path)
    stage.add_argument("--comfy-lora-prefix", default="")
    stage.add_argument("--output", required=True, type=Path)
    stage.set_defaults(func=command_benchmark_stage)
    run = commands.add_parser("benchmark-run")
    run.add_argument("--plan", required=True, type=Path)
    run.add_argument("--workflow", required=True, type=Path)
    run.add_argument("--staging-manifest", required=True, type=Path)
    run.add_argument("--endpoint", default="http://127.0.0.1:8188")
    run.add_argument("--poll-interval", type=float, default=1)
    run.add_argument("--output-root", required=True, type=Path)
    run.add_argument("--output", required=True, type=Path)
    run.add_argument("--limit", type=int)
    run.set_defaults(func=command_benchmark_run)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
