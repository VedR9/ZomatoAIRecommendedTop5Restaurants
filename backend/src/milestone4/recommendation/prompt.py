from milestone1.ingestion.models import Restaurant
from milestone3.retrieval.models import RetrievalPreferences

SYSTEM_PROMPT = """You are an expert restaurant recommendation engine.
You will be provided with a user's preferences and a list of candidate restaurants that strictly match their criteria.
Your job is to rank the best restaurants from the provided candidate list. Provide up to 5 recommendations if there are enough candidates.
You MUST ONLY recommend restaurants from the provided candidate list. Do not invent or recommend any other restaurants.
Provide a clear, concise reasoning for why each restaurant is a good fit based on their cuisines, cost, and rating.
"""

def build_user_prompt(preferences: RetrievalPreferences, candidates: list[Restaurant]) -> str:
    pref_str = (
        f"Location: {preferences.location}\n"
        f"Budget Band: {preferences.budget_band}\n"
        f"Preferred Cuisines: {', '.join(preferences.cuisines) if preferences.cuisines else 'Any'}\n"
        f"Minimum Rating: {preferences.minimum_rating}\n"
    )

    if not candidates:
        return f"User Preferences:\n{pref_str}\n\nCandidate Restaurants:\nNone\n\nPlease output an empty list of recommendations."

    candidates_str = ""
    for c in candidates:
        cuisines = ", ".join(c.cuisines) if c.cuisines else "Unknown"
        candidates_str += f"- ID: {c.id} | Name: {c.name} | Cuisines: {cuisines} | Rating: {c.rating} | Cost for Two: {c.cost_for_two}\n"

    prompt = (
        f"User Preferences:\n{pref_str}\n\n"
        f"Candidate Restaurants:\n{candidates_str}\n\n"
        "Please provide your recommendations from the candidate list."
    )
    return prompt
