"""Text normalization and similarity helpers."""

from __future__ import annotations

import re
from difflib import SequenceMatcher

try:
    from rapidfuzz import fuzz
except ImportError:  # pragma: no cover - used only before dependencies are installed.
    fuzz = None


_TOKEN_RE = re.compile(r"[a-z0-9]+")


def normalize_text(value: str | None) -> str:
    """Lowercase text and keep alphanumeric tokens."""

    if not value:
        return ""
    return " ".join(_TOKEN_RE.findall(value.lower()))


def text_similarity(left: str | None, right: str | None) -> float:
    """Return a normalized similarity score between two short strings."""

    left_norm = normalize_text(left)
    right_norm = normalize_text(right)
    if not left_norm or not right_norm:
        return 0.0
    if fuzz is not None:
        return fuzz.WRatio(left_norm, right_norm) / 100
    return SequenceMatcher(None, left_norm, right_norm).ratio()


def email_local_part(email: str | None) -> str:
    """Extract a readable local part from an email address."""

    if not email or "@" not in email:
        return ""
    local_part = email.split("@", 1)[0]
    return local_part.replace(".", " ").replace("_", " ").replace("-", " ")
