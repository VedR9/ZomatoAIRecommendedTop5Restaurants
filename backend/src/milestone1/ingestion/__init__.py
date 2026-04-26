"""Phase 1 ingestion package."""

from milestone1.ingestion.loader import iter_restaurants, load_restaurants_from_huggingface
from milestone1.ingestion.models import Restaurant

__all__ = ["Restaurant", "iter_restaurants", "load_restaurants_from_huggingface"]
