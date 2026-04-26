from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from milestone2.preferences.validation import (
    SUPPORTED_BUDGET_BANDS,
    normalize_cuisines,
    normalize_optional_text,
    normalize_text,
    parse_minimum_rating,
    validate_budget_band,
    validate_location,
)


class ValidationError(ValueError):
    """Raised when user preferences are invalid."""


@dataclass(frozen=True, slots=True)
class UserPreferences:
    location: str
    budget_band: str
    cuisines: list[str]
    minimum_rating: float
    additional_preferences: str | None = None


def preferences_from_mapping(
    raw: dict[str, Any],
    allowed_city_names: set[str] | None = None,
) -> UserPreferences:
    try:
        location = validate_location(
            normalize_text(raw.get("location")),
            allowed_city_names=allowed_city_names,
        )

        budget_band = validate_budget_band(normalize_text(raw.get("budget_band")))
        cuisines = normalize_cuisines(raw.get("cuisines"))
        if not cuisines:
            raise ValidationError("At least one cuisine must be provided.")

        minimum_rating = parse_minimum_rating(raw.get("minimum_rating"))
        additional_preferences = normalize_optional_text(raw.get("additional_preferences"))
    except ValueError as exc:
        raise ValidationError(str(exc)) from exc

    return UserPreferences(
        location=location,
        budget_band=budget_band,
        cuisines=cuisines,
        minimum_rating=minimum_rating,
        additional_preferences=additional_preferences,
    )


def preference_schema_hint() -> dict[str, Any]:
    return {
        "required_fields": ["location", "budget_band", "cuisines", "minimum_rating"],
        "optional_fields": ["additional_preferences"],
        "budget_band_options": sorted(SUPPORTED_BUDGET_BANDS),
        "minimum_rating_range": "0 to 5 (inclusive)",
    }
