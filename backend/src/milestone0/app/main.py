from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from milestone0.app.config import get_settings
from milestone1.ingestion.loader import load_restaurants_from_huggingface
from milestone5.presentation.api import router as presentation_router
from milestone6.observability.middleware import log_requests
from milestone6.observability.cache import clear_cache

settings = get_settings()

logging.basicConfig(level=settings.log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading restaurant dataset into memory...")
    app.state.dataset_cache = load_restaurants_from_huggingface()
    logger.info(f"Loaded {len(app.state.dataset_cache)} restaurants.")
    yield
    if hasattr(app.state, "dataset_cache"):
        app.state.dataset_cache.clear()
    clear_cache()

app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(log_requests)

app.include_router(presentation_router)

@app.get("/health")
def healthcheck() -> dict[str, str | bool]:
    has_dataset = hasattr(app.state, "dataset_cache") and bool(app.state.dataset_cache)
    return {"status": "ok", "environment": settings.app_env, "dataset_loaded": has_dataset}

@app.get("/phase0/info")
def phase0_info() -> dict[str, str | bool]:
    return {
        "app_name": settings.app_name,
        "environment": settings.app_env,
        "api_key_configured": bool(settings.llm_api_key),
        "message": "Phase 0 scaffold is ready.",
    }
