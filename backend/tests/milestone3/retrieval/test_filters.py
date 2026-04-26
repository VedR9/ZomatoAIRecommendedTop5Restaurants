from milestone1.ingestion.models import Restaurant
from milestone2.preferences.models import UserPreferences
from milestone3.retrieval.filters import budget_band_for_cost, retrieve_candidates
from milestone3.retrieval.models import RetrievalPreferences


def _sample_restaurants() -> list[Restaurant]:
    return [
        Restaurant(
            id="r1",
            name="Spice House",
            location="Bangalore",
            cuisines=["North Indian", "Chinese"],
            cost_for_two=450,
            rating=4.3,
        ),
        Restaurant(
            id="r2",
            name="Urban Fork",
            location="Bangalore",
            cuisines=["Italian", "Mexican"],
            cost_for_two=900,
            rating=4.6,
        ),
        Restaurant(
            id="r3",
            name="Royal Feast",
            location="Bangalore",
            cuisines=["North Indian"],
            cost_for_two=1600,
            rating=4.4,
        ),
        Restaurant(
            id="r4",
            name="Cafe Breeze",
            location="Delhi",
            cuisines=["Cafe", "Italian"],
            cost_for_two=700,
            rating=4.5,
        ),
    ]


def test_budget_band_for_cost() -> None:
    assert budget_band_for_cost(250) == "low"
    assert budget_band_for_cost(800) == "medium"
    assert budget_band_for_cost(1500) == "high"
    assert budget_band_for_cost(None) is None


def test_retrieve_candidates_no_match() -> None:
    preferences = UserPreferences(
        location="Mumbai",
        budget_band="low",
        cuisines=["Thai"],
        minimum_rating=4.5,
    )
    candidates = retrieve_candidates(_sample_restaurants(), preferences, candidate_cap=10)
    assert candidates == []


def test_retrieve_candidates_applies_cap_and_stable_sort() -> None:
    preferences = UserPreferences(
        location="Bangalore",
        budget_band="medium",
        cuisines=["Italian", "Mexican"],
        minimum_rating=4.0,
    )
    candidates = retrieve_candidates(_sample_restaurants(), preferences, candidate_cap=1)

    assert len(candidates) == 1
    assert candidates[0].name == "Urban Fork"


def test_retrieve_candidates_with_sparse_preferences() -> None:
    preferences = RetrievalPreferences(
        location="Bangalore",
        budget_band=None,
        cuisines=None,
        minimum_rating=None,
    )
    candidates = retrieve_candidates(_sample_restaurants(), preferences, candidate_cap=10)

    assert len(candidates) == 3
    assert {candidate.name for candidate in candidates} == {
        "Spice House",
        "Urban Fork",
        "Royal Feast",
    }
