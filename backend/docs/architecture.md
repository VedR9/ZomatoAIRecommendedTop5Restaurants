# Phase-Wise Architecture: AI-Powered Restaurant Recommendation System

## 1) Architecture Overview
This project follows a layered runtime design and a phase-wise delivery plan.

Runtime layers:
1. Data Layer (ingestion and normalization)
2. Preference Layer (input parsing and validation)
3. Retrieval Layer (deterministic candidate filtering)
4. LLM Layer (ranking and explanation generation)
5. Presentation Layer (UI/API response rendering)

Primary flow:
`Dataset -> Canonical restaurant records -> User preferences -> Candidate filtering -> LLM ranking -> Display results`

---

## 2) Phase Plan

### Phase 0: Foundation and Project Setup
**Objective**  
Create a stable base for implementation, local development, and environment management.

**Key components**
- Repository structure (`src`, `docs`, `tests`, `app/ui`)
- Dependency and runtime setup
- Environment configuration (`.env.example`, API key strategy)
- Basic app entry points, with the web UI as the primary input source

**Deliverables**
- Working project scaffold
- README with setup and run instructions
- Configured linting/testing baseline

**Exit criteria**
- Any contributor can run the project locally with documented steps
- Environment variables are clearly defined and not committed

---

### Phase 1: Data Ingestion and Canonical Schema
**Objective**  
Load restaurant data from Hugging Face and transform it into a clean internal schema.

**Key components**
- Dataset loader for `ManikaSaini/zomato-restaurant-recommendation`
- Field mapping and normalization (name, city/location, cuisines, cost, rating)
- Null/missing-value handling and optional deduplication
- Canonical model: `Restaurant`

**Deliverables**
- Ingestion module with reusable loader functions
- Normalized in-memory dataset (or persisted cache)
- Unit tests for parsing/normalization edge cases

**Exit criteria**
- Data can be loaded repeatedly and predictably
- Canonical records are validated and usable by downstream phases

---

### Phase 2: User Preference Model and Validation
**Objective**  
Convert raw user input into a validated, structured preference object.

**Key components**
- Preference model:
  - `location`
  - `budget_band`
  - `cuisines` (one or more)
  - `minimum_rating`
  - `additional_preferences` (optional text)
- Validation and coercion rules
- Friendly error messages for invalid input

**Deliverables**
- Preference parsing/validation module
- Validation test coverage (invalid ratings, unsupported cities, empty cuisines)

**Exit criteria**
- Inputs from UI/API are converted into one validated object for filtering
- Errors are user-readable and actionable

---

### Phase 3: Deterministic Retrieval and Candidate Selection
**Objective**  
Apply business rules to narrow restaurants to a relevant candidate set before LLM usage.

**Key components**
- Deterministic filtering pipeline:
  - Location filter
  - Minimum rating filter
  - Budget compatibility filter
  - Cuisine overlap filter
- Candidate cap (for token and latency control, e.g., top 15-50)
- Optional pre-ranking heuristic (rating, cost-fit, cuisine-match score)

**Deliverables**
- Retrieval module returning ranked candidate list
- Deterministic tests for edge cases:
  - No match
  - Too many matches
  - Sparse/partial preference input

**Exit criteria**
- Given preferences + dataset, system always returns stable candidate output
- LLM is not required for this phase to function correctly

---

### Phase 4: Prompt Assembly and LLM Recommendation Engine
**Objective**  
Ground the LLM on retrieved candidates and generate ranked recommendations with explanations.

**Key components**
- Prompt builder:
  - User preferences section
  - Candidate restaurant section
  - Strict instruction: recommend only from provided candidates
- LLM client:
  - API invocation
  - Timeout and retry policies
  - Temperature/token limits
- Response parser:
  - Enforce structured output (JSON preferred)
  - Validate recommendation references

**Deliverables**
- End-to-end recommendation module
- Fallback path for LLM failures (deterministic top-k + template explanation)
- Tests for malformed LLM output and retry behavior

**Exit criteria**
- System returns ranked recommendations with explanations
- Failure modes degrade gracefully and do not crash user flow

---

### Phase 5: Presentation Layer (UI/API Output Experience)
**Objective**  
Deliver clear recommendation results to users in a simple interface.

**Key components**
- Input form (location, budget, cuisines, min rating, optional notes)
- Results view with required fields:
  - Restaurant name
  - Cuisine
  - Rating
  - Estimated cost
  - AI explanation
- Empty/error state UX:
  - No candidate matches
  - LLM unavailable
  - Input validation errors

**Deliverables**
- Functional user interface and/or API response contract
- Clear, readable output formatting

**Exit criteria**
- Users can complete the full flow from input to result in one run
- Output consistently includes all required recommendation fields

---

### Phase 6: Observability, Quality, and Hardening
**Objective**  
Make the system production-aware and reliable for ongoing iteration.

**Key components**
- Logging:
  - Request latency
  - Candidate counts pre/post filtering
  - LLM call success/failure rates
- Test suites:
  - Unit tests (ingestion, validation, filters, parser)
  - Integration tests (end-to-end recommendation flow)
- Performance controls:
  - Candidate cap
  - Optional response caching for repeated queries

**Deliverables**
- Test coverage and CI-ready checks
- Operational metrics for debugging and tuning

**Exit criteria**
- Common failures are diagnosable from logs
- Core workflows are covered by automated tests

---

### Phase 7: Release Readiness and Documentation
**Objective**  
Prepare the project for handoff, demonstration, and future extension.

**Key components**
- Deployment notes (local/cloud)
- Cost and latency guidance (model choice and usage limits)
- Known limitations and roadmap
- User/developer documentation

**Deliverables**
- Updated docs package (`problemstatement`, `architecture`, setup guide)
- Demo checklist for milestone acceptance

**Exit criteria**
- A new developer can run, understand, and extend the project without tribal knowledge

---

## 3) Dependency and Execution Order
- Phase 0 is mandatory before all others.
- Phase 1 and Phase 2 can be developed in parallel after setup.
- Phase 3 depends on Phase 1 + Phase 2.
- Phase 4 depends on Phase 3.
- Phase 5 depends on Phase 4 (and uses outputs from all prior phases).
- Phase 6 runs continuously but is finalized after core flow works.
- Phase 7 is final packaging and handoff.

---

## 4) Traceability to Problem Statement
- **User Input** -> Phase 2 and Phase 5
- **Candidate Retrieval** -> Phase 3
- **LLM-Based Recommendation** -> Phase 4
- **Output Display** -> Phase 5
- **End-to-end single-run success** -> Phases 5 through 7

---

## 5) Suggested v1 Milestone Cut
If you want a fast first release, stop at:
- Phase 0 through Phase 5 (minimum viable product)

Then add:
- Phase 6 and Phase 7 for production-level reliability and handoff quality.
