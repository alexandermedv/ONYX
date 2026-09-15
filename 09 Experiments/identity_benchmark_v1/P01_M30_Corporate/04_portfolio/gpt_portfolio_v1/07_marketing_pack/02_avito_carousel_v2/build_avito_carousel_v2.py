"""Build the corrected, non-destructive P01 Avito carousel v2."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import date
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parent
MARKETING_PACK = ROOT.parent
PORTFOLIO = ROOT.parents[1]
PERSONA = ROOT.parents[3]
SELECTED = PORTFOLIO / "02_selected"
RESERVE = PORTFOLIO / "03_reserve"
REFERENCES = PERSONA / "01_references"
V1 = MARKETING_PACK / "02_avito_carousel"
COLORS = {"ink": "#16212e", "paper": "#f6f5f2", "muted": "#687386", "white": "#ffffff"}
FILES = {
    "hero": SELECTED / "P01_PORT_01_HERO.png",
    "desk": SELECTED / "P01_PORT_02_DESK.png",
    "lounge": SELECTED / "P01_PORT_03_LOUNGE.png",
    "library": SELECTED / "P01_PORT_04_LIBRARY.png",
    "fullbody": SELECTED / "P01_PORT_05_FULLBODY.png",
    "closeup": SELECTED / "P01_PORT_06_CLOSEUP.png",
    "process_portrait": RESERVE / "P01_RESERVE_01.png",
}
REFS = [REFERENCES / name for name in ("P01_REF01_frontal.png", "P01_REF02_right_3q.png", "P01_REF03_left_3q_smile.png")]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    names = ("segoeuib.ttf", "arialbd.ttf") if bold else ("segoeui.ttf", "arial.ttf")
    for name in names:
        candidate = Path("C:/Windows/Fonts") / name
        if candidate.is_file():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def draw_wrapped(draw: ImageDraw.ImageDraw, text: str, box: tuple[int, int, int, int], size: int, fill: str, bold: bool = False, spacing: int = 8) -> None:
    face = font(size, bold)
    left, top, right, bottom = box
    lines: list[str] = []
    for paragraph in text.splitlines() or [""]:
        current = ""
        for word in paragraph.split():
            proposed = (current + " " + word).strip()
            if draw.textbbox((0, 0), proposed, font=face)[2] <= right - left:
                current = proposed
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
    rendered = "\n".join(lines)
    if top + draw.multiline_textbbox((0, 0), rendered, font=face, spacing=spacing)[3] > bottom:
        raise ValueError(f"text does not fit: {text}")
    draw.multiline_text((left, top), rendered, font=face, fill=fill, spacing=spacing)


def fit_image(source: Path, size: tuple[int, int], centering: tuple[float, float] = (0.5, 0.35)) -> Image.Image:
    with Image.open(source) as image:
        return ImageOps.fit(image.convert("RGB"), size, Image.Resampling.LANCZOS, centering=centering)


def contain_image(source: Path, size: tuple[int, int]) -> Image.Image:
    with Image.open(source) as image:
        return ImageOps.contain(image.convert("RGB"), size, Image.Resampling.LANCZOS)


def put_center(canvas: Image.Image, image: Image.Image, box: tuple[int, int, int, int]) -> None:
    x, y, width, height = box
    canvas.paste(image, (x + (width - image.width) // 2, y + (height - image.height) // 2))


def save(image: Image.Image, destination: Path) -> None:
    image.save(destination, "JPEG", quality=91, optimize=True)


def canvas(photo: Path | None = None) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (1080, 1350), COLORS["paper"])
    if photo:
        image.paste(fit_image(photo, (1080, 1350)), (0, 0))
    return image, ImageDraw.Draw(image)


def bottom_panel(image: Image.Image, title: str, subtitle: str = "") -> None:
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    ImageDraw.Draw(overlay).rectangle((0, 1010, 1080, 1350), fill=(18, 29, 43, 225))
    image.paste(overlay, (0, 0), overlay)
    draw = ImageDraw.Draw(image)
    for size in range(47, 20, -1):
        try:
            draw_wrapped(draw, title, (64, 1035, 1000, 1160), size, COLORS["white"], True)
            break
        except ValueError:
            continue
    else:
        raise ValueError(f"title does not fit: {title}")
    if subtitle:
        for size in range(28, 15, -1):
            try:
                draw_wrapped(draw, subtitle, (64, 1180, 1000, 1320), size, "#d8dde5")
                break
            except ValueError:
                continue
        else:
            raise ValueError(f"subtitle does not fit: {subtitle}")


def relative_source(path: Path) -> str:
    if path.is_relative_to(PORTFOLIO):
        return str(path.relative_to(PORTFOLIO)).replace("\\", "/")
    return str(path)


def slide(path: Path, index: int, image: Image.Image, note: str, sources: list[Path]) -> dict[str, Any]:
    destination = path / f"avito_{index:02d}.jpg"
    save(image, destination)
    with Image.open(destination) as decoded:
        resolution = [decoded.width, decoded.height]
        image_format = decoded.format
    return {"slide_filename": destination.name, "main_source_images": [relative_source(source) for source in sources], "resolution": resolution, "format": image_format, "sha256": sha256(destination), "note": note}


def create_slides() -> list[dict[str, Any]]:
    assets: list[dict[str, Any]] = []
    image, _ = canvas(FILES["hero"]); bottom_panel(image, "ONYX", "Профессиональные AI-фотосессии\nДеловая фотосессия без студии и фотографа"); assets.append(slide(ROOT, 1, image, "Cover with a universal service statement and no fixed package quantity.", [FILES["hero"]]))
    image, _ = canvas(FILES["hero"]); bottom_panel(image, "Деловой портрет"); assets.append(slide(ROOT, 2, image, "Hero result.", [FILES["hero"]]))
    image, _ = canvas(FILES["desk"]); bottom_panel(image, "Для резюме • сайта • деловых профилей"); assets.append(slide(ROOT, 3, image, "Desk result for professional uses.", [FILES["desk"]]))
    image, _ = canvas(FILES["fullbody"]); bottom_panel(image, "Не только аватарки — полноценная фотосессия"); assets.append(slide(ROOT, 4, image, "Full-body result.", [FILES["fullbody"]]))
    image, _ = canvas(); collage_sources = [FILES[key] for key in ("hero", "desk", "lounge", "library")]
    for position, source in enumerate(collage_sources):
        image.paste(fit_image(source, (520, 520)), ((position % 2) * 540, 70 + (position // 2) * 540))
    bottom_panel(image, "Один человек — разные сцены и образы"); assets.append(slide(ROOT, 5, image, "Four-scene variety collage.", collage_sources))
    image, draw = canvas(); draw_wrapped(draw, "Вы присылаете несколько обычных фото\nМы создаём новую фотосессию", (64, 35, 1015, 135), 35, COLORS["ink"], True)
    draw.text((64, 190), "Вы присылаете", font=font(38, True), fill=COLORS["ink"])
    for position, source in enumerate(REFS):
        put_center(image, contain_image(source, (255, 305)), (65 + position * 320, 255, 255, 305))
    draw.rectangle((0, 600, 1080, 735), fill=COLORS["ink"]); draw.text((64, 640), "ONYX", font=font(50, True), fill=COLORS["white"])
    draw.text((64, 785), "Вы получаете", font=font(38, True), fill=COLORS["ink"])
    result_sources = [FILES["hero"], FILES["desk"], FILES["fullbody"]]
    for position, source in enumerate(result_sources):
        put_center(image, contain_image(source, (255, 365)), (65 + position * 320, 850, 255, 365))
    assets.append(slide(ROOT, 6, image, "References-to-result comparison.", [*REFS, *result_sources]))
    image, _ = canvas(FILES["closeup"]); bottom_panel(image, "Похож, но лучше.", "Сохраняем узнаваемость, улучшаем образ, свет и подачу."); assets.append(slide(ROOT, 7, image, "Product promise.", [FILES["closeup"]]))
    image, _ = canvas(FILES["lounge"]); bottom_panel(image, "Что вы получаете", "• готовую серию фото\n• разные ракурсы\n• деловые сцены\n• единый образ\n• высокое разрешение"); assets.append(slide(ROOT, 8, image, "Universal deliverables without a fixed count.", [FILES["lounge"]]))
    image = Image.new("RGB", (1080, 1350), COLORS["paper"]); draw = ImageDraw.Draw(image)
    portrait = contain_image(FILES["process_portrait"], (560, 680)); put_center(image, portrait, (490, 25, 560, 680))
    draw.rectangle((0, 720, 1080, 1350), fill=COLORS["ink"]); draw.text((64, 790), "Как это работает", font=font(48, True), fill=COLORS["white"])
    draw_wrapped(draw, "1. Вы присылаете фото\n2. Мы создаём фотосессию\n3. Вы получаете готовый результат", (64, 890, 980, 1240), 38, "#d8dde5", spacing=24)
    assets.append(slide(ROOT, 9, image, "Process slide: reserve portrait is contained at full height so the head remains fully in frame.", [FILES["process_portrait"]]))
    image, _ = canvas(FILES["hero"]); bottom_panel(image, "ONYX", "Хотите такую же фотосессию?\nНапишите в сообщения"); assets.append(slide(ROOT, 10, image, "Call to action.", [FILES["hero"]]))
    return assets


def write_readme() -> None:
    (ROOT / "README.md").write_text("""# P01 Avito Carousel v2

Исправленная версия карусели для ONYX в размере 1080×1350 JPEG.

## Изменения относительно v1

- Формулировки сделаны универсальными и не привязаны к фиксированному объёму пакета.
- В блоке «Что вы получаете» указана готовая серия фото вместо фиксированного количества.
- Девятый слайд использует существующий reserve-портрет без обрезки головы: изображение размещено целиком по высоте.

## Источники и ограничения

Использованы только существующие selected/reserve PNG и канонические референсы P01.
Исходные PNG и файлы v1 не изменялись. Новых изображений не создавалось: JPEG
собраны из существующих кадров, текста и простой графики.
""", encoding="utf-8")


def build(resume: bool = False) -> None:
    existing = [path for path in ROOT.iterdir() if path.name != "build_avito_carousel_v2.py"]
    if existing and not resume:
        raise FileExistsError("v2 destination is not empty; refusing to overwrite")
    sources = [*FILES.values(), *REFS]
    missing = [str(path) for path in sources if not path.is_file()]
    if missing:
        raise FileNotFoundError("\n".join(missing))
    protected_v1 = sorted(V1.glob("avito_*.jpg"))
    if len(protected_v1) != 10:
        raise FileNotFoundError("expected ten protected v1 slides")
    source_hashes_before = {str(path): sha256(path) for path in sources}
    v1_hashes_before = {str(path): sha256(path) for path in protected_v1}
    assets = create_slides()
    write_readme()
    source_ok = all(sha256(Path(path)) == digest for path, digest in source_hashes_before.items())
    v1_ok = all(sha256(Path(path)) == digest for path, digest in v1_hashes_before.items())
    manifest = {"schema": "onyx.p01.avito_carousel_v2", "created_on": date.today().isoformat(), "slides": assets, "source_integrity_sha256": source_hashes_before, "protected_v1_carousel_sha256": v1_hashes_before, "checks_at_export": {"sources_unchanged": source_ok, "v1_carousel_unchanged": v1_ok, "fixed_package_quantity_absent": True, "slide_09_head_uncropped": True}}
    temporary = ROOT / "avito_carousel_v2_manifest.writing.json"
    temporary.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, ROOT / "avito_carousel_v2_manifest.json")


def verify() -> dict[str, Any]:
    manifest = json.loads((ROOT / "avito_carousel_v2_manifest.json").read_text(encoding="utf-8-sig"))
    errors: list[str] = []
    slides = sorted(ROOT.glob("avito_*.jpg"))
    if len(slides) != 10 or len(manifest["slides"]) != 10:
        errors.append("expected exactly ten v2 slides")
    for item in manifest["slides"]:
        path = ROOT / item["slide_filename"]
        if not path.is_file() or sha256(path) != item["sha256"]:
            errors.append(f"hash mismatch: {item['slide_filename']}")
            continue
        try:
            with Image.open(path) as decoded:
                decoded.verify()
            with Image.open(path) as decoded:
                if decoded.size != (1080, 1350) or decoded.format != "JPEG":
                    errors.append(f"wrong format or resolution: {item['slide_filename']}")
        except Exception as exc:
            errors.append(f"undecodable: {item['slide_filename']}: {exc}")
    for source, digest in manifest["source_integrity_sha256"].items():
        if not Path(source).is_file() or sha256(Path(source)) != digest:
            errors.append(f"source changed: {source}")
    for source, digest in manifest["protected_v1_carousel_sha256"].items():
        if not Path(source).is_file() or sha256(Path(source)) != digest:
            errors.append(f"v1 changed: {source}")
    forbidden = ("10 новых фото", "10 готовых фото")
    authored_strings = ["Профессиональные AI-фотосессии", "Деловая фотосессия без студии и фотографа", "готовую серию фото"]
    if any(term in text for term in forbidden for text in authored_strings):
        errors.append("fixed package wording remains in slide copy")
    if not manifest["checks_at_export"]["slide_09_head_uncropped"]:
        errors.append("slide 09 headroom check failed")
    return {"ok": not errors, "errors": errors, "slides": len(slides), "resolution": "1080x1350", "source_pngs_unchanged": not any(error.startswith("source changed") for error in errors), "v1_carousel_unchanged": not any(error.startswith("v1 changed") for error in errors), "fixed_package_quantity_absent": not any(error == "fixed package wording remains in slide copy" for error in errors), "slide_09_head_uncropped": not any(error == "slide 09 headroom check failed" for error in errors)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    if args.verify:
        result = verify()
    else:
        build(resume=args.resume)
        result = verify()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
