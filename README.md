# NextLeapPractice

Phase 0 implementation for the AI-powered restaurant recommendation system.

## What Is Included in Phase 0
- Project scaffold (`src`, `tests`, `docs`)
- Basic web UI is the planned primary user input surface for milestone 1
- FastAPI application skeleton
- Environment configuration via `.env`
- Dependency management via `pyproject.toml`
- Test and linting baselines

## Phase 1 (Implemented in Separate Folder)
- Ingestion package: `src/milestone1/ingestion/`
- Canonical model: `Restaurant`
- Normalization helpers for rating, cost, cuisines
- Hugging Face loader for `ManikaSaini/zomato-restaurant-recommendation`
- Unit tests for ingestion normalization and mapping

### Phase 1 Ingest Smoke Command
- `python -m milestone1.ingestion.cli --limit 5`

### Phase 1 Live Integration Test (Optional)
- Default `pytest` run skips live Hugging Face access.
- Run live ingestion integration test:
  - `RUN_HF_INTEGRATION=1 pytest -m integration`
- Run all non-integration tests only:
  - `pytest -m "not integration"`

## Phase 2 (Implemented in Separate Folder)
- Preferences package: `src/milestone2/preferences/`
- Structured validated model: `UserPreferences`
- Validation rules for:
  - `location`
  - `budget_band` (`low`, `medium`, `high`)
  - `cuisines` (required, normalized, deduplicated)
  - `minimum_rating` (0 to 5)
- Helper to build allowed city list from ingested restaurants

### Phase 2 Parse Command
- `python -m milestone2.preferences.cli --location Bangalore --budget-band medium --cuisines "Italian,Chinese" --minimum-rating 4.0`

## Phase 3 (Implemented in Separate Folder)
- Retrieval package: `src/milestone3/retrieval/`
- Deterministic hard filters:
  - location
  - minimum rating
  - budget compatibility
  - cuisine overlap
- Candidate capping and stable pre-ranking sort

### Phase 3 Usage (Python)
- `from milestone3.retrieval import retrieve_candidates`

## Prerequisites
- Python 3.11 or higher

## Setup
1. Create a virtual environment:
   - `python3 -m venv .venv`
2. Activate it:
   - macOS/Linux: `source .venv/bin/activate`
3. Install dependencies:
   - `pip install -e ".[dev]"`
4. Create local environment file:
   - `cp .env.example .env`
   - Fill values as needed.

## Run the API
- `uvicorn milestone0.app.main:app --app-dir src --reload --port 8000`

## Verify the Service
- Health check:
  - `curl http://127.0.0.1:8000/health`
- Phase 0 info:
  - `curl http://127.0.0.1:8000/phase0/info`

## Run Tests and Lint
- Tests: `pytest`
- Lint: `ruff check .`

## Phase 0 Exit Criteria Mapping
- Working scaffold: yes
- README with run instructions: yes
- Lint/test baseline: yes
- Environment variables defined and not committed: yes (`.env.example` + `.gitignore`)
