from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class CaptionPolicy:
    trigger_word: str
    required_prefix: str
    max_words: int = 45
    forbidden_terms: tuple[str, ...] = ()


def validate_caption(caption: str, policy: CaptionPolicy) -> list[str]:
    errors: list[str] = []
    normalized = " ".join(caption.split())
    token_matches = re.findall(rf"\b{re.escape(policy.trigger_word)}\b", normalized, re.IGNORECASE)
    if len(token_matches) != 1:
        errors.append("trigger_word_must_appear_exactly_once")
    if not normalized.lower().startswith(policy.required_prefix.lower()):
        errors.append("required_prefix_missing")
    if len(normalized.split()) > policy.max_words:
        errors.append("caption_too_long")
    lower = normalized.lower()
    for term in policy.forbidden_terms:
        if term.lower() in lower:
            errors.append(f"forbidden_term:{term}")
    return errors
