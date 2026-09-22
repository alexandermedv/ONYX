from pathlib import Path
from PIL import Image
import hashlib
import json


ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT.parents[3]
V23_MASTER = ROOT / "04_master" / "v2_3"
V23_EXPORT = ROOT / "05_export" / "v2_3"
MASTER = ROOT / "04_master" / "v2_4"
EXPORT = ROOT / "05_export" / "v2_4"
QA = ROOT / "06_qa" / "v2_4"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


checks = []
masters = sorted(MASTER.glob("AVITO_V2_4_*.png"))
exports = sorted(EXPORT.glob("AVITO_V2_4_*.jpg"))
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
checks.append("ten v2.4 masters and exports")

for slide in (1, 2, 4, 5, 6, 7, 8, 9, 10):
    assert sha256(MASTER / f"AVITO_V2_4_{slide:02d}.png") == sha256(V23_MASTER / f"AVITO_V2_3_{slide:02d}.png")
    assert sha256(EXPORT / f"AVITO_V2_4_{slide:02d}.jpg") == sha256(V23_EXPORT / f"AVITO_V2_3_{slide:02d}.jpg")
assert sha256(MASTER / "AVITO_V2_4_03.png") != sha256(V23_MASTER / "AVITO_V2_3_03.png")
checks.append("only slide 03 changed from v2.3")

v23_inspection = json.loads((ROOT / "06_qa" / "v2_3" / "render_inspection_v2_3.json").read_text(encoding="utf-8"))
for item in v23_inspection["files"]:
    path = ROOT / item["path"]
    assert path.exists() and sha256(path) == item["sha256"], f"v2.3 output changed: {item['path']}"
checks.append("v2.3 outputs preserved")

inventory_path = REPO / "13 Production" / "Portfolio" / "P02" / "LIFESTYLE_V1_SOURCE_INVENTORY.json"
inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
assert inventory["synthetic_persona"] is True
assert inventory["synthetic_provenance_status"] == "CONFIRMED"
assert inventory["marketing_approved"] is True
assert inventory["avito_publication_approved"] is True
assert inventory["publish_approved"] is True
assert inventory["approval_scope"] == "AVITO_LAUNCH_V1"
assert inventory["approved_exact_asset_ids"] == [f"LIFE_{i:02d}" for i in range(1, 11)]
for item in inventory["photos"]:
    path = REPO / item["source"]
    assert path.exists() and sha256(path) == item["sha256"], f"source hash mismatch: {item['source']}"
checks.append("ten exact Lifestyle hashes and approval scope verified")

provenance_path = ROOT / "01_asset_candidates" / "PROVENANCE.json"
provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
assert [item["id"] for item in provenance["lifestyle_assets"]] == [f"LIFE_{i:02d}" for i in range(1, 11)]
for item in provenance["lifestyle_assets"]:
    assert item["synthetic_persona"] is True
    assert item["synthetic_provenance_status"] == "CONFIRMED"
    assert item["marketing_approved"] is True
    assert item["avito_publication_approved"] is True
    assert item["publish_approved"] is True
    assert item["approval_scope"] == "AVITO_LAUNCH_V1"
    assert item["source_mutated"] is False
    assert sha256(REPO / item["source"]) == item["source_sha256"]
assert provenance["revision_v2_4"]["business_collection_asset_id"] == "A03"
assert provenance["revision_v2_4"]["lifestyle_collection_asset_id"] == "LIFE_06"
checks.append("file-level provenance and selected A03/LIFE_06 pair verified")

listing = (ROOT / "00_docs" / "AVITO_LISTING_COPY_v2.md").read_text(encoding="utf-8")
for required in (
    "Business — деловые портреты для резюме, профессионального профиля, сайта и личного бренда.",
    "Lifestyle — естественные современные фотографии для соцсетей, личного профиля и повседневного образа.",
    "Другие направления — по индивидуальному согласованию до оплаты.",
    "Portrait — 1 фото / 1 000 ₽",
    "Signature — 10 фото / 3 000 ₽",
    "Premium — 20 фото / 5 000 ₽",
):
    assert required in listing, required
checks.append("listing collections and unchanged product prices verified")

build_script = (ROOT / "03_working" / "v2_4" / "build_final_pack_v2_4.py").read_text(encoding="utf-8")
assert "P02_LIFE_06_weekend_street.png" in build_script
assert "ONYX_P02_BUSINESS_03_WAIST.jpg" in build_script
assert "Orders" not in build_script
checks.append("card 03 uses only approved synthetic Business and Lifestyle sources")

inspection = json.loads((QA / "render_inspection_v2_4.json").read_text(encoding="utf-8"))
assert inspection["status"] == "PASS" and len(inspection["files"]) == 22
assert (ROOT / "02_contact_sheets" / "AVITO_CAROUSEL_FINAL_v2_4.jpg").exists()
assert (QA / "AVITO_MOBILE_QA_v2_4.jpg").exists()
checks.append("final carousel and exact 390 px mobile preview")

result = {
    "status": "PASS",
    "release_status": "APPROVED_FOR_AVITO_PUBLISH",
    "revision": "v2.4",
    "selected_business_asset": "A03 / ONYX_P02_BUSINESS_03_WAIST.jpg",
    "selected_lifestyle_asset": "LIFE_06 / P02_LIFE_06_weekend_street.png",
    "checks": checks,
    "canonical_sources_mutated": False,
    "publication_performed": False,
}
(QA / "validation_result_v2_4.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False))
