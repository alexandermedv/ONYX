"""Build repeatable ONYX client-delivery derivatives from approved masters."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def save_jpeg(source: Path, target: Path, edge: int, quality: int) -> None:
    with Image.open(source) as image:
        image = image.convert("RGB")
        image.thumbnail((edge, edge), Image.Resampling.LANCZOS)
        image.save(target, "JPEG", quality=quality, optimize=True, progressive=True)


def glyph(text: str, font_path: Path, size: int, color: tuple[int, int, int, int], scale: int = 3) -> Image.Image:
    font = ImageFont.truetype(str(font_path), size * scale)
    box = font.getbbox(text)
    image = Image.new("RGBA", (box[2] - box[0], box[3] - box[1]))
    ImageDraw.Draw(image).text((-box[0], -box[1]), text, font=font, fill=color)
    return image


def build_client_preview_frame(source: Path, serif_font: Path, stone_texture: Path) -> Image.Image:
    scale = 3
    sans_font = Path(r"C:\Windows\Fonts\segoeui.ttf")
    gold = (218, 177, 68, 255)
    warm_white = (246, 244, 239, 255)
    with Image.open(source) as framed:
        framed = framed.convert("RGB")
        if framed.size != (1080, 1350):
            raise ValueError(f"Expected 1080x1350 framed preview, found {framed.size}: {source}")
        canvas = framed.copy()
    layer = Image.new("RGBA", (1080 * scale, 230 * scale))
    ring = glyph("O", serif_font, 86, gold, scale)
    ring.thumbnail((58 * scale, 58 * scale), Image.Resampling.LANCZOS)
    cx, top, bottom = 170 * scale, 70 * scale, 160 * scale
    layer.alpha_composite(ring, (cx - ring.width // 2, top))
    draw = ImageDraw.Draw(layer)
    cy = top + ring.height // 2
    draw.polygon([(cx, cy - 18 * scale), (cx + 2 * scale, cy), (cx, cy + 18 * scale), (cx - 2 * scale, cy)], fill=gold)
    word = glyph("O N Y X", serif_font, 20, gold, scale)
    layer.alpha_composite(word, (cx - word.width // 2, bottom - word.height))
    draw.line((330 * scale, top, 1010 * scale, top), fill=gold, width=2 * scale)
    title = glyph("BUSINESS COLLECTION", sans_font, 25, warm_white, scale)
    subtitle = glyph("CLIENT PREVIEW", sans_font, 19, gold, scale)
    layer.alpha_composite(title, (330 * scale, 105 * scale))
    layer.alpha_composite(subtitle, (330 * scale, bottom - subtitle.height))
    with Image.open(stone_texture) as raw:
        raw = raw.convert("RGB")
        texture = ImageOps.fit(raw.crop((0, 0, int(raw.width * .30), raw.height)), (1080 * scale, 230 * scale), method=Image.Resampling.LANCZOS)
    texture = Image.blend(texture, Image.new("RGB", texture.size, (17, 17, 17)), .34).convert("RGBA")
    texture.alpha_composite(layer)
    canvas.paste(texture.convert("RGB").resize((1080, 230), Image.Resampling.LANCZOS), (0, 1120))
    return canvas


def add_preview_mark(image: Image.Image, target: Path, font_path: Path, order_id: str) -> None:
    image = image.convert("RGB")
    image.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    regular = ImageFont.truetype(str(font_path), 42)
    small = ImageFont.truetype(str(font_path), 16)
    w, h = image.size
    for cx, cy in ((w*0.18,h*0.22),(w*0.82,h*0.22),(w*0.18,h*0.50),(w*0.82,h*0.50),(w*0.50,h*0.48)):
        col=(246,244,239,105); sub=(246,244,239,88); r=23
        draw.ellipse((cx-r,cy-r,cx+r,cy+r), outline=col, width=2)
        draw.polygon([(cx,cy-14),(cx+2,cy),(cx,cy+14),(cx-2,cy)], fill=col)
        draw.text((cx+32,cy-20), "ONYX", font=regular, fill=col, stroke_width=1, stroke_fill=(17,17,17,40))
        draw.text((cx+32,cy+13), "PRIVATE PREVIEW", font=small, fill=sub)
    image = Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")
    image.save(target, "JPEG", quality=82, optimize=True, progressive=True)


def delivery_filename(master: Path) -> str:
    return master.name.replace("_00001_", "").replace(".png", ".jpg")


def write_client_readme(delivery: Path, order_id: str) -> Path:
    target = delivery / "README.txt"
    target.write_text(
        "ONYX — клиентская выдача\n\n"
        f"Заказ: {order_id}\n\n"
        "00_PREPAYMENT_PREVIEW — защищённые превью до оплаты; не предназначены для публикации.\n"
        "01_LIGHT_JPEG — лёгкие файлы для телефона, мессенджеров и социальных сетей.\n"
        "02_HIGH_QUALITY_JPEG — качественные JPEG для повседневного использования.\n"
        "03_FULL_RESOLUTION_PNG — полные upscale-файлы для печати, ретуши и архива.\n\n"
        "Оплаченные наборы не содержат водяных знаков.\n",
        encoding="utf-8-sig",
    )
    return target


def build_archives(delivery: Path, order_id: str, readme: Path) -> None:
    safe_order = "".join(char if char.isalnum() or char in "-_" else "_" for char in order_id)
    archives = {
        delivery / f"ONYX_{safe_order}_LIGHT.zip": ("01_LIGHT_JPEG",),
        delivery / f"ONYX_{safe_order}_FULL.zip": ("01_LIGHT_JPEG", "02_HIGH_QUALITY_JPEG", "03_FULL_RESOLUTION_PNG"),
    }
    for archive, folder_names in archives.items():
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_STORED) as bundle:
            bundle.write(readme, readme.name)
            for folder_name in folder_names:
                for path in sorted((delivery / folder_name).iterdir()):
                    bundle.write(path, f"{folder_name}/{path.name}")


def remove_legacy_delivery_layout(delivery: Path) -> None:
    for folder_name in ("prepayment_preview", "web_jpeg_1600", "client_jpeg_2048", "full_resolution"):
        legacy = delivery / folder_name
        if legacy.is_dir():
            shutil.rmtree(legacy)
    legacy_manifest = delivery / "PREPAYMENT_PREVIEW_MANIFEST_V1.json"
    if legacy_manifest.is_file():
        legacy_manifest.unlink()


def discover_masters(package: Path) -> list[Path]:
    candidate_dirs = (
        package / "upscale_master",
        package / "upscale_smoke",
        package / "upscale_p01_v1",
        package / "upscale_p02_v1",
        package / "upscale_p03_v1",
    )
    by_delivery_name: dict[str, Path] = {}
    for directory in candidate_dirs:
        for master in sorted(directory.glob("ONYX_*.png")):
            by_delivery_name.setdefault(delivery_filename(master), master)
    return [by_delivery_name[name] for name in sorted(by_delivery_name)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("package", type=Path, help="Business_V1 package directory")
    parser.add_argument("--order-id", default="<ID>")
    parser.add_argument("--font", type=Path, required=True)
    args = parser.parse_args()
    package = args.package
    repo = package.resolve().parents[3]
    stone_texture = repo / "13 Production" / "Brand" / "Logo" / "Presentations" / "ONYX_MONOGRAM_ONYX_SILK_PRESENTATION_V1.png"
    if not stone_texture.exists():
        raise SystemExit(f"Approved ONYX stone texture is missing: {stone_texture}")
    masters = discover_masters(package)
    if not masters:
        raise SystemExit("No approved upscale PNG masters found")
    if len(masters) != 10:
        raise SystemExit(f"Expected 10 approved masters, found {len(masters)}")
    delivery = package / "client_delivery"
    remove_legacy_delivery_layout(delivery)
    dirs = {
        "prepayment_preview": delivery / "00_PREPAYMENT_PREVIEW",
        "web_jpeg_1600": delivery / "01_LIGHT_JPEG",
        "client_jpeg_2048": delivery / "02_HIGH_QUALITY_JPEG",
        "full_resolution": delivery / "03_FULL_RESOLUTION_PNG",
    }
    for directory in dirs.values(): directory.mkdir(parents=True, exist_ok=True)
    records = []
    for index, master in enumerate(masters, start=1):
        filename = delivery_filename(master)
        client_stem = f"ONYX_{index:02d}"
        full_resolution = dirs["full_resolution"] / f"{client_stem}.png"
        shutil.copy2(master, full_resolution)
        high_quality = dirs["client_jpeg_2048"] / f"{client_stem}.jpg"
        light = dirs["web_jpeg_1600"] / f"{client_stem}.jpg"
        preview = dirs["prepayment_preview"] / f"{client_stem}.jpg"
        save_jpeg(master, high_quality, 2048, 92)
        save_jpeg(master, light, 1600, 88)
        preview_source = package / "portfolio_framed_preview" / filename
        if not preview_source.exists():
            raise SystemExit(f"Approved framed preview with footer is missing: {preview_source}")
        framed = build_client_preview_frame(preview_source, args.font, stone_texture)
        add_preview_mark(framed, preview, args.font, args.order_id)
        records.append({"master": master.as_posix(), "master_sha256": sha256(master), "full_resolution": full_resolution.as_posix(), "full_resolution_sha256": sha256(full_resolution), "client_jpeg_2048": high_quality.as_posix(), "web_jpeg_1600": light.as_posix(), "prepayment_preview": preview.as_posix(), "watermark": f"ONYX / PRIVATE PREVIEW / ORDER {args.order_id}"})
    (delivery / "CLIENT_DELIVERY_MANIFEST_V1.json").write_text(json.dumps({"schema": "onyx.production.client_delivery", "order_id": args.order_id, "records": records}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    readme = write_client_readme(delivery, args.order_id)
    build_archives(delivery, args.order_id, readme)
    print(f"Built {len(records)} delivery sets in {delivery}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())



