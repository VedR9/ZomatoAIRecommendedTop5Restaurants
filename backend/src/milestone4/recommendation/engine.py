import json
import time
import logging
from google.genai import types, errors as genai_errors
from milestone1.ingestion.models import Restaurant
from milestone3.retrieval.models import RetrievalPreferences
from milestone4.recommendation.client import get_client
from milestone4.recommendation.models import RecommendationResult
from milestone4.recommendation.prompt import SYSTEM_PROMPT, build_user_prompt

logger = logging.getLogger(__name__)

# Tried in order; moves to next on 503/429
_MODEL_FALLBACK_CHAIN = [
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash",
    "gemini-flash-latest",
]

def _call_model(client, model_name: str, user_prompt: str) -> RecommendationResult:
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
    if response.text:
        data = json.loads(response.text)
        return RecommendationResult.model_validate(data)
    return RecommendationResult(recommendations=[])


def generate_recommendations(
    preferences: RetrievalPreferences,
    candidates: list[Restaurant],
    model_name: str = None,
) -> RecommendationResult:
    if not candidates:
        logger.info("No candidates provided to generate_recommendations.")
        return RecommendationResult(recommendations=[])

    client = get_client()
    user_prompt = build_user_prompt(preferences, candidates)

    models_to_try = [model_name] if model_name else _MODEL_FALLBACK_CHAIN
    last_error = None

    for model in models_to_try:
        logger.info(f"Calling LLM '{model}' with {len(candidates)} candidates...")
        start_time = time.time()
        try:
            result = _call_model(client, model, user_prompt)
            latency = (time.time() - start_time) * 1000
            logger.info(f"LLM '{model}' succeeded in {latency:.2f}ms.")
            return result
        except (genai_errors.ServerError, genai_errors.ClientError) as e:
            latency = (time.time() - start_time) * 1000
            # 503 = overloaded, 429 = quota exhausted — both are retryable with next model
            if e.status_code in (503, 429):
                logger.warning(f"Model '{model}' unavailable ({e.status_code}), trying next...")
                last_error = e
                continue
            raise RuntimeError(f"LLM call failed: {e}") from e
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            logger.warning(f"LLM '{model}' failed after {latency:.2f}ms: {e}")
            raise RuntimeError(f"LLM call failed: {e}") from e

    raise RuntimeError(
        f"All models unavailable. Last error: {last_error}"
    ) from last_error
