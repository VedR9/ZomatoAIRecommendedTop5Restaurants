import os

import pytest

from milestone1.ingestion.loader import load_restaurants_from_huggingface


@pytest.mark.integration
def test_load_restaurants_from_huggingface_live() -> None:
    if os.getenv("RUN_HF_INTEGRATION") != "1":
        pytest.skip("Set RUN_HF_INTEGRATION=1 to run live Hugging Face integration tests.")

    restaurants = load_restaurants_from_huggingface(limit=3)

    assert len(restaurants) > 0
    for restaurant in restaurants:
        assert restaurant.name
        assert restaurant.location
