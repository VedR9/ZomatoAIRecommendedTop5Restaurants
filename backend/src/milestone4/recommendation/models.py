from pydantic import BaseModel, Field

class Recommendation(BaseModel):
    restaurant_id: str = Field(..., description="The unique ID of the recommended restaurant from the provided candidates")
    restaurant_name: str = Field(..., description="The name of the restaurant")
    reasoning: str = Field(..., description="Concise explanation of why this restaurant fits the user's preferences")
    rank: int = Field(..., description="The rank of this recommendation, starting from 1")

class RecommendationResult(BaseModel):
    recommendations: list[Recommendation] = Field(..., description="A ranked list of restaurant recommendations")
