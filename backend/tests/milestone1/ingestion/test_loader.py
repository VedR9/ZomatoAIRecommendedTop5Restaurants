from milestone1.ingestion.loader import iter_restaurants, restaurant_from_row


def test_restaurant_from_row_maps_aliases() -> None:
    row = {
        "restaurant_name": "Spice House",
        "city": "Bangalore",
        "cuisines": "North Indian, Chinese",
        "average_cost_for_two": "₹800",
        "aggregate_rating": "4.1/5",
    }
    restaurant = restaurant_from_row(row, index=2)

    assert restaurant is not None
    assert restaurant.name == "Spice House"
    assert restaurant.location == "Bangalore"
    assert restaurant.cuisines == ["North Indian", "Chinese"]
    assert restaurant.cost_for_two == 800.0
    assert restaurant.rating == 4.1
    assert len(restaurant.id) == 12


def test_restaurant_from_row_drops_missing_required_fields() -> None:
    row = {"restaurant_name": "", "city": "Delhi"}
    restaurant = restaurant_from_row(row, index=0)
    assert restaurant is None


def test_iter_restaurants_skips_invalid_rows() -> None:
    rows = [
        {"name": "A", "location": "Delhi", "rating": "4.0"},
        {"name": "", "location": "Delhi"},
        {"name": "B", "location": "Mumbai", "rating": "NEW"},
    ]
    restaurants = list(iter_restaurants(rows))

    assert len(restaurants) == 2
    assert restaurants[0].name == "A"
    assert restaurants[1].name == "B"
    assert restaurants[1].rating is None


def test_restaurant_from_row_handles_hf_column_names() -> None:
    row = {
        "name": "Jalsa",
        "location": "Banashankari",
        "cuisines": "North Indian, Mughlai, Chinese",
        "approx_cost(for two people)": "800",
        "rate": "4.1/5",
    }
    restaurant = restaurant_from_row(row, index=0)

    assert restaurant is not None
    assert restaurant.cost_for_two == 800.0
    assert restaurant.rating == 4.1
