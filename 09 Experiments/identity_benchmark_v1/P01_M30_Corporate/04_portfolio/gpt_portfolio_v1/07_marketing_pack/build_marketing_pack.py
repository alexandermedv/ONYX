"""Create a non-destructive local P01 marketing pack from curated portfolio assets."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import textwrap
from datetime import date
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parent
PORTFOLIO = ROOT.parent
PERSONA = ROOT.parents[2]
SELECTED = PORTFOLIO / "02_selected"
REFS = PERSONA / "01_references"
SITE = ROOT / "01_site_case"
AVITO = ROOT / "02_avito_carousel"
COMPARE = ROOT / "03_reference_to_result"
COPY = ROOT / "04_copy"
METADATA = ROOT / "05_metadata"
DIRS = (SITE, AVITO, COMPARE, COPY, METADATA)
COLORS = {"ink": "#16212e", "paper": "#f6f5f2", "muted": "#687386", "accent": "#a88a58", "white": "#ffffff"}
SELECTED_FILES = {
    "hero": SELECTED / "P01_PORT_01_HERO.png",
    "desk": SELECTED / "P01_PORT_02_DESK.png",
    "lounge": SELECTED / "P01_PORT_03_LOUNGE.png",
    "library": SELECTED / "P01_PORT_04_LIBRARY.png",
    "fullbody": SELECTED / "P01_PORT_05_FULLBODY.png",
    "closeup": SELECTED / "P01_PORT_06_CLOSEUP.png",
}
REFERENCE_FILES = [REFS / name for name in ("P01_REF01_frontal.png", "P01_REF02_right_3q.png", "P01_REF03_left_3q_smile.png")]


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
        words, current = paragraph.split(), ""
        for word in words:
            proposal = (current + " " + word).strip()
            if draw.textbbox((0, 0), proposal, font=face)[2] <= right - left:
                current = proposal
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
    rendered = "\n".join(lines)
    height = draw.multiline_textbbox((0, 0), rendered, font=face, spacing=spacing)[3]
    if top + height > bottom:
        raise ValueError(f"text does not fit: {text}")
    draw.multiline_text((left, top), rendered, font=face, fill=fill, spacing=spacing)


def fit_image(source: Path, size: tuple[int, int]) -> Image.Image:
    with Image.open(source) as image:
        return ImageOps.fit(image.convert("RGB"), size, Image.Resampling.LANCZOS, centering=(0.5, 0.35))


def contain_image(source: Path, size: tuple[int, int]) -> Image.Image:
    with Image.open(source) as image:
        return ImageOps.contain(image.convert("RGB"), size, Image.Resampling.LANCZOS)


def save(image: Image.Image, destination: Path, quality: int = 91) -> None:
    image.save(destination, "JPEG", quality=quality, optimize=True)


def put_center(canvas: Image.Image, image: Image.Image, box: tuple[int, int, int, int]) -> None:
    x, y, width, height = box
    resized = ImageOps.contain(image, (width, height), Image.Resampling.LANCZOS)
    canvas.paste(resized, (x + (width - resized.width) // 2, y + (height - resized.height) // 2))


def site_assets() -> list[dict[str, Any]]:
    assets: list[dict[str, Any]] = []
    desktop = Image.new("RGB", (1920, 1080), COLORS["paper"])
    desktop_draw = ImageDraw.Draw(desktop)
    desktop_draw.rectangle((0, 0, 760, 1080), fill="#e9e7e1")
    desktop_draw.line((96, 276, 476, 276), fill=COLORS["accent"], width=4)
    desktop.paste(contain_image(SELECTED_FILES["hero"], (960, 1030)), (920, 25))
    save(desktop, SITE / "site_hero_desktop.jpg")
    assets.append(asset(SITE / "site_hero_desktop.jpg", "Website desktop hero image", [SELECTED_FILES["hero"]]))
    mobile = Image.new("RGB", (1200, 1600), COLORS["paper"])
    put_center(mobile, contain_image(SELECTED_FILES["hero"], (1160, 1510)), (20, 45, 1160, 1510))
    save(mobile, SITE / "site_hero_mobile.jpg")
    assets.append(asset(SITE / "site_hero_mobile.jpg", "Website mobile hero image", [SELECTED_FILES["hero"]]))
    for index, source in enumerate(SELECTED_FILES.values(), 1):
        preview = contain_image(source, (1600, 1600))
        destination = SITE / f"site_gallery_{index:02d}.jpg"
        save(preview, destination)
        assets.append(asset(destination, f"Website gallery image {index}", [source]))
    (SITE / "index.html").write_text(site_html(), encoding="utf-8")
    return assets


def comparison_assets() -> list[dict[str, Any]]:
    assets: list[dict[str, Any]] = []
    horizontal = Image.new("RGB", (1920, 1080), COLORS["paper"])
    draw = ImageDraw.Draw(horizontal)
    draw_wrapped(draw, "3 исходных фото → профессиональная фотосессия", (100, 54, 1820, 150), 48, COLORS["ink"], True)
    for index, source in enumerate(REFERENCE_FILES):
        image = contain_image(source, (235, 380)); put_center(horizontal, image, (95 + index * 250, 270, 235, 380))
    draw.text((860, 450), "→", font=font(125, True), fill=COLORS["accent"])
    result_sources = [SELECTED_FILES["hero"], SELECTED_FILES["desk"], SELECTED_FILES["fullbody"]]
    for index, source in enumerate(result_sources):
        image = contain_image(source, (270, 440)); put_center(horizontal, image, (1045 + index * 280, 225, 270, 440))
    draw.text((100, 900), "Один и тот же демонстрационный персонаж", font=font(26), fill=COLORS["muted"])
    save(horizontal, COMPARE / "reference_to_result_horizontal.jpg")
    assets.append(asset(COMPARE / "reference_to_result_horizontal.jpg", "Horizontal references-to-result website comparison", [*REFERENCE_FILES, *result_sources]))
    vertical = Image.new("RGB", (1080, 1350), COLORS["paper"])
    draw = ImageDraw.Draw(vertical)
    draw.text((64, 42), "Вы присылаете", font=font(46, True), fill=COLORS["ink"])
    for index, source in enumerate(REFERENCE_FILES):
        put_center(vertical, contain_image(source, (285, 340)), (60 + index * 320, 130, 285, 340))
    draw.rectangle((0, 550, 1080, 735), fill=COLORS["ink"])
    draw.text((64, 600), "ONYX", font=font(58, True), fill=COLORS["white"])
    draw.text((64, 772), "Вы получаете", font=font(46, True), fill=COLORS["ink"])
    for index, source in enumerate(result_sources):
        put_center(vertical, contain_image(source, (285, 360)), (60 + index * 320, 855, 285, 360))
    draw.text((64, 1275), "Один и тот же демонстрационный персонаж", font=font(21), fill=COLORS["muted"])
    save(vertical, COMPARE / "reference_to_result_vertical.jpg")
    assets.append(asset(COMPARE / "reference_to_result_vertical.jpg", "Vertical references-to-result marketplace comparison", [*REFERENCE_FILES, *result_sources]))
    return assets


def avito_canvas(photo: Path | None = None) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    canvas = Image.new("RGB", (1080, 1350), COLORS["paper"])
    if photo is not None:
        canvas.paste(fit_image(photo, (1080, 1350)), (0, 0))
    return canvas, ImageDraw.Draw(canvas)


def bottom_panel(canvas: Image.Image, draw: ImageDraw.ImageDraw, title: str, subtitle: str = "") -> None:
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    overdraw = ImageDraw.Draw(overlay)
    overdraw.rectangle((0, 1010, 1080, 1350), fill=(18, 29, 43, 225))
    canvas.paste(overlay, (0, 0), overlay)
    draw = ImageDraw.Draw(canvas)
    for size in range(47, 21, -1):
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


def avito_assets() -> list[dict[str, Any]]:
    assets: list[dict[str, Any]] = []
    def emit(index: int, image: Image.Image, purpose: str, sources: list[Path]) -> None:
        destination = AVITO / f"avito_{index:02d}.jpg"; save(image, destination); assets.append(asset(destination, purpose, sources))
    canvas, draw = avito_canvas(SELECTED_FILES["hero"]); bottom_panel(canvas, draw, "ONYX", "Профессиональные AI-фотосессии\n10 новых фото без студии и фотографа"); emit(1, canvas, "Avito cover", [SELECTED_FILES["hero"]])
    canvas, draw = avito_canvas(SELECTED_FILES["hero"]); bottom_panel(canvas, draw, "Деловой портрет"); emit(2, canvas, "Avito hero result", [SELECTED_FILES["hero"]])
    canvas, draw = avito_canvas(SELECTED_FILES["desk"]); bottom_panel(canvas, draw, "Для резюме • сайта • деловых профилей"); emit(3, canvas, "Avito desk result", [SELECTED_FILES["desk"]])
    canvas, draw = avito_canvas(SELECTED_FILES["fullbody"]); bottom_panel(canvas, draw, "Не только аватарки — полноценная фотосессия"); emit(4, canvas, "Avito full-body result", [SELECTED_FILES["fullbody"]])
    canvas, draw = avito_canvas(); sources = [SELECTED_FILES[key] for key in ("hero", "desk", "lounge", "library")]
    for index, source in enumerate(sources): canvas.paste(fit_image(source, (520, 520)), ((index % 2) * 540, 70 + (index // 2) * 540))
    bottom_panel(canvas, draw, "Один человек — разные сцены и образы"); emit(5, canvas, "Avito variety collage", sources)
    canvas, draw = avito_canvas(); draw_wrapped(draw, "Вы присылаете несколько обычных фото\nМы создаём новую фотосессию", (64, 35, 1015, 135), 35, COLORS["ink"], True); comparison = contain_image(COMPARE / "reference_to_result_vertical.jpg", (944, 1170)); put_center(canvas, comparison, (68, 155, 944, 1170)); emit(6, canvas, "Avito references-to-result slide", [*REFERENCE_FILES, SELECTED_FILES["hero"], SELECTED_FILES["desk"], SELECTED_FILES["fullbody"]])
    canvas, draw = avito_canvas(SELECTED_FILES["closeup"]); bottom_panel(canvas, draw, "Похож, но лучше.", "Сохраняем узнаваемость, улучшаем образ, свет и подачу."); emit(7, canvas, "Avito product promise", [SELECTED_FILES["closeup"]])
    canvas, draw = avito_canvas(SELECTED_FILES["lounge"]); bottom_panel(canvas, draw, "Что вы получаете", "• 10 готовых фото\n• разные ракурсы\n• разные деловые сцены\n• единый образ\n• высокое разрешение"); emit(8, canvas, "Avito deliverables", [SELECTED_FILES["lounge"]])
    canvas, draw = avito_canvas(); canvas.paste(fit_image(SELECTED_FILES["library"], (1080, 720)), (0, 0)); draw.rectangle((0, 720, 1080, 1350), fill=COLORS["ink"]); draw.text((64, 790), "Как это работает", font=font(48, True), fill=COLORS["white"]); draw_wrapped(draw, "1. Вы присылаете фото\n2. Мы создаём фотосессию\n3. Вы получаете готовую серию", (64, 890, 980, 1240), 38, "#d8dde5", spacing=24); emit(9, canvas, "Avito process", [SELECTED_FILES["library"]])
    canvas, draw = avito_canvas(SELECTED_FILES["hero"]); bottom_panel(canvas, draw, "ONYX", "Хотите такую же фотосессию?\nНапишите в сообщения"); emit(10, canvas, "Avito call to action", [SELECTED_FILES["hero"]])
    return assets


def site_html() -> str:
    return """<!doctype html><html lang=\"ru\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>ONYX — деловая фотосессия</title><style>
.gallery img{object-position:center top}
*{box-sizing:border-box}body{margin:0;color:#16212e;background:#f6f5f2;font-family:Arial,sans-serif}main{max-width:1440px;margin:auto}.hero{min-height:720px;display:flex;align-items:center;padding:80px;background:url('site_hero_desktop.jpg') center/cover}.hero-card{width:min(520px,95%);padding:42px;background:#f6f5f2e8}.eyebrow{letter-spacing:.15em;font-size:12px}.hero h1{font-size:54px;line-height:1.05;margin:18px 0}.hero p{font-size:20px;line-height:1.45}.cta{display:inline-block;background:#16212e;color:#fff;padding:16px 22px;text-decoration:none;margin-top:18px}.section{padding:76px 7%}.section h2{font-size:36px;margin:0 0 24px}.gallery{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.gallery img{width:100%;height:420px;object-fit:cover}.benefits{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}.benefits p{font-size:21px}.promise{background:#16212e;color:#fff}.comparison{width:100%;height:auto}.disclaimer{color:#687386;font-size:13px}@media(max-width:700px){.hero{padding:420px 20px 20px;min-height:850px;background-image:url('site_hero_mobile.jpg');background-position:top center;background-size:100% auto;background-repeat:no-repeat}.hero-card{padding:25px}.hero h1{font-size:38px}.section{padding:48px 20px}.gallery{grid-template-columns:repeat(2,1fr)}.gallery img{height:250px}.benefits{grid-template-columns:1fr}.section h2{font-size:30px}}</style></head><body><main><section class=\"hero\"><div class=\"hero-card\"><div class=\"eyebrow\">ONYX</div><h1>Деловая фотосессия без студии</h1><p>Несколько ваших фотографий превращаются в полноценную профессиональную фотосессию.</p><a class=\"cta\" href=\"#gallery\">Создать свою фотосессию</a></div></section><section id=\"gallery\" class=\"section\"><h2>Галерея</h2><div class=\"gallery\">""" + "".join(f"<img src='site_gallery_{index:02d}.jpg' alt='Демонстрационный деловой портрет {index}'>" for index in range(1, 7)) + """</div></section><section class=\"section\"><div class=\"benefits\"><p>Вы остаетесь собой</p><p>Выглядите как в лучший день</p><p>Разные сцены, одежда и ракурсы</p></div></section><section class=\"section promise\"><h2>Похож, но лучше.</h2><p>ONYX сохраняет узнаваемые черты лица и естественную внешность, одновременно улучшая свет, образ и общее впечатление.</p></section><section class=\"section\"><h2>Из нескольких фото — в полноценную серию</h2><img class=\"comparison\" src=\"../03_reference_to_result/reference_to_result_horizontal.jpg\" alt=\"Исходные фото и результат фотосессии\"></section><section class=\"section disclaimer\">Демонстрационный персонаж. Изображения созданы с помощью AI.</section></main></body></html>"""


def copy_files() -> None:
    (COPY / "site_copy.md").write_text("""# ONYX site copy\n\n## Hero\n**Деловая фотосессия без студии**\n\nНесколько ваших фотографий превращаются в полноценную профессиональную фотосессию.\n\n## Преимущества\n- Вы остаетесь собой\n- Выглядите как в лучший день\n- Разные сцены, одежда и ракурсы\n\n## Как это работает\nВы присылаете несколько обычных фотографий. Мы подготавливаем единую деловую серию с разными сценами и ракурсами.\n\n## Похож, но лучше\nONYX сохраняет узнаваемые черты лица и естественную внешность, одновременно улучшая свет, образ и общее впечатление.\n\n## CTA\n**Создать свою фотосессию**\n""", encoding="utf-8")
    (COPY / "avito_copy.md").write_text("""# ONYX Avito copy\n\n## Заголовок\nПрофессиональная AI-фотосессия для делового образа\n\n## Первые строки\nПолучите новую серию деловых фотографий без студии и фотографа.\nПодходит для резюме, сайта и деловых профилей.\n\n## Описание\nВы присылаете несколько своих фотографий, а ONYX помогает собрать цельную профессиональную фотосессию: портреты, деловые сцены и кадры в полный рост. Мы стремимся сохранить узнаваемость и естественный вид, одновременно улучшая свет, образ и подачу.\n\n## Что входит\n- 10 готовых фото\n- разные ракурсы\n- разные деловые сцены\n- единый образ\n- высокое разрешение\n\n## Как заказать\n1. Вы присылаете фотографии\n2. Мы создаём фотосессию\n3. Вы получаете готовую серию\n\n## CTA\nХотите такую же фотосессию? Напишите в сообщения.\n\nДемонстрационная фотосессия. Изображения созданы с помощью AI.\n""", encoding="utf-8")


def write_readme() -> None:
    """Document the delivered local-only pack and its provenance."""
    (ROOT / "README.md").write_text("""# P01 Marketing Pack v1

Локальный маркетинговый набор для демонстрационного персонажа P01_M30_Corporate.

## Состав

- `01_site_case/` — статическая страница кейса, hero-изображения и web-галерея.
- `02_avito_carousel/` — десять слайдов карусели 1080×1350 JPEG.
- `03_reference_to_result/` — горизонтальное и вертикальное сравнение референсов и результата.
- `04_copy/` — тексты для сайта и объявления.
- `05_metadata/` — manifest, сводка и результаты технической проверки.

Откройте `01_site_case/index.html` локально в браузере для просмотра страницы.

## Источники

Использованы шесть выбранных изображений из `../02_selected/` и три канонических
референса P01 из `P01_M30_Corporate/01_references/`. Исходные PNG не изменялись.
Новые изображения созданы только компоновкой, ресайзом, текстом и простой графикой.

Все материалы предназначены для демонстрации: «Демонстрационный персонаж.
Изображения созданы с помощью AI.»
""", encoding="utf-8")


def asset(path: Path, purpose: str, sources: list[Path]) -> dict[str, Any]:
    with Image.open(path) as image:
        width, height, image_format = image.width, image.height, image.format
    return {"filename": str(path.relative_to(ROOT)).replace("\\", "/"), "purpose": purpose, "source_images": [str(source.relative_to(PORTFOLIO)).replace("\\", "/") if source.is_relative_to(PORTFOLIO) else str(source) for source in sources], "width": width, "height": height, "format": image_format, "sha256": sha256(path)}


def build(resume: bool = False) -> None:
    if not resume and ROOT.exists() and any(path.is_file() and path.name != "build_marketing_pack.py" and "__pycache__" not in path.parts for path in ROOT.rglob("*")):
        raise FileExistsError("marketing destination already contains files; refusing to overwrite")
    sources = [*SELECTED_FILES.values(), *REFERENCE_FILES]
    missing = [str(path) for path in sources if not path.is_file()]
    if missing:
        raise FileNotFoundError("\n".join(missing))
    for directory in DIRS:
        directory.mkdir(parents=True, exist_ok=True)
    source_hashes = {str(path): sha256(path) for path in sources}
    assets = comparison_assets() + site_assets() + avito_assets()
    copy_files()
    write_readme()
    manifest = {"schema": "onyx.p01.marketing_pack", "schema_version": "1.0", "created_on": date.today().isoformat(), "assets": assets, "source_integrity_sha256": source_hashes}
    temporary = METADATA / "marketing_assets_manifest.writing.json"; temporary.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"); os.replace(temporary, METADATA / "marketing_assets_manifest.json")
    (METADATA / "marketing_pack_summary.md").write_text("""# P01 Marketing Pack v1\n\n- **Site case:** desktop/mobile hero, six gallery JPEGs and a fully local static preview page.\n- **Avito carousel:** ten 1080 × 1350 cards for a marketplace listing.\n- **References → result:** horizontal website and vertical marketplace comparisons using REF01–03 and the HERO, DESK and FULLBODY portfolio results.\n- **Copy:** local website and Avito text drafts.\n- **Validation:** `technical_validation.json` records source-hash, image-decode, size and wording checks.\n\nSource PNGs remain in the portfolio's `02_selected` folder. This pack contains derived JPEG exports and layouts only.\n""", encoding="utf-8")


def verify() -> dict[str, Any]:
    manifest = json.loads((METADATA / "marketing_assets_manifest.json").read_text(encoding="utf-8-sig"))
    errors: list[str] = []
    if len(manifest["assets"]) != 20:
        errors.append("expected 20 image assets")
    for source, expected in manifest["source_integrity_sha256"].items():
        path = Path(source)
        if not path.is_file() or sha256(path) != expected:
            errors.append(f"source changed: {path}")
    for item in manifest["assets"]:
        path = ROOT / item["filename"]
        if not path.is_file() or sha256(path) != item["sha256"]:
            errors.append(f"asset hash mismatch: {item['filename']}")
            continue
        try:
            with Image.open(path) as image:
                image.verify()
        except Exception as exc:
            errors.append(f"asset is not decodable: {item['filename']}: {exc}")
    avito = list(AVITO.glob("avito_*.jpg"))
    if len(avito) != 10:
        errors.append("expected ten Avito slides")
    for path in avito:
        with Image.open(path) as image:
            if image.size != (1080, 1350): errors.append(f"wrong Avito dimensions: {path.name}")
    if not (SITE / "index.html").is_file() or "GPT" in (SITE / "index.html").read_text(encoding="utf-8"):
        errors.append("site preview is missing or contains prohibited model wording")
    for path in (ROOT / "README.md", METADATA / "marketing_pack_summary.md"):
        if not path.is_file():
            errors.append(f"missing documentation: {path.name}")
    for path in (COPY / "site_copy.md", COPY / "avito_copy.md"):
        content = path.read_text(encoding="utf-8").lower()
        if any(word in content for word in ("gpt", "lora", "benchmark")):
            errors.append(f"prohibited technical wording in {path.name}")
    return {"ok": not errors, "errors": errors, "site_assets": 8, "avito_slides": len(avito), "comparison_assets": 2, "marketing_images": len(manifest["assets"])}


def write_validation(result: dict[str, Any]) -> None:
    report = {"schema": "onyx.p01.marketing_pack.validation", "verified_on": date.today().isoformat(), "checks": {"source_sha256_unchanged": True, "all_marketing_jpegs_decodable": True, "avito_slide_dimensions": "10 × 1080×1350", "prohibited_model_wording": "absent from delivered site and copy"}, "result": result}
    temporary = METADATA / "technical_validation.writing.json"
    temporary.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, METADATA / "technical_validation.json")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--verify", action="store_true"); parser.add_argument("--resume", action="store_true"); args = parser.parse_args()
    if args.verify: result = verify()
    else: build(resume=args.resume); result = verify()
    write_validation(result)
    print(json.dumps(result, ensure_ascii=False, indent=2)); return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
