from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import cv2
import numpy as np
import pandas as pd


# ============================================================
# CUDA / cuDNN runtime
# ============================================================

if sys.platform == "win32":
    site_packages = Path(sys.executable).parent / "Lib" / "site-packages"

    nvidia_bin_dirs = [
        site_packages / "nvidia" / "cudnn" / "bin",
        site_packages / "nvidia" / "cublas" / "bin",
        site_packages / "nvidia" / "cuda_runtime" / "bin",
        site_packages / "nvidia" / "cufft" / "bin",
        site_packages / "nvidia" / "curand" / "bin",
        site_packages / "nvidia" / "nvjitlink" / "bin",
    ]

    for dll_dir in nvidia_bin_dirs:
        if dll_dir.exists():
            os.add_dll_directory(str(dll_dir))
            os.environ["PATH"] = (
                str(dll_dir)
                + os.pathsep
                + os.environ.get("PATH", "")
            )


import onnxruntime as ort

ort.preload_dlls(directory="")

from insightface.app import FaceAnalysis


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


# ============================================================
# InsightFace
# ============================================================

def load_analyzer() -> FaceAnalysis:
    app = FaceAnalysis(
        name="buffalo_l",
        providers=[
            "CUDAExecutionProvider",
            "CPUExecutionProvider",
        ],
    )

    app.prepare(
        ctx_id=0,
        det_size=(640, 640),
    )

    return app


# ============================================================
# Image IO
# ============================================================

def read_image(path: Path):
    """Unicode-safe image loading on Windows."""
    data = np.fromfile(path, dtype=np.uint8)

    if data.size == 0:
        return None

    return cv2.imdecode(data, cv2.IMREAD_COLOR)


def get_images(folder: Path) -> list[Path]:
    return sorted(
        p
        for p in folder.iterdir()
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    )


# ============================================================
# Face analysis
# ============================================================

def analyze_face(
    app: FaceAnalysis,
    image_path: Path,
) -> tuple[np.ndarray | None, dict]:

    image = read_image(image_path)

    if image is None:
        return None, {
            "face_detected": False,
            "face_count": 0,
            "face_area_ratio": np.nan,
            "error": "cannot_read_image",
        }

    faces = app.get(image)

    if not faces:
        return None, {
            "face_detected": False,
            "face_count": 0,
            "face_area_ratio": 0.0,
            "error": "no_face_detected",
        }

    # For portrait QA the primary person is assumed to be
    # the largest detected face.
    face = max(
        faces,
        key=lambda f: (
            (f.bbox[2] - f.bbox[0])
            * (f.bbox[3] - f.bbox[1])
        ),
    )

    embedding = np.asarray(
        face.normed_embedding,
        dtype=np.float32,
    )

    height, width = image.shape[:2]

    bbox_width = float(face.bbox[2] - face.bbox[0])
    bbox_height = float(face.bbox[3] - face.bbox[1])

    area_ratio = (
        bbox_width * bbox_height
    ) / float(width * height)

    return embedding, {
        "face_detected": True,
        "face_count": len(faces),
        "face_area_ratio": area_ratio,
        "error": "",
    }


def cosine_similarity(
    a: np.ndarray,
    b: np.ndarray,
) -> float:
    # normed_embedding is already L2-normalized.
    return float(np.dot(a, b))


# ============================================================
# Reference profile
# ============================================================

def build_reference_profile(
    app: FaceAnalysis,
    reference_folder: Path,
) -> tuple[list[str], list[np.ndarray]]:

    images = get_images(reference_folder)

    if len(images) < 2:
        raise RuntimeError(
            f"At least 2 reference images required; "
            f"found {len(images)}"
        )

    names: list[str] = []
    embeddings: list[np.ndarray] = []

    print()
    print("REFERENCE PROFILE")
    print("=" * 72)

    for index, path in enumerate(images, start=1):

        print(
            f"[{index}/{len(images)}] {path.name}",
            end=" ... ",
            flush=True,
        )

        embedding, info = analyze_face(app, path)

        if embedding is None:
            print(f"FAILED ({info['error']})")
            continue

        names.append(path.name)
        embeddings.append(embedding)

        print(
            f"OK | faces={info['face_count']} "
            f"| area={info['face_area_ratio']:.3f}"
        )

    if len(embeddings) < 2:
        raise RuntimeError(
            "Not enough valid reference faces."
        )

    return names, embeddings


# ============================================================
# Calibration
# ============================================================

def run_calibration(
    app: FaceAnalysis,
    reference_folder: Path,
    output: Path,
) -> None:

    names, embeddings = build_reference_profile(
        app,
        reference_folder,
    )

    matrix = np.zeros(
        (len(names), len(names)),
        dtype=np.float32,
    )

    for i, emb_a in enumerate(embeddings):
        for j, emb_b in enumerate(embeddings):
            matrix[i, j] = cosine_similarity(
                emb_a,
                emb_b,
            )

    df = pd.DataFrame(
        matrix,
        index=names,
        columns=names,
    )

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        output,
        encoding="utf-8-sig",
    )

    print()
    print("COSINE SIMILARITY")
    print("=" * 72)
    print(df.round(3).to_string())

    pair_scores = [
        matrix[i, j]
        for i in range(len(names))
        for j in range(i + 1, len(names))
    ]

    print()
    print("REFERENCE BASELINE")
    print("=" * 72)
    print(f"Pairs : {len(pair_scores)}")
    print(f"Min   : {np.min(pair_scores):.3f}")
    print(f"Mean  : {np.mean(pair_scores):.3f}")
    print(f"Median: {np.median(pair_scores):.3f}")
    print(f"Max   : {np.max(pair_scores):.3f}")
    print()
    print(f"CSV   : {output.resolve()}")


# ============================================================
# Job analysis
# ============================================================

def run_job_analysis(
    app: FaceAnalysis,
    reference_folder: Path,
    manifest_path: Path,
    output: Path,
    summary_output: Path,
) -> None:

    reference_names, reference_embeddings = (
        build_reference_profile(
            app,
            reference_folder,
        )
    )

    with manifest_path.open(
        "r",
        encoding="utf-8-sig",
    ) as f:
        manifest = json.load(f)

    postprocess = manifest.get("postprocess", {})
    runs = postprocess.get("runs", [])

    if not runs:
        raise RuntimeError(
            "Manifest contains no postprocess.runs"
        )

    # We measure identity BEFORE upscale.
    candidates = [
        r
        for r in runs
        if r.get("status") == "completed"
        and r.get("source")
    ]

    print()
    print("JOB ANALYSIS")
    print("=" * 72)
    print(f"Job        : {manifest.get('job_id')}")
    print(f"Candidates : {len(candidates)}")
    print(f"References : {len(reference_embeddings)}")
    print("=" * 72)

    rows = []

    for index, candidate in enumerate(
        candidates,
        start=1,
    ):

        scene_id = candidate.get(
            "scene_id",
            "",
        )

        method = candidate.get(
            "method",
            "",
        )

        source = Path(candidate["source"])

        print(
            f"[{index:03d}/{len(candidates):03d}] "
            f"{scene_id} | {method}",
            end=" ... ",
            flush=True,
        )

        embedding, face_info = analyze_face(
            app,
            source,
        )

        row = {
            "job_id": manifest.get(
                "job_id",
                "",
            ),
            "scene_id": scene_id,
            "method": method,
            "source": str(source),
            "postprocessed_output": candidate.get(
                "output",
                "",
            ),
            "face_detected": face_info[
                "face_detected"
            ],
            "face_count": face_info[
                "face_count"
            ],
            "face_area_ratio": face_info[
                "face_area_ratio"
            ],
            "error": face_info["error"],
        }

        if embedding is None:
            for ref_index in range(
                len(reference_embeddings)
            ):
                row[
                    f"sim_ref_{ref_index + 1}"
                ] = np.nan

            row["sim_min"] = np.nan
            row["sim_mean"] = np.nan
            row["sim_median"] = np.nan
            row["sim_max"] = np.nan
            row["reference_best"] = ""

            print(
                f"FAILED ({face_info['error']})"
            )

        else:

            similarities = [
                cosine_similarity(
                    embedding,
                    ref_embedding,
                )
                for ref_embedding
                in reference_embeddings
            ]

            for ref_index, score in enumerate(
                similarities
            ):
                row[
                    f"sim_ref_{ref_index + 1}"
                ] = score

            best_index = int(
                np.argmax(similarities)
            )

            row["sim_min"] = float(
                np.min(similarities)
            )
            row["sim_mean"] = float(
                np.mean(similarities)
            )
            row["sim_median"] = float(
                np.median(similarities)
            )
            row["sim_max"] = float(
                np.max(similarities)
            )

            row["reference_best"] = (
                reference_names[best_index]
            )

            print(
                f"OK | mean={row['sim_mean']:.3f} "
                f"| median={row['sim_median']:.3f} "
                f"| max={row['sim_max']:.3f}"
            )

        # Manual annotation fields.
        row["human_rating"] = ""
        row["human_reason"] = ""

        rows.append(row)

    df = pd.DataFrame(rows)

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        output,
        index=False,
        encoding="utf-8-sig",
    )

    # --------------------------------------------------------
    # Method summary
    # --------------------------------------------------------

    valid = df[
        df["face_detected"] == True
    ].copy()

    summary = (
        valid
        .groupby("method")
        .agg(
            count=("sim_mean", "count"),
            sim_mean=("sim_mean", "mean"),
            sim_median=("sim_mean", "median"),
            sim_min=("sim_mean", "min"),
            sim_max=("sim_mean", "max"),
            p25=(
                "sim_mean",
                lambda s: s.quantile(0.25),
            ),
            p75=(
                "sim_mean",
                lambda s: s.quantile(0.75),
            ),
            mean_face_area=(
                "face_area_ratio",
                "mean",
            ),
        )
        .sort_values(
            "sim_mean",
            ascending=False,
        )
        .reset_index()
    )

    summary.to_csv(
        summary_output,
        index=False,
        encoding="utf-8-sig",
    )

    print()
    print("IDENTITY SUMMARY")
    print("=" * 72)

    if summary.empty:
        print("No valid faces.")
    else:
        print(
            summary.round(3).to_string(
                index=False
            )
        )

    print()
    print(f"Report  : {output.resolve()}")
    print(
        f"Summary : {summary_output.resolve()}"
    )


# ============================================================
# CLI
# ============================================================

def main() -> int:

    parser = argparse.ArgumentParser(
        description=(
            "ONYX Quality Gate — Identity Analyzer"
        )
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    calibration = subparsers.add_parser(
        "calibrate",
        help="Measure similarity between reference photos",
    )

    calibration.add_argument(
        "reference_folder",
        type=Path,
    )

    calibration.add_argument(
        "--output",
        type=Path,
        default=Path(
            "identity_calibration.csv"
        ),
    )

    analyze_job = subparsers.add_parser(
        "analyze-job",
        help="Analyze identity similarity for an ensemble manifest",
    )

    analyze_job.add_argument(
        "reference_folder",
        type=Path,
    )

    analyze_job.add_argument(
        "manifest",
        type=Path,
    )

    analyze_job.add_argument(
        "--output",
        type=Path,
        default=Path(
            "quality_report.csv"
        ),
    )

    analyze_job.add_argument(
        "--summary",
        type=Path,
        default=Path(
            "identity_summary.csv"
        ),
    )

    args = parser.parse_args()

    print("ONYX Quality Gate v0.2")
    print("=" * 72)
    print("Model    : InsightFace buffalo_l")
    print("Provider : CUDAExecutionProvider")
    print("=" * 72)

    app = load_analyzer()

    if args.command == "calibrate":

        run_calibration(
            app,
            args.reference_folder,
            args.output,
        )

    elif args.command == "analyze-job":

        run_job_analysis(
            app,
            args.reference_folder,
            args.manifest,
            args.output,
            args.summary,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())