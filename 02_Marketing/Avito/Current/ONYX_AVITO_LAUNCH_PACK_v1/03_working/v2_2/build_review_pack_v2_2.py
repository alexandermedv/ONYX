from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import hashlib
import json
import math
import shutil


ROOT = Path(__file__).resolve().parents[2]
PRODUCTION = ROOT.parents[2]
BRAND = PRODUCTION / "Brand"
V21_MASTER = ROOT / "04_master" / "v2_1"
V21_EXPORT = ROOT / "05_export" / "v2_1"
MASTER = ROOT / "04_master" / "v2_2"
EXPORT = ROOT / "05_export" / "v2_2"
SHEETS = ROOT / "02_contact_sheets"
QA = ROOT / "06_qa" / "v2_2"
ASSET_A03 = ROOT / "01_asset_candidates" / "ONYX_P02_BUSINESS_03_WAIST.jpg"

for directory in (MASTER, EXPORT, SHEETS, QA):
    directory.mkdir(parents=True, exist_ok=True)

ONYX = "#111111"
CARBON = "#242424"
WARM = "#F6F4EF"
STONE = "#D8D3CA"
CHAMPAGNE = "#B5A079"
MUTED = "#77736D"
MANROPE = BRAND / "Typography" / "Manrope-Variable.ttf"
CORMORANT = BRAND / "Typography" / "CormorantGaramond-Variable.ttf"


def font(path, size):
    return ImageFont.truetype(str(path), size=size)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def fitted(path, size, centering=(0.5, 0.38)):
    with Image.open(path) as source:
        return ImageOps.fit(source.convert("RGB"), size, Image.Resampling.LANCZOS, centering=centering)


def multiline(draw, xy, text, text_font, fill, spacing=4):
    draw.multiline_text(xy, text, font=text_font, fill=fill, spacing=spacing)


def star(draw, center, outer_radius, inner_radius, fill):
    points = []
    for index in range(10):
        angle = -math.pi / 2 + index * math.pi / 5
        radius = outer_radius if index % 2 == 0 else inner_radius
        points.append((center[0] + math.cos(angle) * radius, center[1] + math.sin(angle) * radius))
    draw.polygon(points, fill=fill)


def base(slide, light=False):
    background = WARM if light else ONYX
    foreground = ONYX if light else WARM
    image = Image.new("RGB", (2560, 1920), background)
    draw = ImageDraw.Draw(image)
    draw.text((135, 82), "ONYX", font=font(CORMORANT, 84), fill=CHAMPAGNE)
    draw.text((2425, 115), f"{slide:02d} / 10", font=font(MANROPE, 30), fill=MUTED, anchor="ra")
    draw.line((135, 205, 2425, 205), fill=CHAMPAGNE, width=3)
    return image, draw, foreground


def save_card(slide, image):
    stem = f"AVITO_V2_2_{slide:02d}"
    image.save(MASTER / f"{stem}.png", "PNG", optimize=True)
    image.resize((1280, 960), Image.Resampling.LANCZOS).save(
        EXPORT / f"{stem}.jpg", "JPEG", quality=92, subsampling=0, optimize=True
    )


def copy_unchanged_cards():
    for slide in (1, 2, 6, 7, 9, 10):
        shutil.copy2(
            V21_MASTER / f"AVITO_V2_1_{slide:02d}.png",
            MASTER / f"AVITO_V2_2_{slide:02d}.png",
        )
        shutil.copy2(
            V21_EXPORT / f"AVITO_V2_1_{slide:02d}.jpg",
            EXPORT / f"AVITO_V2_2_{slide:02d}.jpg",
        )


def collections_card():
    image, draw, foreground = base(3)
    multiline(draw, (135, 305), "Выберите свою\nколлекцию", font(CORMORANT, 110), foreground, spacing=0)
    multiline(
        draw,
        (135, 670),
        "Направление фотосессии\nпод вашу задачу и образ",
        font(MANROPE, 42),
        STONE,
        spacing=10,
    )
    draw.rounded_rectangle((135, 990, 1350, 1490), radius=30, fill=CARBON, outline=CHAMPAGNE, width=3)
    draw.text((195, 1050), "ДОСТУПНО НА SOFT LAUNCH", font=font(MANROPE, 28), fill=CHAMPAGNE)
    draw.text((195, 1175), "Business", font=font(CORMORANT, 106), fill=WARM)
    draw.text((195, 1380), "Профиль · резюме · личный бренд", font=font(MANROPE, 35), fill=STONE)
    multiline(
        draw,
        (135, 1605),
        "Другие направления подтверждаем\nиндивидуально до оплаты",
        font(MANROPE, 34),
        MUTED,
        spacing=6,
    )
    image.paste(fitted(ASSET_A03, (875, 1400), (0.5, 0.38)), (1550, 310))
    draw.rectangle((1550, 310, 2425, 1710), outline=CHAMPAGNE, width=3)
    draw.text((1550, 1760), "ВИЗУАЛЬНЫЙ ПРИМЕР · BUSINESS", font=font(MANROPE, 27), fill=CHAMPAGNE)
    save_card(3, image)


def range_card():
    with Image.open(V21_MASTER / "AVITO_V2_1_04.png") as source:
        image = source.convert("RGB")
    draw = ImageDraw.Draw(image)
    draw.rectangle((120, 250, 2440, 625), fill=WARM)
    multiline(draw, (135, 305), "Разные ракурсы.\nОдин узнаваемый образ.", font(CORMORANT, 100), ONYX, spacing=2)
    save_card(4, image)


def scenes_card():
    with Image.open(V21_MASTER / "AVITO_V2_1_05.png") as source:
        image = source.convert("RGB")
    draw = ImageDraw.Draw(image)
    draw.rectangle((1910, 1040, 2440, 1810), fill=ONYX)
    multiline(draw, (1950, 1130), "Разные\nсцены.\nОдна цельная\nфотосессия.", font(CORMORANT, 66), WARM, spacing=0)
    save_card(5, image)


def pricing_card():
    image, draw, foreground = base(8, light=True)
    draw.text((135, 285), "Можно начать с 1 фото", font=font(CORMORANT, 100), fill=foreground)
    draw.text((135, 465), "Portrait 1 000 ₽  →  Signature 3 000 ₽", font=font(MANROPE, 58), fill=ONYX)
    draw.rounded_rectangle((135, 555, 1100, 680), radius=28, fill=CHAMPAGNE)
    draw.text((617, 617), "ДОПЛАТА 2 000 ₽", font=font(MANROPE, 48), fill=ONYX, anchor="mm")

    draw.rounded_rectangle((135, 800, 680, 1500), radius=30, fill="#FFFFFF", outline=STONE, width=3)
    draw.text((185, 855), "PORTRAIT", font=font(MANROPE, 46), fill=MUTED)
    draw.text((185, 1015), "1 фото", font=font(CORMORANT, 78), fill=ONYX)
    draw.text((185, 1245), "1 000 ₽", font=font(MANROPE, 64), fill=ONYX)

    draw.rounded_rectangle((765, 720, 1795, 1570), radius=34, fill=ONYX, outline=CHAMPAGNE, width=5)
    draw.rounded_rectangle((1350, 770, 1715, 850), radius=40, fill=CHAMPAGNE)
    draw.text((1532, 810), "РЕКОМЕНДУЕМ", font=font(MANROPE, 25), fill=ONYX, anchor="mm")
    draw.text((835, 790), "SIGNATURE", font=font(MANROPE, 46), fill=CHAMPAGNE)
    star(draw, (1105, 812), 23, 10, CHAMPAGNE)
    draw.text((835, 1000), "10 фото", font=font(CORMORANT, 106), fill=WARM)
    draw.text((835, 1240), "3 000 ₽", font=font(MANROPE, 84), fill=WARM)
    draw.text((835, 1450), "Полная фотосессия", font=font(MANROPE, 38), fill=STONE)

    draw.rounded_rectangle((1880, 800, 2425, 1500), radius=30, fill="#FFFFFF", outline=STONE, width=3)
    draw.text((1930, 855), "PREMIUM", font=font(MANROPE, 46), fill=MUTED)
    draw.text((1930, 1015), "20 фото", font=font(CORMORANT, 78), fill=ONYX)
    draw.text((1930, 1245), "5 000 ₽", font=font(MANROPE, 64), fill=ONYX)

    draw.text((135, 1730), "Стоимость Portrait засчитаем полностью", font=font(MANROPE, 42), fill=MUTED)
    save_card(8, image)


def contact_sheet():
    image = Image.new("RGB", (2000, 1300), WARM)
    draw = ImageDraw.Draw(image)
    draw.text((70, 55), "ONYX · AVITO CAROUSEL FINAL REVIEW V2.2", font=font(CORMORANT, 62), fill=ONYX)
    draw.text((70, 130), "COLLECTION CHOICE · PORTRAIT → SIGNATURE UPGRADE", font=font(MANROPE, 25), fill=MUTED)
    labels = ["HERO", "BEFORE → AFTER", "COLLECTIONS", "IDENTITY / RANGE", "SCENES", "PROCESS", "QUALITY", "PRICING + UPGRADE", "BOOK", "CTA"]
    changed = {3, 4, 5, 8}
    for index, label in enumerate(labels, start=1):
        col, row = (index - 1) % 5, (index - 1) // 5
        x, y = 70 + col * 385, 215 + row * 500
        with Image.open(EXPORT / f"AVITO_V2_2_{index:02d}.jpg") as card:
            thumb = card.convert("RGB").resize((340, 255), Image.Resampling.LANCZOS)
        image.paste(thumb, (x, y))
        draw.rectangle((x, y, x + 340, y + 255), outline=CHAMPAGNE, width=2)
        draw.text((x, y + 280), f"{index:02d} · {label}", font=font(MANROPE, 22), fill=ONYX)
        draw.text((x, y + 320), "V2.2 UPDATE" if index in changed else "UNCHANGED FROM V2.1", font=font(MANROPE, 18), fill="#786A49")
    draw.text((70, 1235), "Status: READY_FOR_AVITO_PUBLISH_REVIEW", font=font(MANROPE, 23), fill=ONYX)
    image.save(SHEETS / "AVITO_CAROUSEL_FINAL_REVIEW_v2_2.jpg", "JPEG", quality=92, subsampling=0, optimize=True)


def mobile_sheet():
    image = Image.new("RGB", (1100, 1000), CARBON)
    draw = ImageDraw.Draw(image)
    draw.text((70, 35), "V2.2 MOBILE QA · EXACT 390 PX CARD PREVIEWS", font=font(MANROPE, 30), fill=CHAMPAGNE)
    for column, (slide, label) in enumerate(((3, "COLLECTIONS"), (8, "PRICING + UPGRADE"))):
        x, y = 70 + column * 500, 115
        with Image.open(EXPORT / f"AVITO_V2_2_{slide:02d}.jpg") as card:
            preview = card.convert("RGB").resize((390, 293), Image.Resampling.LANCZOS)
        image.paste(preview, (x, y))
        draw.rectangle((x, y, x + 390, y + 293), outline=CHAMPAGNE, width=2)
        draw.text((x, y + 315), f"{slide:02d} · {label}", font=font(MANROPE, 21), fill=WARM)
        draw.text((x, y + 350), "390 px · review without zoom", font=font(MANROPE, 17), fill=MUTED)

    draw.text((70, 520), "FULL SEQUENCE · 170 PX PREVIEWS", font=font(MANROPE, 23), fill=CHAMPAGNE)
    for index in range(1, 11):
        col, row = (index - 1) % 5, (index - 1) // 5
        x, y = 70 + col * 200, 575 + row * 160
        with Image.open(EXPORT / f"AVITO_V2_2_{index:02d}.jpg") as card:
            thumb = card.convert("RGB").resize((170, 128), Image.Resampling.LANCZOS)
        image.paste(thumb, (x, y))
        draw.rectangle((x, y, x + 170, y + 128), outline="#5E5647", width=1)
        draw.text((x + 6, y + 6), f"{index:02d}", font=font(MANROPE, 16), fill=WARM)
    image.save(QA / "AVITO_MOBILE_QA_v2_2.jpg", "JPEG", quality=92, subsampling=0, optimize=True)


def inspection():
    paths = [*sorted(MASTER.glob("AVITO_V2_2_*.png")), *sorted(EXPORT.glob("AVITO_V2_2_*.jpg"))]
    paths += [SHEETS / "AVITO_CAROUSEL_FINAL_REVIEW_v2_2.jpg", QA / "AVITO_MOBILE_QA_v2_2.jpg"]
    records = []
    for path in paths:
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            records.append({
                "path": path.relative_to(ROOT).as_posix(),
                "format": image.format,
                "width": image.width,
                "height": image.height,
                "mode": image.mode,
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            })
    (QA / "render_inspection_v2_2.json").write_text(
        json.dumps({"status": "PASS", "files": records}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": "PASS", "revision": "v2.2", "rendered": len(records)}, ensure_ascii=False))


copy_unchanged_cards()
collections_card()
range_card()
scenes_card()
pricing_card()
contact_sheet()
mobile_sheet()
inspection()
