from __future__ import annotations

import json
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "engine"))

from lora_lab.benchmark import plan_benchmark
from lora_lab.captions import CaptionPolicy, validate_caption
from lora_lab.io import read_json, read_jsonl, write_json, write_jsonl
from lora_lab.metrics import aggregate_metrics, choose_best_checkpoint
from lora_lab.materialize import materialize_approved, verify_materialized
from lora_lab.models import DatasetSpec, SourceRecord, SpecError, TrainingSpec
from lora_lab.night_run import missing_expected_outputs
from lora_lab.benchmark_executor import checkpoint_mapping, output_path, substitute_workflow, validate_stage1_plan
from lora_lab.preflight import build_night_plan, render_smoke_config
from lora_lab.reporting import serialize_results
from lora_lab.selector import select_nested
from lora_lab.specs import load_benchmark_spec, load_training_spec
from lora_lab.training import plan_training
from lora_lab.trainers.ai_toolkit import render_ai_toolkit_config
from lora_lab.telemetry import checkpoint_telemetry


def record(index: int, pose: str, *, historical: bool = True) -> SourceRecord:
    return SourceRecord(
        source_id=f"source_{index:02d}", source_path=f"C:/source/{index:02d}.jpg", sha256=f"{index:064x}",
        width=1000, height=1200, face_detected=True, face_count=1, face_area_ratio=0.08,
        yaw=0.0, pitch=0.0, roll=0.0, pose_bucket=pose, sharpness=200 + index,
        exposure_mean=128, exposure_low_fraction=0.01, exposure_high_fraction=0.01,
        identity_similarity=0.70 + index / 1000, historical_full_21=historical,
        perceptual_hash=f"{index * 7919 & ((1 << 64) - 1):016x}",
    )


class SelectionTests(unittest.TestCase):
    def test_nested_selection_is_deterministic_with_frozen_control(self) -> None:
        poses = ["frontal", "three_quarter_left", "three_quarter_right", "profile_left", "profile_right"]
        rows = [record(index, poses[index % len(poses)]) for index in range(21)]
        rows.extend(record(index + 30, "frontal", historical=False) for index in range(4))
        first, memberships = select_nested(rows)
        second, repeated = select_nested(list(reversed(rows)))
        self.assertEqual(memberships, repeated)
        self.assertEqual(3, len(memberships["mini_3"]))
        self.assertEqual(5, len(memberships["mini_5"]))
        self.assertEqual(10, len(memberships["mini_10"]))
        self.assertEqual(21, len(memberships["full_21"]))
        self.assertLess(set(memberships["mini_3"]), set(memberships["mini_5"]))
        self.assertLess(set(memberships["mini_5"]), set(memberships["mini_10"]))
        self.assertEqual({row.sha256 for row in rows if row.historical_full_21}, set(memberships["full_21"]))

    def test_selection_is_deterministic_for_equal_input_content(self) -> None:
        rows = [record(index, "frontal") for index in range(21)]
        _, forward = select_nested(rows)
        _, shuffled = select_nested(rows[::2] + rows[1::2])
        self.assertEqual(forward, shuffled)

    def test_visual_near_duplicate_is_penalized(self) -> None:
        rows = [record(index, "frontal") for index in range(21)]
        rows[20] = replace(rows[20], perceptual_hash="0000000000000000", identity_similarity=0.99)
        rows[19] = replace(rows[19], perceptual_hash="0000000000000001", identity_similarity=0.98)
        rows[18] = replace(rows[18], perceptual_hash="ffffffffffffffff", identity_similarity=0.90)
        selected, _ = select_nested(rows)
        ranked = sorted((row for row in selected if row.selection_rank), key=lambda row: row.selection_rank)
        self.assertEqual(rows[20].sha256, ranked[0].sha256)
        self.assertEqual(rows[18].sha256, ranked[1].sha256)
        self.assertNotEqual(rows[19].sha256, ranked[1].sha256)

    def test_hard_filtered_image_cannot_enter_mini(self) -> None:
        rows = [record(index, "frontal") for index in range(21)]
        rows[20] = replace(rows[20], quality_flags=["small_face"], identity_similarity=1.0,
                           sharpness=9999, face_area_ratio=0.5)
        _, memberships = select_nested(rows)
        self.assertNotIn(rows[20].sha256, memberships["mini_10"])

    def test_mini3_has_at_most_two_images_per_capture_group(self) -> None:
        rows = [record(index, "frontal") for index in range(21)]
        for index in range(3):
            rows[index] = replace(rows[index], capture_group="fresh_session", identity_similarity=1.0,
                                  sharpness=900 + index, perceptual_hash=f"{index * ((1<<63)-1):016x}")
        selected, memberships = select_nested(rows)
        lookup = {row.sha256: row for row in selected}
        groups = [lookup[value].capture_group for value in memberships["mini_3"]]
        self.assertLessEqual(groups.count("fresh_session"), 2)

    def test_new_pool_image_can_enter_mini_without_changing_full21(self) -> None:
        rows = [record(index, "frontal") for index in range(21)]
        fresh = replace(record(30, "three_quarter_left", historical=False),
                        identity_similarity=1.0, sharpness=1000, capture_group="fresh")
        _, memberships = select_nested(rows + [fresh])
        self.assertIn(fresh.sha256, memberships["mini_10"])
        self.assertNotIn(fresh.sha256, memberships["full_21"])
        self.assertEqual(21, len(memberships["full_21"]))

    def test_full_21_is_not_changed_by_mini_quality_filters(self) -> None:
        poses = ["frontal", "three_quarter_left", "three_quarter_right"]
        rows = [record(index, poses[index % len(poses)]) for index in range(21)]
        rows[0].quality_flags.append("small_face")
        _, memberships = select_nested(rows)
        self.assertEqual(21, len(memberships["full_21"]))
        self.assertEqual({row.sha256 for row in rows}, set(memberships["full_21"]))
        self.assertNotIn(rows[0].sha256, memberships["mini_10"])


class SpecAndPlannerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.spec = load_training_spec(ROOT / "09 Experiments" / "alexander_lora_dataset_size_v1" / "training_spec.json")

    def test_training_spec_validation(self) -> None:
        with self.assertRaises(SpecError):
            replace(self.spec, rank=0)

    def test_fixed_steps_and_fixed_exposure(self) -> None:
        datasets = [DatasetSpec("mini_3", 3, "manifest.json"), DatasetSpec("full_21", 21, "manifest.json")]
        fixed = plan_training(self.spec, datasets, "fixed_steps")
        exposure = plan_training(self.spec, datasets, "fixed_exposure")
        self.assertEqual([1250, 1250], [row["optimizer_steps"] for row in fixed["runs"]])
        self.assertEqual([180, 1260], [row["optimizer_steps"] for row in exposure["runs"]])
        self.assertEqual([250, 500, 750, 1000, 1250], fixed["runs"][0]["checkpoint_steps"])

    def test_ai_toolkit_renderer_matches_controlled_parameters(self) -> None:
        run = plan_training(self.spec, [DatasetSpec("mini_3", 3, "m.json")], "fixed_steps")["runs"][0]
        config = render_ai_toolkit_config(self.spec, run, "D:/runtime/mini_3")
        process = config["config"]["process"][0]
        self.assertEqual(1250, process["train"]["steps"])
        self.assertEqual(16, process["network"]["linear"])
        self.assertTrue(process["train"]["disable_sampling"])
        self.assertEqual("D:/runtime/mini_3", process["datasets"][0]["folder_path"])

    def test_smoke_config_is_isolated_and_bounded(self) -> None:
        run = plan_training(self.spec, [DatasetSpec("mini_3", 3, "m.json")], "fixed_steps")["runs"][0]
        production = render_ai_toolkit_config(self.spec, run, "D:/runtime/mini_3")
        smoke = render_smoke_config(production, Path("D:/smoke/dataset"), Path("D:/smoke/output"), steps=10)
        process = smoke["config"]["process"][0]
        self.assertEqual(10, process["train"]["steps"])
        self.assertEqual(10, process["save"]["save_every"])
        self.assertEqual(Path("D:/smoke/output"), Path(process["training_folder"]))
        self.assertEqual(1250, production["config"]["process"][0]["train"]["steps"])

    def test_night_plan_requires_clear_gpu(self) -> None:
        training = plan_training(self.spec, [DatasetSpec("mini_3", 3, "m.json")], "fixed_steps")
        plan = build_night_plan(
            training, Path("configs"), Path("datasets"), Path("runtime"), Path("toolkit"),
            Path("python.exe"), Path("model"), 100, Path("output"),
        )
        self.assertEqual(20_000, plan["required_free_vram_mib"])


class BenchmarkTests(unittest.TestCase):
    def test_staged_counts_and_determinism(self) -> None:
        spec = load_benchmark_spec(ROOT / "09 Experiments" / "alexander_lora_dataset_size_v1" / "benchmark_spec.json")
        stage1 = plan_benchmark(spec, "stage_1_screening")
        stage2 = plan_benchmark(spec, "stage_2_full")
        self.assertEqual(80, stage1["task_count"])
        self.assertEqual(96, stage2["task_count"])
        self.assertEqual(stage1, plan_benchmark(spec, "stage_1_screening"))
        self.assertEqual("BEST_CHECKPOINT_PENDING_STAGE_1", stage2["tasks"][0]["checkpoint"])

    def test_stage1_executor_contract_and_paths(self) -> None:
        spec = load_benchmark_spec(ROOT / "09 Experiments" / "alexander_lora_dataset_size_v1" / "benchmark_spec.json")
        plan = plan_benchmark(spec, "stage_1_screening")
        validate_stage1_plan(plan)
        self.assertEqual(80, len(plan["tasks"]))
        task = plan["tasks"][0]
        self.assertEqual("images/mini_3/250/closeup_neutral__seed_202608290101.png", output_path(Path("."), task).as_posix())
        template = {"4": {"inputs": {}}, "5": {"inputs": {}}, "7": {"inputs": {}}, "8": {"inputs": {}}, "10": {"inputs": {}}}
        rendered = substitute_workflow(template, task, {"staged_filename": "mini_3__0250.safetensors", "comfy_lora_name": "onyx_benchmark\\alexander_dataset_size_v1\\mini_3__0250.safetensors"})
        self.assertEqual("onyx_benchmark\\alexander_dataset_size_v1\\mini_3__0250.safetensors", rendered["4"]["inputs"]["lora_name"])
        self.assertEqual(30, rendered["8"]["inputs"]["steps"])
        self.assertEqual(4.0, rendered["8"]["inputs"]["cfg"])


class CaptionAndMetricsTests(unittest.TestCase):
    def test_caption_policy(self) -> None:
        policy = CaptionPolicy("alexonyx", "photo of alexonyx man", forbidden_terms=("handsome",))
        self.assertEqual([], validate_caption("photo of alexonyx man, neutral close-up portrait", policy))
        self.assertIn("trigger_word_must_appear_exactly_once", validate_caption("photo of a man", policy))

    def test_metrics_and_time_to_best(self) -> None:
        aggregate = aggregate_metrics([
            {"identity_similarity": 0.8, "quality_pass": True},
            {"identity_similarity": 0.6, "quality_pass": True},
            {"identity_similarity": None, "quality_pass": False},
        ], 0.7)
        self.assertAlmostEqual(0.7, aggregate["identity_mean"])
        self.assertAlmostEqual(1 / 3, aggregate["yield_rate"])
        best = choose_best_checkpoint([
            {"checkpoint": "250", "optimizer_step": 250, "effective_epochs": 50, "training_elapsed_seconds": 1000, "yield_rate": .7, "identity_p10": .65, "identity_mean": .72},
            {"checkpoint": "500", "optimizer_step": 500, "effective_epochs": 100, "training_elapsed_seconds": 2000, "yield_rate": .8, "identity_p10": .67, "identity_mean": .74},
        ])
        self.assertEqual("500", best["best_checkpoint"])
        self.assertEqual(2000, best["time_to_best_checkpoint_seconds"])


class SerializationTests(unittest.TestCase):
    def _checkpoint_run(self, output: Path) -> dict:
        return {
            "run_id": "test_run",
            "output_directory": str(output),
            "optimizer_steps": 1000,
            "checkpoint_steps": [250, 500, 750, 1000],
        }

    def _write_checkpoint(self, output: Path, name: str) -> None:
        output.mkdir(parents=True, exist_ok=True)
        (output / name).write_bytes(b"checkpoint")

    def test_checkpoint_validation_accepts_final_only(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder)
            for step in (250, 500, 750):
                self._write_checkpoint(output, f"test_run_{step:09d}.safetensors")
            self._write_checkpoint(output, "test_run.safetensors")
            self.assertEqual([], missing_expected_outputs(self._checkpoint_run(output)))

    def test_checkpoint_validation_accepts_numbered_final_and_final(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder)
            for step in (250, 500, 750, 1000):
                self._write_checkpoint(output, f"test_run_{step:09d}.safetensors")
            self._write_checkpoint(output, "test_run.safetensors")
            self.assertEqual([], missing_expected_outputs(self._checkpoint_run(output)))

    def test_checkpoint_validation_rejects_missing_final_alternatives(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder)
            for step in (250, 500, 750):
                self._write_checkpoint(output, f"test_run_{step:09d}.safetensors")
            missing = missing_expected_outputs(self._checkpoint_run(output))
            self.assertEqual(1, len(missing))
            self.assertIn("one_of:", missing[0])

    def test_checkpoint_validation_rejects_missing_intermediate(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder)
            for step in (250, 500):
                self._write_checkpoint(output, f"test_run_{step:09d}.safetensors")
            self._write_checkpoint(output, "test_run.safetensors")
            missing = missing_expected_outputs(self._checkpoint_run(output))
            self.assertEqual([str(output / "test_run_000000750.safetensors")], missing)

    def test_manifest_and_result_serialization(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            rows = [record(1, "frontal")]
            write_jsonl(root / "manifest.jsonl", rows)
            self.assertEqual(rows[0].sha256, read_jsonl(root / "manifest.jsonl")[0]["sha256"])
            serialize_results(root, [{"model": "mini_3", "photos": 3}])
            self.assertEqual("mini_3", read_json(root / "experiment_results.json")["results"][0]["model"])
            self.assertTrue((root / "experiment_results.csv").exists())

    def test_checkpoint_elapsed_telemetry(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            checkpoint = Path(folder) / "model_250.safetensors"
            checkpoint.write_bytes(b"test")
            saved = checkpoint.stat().st_mtime
            row = checkpoint_telemetry(checkpoint, 250, saved - 125, 5)
            self.assertAlmostEqual(125, row["training_elapsed_seconds"], places=2)
            self.assertEqual(50, row["effective_epochs"])

    def test_materialization_copies_and_verifies_without_overwrite(self) -> None:
        import hashlib
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            sources = []
            for index in range(21):
                source = root / f"source_{index}.jpg"
                source.write_bytes(f"image-{index}".encode())
                sources.append({"filename": source.name, "source_path": str(source),
                                "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                                "caption": "photo of alexonyx man", "caption_sha256": "unused"})
            manifest = {"status": "approved", "datasets": {
                "mini_3": {"size": 3, "items": sources[:3]},
                "mini_5": {"size": 5, "items": sources[:5]},
                "mini_10": {"size": 10, "items": sources[:10]},
                "full_21": {"size": 21, "items": sources},
            }}
            target = root / "runtime"
            materialize_approved(manifest, target)
            verification = verify_materialized(target)
            self.assertTrue(verification["valid"])
            self.assertEqual(3, verification["mini_3"]["images"])
            with self.assertRaises(FileExistsError):
                materialize_approved(manifest, target)


if __name__ == "__main__":
    unittest.main()
