from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from milestone1.ingestion.models import Restaurant

SUPPORTED_BUDGET_BANDS = {"low", "medium", "high"}


def normalize_text(value: Any) -> str | None:
    if value is None:
        return None
    normalized = str(value).strip()
    return normalized if normalized else None


def normalize_optional_text(value: Any) -> str | None:
    text = normalize_text(value)
    if not text:
        return None
    return text


def normalize_cuisines(value: Any) -> list[str]:
    text = normalize_text(value)
    if text is None:
        return []

    if isinstance(value, list):
        source_items = value
    else:
        source_items = [part for part in text.replace("/", ",").split(",")]

    cuisines: list[str] = []
    seen: set[str] = set()
    for item in source_items:
        cuisine = normalize_text(item)
        if not cuisine:
            continue
        key = cuisine.lower()
        if key in seen:
            continue
        seen.add(key)
        cuisines.append(cuisine)
    return cuisines


def parse_minimum_rating(value: Any) -> float:
    if value is None:
        raise ValueError("Minimum rating is required.")
    try:
        rating = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("Minimum rating must be a valid number.") from exc

    if not (0 <= rating <= 5):
        raise ValueError("Minimum rating must be between 0 and 5.")
    return round(rating, 2)


def validate_budget_band(value: str | None) -> str:
    if not value:
        raise ValueError("Budget band is required.")
    normalized = value.lower()
    if normalized not in SUPPORTED_BUDGET_BANDS:
        options = ", ".join(sorted(SUPPORTED_BUDGET_BANDS))
        raise ValueError(f"Budget band must be one of: {options}.")
    return normalized


def validate_location(value: str | None, allowed_city_names: set[str] | None = None) -> str:
    if not value:
        raise ValueError("Location is required.")
    if allowed_city_names and value.lower() not in allowed_city_names:
        raise ValueError("Location is not supported in the current dataset.")
    return value


def allowed_cities_from_restaurants(restaurants: Iterable[Restaurant]) -> set[str]:
    return {restaurant.location.lower() for restaurant in restaurants if restaurant.location}
