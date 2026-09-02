from __future__ import annotations

import csv
import hashlib
import math
from pathlib import Path
from typing import Any

from .models import SourceRecord


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_historical_names(path: Path) -> set[str]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return {row["OriginalName"] for row in csv.DictReader(stream)}


def pose_bucket(yaw: float | None) -> str:
    if yaw is None:
        return "unknown"
    if yaw <= -45:
        return "profile_left"
    if yaw <= -15:
        return "three_quarter_left"
    if yaw < 15:
        return "frontal"
    if yaw < 45:
        return "three_quarter_right"
    return "profile_right"


def _flags(face_count: int, face_ratio: float | None, sharpness: float,
           low: float, high: float) -> list[str]:
    flags = []
    if face_count == 0:
        flags.append("no_face")
    elif face_count > 1:
        flags.append("multiple_faces")
    if face_ratio is not None and face_ratio < 0.015:
        flags.append("small_face")
    if sharpness < 45:
        flags.append("low_sharpness")
    if low > 0.35:
        flags.append("underexposed")
    if high > 0.20:
        flags.append("overexposed")
    return flags


def difference_hash(gray: Any) -> str:
    import cv2
    resized = cv2.resize(gray, (9, 8), interpolation=cv2.INTER_AREA)
    bits = (resized[:, 1:] > resized[:, :-1]).flatten()
    return f"{sum(int(bit) << index for index, bit in enumerate(bits)):016x}"


def lighting_bucket(mean: float, low_fraction: float, high_fraction: float) -> str:
    if low_fraction > 0.20 and high_fraction > 0.08:
        return "high_contrast"
    if mean < 85:
        return "low_key"
    if mean > 175:
        return "bright"
    return "balanced"


def _face_pose(face: Any) -> tuple[float | None, float | None, float | None]:
    pose = getattr(face, "pose", None)
    if pose is not None and len(pose) >= 3:
        pitch, yaw, roll = (float(value) for value in pose[:3])
        return yaw, pitch, roll
    landmarks = getattr(face, "kps", None)
    if landmarks is None or len(landmarks) < 5:
        return None, None, None
    left_eye, right_eye, nose, left_mouth, right_mouth = landmarks[:5]
    eye_mid_x = (float(left_eye[0]) + float(right_eye[0])) / 2
    eye_distance = max(1.0, abs(float(right_eye[0]) - float(left_eye[0])))
    yaw = max(-60.0, min(60.0, (float(nose[0]) - eye_mid_x) / eye_distance * 90.0))
    roll = math.degrees(math.atan2(float(right_eye[1] - left_eye[1]), float(right_eye[0] - left_eye[0])))
    eye_y = (float(left_eye[1]) + float(right_eye[1])) / 2
    mouth_y = (float(left_mouth[1]) + float(right_mouth[1])) / 2
    pitch = max(-45.0, min(45.0, ((float(nose[1]) - eye_y) / max(1.0, mouth_y - eye_y) - 0.55) * 60))
    return yaw, pitch, roll


def load_insightface_cpu() -> Any:
    from insightface.app import FaceAnalysis
    app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
    app.prepare(ctx_id=-1, det_size=(640, 640))
    return app


def build_reference_embedding(app: Any, paths: list[Path]) -> Any:
    import cv2
    import numpy as np
    embeddings = []
    for path in paths:
        image = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
        faces = app.get(image) if image is not None else []
        if faces:
            embeddings.append(max(faces, key=lambda f: float((f.bbox[2]-f.bbox[0])*(f.bbox[3]-f.bbox[1]))).normed_embedding)
    if len(embeddings) < 2:
        raise RuntimeError("at least two valid fixed reference faces are required")
    centroid = np.mean(np.asarray(embeddings, dtype=np.float32), axis=0)
    return centroid / np.linalg.norm(centroid)


def analyze_pool(source: Path, historical_manifest: Path, reference_paths: list[Path],
                 app: Any | None = None, capture_group: str = "") -> list[SourceRecord]:
    import cv2
    import numpy as np
    historical = load_historical_names(historical_manifest)
    analyzer = app or load_insightface_cpu()
    reference = build_reference_embedding(analyzer, reference_paths)
    records = []
    for path in sorted((p for p in source.iterdir() if p.suffix.lower() in IMAGE_EXTENSIONS), key=lambda p: p.name.casefold()):
        raw = np.fromfile(path, dtype=np.uint8)
        image = cv2.imdecode(raw, cv2.IMREAD_COLOR)
        if image is None:
            records.append(SourceRecord(path.stem, str(path), sha256_file(path), 0, 0, False, 0, None, None, None, None, "unknown", 0, 0, 1, 0, None, ["cannot_read"], path.name in historical))
            continue
        height, width = image.shape[:2]
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sharpness = float(cv2.Laplacian(gray, cv2.CV_64F).var())
        exposure = float(gray.mean())
        low = float(np.mean(gray <= 20))
        high = float(np.mean(gray >= 235))
        faces = analyzer.get(image)
        primary = max(faces, key=lambda f: float((f.bbox[2]-f.bbox[0])*(f.bbox[3]-f.bbox[1]))) if faces else None
        ratio = None if primary is None else float((primary.bbox[2]-primary.bbox[0])*(primary.bbox[3]-primary.bbox[1])/(width*height))
        yaw, pitch, roll = _face_pose(primary) if primary is not None else (None, None, None)
        similarity = None if primary is None else float(np.dot(primary.normed_embedding, reference))
        records.append(SourceRecord(
            source_id=path.stem, source_path=str(path), sha256=sha256_file(path), width=width, height=height,
            face_detected=bool(faces), face_count=len(faces), face_area_ratio=ratio, yaw=yaw, pitch=pitch, roll=roll,
            pose_bucket=pose_bucket(yaw), sharpness=sharpness, exposure_mean=exposure,
            exposure_low_fraction=low, exposure_high_fraction=high, identity_similarity=similarity,
            quality_flags=_flags(len(faces), ratio, sharpness, low, high), historical_full_21=path.name in historical,
            perceptual_hash=difference_hash(gray),
            capture_group=capture_group,
            lighting_bucket=lighting_bucket(exposure, low, high),
        ))
    return records
