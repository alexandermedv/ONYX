from pathlib import Path
from PIL import Image
import hashlib
import json


ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT.parents[3]
INVENTORY = REPO / "01_Characters" / "P02" / "02_Sessions" / "Business_v1" / "WIP" / "manifests" / "BUSINESS_V1_SOURCE_INVENTORY.json"
REFERENCE = REPO / "09 Experiments" / "identity_benchmark_v1" / "P02_F30_Lifestyle" / "01_references" / "P02_REF03.png"
REFERENCE_COPY = ROOT / "01_asset_candidates" / "v2" / "P02_REF03.png"
IDENTITY_MANIFEST = REPO / "09 Experiments" / "identity_benchmark_v1" / "P02_F30_Lifestyle" / "identity_manifest.yaml"
MASTER = ROOT / "04_master" / "v2"
EXPORT = ROOT / "05_export" / "v2"
QA = ROOT / "06_qa" / "v2"
REF_SHA = "23fb0883218085354fe2de85d92d2641916501ac41e754735892babb10a004c2"
A10_SHA = "d918c5e894d5a6f8a0b191e1d78db72f03d3a30e4be98db4797e60c99261f6f5"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


checks = []
inventory = json.loads(INVENTORY.read_text(encoding="utf-8-sig"))
approval = inventory["before_after_reference_approval"]
assert approval["approval_scope"] == "AVITO_LAUNCH_V1_BEFORE_AFTER"
assert approval["unlisted_references_approved"] is False
assert len(approval["assets"]) == 1
record = approval["assets"][0]
for key, value in {
    "synthetic_persona": True,
    "marketing_approved": True,
    "avito_publication_approved": True,
    "publish_approved": True,
    "approval_scope": "AVITO_LAUNCH_V1_BEFORE_AFTER",
    "source_assets_mutable": False,
}.items():
    assert record[key] == value, f"inventory reference field mismatch: {key}"
assert record["sha256"] == REF_SHA and Path(record["source"]).name == "P02_REF03.png"
checks.append("exact REF03 approval scope")

manifest_text = IDENTITY_MANIFEST.read_text(encoding="utf-8")
assert "synthetic_identity: true" in manifest_text
assert "01_references/P02_REF03.png" in manifest_text and REF_SHA in manifest_text
checks.append("synthetic canonical identity provenance")

assert sha256(REFERENCE) == REF_SHA
assert sha256(REFERENCE_COPY) == REF_SHA
provenance = json.loads((ROOT / "01_asset_candidates" / "PROVENANCE.json").read_text(encoding="utf-8"))
refs = provenance["before_after_references"]
assert len(refs) == 1 and refs[0]["source_sha256"] == REF_SHA
assert refs[0]["candidate_copy_sha256"] == REF_SHA
assert refs[0]["after_source_sha256"] == A10_SHA
assert refs[0]["approval_scope"] == "AVITO_LAUNCH_V1_BEFORE_AFTER"
assert "/orders/" not in refs[0]["source"].lower()
checks.append("Before/After source-copy hashes")

masters = sorted(MASTER.glob("AVITO_V2_*.png"))
exports = sorted(EXPORT.glob("AVITO_V2_*.jpg"))
assert len(masters) == 10 and len(exports) == 10
for path in masters:
    with Image.open(path) as image:
        image.verify()
    with Image.open(path) as image:
        assert image.size == (2560, 1920) and image.mode == "RGB"
for path in exports:
    with Image.open(path) as image:
        image.verify()
    with Image.open(path) as image:
        assert image.size == (1280, 960) and image.mode == "RGB"
checks.append("ten v2 masters and ten v2 exports")

inspection = json.loads((QA / "render_inspection_v2.json").read_text(encoding="utf-8"))
assert inspection["status"] == "PASS" and len(inspection["files"]) == 23
checks.append("v2 render inspection")

v1_inspection = json.loads((ROOT / "06_qa" / "render_inspection.json").read_text(encoding="utf-8"))
for item in v1_inspection["files"]:
    path = ROOT / item["path"]
    assert path.exists() and sha256(path) == item["sha256"], f"v1 output changed: {item['path']}"
checks.append("v1 rendered outputs preserved")

renderer_text = (ROOT / "03_working" / "v2" / "build_review_pack_v2.py").read_text(encoding="utf-8")
for required in ("1 000 ₽", "3 000 ₽", "5 000 ₽", "+1 фото — 500 ₽", "Срочно — от +50%"):
    assert required in renderer_text
checks.append("frozen public prices")

result = {
    "status": "PASS",
    "revision": "v2",
    "checks": checks,
    "canonical_reference_unchanged_by_hash": True,
    "v1_outputs_preserved": True,
}
(QA / "validation_result_v2.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(json.dumps(result, ensure_ascii=False))
