from pathlib import Path
from PIL import Image
import hashlib
import json


ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT.parents[3]
REFERENCE = REPO / "09 Experiments" / "identity_benchmark_v1" / "P02_F30_Lifestyle" / "01_references" / "P02_REF03.png"
REFERENCE_COPY = ROOT / "01_asset_candidates" / "v2" / "P02_REF03.png"
INVENTORY = REPO / "01_Characters" / "P02" / "02_Sessions" / "Business_v1" / "WIP" / "manifests" / "BUSINESS_V1_SOURCE_INVENTORY.json"
V2_MASTER = ROOT / "04_master" / "v2"
V2_EXPORT = ROOT / "05_export" / "v2"
MASTER = ROOT / "04_master" / "v2_1"
EXPORT = ROOT / "05_export" / "v2_1"
QA = ROOT / "06_qa" / "v2_1"
REF_SHA = "23fb0883218085354fe2de85d92d2641916501ac41e754735892babb10a004c2"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


checks = []

inventory = json.loads(INVENTORY.read_text(encoding="utf-8-sig"))
approval = inventory["before_after_reference_approval"]
record = approval["assets"][0]
assert len(approval["assets"]) == 1
assert approval["unlisted_references_approved"] is False
assert record["approval_scope"] == "AVITO_LAUNCH_V1_BEFORE_AFTER"
assert record["synthetic_persona"] is True
assert record["marketing_approved"] is True
assert record["avito_publication_approved"] is True
assert record["publish_approved"] is True
assert record["source_assets_mutable"] is False
assert record["sha256"] == REF_SHA
checks.append("exact REF03 approval and immutable-source scope")

assert sha256(REFERENCE) == REF_SHA
assert sha256(REFERENCE_COPY) == REF_SHA
checks.append("canonical and working-copy REF03 hashes")

provenance = json.loads((ROOT / "01_asset_candidates" / "PROVENANCE.json").read_text(encoding="utf-8"))
revision = provenance["revision_v2_1"]
assert revision["status"] == "READY_FOR_AVITO_LAUNCH_APPROVAL"
assert revision["before_reference_id"] == "B01"
assert revision["before_reference_changed"] is False
assert revision["cards_02_10_preserved_from_v2"] is True
assert revision["publication_performed"] is False
checks.append("v2.1 provenance and publication hold")

assets = provenance["assets"]
assert [item["id"] for item in assets] == [f"A{index:02d}" for index in range(1, 11)]
for item in assets:
    assert item["synthetic_persona"] is True
    assert item["marketing_approved"] is True
    assert item["avito_publication_approved"] is True
    assert item["publish_approved"] is True
    assert item["approval_scope"] == "AVITO_LAUNCH_V1"
    assert item["source_mutated"] is False
    assert item["source"].startswith("01_Characters/P02/02_Sessions/Business_v1/02_Final/")
    assert sha256(REPO / item["source"]) == item["source_sha256"]
    assert sha256(ROOT / item["candidate_copy"]) == item["candidate_copy_sha256"]
    assert item["source_sha256"] == item["candidate_copy_sha256"]
checks.append("P02 Business A01–A10 rights and byte-identical provenance")

masters = sorted(MASTER.glob("AVITO_V2_1_*.png"))
exports = sorted(EXPORT.glob("AVITO_V2_1_*.jpg"))
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
checks.append("ten v2.1 masters and ten v2.1 exports")

assert sha256(MASTER / "AVITO_V2_1_01.png") != sha256(V2_MASTER / "AVITO_V2_01.png")
assert sha256(EXPORT / "AVITO_V2_1_01.jpg") != sha256(V2_EXPORT / "AVITO_V2_01.jpg")
for slide in range(2, 11):
    assert sha256(MASTER / f"AVITO_V2_1_{slide:02d}.png") == sha256(V2_MASTER / f"AVITO_V2_{slide:02d}.png")
    assert sha256(EXPORT / f"AVITO_V2_1_{slide:02d}.jpg") == sha256(V2_EXPORT / f"AVITO_V2_{slide:02d}.jpg")
checks.append("only HERO changed; cards 02–10 are byte-identical to v2")

v2_inspection = json.loads((ROOT / "06_qa" / "v2" / "render_inspection_v2.json").read_text(encoding="utf-8"))
for item in v2_inspection["files"]:
    path = ROOT / item["path"]
    assert path.exists() and sha256(path) == item["sha256"], f"v2 output changed: {item['path']}"
checks.append("v2 rendered outputs preserved")

inspection = json.loads((QA / "render_inspection_v2_1.json").read_text(encoding="utf-8"))
assert inspection["status"] == "PASS" and len(inspection["files"]) == 22
assert (ROOT / "02_contact_sheets" / "AVITO_CAROUSEL_FINAL_REVIEW_v2_1.jpg").exists()
assert (QA / "AVITO_MOBILE_QA_v2_1.jpg").exists()
checks.append("final contact sheet and 390 px mobile QA preview")

renderer = (ROOT / "03_working" / "v2" / "build_review_pack_v2.py").read_text(encoding="utf-8")
for required in ("1 000 ₽", "3 000 ₽", "5 000 ₽", "+1 фото — 500 ₽", "Срочно — от +50%", "Напишите «Хочу ONYX»"):
    assert required in renderer
checks.append("frozen prices and CTA text")

result = {
    "status": "PASS",
    "release_status": "READY_FOR_AVITO_LAUNCH_APPROVAL",
    "revision": "v2.1",
    "checks": checks,
    "before_reference": "P02_REF03.png",
    "before_reference_changed": False,
    "canonical_sources_unchanged_by_hash": True,
    "publication_performed": False,
}
(QA / "validation_result_v2_1.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(result, ensure_ascii=False))
