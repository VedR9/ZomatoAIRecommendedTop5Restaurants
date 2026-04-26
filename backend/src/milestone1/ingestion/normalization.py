import re
from typing import Any

_CURRENCY_RE = re.compile(r"[^\d.\-]")
_RATING_INLINE_RE = re.compile(r"(\d+(?:\.\d+)?)")


def normalize_text(value: Any) -> str | None:
    if value is None:
        return None
    normalized = str(value).strip()
    return normalized if normalized else None


def parse_rating(value: Any) -> float | None:
    text = normalize_text(value)
    if text is None:
        return None

    lowered = text.lower()
    if lowered in {"new", "n/a", "na", "-", "--", "not rated"}:
        return None

    if "/" in text:
        text = text.split("/", maxsplit=1)[0].strip()

    direct_match = _RATING_INLINE_RE.search(text)
    if not direct_match:
        return None

    rating = float(direct_match.group(1))
    if 0 <= rating <= 5:
        return round(rating, 2)
    return None


def parse_cost_for_two(value: Any) -> float | None:
    text = normalize_text(value)
    if text is None:
        return None

    cleaned = _CURRENCY_RE.sub("", text.replace(",", ""))
    if not cleaned:
        return None

    try:
        cost = float(cleaned)
    except ValueError:
        return None

    if cost < 0:
        return None
    return round(cost, 2)


def normalize_cuisines(value: Any) -> list[str]:
    text = normalize_text(value)
    if text is None:
        return []

    separators = [",", "/", "|", "&"]
    for separator in separators:
        text = text.replace(separator, ",")

    cuisines = []
    seen = set()
    for part in text.split(","):
        cuisine = " ".join(part.split())
        if not cuisine:
            continue
        token = cuisine.lower()
        if token in seen:
            continue
        seen.add(token)
        cuisines.append(cuisine)
    return cuisines
