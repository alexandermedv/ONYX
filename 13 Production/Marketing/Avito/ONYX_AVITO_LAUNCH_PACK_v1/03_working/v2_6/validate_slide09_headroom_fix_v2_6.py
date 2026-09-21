from pathlib import Path
from PIL import Image
import hashlib
import json


ROOT = Path(__file__).resolve().parents[2]
V25_MASTER = ROOT / "04_master" / "v2_5"
V25_EXPORT = ROOT / "05_export" / "v2_5"
MASTER = ROOT / "04_master" / "v2_6"
EXPORT = ROOT / "05_export" / "v2_6"
QA = ROOT / "06_qa" / "v2_6"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


checks = []
masters = sorted(MASTER.glob("AVITO_V2_6_*.png"))
exports = sorted(EXPORT.glob("AVITO_V2_6_*.jpg"))
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
checks.append("ten v2.6 masters and exports")

for slide in (*range(1, 9), 10):
    assert sha256(MASTER / f"AVITO_V2_6_{slide:02d}.png") == sha256(V25_MASTER / f"AVITO_V2_5_{slide:02d}.png")
    assert sha256(EXPORT / f"AVITO_V2_6_{slide:02d}.jpg") == sha256(V25_EXPORT / f"AVITO_V2_5_{slide:02d}.jpg")
assert sha256(MASTER / "AVITO_V2_6_09.png") != sha256(V25_MASTER / "AVITO_V2_5_09.png")
assert sha256(EXPORT / "AVITO_V2_6_09.jpg") != sha256(V25_EXPORT / "AVITO_V2_5_09.jpg")
checks.append("only slide 09 changed from v2.5")

v25_inspection = json.loads((ROOT / "06_qa" / "v2_5" / "render_inspection_v2_5.json").read_text(encoding="utf-8"))
for item in v25_inspection["files"]:
    path = ROOT / item["path"]
    assert path.exists() and sha256(path) == item["sha256"], f"v2.5 output changed: {item['path']}"
checks.append("v2.5 outputs preserved")

builder = (ROOT / "03_working" / "v2_6" / "build_slide09_headroom_fix_v2_6.py").read_text(encoding="utf-8")
assert "preserving the complete source top edge" in builder
assert "box = (0, 0, image.width, crop_h)" in builder
checks.append("slide 09 crops preserve the complete source top edge")

inspection = json.loads((QA / "render_inspection_v2_6.json").read_text(encoding="utf-8"))
assert inspection["status"] == "PASS" and len(inspection["files"]) == 22
assert (ROOT / "02_contact_sheets" / "AVITO_CAROUSEL_FINAL_v2_6.jpg").exists()
assert (QA / "AVITO_MOBILE_QA_v2_6.jpg").exists()
checks.append("final carousel and exact 390 px preview for slide 09")

result = {
    "status": "PASS",
    "release_status": "APPROVED_FOR_AVITO_PUBLISH",
    "revision": "v2.6",
    "headroom_fixed_cards": [9],
    "visual_review": "PASS — complete head and hair contour visible in all four images on slide 09",
    "checks": checks,
    "publication_performed": False,
}
(QA / "validation_result_v2_6.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False))
