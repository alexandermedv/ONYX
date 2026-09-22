from pathlib import Path
from PIL import Image
import hashlib
import json


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[3]
SOURCE = REPO / "13 Production" / "Portfolio" / "P02" / "Business_V1" / "final_source_resolution"
INVENTORY = REPO / "13 Production" / "Portfolio" / "P02" / "BUSINESS_V1_SOURCE_INVENTORY.json"
EXPECTED = {
    "ONYX_P02_BUSINESS_01_HERO.jpg": "ffcd2a6e021d4edc4e1fd31159ae314ecde6097ea8610267ea86b7fe24c05162",
    "ONYX_P02_BUSINESS_02_CLOSE.jpg": "a8c54ee3f73541d513f19e89c84beb05e319f33e0c40edbc636e11c335387582",
    "ONYX_P02_BUSINESS_03_WAIST.jpg": "0e984d2851d5e3d99f4ff97906dbcfe748d27482eec4aa1280bf251738e23479",
    "ONYX_P02_BUSINESS_04_SEATED.jpg": "c51335f9dd689e77d0169be643b7d721fd443c23487b51c8d8bbb06ff1c0ddc3",
    "ONYX_P02_BUSINESS_05_ENVIRONMENT.jpg": "e5fc685dd0d6859f7afeaa31f85dab2659535dd7ac58f7aea6c368ecb68157c0",
    "ONYX_P02_BUSINESS_06_ACTION.jpg": "f6c071d10147c4187192b2cf6274f5366f53b15fc07cbf6b3953b8d748f3a1c8",
    "ONYX_P02_BUSINESS_07_3Q_BODY.jpg": "ced65a4bab43cdeadd2406321eb2c1fd8a63971081f58288c39663d35c6ace58",
    "ONYX_P02_BUSINESS_08_FULL_BODY.jpg": "6cc8ec0317a48b54fd5c48d9d7a515f29f1b8fcfc0ee5cd53ba005f87732a425",
    "ONYX_P02_BUSINESS_09_MOOD.jpg": "aa84f1f2f61e125cd6b91fbbb8095a529a1408ead5b4dd830298be8a91c746fd",
    "ONYX_P02_BUSINESS_10_EDITORIAL.jpg": "d918c5e894d5a6f8a0b191e1d78db72f03d3a30e4be98db4797e60c99261f6f5",
}


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


checks = []
inventory = json.loads(INVENTORY.read_text(encoding="utf-8-sig"))
for key, value in {
    "synthetic_persona": True,
    "marketing_approved": True,
    "avito_publication_approved": True,
    "publish_approved": True,
    "approval_scope": "AVITO_LAUNCH_V1",
    "unlisted_assets_approved": False,
}.items():
    assert inventory[key] == value, f"inventory field mismatch: {key}"
expected_inventory_paths = {
    f"13 Production/Portfolio/P02/Business_V1/final_source_resolution/{filename}"
    for filename in EXPECTED
}
assert set(inventory["publish_approval_applies_to"]) == expected_inventory_paths
assert inventory["approval"]["scope"] == "AVITO_LAUNCH_V1"
assert inventory["approval"]["source_assets_mutable"] is False
checks.append("inventory approval fields")

provenance = json.loads((ROOT / "01_asset_candidates" / "PROVENANCE.json").read_text(encoding="utf-8"))
assert len(provenance["assets"]) == 10
assert provenance["unlisted_assets_approved"] is False
for record in provenance["assets"]:
    filename = Path(record["source"]).name
    expected = EXPECTED[filename]
    source = SOURCE / filename
    candidate = ROOT / record["candidate_copy"]
    assert sha256(source) == expected
    assert sha256(candidate) == expected
    assert record["source_sha256"] == expected
    assert record["candidate_copy_sha256"] == expected
    assert record["approval_scope"] == "AVITO_LAUNCH_V1"
    assert record["source_mutated"] is False
    lowered = record["source"].lower()
    assert "/orders/" not in lowered and "/p01/" not in lowered and "/p03/" not in lowered
checks.append("ten source/copy SHA-256 pairs")

masters = sorted((ROOT / "04_master").glob("AVITO_*.png"))
exports = sorted((ROOT / "05_export").glob("AVITO_*.jpg"))
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
checks.append("ten masters and ten exports")

inspection = json.loads((ROOT / "06_qa" / "render_inspection.json").read_text(encoding="utf-8"))
assert inspection["status"] == "PASS" and len(inspection["files"]) == 23
checks.append("render inspection")

result = {"status": "PASS", "checks": checks, "source_files_unchanged_by_hash": 10}
(ROOT / "06_qa" / "validation_result.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(json.dumps(result, ensure_ascii=False))
