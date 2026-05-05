from __future__ import annotations

import logging
from collections.abc import Iterable

from milestone1.ingestion.models import Restaurant
from milestone2.preferences.models import UserPreferences
from milestone3.retrieval.models import RetrievalPreferences

logger = logging.getLogger(__name__)


def budget_band_for_cost(cost_for_two: float | None) -> str | None:
    if cost_for_two is None:
        return None
    if cost_for_two <= 500:
        return "low"
    if cost_for_two <= 1200:
        return "medium"
    return "high"


def _coerce_preferences(
    preferences: RetrievalPreferences | UserPreferences,
) -> RetrievalPreferences:
    if isinstance(preferences, UserPreferences):
        return RetrievalPreferences.from_user_preferences(preferences)
    return preferences


def _location_matches(restaurant: Restaurant, location: str | None) -> bool:
    if not location:
        return True
    return restaurant.location.lower() == location.lower()


def _rating_matches(restaurant: Restaurant, minimum_rating: float | None) -> bool:
    if minimum_rating is None:
        return True
    if restaurant.rating is None:
        return False
    return restaurant.rating >= minimum_rating


def _budget_matches(restaurant: Restaurant, budget_band: str | None) -> bool:
    if not budget_band:
        return True
    return budget_band_for_cost(restaurant.cost_for_two) == budget_band.lower()


def _cuisine_overlap_count(restaurant: Restaurant, cuisines: list[str] | None) -> int:
    if not cuisines:
        return 0
    wanted = {cuisine.lower() for cuisine in cuisines}
    available = {cuisine.lower() for cuisine in restaurant.cuisines}
    return len(wanted & available)


def _cuisines_match(restaurant: Restaurant, cuisines: list[str] | None) -> bool:
    if not cuisines:
        return True
    return _cuisine_overlap_count(restaurant, cuisines) > 0


def _sort_key(
    restaurant: Restaurant,
    preferences: RetrievalPreferences,
) -> tuple[float, float, str, str]:
    cuisine_overlap = _cuisine_overlap_count(restaurant, preferences.cuisines)
    rating = restaurant.rating or 0.0
    score = (2.0 * cuisine_overlap) + rating
    return (-score, -rating, restaurant.name.lower(), restaurant.id)


def retrieve_candidates(
    restaurants: Iterable[Restaurant],
    preferences: RetrievalPreferences | UserPreferences,
    candidate_cap: int = 25,
) -> list[Restaurant]:
    if candidate_cap <= 0:
        raise ValueError("candidate_cap must be greater than 0.")

    coerced_preferences = _coerce_preferences(preferences)

    all_restaurants = list(restaurants)
    pre_filter_count = len(all_restaurants)

    filtered: list[Restaurant] = []
    for restaurant in all_restaurants:
        if not _location_matches(restaurant, coerced_preferences.location):
            continue
        if not _rating_matches(restaurant, coerced_preferences.minimum_rating):
            continue
        if not _budget_matches(restaurant, coerced_preferences.budget_band):
            continue
        if not _cuisines_match(restaurant, coerced_preferences.cuisines):
            continue
        filtered.append(restaurant)

    post_filter_count = len(filtered)
    filtered.sort(key=lambda item: _sort_key(item, coerced_preferences))
    capped = filtered[:candidate_cap]

    logger.info(
        "Retrieval: %d input -> %d after filters -> %d after cap (cap=%d)",
        pre_filter_count,
        post_filter_count,
        len(capped),
        candidate_cap,
    )
    return capped
