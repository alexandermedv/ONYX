from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import hashlib
import json
import math
import shutil


ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT.parents[3]
PRODUCTION = ROOT.parents[2]
BRAND = PRODUCTION / "Brand"
BUSINESS = REPO / "01_Characters" / "P02" / "02_Sessions" / "Business_v1" / "02_Final"
REFERENCE = REPO / "09 Experiments" / "identity_benchmark_v1" / "P02_F30_Lifestyle" / "01_references" / "P02_REF03.png"
CANDIDATES = ROOT / "01_asset_candidates" / "v2"
MASTER = ROOT / "04_master" / "v2"
EXPORT = ROOT / "05_export" / "v2"
SHEETS = ROOT / "02_contact_sheets"
QA = ROOT / "06_qa" / "v2"
for directory in (CANDIDATES, MASTER, EXPORT, SHEETS, QA):
    directory.mkdir(parents=True, exist_ok=True)

ONYX = "#111111"
CARBON = "#242424"
WARM = "#F6F4EF"
STONE = "#D8D3CA"
CHAMPAGNE = "#B5A079"
MUTED = "#77736D"
WHITE = "#FFFFFF"
MANROPE = BRAND / "Typography" / "Manrope-Variable.ttf"
CORMORANT = BRAND / "Typography" / "CormorantGaramond-Variable.ttf"

ASSETS = {
    "A01": BUSINESS / "ONYX_P02_BUSINESS_01_HERO.jpg",
    "A02": BUSINESS / "ONYX_P02_BUSINESS_02_CLOSE.jpg",
    "A03": BUSINESS / "ONYX_P02_BUSINESS_03_WAIST.jpg",
    "A04": BUSINESS / "ONYX_P02_BUSINESS_04_SEATED.jpg",
    "A05": BUSINESS / "ONYX_P02_BUSINESS_05_ENVIRONMENT.jpg",
    "A06": BUSINESS / "ONYX_P02_BUSINESS_06_ACTION.jpg",
    "A07": BUSINESS / "ONYX_P02_BUSINESS_07_3Q_BODY.jpg",
    "A08": BUSINESS / "ONYX_P02_BUSINESS_08_FULL_BODY.jpg",
    "A09": BUSINESS / "ONYX_P02_BUSINESS_09_MOOD.jpg",
    "A10": BUSINESS / "ONYX_P02_BUSINESS_10_EDITORIAL.jpg",
}
REF03_SHA256 = "23fb0883218085354fe2de85d92d2641916501ac41e754735892babb10a004c2"


def face(path, size):
    return ImageFont.truetype(str(path), size=size)


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
    canvas.paste(fitted(path, (x2 - x1, y2 - y1), centering), (x1, y1))
    if border:
        ImageDraw.Draw(canvas).rectangle(box, outline=CHAMPAGNE, width=border)


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def star(draw, center, outer_radius, inner_radius, fill):
    points = []
    for index in range(10):
        angle = -math.pi / 2 + index * math.pi / 5
        radius = outer_radius if index % 2 == 0 else inner_radius
        points.append((center[0] + math.cos(angle) * radius, center[1] + math.sin(angle) * radius))
    draw.polygon(points, fill=fill)


def multi(draw, xy, text, font, fill, spacing=8, anchor=None, align="left"):
    draw.multiline_text(xy, text, font=font, fill=fill, spacing=spacing, anchor=anchor, align=align)


def base(slide, light=False):
    background = WARM if light else ONYX
    foreground = ONYX if light else WARM
    image = Image.new("RGB", (2560, 1920), background)
    draw = ImageDraw.Draw(image)
    draw.text((135, 82), "ONYX", font=face(CORMORANT, 84), fill=CHAMPAGNE)
    draw.text((2425, 115), f"{slide:02d} / 10", font=face(MANROPE, 30), fill=MUTED, anchor="ra")
    draw.line((135, 205, 2425, 205), fill=CHAMPAGNE, width=3)
    return image, draw, foreground


def save_card(slide, image):
    stem = f"AVITO_V2_{slide:02d}"
    image.save(MASTER / f"{stem}.png", "PNG", optimize=True)
    image.resize((1280, 960), Image.Resampling.LANCZOS).save(
        EXPORT / f"{stem}.jpg", "JPEG", quality=92, subsampling=0, optimize=True
    )


def update_provenance():
    if sha256(REFERENCE) != REF03_SHA256:
        raise RuntimeError("P02_REF03 canonical hash mismatch")
    copy = CANDIDATES / "P02_REF03.png"
    shutil.copy2(REFERENCE, copy)
    if sha256(copy) != REF03_SHA256:
        raise RuntimeError("P02_REF03 working-copy hash mismatch")
    path = ROOT / "01_asset_candidates" / "PROVENANCE.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["revision_scopes"] = ["AVITO_LAUNCH_V1", "AVITO_LAUNCH_V1_BEFORE_AFTER"]
    payload["before_after_references"] = [{
        "id": "B01",
        "persona": "P02 / Anna",
        "identity_version": 1,
        "role": "BEFORE / canonical synthetic reference",
        "source": REFERENCE.relative_to(REPO).as_posix(),
        "source_sha256": REF03_SHA256,
        "candidate_copy": copy.relative_to(ROOT).as_posix(),
        "candidate_copy_sha256": REF03_SHA256,
        "after_asset_id": "A10",
        "after_source_sha256": sha256(ASSETS["A10"]),
        "synthetic_persona": True,
        "marketing_approved": True,
        "avito_publication_approved": True,
        "publish_approved": True,
        "approval_scope": "AVITO_LAUNCH_V1_BEFORE_AFTER",
        "source_mutated": False,
    }]
    payload["revision_v2"] = {
        "status": "READY_FOR_HUMAN_AVITO_REVIEW_V2",
        "carousel_cards": 10,
        "before_after_pair": ["B01", "A10"],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def hero():
    image, draw, fg = base(1)
    paste_photo(image, ASSETS["A01"], (1020, 260, 2425, 1820), (0.5, 0.34))
    draw.text((135, 315), "ПЕРСОНАЛЬНАЯ ФОТОСЕССИЯ", font=face(MANROPE, 31), fill=CHAMPAGNE)
    multi(draw, (135, 510), "AI-фотосессия\nпо вашим фото", face(CORMORANT, 128), fg, spacing=2)
    draw.text((135, 1160), "от 1 000 ₽", font=face(MANROPE, 92), fill=CHAMPAGNE)
    draw.text((135, 1335), "Без студии и сложной съёмки", font=face(MANROPE, 42), fill=WARM)
    save_card(1, image)


def before_after():
    image, draw, fg = base(2, light=True)
    multi(draw, (135, 300), "Обычные фото →\nпрофессиональная фотосессия", face(CORMORANT, 96), fg, spacing=2)
    left = (150, 655, 1050, 1655)
    right = (1510, 655, 2410, 1655)
    paste_photo(image, REFERENCE, left, (0.5, 0.42), border=3)
    paste_photo(image, ASSETS["A10"], right, (0.5, 0.43), border=3)
    rounded(draw, (1165, 1030, 1395, 1260), 115, CHAMPAGNE)
    draw.text((1280, 1145), "→", font=face(MANROPE, 88), fill=ONYX, anchor="mm")
    draw.text((150, 1700), "ВАШЕ ИСХОДНОЕ ФОТО", font=face(MANROPE, 32), fill=MUTED)
    draw.text((1510, 1700), "ГОТОВАЯ СЕРИЯ ONYX", font=face(MANROPE, 32), fill=ONYX)
    draw.text((1280, 1805), "Демонстрация на синтетическом персонаже", font=face(MANROPE, 34), fill=MUTED, anchor="ma")
    save_card(2, image)


def diversity():
    image, draw, fg = base(3)
    multi(draw, (135, 305), "Одна фотосессия.\nРазные задачи.", face(CORMORANT, 104), fg, spacing=2)
    items = [
        ("A03", "ПОРТРЕТ", (135, 735, 660, 1660), (0.5, 0.38)),
        ("A04", "РАБОТА", (720, 665, 1245, 1660), (0.5, 0.46)),
        ("A06", "ДВИЖЕНИЕ", (1305, 735, 1830, 1660), (0.5, 0.43)),
        ("A10", "В ПОЛНЫЙ РОСТ", (1890, 665, 2415, 1660), (0.5, 0.44)),
    ]
    for asset, label, box, center in items:
        paste_photo(image, ASSETS[asset], box, center, border=2)
        draw.text((box[0], 1715), label, font=face(MANROPE, 29), fill=CHAMPAGNE)
    save_card(3, image)


def portrait():
    image, draw, fg = base(4, light=True)
    multi(draw, (135, 305), "Сохранить внешность.\nПоказать характер.", face(CORMORANT, 100), fg, spacing=2)
    paste_photo(image, ASSETS["A02"], (135, 670, 1195, 1740), (0.5, 0.38), border=2)
    paste_photo(image, ASSETS["A03"], (1270, 590, 2425, 1740), (0.5, 0.38), border=2)
    draw.text((135, 1790), "РЕЗЮМЕ  ·  ПРОФИЛЬ  ·  ЛИЧНЫЙ БРЕНД", font=face(MANROPE, 34), fill=MUTED)
    save_card(4, image)


def work_context():
    image, draw, fg = base(5)
    paste_photo(image, ASSETS["A04"], (135, 290, 1370, 1790), (0.5, 0.46), border=2)
    paste_photo(image, ASSETS["A09"], (1445, 290, 2425, 1010), (0.5, 0.46), border=2)
    paste_photo(image, ASSETS["A05"], (1445, 1080, 1900, 1790), (0.5, 0.42), border=2)
    multi(draw, (1950, 1140), "Для работы,\nпрофиля\nи личного\nбренда", face(CORMORANT, 70), fg, spacing=0)
    save_card(5, image)


def process():
    image, draw, fg = base(6)
    multi(draw, (135, 325), "Готовый результат,\nа не случайные генерации", face(CORMORANT, 108), fg, spacing=2)
    steps = ["Ваши фото", "Концепция", "Отбор", "Контроль", "Финал"]
    y = 940
    for index, step in enumerate(steps):
        x = 135 + index * 465
        rounded(draw, (x, y, x + 375, y + 230), 30, CARBON, CHAMPAGNE, 3)
        draw.text((x + 187, y + 115), step, font=face(MANROPE, 52), fill=WARM, anchor="mm")
        if index < len(steps) - 1:
            draw.text((x + 420, y + 115), "→", font=face(MANROPE, 48), fill=CHAMPAGNE, anchor="mm")
    draw.text((135, 1535), "Сначала бесплатно проверим ваши фотографии", font=face(MANROPE, 46), fill=CHAMPAGNE)
    save_card(6, image)


def quality():
    image, draw, fg = base(7, light=True)
    multi(draw, (135, 315), "Каждый финальный кадр\nпроходит ручной контроль", face(CORMORANT, 104), fg, spacing=2)
    items = ["Сходство", "Лицо и глаза", "Руки и анатомия", "Пропорции", "Реализм", "Разнообразие серии"]
    for index, item in enumerate(items):
        col, row = index % 2, index // 2
        x, y = 135 + col * 1160, 855 + row * 250
        rounded(draw, (x, y, x + 1050, y + 185), 26, WHITE, STONE, 3)
        draw.ellipse((x + 42, y + 76, x + 62, y + 96), fill=CHAMPAGNE)
        draw.text((x + 100, y + 92), item, font=face(MANROPE, 56), fill=ONYX, anchor="lm")
    save_card(7, image)


def pricing():
    image, draw, fg = base(8, light=True)
    draw.text((135, 320), "Выберите формат", font=face(CORMORANT, 106), fill=fg)
    # Side products remain clear; Signature receives the largest, darkest field.
    side_y = 820
    rounded(draw, (135, side_y, 680, 1500), 30, WHITE, STONE, 3)
    draw.text((185, side_y + 60), "PORTRAIT", font=face(MANROPE, 30), fill=MUTED)
    draw.text((185, side_y + 190), "1 фото", font=face(CORMORANT, 72), fill=ONYX)
    draw.text((185, side_y + 360), "1 000 ₽", font=face(MANROPE, 58), fill=ONYX)
    rounded(draw, (765, 610, 1795, 1560), 34, ONYX, CHAMPAGNE, 5)
    rounded(draw, (1350, 660, 1715, 730), 35, CHAMPAGNE)
    draw.text((1532, 695), "РЕКОМЕНДУЕМ", font=face(MANROPE, 25), fill=ONYX, anchor="mm")
    draw.text((835, 685), "SIGNATURE", font=face(MANROPE, 38), fill=CHAMPAGNE)
    star(draw, (1095, 708), 22, 10, CHAMPAGNE)
    draw.text((835, 880), "10 фото", font=face(CORMORANT, 100), fill=WARM)
    draw.text((835, 1110), "3 000 ₽", font=face(MANROPE, 78), fill=WARM)
    draw.text((835, 1330), "Полная фотосессия", font=face(MANROPE, 36), fill=STONE)
    rounded(draw, (1880, side_y, 2425, 1500), 30, WHITE, STONE, 3)
    draw.text((1930, side_y + 60), "PREMIUM", font=face(MANROPE, 30), fill=MUTED)
    draw.text((1930, side_y + 190), "20 фото", font=face(CORMORANT, 72), fill=ONYX)
    draw.text((1930, side_y + 360), "5 000 ₽", font=face(MANROPE, 58), fill=ONYX)
    draw.text((135, 1710), "+1 фото — 500 ₽     ·     Срочно — от +50%", font=face(MANROPE, 38), fill=MUTED)
    save_card(8, image)


def book():
    image, draw, fg = base(9)
    multi(draw, (135, 300), "Персональная фотокнига PDF\nвходит в Signature и Premium", face(CORMORANT, 90), fg, spacing=2)
    rounded(draw, (250, 765, 2310, 1655), 20, "#050505")
    rounded(draw, (270, 735, 2290, 1625), 16, WARM)
    draw.line((1275, 765, 1275, 1595), fill=STONE, width=4)
    paste_photo(image, ASSETS["A01"], (315, 785, 755, 1545), (0.5, 0.33))
    paste_photo(image, ASSETS["A06"], (795, 785, 1225, 1165), (0.5, 0.41))
    paste_photo(image, ASSETS["A03"], (795, 1205, 1225, 1545), (0.5, 0.40))
    paste_photo(image, ASSETS["A10"], (1325, 785, 2245, 1545), (0.5, 0.44))
    draw.text((1280, 1765), "Электронная книга с вашей готовой серией", font=face(MANROPE, 38), fill=CHAMPAGNE, anchor="ma")
    save_card(9, image)


def cta():
    image, draw, fg = base(10)
    paste_photo(image, ASSETS["A01"], (1490, 260, 2425, 1820), (0.5, 0.34))
    multi(draw, (135, 350), "Хотите такую\nфотосессию?", face(CORMORANT, 118), fg, spacing=2)
    rounded(draw, (135, 890, 1360, 1090), 34, CHAMPAGNE)
    draw.text((747, 990), "Напишите «Хочу ONYX»", font=face(MANROPE, 53), fill=ONYX, anchor="mm")
    draw.ellipse((145, 1280, 169, 1304), fill=CHAMPAGNE)
    draw.text((205, 1292), "Бесплатно проверим ваши фото", font=face(MANROPE, 40), fill=WARM, anchor="lm")
    draw.ellipse((145, 1405, 169, 1429), fill=CHAMPAGNE)
    draw.text((205, 1417), "Подскажем подходящий формат", font=face(MANROPE, 40), fill=WARM, anchor="lm")
    save_card(10, image)


def candidate_sheet():
    image = Image.new("RGB", (2200, 1430), ONYX)
    draw = ImageDraw.Draw(image)
    draw.text((65, 45), "ONYX · V2 APPROVED ASSET SET", font=face(CORMORANT, 64), fill=CHAMPAGNE)
    draw.text((65, 120), "B01 BEFORE REFERENCE + P02 BUSINESS A01–A10", font=face(MANROPE, 25), fill=MUTED)
    items = [("B01", REFERENCE, "BEFORE / REF03")] + [(asset, path, asset) for asset, path in ASSETS.items()]
    for index, (asset_id, path, label) in enumerate(items):
        col, row = index % 6, index // 6
        x, y = 65 + col * 350, 205 + row * 570
        paste_photo(image, path, (x, y, x + 295, y + 395), (0.5, 0.40), border=2)
        draw.text((x, y + 418), f"{asset_id} · ANNA", font=face(MANROPE, 23), fill=WARM)
        draw.text((x, y + 455), label, font=face(MANROPE, 19), fill=CHAMPAGNE)
    draw.text((65, 1370), "B01 scope: AVITO_LAUNCH_V1_BEFORE_AFTER · canonical sources unchanged", font=face(MANROPE, 22), fill=MUTED)
    image.save(SHEETS / "AVITO_ASSET_CANDIDATES_v2.jpg", "JPEG", quality=92, subsampling=0, optimize=True)


def carousel_sheet():
    image = Image.new("RGB", (2000, 1300), WARM)
    draw = ImageDraw.Draw(image)
    draw.text((70, 55), "ONYX · AVITO CAROUSEL REVISION V2", font=face(CORMORANT, 62), fill=ONYX)
    draw.text((70, 130), "MOBILE-FIRST CONVERSION PASS · HUMAN REVIEW BUILD", font=face(MANROPE, 25), fill=MUTED)
    labels = ["HERO", "BEFORE → AFTER", "DIVERSITY", "PORTRAIT", "WORK", "PROCESS", "QUALITY", "PRICING", "BOOK", "CTA"]
    for index, label in enumerate(labels):
        col, row = index % 5, index // 5
        x, y = 70 + col * 385, 215 + row * 500
        thumb = fitted(EXPORT / f"AVITO_V2_{index + 1:02d}.jpg", (340, 255), (0.5, 0.5))
        image.paste(thumb, (x, y))
        draw.rectangle((x, y, x + 340, y + 255), outline=CHAMPAGNE, width=2)
        draw.text((x, y + 280), f"{index + 1:02d} · {label}", font=face(MANROPE, 22), fill=ONYX)
        draw.text((x, y + 320), "READY FOR REVIEW", font=face(MANROPE, 18), fill="#786A49")
    draw.text((70, 1235), "Status: READY_FOR_HUMAN_AVITO_REVIEW_V2", font=face(MANROPE, 23), fill=ONYX)
    image.save(SHEETS / "AVITO_CAROUSEL_PROPOSED_v2.jpg", "JPEG", quality=92, subsampling=0, optimize=True)


def mobile_sheet():
    image = Image.new("RGB", (2100, 1280), CARBON)
    draw = ImageDraw.Draw(image)
    draw.text((55, 45), "V2 MOBILE QA · 350 × 263 PREVIEWS", font=face(MANROPE, 30), fill=CHAMPAGNE)
    for index in range(10):
        col, row = index % 5, index // 5
        x, y = 55 + col * 405, 130 + row * 535
        thumb = fitted(EXPORT / f"AVITO_V2_{index + 1:02d}.jpg", (350, 263), (0.5, 0.5))
        image.paste(thumb, (x, y))
        draw.text((x, y + 290), f"AVITO_V2_{index + 1:02d}", font=face(MANROPE, 23), fill=WARM)
        draw.text((x, y + 330), "HEADLINE / SUBJECT / CTA", font=face(MANROPE, 17), fill=MUTED)
    draw.text((55, 1220), "Review scale: key message must remain clear without zoom", font=face(MANROPE, 22), fill=MUTED)
    image.save(QA / "AVITO_MOBILE_QA_v2.jpg", "JPEG", quality=92, subsampling=0, optimize=True)


update_provenance()
hero()
before_after()
diversity()
portrait()
work_context()
process()
quality()
pricing()
book()
cta()
candidate_sheet()
carousel_sheet()
mobile_sheet()

records = []
for path in sorted([*MASTER.glob("*.png"), *EXPORT.glob("*.jpg"), SHEETS / "AVITO_ASSET_CANDIDATES_v2.jpg", SHEETS / "AVITO_CAROUSEL_PROPOSED_v2.jpg", QA / "AVITO_MOBILE_QA_v2.jpg"]):
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
(QA / "render_inspection_v2.json").write_text(
    json.dumps({"status": "PASS", "files": records}, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(json.dumps({"status": "PASS", "rendered": len(records), "revision": "v2"}, ensure_ascii=False))
