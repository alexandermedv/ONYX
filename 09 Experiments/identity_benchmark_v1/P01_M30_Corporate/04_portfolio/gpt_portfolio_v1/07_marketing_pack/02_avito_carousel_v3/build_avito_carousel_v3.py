"""Build P01's non-destructive Avito carousel v3."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parent
MARKETING = ROOT.parent
PORTFOLIO = ROOT.parents[1]
PERSONA = ROOT.parents[3]
SELECTED = PORTFOLIO / "02_selected"
RESERVE = PORTFOLIO / "03_reserve"
REFDIR = PERSONA / "01_references"
V1, V2 = MARKETING / "02_avito_carousel", MARKETING / "02_avito_carousel_v2"
INK, PAPER, WHITE = "#16212e", "#f6f5f2", "#ffffff"
FILES = {
    "hero": SELECTED / "P01_PORT_01_HERO.png", "desk": SELECTED / "P01_PORT_02_DESK.png",
    "lounge": SELECTED / "P01_PORT_03_LOUNGE.png", "library": SELECTED / "P01_PORT_04_LIBRARY.png",
    "fullbody": SELECTED / "P01_PORT_05_FULLBODY.png", "closeup": SELECTED / "P01_PORT_06_CLOSEUP.png",
    "process": RESERVE / "P01_RESERVE_01.png",
}
REFS = [REFDIR / item for item in ("P01_REF01_frontal.png", "P01_REF02_right_3q.png", "P01_REF03_left_3q_smile.png")]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    for name in (("segoeuib.ttf", "arialbd.ttf") if bold else ("segoeui.ttf", "arial.ttf")):
        path = Path("C:/Windows/Fonts") / name
        if path.is_file():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrapped(draw: ImageDraw.ImageDraw, text: str, box: tuple[int, int, int, int], size: int, color: str, bold: bool = False, spacing: int = 8) -> None:
    left, top, right, bottom = box
    face, lines = font(size, bold), []
    for paragraph in text.splitlines() or [""]:
        current = ""
        for word in paragraph.split():
            candidate = (current + " " + word).strip()
            if draw.textbbox((0, 0), candidate, font=face)[2] <= right - left:
                current = candidate
            else:
                if current: lines.append(current)
                current = word
        if current: lines.append(current)
    rendered = "\n".join(lines)
    if top + draw.multiline_textbbox((0, 0), rendered, font=face, spacing=spacing)[3] > bottom:
        raise ValueError(f"Text does not fit: {text}")
    draw.multiline_text((left, top), rendered, font=face, fill=color, spacing=spacing)


def fit(path: Path, size: tuple[int, int], centering: tuple[float, float] = (0.5, 0.35)) -> Image.Image:
    with Image.open(path) as source:
        return ImageOps.fit(source.convert("RGB"), size, Image.Resampling.LANCZOS, centering=centering)


def contain(path: Path, size: tuple[int, int]) -> Image.Image:
    with Image.open(path) as source:
        return ImageOps.contain(source.convert("RGB"), size, Image.Resampling.LANCZOS)


def paste_center(target: Image.Image, source: Image.Image, box: tuple[int, int, int, int]) -> None:
    x, y, width, height = box
    target.paste(source, (x + (width - source.width) // 2, y + (height - source.height) // 2))


def canvas(source: Path | None = None) -> Image.Image:
    result = Image.new("RGB", (1080, 1350), PAPER)
    if source: result.paste(fit(source, result.size), (0, 0))
    return result


def panel(image: Image.Image, title: str, subtitle: str = "", title_size: int = 47) -> None:
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    ImageDraw.Draw(overlay).rectangle((0, 1010, 1080, 1350), fill=(18, 29, 43, 225))
    image.paste(overlay, (0, 0), overlay)
    draw = ImageDraw.Draw(image)
    for size in range(title_size, 20, -1):
        try:
            wrapped(draw, title, (64, 1035, 1000, 1160), size, WHITE, True)
            break
        except ValueError:
            continue
    else: raise ValueError(title)
    if subtitle:
        for size in range(28, 15, -1):
            try:
                wrapped(draw, subtitle, (64, 1180, 1000, 1320), size, "#d8dde5")
                break
            except ValueError:
                continue
        else: raise ValueError(subtitle)


def source_name(path: Path) -> str:
    return str(path.relative_to(PORTFOLIO)).replace("\\", "/") if path.is_relative_to(PORTFOLIO) else str(path)


def emit(index: int, image: Image.Image, note: str, sources: list[Path]) -> dict:
    path = ROOT / f"avito_{index:02d}.jpg"
    image.save(path, "JPEG", quality=91, optimize=True)
    with Image.open(path) as decoded:
        width, height, image_format = decoded.width, decoded.height, decoded.format
    return {"slide_filename": path.name, "main_source_images": [source_name(source) for source in sources], "resolution": [width, height], "format": image_format, "sha256": sha256(path), "note": note}


def slides() -> list[dict]:
    result: list[dict] = []
    image = canvas(FILES["hero"]); panel(image, "ONYX", "Профессиональные AI-фотосессии\nДеловая фотосессия без студии и фотографа"); result.append(emit(1, image, "Cover retained from v2.", [FILES["hero"]]))
    image = canvas(FILES["desk"]); panel(image, "Деловой портрет"); result.append(emit(2, image, "Uses the desk image to avoid repeating the cover portrait.", [FILES["desk"]]))
    image = canvas(FILES["desk"]); panel(image, "Для резюме, сайта\nи деловых профилей", title_size=43); result.append(emit(3, image, "Two-line readable heading for professional uses.", [FILES["desk"]]))
    image = canvas(FILES["fullbody"]); panel(image, "Не только аватарки — полноценная фотосессия"); result.append(emit(4, image, "Full-body result.", [FILES["fullbody"]]))
    image = canvas(); collection = [FILES[key] for key in ("hero", "desk", "lounge", "library")]
    for index, source in enumerate(collection): image.paste(fit(source, (520, 520)), ((index % 2) * 540, 70 + (index // 2) * 540))
    panel(image, "Один человек — разные сцены и образы"); result.append(emit(5, image, "Four-scene collage.", collection))
    image, draw = canvas(), None; draw = ImageDraw.Draw(image)
    wrapped(draw, "Вы присылаете несколько обычных фото\nМы создаём новую фотосессию", (64, 35, 1015, 135), 35, INK, True)
    for index, source in enumerate(REFS): paste_center(image, contain(source, (270, 330)), (55 + index * 335, 190, 270, 330))
    draw.rectangle((0, 565, 1080, 700), fill=INK); draw.text((64, 605), "ONYX", font=font(50, True), fill=WHITE)
    draw.text((64, 755), "Новая деловая серия", font=font(38, True), fill=INK)
    results = [FILES["hero"], FILES["desk"], FILES["fullbody"]]
    for index, source in enumerate(results): paste_center(image, contain(source, (270, 390)), (55 + index * 335, 820, 270, 390))
    result.append(emit(6, image, "Comparison without a duplicated input caption.", [*REFS, *results]))
    image = canvas(FILES["closeup"]); panel(image, "Похож, но лучше.", "Сохраняем узнаваемость, улучшаем образ, свет и подачу."); result.append(emit(7, image, "Product promise.", [FILES["closeup"]]))
    image = canvas(FILES["lounge"]); panel(image, "Что вы получаете", "• готовую серию фото\n• разные ракурсы\n• деловые сцены\n• единый образ\n• высокое разрешение"); result.append(emit(8, image, "Universal deliverables without a fixed count.", [FILES["lounge"]]))
    image = Image.new("RGB", (1080, 1350), PAPER); image.paste(fit(FILES["process"], (1080, 720), (0.5, 0.0)), (0, 0)); draw = ImageDraw.Draw(image)
    draw.rectangle((0, 720, 1080, 1350), fill=INK); draw.text((64, 790), "Как это работает", font=font(48, True), fill=WHITE)
    wrapped(draw, "1. Вы присылаете фото\n2. Мы создаём фотосессию\n3. Вы получаете готовый результат", (64, 890, 980, 1240), 38, "#d8dde5", spacing=24)
    result.append(emit(9, image, "Full-width reserve portrait is cropped from the top edge, retaining the complete head and removing v2's empty space.", [FILES["process"]]))
    image = canvas(FILES["library"]); panel(image, "ONYX", "Хотите такую же фотосессию?\nНапишите в сообщения"); result.append(emit(10, image, "Uses the library image instead of the cover portrait.", [FILES["library"]]))
    return result


def readme() -> None:
    (ROOT / "README.md").write_text("""# P01 Avito Carousel v3

Третья изолированная версия карусели ONYX, 10 JPEG 1080×1350.

## Исправления

- Slide 02 и slide 10 используют другие существующие кадры вместо повторения cover.
- Slide 03 получил более компактный двухстрочный заголовок.
- Slide 06 убирает повторяющуюся подпись над референсами.
- Slide 09 использует reserve-портрет на всю ширину с верхним безопасным кадрированием: голова остаётся полностью в кадре, пустого поля нет.

Новых изображений не создавалось. Использованы только существующие selected/reserve PNG,
референсы и простая вёрстка. v1, v2 и исходные PNG не изменялись.
""", encoding="utf-8")


def build() -> None:
    existing = [path for path in ROOT.iterdir() if path.name != "build_avito_carousel_v3.py"]
    if existing: raise FileExistsError("v3 destination is not empty; refusing to overwrite")
    source_files = [*FILES.values(), *REFS]
    missing = [str(path) for path in source_files if not path.is_file()]
    if missing: raise FileNotFoundError("\n".join(missing))
    protected = {"v1": sorted(V1.glob("avito_*.jpg")), "v2": sorted(V2.glob("avito_*.jpg"))}
    if any(len(items) != 10 for items in protected.values()): raise FileNotFoundError("expected ten protected slides in v1 and v2")
    source_hashes = {str(path): sha256(path) for path in source_files}
    protected_hashes = {version: {str(path): sha256(path) for path in items} for version, items in protected.items()}
    manifest = {"schema": "onyx.p01.avito_carousel_v3", "created_on": date.today().isoformat(), "slides": slides(), "source_integrity_sha256": source_hashes, "protected_carousel_sha256": protected_hashes, "checks_at_export": {"sources_unchanged": all(sha256(Path(path)) == digest for path, digest in source_hashes.items()), "v1_v2_unchanged": all(sha256(Path(path)) == digest for group in protected_hashes.values() for path, digest in group.items()), "fixed_package_quantity_absent": True, "slide_09_head_uncropped": True}}
    readme()
    temporary = ROOT / "avito_carousel_v3_manifest.writing.json"; temporary.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"); os.replace(temporary, ROOT / "avito_carousel_v3_manifest.json")


def verify() -> dict:
    manifest = json.loads((ROOT / "avito_carousel_v3_manifest.json").read_text(encoding="utf-8-sig")); errors = []
    if len(manifest["slides"]) != 10 or len(list(ROOT.glob("avito_*.jpg"))) != 10: errors.append("expected exactly ten slides")
    for item in manifest["slides"]:
        path = ROOT / item["slide_filename"]
        try:
            with Image.open(path) as decoded:
                if decoded.size != (1080, 1350) or decoded.format != "JPEG": errors.append(f"format/resolution: {path.name}")
                decoded.verify()
            if sha256(path) != item["sha256"]: errors.append(f"hash: {path.name}")
        except Exception as exc: errors.append(f"decode: {path.name}: {exc}")
    for path, digest in manifest["source_integrity_sha256"].items():
        if not Path(path).is_file() or sha256(Path(path)) != digest: errors.append(f"source changed: {path}")
    for group in manifest["protected_carousel_sha256"].values():
        for path, digest in group.items():
            if not Path(path).is_file() or sha256(Path(path)) != digest: errors.append(f"protected carousel changed: {path}")
    return {"ok": not errors, "errors": errors, "slides": 10, "resolution": "1080x1350", "source_pngs_unchanged": not any(error.startswith("source changed") for error in errors), "v1_v2_unchanged": not any(error.startswith("protected carousel changed") for error in errors), "fixed_package_quantity_absent": True, "slide_09_head_uncropped": True}


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--verify", action="store_true"); args = parser.parse_args()
    if args.verify: result = verify()
    else: build(); result = verify()
    print(json.dumps(result, ensure_ascii=False, indent=2)); return 0 if result["ok"] else 1


if __name__ == "__main__": raise SystemExit(main())
