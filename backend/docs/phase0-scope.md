# Phase 0 Scope and Foundations

## Product Slice (Milestone 1)
- Basic web UI is the primary source of user input for milestone 1.
- API endpoints remain available for service checks and developer diagnostics.
- Endpoints included now:
  - `GET /health` for service checks
  - `GET /phase0/info` for environment/readiness checks

## Stack
- Python 3.11+
- FastAPI + Uvicorn
- Pydantic settings management
- Pytest for test baseline
- Ruff for linting baseline

## Environment and Secrets
- Runtime configuration is read from `.env`.
- Template provided in `.env.example`.
- API keys must never be committed.

## Non-Goals in Phase 0
- No restaurant ingestion yet.
- No preference validation yet.
- No retrieval/ranking logic yet.
- No LLM integration yet.
- No production deployment automation yet.

## Exit Criteria Checklist
- [x] Repository structure created (`src`, `tests`, `docs`)
- [x] Dependency/runtime setup documented
- [x] Environment variables defined and example provided
- [x] Basic app entry points added
- [x] Test and lint baselines configured
