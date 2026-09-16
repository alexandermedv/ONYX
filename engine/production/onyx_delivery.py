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
    masters = discover_masters(package)
    if not masters:
        raise SystemExit("No approved upscale PNG masters found")
    if len(masters) != 10:
        raise SystemExit(f"Expected 10 approved masters, found {len(masters)}")
    delivery = package / "client_delivery"
    dirs = {"client_jpeg_2048": delivery / "client_jpeg_2048", "web_jpeg_1600": delivery / "web_jpeg_1600", "prepayment_preview": delivery / "prepayment_preview"}
    for directory in dirs.values(): directory.mkdir(parents=True, exist_ok=True)
    records = []
    for master in masters:
        filename = delivery_filename(master)
        save_jpeg(master, dirs["client_jpeg_2048"] / filename, 2048, 92)
        save_jpeg(master, dirs["web_jpeg_1600"] / filename, 1600, 88)
        preview_source = package / "portfolio_framed_preview" / filename
        if not preview_source.exists():
            raise SystemExit(f"Approved framed preview with footer is missing: {preview_source}")
        add_preview_mark(preview_source, dirs["prepayment_preview"] / filename, args.font, args.order_id)
        records.append({"master": master.as_posix(), "master_sha256": sha256(master), "client_jpeg_2048": (dirs["client_jpeg_2048"] / filename).as_posix(), "web_jpeg_1600": (dirs["web_jpeg_1600"] / filename).as_posix(), "prepayment_preview": (dirs["prepayment_preview"] / filename).as_posix(), "watermark": f"ONYX / PRIVATE PREVIEW / ORDER {args.order_id}"})
    (delivery / "CLIENT_DELIVERY_MANIFEST_V1.json").write_text(json.dumps({"schema": "onyx.production.client_delivery", "order_id": args.order_id, "records": records}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Built {len(records)} delivery sets in {delivery}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())



