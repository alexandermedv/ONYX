#!/usr/bin/env python3
"""Read-only personal media consolidation to an S3-compatible rclone remote.

The source roots are never modified.  This is intentionally dependency-free:
metadata support is conservative and unsupported media is retained in review.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import struct
import subprocess
import sys
import time
from collections import defaultdict
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".heic", ".heif", ".tif", ".tiff", ".dng", ".raw", ".cr2", ".nef", ".arw"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".m4v", ".avi", ".mkv", ".webm", ".wmv", ".mts", ".m2ts", ".3gp", ".mpg", ".mpeg"}
REPORT_NAMES = ("inventory.csv", "exact_duplicates.csv", "near_duplicates.csv", "quality_review.csv", "copy_manifest.csv", "errors.csv", "summary.md")


@dataclass
class Item:
    source_archive: str
    source_path: str
    relative_path: str
    filename: str
    extension: str
    size: int
    mtime_ns: int
    modification_timestamp: str
    media_type: str
    media_status: str = "valid_or_unparsed"
    sha256: str = ""
    capture_timestamp: str = ""
    date_source: str = "filesystem_mtime"
    width: str = ""
    height: str = ""
    duration_seconds: str = ""
    status: str = "KEEP"
    selected_destination: str = ""
    canonical_source_path: str = ""
    notes: str = ""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(4 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def iso_from_timestamp(value: float) -> str:
    return datetime.fromtimestamp(value).astimezone().isoformat(timespec="seconds")


def read_jpeg_metadata(path: Path) -> tuple[str, str, str]:
    """Return DateTimeOriginal (if present), width and height without a decoder."""
    try:
        payload = path.read_bytes()
    except OSError:
        return "", "", ""
    if not payload.startswith(b"\xff\xd8"):
        return "", "", ""
    exif_date = ""
    index = 2
    while index + 4 <= len(payload):
        if payload[index] != 0xFF:
            index += 1
            continue
        marker = payload[index + 1]
        index += 2
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            continue
        if index + 2 > len(payload):
            break
        length = struct.unpack(">H", payload[index:index + 2])[0]
        if length < 2 or index + length > len(payload):
            break
        segment = payload[index + 2:index + length]
        if marker == 0xE1 and segment.startswith(b"Exif\x00\x00"):
            exif_date = exif_datetime_original(segment[6:])
        if marker in {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF} and len(segment) >= 5:
            return exif_date, str(struct.unpack(">H", segment[3:5])[0]), str(struct.unpack(">H", segment[1:3])[0])
        index += length
    return exif_date, "", ""


def exif_datetime_original(tiff: bytes) -> str:
    try:
        order = tiff[:2]
        endian = "<" if order == b"II" else ">" if order == b"MM" else ""
        if not endian or struct.unpack(endian + "H", tiff[2:4])[0] != 42:
            return ""

        def entries(offset: int) -> dict[int, tuple[int, int, int]]:
            count = struct.unpack(endian + "H", tiff[offset:offset + 2])[0]
            result: dict[int, tuple[int, int, int]] = {}
            for n in range(count):
                start = offset + 2 + n * 12
                tag, typ, num, value = struct.unpack(endian + "HHII", tiff[start:start + 12])
                result[tag] = (typ, num, value)
            return result

        ifd0 = entries(struct.unpack(endian + "I", tiff[4:8])[0])
        pointer = ifd0.get(0x8769)
        if not pointer:
            return ""
        original = entries(pointer[2]).get(0x9003)
        if not original:
            return ""
        start, length = original[2], original[1]
        value = tiff[start:start + length].split(b"\x00", 1)[0].decode("ascii", "ignore")
        return datetime.strptime(value, "%Y:%m:%d %H:%M:%S").isoformat()
    except (IndexError, ValueError, struct.error):
        return ""


def image_dimensions(path: Path) -> tuple[str, str, str]:
    ext = path.suffix.lower()
    try:
        with path.open("rb") as handle:
            header = handle.read(32)
        if ext in {".jpg", ".jpeg"}:
            return read_jpeg_metadata(path)
        if header.startswith(b"\x89PNG\r\n\x1a\n"):
            return "", str(struct.unpack(">I", header[16:20])[0]), str(struct.unpack(">I", header[20:24])[0])
        if header[:6] in (b"GIF87a", b"GIF89a"):
            return "", str(struct.unpack("<H", header[6:8])[0]), str(struct.unpack("<H", header[8:10])[0])
        if header.startswith(b"BM"):
            return "", str(struct.unpack("<I", header[18:22])[0]), str(abs(struct.unpack("<i", header[22:26])[0]))
    except (OSError, struct.error):
        pass
    return "", "", ""


def ffprobe(path: Path, executable: str) -> dict[str, Any]:
    command = [executable, "-v", "error", "-show_entries", "format=duration:format_tags=creation_time:stream=codec_type,width,height:stream_tags=creation_time", "-of", "json", str(path)]
    completed = subprocess.run(command, capture_output=True, text=True, timeout=120)
    if completed.returncode:
        raise RuntimeError(completed.stderr.strip() or "ffprobe failed")
    return json.loads(completed.stdout)


def video_metadata(path: Path, executable: str | None) -> tuple[str, str, str, str]:
    if not executable:
        return "", "", "", ""
    data = ffprobe(path, executable)
    creation = data.get("format", {}).get("tags", {}).get("creation_time", "")
    width = height = ""
    for stream in data.get("streams", []):
        if stream.get("codec_type") == "video":
            width, height = str(stream.get("width", "")), str(stream.get("height", ""))
            creation = creation or stream.get("tags", {}).get("creation_time", "")
            break
    return creation, width, height, str(data.get("format", {}).get("duration", ""))


def classify(path: Path) -> str:
    extension = path.suffix.lower()
    if extension in PHOTO_EXTENSIONS:
        return "photo"
    if extension in VIDEO_EXTENSIONS:
        return "video"
    return "other"


def walk_files(root: Path) -> Iterable[Path]:
    for current, directories, filenames in os.walk(root, topdown=True):
        directories.sort(key=str.casefold)
        for filename in sorted(filenames, key=str.casefold):
            yield Path(current) / filename


def safe_name(item: Item, used: dict[str, str]) -> str:
    name = item.filename
    candidate = name
    if candidate in used and used[candidate] != item.sha256:
        stem, ext = os.path.splitext(name)
        candidate = f"{stem}__{item.sha256[:8]}{ext}"
    used[candidate] = item.sha256
    return candidate


def organise_path(item: Item, filename: str) -> str:
    if item.media_status == "corrupt_or_unreadable":
        return f"archive/media/review/corrupt/{filename}"
    if item.media_type == "other":
        return f"archive/media/review/unsupported/{filename}"
    date = item.capture_timestamp or item.modification_timestamp
    match = re.match(r"(\d{4})-(\d{2})", date)
    if match:
        year, month = match.groups()
        kind = "photos" if item.media_type == "photo" else "videos"
        return f"archive/media/{kind}/{year}/{year}-{month}/{filename}"
    kind = "photos" if item.media_type == "photo" else "videos"
    return f"archive/media/{kind}/unknown-date/{filename}"


def write_csv(path: Path, rows: Iterable[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def rclone(command: list[str], executable: str, timeout: int = 600) -> subprocess.CompletedProcess[str]:
    return subprocess.run([executable, *command], text=True, capture_output=True, timeout=timeout)


def remote_size(remote: str, executable: str) -> int | None:
    outcome = rclone(["lsjson", remote], executable)
    if outcome.returncode:
        raise RuntimeError(outcome.stderr.strip() or outcome.stdout.strip() or "rclone lsjson failed")
    entries = json.loads(outcome.stdout)
    return int(entries[0]["Size"]) if entries else None


def snapshot_sources(sources: list[tuple[str, Path]]) -> dict[str, dict[str, int]]:
    """Read-only count/byte snapshot used to detect source changes."""
    result: dict[str, dict[str, int]] = {}
    for name, root in sources:
        files = total_bytes = 0
        for path in walk_files(root):
            stat = path.stat()
            files += 1
            total_bytes += stat.st_size
        result[name] = {"files": files, "bytes": total_bytes}
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", action="append", required=True, metavar="NAME=PATH")
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--rclone", required=True)
    parser.add_argument("--remote", default="minio-alexander")
    parser.add_argument("--ffprobe")
    parser.add_argument("--reuse-inventory", help="Reuse a prior inventory and scan only source files absent from it.")
    parser.add_argument("--retry-failed", action="store_true", help="Retry only FAILED entries from the existing copy manifest.")
    parser.add_argument("--copy-timeout-seconds", type=int, default=600, help="Per-object rclone copy timeout (default: 600).")
    parser.add_argument("--copy", action="store_true", help="Upload canonical mapped files after inventory.")
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    errors: list[dict[str, str]] = []
    fatal_inventory_errors: list[dict[str, str]] = []
    sources: list[tuple[str, Path]] = []
    for source in args.source:
        name, raw_path = source.split("=", 1)
        root = Path(raw_path)
        if not root.is_dir():
            raise SystemExit(f"Source is not an accessible directory: {root}")
        sources.append((name, root))
    if not Path(args.rclone).is_file():
        raise SystemExit("rclone executable is not accessible")

    items: list[Item] = []
    if args.reuse_inventory:
        with Path(args.reuse_inventory).open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                row["size"] = int(row["size"])
                row["mtime_ns"] = int(row["mtime_ns"])
                row.setdefault("media_status", "valid_or_unparsed")
                items.append(Item(**row))
    known_paths = {item.source_path for item in items}
    for archive_name, root in sources:
        for path in walk_files(root):
            if str(path) in known_paths:
                continue
            try:
                stat = path.stat()
                media_type = classify(path)
                item = Item(archive_name, str(path), str(path.relative_to(root)), path.name, path.suffix.lower(), stat.st_size, stat.st_mtime_ns, iso_from_timestamp(stat.st_mtime), media_type)
                if not stat.st_size:
                    item.status, item.notes = "TECHNICAL_REJECT", "zero-byte file"
                else:
                    item.sha256 = sha256_file(path)
                    if media_type == "photo":
                        item.capture_timestamp, item.width, item.height = image_dimensions(path)
                        if item.capture_timestamp:
                            item.date_source = "EXIF_DateTimeOriginal"
                    elif media_type == "video":
                        try:
                            item.capture_timestamp, item.width, item.height, item.duration_seconds = video_metadata(path, args.ffprobe)
                            if item.capture_timestamp:
                                item.date_source = "video_creation_time"
                            if item.duration_seconds and float(item.duration_seconds) <= 0:
                                item.status, item.notes = "TECHNICAL_REJECT", "zero-duration video"
                        except Exception as exc:
                            item.media_status = "corrupt_or_unreadable"
                            item.status = "REVIEW_TECHNICAL_REJECT"
                            item.notes = "MP4 container unreadable: moov atom not found"
                            errors.append({"source_path": str(path), "stage": "media_metadata", "error": str(exc)})
                    elif media_type == "other":
                        item.status, item.notes = "REVIEW", "unsupported media type retained in review"
                items.append(item)
            except Exception as exc:  # A missing hash/stat record makes inventory incomplete.
                record = {"source_path": str(path), "stage": "inventory", "error": str(exc)}
                errors.append(record)
                fatal_inventory_errors.append(record)

    groups: dict[str, list[Item]] = defaultdict(list)
    for item in items:
        if item.sha256:
            groups[item.sha256].append(item)
    duplicate_rows: list[dict[str, Any]] = []
    canonical: list[Item] = []
    for digest, group in groups.items():
        group.sort(key=lambda value: (value.relative_path.casefold(), value.source_path.casefold()))
        chosen = group[0]
        canonical.append(chosen)
        for item in group:
            item.canonical_source_path = chosen.source_path
            if item is not chosen:
                item.status = "EXACT_DUPLICATE"
            duplicate_rows.append({"sha256": digest, "canonical_source_path": chosen.source_path, "source_path": item.source_path, "size": item.size, "is_canonical": item is chosen})

    used_by_directory: dict[str, dict[str, str]] = defaultdict(dict)
    for item in canonical:
        if item.status == "TECHNICAL_REJECT":
            continue
        prototype = organise_path(item, item.filename)
        directory = str(Path(prototype).parent).replace("\\", "/")
        filename = safe_name(item, used_by_directory[directory])
        item.selected_destination = organise_path(item, filename)
    for item in items:
        if item.status == "EXACT_DUPLICATE":
            item.selected_destination = next(candidate.selected_destination for candidate in canonical if candidate.source_path == item.canonical_source_path)

    inventory_fields = list(asdict(items[0]).keys()) if items else list(asdict(Item("", "", "", "", "", 0, 0, "", "")).keys())
    write_csv(run_dir / "inventory.csv", (asdict(item) for item in items), inventory_fields)
    write_csv(run_dir / "exact_duplicates.csv", duplicate_rows, ["sha256", "canonical_source_path", "source_path", "size", "is_canonical"])
    write_csv(run_dir / "near_duplicates.csv", [{"status": "SKIPPED", "reason": "No Pillow/OpenCV image decoder installed; no new dependency installed during night run."}], ["status", "reason"])
    quality_rows = [{"source_path": item.source_path, "status": item.status, "reason": item.notes} for item in items if item.status != "KEEP"]
    write_csv(run_dir / "quality_review.csv", quality_rows, ["source_path", "status", "reason"])

    copy_rows: list[dict[str, Any]] = []
    retry_sources: set[str] | None = None
    if args.retry_failed:
        manifest_path = run_dir / "copy_manifest.csv"
        if not args.copy or not manifest_path.is_file():
            raise SystemExit("--retry-failed requires --copy and an existing copy_manifest.csv")
        prior_rows = list(csv.DictReader(manifest_path.open(newline="", encoding="utf-8")))
        retry_sources = {row["source_path"] for row in prior_rows if row["status"] == "FAILED"}
        if not retry_sources:
            raise SystemExit("No FAILED entries to retry")
        copy_rows = [row for row in prior_rows if row["source_path"] not in retry_sources]
    copy_stopped_for_system_error = False
    # A failed hash/metadata read means the inventory is incomplete.  Never
    # start a write phase from an inconsistent manifest.
    if fatal_inventory_errors and args.copy:
        args.copy = False
    if args.copy:
        consecutive_copy_failures = 0
        for item in canonical:
            if retry_sources is not None and item.source_path not in retry_sources:
                continue
            if item.status == "TECHNICAL_REJECT" or not item.selected_destination:
                continue
            path = Path(item.source_path)
            try:
                current = path.stat()
                if current.st_size != item.size or current.st_mtime_ns != item.mtime_ns:
                    raise RuntimeError("source changed since inventory; upload stopped for this file")
                target = f"{args.remote}:alexander/{item.selected_destination}"
                existing = remote_size(target, args.rclone)
                if existing is not None:
                    if existing != item.size:
                        raise RuntimeError(f"destination collision: existing size {existing}, source size {item.size}")
                    outcome = "already_present_same_size"
                else:
                    result = rclone(["copyto", str(path), target], args.rclone, timeout=args.copy_timeout_seconds)
                    if result.returncode:
                        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "rclone copyto failed")
                    verified_size = remote_size(target, args.rclone)
                    if verified_size != item.size:
                        raise RuntimeError(f"remote size mismatch: expected {item.size}, got {verified_size}")
                    outcome = "copied_size_verified"
                copy_rows.append({"source_path": item.source_path, "destination": item.selected_destination, "sha256": item.sha256, "size": item.size, "status": outcome})
                consecutive_copy_failures = 0
            except Exception as exc:
                errors.append({"source_path": item.source_path, "stage": "copy", "error": str(exc)})
                copy_rows.append({"source_path": item.source_path, "destination": item.selected_destination, "sha256": item.sha256, "size": item.size, "status": "FAILED"})
                consecutive_copy_failures += 1
                if consecutive_copy_failures >= 3:
                    copy_stopped_for_system_error = True
                    errors.append({"source_path": "", "stage": "copy", "error": "stopped after three consecutive storage/network failures"})
                    break

    write_csv(run_dir / "copy_manifest.csv", copy_rows, ["source_path", "destination", "sha256", "size", "status"])
    write_csv(run_dir / "errors.csv", errors, ["source_path", "stage", "error"])
    source_stats = {name: {"files": sum(1 for item in items if item.source_archive == name), "bytes": sum(item.size for item in items if item.source_archive == name)} for name, _ in sources}
    post_source_stats: dict[str, dict[str, int]] | None = None
    source_integrity = "not_run"
    if args.copy:
        try:
            post_source_stats = snapshot_sources(sources)
            source_integrity = "PASS" if post_source_stats == source_stats else "FAIL"
            if source_integrity == "FAIL":
                errors.append({"source_path": "", "stage": "source_post_check", "error": "source counts or bytes changed during copy"})
        except Exception as exc:
            source_integrity = "ERROR"
            errors.append({"source_path": "", "stage": "source_post_check", "error": str(exc)})
    duplicates = sum(1 for item in items if item.status == "EXACT_DUPLICATE")
    savings = sum(item.size for item in items if item.status == "EXACT_DUPLICATE")
    copied = sum(1 for row in copy_rows if row["status"] in {"copied_size_verified", "already_present_same_size"})
    copied_bytes = sum(int(row["size"]) for row in copy_rows if row["status"] in {"copied_size_verified", "already_present_same_size"})
    corrupt_items = [item for item in items if item.media_status == "corrupt_or_unreadable"]
    corrupt_unique = len({item.sha256 for item in corrupt_items if item.sha256})
    corrupt_occurrences = len(corrupt_items)
    copied_photos = sum(1 for row in copy_rows if row["status"] in {"copied_size_verified", "already_present_same_size"} and next(item.media_type for item in canonical if item.source_path == row["source_path"]) == "photo")
    copied_videos = sum(1 for row in copy_rows if row["status"] in {"copied_size_verified", "already_present_same_size"} and next(item.media_type for item in canonical if item.source_path == row["source_path"]) == "video")
    copied_review = copied - copied_photos - copied_videos
    summary = ["# Personal media archive summary", "", f"- Generated: {datetime.now().astimezone().isoformat(timespec='seconds')}"]
    summary += [f"- Source {name}: {value['files']} files, {value['bytes']} bytes" for name, value in source_stats.items()]
    summary += [f"- Photos: {sum(item.media_type == 'photo' for item in items)}", f"- Videos: {sum(item.media_type == 'video' for item in items)}", f"- Other/review: {sum(item.media_type == 'other' for item in items)}", f"- Exact duplicate source copies: {duplicates}; dedup savings: {savings} bytes", f"- Corrupt unique files: {corrupt_unique}; corrupt source occurrences: {corrupt_occurrences}", "- Near-duplicate analysis: skipped (no image decoder dependency; no dependency installed).", f"- Canonical files copied or verified: {copied}", f"- Photos copied: {copied_photos}; videos copied: {copied_videos}; review files copied: {copied_review}", f"- Bytes copied or verified: {copied_bytes}", f"- Failed uploads: {sum(row['status'] == 'FAILED' for row in copy_rows)}", f"- Copy stopped for systemic error: {copy_stopped_for_system_error}", f"- Errors: {len(errors)}", f"- Source integrity post-check: {source_integrity}"]
    (run_dir / "summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")

    if args.copy:
        for report in REPORT_NAMES:
            result = rclone(["copyto", str(run_dir / report), f"{args.remote}:alexander/archive/media/system/{report}"], args.rclone)
            if result.returncode:
                errors.append({"source_path": str(run_dir / report), "stage": "report_upload", "error": result.stderr.strip()})
        write_csv(run_dir / "errors.csv", errors, ["source_path", "stage", "error"])
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
