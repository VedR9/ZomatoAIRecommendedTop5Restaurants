from pydantic import BaseModel, Field


class _LLMRecommendation(BaseModel):
    """Minimal schema sent to the LLM as response_schema — never expose externally."""
    restaurant_id: str = Field(..., description="The unique ID of the recommended restaurant from the provided candidates")
    restaurant_name: str = Field(..., description="The name of the restaurant")
    reasoning: str = Field(..., description="Concise explanation of why this restaurant fits the user's preferences")
    rank: int = Field(..., description="The rank of this recommendation, starting from 1")


class _LLMResult(BaseModel):
    recommendations: list[_LLMRecommendation] = Field(..., description="A ranked list of restaurant recommendations")


class Recommendation(BaseModel):
    restaurant_id: str
    restaurant_name: str
    reasoning: str
    rank: int
    # Enriched from candidate data after the LLM call
    rating: float | None = None
    cuisines: list[str] | None = None
    location: str | None = None
    cost_for_two: float | None = None


class RecommendationResult(BaseModel):
    recommendations: list[Recommendation] = Field(..., description="A ranked list of restaurant recommendations")
