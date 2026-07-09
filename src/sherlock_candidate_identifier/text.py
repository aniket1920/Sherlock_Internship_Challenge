from __future__ import annotations

import re
from difflib import SequenceMatcher


_TOKEN_RE = re.compile(r"[a-z0-9]+")


def normalize_text(value: str | None) -> str:
    if not value:
        return ""
    return " ".join(_TOKEN_RE.findall(value.lower()))


def token_set(value: str | None) -> set[str]:
    return set(normalize_text(value).split())


def name_similarity(left: str | None, right: str | None) -> float:
    left_norm = normalize_text(left)
    right_norm = normalize_text(right)
    if not left_norm or not right_norm:
        return 0.0

    exact_or_contains = left_norm == right_norm or left_norm in right_norm or right_norm in left_norm
    ratio = SequenceMatcher(None, left_norm, right_norm).ratio()
    overlap = token_set(left_norm) & token_set(right_norm)
    token_score = len(overlap) / max(len(token_set(left_norm)), 1)
    return min(1.0, max(ratio, token_score, 0.95 if exact_or_contains else 0.0))


def email_local_part(email: str | None) -> str:
    if not email or "@" not in email:
        return ""
    return email.split("@", 1)[0].replace(".", " ").replace("_", " ").replace("-", " ")
