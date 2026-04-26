import hashlib
import logging
from milestone4.recommendation.models import RecommendationResult

logger = logging.getLogger(__name__)

_response_cache: dict[str, RecommendationResult] = {}

def clear_cache():
    _response_cache.clear()

def get_cached_recommendation(payload_json: str) -> RecommendationResult | None:
    cache_key = hashlib.md5(payload_json.encode()).hexdigest()
    if cache_key in _response_cache:
        logger.info(f"Returning cached response for request: {payload_json}")
        return _response_cache[cache_key]
    return None

def set_cached_recommendation(payload_json: str, result: RecommendationResult) -> None:
    cache_key = hashlib.md5(payload_json.encode()).hexdigest()
    _response_cache[cache_key] = result
