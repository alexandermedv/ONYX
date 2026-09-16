"""Build repeatable ONYX client-delivery derivatives from approved masters."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


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


def add_preview_mark(source: Path, target: Path, font_path: Path, order_id: str) -> None:
    with Image.open(source) as image:
        image = image.convert("RGB")
        image.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
        overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        regular = ImageFont.truetype(str(font_path), 88)
        small = ImageFont.truetype(str(font_path), 28)
        cx, cy = image.width // 2, image.height // 2
        title = "ONYX"
        box = draw.textbbox((0, 0), title, font=regular)
        draw.text((cx - (box[2] - box[0]) // 2, cy - 55), title, font=regular,
                  fill=(246, 244, 239, 175), stroke_width=1, stroke_fill=(17, 17, 17, 80))
        label = f"PRIVATE PREVIEW  /  ORDER {order_id}"
        box = draw.textbbox((0, 0), label, font=small)
        draw.text((cx - (box[2] - box[0]) // 2, cy + 48), label, font=small,
                  fill=(246, 244, 239, 190), stroke_width=1, stroke_fill=(17, 17, 17, 90))
        for x, y in ((cx - 360, cy - 330), (cx + 260, cy + 300)):
            draw.text((x, y), title, font=small, fill=(246, 244, 239, 75),
                      stroke_width=1, stroke_fill=(17, 17, 17, 35))
        image = Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")
        image.save(target, "JPEG", quality=82, optimize=True, progressive=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("package", type=Path, help="Business_V1 package directory")
    parser.add_argument("--order-id", default="<ID>")
    parser.add_argument("--font", type=Path, required=True)
    args = parser.parse_args()
    package = args.package
    masters = sorted((package / "upscale_master").glob("*.png"))
    if not masters:
        masters = sorted((package / "upscale_p03_v1").glob("*.png")) + sorted((package / "upscale_p01_v1").glob("*.png")) + sorted((package / "upscale_p02_v1").glob("*.png"))
    if not masters:
        raise SystemExit("No approved upscale PNG masters found")
    delivery = package / "client_delivery"
    dirs = {"client_jpeg_2048": delivery / "client_jpeg_2048", "web_jpeg_1600": delivery / "web_jpeg_1600", "prepayment_preview": delivery / "prepayment_preview"}
    for directory in dirs.values(): directory.mkdir(parents=True, exist_ok=True)
    records = []
    for master in masters:
        filename = master.name.replace("_00001_", "").replace(".png", ".jpg")
        save_jpeg(master, dirs["client_jpeg_2048"] / filename, 2048, 92)
        save_jpeg(master, dirs["web_jpeg_1600"] / filename, 1600, 88)
        add_preview_mark(dirs["web_jpeg_1600"] / filename, dirs["prepayment_preview"] / filename, args.font, args.order_id)
        records.append({"master": master.as_posix(), "master_sha256": sha256(master), "client_jpeg_2048": (dirs["client_jpeg_2048"] / filename).as_posix(), "web_jpeg_1600": (dirs["web_jpeg_1600"] / filename).as_posix(), "prepayment_preview": (dirs["prepayment_preview"] / filename).as_posix(), "watermark": f"ONYX / PRIVATE PREVIEW / ORDER {args.order_id}"})
    (delivery / "CLIENT_DELIVERY_MANIFEST_V1.json").write_text(json.dumps({"schema": "onyx.production.client_delivery", "order_id": args.order_id, "records": records}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Built {len(records)} delivery sets in {delivery}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
