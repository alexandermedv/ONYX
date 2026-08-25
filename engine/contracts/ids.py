from __future__ import annotations

import hashlib
import json
import uuid
from typing import Any


ONYX_NAMESPACE = uuid.UUID("b376a3d6-9f13-5e9b-a23e-83d6a9847925")


def _canonical(parts: dict[str, Any]) -> str:
    return json.dumps(parts, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def stable_id(entity_type: str, **dimensions: Any) -> str:
    """Return a deterministic UUIDv5 ID for a logical ONYX entity."""
    if not entity_type or not dimensions:
        raise ValueError("entity_type and at least one stable dimension are required")
    name = _canonical({"entity_type": entity_type, **dimensions})
    prefixes = {
        "generation": "gen",
        "identity": "idn",
        "evaluation": "eval",
        "human_review": "review",
        "selection": "sel",
        "postprocess": "post",
        "delivery": "del",
        "artifact": "art",
        "attempt": "attempt",
        "manifest": "manifest",
    }
    prefix = prefixes.get(entity_type, entity_type)
    return f"{prefix}_{uuid.uuid5(ONYX_NAMESPACE, name)}"


def generation_result_id(
    *, job_id: str, scene_id: str, provider_id: str, candidate_index: int
) -> str:
    return stable_id(
        "generation",
        job_id=job_id,
        scene_id=scene_id,
        provider_id=provider_id,
        candidate_index=candidate_index,
    )


def identity_result_id(
    *, generation_result_id: str, provider_id: str, result_index: int = 0
) -> str:
    return stable_id(
        "identity",
        generation_result_id=generation_result_id,
        provider_id=provider_id,
        result_index=result_index,
    )


def evaluation_result_id(*, identity_result_id: str, provider_id: str) -> str:
    return stable_id(
        "evaluation",
        identity_result_id=identity_result_id,
        provider_id=provider_id,
    )


def postprocess_result_id(*, selection_decision_id: str, provider_id: str) -> str:
    return stable_id(
        "postprocess",
        selection_decision_id=selection_decision_id,
        provider_id=provider_id,
    )


def delivery_result_id(*, postprocess_result_id: str, provider_id: str) -> str:
    return stable_id(
        "delivery",
        postprocess_result_id=postprocess_result_id,
        provider_id=provider_id,
    )


def derive_seed(
    *,
    base_seed: int,
    job_id: str,
    scene_id: str,
    provider_id: str,
    candidate_index: int,
    stage: str,
) -> int:
    """Derive a deterministic signed-64-bit-safe seed using sha256-derived-v1."""
    payload = _canonical(
        {
            "algorithm": "sha256-derived-v1",
            "base_seed": int(base_seed),
            "job_id": job_id,
            "scene_id": scene_id,
            "provider_id": provider_id,
            "candidate_index": int(candidate_index),
            "stage": stage,
        }
    ).encode("utf-8")
    return int.from_bytes(hashlib.sha256(payload).digest()[:8], "big") & ((1 << 63) - 1)


