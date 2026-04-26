import json
import time
import logging
from google.genai import types
from milestone1.ingestion.models import Restaurant
from milestone3.retrieval.models import RetrievalPreferences
from milestone4.recommendation.client import get_client
from milestone4.recommendation.models import RecommendationResult, Recommendation
from milestone4.recommendation.prompt import SYSTEM_PROMPT, build_user_prompt

logger = logging.getLogger(__name__)

def generate_recommendations(
    preferences: RetrievalPreferences, 
    candidates: list[Restaurant],
    model_name: str = "gemini-2.5-flash"
) -> RecommendationResult:
    if not candidates:
        logger.info("No candidates provided to generate_recommendations.")
        return RecommendationResult(recommendations=[])

    client = get_client()
    user_prompt = build_user_prompt(preferences, candidates)
    
    logger.info(f"Calling LLM '{model_name}' with {len(candidates)} deterministic candidates...")
    start_time = time.time()

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_mime_type="application/json",
                response_schema=RecommendationResult,
                temperature=0.2,
            ),
        )
        latency = (time.time() - start_time) * 1000
        logger.info(f"LLM call succeeded in {latency:.2f}ms.")
        if response.text:
            data = json.loads(response.text)
            return RecommendationResult.model_validate(data)
        return RecommendationResult(recommendations=[])
    except Exception as e:
        latency = (time.time() - start_time) * 1000
        logger.warning(f"LLM generation failed after {latency:.2f}ms: {e}")
        # Deterministic fallback based on rating
        top_candidates = sorted(candidates, key=lambda c: c.rating or 0.0, reverse=True)[:3]
        recs = [
            Recommendation(
                restaurant_id=c.id,
                restaurant_name=c.name,
                reasoning="Fallback recommendation based on highest rating.",
                rank=i+1
            ) for i, c in enumerate(top_candidates)
        ]
        return RecommendationResult(recommendations=recs)
