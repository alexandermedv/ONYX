from __future__ import annotations

from collections import Counter
from dataclasses import replace

from .models import SourceRecord


POSE_BONUS = {
    "frontal": 1.0, "three_quarter_left": 0.92, "three_quarter_right": 0.92,
    "profile_left": 0.72, "profile_right": 0.72, "unknown": 0.25,
}


def eligible_for_mini(record: SourceRecord) -> bool:
    in_expanded_pool = record.historical_full_21 or bool(record.capture_group)
    return in_expanded_pool and record.face_count == 1 and not record.quality_flags


def base_score(record: SourceRecord) -> float:
    face = min((record.face_area_ratio or 0) / 0.12, 1.0)
    sharp = min(record.sharpness / 500.0, 1.0)
    exposure = max(0.0, 1.0 - abs(record.exposure_mean - 128) / 128)
    identity = record.identity_similarity or 0.0
    penalties = 0.15 * len([flag for flag in record.quality_flags if flag != "small_face"])
    return 0.32 * identity + 0.22 * sharp + 0.18 * face + 0.13 * exposure + 0.15 * POSE_BONUS[record.pose_bucket] - penalties


def visual_distance(left: SourceRecord, right: SourceRecord) -> float:
    if not left.perceptual_hash or not right.perceptual_hash:
        return 0.5
    return (int(left.perceptual_hash, 16) ^ int(right.perceptual_hash, 16)).bit_count() / 64.0


def crop_bucket(record: SourceRecord) -> str:
    ratio = record.face_area_ratio or 0.0
    if ratio >= 0.10:
        return "close"
    if ratio >= 0.04:
        return "portrait"
    return "wide"


def session_key(record: SourceRecord) -> str:
    return record.capture_group or f"source:{record.sha256}"


def select_nested(records: list[SourceRecord]) -> tuple[list[SourceRecord], dict[str, list[str]]]:
    control = [record for record in records if record.historical_full_21]
    if len(control) != 21:
        raise ValueError(f"historical full_21 must contain exactly 21 images; found {len(control)}")
    candidates = [record for record in records if eligible_for_mini(record)]
    if len(candidates) < 10:
        raise ValueError(f"at least 10 eligible historical images required; found {len(candidates)}")
    chosen: list[SourceRecord] = []
    pose_counts: Counter[str] = Counter()
    crop_counts: Counter[str] = Counter()
    expression_counts: Counter[str] = Counter()
    lighting_counts: Counter[str] = Counter()
    session_counts: Counter[str] = Counter()
    remaining = list(candidates)
    while remaining:
        scored = []
        for record in remaining:
            if len(chosen) < 3 and session_counts[session_key(record)] >= 2:
                continue
            pose_diversity = 1.0 / (1 + pose_counts[record.pose_bucket])
            visual_diversity = min((visual_distance(record, item) for item in chosen), default=1.0)
            framing_diversity = 1.0 / (1 + crop_counts[crop_bucket(record)])
            expression_diversity = 1.0 / (1 + expression_counts[record.expression_bucket])
            lighting_diversity = 1.0 / (1 + lighting_counts[record.lighting_bucket])
            capture_diversity = 1.0 / (1 + session_counts[session_key(record)])
            diversity = (0.25 * pose_diversity + 0.20 * framing_diversity +
                         0.20 * visual_diversity + 0.10 * expression_diversity +
                         0.10 * lighting_diversity + 0.15 * capture_diversity)
            score = base_score(record) + 0.45 * diversity
            scored.append((score, diversity, visual_diversity, framing_diversity, capture_diversity,
                           record.sha256, record))
        if not scored:
            raise ValueError("capture-group constraints made selection impossible")
        score, diversity, perceptual_distance, framing_diversity, capture_diversity, _, selected = max(
            scored, key=lambda item: (item[0], item[5]))
        rank = len(chosen) + 1
        reason = (f"rank={rank}; pose={selected.pose_bucket}; crop={crop_bucket(selected)}; "
                  f"base={base_score(selected):.4f}; diversity={diversity:.4f}; "
                  f"perceptual_distance={perceptual_distance:.4f}; framing_diversity={framing_diversity:.4f}; "
                  f"capture_group={session_key(selected)}; capture_diversity={capture_diversity:.4f}; "
                  f"expression={selected.expression_bucket}; lighting={selected.lighting_bucket}")
        memberships = ["full_21"]
        if rank <= 10: memberships.append("mini_10")
        if rank <= 5: memberships.append("mini_5")
        if rank <= 3: memberships.append("mini_3")
        chosen.append(replace(selected, selection_rank=rank, diversity_contribution=diversity,
                              perceptual_distance=perceptual_distance,
                              selection_reason=reason, selected_memberships=memberships))
        pose_counts[selected.pose_bucket] += 1
        crop_counts[crop_bucket(selected)] += 1
        expression_counts[selected.expression_bucket] += 1
        lighting_counts[selected.lighting_bucket] += 1
        session_counts[session_key(selected)] += 1
        remaining.remove(selected)
    by_hash = {record.sha256: record for record in chosen}
    merged = []
    for record in records:
        if record.sha256 in by_hash:
            merged.append(by_hash[record.sha256])
        elif record.historical_full_21:
            merged.append(replace(record, selected_memberships=["full_21"],
                                  selection_reason="historical manual control; excluded from mini ranking by quality flags"))
        else:
            merged.append(record)
    memberships = {
        "mini_3": [record.sha256 for record in chosen[:3]],
        "mini_5": [record.sha256 for record in chosen[:5]],
        "mini_10": [record.sha256 for record in chosen[:10]],
        "full_21": [record.sha256 for record in sorted(control, key=lambda r: r.sha256)],
    }
    assert set(memberships["mini_3"]) < set(memberships["mini_5"])
    assert set(memberships["mini_5"]) < set(memberships["mini_10"])
    return merged, memberships
