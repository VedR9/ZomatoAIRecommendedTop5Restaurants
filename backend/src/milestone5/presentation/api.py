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
    result = generate_recommendations(prefs, candidates)
    
    # Store in cache
    set_cached_recommendation(payload_json, result)
    return result
