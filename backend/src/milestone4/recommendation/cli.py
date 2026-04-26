import argparse
from milestone3.retrieval.models import RetrievalPreferences
from milestone4.recommendation.engine import generate_recommendations
from milestone1.ingestion.models import Restaurant

def main():
    parser = argparse.ArgumentParser(description="Test Phase 4 Gemini LLM Engine")
    parser.add_argument("--location", default="Bangalore")
    parser.add_argument("--budget", default="medium")
    parser.add_argument("--cuisines", default="Italian,Chinese")
    parser.add_argument("--min-rating", type=float, default=4.0)
    args = parser.parse_args()

    candidates = [
        Restaurant(id="1", name="Pasta Fresca", location=args.location, cuisines=["Italian"], cost_for_two=1200, rating=4.5),
        Restaurant(id="2", name="Wok This Way", location=args.location, cuisines=["Chinese"], cost_for_two=800, rating=4.2),
        Restaurant(id="3", name="Pizza Hut", location=args.location, cuisines=["Italian"], cost_for_two=600, rating=3.9),
        Restaurant(id="4", name="Dragon Express", location=args.location, cuisines=["Chinese"], cost_for_two=900, rating=4.8),
    ]

    prefs = RetrievalPreferences(
        location=args.location,
        budget_band=args.budget,
        cuisines=args.cuisines.split(","),
        minimum_rating=args.min_rating
    )

    print(f"Testing Gemini LLM with {len(candidates)} dummy candidates...")
    try:
        result = generate_recommendations(prefs, candidates)
        print("\n--- Recommendations ---")
        for rec in result.recommendations:
            print(f"#{rec.rank}: {rec.restaurant_name} (ID: {rec.restaurant_id})")
            print(f"  Reason: {rec.reasoning}")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    main()
