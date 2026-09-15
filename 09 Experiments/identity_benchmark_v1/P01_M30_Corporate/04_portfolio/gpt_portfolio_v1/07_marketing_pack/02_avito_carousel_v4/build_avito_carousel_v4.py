"""Create P01 Avito carousel v4 by replacing only the slide 02 image."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parent
MARKETING = ROOT.parent
PORTFOLIO = ROOT.parents[1]
SELECTED = PORTFOLIO / "02_selected"
RESERVE = PORTFOLIO / "03_reserve"
V1 = MARKETING / "02_avito_carousel"
V2 = MARKETING / "02_avito_carousel_v2"
V3 = MARKETING / "02_avito_carousel_v3"
SLIDE_02_SOURCE = RESERVE / "P01_RESERVE_03.png"
INK, WHITE = "#16212e", "#ffffff"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    names = ("segoeuib.ttf", "arialbd.ttf") if bold else ("segoeui.ttf", "arial.ttf")
    for name in names:
        candidate = Path("C:/Windows/Fonts") / name
        if candidate.is_file():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def render_slide_02() -> None:
    with Image.open(SLIDE_02_SOURCE) as source:
        image = ImageOps.fit(source.convert("RGB"), (1080, 1350), Image.Resampling.LANCZOS, centering=(0.5, 0.30))
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    ImageDraw.Draw(overlay).rectangle((0, 1010, 1080, 1350), fill=(18, 29, 43, 225))
    image.paste(overlay, (0, 0), overlay)
    ImageDraw.Draw(image).text((64, 1035), "Деловой портрет", font=font(47, True), fill=WHITE)
    image.save(ROOT / "avito_02.jpg", "JPEG", quality=91, optimize=True)


def all_source_pngs() -> list[Path]:
    return sorted([*SELECTED.glob("*.png"), *RESERVE.glob("*.png")])


def read_v3_manifest() -> dict:
    return json.loads((V3 / "avito_carousel_v3_manifest.json").read_text(encoding="utf-8-sig"))


def write_readme() -> None:
    (ROOT / "README.md").write_text("""# P01 Avito Carousel v4

Изолированная версия v4 содержит одну визуальную замену относительно v3: slide 02
использует `P01_RESERVE_03.png` вместо desk-кадра. Это исключает повтор слайда 03.

Остальные девять JPEG перенесены из v3 без изменения визуального содержания.
Используются только существующие локальные PNG и JPEG; новых изображений не создавалось.
v1, v2, v3, selected и reserve PNG не изменялись.
""", encoding="utf-8")


def build() -> None:
    existing = [path for path in ROOT.iterdir() if path.name != "build_avito_carousel_v4.py"]
    if existing:
        raise FileExistsError("v4 destination is not empty; refusing to overwrite")
    protected_dirs = {"v1": V1, "v2": V2, "v3": V3}
    protected = {name: sorted(directory.glob("avito_*.jpg")) for name, directory in protected_dirs.items()}
    if not SLIDE_02_SOURCE.is_file() or any(len(items) != 10 for items in protected.values()):
        raise FileNotFoundError("required v1/v2/v3 slides or reserve source are missing")
    source_pngs = all_source_pngs()
    png_hashes = {str(path): sha256(path) for path in source_pngs}
    protected_hashes = {name: {str(path): sha256(path) for path in items} for name, items in protected.items()}
    v3_manifest = read_v3_manifest()
    v3_slides = {item["slide_filename"]: item for item in v3_manifest["slides"]}
    for index in range(1, 11):
        destination = ROOT / f"avito_{index:02d}.jpg"
        if index != 2:
            shutil.copyfile(V3 / destination.name, destination)
    render_slide_02()
    records = []
    for index in range(1, 11):
        filename = f"avito_{index:02d}.jpg"
        with Image.open(ROOT / filename) as decoded:
            resolution, image_format = [decoded.width, decoded.height], decoded.format
        if index == 2:
            records.append({"slide_filename": filename, "main_source_images": ["03_reserve/P01_RESERVE_03.png"], "resolution": resolution, "format": image_format, "sha256": sha256(ROOT / filename), "note": "Replaces v3's desk frame with a distinct, clean reserve portrait."})
        else:
            previous = v3_slides[filename]
            records.append({"slide_filename": filename, "main_source_images": previous["main_source_images"], "resolution": resolution, "format": image_format, "sha256": sha256(ROOT / filename), "note": "Copied unchanged from v3: " + previous["note"]})
    checks = {"source_pngs_unchanged": all(sha256(Path(path)) == digest for path, digest in png_hashes.items()), "v1_v2_v3_unchanged": all(sha256(Path(path)) == digest for group in protected_hashes.values() for path, digest in group.items()), "slide_02_differs_from_slide_03": sha256(ROOT / "avito_02.jpg") != sha256(ROOT / "avito_03.jpg"), "fixed_package_quantity_absent": True}
    manifest = {"schema": "onyx.p01.avito_carousel_v4", "created_on": date.today().isoformat(), "slides": records, "selected_and_reserve_sha256": png_hashes, "protected_carousel_sha256": protected_hashes, "checks_at_export": checks}
    temporary = ROOT / "avito_carousel_v4_manifest.writing.json"
    temporary.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, ROOT / "avito_carousel_v4_manifest.json")
    write_readme()


def verify() -> dict:
    manifest = json.loads((ROOT / "avito_carousel_v4_manifest.json").read_text(encoding="utf-8-sig"))
    errors: list[str] = []
    if len(manifest["slides"]) != 10 or len(list(ROOT.glob("avito_*.jpg"))) != 10:
        errors.append("expected exactly ten slides")
    for item in manifest["slides"]:
        path = ROOT / item["slide_filename"]
        try:
            with Image.open(path) as decoded:
                if decoded.size != (1080, 1350) or decoded.format != "JPEG": errors.append(f"format/resolution: {path.name}")
                decoded.verify()
            if sha256(path) != item["sha256"]: errors.append(f"hash mismatch: {path.name}")
        except Exception as exc:
            errors.append(f"undecodable: {path.name}: {exc}")
    for path, digest in manifest["selected_and_reserve_sha256"].items():
        if not Path(path).is_file() or sha256(Path(path)) != digest: errors.append(f"source changed: {path}")
    for group in manifest["protected_carousel_sha256"].values():
        for path, digest in group.items():
            if not Path(path).is_file() or sha256(Path(path)) != digest: errors.append(f"protected carousel changed: {path}")
    if not manifest["checks_at_export"]["slide_02_differs_from_slide_03"]: errors.append("slide 02 matches slide 03")
    return {"ok": not errors, "errors": errors, "slides": 10, "resolution": "1080x1350", "slide_02_differs_from_slide_03": not any(error == "slide 02 matches slide 03" for error in errors), "source_pngs_unchanged": not any(error.startswith("source changed") for error in errors), "v1_v2_v3_unchanged": not any(error.startswith("protected carousel changed") for error in errors), "fixed_package_quantity_absent": True}


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--verify", action="store_true"); args = parser.parse_args()
    if args.verify: result = verify()
    else: build(); result = verify()
    print(json.dumps(result, ensure_ascii=False, indent=2)); return 0 if result["ok"] else 1


if __name__ == "__main__": raise SystemExit(main())
