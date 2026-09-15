"""Self-contained smoke tests for the blind-review package and local UI."""
from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
from pathlib import Path


APP_DIR = Path(__file__).resolve().parent
ROOT = APP_DIR.parent
spec = importlib.util.spec_from_file_location("blind_review_app", APP_DIR / "app.py")
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def main() -> int:
    config = json.loads((ROOT / "review_config.json").read_text(encoding="utf-8-sig"))
    mapping = json.loads((ROOT / "blind_mapping.json").read_text(encoding="utf-8-sig"))
    assert len(config["review_order"]) == 36
    assert len({item["candidate_id"] for item in config["review_order"]}) == 36
    assert {item["scene"] for item in config["review_order"]} == {"BUS_01", "BUS_06", "BUS_09"}
    assert all(len(mapping["mapping"][scene]) == 12 for scene in ("BUS_01", "BUS_06", "BUS_09"))

    with tempfile.TemporaryDirectory() as directory:
        review_root = Path(directory)
        for name in ("review_config.json", "blind_mapping.json", "blind_review_scores.csv"):
            shutil.copy2(ROOT / name, review_root / name)
        app = module.create_app(review_root)
        client = app.test_client()
        homepage = client.get("/")
        assert homepage.status_code == 200
        assert b"model_name" not in homepage.data
        assert client.get("/blind_mapping.json").status_code == 404
        first = client.get("/api/item/0").get_json()
        assert first["scene"] == "BUS_01" and "source" not in first and "model_name" not in first
        assert client.get("/api/candidate/" + first["candidate_id"]).status_code == 200
        assert client.get("/api/reference/master").status_code == 200
        assert client.post("/api/finish").status_code == 400
        payload = {"candidate_id": first["candidate_id"], "identity_score": 5, "realism_score": 4, "scene_score": 3, "commercial_score": 2, "verdict": "REPAIR", "comment": "persistence smoke test"}
        assert client.post("/api/save", json=payload).get_json()["ok"] is True
        assert client.get("/api/progress").get_json() == {"reviewed": 1, "total": 36}
        reloaded = module.create_app(review_root).test_client().get("/api/item/0").get_json()
        assert reloaded["scores"]["identity_score"] == 5 and reloaded["verdict"] == "REPAIR"
    print("blind_review_tests=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
