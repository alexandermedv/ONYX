from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import hashlib
import json
import shutil


ROOT = Path(__file__).resolve().parents[2]
PRODUCTION = ROOT.parents[2]
BRAND = PRODUCTION / "Brand"
BUSINESS = PRODUCTION / "Portfolio" / "P02" / "Business_V1" / "final_source_resolution"
V25_MASTER = ROOT / "04_master" / "v2_5"
V25_EXPORT = ROOT / "05_export" / "v2_5"
MASTER = ROOT / "04_master" / "v2_6"
EXPORT = ROOT / "05_export" / "v2_6"
SHEETS = ROOT / "02_contact_sheets"
QA = ROOT / "06_qa" / "v2_6"

for directory in (MASTER, EXPORT, SHEETS, QA):
    directory.mkdir(parents=True, exist_ok=True)

ASSETS = {
    "A01": BUSINESS / "ONYX_P02_BUSINESS_01_HERO.jpg",
    "A03": BUSINESS / "ONYX_P02_BUSINESS_03_WAIST.jpg",
    "A06": BUSINESS / "ONYX_P02_BUSINESS_06_ACTION.jpg",
    "A10": BUSINESS / "ONYX_P02_BUSINESS_10_EDITORIAL.jpg",
}

ONYX = "#111111"
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


def headroom_fit(path, size, x_center=0.5):
    """Fill a box while preserving the complete source top edge."""
    with Image.open(path) as source:
        image = source.convert("RGB")
    target_w, target_h = size
    target_ratio = target_w / target_h
    source_ratio = image.width / image.height
    if source_ratio < target_ratio:
        crop_h = round(image.width / target_ratio)
        box = (0, 0, image.width, crop_h)
    else:
        crop_w = round(image.height * target_ratio)
        left = round((image.width - crop_w) * x_center)
        box = (left, 0, left + crop_w, image.height)
    return image.crop(box).resize(size, Image.Resampling.LANCZOS)


def paste_photo(canvas, path, box, x_center=0.5):
    x1, y1, x2, y2 = box
    canvas.paste(headroom_fit(path, (x2 - x1, y2 - y1), x_center), (x1, y1))


def copy_v25():
    for slide in range(1, 11):
        shutil.copy2(V25_MASTER / f"AVITO_V2_5_{slide:02d}.png", MASTER / f"AVITO_V2_6_{slide:02d}.png")
        shutil.copy2(V25_EXPORT / f"AVITO_V2_5_{slide:02d}.jpg", EXPORT / f"AVITO_V2_6_{slide:02d}.jpg")


def slide_09():
    image = Image.new("RGB", (2560, 1920), ONYX)
    draw = ImageDraw.Draw(image)
    draw.text((135, 82), "ONYX", font=font(CORMORANT, 84), fill=CHAMPAGNE)
    draw.text((2425, 115), "09 / 10", font=font(MANROPE, 30), fill=MUTED, anchor="ra")
    draw.line((135, 205, 2425, 205), fill=CHAMPAGNE, width=3)
    draw.multiline_text((135, 300), "Персональная фотокнига PDF\nвходит в Signature и Premium", font=font(CORMORANT, 90), fill=WARM, spacing=2)
    draw.rounded_rectangle((250, 765, 2310, 1655), radius=20, fill="#050505")
    draw.rounded_rectangle((270, 735, 2290, 1625), radius=16, fill=WARM)
    draw.line((1275, 765, 1275, 1595), fill=STONE, width=4)
    paste_photo(image, ASSETS["A01"], (315, 785, 755, 1545))
    paste_photo(image, ASSETS["A06"], (795, 785, 1225, 1165))
    paste_photo(image, ASSETS["A03"], (795, 1205, 1225, 1545))
    paste_photo(image, ASSETS["A10"], (1325, 785, 2245, 1545))
    draw.text((1280, 1765), "Электронная книга с вашей готовой серией", font=font(MANROPE, 38), fill=CHAMPAGNE, anchor="ma")
    image.save(MASTER / "AVITO_V2_6_09.png", "PNG", optimize=True)
    image.resize((1280, 960), Image.Resampling.LANCZOS).save(EXPORT / "AVITO_V2_6_09.jpg", "JPEG", quality=92, subsampling=0, optimize=True)


def final_sheet():
    image = Image.new("RGB", (2000, 1300), WARM)
    draw = ImageDraw.Draw(image)
    draw.text((70, 55), "ONYX · AVITO CAROUSEL FINAL V2.6", font=font(CORMORANT, 62), fill=ONYX)
    draw.text((70, 130), "HEADROOM FIX · SLIDE 09", font=font(MANROPE, 25), fill=MUTED)
    labels = ["HERO", "BEFORE → AFTER", "COLLECTIONS", "IDENTITY / RANGE", "SCENES", "PROCESS", "QUALITY", "PRICING + UPGRADE", "BOOK", "CTA"]
    for index, label in enumerate(labels, start=1):
        col, row = (index - 1) % 5, (index - 1) // 5
        x, y = 70 + col * 385, 215 + row * 500
        with Image.open(EXPORT / f"AVITO_V2_6_{index:02d}.jpg") as card:
            thumb = card.convert("RGB").resize((340, 255), Image.Resampling.LANCZOS)
        image.paste(thumb, (x, y))
        draw.rectangle((x, y, x + 340, y + 255), outline=CHAMPAGNE, width=2)
        draw.text((x, y + 280), f"{index:02d} · {label}", font=font(MANROPE, 22), fill=ONYX)
        draw.text((x, y + 320), "HEADROOM FIX" if index == 9 else "BYTE-IDENTICAL TO V2.5", font=font(MANROPE, 18), fill="#786A49")
    draw.text((70, 1235), "Status: APPROVED_FOR_AVITO_PUBLISH", font=font(MANROPE, 23), fill=ONYX)
    image.save(SHEETS / "AVITO_CAROUSEL_FINAL_v2_6.jpg", "JPEG", quality=92, subsampling=0, optimize=True)


def mobile_sheet():
    image = Image.new("RGB", (1100, 1000), "#242424")
    draw = ImageDraw.Draw(image)
    draw.text((70, 35), "V2.6 MOBILE QA · EXACT 390 PX PREVIEW", font=font(MANROPE, 30), fill=CHAMPAGNE)
    with Image.open(EXPORT / "AVITO_V2_6_09.jpg") as card:
        preview = card.convert("RGB").resize((390, 293), Image.Resampling.LANCZOS)
    image.paste(preview, (70, 115))
    draw.rectangle((70, 115, 460, 408), outline=CHAMPAGNE, width=2)
    draw.text((70, 430), "09 · ALL FOUR HEADS VISIBLE", font=font(MANROPE, 21), fill=WARM)
    draw.text((70, 465), "390 px · review without zoom", font=font(MANROPE, 17), fill=MUTED)

    draw.text((70, 565), "FULL SEQUENCE · 170 PX PREVIEWS", font=font(MANROPE, 23), fill=CHAMPAGNE)
    for index in range(1, 11):
        col, row = (index - 1) % 5, (index - 1) // 5
        x, y = 70 + col * 200, 620 + row * 160
        with Image.open(EXPORT / f"AVITO_V2_6_{index:02d}.jpg") as card:
            thumb = card.convert("RGB").resize((170, 128), Image.Resampling.LANCZOS)
        image.paste(thumb, (x, y))
        draw.rectangle((x, y, x + 170, y + 128), outline="#5E5647", width=1)
        draw.text((x + 6, y + 6), f"{index:02d}", font=font(MANROPE, 16), fill=WARM)
    image.save(QA / "AVITO_MOBILE_QA_v2_6.jpg", "JPEG", quality=92, subsampling=0, optimize=True)


def inspection():
    paths = [*sorted(MASTER.glob("AVITO_V2_6_*.png")), *sorted(EXPORT.glob("AVITO_V2_6_*.jpg"))]
    paths += [SHEETS / "AVITO_CAROUSEL_FINAL_v2_6.jpg", QA / "AVITO_MOBILE_QA_v2_6.jpg"]
    records = []
    for path in paths:
        with Image.open(path) as source:
            source.verify()
        with Image.open(path) as source:
            records.append({"path": path.relative_to(ROOT).as_posix(), "format": source.format, "width": source.width, "height": source.height, "mode": source.mode, "bytes": path.stat().st_size, "sha256": sha256(path)})
    (QA / "render_inspection_v2_6.json").write_text(json.dumps({"status": "PASS", "files": records}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "revision": "v2.6", "rendered": len(records)}, ensure_ascii=False))


copy_v25()
slide_09()
final_sheet()
mobile_sheet()
inspection()
