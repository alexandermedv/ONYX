"""Build and verify a non-destructive P01 GPT portfolio pack."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import shutil
from datetime import date
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parent
PERSONA = ROOT.parents[1]
SOURCE_ROOT = PERSONA / "06_final_round_v1"
RAW = ROOT / "01_inputs_raw"
SELECTED = ROOT / "02_selected"
RESERVE = ROOT / "03_reserve"
SHEETS = ROOT / "04_contact_sheets"
METADATA = ROOT / "05_metadata"
PREVIEWS = ROOT / "06_preview_exports"
SUBDIRS = (RAW, SELECTED, RESERVE, SHEETS, METADATA, PREVIEWS)

PORTFOLIO = (
    {"source": "BUS02.png", "copied": "P01_PORT_01_HERO.png", "set": "selected", "scene_tag": "hero", "identity": 4, "commercial": 5, "beautification": "moderate", "diversity": "high", "notes": "Standing three-quarter office portrait with polished hero framing and clear identity."},
    {"source": "BUS06.png", "copied": "P01_PORT_02_DESK.png", "set": "selected", "scene_tag": "desk", "identity": 4, "commercial": 4, "beautification": "moderate", "diversity": "high", "notes": "Seated desk context, readable executive story, and technically clean hands."},
    {"source": "BUS05.png", "copied": "P01_PORT_03_LOUNGE.png", "set": "selected", "scene_tag": "lounge", "identity": 4, "commercial": 5, "beautification": "moderate", "diversity": "high", "notes": "Relaxed seated lounge variation with natural clasped hands and strong commercial composition."},
    {"source": "BUS08.png", "copied": "P01_PORT_04_LIBRARY.png", "set": "selected", "scene_tag": "library", "identity": 4, "commercial": 4, "beautification": "moderate", "diversity": "high", "notes": "Library environment adds scene variety while retaining a credible executive look."},
    {"source": "BUS09.png", "copied": "P01_PORT_05_FULLBODY.png", "set": "selected", "scene_tag": "fullbody", "identity": 4, "commercial": 4, "beautification": "moderate", "diversity": "high", "notes": "Head-to-shoes lobby frame provides the selected set's complete silhouette and suit presentation."},
    {"source": "BUS01.png", "copied": "P01_PORT_06_CLOSEUP.png", "set": "selected", "scene_tag": "closeup", "identity": 4, "commercial": 5, "beautification": "moderate", "diversity": "high", "notes": "Clean close portrait with direct eye contact and an appealing, controlled polished finish."},
    {"source": "BUS03.png", "copied": "P01_RESERVE_01.png", "set": "reserve", "scene_tag": "formal_desk", "identity": 4, "commercial": 4, "beautification": "moderate", "diversity": "medium", "notes": "Strong formal desk alternative, held in reserve because it overlaps the selected desk coverage."},
    {"source": "BUS04.png", "copied": "P01_RESERVE_02.png", "set": "reserve", "scene_tag": "lobby_standing", "identity": 4, "commercial": 4, "beautification": "moderate", "diversity": "medium", "notes": "Good standing lobby option; prominent background branding makes it less universally reusable."},
    {"source": "BUS07.png", "copied": "P01_RESERVE_03.png", "set": "reserve", "scene_tag": "standing", "identity": 4, "commercial": 4, "beautification": "moderate", "diversity": "medium", "notes": "Clean standing portrait, reserved because it overlaps hero and full-body coverage."},
    {"source": "BUS10.png", "copied": "P01_RESERVE_04.png", "set": "reserve", "scene_tag": "corridor", "identity": 4, "commercial": 4, "beautification": "moderate", "diversity": "medium", "notes": "Useful corridor alternate, reserved to keep the selected set more scene-diverse."},
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def font(size: int) -> ImageFont.ImageFont:
    for candidate in (Path("C:/Windows/Fonts/arial.ttf"), Path("C:/Windows/Fonts/segoeui.ttf")):
        if candidate.is_file():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def atomic_json(destination: Path, payload: Any) -> None:
    temporary = destination.with_suffix(destination.suffix + ".writing")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, destination)


def atomic_csv(destination: Path, rows: list[dict[str, Any]], columns: list[str]) -> None:
    temporary = destination.with_suffix(".writing.csv")
    with temporary.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, destination)


def copy_source(source: Path, destination: Path) -> None:
    if destination.exists():
        raise FileExistsError(destination)
    shutil.copy2(source, destination)
    if sha256(source) != sha256(destination):
        raise ValueError(f"copy hash mismatch: {source.name}")


def contact_sheet(records: list[dict[str, Any]], destination: Path, columns: int, label_size: int) -> None:
    cell_w, cell_h, label_h, margin = 500, 610, label_size + 26, 16
    rows = (len(records) + columns - 1) // columns
    canvas = Image.new("RGB", (columns * cell_w, rows * (cell_h + label_h)), "#f4f4f2")
    draw = ImageDraw.Draw(canvas)
    label_font = font(label_size)
    for index, record in enumerate(records):
        source = Path(record["copied_path"])
        with Image.open(source) as image:
            thumbnail = ImageOps.contain(image.convert("RGB"), (cell_w - margin * 2, cell_h - margin * 2), Image.Resampling.LANCZOS)
        x, y = (index % columns) * cell_w, (index // columns) * (cell_h + label_h)
        canvas.paste(thumbnail, (x + (cell_w - thumbnail.width) // 2, y + (cell_h - thumbnail.height) // 2))
        draw.text((x + margin, y + cell_h + 10), record["copied_filename"], fill="#141414", font=label_font)
    if destination.suffix.lower() == ".png":
        canvas.save(destination, optimize=True)
    else:
        canvas.save(destination, quality=92, optimize=True)


def preview(record: dict[str, Any]) -> None:
    with Image.open(record["copied_path"]) as image:
        preview_image = ImageOps.contain(image.convert("RGB"), (1600, 1600), Image.Resampling.LANCZOS)
    preview_image.save(PREVIEWS / (Path(record["copied_filename"]).stem + ".jpg"), quality=90, optimize=True)


def write_readme(records: list[dict[str, Any]]) -> None:
    selected = [record for record in records if record["set"] == "selected"]
    reserve = [record for record in records if record["set"] == "reserve"]
    lines = ["# P01 GPT portfolio v1", "", "This package is a curated portfolio pack for P01_M30_Corporate, built from ten existing GPT-generated final-round images. It is not a benchmark, and it does not replace the benchmark, blind review, or qualifier records.", "", "The selection permits controlled beautification: fresher skin, favourable light, and a polished business look are appropriate when identity remains recognizably P01. The selected set optimizes scene variety and commercial appeal; reserve frames remain available as alternates.", "", f"Created: {date.today().isoformat()}", "", "## Selected", ""]
    for record in selected:
        lines.append(f"- `{record['copied_filename']}` — {record['notes']}")
    lines.extend(["", "## Reserve", ""])
    for record in reserve:
        lines.append(f"- `{record['copied_filename']}` — {record['notes']}")
    lines.extend(["", "## Preservation", "", "Original final-round images remain unchanged in `06_final_round_v1`. Raw and selected/reserve copies preserve the source PNG bytes and SHA256. JPEG files in `06_preview_exports` and `04_contact_sheets` are derived previews only."])
    (ROOT / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build() -> None:
    if not SOURCE_ROOT.is_dir():
        raise FileNotFoundError(SOURCE_ROOT)
    if ROOT.exists() and any(path.is_file() and path.name != "build_portfolio.py" and "__pycache__" not in path.parts for path in ROOT.rglob("*")):
        raise FileExistsError("portfolio destination already contains files; refusing to overwrite")
    sources = [SOURCE_ROOT / record["source"] for record in PORTFOLIO]
    missing = [str(source) for source in sources if not source.is_file()]
    if missing:
        raise FileNotFoundError("\n".join(missing))
    for directory in SUBDIRS:
        directory.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, Any]] = []
    for rank, item in enumerate(PORTFOLIO, 1):
        source = SOURCE_ROOT / item["source"]
        raw_destination = RAW / item["source"]
        destination = (SELECTED if item["set"] == "selected" else RESERVE) / item["copied"]
        copy_source(source, raw_destination)
        copy_source(source, destination)
        with Image.open(source) as image:
            width, height = image.size
        records.append({"rank_in_portfolio": rank, "source_filename": item["source"], "source_path": str(source.resolve()), "copied_filename": item["copied"], "copied_path": str(destination.resolve()), "set": item["set"], "scene_tag": item["scene_tag"], "sha256": sha256(source), "width": width, "height": height, "orientation": "portrait" if height > width else "landscape" if width > height else "square", "identity_score": item["identity"], "commercial_score": item["commercial"], "scene_diversity_value": item["diversity"], "beautification_level": item["beautification"], "notes": item["notes"]})
    selected = [record for record in records if record["set"] == "selected"]
    contact_sheet(records, SHEETS / "contact_sheet_all_10.jpg", columns=5, label_size=18)
    contact_sheet(selected, SHEETS / "contact_sheet_selected_6.jpg", columns=3, label_size=20)
    contact_sheet(selected, SHEETS / "contact_sheet_selected_6_labeled.png", columns=3, label_size=28)
    for record in selected:
        preview(record)
    atomic_json(METADATA / "portfolio_manifest.json", {"schema": "onyx.p01.gpt_portfolio", "schema_version": "1.0", "created_on": date.today().isoformat(), "source_directory": str(SOURCE_ROOT.resolve()), "source_image_count": 10, "selected_count": 6, "reserve_count": 4, "preservation": "Source images are read-only. Raw and selected/reserve copies have matching SHA256; previews and contact sheets are derived only.", "images": records})
    atomic_csv(METADATA / "portfolio_selection.csv", records, ["rank_in_portfolio", "source_filename", "copied_filename", "set", "scene_tag", "identity_score", "commercial_score", "scene_diversity_value", "beautification_level", "notes"])
    write_readme(records)


def verify() -> dict[str, Any]:
    manifest_path = METADATA / "portfolio_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    records = manifest["images"]
    errors: list[str] = []
    if len(records) != 10 or sum(record["set"] == "selected" for record in records) != 6 or sum(record["set"] == "reserve" for record in records) != 4:
        errors.append("portfolio set counts are invalid")
    if len({record["source_filename"] for record in records}) != 10 or len({record["copied_filename"] for record in records}) != 10:
        errors.append("source or portfolio filenames are duplicated")
    for record in records:
        source, raw, copied = Path(record["source_path"]), RAW / record["source_filename"], Path(record["copied_path"])
        if not all(path.is_file() for path in (source, raw, copied)):
            errors.append(f"missing copy: {record['source_filename']}")
            continue
        if len({sha256(source), sha256(raw), sha256(copied), record["sha256"]}) != 1:
            errors.append(f"hash mismatch: {record['source_filename']}")
        try:
            with Image.open(copied) as image:
                image.verify()
        except Exception as exc:
            errors.append(f"not decodable: {record['copied_filename']}: {exc}")
    for name in ("contact_sheet_all_10.jpg", "contact_sheet_selected_6.jpg", "contact_sheet_selected_6_labeled.png"):
        try:
            with Image.open(SHEETS / name) as image:
                image.verify()
        except Exception as exc:
            errors.append(f"bad contact sheet {name}: {exc}")
    previews = list(PREVIEWS.glob("*.jpg"))
    if len(previews) != 6:
        errors.append("preview count is not six")
    for image_path in previews:
        with Image.open(image_path) as image:
            if max(image.size) > 1600:
                errors.append(f"preview too large: {image_path.name}")
    with (METADATA / "portfolio_selection.csv").open(encoding="utf-8-sig", newline="") as stream:
        if len(list(csv.DictReader(stream))) != 10:
            errors.append("selection CSV does not have ten rows")
    return {"ok": not errors, "errors": errors, "source_images": 10, "selected": 6, "reserve": 4, "previews": len(previews)}


def finish_partial_build() -> None:
    """Finish derived metadata after a recoverable write failure; never recopy inputs."""
    manifest = json.loads((METADATA / "portfolio_manifest.json").read_text(encoding="utf-8-sig"))
    records = manifest["images"]
    selected = [record for record in records if record["set"] == "selected"]
    contact_sheet(records, SHEETS / "contact_sheet_all_10.jpg", columns=5, label_size=18)
    contact_sheet(selected, SHEETS / "contact_sheet_selected_6.jpg", columns=3, label_size=20)
    contact_sheet(selected, SHEETS / "contact_sheet_selected_6_labeled.png", columns=3, label_size=28)
    for record in selected:
        preview(record)
    atomic_csv(METADATA / "portfolio_selection.csv", records, ["rank_in_portfolio", "source_filename", "copied_filename", "set", "scene_tag", "identity_score", "commercial_score", "scene_diversity_value", "beautification_level", "notes"])
    write_readme(records)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--finish-partial-build", action="store_true")
    args = parser.parse_args()
    if args.verify:
        result = verify()
    elif args.finish_partial_build:
        finish_partial_build()
        result = verify()
    else:
        build()
        result = verify()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
