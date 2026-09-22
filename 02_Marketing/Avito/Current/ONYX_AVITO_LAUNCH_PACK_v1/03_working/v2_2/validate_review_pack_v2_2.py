from pathlib import Path
from PIL import Image
import hashlib
import json


ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT.parents[3]
V21_MASTER = ROOT / "04_master" / "v2_1"
V21_EXPORT = ROOT / "05_export" / "v2_1"
MASTER = ROOT / "04_master" / "v2_2"
EXPORT = ROOT / "05_export" / "v2_2"
QA = ROOT / "06_qa" / "v2_2"
PROVENANCE = ROOT / "01_asset_candidates" / "PROVENANCE.json"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


checks = []

masters = sorted(MASTER.glob("AVITO_V2_2_*.png"))
exports = sorted(EXPORT.glob("AVITO_V2_2_*.jpg"))
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
checks.append("ten v2.2 masters and exports")

for slide in (1, 2, 6, 7, 9, 10):
    assert sha256(MASTER / f"AVITO_V2_2_{slide:02d}.png") == sha256(V21_MASTER / f"AVITO_V2_1_{slide:02d}.png")
    assert sha256(EXPORT / f"AVITO_V2_2_{slide:02d}.jpg") == sha256(V21_EXPORT / f"AVITO_V2_1_{slide:02d}.jpg")
for slide in (3, 4, 5, 8):
    assert sha256(MASTER / f"AVITO_V2_2_{slide:02d}.png") != sha256(V21_MASTER / f"AVITO_V2_1_{slide:02d}.png")
checks.append("only slides 03, 04, 05 and 08 changed")

v21_inspection = json.loads((ROOT / "06_qa" / "v2_1" / "render_inspection_v2_1.json").read_text(encoding="utf-8"))
for item in v21_inspection["files"]:
    path = ROOT / item["path"]
    assert path.exists() and sha256(path) == item["sha256"], f"v2.1 output changed: {item['path']}"
checks.append("v2.1 rendered outputs preserved")

provenance = json.loads(PROVENANCE.read_text(encoding="utf-8"))
assert [asset["id"] for asset in provenance["assets"]] == [f"A{index:02d}" for index in range(1, 11)]
for asset in provenance["assets"]:
    assert asset["synthetic_persona"] is True
    assert asset["marketing_approved"] is True
    assert asset["avito_publication_approved"] is True
    assert asset["publish_approved"] is True
    assert asset["approval_scope"] == "AVITO_LAUNCH_V1"
    assert asset["source_mutated"] is False
assert provenance["before_after_references"][0]["id"] == "B01"
assert provenance["before_after_references"][0]["approval_scope"] == "AVITO_LAUNCH_V1_BEFORE_AFTER"
checks.append("approved synthetic P02 rights scope only")

listing = (ROOT / "00_docs" / "AVITO_LISTING_COPY_v2.md").read_text(encoding="utf-8")
for required in (
    "Business",
    "Portrait — 1 фото / 1 000 ₽",
    "Signature — 10 фото / 3 000 ₽",
    "Premium — 20 фото / 5 000 ₽",
    "доплатить только 2 000 ₽",
    "Signature → Premium",
    "7 календарных дней",
    "+1 final image — 500 ₽",
    "Additional Concept — 1 000 ₽",
    "Priority ≤24h — +50%",
    "Repair — от 500 ₽",
    "Напишите «Хочу ONYX»",
    "не публикуются без отдельного разрешения",
):
    assert required in listing, required
for forbidden in ("trial", "demo", "пробник", "тестовое фото"):
    assert forbidden not in listing.lower()
checks.append("listing copy commercial, upgrade, CTA and privacy requirements")

catalog = (REPO / "13 Production" / "Product_Standards" / "ONYX_COLLECTION_CATALOG.md").read_text(encoding="utf-8")
assert "entries below do not imply a launched public offer" in catalog
blueprint = (ROOT / "03_working" / "v2_2" / "CAROUSEL_BLUEPRINT_v2_2.md").read_text(encoding="utf-8")
assert "Business is the only explicitly evidenced launch-ready Collection" in blueprint
checks.append("collection availability follows source of truth")

inspection = json.loads((QA / "render_inspection_v2_2.json").read_text(encoding="utf-8"))
assert inspection["status"] == "PASS" and len(inspection["files"]) == 22
assert (ROOT / "02_contact_sheets" / "AVITO_CAROUSEL_FINAL_REVIEW_v2_2.jpg").exists()
assert (QA / "AVITO_MOBILE_QA_v2_2.jpg").exists()
checks.append("final contact sheet and exact 390 px mobile preview")

result = {
    "status": "PASS",
    "release_status": "READY_FOR_AVITO_PUBLISH_REVIEW",
    "revision": "v2.2",
    "launch_ready_collections": ["Business"],
    "checks": checks,
    "v2_1_preserved": True,
    "publication_performed": False,
}
(QA / "validation_result_v2_2.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(result, ensure_ascii=False))
