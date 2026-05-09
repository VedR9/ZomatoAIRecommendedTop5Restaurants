from fastapi import APIRouter, Request
from pydantic import BaseModel

from milestone3.retrieval.models import RetrievalPreferences
from milestone3.retrieval.filters import retrieve_candidates
from milestone4.recommendation.engine import generate_recommendations
from milestone4.recommendation.models import Recommendation, RecommendationResult
from milestone6.observability.cache import get_cached_recommendation, set_cached_recommendation

router = APIRouter()


class RecommendRequest(BaseModel):
    location: str
    budget_band: str
    cuisines: list[str]
    minimum_rating: float
    use_fallback: bool = False


def _get_dataset(request: Request):
    return request.app.state.dataset_cache if hasattr(request.app.state, "dataset_cache") else []


@router.get("/api/locations")
def get_locations(request: Request) -> list[str]:
    return sorted(set(r.location for r in _get_dataset(request)))


@router.get("/api/cuisines")
def get_cuisines(request: Request) -> list[str]:
    return sorted(set(c for r in _get_dataset(request) for c in (r.cuisines or [])))


@router.post("/api/recommend", response_model=RecommendationResult)
def get_recommendations(request: Request, payload: RecommendRequest):
    payload_json = payload.model_dump_json()
    cached_result = get_cached_recommendation(payload_json)
    if cached_result:
        return cached_result

    prefs = RetrievalPreferences(
        location=payload.location,
        budget_band=payload.budget_band,
        cuisines=payload.cuisines,
        minimum_rating=payload.minimum_rating,
    )

    dataset = _get_dataset(request)
    candidates = retrieve_candidates(dataset, prefs, candidate_cap=25)

    if payload.use_fallback:
        top = sorted(candidates, key=lambda c: c.rating or 0.0, reverse=True)[:3]
        recs = [
            Recommendation(
                restaurant_id=c.id,
                restaurant_name=c.name,
                reasoning=f"Fallback: rated {c.rating} in {c.location}.",
                rank=i + 1,
                rating=c.rating,
                cuisines=c.cuisines,
                location=c.location,
                cost_for_two=c.cost_for_two,
            )
            for i, c in enumerate(top)
        ]
        result = RecommendationResult(recommendations=recs)
    else:
        result = generate_recommendations(prefs, candidates)

    set_cached_recommendation(payload_json, result)
    return result
