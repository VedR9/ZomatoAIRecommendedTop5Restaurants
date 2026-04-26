from milestone1.ingestion.models import Restaurant
from milestone3.retrieval.models import RetrievalPreferences
from milestone4.recommendation.prompt import build_user_prompt
from milestone4.recommendation.engine import generate_recommendations

def test_build_user_prompt_empty_candidates():
    prefs = RetrievalPreferences(location="Delhi", budget_band="low", cuisines=["Indian"], minimum_rating=4.0)
    prompt = build_user_prompt(prefs, [])
    assert "None" in prompt
    assert "Delhi" in prompt

def test_build_user_prompt_with_candidates():
    prefs = RetrievalPreferences(location="Delhi", budget_band="low", cuisines=["Indian"], minimum_rating=4.0)
    c1 = Restaurant(id="1", name="Test Rest", location="Delhi", cuisines=["Indian"], cost_for_two=500.0, rating=4.5)
    prompt = build_user_prompt(prefs, [c1])
    assert "Test Rest" in prompt
    assert "Indian" in prompt

def test_generate_recommendations_fallback():
    # If the LLM call fails (e.g., no API key in tests), the deterministic fallback should rank by rating
    prefs = RetrievalPreferences(location="Delhi", budget_band="low", cuisines=["Indian"], minimum_rating=4.0)
    c1 = Restaurant(id="1", name="High Rating", location="Delhi", cuisines=["Indian"], cost_for_two=500.0, rating=4.9)
    c2 = Restaurant(id="2", name="Low Rating", location="Delhi", cuisines=["Indian"], cost_for_two=500.0, rating=3.0)
    
    # Passing a dummy model name or lacking config will force an exception in client.py
    res = generate_recommendations(prefs, [c1, c2], model_name="dummy")
    assert len(res.recommendations) == 2
    assert res.recommendations[0].restaurant_id == "1" # Highest rating first
    assert res.recommendations[1].restaurant_id == "2"
