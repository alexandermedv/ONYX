from __future__ import annotations

from pathlib import Path

from .models import SourceRecord


def create_selection_report(records: list[SourceRecord], output: Path) -> None:
    """Create a deterministic contact sheet using the already-installed Pillow stack."""
    from PIL import Image, ImageDraw, ImageFont, ImageOps
    selected = sorted((row for row in records if row.selection_rank), key=lambda row: row.selection_rank or 999)
    thumb_w, thumb_h, label_h, columns = 260, 260, 128, 4
    rows = (len(selected) + columns - 1) // columns
    canvas = Image.new("RGB", (columns * thumb_w, rows * (thumb_h + label_h)), "white")
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default()
    for index, record in enumerate(selected):
        x = (index % columns) * thumb_w
        y = (index // columns) * (thumb_h + label_h)
        with Image.open(record.source_path) as image:
            thumb = ImageOps.fit(image.convert("RGB"), (thumb_w, thumb_h))
        canvas.paste(thumb, (x, y))
        label = (
            f"#{record.selection_rank} {Path(record.source_path).name[:28]}\n"
            f"pose={record.pose_bucket} face={record.face_area_ratio or 0:.3f}\n"
            f"sharp={record.sharpness:.1f} exposure={record.exposure_mean:.1f}\n"
            f"identity={record.identity_similarity or 0:.3f} diversity={record.diversity_contribution or 0:.3f}\n"
            f"p-distance={record.perceptual_distance or 0:.3f} group={record.capture_group or 'legacy'}"
        )
        draw.multiline_text((x + 4, y + thumb_h + 4), label, fill="black", font=font, spacing=2)
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output)


def selection_rows(records: list[SourceRecord]) -> list[dict]:
    return [{
        "rank": row.selection_rank, "source": row.source_path, "memberships": "|".join(row.selected_memberships),
        "pose": row.pose_bucket, "face_size": row.face_area_ratio, "sharpness": row.sharpness,
        "exposure": row.exposure_mean, "identity_similarity": row.identity_similarity,
        "diversity_contribution": row.diversity_contribution, "selection_reason": row.selection_reason,
        "perceptual_distance": row.perceptual_distance,
        "capture_group": row.capture_group, "expression": row.expression_bucket,
        "lighting": row.lighting_bucket,
    } for row in sorted((item for item in records if item.selection_rank), key=lambda item: item.selection_rank or 999)]


def create_comparison_sheet(records: list[SourceRecord], old_filenames: list[str], output: Path) -> None:
    from PIL import Image, ImageDraw, ImageFont, ImageOps
    by_name = {Path(record.source_path).name: record for record in records}
    proposed = [record for record in sorted(records, key=lambda item: item.selection_rank or 999)
                if record.selection_rank and record.selection_rank <= 3]
    groups = [("A - old human candidate", [by_name[name] for name in old_filenames]),
              ("B - new selector proposal", proposed)]
    thumb_w, thumb_h, header_h, label_h = 300, 300, 42, 54
    canvas = Image.new("RGB", (3 * thumb_w, 2 * (header_h + thumb_h + label_h)), "white")
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default()
    for group_index, (title, items) in enumerate(groups):
        top = group_index * (header_h + thumb_h + label_h)
        draw.text((8, top + 10), title, fill="black", font=font)
        for index, record in enumerate(items):
            x, y = index * thumb_w, top + header_h
            with Image.open(record.source_path) as image:
                thumb = ImageOps.fit(image.convert("RGB"), (thumb_w, thumb_h))
            canvas.paste(thumb, (x, y))
            draw.multiline_text((x + 4, y + thumb_h + 4),
                                f"{index + 1}. {Path(record.source_path).name[:34]}\n"
                                f"pose={record.pose_bucket} identity={record.identity_similarity or 0:.3f}",
                                fill="black", font=font, spacing=2)
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output)
