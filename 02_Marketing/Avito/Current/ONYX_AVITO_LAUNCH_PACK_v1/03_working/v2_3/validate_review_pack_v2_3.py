from pathlib import Path
from PIL import Image
import hashlib
import json


ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT.parents[3]
V22_MASTER = ROOT / "04_master" / "v2_2"
V22_EXPORT = ROOT / "05_export" / "v2_2"
MASTER = ROOT / "04_master" / "v2_3"
EXPORT = ROOT / "05_export" / "v2_3"
QA = ROOT / "06_qa" / "v2_3"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


checks = []
masters = sorted(MASTER.glob("AVITO_V2_3_*.png"))
exports = sorted(EXPORT.glob("AVITO_V2_3_*.jpg"))
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
checks.append("ten v2.3 masters and exports")

for slide in (1, 2, 4, 5, 6, 7, 8, 9, 10):
    assert sha256(MASTER / f"AVITO_V2_3_{slide:02d}.png") == sha256(V22_MASTER / f"AVITO_V2_2_{slide:02d}.png")
    assert sha256(EXPORT / f"AVITO_V2_3_{slide:02d}.jpg") == sha256(V22_EXPORT / f"AVITO_V2_2_{slide:02d}.jpg")
assert sha256(MASTER / "AVITO_V2_3_03.png") != sha256(V22_MASTER / "AVITO_V2_2_03.png")
assert sha256(EXPORT / "AVITO_V2_3_03.jpg") != sha256(V22_EXPORT / "AVITO_V2_2_03.jpg")
checks.append("only slide 03 changed from v2.2")

v22_inspection = json.loads((ROOT / "06_qa" / "v2_2" / "render_inspection_v2_2.json").read_text(encoding="utf-8"))
for item in v22_inspection["files"]:
    path = ROOT / item["path"]
    assert path.exists() and sha256(path) == item["sha256"], f"v2.2 output changed: {item['path']}"
checks.append("v2.2 rendered outputs preserved")

product_system = (REPO / "03_Standards" / "Product" / "ONYX_PRODUCT_SYSTEM.md").read_text(encoding="utf-8")
products_yaml = (REPO / "03_Standards" / "Product" / "products_v1.yaml").read_text(encoding="utf-8")
catalog = (REPO / "03_Standards" / "Portfolio" / "ONYX_COLLECTION_CATALOG.md").read_text(encoding="utf-8")
for content in (product_system, products_yaml, catalog):
    assert content.count("PUBLIC_LAUNCH_AVAILABLE") >= 2
assert "unlisted_collections_publicly_available: false" in products_yaml
assert "multi_collection_default_in_premium: false" in products_yaml
checks.append("Business and Lifestyle only are public launch Collections")

inventory = json.loads((REPO / "01_Characters" / "P02" / "02_Sessions" / "Business_v1" / "WIP" / "manifests" / "LIFESTYLE_V1_SOURCE_INVENTORY.json").read_text(encoding="utf-8"))
assert inventory["synthetic_persona"] is True
assert inventory["synthetic_provenance_status"] == "CONFIRMED"
assert inventory["production_capability"] == "CONFIRMED_FOR_COLLECTION_OFFER"
assert inventory["launch_status"] == "PUBLIC_LAUNCH_AVAILABLE"
assert inventory["marketing_approved"] is False
assert inventory["avito_publication_approved"] is False
assert inventory["publish_approved"] is False
assert len(inventory["photos"]) == 10
assert all(item["decision"] == "PENDING" and item["production_approved"] is False for item in inventory["photos"])
for item in inventory["identity"] + inventory["photos"]:
    source = REPO / item["source"]
    assert source.exists() and sha256(source) == item["sha256"], f"source hash mismatch: {item['source']}"
checks.append("Lifestyle production capability is separate from exact-asset rights; source hashes preserved")

listing = (ROOT / "00_docs" / "AVITO_LISTING_COPY_v2.md").read_text(encoding="utf-8")
for required in (
    "Business — деловые портреты",
    "Lifestyle — естественные современные фотографии",
    "Portrait — 1 фото / 1 000 ₽",
    "Signature — 10 фото / 3 000 ₽",
    "Premium — 20 фото / 5 000 ₽",
    "доплатить только 2 000 ₽",
    "Signature → Premium: доплата 2 000 ₽",
    "Premium не включает полные Business и Lifestyle одновременно",
    "Напишите «Хочу ONYX»",
):
    assert required in listing, required
for forbidden in ("production-маршрут", "Reference QA", "production context", "order metadata", "100% prepayment", "subject to capacity", "soft launch"):
    assert forbidden.lower() not in listing.lower(), forbidden
checks.append("listing is customer-facing and preserves prices, upgrades and one-Collection Premium")

blueprint = (ROOT / "03_working" / "v2_3" / "CAROUSEL_BLUEPRINT_v2_3.md").read_text(encoding="utf-8")
for required in ("BUSINESS", "LIFESTYLE", "Другие направления — по согласованию", "uses no Lifestyle visual"):
    assert required in blueprint
build_script = (ROOT / "03_working" / "v2_3" / "build_review_pack_v2_3.py").read_text(encoding="utf-8")
assert "P02_F30_Lifestyle" not in build_script and "Orders" not in build_script
checks.append("slide 03 is typographic and uses no unapproved or private asset")

inspection = json.loads((QA / "render_inspection_v2_3.json").read_text(encoding="utf-8"))
assert inspection["status"] == "PASS" and len(inspection["files"]) == 22
assert (ROOT / "02_contact_sheets" / "AVITO_CAROUSEL_FINAL_REVIEW_v2_3.jpg").exists()
assert (QA / "AVITO_MOBILE_QA_v2_3.jpg").exists()
checks.append("final contact sheet and exact 390 px mobile preview")

result = {
    "status": "PASS",
    "release_status": "READY_FOR_AVITO_PUBLISH_APPROVAL",
    "revision": "v2.3",
    "public_collections": ["Business", "Lifestyle"],
    "lifestyle_exact_assets_published": False,
    "checks": checks,
    "publication_performed": False,
}
(QA / "validation_result_v2_3.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False))
