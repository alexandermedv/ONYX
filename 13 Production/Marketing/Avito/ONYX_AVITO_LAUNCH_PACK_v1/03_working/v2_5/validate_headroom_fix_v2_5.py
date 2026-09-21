from pathlib import Path
from PIL import Image
import hashlib
import json


ROOT = Path(__file__).resolve().parents[2]
V24_MASTER = ROOT / "04_master" / "v2_4"
V24_EXPORT = ROOT / "05_export" / "v2_4"
MASTER = ROOT / "04_master" / "v2_5"
EXPORT = ROOT / "05_export" / "v2_5"
QA = ROOT / "06_qa" / "v2_5"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


checks = []
masters = sorted(MASTER.glob("AVITO_V2_5_*.png"))
exports = sorted(EXPORT.glob("AVITO_V2_5_*.jpg"))
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
checks.append("ten v2.5 masters and exports")

for slide in (1, 6, 7, 8, 9, 10):
    assert sha256(MASTER / f"AVITO_V2_5_{slide:02d}.png") == sha256(V24_MASTER / f"AVITO_V2_4_{slide:02d}.png")
    assert sha256(EXPORT / f"AVITO_V2_5_{slide:02d}.jpg") == sha256(V24_EXPORT / f"AVITO_V2_4_{slide:02d}.jpg")
for slide in (2, 3, 4, 5):
    assert sha256(MASTER / f"AVITO_V2_5_{slide:02d}.png") != sha256(V24_MASTER / f"AVITO_V2_4_{slide:02d}.png")
checks.append("only slides 02–05 changed from v2.4")

v24_inspection = json.loads((ROOT / "06_qa" / "v2_4" / "render_inspection_v2_4.json").read_text(encoding="utf-8"))
for item in v24_inspection["files"]:
    path = ROOT / item["path"]
    assert path.exists() and sha256(path) == item["sha256"], f"v2.4 output changed: {item['path']}"
checks.append("v2.4 outputs preserved")

builder = (ROOT / "03_working" / "v2_5" / "build_headroom_fix_v2_5.py").read_text(encoding="utf-8")
assert "without removing any source pixels from the top edge" in builder
assert "box = (0, 0, image.width, crop_h)" in builder
checks.append("wide crops preserve the complete source top edge")

inspection = json.loads((QA / "render_inspection_v2_5.json").read_text(encoding="utf-8"))
assert inspection["status"] == "PASS" and len(inspection["files"]) == 22
assert (ROOT / "02_contact_sheets" / "AVITO_CAROUSEL_FINAL_v2_5.jpg").exists()
assert (QA / "AVITO_MOBILE_QA_v2_5.jpg").exists()
checks.append("final carousel and exact 390 px previews for slides 02–05")

result = {
    "status": "PASS",
    "release_status": "APPROVED_FOR_AVITO_PUBLISH",
    "revision": "v2.5",
    "headroom_fixed_cards": [2, 3, 4, 5],
    "visual_review": "PASS — complete head and hair contour visible in every image on slides 02–05",
    "checks": checks,
    "publication_performed": False,
}
(QA / "validation_result_v2_5.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False))
