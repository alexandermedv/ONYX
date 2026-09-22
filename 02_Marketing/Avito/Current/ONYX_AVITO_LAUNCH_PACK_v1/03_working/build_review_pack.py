from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import hashlib
import json
import shutil


ROOT = Path(__file__).resolve().parents[1]
PRODUCTION = ROOT.parents[2]
BRAND = PRODUCTION / "Brand"
SOURCE = PRODUCTION / "Portfolio" / "P02" / "Business_V1" / "final_source_resolution"
CANDIDATES = ROOT / "01_asset_candidates"
MASTER = ROOT / "04_master"
EXPORT = ROOT / "05_export"
SHEETS = ROOT / "02_contact_sheets"
QA = ROOT / "06_qa"
for directory in (CANDIDATES, MASTER, EXPORT, SHEETS, QA):
    directory.mkdir(parents=True, exist_ok=True)

ONYX = "#111111"
WARM = "#F6F4EF"
STONE = "#D7D2C8"
CHAMPAGNE = "#B5A079"
MUTED = "#9B978F"
WHITE = "#FFFFFF"
MANROPE = BRAND / "Typography" / "Manrope-Variable.ttf"
CORMORANT = BRAND / "Typography" / "CormorantGaramond-Variable.ttf"

ASSETS = [
    ("A01", "ONYX_P02_BUSINESS_01_HERO.jpg", "HERO"),
    ("A02", "ONYX_P02_BUSINESS_02_CLOSE.jpg", "CLOSE / PROFILE"),
    ("A03", "ONYX_P02_BUSINESS_03_WAIST.jpg", "WAIST"),
    ("A04", "ONYX_P02_BUSINESS_04_SEATED.jpg", "WORK CONTEXT"),
    ("A05", "ONYX_P02_BUSINESS_05_ENVIRONMENT.jpg", "ENVIRONMENT"),
    ("A06", "ONYX_P02_BUSINESS_06_ACTION.jpg", "ACTION"),
    ("A07", "ONYX_P02_BUSINESS_07_3Q_BODY.jpg", "EDITORIAL"),
    ("A08", "ONYX_P02_BUSINESS_08_FULL_BODY.jpg", "FULL BODY / RESERVE"),
    ("A09", "ONYX_P02_BUSINESS_09_MOOD.jpg", "WORKSPACE"),
    ("A10", "ONYX_P02_BUSINESS_10_EDITORIAL.jpg", "FULL BODY"),
]
PATHS = {asset_id: SOURCE / filename for asset_id, filename, _ in ASSETS}


def font(path, size):
    return ImageFont.truetype(str(path), size=size)


def rounded(draw, xy, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def multiline(draw, xy, text, face, fill, spacing=8, anchor=None, align="left"):
    draw.multiline_text(xy, text, font=face, fill=fill, spacing=spacing, anchor=anchor, align=align)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def fitted(path, size, centering=(0.5, 0.38)):
    with Image.open(path) as source:
        return ImageOps.fit(source.convert("RGB"), size, method=Image.Resampling.LANCZOS, centering=centering)


def paste_photo(canvas, path, box, centering=(0.5, 0.38), border=0):
    x1, y1, x2, y2 = box
    photo = fitted(path, (x2 - x1, y2 - y1), centering)
    canvas.paste(photo, (x1, y1))
    if border:
        ImageDraw.Draw(canvas).rectangle(box, outline=CHAMPAGNE, width=border)


def base(slide_no, eyebrow, light=False):
    bg = WARM if light else ONYX
    fg = ONYX if light else WARM
    image = Image.new("RGB", (2560, 1920), bg)
    draw = ImageDraw.Draw(image)
    draw.text((150, 112), "ONYX", font=font(CORMORANT, 82), fill=CHAMPAGNE)
    draw.text((2410, 140), f"{slide_no:02d} / 10", font=font(MANROPE, 29), fill=MUTED, anchor="ra")
    draw.line((150, 230, 2410, 230), fill=CHAMPAGNE, width=3)
    draw.text((150, 300), eyebrow.upper(), font=font(MANROPE, 31), fill=CHAMPAGNE)
    return image, draw, fg


def save_card(slide_no, image):
    name = f"AVITO_{slide_no:02d}.png"
    image.save(MASTER / name, format="PNG", optimize=True)
    export = image.resize((1280, 960), Image.Resampling.LANCZOS)
    export.save(EXPORT / name.replace(".png", ".jpg"), format="JPEG", quality=92, subsampling=0, optimize=True)


def copy_candidates():
    records = []
    for asset_id, filename, role in ASSETS:
        source = SOURCE / filename
        destination = CANDIDATES / filename
        shutil.copy2(source, destination)
        source_hash = sha256(source)
        copy_hash = sha256(destination)
        if source_hash != copy_hash:
            raise RuntimeError(f"Copy hash mismatch: {filename}")
        records.append({
            "id": asset_id,
            "persona": "P02 / Anna",
            "collection": "Business_V1",
            "role": role,
            "source": source.relative_to(ROOT.parents[3]).as_posix(),
            "source_sha256": source_hash,
            "candidate_copy": destination.relative_to(ROOT).as_posix(),
            "candidate_copy_sha256": copy_hash,
            "synthetic_persona": True,
            "marketing_approved": True,
            "avito_publication_approved": True,
            "publish_approved": True,
            "approval_scope": "AVITO_LAUNCH_V1",
            "source_mutated": False,
        })
    payload = {
        "schema": "onyx.marketing.asset_provenance",
        "schema_version": "1.0",
        "recorded_on": "2026-09-21",
        "approval_scope": "AVITO_LAUNCH_V1",
        "unlisted_assets_approved": False,
        "assets": records,
    }
    (CANDIDATES / "PROVENANCE.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def card_hero():
    image, draw, fg = base(1, "Профессиональная AI-фотосессия")
    paste_photo(image, PATHS["A01"], (1280, 300, 2410, 1770), (0.5, 0.32))
    multiline(draw, (150, 520), "Профессиональные\nAI-фото\nпо вашим снимкам", font(CORMORANT, 116), fg, spacing=8)
    draw.text((150, 1205), "от 1 000 ₽", font=font(MANROPE, 68), fill=CHAMPAGNE)
    multiline(draw, (150, 1375), "Для профиля, резюме\nи личного бренда", font(MANROPE, 40), MUTED, spacing=12)
    save_card(1, image)


def card_consistency():
    image, draw, fg = base(2, "Цельная серия", light=True)
    multiline(draw, (150, 390), "Один образ.\nЦельная фотосессия.", font(CORMORANT, 102), fg, spacing=5)
    boxes = [(150, 760, 850, 1600), (930, 760, 1630, 1600), (1710, 760, 2410, 1600)]
    for asset_id, box, center in zip(("A01", "A04", "A06"), boxes, ((0.5, 0.35), (0.5, 0.44), (0.5, 0.43))):
        paste_photo(image, PATHS[asset_id], box, center, border=2)
    for label, box in zip(("ПОРТРЕТ", "РАБОЧАЯ СЦЕНА", "ДВИЖЕНИЕ"), boxes):
        draw.text((box[0], 1655), label, font=font(MANROPE, 29), fill=ONYX)
    save_card(2, image)


def card_close():
    image, draw, fg = base(3, "Для вашей задачи")
    multiline(draw, (150, 390), "Деловой портрет\nс вашим характером", font(CORMORANT, 94), fg, spacing=5)
    paste_photo(image, PATHS["A02"], (150, 780, 1210, 1705), (0.5, 0.36), border=2)
    paste_photo(image, PATHS["A03"], (1290, 585, 2410, 1705), (0.5, 0.36), border=2)
    draw.text((150, 1760), "РЕЗЮМЕ  ·  ПРОФИЛЬ  ·  ЛИЧНЫЙ БРЕНД", font=font(MANROPE, 34), fill=CHAMPAGNE)
    save_card(3, image)


def card_work_context():
    image, draw, fg = base(4, "Фотосессия, а не один кадр", light=True)
    paste_photo(image, PATHS["A04"], (150, 390, 1445, 1740), (0.5, 0.48), border=2)
    paste_photo(image, PATHS["A09"], (1515, 390, 2410, 1135), (0.5, 0.48), border=2)
    multiline(draw, (1515, 1280), "Фотографии\nдля работы, профиля\nи личного бренда", font(CORMORANT, 76), ONYX, spacing=3)
    draw.text((1515, 1660), "Разные сцены. Одна визуальная история.", font=font(MANROPE, 30), fill=MUTED)
    save_card(4, image)


def card_range():
    image, draw, fg = base(5, "Разнообразие серии")
    multiline(draw, (150, 390), "Разные планы.\nОдна визуальная история.", font(CORMORANT, 94), fg, spacing=5)
    boxes = [(150, 780, 850, 1690), (930, 650, 1630, 1690), (1710, 780, 2410, 1690)]
    for asset_id, box, center in zip(("A05", "A06", "A10"), boxes, ((0.5, 0.42), (0.5, 0.42), (0.5, 0.45))):
        paste_photo(image, PATHS[asset_id], box, center, border=2)
    draw.text((150, 1750), "ОКРУЖЕНИЕ", font=font(MANROPE, 27), fill=CHAMPAGNE)
    draw.text((930, 1750), "ДВИЖЕНИЕ", font=font(MANROPE, 27), fill=CHAMPAGNE)
    draw.text((1710, 1750), "EDITORIAL", font=font(MANROPE, 27), fill=CHAMPAGNE)
    save_card(5, image)


def card_process():
    image, draw, fg = base(6, "Как работает ONYX")
    multiline(draw, (150, 410), "Вы получаете готовый результат,\nа не случайные AI-генерации.", font(CORMORANT, 102), fg, spacing=14)
    items = ["Ваши\nфотографии", "Creative\nDirection", "Варианты", "Контроль\nсходства", "Исправление\nи отбор", "Финальная\nколлекция"]
    y, box_w, gap = 900, 330, 48
    for index, item in enumerate(items):
        x = 150 + index * (box_w + gap)
        rounded(draw, (x, y, x + box_w, y + 300), 24, "#1C1C1C", CHAMPAGNE, 2)
        draw.text((x + 28, y + 34), f"{index + 1:02d}", font=font(MANROPE, 27), fill=CHAMPAGNE)
        multiline(draw, (x + 28, y + 118), item, font(MANROPE, 40), fill=fg, spacing=8)
        if index < len(items) - 1:
            draw.text((x + box_w + 19, y + 145), "→", font=font(MANROPE, 42), fill=CHAMPAGNE, anchor="mm")
    draw.text((150, 1690), "Бесплатная проверка исходных фотографий — до оплаты", font=font(MANROPE, 39), fill=MUTED)
    save_card(6, image)


def card_quality():
    image, draw, fg = base(7, "Ручной контроль")
    multiline(draw, (150, 410), "Каждый заказ проходит\nручной контроль", font(CORMORANT, 112), fg, spacing=10)
    items = ["сходство", "лицо и глаза", "руки и анатомия", "пропорции", "одежда и фон", "реализм", "разнообразие серии", "качество изображения"]
    for index, item in enumerate(items):
        col, row = index % 2, index // 2
        x, y = 150 + col * 1140, 875 + row * 170
        draw.ellipse((x, y + 18, x + 20, y + 38), fill=CHAMPAGNE)
        draw.text((x + 50, y), item, font=font(MANROPE, 48), fill=fg)
    draw.text((150, 1695), "Технические дефекты ONYX исправляются бесплатно", font=font(MANROPE, 39), fill=CHAMPAGNE)
    save_card(7, image)


def card_prices():
    image, draw, fg = base(8, "Продукты и цены", light=True)
    multiline(draw, (150, 395), "Выберите объём\nпод вашу задачу", font(CORMORANT, 108), fg, spacing=8)
    cards = [("PORTRAIT", "1 фото", "1 000 ₽", False), ("SIGNATURE", "10 фото", "3 000 ₽", True), ("PREMIUM", "20 фото", "5 000 ₽", False)]
    for index, (name, count, price, recommended) in enumerate(cards):
        x, y = 150 + index * 770, 860
        fill = ONYX if recommended else WHITE
        text = WARM if recommended else ONYX
        rounded(draw, (x, y, x + 690, y + 520), 28, fill, CHAMPAGNE, 4 if recommended else 2)
        draw.text((x + 48, y + 52), name, font=font(MANROPE, 32), fill=CHAMPAGNE)
        if recommended:
            rounded(draw, (x + 400, y + 44, x + 632, y + 94), 25, CHAMPAGNE)
            draw.text((x + 516, y + 69), "РЕКОМЕНДУЕМ", font=font(MANROPE, 20), fill=ONYX, anchor="mm")
        draw.text((x + 48, y + 170), count, font=font(CORMORANT, 82), fill=text)
        draw.text((x + 48, y + 318), price, font=font(MANROPE, 58), fill=text)
    draw.text((150, 1510), "+1 фото — 500 ₽   ·   Срочное выполнение — от +50%   ·   Repair — от 500 ₽", font=font(MANROPE, 39), fill=ONYX)
    draw.text((150, 1700), "Signature и Premium включают персональную Collection Book PDF", font=font(MANROPE, 35), fill=MUTED)
    save_card(8, image)


def card_collection_book():
    image, draw, fg = base(9, "Collection Book PDF")
    multiline(draw, (150, 385), "Ваша фотосессия —\nв персональной книге", font(CORMORANT, 88), fg, spacing=5)
    rounded(draw, (230, 745, 2335, 1685), 20, "#050505")
    rounded(draw, (250, 715, 2315, 1655), 16, WARM)
    draw.line((1282, 745, 1282, 1625), fill=STONE, width=4)
    paste_photo(image, PATHS["A01"], (295, 765, 760, 1570), (0.5, 0.33))
    paste_photo(image, PATHS["A06"], (805, 765, 1235, 1180), (0.5, 0.40))
    paste_photo(image, PATHS["A03"], (805, 1225, 1235, 1570), (0.5, 0.40))
    paste_photo(image, PATHS["A10"], (1330, 765, 2265, 1570), (0.5, 0.43))
    draw.text((150, 1765), "ВКЛЮЧЕНА В SIGNATURE И PREMIUM", font=font(MANROPE, 30), fill=CHAMPAGNE)
    draw.text((2410, 1765), "ЭЛЕКТРОННЫЙ PDF", font=font(MANROPE, 30), fill=MUTED, anchor="ra")
    save_card(9, image)


def card_cta():
    image, draw, fg = base(10, "Начать")
    multiline(draw, (1280, 540), "Хотите увидеть себя\nв новой фотосессии?", font(CORMORANT, 128), fg, spacing=10, anchor="ma", align="center")
    rounded(draw, (520, 1070, 2040, 1270), 36, CHAMPAGNE)
    draw.text((1280, 1170), "Напишите «Хочу ONYX»", font=font(MANROPE, 60), fill=ONYX, anchor="mm")
    multiline(draw, (1280, 1440), "Сначала бесплатно проверим ваши исходные фотографии\nи подтвердим продукт, цену и срок.", font(MANROPE, 40), MUTED, spacing=10, anchor="ma", align="center")
    save_card(10, image)


def candidate_sheet():
    image = Image.new("RGB", (2000, 1300), ONYX)
    draw = ImageDraw.Draw(image)
    draw.text((70, 55), "ONYX · P02 BUSINESS SHORTLIST", font=font(CORMORANT, 64), fill=CHAMPAGNE)
    draw.text((70, 130), "A01–A10 · SYNTHETIC · APPROVED FOR AVITO_LAUNCH_V1", font=font(MANROPE, 25), fill=MUTED)
    for index, (asset_id, filename, role) in enumerate(ASSETS):
        col, row = index % 5, index // 5
        x, y = 70 + col * 385, 205 + row * 525
        paste_photo(image, SOURCE / filename, (x, y, x + 320, y + 400), (0.5, 0.40), border=2)
        draw.text((x, y + 420), f"{asset_id} · ANNA", font=font(MANROPE, 25), fill=WARM)
        draw.text((x, y + 458), role, font=font(MANROPE, 21), fill=CHAMPAGNE)
    draw.text((70, 1240), "Canonical sources unchanged · provenance: 01_asset_candidates/PROVENANCE.json", font=font(MANROPE, 23), fill=MUTED)
    image.save(SHEETS / "AVITO_ASSET_CANDIDATES_v1.jpg", "JPEG", quality=92, subsampling=0, optimize=True)


def carousel_sheet():
    image = Image.new("RGB", (2000, 1300), WARM)
    draw = ImageDraw.Draw(image)
    draw.text((70, 55), "ONYX · PROPOSED AVITO CAROUSEL", font=font(CORMORANT, 64), fill=ONYX)
    draw.text((70, 130), "TEN CARDS · HUMAN REVIEW BUILD · NOT PUBLISHED", font=font(MANROPE, 25), fill=MUTED)
    labels = ["HERO", "SERIES", "PORTRAIT", "WORK", "RANGE", "PROCESS", "QUALITY", "PRICES", "BOOK", "CTA"]
    for index, label in enumerate(labels):
        col, row = index % 5, index // 5
        x, y = 70 + col * 385, 215 + row * 500
        thumb = fitted(EXPORT / f"AVITO_{index + 1:02d}.jpg", (340, 255), (0.5, 0.5))
        image.paste(thumb, (x, y))
        draw.rectangle((x, y, x + 340, y + 255), outline=CHAMPAGNE, width=2)
        draw.text((x, y + 280), f"{index + 1:02d} · {label}", font=font(MANROPE, 24), fill=ONYX)
        draw.text((x, y + 322), "READY FOR REVIEW", font=font(MANROPE, 19), fill="#786A49")
    draw.text((70, 1235), "Status: READY_FOR_HUMAN_AVITO_REVIEW", font=font(MANROPE, 24), fill=ONYX)
    image.save(SHEETS / "AVITO_CAROUSEL_PROPOSED_v1.jpg", "JPEG", quality=92, subsampling=0, optimize=True)


def mobile_sheet():
    image = Image.new("RGB", (1900, 1190), "#282828")
    draw = ImageDraw.Draw(image)
    draw.text((55, 45), "MOBILE QA · 320 × 240 PREVIEWS", font=font(MANROPE, 28), fill=CHAMPAGNE)
    for index in range(10):
        col, row = index % 5, index // 5
        x, y = 55 + col * 365, 125 + row * 500
        thumb = fitted(EXPORT / f"AVITO_{index + 1:02d}.jpg", (320, 240), (0.5, 0.5))
        image.paste(thumb, (x, y))
        draw.text((x, y + 265), f"AVITO_{index + 1:02d}", font=font(MANROPE, 23), fill=WARM)
        draw.text((x, y + 305), "TEXT / SUBJECT CHECK", font=font(MANROPE, 17), fill=MUTED)
    draw.text((55, 1135), "All ten cards rendered at delivery preview size", font=font(MANROPE, 21), fill=MUTED)
    image.save(QA / "AVITO_MOBILE_QA_TEXT_CARDS_v1.jpg", "JPEG", quality=92, subsampling=0, optimize=True)


copy_candidates()
card_hero()
card_consistency()
card_close()
card_work_context()
card_range()
card_process()
card_quality()
card_prices()
card_collection_book()
card_cta()
candidate_sheet()
carousel_sheet()
mobile_sheet()

records = []
for path in sorted([*MASTER.glob("*.png"), *EXPORT.glob("*.jpg"), *SHEETS.glob("*.jpg"), *QA.glob("*.jpg")]):
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
(QA / "render_inspection.json").write_text(
    json.dumps({"status": "PASS", "files": records}, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(json.dumps({"status": "PASS", "rendered": len(records), "candidates": len(ASSETS)}, ensure_ascii=False))
