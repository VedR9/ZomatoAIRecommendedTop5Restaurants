from __future__ import annotations

import hashlib
from collections.abc import Iterable, Iterator, Mapping
from typing import Any

from milestone1.ingestion.models import Restaurant
from milestone1.ingestion.normalization import (
    normalize_cuisines,
    normalize_text,
    parse_cost_for_two,
    parse_rating,
)

HF_DATASET = "ManikaSaini/zomato-restaurant-recommendation"

NAME_ALIASES = ("restaurant_name", "name", "res_name", "title")
LOCATION_ALIASES = ("city", "location", "locality", "listed_in(city)")
CUISINE_ALIASES = ("cuisines", "cuisine", "type_of_food")
COST_ALIASES = (
    "cost_for_two",
    "average_cost_for_two",
    "cost",
    "price_for_two",
    "approx_cost(for two people)",
)
RATING_ALIASES = ("aggregate_rating", "rating", "user_rating", "rate")


def _first_present_value(row: Mapping[str, Any], aliases: tuple[str, ...]) -> Any:
    for key in aliases:
        if key in row:
            return row[key]
    return None


def _make_restaurant_id(index: int, name: str, location: str) -> str:
    raw = f"{index}:{name}:{location}".encode("utf-8")
    return hashlib.sha1(raw).hexdigest()[:12]


def restaurant_from_row(row: Mapping[str, Any], index: int) -> Restaurant | None:
    name = normalize_text(_first_present_value(row, NAME_ALIASES))
    location = normalize_text(_first_present_value(row, LOCATION_ALIASES))
    if not name or not location:
        return None

    cuisines = normalize_cuisines(_first_present_value(row, CUISINE_ALIASES))
    cost_for_two = parse_cost_for_two(_first_present_value(row, COST_ALIASES))
    rating = parse_rating(_first_present_value(row, RATING_ALIASES))

    return Restaurant(
        id=_make_restaurant_id(index=index, name=name, location=location),
        name=name,
        location=location,
        cuisines=cuisines,
        cost_for_two=cost_for_two,
        rating=rating,
    )


def iter_restaurants(rows: Iterable[Mapping[str, Any]]) -> Iterator[Restaurant]:
    seen: set[tuple[str, str]] = set()
    for idx, row in enumerate(rows):
        restaurant = restaurant_from_row(row=row, index=idx)
        if restaurant is None:
            continue
            
        # Deduplicate by name and location
        key = (restaurant.name.lower(), restaurant.location.lower())
        if key in seen:
            continue
            
        seen.add(key)
        yield restaurant


def load_restaurants_from_huggingface(
    split: str = "train",
    limit: int | None = None,
    revision: str | None = None,
) -> list[Restaurant]:
    from datasets import load_dataset

    dataset = load_dataset(HF_DATASET, split=split, revision=revision)
    if limit is not None:
        dataset = dataset.select(range(min(limit, len(dataset))))

    # Dataset rows are returned as dict-like objects that match Mapping[str, Any].
    return list(iter_restaurants(dataset))
