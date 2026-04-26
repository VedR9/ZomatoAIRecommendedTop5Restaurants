import json
import time
import logging
from milestone1.ingestion.models import Restaurant
from milestone3.retrieval.models import RetrievalPreferences
from milestone4.recommendation.client import get_client
from milestone4.recommendation.models import RecommendationResult, Recommendation
from milestone4.recommendation.prompt import SYSTEM_PROMPT, build_user_prompt

logger = logging.getLogger(__name__)

GROQ_MODEL = "llama-3.3-70b-versatile"

def generate_recommendations(
    preferences: RetrievalPreferences,
    candidates: list[Restaurant],
    model_name: str = GROQ_MODEL,
) -> RecommendationResult:
    if not candidates:
        logger.info("No candidates provided to generate_recommendations.")
        return RecommendationResult(recommendations=[])

    client = get_client()
    user_prompt = build_user_prompt(preferences, candidates)

    logger.info(f"Calling Groq '{model_name}' with {len(candidates)} candidates...")
    start_time = time.time()

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
        )
        latency = (time.time() - start_time) * 1000
        logger.info(f"Groq call succeeded in {latency:.2f}ms.")
        raw = response.choices[0].message.content or "{}"
        data = json.loads(raw)
        return RecommendationResult.model_validate(data)
    except Exception as e:
        latency = (time.time() - start_time) * 1000
        logger.warning(f"LLM generation failed after {latency:.2f}ms: {e}")
        top_candidates = sorted(candidates, key=lambda c: c.rating or 0.0, reverse=True)[:3]
        recs = [
            Recommendation(
                restaurant_id=c.id,
                restaurant_name=c.name,
                reasoning="Fallback recommendation based on highest rating.",
                rank=i + 1,
            )
            for i, c in enumerate(top_candidates)
        ]
        return RecommendationResult(recommendations=recs)
