from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from engine.production_pilot.runner import critically_low, dry_run, render_workflow, resolve_scene_variants, should_free, smoke_payload, validate_spec


ROOT = Path(__file__).resolve().parents[2]


class ProductionPilotTests(unittest.TestCase):
    def setUp(self) -> None:
        self.spec = json.loads((ROOT / "09 Experiments/production_pilot_v0_1/pilot_spec.json").read_text(encoding="utf-8"))

    def test_fixed_scene_pack_and_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            validate_spec(self.spec, ROOT)
        plan = dry_run(self.spec, ROOT, "test_run")
        self.assertEqual(12, plan["scene_count"])
        immutable = "photo of alexonyx man, bald man with a shaved head, clean-shaven face, no beard, no moustache, no stubble, blue eyes, same person, consistent facial identity, realistic skin texture."
        self.assertTrue(all(item["prompt"].startswith(immutable) for item in plan["scenes"]))
        self.assertTrue(all(item["lora_name"].endswith("mini_5__1250.safetensors") for item in plan["scenes"]))

    def test_render_does_not_mutate_template(self) -> None:
        template = json.loads((ROOT / self.spec["workflow"]).read_text(encoding="utf-8"))
        workflow, prompt = render_workflow(template, self.spec, self.spec["scenes"][0], "run_x")
        self.assertTrue(prompt.startswith("photo of alexonyx man, bald man with a shaved head,"))
        self.assertEqual("alexonyx_v1.safetensors", template["56:59"]["inputs"]["lora_name"])
        self.assertIn("mini_5__1250", workflow["56:59"]["inputs"]["lora_name"])
        self.assertEqual(1.0, workflow["56:59"]["inputs"]["strength_model"])
        self.assertEqual(self.spec["scenes"][0]["seed"], workflow["56:58"]["inputs"]["seed"])
        self.assertEqual(20, workflow["56:58"]["inputs"]["steps"])
        self.assertEqual(1.0, workflow["56:58"]["inputs"]["cfg"])
        self.assertEqual((896, 1152), (workflow["56:50"]["inputs"]["width"], workflow["56:50"]["inputs"]["height"]))

    def test_smoke_keeps_canonical_prompt_and_seed(self) -> None:
        payload = smoke_payload(self.spec, ROOT, "smoke")
        template = json.loads((ROOT / self.spec["workflow"]).read_text(encoding="utf-8"))
        self.assertEqual(template["56:51"]["inputs"]["text"], payload["prompt"])
        self.assertEqual(1090798370788838, payload["seed"])
        self.assertEqual("flux1-dev.safetensors", payload["model"])
        self.assertEqual(1.0, payload["lora"]["weight"])

    def test_selected_scene_seed_variants_are_deterministic(self) -> None:
        variants = resolve_scene_variants(self.spec, "1,4,7", 2)
        self.assertEqual([202609020101, 202609020102, 202609020104, 202609020105, 202609020107, 202609020108], [item["seed"] for item in variants])

    def test_memory_guard_is_not_blind_free(self) -> None:
        guard = self.spec["memory_guard"]
        safe = {"ram_free_mib": 8000, "commit_free_mib": 8000, "gpu": {"free_mib": 2543}}
        soft = {"ram_free_mib": 3000, "commit_free_mib": 8000, "gpu": {"free_mib": 2543}}
        critical = {"ram_free_mib": 1000, "commit_free_mib": 8000, "gpu": {"free_mib": 2543}}
        self.assertFalse(should_free(safe, guard)); self.assertTrue(should_free(soft, guard)); self.assertTrue(critically_low(critical, guard))
        self.assertFalse(critically_low(safe, guard))  # loaded FLUX VRAM is not a stop condition
