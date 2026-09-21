from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import hashlib
import json
import shutil


ROOT = Path(__file__).resolve().parents[2]
PRODUCTION = ROOT.parents[2]
BRAND = PRODUCTION / "Brand"
V2_MASTER = ROOT / "04_master" / "v2"
V2_EXPORT = ROOT / "05_export" / "v2"
MASTER = ROOT / "04_master" / "v2_1"
EXPORT = ROOT / "05_export" / "v2_1"
SHEETS = ROOT / "02_contact_sheets"
QA = ROOT / "06_qa" / "v2_1"
PROVENANCE = ROOT / "01_asset_candidates" / "PROVENANCE.json"

for directory in (MASTER, EXPORT, SHEETS, QA):
    directory.mkdir(parents=True, exist_ok=True)

ONYX = "#111111"
CARBON = "#242424"
WARM = "#F6F4EF"
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


def update_provenance():
    payload = json.loads(PROVENANCE.read_text(encoding="utf-8"))
    payload["revision_v2_1"] = {
        "status": "READY_FOR_AVITO_LAUNCH_APPROVAL",
        "carousel_cards": 10,
        "before_reference_id": "B01",
        "before_reference_changed": False,
        "hero_price_emphasis": "slightly increased",
        "cards_02_10_preserved_from_v2": True,
        "publication_performed": False,
    }
    PROVENANCE.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def build_cards():
    # Cards 02–10 are exact copies of the reviewed v2 files.
    for slide in range(2, 11):
        shutil.copy2(
            V2_MASTER / f"AVITO_V2_{slide:02d}.png",
            MASTER / f"AVITO_V2_1_{slide:02d}.png",
        )
        shutil.copy2(
            V2_EXPORT / f"AVITO_V2_{slide:02d}.jpg",
            EXPORT / f"AVITO_V2_1_{slide:02d}.jpg",
        )

    # The only visual change in v2.1: a modest size increase for the entry price.
    with Image.open(V2_MASTER / "AVITO_V2_01.png") as source:
        hero = source.convert("RGB")
    draw = ImageDraw.Draw(hero)
    draw.rectangle((118, 1100, 875, 1300), fill=ONYX)
    draw.text((135, 1140), "от 1 000 ₽", font=font(MANROPE, 106), fill=CHAMPAGNE)
    hero.save(MASTER / "AVITO_V2_1_01.png", "PNG", optimize=True)
    hero.resize((1280, 960), Image.Resampling.LANCZOS).save(
        EXPORT / "AVITO_V2_1_01.jpg",
        "JPEG",
        quality=92,
        subsampling=0,
        optimize=True,
    )


def final_contact_sheet():
    canvas = Image.new("RGB", (2000, 1300), WARM)
    draw = ImageDraw.Draw(canvas)
    draw.text((70, 55), "ONYX · AVITO CAROUSEL FINAL REVIEW V2.1", font=font(CORMORANT, 62), fill=ONYX)
    draw.text((70, 130), "MICRO-PASS · HERO PRICE EMPHASIS · FINAL HUMAN APPROVAL", font=font(MANROPE, 25), fill=MUTED)
    labels = ["HERO", "BEFORE → AFTER", "DIVERSITY", "PORTRAIT", "WORK", "PROCESS", "QUALITY", "PRICING", "BOOK", "CTA"]
    for index, label in enumerate(labels, start=1):
        col, row = (index - 1) % 5, (index - 1) // 5
        x, y = 70 + col * 385, 215 + row * 500
        with Image.open(EXPORT / f"AVITO_V2_1_{index:02d}.jpg") as card:
            thumb = card.convert("RGB").resize((340, 255), Image.Resampling.LANCZOS)
        canvas.paste(thumb, (x, y))
        draw.rectangle((x, y, x + 340, y + 255), outline=CHAMPAGNE, width=2)
        draw.text((x, y + 280), f"{index:02d} · {label}", font=font(MANROPE, 22), fill=ONYX)
        note = "V2.1 MICRO-PASS" if index == 1 else "UNCHANGED FROM V2"
        draw.text((x, y + 320), note, font=font(MANROPE, 18), fill="#786A49")
    draw.text((70, 1235), "Status: READY_FOR_AVITO_LAUNCH_APPROVAL", font=font(MANROPE, 23), fill=ONYX)
    canvas.save(
        SHEETS / "AVITO_CAROUSEL_FINAL_REVIEW_v2_1.jpg",
        "JPEG",
        quality=92,
        subsampling=0,
        optimize=True,
    )


def mobile_qa_sheet():
    canvas = Image.new("RGB", (1300, 1000), CARBON)
    draw = ImageDraw.Draw(canvas)
    draw.text((45, 35), "V2.1 MOBILE QA · EXACT 390 PX CARD PREVIEWS", font=font(MANROPE, 30), fill=CHAMPAGNE)
    focus = [(1, "HERO / ENTRY PRICE"), (8, "PRICING / ALL PRICES"), (10, "CTA / ACTION")]
    for column, (slide, label) in enumerate(focus):
        x, y = 45 + column * 420, 115
        with Image.open(EXPORT / f"AVITO_V2_1_{slide:02d}.jpg") as card:
            preview = card.convert("RGB").resize((390, 293), Image.Resampling.LANCZOS)
        canvas.paste(preview, (x, y))
        draw.rectangle((x, y, x + 390, y + 293), outline=CHAMPAGNE, width=2)
        draw.text((x, y + 315), f"{slide:02d} · {label}", font=font(MANROPE, 21), fill=WARM)
        draw.text((x, y + 350), "390 px · review without zoom", font=font(MANROPE, 17), fill=MUTED)

    draw.text((45, 520), "FULL SEQUENCE · 220 PX PREVIEWS", font=font(MANROPE, 23), fill=CHAMPAGNE)
    for index in range(1, 11):
        col, row = (index - 1) % 5, (index - 1) // 5
        x, y = 45 + col * 250, 575 + row * 195
        with Image.open(EXPORT / f"AVITO_V2_1_{index:02d}.jpg") as card:
            thumb = card.convert("RGB").resize((220, 165), Image.Resampling.LANCZOS)
        canvas.paste(thumb, (x, y))
        draw.rectangle((x, y, x + 220, y + 165), outline="#5E5647", width=1)
        draw.text((x + 8, y + 8), f"{index:02d}", font=font(MANROPE, 17), fill=WARM)
    canvas.save(
        QA / "AVITO_MOBILE_QA_v2_1.jpg",
        "JPEG",
        quality=92,
        subsampling=0,
        optimize=True,
    )


def write_inspection():
    paths = [*sorted(MASTER.glob("AVITO_V2_1_*.png")), *sorted(EXPORT.glob("AVITO_V2_1_*.jpg"))]
    paths += [
        SHEETS / "AVITO_CAROUSEL_FINAL_REVIEW_v2_1.jpg",
        QA / "AVITO_MOBILE_QA_v2_1.jpg",
    ]
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
    (QA / "render_inspection_v2_1.json").write_text(
        json.dumps({"status": "PASS", "files": records}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": "PASS", "rendered": len(records), "revision": "v2.1"}, ensure_ascii=False))


update_provenance()
build_cards()
final_contact_sheet()
mobile_qa_sheet()
write_inspection()
