from milestone1.ingestion.normalization import normalize_cuisines, parse_cost_for_two, parse_rating


def test_parse_rating_formats() -> None:
    assert parse_rating("4.3/5") == 4.3
    assert parse_rating("NEW") is None
    assert parse_rating("not rated") is None
    assert parse_rating("6.2") is None


def test_parse_cost_for_two_formats() -> None:
    assert parse_cost_for_two("₹1,200") == 1200.0
    assert parse_cost_for_two("450") == 450.0
    assert parse_cost_for_two("-20") is None
    assert parse_cost_for_two("unknown") is None


def test_normalize_cuisines_and_deduplicate() -> None:
    cuisines = normalize_cuisines("Italian, Chinese / Italian | North Indian")
    assert cuisines == ["Italian", "Chinese", "North Indian"]
