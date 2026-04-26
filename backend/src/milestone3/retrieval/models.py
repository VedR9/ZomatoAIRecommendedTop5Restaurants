from __future__ import annotations

from dataclasses import dataclass

from milestone2.preferences.models import UserPreferences


@dataclass(frozen=True, slots=True)
class RetrievalPreferences:
    location: str | None = None
    budget_band: str | None = None
    cuisines: list[str] | None = None
    minimum_rating: float | None = None

    @classmethod
    def from_user_preferences(cls, preferences: UserPreferences) -> "RetrievalPreferences":
        return cls(
            location=preferences.location,
            budget_band=preferences.budget_band,
            cuisines=preferences.cuisines,
            minimum_rating=preferences.minimum_rating,
        )
