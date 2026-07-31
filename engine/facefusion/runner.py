#!/usr/bin/env python3
"""
ONYX FaceFusion Runner v3.0

Batch face replacement using FaceFusion.

This module intentionally does not know anything about ONYX,
Job Engine or settings.yaml.
It simply receives folders from Job Engine and performs face swapping.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


IMAGE_SUFFIXES = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}


def images_in(folder: Path) -> list[Path]:
    """Return all supported images inside folder."""
    return sorted(
        path
        for path in folder.iterdir()
        if path.is_file()
        and path.suffix.lower() in IMAGE_SUFFIXES
    )


def main() -> int:

    parser = argparse.ArgumentParser(
        description="ONYX FaceFusion Runner"
    )

    parser.add_argument(
        "--facefusion-folder",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "--python",
        default=sys.executable,
    )

    parser.add_argument(
        "--source-dir",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "--target-dir",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "--model",
        default="hyperswap_1a_256",
    )

    parser.add_argument(
        "--reference-distance",
        type=float,
        default=0.30,
    )

    args = parser.parse_args()

    # --------------------------------------------------
    # Resolve paths
    # --------------------------------------------------

    args.facefusion_folder = args.facefusion_folder.resolve()
    args.source_dir = args.source_dir.resolve()
    args.target_dir = args.target_dir.resolve()
    args.output_dir = args.output_dir.resolve()

    python_executable = Path(args.python).resolve()

    if not args.facefusion_folder.exists():
        parser.error(
            f"FaceFusion folder not found:\n{args.facefusion_folder}"
        )

    if not python_executable.exists():
        parser.error(
            f"Python executable not found:\n{python_executable}"
        )

    if not args.source_dir.exists():
        parser.error(
            f"Source folder not found:\n{args.source_dir}"
        )

    if not args.target_dir.exists():
        parser.error(
            f"Target folder not found:\n{args.target_dir}"
        )

    args.output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    sources = images_in(args.source_dir)
    targets = images_in(args.target_dir)

    if not sources:
        parser.error(
            f"No client photos found in\n{args.source_dir}"
        )

    if not targets:
        parser.error(
            f"No target scenes found in\n{args.target_dir}"
        )

    log_file = args.output_dir / "facefusion.log"

    print("=" * 80)
    print("ONYX FaceFusion Runner")
    print("=" * 80)
    print(f"FaceFusion : {args.facefusion_folder}")
    print(f"Python     : {python_executable}")
    print(f"Source     : {args.source_dir}")
    print(f"Targets    : {args.target_dir}")
    print(f"Output     : {args.output_dir}")
    print(f"Model      : {args.model}")
    print(f"Reference  : {args.reference_distance}")
    print("=" * 80)
    print(f"Client photos : {len(sources)}")
    print(f"Scenes        : {len(targets)}")
    print("=" * 80)

    success = 0

    for index, target in enumerate(targets, start=1):

        output = args.output_dir / target.name

        command = [
            str(python_executable),
            "facefusion.py",
            "headless-run",

            "-s",
            *(str(photo) for photo in sources),

            "-t",
            str(target),

            "-o",
            str(output),

            "--processors",
            "face_swapper",

            "--face-swapper-model",
            args.model,

            "--face-selector-mode",
            "reference",

            "--reference-face-distance",
            str(args.reference_distance),
        ]

        started = time.monotonic()

        result = subprocess.run(
            command,
            cwd=args.facefusion_folder,
            capture_output=True,
            text=True,
        )

        elapsed = time.monotonic() - started

        ok = (
            result.returncode == 0
            and output.exists()
        )

        status = "OK" if ok else "ERROR"

        with log_file.open(
            "a",
            encoding="utf-8",
        ) as log:

            log.write(
                f"{datetime.now():%Y-%m-%d %H:%M:%S} | "
                f"{target.name} | "
                f"{status} | "
                f"{elapsed:.1f} sec\n"
            )

            if result.stdout:
                log.write(result.stdout)
                log.write("\n")

            if result.stderr:
                log.write(result.stderr)
                log.write("\n")

        print(
            f"[{index}/{len(targets)}] "
            f"{target.name}: "
            f"{status} "
            f"({elapsed:.1f} sec)"
        )

        if ok:
            success += 1
        else:

            if result.stderr:
                print(result.stderr.strip())

            if result.stdout:
                print(result.stdout.strip())

    failed = len(targets) - success

    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Successful : {success}")
    print(f"Failed     : {failed}")
    print(f"Output     : {args.output_dir}")
    print("=" * 80)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())