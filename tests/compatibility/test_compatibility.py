from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "engine"))

from contracts.compatibility import load_ensemble_job, load_job_engine_job
from contracts.validation import validate_job_spec


FIXTURES = ROOT / "tests" / "fixtures"


class CompatibilityTests(unittest.TestCase):
    def test_current_job_engine_fixture_parses(self) -> None:
        job = load_job_engine_job(FIXTURES / "job_engine_job.json")
        validate_job_spec(job)
        self.assertEqual("fixture_job_engine", job.job_id)
        self.assertEqual("onyx.job_engine.job.v1", job.legacy["source_format"])
        self.assertEqual(2, len(job.scenes))
        self.assertNotIn("X:\\SANITIZED", str(job.to_dict()))

    def test_current_ensemble_fixture_parses(self) -> None:
        job = load_ensemble_job(FIXTURES / "ensemble_job.json")
        validate_job_spec(job)
        self.assertEqual("fixture_ensemble", job.job_id)
        self.assertEqual("onyx.ensemble.job.v0.3", job.legacy["source_format"])
        self.assertNotIn("X:\\SANITIZED", str(job.to_dict().get("workspace_uri")))
        providers = {item.provider.provider_id for item in job.scene_generators}
        self.assertIn("scene.dreamo_t2i", providers)
        self.assertIn("scene.flux_personal_lora", providers)


if __name__ == "__main__":
    unittest.main()
