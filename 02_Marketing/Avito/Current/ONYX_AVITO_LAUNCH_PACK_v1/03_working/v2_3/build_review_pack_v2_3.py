from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import hashlib
import json
import shutil


ROOT = Path(__file__).resolve().parents[2]
PRODUCTION = ROOT.parents[2]
BRAND = PRODUCTION / "Brand"
V22_MASTER = ROOT / "04_master" / "v2_2"
V22_EXPORT = ROOT / "05_export" / "v2_2"
MASTER = ROOT / "04_master" / "v2_3"
EXPORT = ROOT / "05_export" / "v2_3"
SHEETS = ROOT / "02_contact_sheets"
QA = ROOT / "06_qa" / "v2_3"

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


def copy_v22():
    for slide in range(1, 11):
        shutil.copy2(V22_MASTER / f"AVITO_V2_2_{slide:02d}.png", MASTER / f"AVITO_V2_3_{slide:02d}.png")
        shutil.copy2(V22_EXPORT / f"AVITO_V2_2_{slide:02d}.jpg", EXPORT / f"AVITO_V2_3_{slide:02d}.jpg")


def collections_card():
    image = Image.new("RGB", (2560, 1920), ONYX)
    draw = ImageDraw.Draw(image)
    draw.text((135, 82), "ONYX", font=font(CORMORANT, 84), fill=CHAMPAGNE)
    draw.text((2425, 115), "03 / 10", font=font(MANROPE, 30), fill=MUTED, anchor="ra")
    draw.line((135, 205, 2425, 205), fill=CHAMPAGNE, width=3)

    draw.multiline_text(
        (135, 300),
        "ВЫБЕРИТЕ НАПРАВЛЕНИЕ\nФОТОСЕССИИ",
        font=font(MANROPE, 76),
        fill=WARM,
        spacing=8,
    )
    draw.text((135, 525), "Подберём стиль под вашу задачу и образ", font=font(MANROPE, 38), fill=STONE)

    panels = (
        (135, 700, 1235, 1450, "BUSINESS", "Профиль · резюме ·\nличный бренд"),
        (1325, 700, 2425, 1450, "LIFESTYLE", "Соцсети · личный профиль ·\nповседневный образ"),
    )
    for left, top, right, bottom, title, description in panels:
        draw.rounded_rectangle((left, top, right, bottom), radius=34, fill=CARBON, outline=CHAMPAGNE, width=4)
        draw.text((left + 70, top + 75), title, font=font(MANROPE, 57), fill=CHAMPAGNE)
        draw.line((left + 70, top + 180, right - 70, top + 180), fill="#5E5647", width=2)
        draw.multiline_text((left + 70, top + 285), description, font=font(CORMORANT, 76), fill=WARM, spacing=16)

    draw.text((1280, 1650), "Другие направления — по согласованию", font=font(MANROPE, 36), fill=STONE, anchor="mm")
    master_path = MASTER / "AVITO_V2_3_03.png"
    export_path = EXPORT / "AVITO_V2_3_03.jpg"
    image.save(master_path, "PNG", optimize=True)
    image.resize((1280, 960), Image.Resampling.LANCZOS).save(export_path, "JPEG", quality=92, subsampling=0, optimize=True)


def contact_sheet():
    image = Image.new("RGB", (2000, 1300), WARM)
    draw = ImageDraw.Draw(image)
    draw.text((70, 55), "ONYX · AVITO CAROUSEL FINAL REVIEW V2.3", font=font(CORMORANT, 62), fill=ONYX)
    draw.text((70, 130), "BUSINESS + LIFESTYLE · PUBLIC COLLECTIONS", font=font(MANROPE, 25), fill=MUTED)
    labels = ["HERO", "BEFORE → AFTER", "COLLECTIONS", "IDENTITY / RANGE", "SCENES", "PROCESS", "QUALITY", "PRICING + UPGRADE", "BOOK", "CTA"]
    for index, label in enumerate(labels, start=1):
        col, row = (index - 1) % 5, (index - 1) // 5
        x, y = 70 + col * 385, 215 + row * 500
        with Image.open(EXPORT / f"AVITO_V2_3_{index:02d}.jpg") as card:
            thumb = card.convert("RGB").resize((340, 255), Image.Resampling.LANCZOS)
        image.paste(thumb, (x, y))
        draw.rectangle((x, y, x + 340, y + 255), outline=CHAMPAGNE, width=2)
        draw.text((x, y + 280), f"{index:02d} · {label}", font=font(MANROPE, 22), fill=ONYX)
        draw.text((x, y + 320), "V2.3 UPDATE" if index == 3 else "UNCHANGED FROM V2.2", font=font(MANROPE, 18), fill="#786A49")
    draw.text((70, 1235), "Status: READY_FOR_AVITO_PUBLISH_APPROVAL", font=font(MANROPE, 23), fill=ONYX)
    image.save(SHEETS / "AVITO_CAROUSEL_FINAL_REVIEW_v2_3.jpg", "JPEG", quality=92, subsampling=0, optimize=True)


def mobile_sheet():
    image = Image.new("RGB", (1100, 1000), CARBON)
    draw = ImageDraw.Draw(image)
    draw.text((70, 35), "V2.3 MOBILE QA · EXACT 390 PX CARD PREVIEWS", font=font(MANROPE, 30), fill=CHAMPAGNE)
    for column, (slide, label) in enumerate(((3, "COLLECTIONS"), (8, "PRICING + UPGRADE"))):
        x, y = 70 + column * 500, 115
        with Image.open(EXPORT / f"AVITO_V2_3_{slide:02d}.jpg") as card:
            preview = card.convert("RGB").resize((390, 293), Image.Resampling.LANCZOS)
        image.paste(preview, (x, y))
        draw.rectangle((x, y, x + 390, y + 293), outline=CHAMPAGNE, width=2)
        draw.text((x, y + 315), f"{slide:02d} · {label}", font=font(MANROPE, 21), fill=WARM)
        draw.text((x, y + 350), "390 px · review without zoom", font=font(MANROPE, 17), fill=MUTED)

    draw.text((70, 520), "FULL SEQUENCE · 170 PX PREVIEWS", font=font(MANROPE, 23), fill=CHAMPAGNE)
    for index in range(1, 11):
        col, row = (index - 1) % 5, (index - 1) // 5
        x, y = 70 + col * 200, 575 + row * 160
        with Image.open(EXPORT / f"AVITO_V2_3_{index:02d}.jpg") as card:
            thumb = card.convert("RGB").resize((170, 128), Image.Resampling.LANCZOS)
        image.paste(thumb, (x, y))
        draw.rectangle((x, y, x + 170, y + 128), outline="#5E5647", width=1)
        draw.text((x + 6, y + 6), f"{index:02d}", font=font(MANROPE, 16), fill=WARM)
    image.save(QA / "AVITO_MOBILE_QA_v2_3.jpg", "JPEG", quality=92, subsampling=0, optimize=True)


def inspection():
    paths = [*sorted(MASTER.glob("AVITO_V2_3_*.png")), *sorted(EXPORT.glob("AVITO_V2_3_*.jpg"))]
    paths += [SHEETS / "AVITO_CAROUSEL_FINAL_REVIEW_v2_3.jpg", QA / "AVITO_MOBILE_QA_v2_3.jpg"]
    records = []
    for path in paths:
        with Image.open(path) as source:
            source.verify()
        with Image.open(path) as source:
            records.append({"path": path.relative_to(ROOT).as_posix(), "format": source.format, "width": source.width, "height": source.height, "mode": source.mode, "bytes": path.stat().st_size, "sha256": sha256(path)})
    (QA / "render_inspection_v2_3.json").write_text(json.dumps({"status": "PASS", "files": records}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "revision": "v2.3", "rendered": len(records)}, ensure_ascii=False))


copy_v22()
collections_card()
contact_sheet()
mobile_sheet()
inspection()
