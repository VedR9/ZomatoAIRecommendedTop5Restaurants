import pytest

from milestone1.ingestion.models import Restaurant
from milestone2.preferences.models import ValidationError, preferences_from_mapping
from milestone2.preferences.validation import allowed_cities_from_restaurants


def test_preferences_from_mapping_valid_payload() -> None:
    payload = {
        "location": "Bangalore",
        "budget_band": "Medium",
        "cuisines": "Italian, Chinese, Italian",
        "minimum_rating": "4.2",
        "additional_preferences": "family-friendly",
    }
    preferences = preferences_from_mapping(payload)

    assert preferences.location == "Bangalore"
    assert preferences.budget_band == "medium"
    assert preferences.cuisines == ["Italian", "Chinese"]
    assert preferences.minimum_rating == 4.2
    assert preferences.additional_preferences == "family-friendly"


def test_preferences_reject_invalid_rating() -> None:
    payload = {
        "location": "Bangalore",
        "budget_band": "low",
        "cuisines": "North Indian",
        "minimum_rating": 7,
    }
    with pytest.raises(ValidationError, match="between 0 and 5"):
        preferences_from_mapping(payload)


def test_preferences_reject_unsupported_location_when_allow_list_provided() -> None:
    payload = {
        "location": "Unknown City",
        "budget_band": "high",
        "cuisines": "Thai",
        "minimum_rating": 4,
    }
    with pytest.raises(ValidationError, match="not supported"):
        preferences_from_mapping(payload, allowed_city_names={"bangalore", "delhi"})


def test_allowed_cities_from_restaurants() -> None:
    restaurants = [
        Restaurant(
            id="1",
            name="A",
            location="Bangalore",
            cuisines=["Thai"],
            cost_for_two=500,
            rating=4.0,
        ),
        Restaurant(
            id="2",
            name="B",
            location="Delhi",
            cuisines=["Chinese"],
            cost_for_two=700,
            rating=4.2,
        ),
    ]
    allowed = allowed_cities_from_restaurants(restaurants)
    assert allowed == {"bangalore", "delhi"}
