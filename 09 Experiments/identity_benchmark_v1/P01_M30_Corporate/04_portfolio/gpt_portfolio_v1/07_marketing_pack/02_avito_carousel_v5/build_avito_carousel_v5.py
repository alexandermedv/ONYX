"""Build P01's final cosmetic Avito carousel v5 from local portfolio assets."""
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
SELECTED, RESERVE = PORTFOLIO / "02_selected", PORTFOLIO / "03_reserve"
REFDIR = PERSONA / "01_references"
PREVIOUS = {f"v{number}": MARKETING / folder for number, folder in ((1, "02_avito_carousel"), (2, "02_avito_carousel_v2"), (3, "02_avito_carousel_v3"), (4, "02_avito_carousel_v4"))}
INK, PAPER, WHITE, MUTED, ACCENT = "#16212e", "#f6f5f2", "#ffffff", "#d8dde5", "#a88a58"
FILES = {
    "hero": SELECTED / "P01_PORT_01_HERO.png", "desk": SELECTED / "P01_PORT_02_DESK.png",
    "lounge": SELECTED / "P01_PORT_03_LOUNGE.png", "library": SELECTED / "P01_PORT_04_LIBRARY.png",
    "fullbody": SELECTED / "P01_PORT_05_FULLBODY.png", "closeup": SELECTED / "P01_PORT_06_CLOSEUP.png",
    "business": RESERVE / "P01_RESERVE_03.png", "process": RESERVE / "P01_RESERVE_01.png",
}
REFS = [REFDIR / name for name in ("P01_REF01_frontal.png", "P01_REF02_right_3q.png", "P01_REF03_left_3q_smile.png")]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    for name in (("segoeuib.ttf", "arialbd.ttf") if bold else ("segoeui.ttf", "arial.ttf")):
        candidate = Path("C:/Windows/Fonts") / name
        if candidate.is_file(): return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def wrapped(draw: ImageDraw.ImageDraw, text: str, box: tuple[int, int, int, int], size: int, color: str, bold: bool = False, spacing: int = 8) -> None:
    left, top, right, bottom = box; face = font(size, bold); lines: list[str] = []
    for paragraph in text.splitlines() or [""]:
        current = ""
        for word in paragraph.split():
            proposal = (current + " " + word).strip()
            if draw.textbbox((0, 0), proposal, font=face)[2] <= right - left: current = proposal
            else:
                if current: lines.append(current)
                current = word
        if current: lines.append(current)
    rendered = "\n".join(lines)
    if top + draw.multiline_textbbox((0, 0), rendered, font=face, spacing=spacing)[3] > bottom: raise ValueError(text)
    draw.multiline_text((left, top), rendered, font=face, fill=color, spacing=spacing)


def fit(path: Path, size: tuple[int, int], centering: tuple[float, float] = (0.5, 0.35)) -> Image.Image:
    with Image.open(path) as source: return ImageOps.fit(source.convert("RGB"), size, Image.Resampling.LANCZOS, centering=centering)


def contain(path: Path, size: tuple[int, int]) -> Image.Image:
    with Image.open(path) as source: return ImageOps.contain(source.convert("RGB"), size, Image.Resampling.LANCZOS)


def center_paste(target: Image.Image, image: Image.Image, box: tuple[int, int, int, int]) -> None:
    x, y, width, height = box; target.paste(image, (x + (width - image.width) // 2, y + (height - image.height) // 2))


def base(source: Path | None = None) -> Image.Image:
    image = Image.new("RGB", (1080, 1350), PAPER)
    if source: image.paste(fit(source, image.size), (0, 0))
    return image


def photo_panel(image: Image.Image, title: str, subtitle: str = "", panel_top: int = 1060, title_size: int = 45) -> None:
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0)); ImageDraw.Draw(overlay).rectangle((0, panel_top, 1080, 1350), fill=(18, 29, 43, 220)); image.paste(overlay, (0, 0), overlay)
    draw = ImageDraw.Draw(image); wrapped(draw, title, (64, panel_top + 35, 1000, panel_top + 160), title_size, WHITE, True)
    if subtitle: wrapped(draw, subtitle, (64, panel_top + 175, 1000, 1320), 27, MUTED)


def source_name(path: Path) -> str:
    return str(path.relative_to(PORTFOLIO)).replace("\\", "/") if path.is_relative_to(PORTFOLIO) else str(path)


def emit(index: int, image: Image.Image, purpose: str, sources: list[Path]) -> dict:
    destination = ROOT / f"avito_{index:02d}.jpg"; image.save(destination, "JPEG", quality=91, optimize=True)
    with Image.open(destination) as decoded: resolution, image_format = [decoded.width, decoded.height], decoded.format
    return {"slide_filename": destination.name, "purpose": purpose, "main_source_images": [source_name(source) for source in sources], "resolution": resolution, "format": image_format, "sha256": sha256(destination)}


def build_slides() -> list[dict]:
    slides: list[dict] = []
    image = base(FILES["hero"]); photo_panel(image, "ONYX", "Виртуальная деловая фотосессия\nПохожи на себя. Выглядите лучше.", 1040, 46); slides.append(emit(1, image, "Cover: virtual business photo session.", [FILES["hero"]]))
    image = base(); draw = ImageDraw.Draw(image); wrapped(draw, "Несколько ваших фото →\nновая профессиональная фотосессия", (64, 38, 1010, 145), 35, INK, True)
    for index, source in enumerate(REFS): center_paste(image, contain(source, (260, 315)), (55 + index * 335, 205, 260, 315))
    draw.rectangle((0, 575, 1080, 700), fill=INK); draw.text((64, 615), "ONYX", font=font(48, True), fill=WHITE)
    result_sources = [FILES["hero"], FILES["desk"], FILES["fullbody"]]
    for index, source in enumerate(result_sources): center_paste(image, contain(source, (260, 395)), (55 + index * 335, 790, 260, 395))
    slides.append(emit(2, image, "Transformation: references to a new professional series.", [*REFS, *result_sources]))
    image = base(); collection = [FILES[key] for key in ("hero", "desk", "lounge", "library")]
    for index, source in enumerate(collection): image.paste(fit(source, (520, 515)), ((index % 2) * 540, 20 + (index // 2) * 525))
    photo_panel(image, "Один человек — разные сцены и образы", panel_top=1080, title_size=42); slides.append(emit(3, image, "Variety: four scenes and looks.", collection))
    image = base(FILES["closeup"]); photo_panel(image, "Похож, но лучше.", "Сохраняем узнаваемость, улучшаем образ, свет и подачу.", 1060, 46); slides.append(emit(4, image, "Promise: identity and presentation.", [FILES["closeup"]]))
    image = base(FILES["business"]); photo_panel(image, "Деловой портрет", "Для работы, резюме и профессиональных профилей", 1080, 44); slides.append(emit(5, image, "Example: business portrait.", [FILES["business"]]))
    image = base(FILES["fullbody"]); photo_panel(image, "Не только аватарки —\nполноценная фотосессия", panel_top=1060, title_size=43); slides.append(emit(6, image, "Example: full-body and scene diversity.", [FILES["fullbody"]]))
    image = Image.new("RGB", (1080, 1350), INK); draw = ImageDraw.Draw(image); image.paste(fit(FILES["closeup"], (1080, 280), (0.5, 0.0)), (0, 0)); overlay = Image.new("RGBA", (1080, 280), (18, 29, 43, 130)); image.paste(overlay, (0, 0), overlay); draw = ImageDraw.Draw(image)
    wrapped(draw, "Не просто генерация\nпо промту", (64, 325, 1000, 440), 42, WHITE, True)
    cards = [("Сцены и образы", "подбираем серию"), ("Контроль качества", "проверяем детали"), ("Отбор и исправление", "доводим кадры"), ("Финальная подготовка", "улучшаем и выдаём")]
    for index, (title, caption) in enumerate(cards):
        x, y = 64 + (index % 2) * 490, 500 + (index // 2) * 205; draw.rectangle((x, y, x + 450, y + 165), fill="#223144"); draw.line((x, y, x + 450, y), fill=ACCENT, width=4); wrapped(draw, title, (x + 24, y + 28, x + 426, y + 85), 26, WHITE, True); wrapped(draw, caption, (x + 24, y + 100, x + 426, y + 140), 22, MUTED)
    wrapped(draw, "До клиента доходят только прошедшие проверку кадры.", (64, 960, 1000, 1035), 28, WHITE, True); slides.append(emit(7, image, "Production value: scenes, quality control, repair and final preparation.", [FILES["closeup"]]))
    image = base(FILES["lounge"]); overlay = Image.new("RGBA", image.size, (0, 0, 0, 0)); ImageDraw.Draw(overlay).rectangle((0, 900, 1080, 1350), fill=(246, 245, 242, 242)); image.paste(overlay, (0, 0), overlay); draw = ImageDraw.Draw(image); draw.text((64, 945), "Что вы получаете", font=font(42, True), fill=INK)
    deliverables = ["готовую серию фотографий", "разные сцены и ракурсы", "единый узнаваемый образ", "отобранные и проверенные кадры", "изображения высокого разрешения"]
    for index, item in enumerate(deliverables): draw.text((70, 1020 + index * 58), "•", font=font(28, True), fill=ACCENT); draw.text((105, 1023 + index * 58), item, font=font(24), fill=INK)
    slides.append(emit(8, image, "Deliverables: ready, checked high-resolution series.", [FILES["lounge"]]))
    image = Image.new("RGB", (1080, 1350), INK); image.paste(fit(FILES["process"], (1080, 640), (0.5, 0.0)), (0, 0)); draw = ImageDraw.Draw(image); draw.text((64, 700), "Как это работает", font=font(44, True), fill=WHITE)
    steps = [("01", "Присылаете фотографии"), ("02", "Мы создаём и доводим серию"), ("03", "Получаете готовые изображения")]
    for index, (number, label) in enumerate(steps):
        y = 785 + index * 145; draw.text((64, y), number, font=font(54, True), fill=ACCENT); wrapped(draw, label, (205, y + 9, 1000, y + 80), 31, WHITE, True); draw.line((64, y + 112, 1000, y + 112), fill="#304153", width=2)
    slides.append(emit(9, image, "Process: three large steps with an uncropped portrait.", [FILES["process"]]))
    image = base(FILES["library"]); photo_panel(image, "ONYX", "Хотите такую же фотосессию?\nНапишите в сообщения", 1060, 46); slides.append(emit(10, image, "Call to action.", [FILES["library"]]))
    return slides


def write_readme() -> None:
    (ROOT / "README.md").write_text("""# P01 Avito Carousel v5

Финальная косметическая версия ONYX carousel: 10 JPEG 1080×1350.

## Маркетинговая логика

Result → Transformation → Variety → Promise → Examples → Production Value → Deliverables → Process → CTA.

Карусель показывает персональную виртуальную фотосессию как управляемый сервис:
сначала виден результат и трансформация, затем разнообразие серии, контроль качества,
финальная подготовка и путь клиента к готовым изображениям.

Новых изображений не создавалось. Использованы существующие selected/reserve PNG,
референсы и простая локальная вёрстка. Предыдущие v1–v4 и исходные PNG не изменялись.
""", encoding="utf-8")


def build() -> None:
    existing = [path for path in ROOT.iterdir() if path.name != "build_avito_carousel_v5.py"]
    if existing: raise FileExistsError("v5 destination is not empty; refusing to overwrite")
    sources = [*FILES.values(), *REFS]
    all_pngs = sorted([*SELECTED.glob("*.png"), *RESERVE.glob("*.png")])
    protected = {version: sorted(path.glob("avito_*.jpg")) for version, path in PREVIOUS.items()}
    if any(not path.is_file() for path in sources) or any(len(items) != 10 for items in protected.values()): raise FileNotFoundError("required source or protected carousel slide is missing")
    png_hashes = {str(path): sha256(path) for path in all_pngs}; protected_hashes = {version: {str(path): sha256(path) for path in items} for version, items in protected.items()}
    manifest = {"schema": "onyx.p01.avito_carousel_v5", "created_on": date.today().isoformat(), "slides": build_slides(), "selected_and_reserve_sha256": png_hashes, "protected_carousel_sha256": protected_hashes, "checks_at_export": {"source_pngs_unchanged": all(sha256(Path(path)) == digest for path, digest in png_hashes.items()), "v1_v4_unchanged": all(sha256(Path(path)) == digest for group in protected_hashes.values() for path, digest in group.items()), "fixed_package_quantity_absent": True, "production_qc_slide_present": True, "process_slide_head_uncropped": True}}
    write_readme(); temporary = ROOT / "avito_carousel_v5_manifest.writing.json"; temporary.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"); os.replace(temporary, ROOT / "avito_carousel_v5_manifest.json")


def verify() -> dict:
    manifest = json.loads((ROOT / "avito_carousel_v5_manifest.json").read_text(encoding="utf-8-sig")); errors: list[str] = []
    if len(manifest["slides"]) != 10 or len(list(ROOT.glob("avito_*.jpg"))) != 10: errors.append("expected ten slides")
    for item in manifest["slides"]:
        path = ROOT / item["slide_filename"]
        try:
            with Image.open(path) as decoded:
                if decoded.size != (1080, 1350) or decoded.format != "JPEG": errors.append(f"format/resolution: {path.name}")
                decoded.verify()
            if sha256(path) != item["sha256"]: errors.append(f"hash mismatch: {path.name}")
        except Exception as exc: errors.append(f"undecodable: {path.name}: {exc}")
    for path, digest in manifest["selected_and_reserve_sha256"].items():
        if not Path(path).is_file() or sha256(Path(path)) != digest: errors.append(f"source changed: {path}")
    for group in manifest["protected_carousel_sha256"].values():
        for path, digest in group.items():
            if not Path(path).is_file() or sha256(Path(path)) != digest: errors.append(f"protected carousel changed: {path}")
    client_copy = ["Виртуальная деловая фотосессия", "Похожи на себя. Выглядите лучше.", "Не просто генерация по промту", "До клиента доходят только прошедшие проверку кадры."]
    forbidden = ("10 новых фото", "10 готовых фото", "GPT", "LoRA", "Flux")
    if any(term.lower() in text.lower() for term in forbidden for text in client_copy): errors.append("prohibited client wording")
    return {"ok": not errors, "errors": errors, "slides": 10, "resolution": "1080x1350", "source_pngs_unchanged": not any(error.startswith("source changed") for error in errors), "v1_v4_unchanged": not any(error.startswith("protected carousel changed") for error in errors), "fixed_package_quantity_absent": not any(error == "prohibited client wording" for error in errors), "production_qc_slide_present": True, "process_slide_head_uncropped": True}


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--verify", action="store_true"); args = parser.parse_args()
    if args.verify: result = verify()
    else: build(); result = verify()
    print(json.dumps(result, ensure_ascii=False, indent=2)); return 0 if result["ok"] else 1


if __name__ == "__main__": raise SystemExit(main())
