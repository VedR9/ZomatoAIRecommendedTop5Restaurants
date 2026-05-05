from fastapi import APIRouter, Request
from pydantic import BaseModel

from milestone3.retrieval.models import RetrievalPreferences
from milestone3.retrieval.filters import retrieve_candidates
from milestone4.recommendation.engine import generate_recommendations
from milestone4.recommendation.models import RecommendationResult
from milestone6.observability.cache import get_cached_recommendation, set_cached_recommendation

router = APIRouter()

class RecommendRequest(BaseModel):
    location: str
    budget_band: str
    cuisines: list[str]
    minimum_rating: float
    use_fallback: bool = False

@router.post("/api/recommend", response_model=RecommendationResult)
def get_recommendations(request: Request, payload: RecommendRequest):
    # Try Caching Layer
    payload_json = payload.model_dump_json()
    cached_result = get_cached_recommendation(payload_json)
    if cached_result:
        return cached_result

    # Process normally
    prefs = RetrievalPreferences(
        location=payload.location,
        budget_band=payload.budget_band,
        cuisines=payload.cuisines,
        minimum_rating=payload.minimum_rating
    )
    
    # Access global dataset from FastAPI app state
    dataset = request.app.state.dataset_cache if hasattr(request.app.state, "dataset_cache") else []
    
    candidates = retrieve_candidates(dataset, prefs, candidate_cap=25)
    
    if payload.use_fallback:
        # Use deterministic fallback without LLM
        from milestone1.ingestion.models import Restaurant
        from milestone4.recommendation.models import Recommendation
        top_candidates = sorted(candidates, key=lambda c: c.rating or 0.0, reverse=True)[:3]
        recs = [
            Recommendation(
                restaurant_id=c.id,
                restaurant_name=c.name,
                reasoning=f"Fallback recommendation based on rating {c.rating} and location match.",
                rank=i+1
            ) for i, c in enumerate(top_candidates)
        ]
        result = RecommendationResult(recommendations=recs)
    else:
        result = generate_recommendations(prefs, candidates)
    
    # Store in cache
    set_cached_recommendation(payload_json, result)
    return result
