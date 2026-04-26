# Detailed Edge Cases: AI-Powered Restaurant Recommendation System

This document lists detailed edge cases for the project, aligned with:
- `docs/problemstatement.md`
- `docs/architecture.md`

It is organized phase-wise and includes expected behavior so implementation and testing can remain consistent.

---

## Phase 0: Foundation and Project Setup

### Environment and Configuration
- **Missing API key**
  - Case: LLM provider key is not set.
  - Expected: App starts with a clear warning; recommendation endpoint fails gracefully with actionable message.
- **Invalid API key**
  - Case: Key exists but is revoked/incorrect.
  - Expected: LLM call fails with provider error mapping; UI shows recoverable error, not stack trace.
- **Missing `.env` in local setup**
  - Case: New contributor runs project without env file.
  - Expected: Startup validation lists required variables and sample values.

### Dependency and Runtime
- **Incompatible package versions**
  - Case: Lockfile mismatch or unsupported runtime version.
  - Expected: Setup command fails early with clear version constraints.
- **Partial install state**
  - Case: Interrupted install leaves inconsistent dependencies.
  - Expected: Diagnostics command identifies missing modules and recovery steps.

---

## Phase 1: Data Ingestion and Canonical Schema

### Dataset Access
- **Hugging Face dataset unavailable**
  - Case: Network outage, dataset removed, or temporary endpoint failure.
  - Expected: Retry with backoff; if still failing, return explicit ingestion failure and optional cached fallback.
- **Rate limiting from source**
  - Case: Too many requests in short time.
  - Expected: Respect retry-after behavior; avoid tight retry loops.

### Schema and Data Quality
- **Unexpected schema change**
  - Case: Source column names/types changed.
  - Expected: Schema assertion fails fast with exact missing/changed fields.
- **Missing critical fields**
  - Case: Restaurant has empty name or location.
  - Expected: Drop record or mark invalid based on policy; emit ingestion counters.
- **Malformed ratings**
  - Case: Rating text such as `"NEW"`, `"N/A"`, `"4.1/5"` string format.
  - Expected: Normalize when possible; otherwise mark as null and handle in filter logic.
- **Ambiguous cost values**
  - Case: Cost appears as mixed currency strings or ranges.
  - Expected: Normalize to internal numeric or budget-band mapping; unknown values flagged.
- **Duplicate restaurants**
  - Case: Same restaurant duplicated across rows with slight naming differences.
  - Expected: Deduplication strategy documented (strict/loose); retain deterministic winner.
- **Encoding/special character issues**
  - Case: Non-ASCII cuisine or locality names.
  - Expected: Preserve display-safe text; normalize for matching without losing original form.

### Performance and Scale
- **Very large dataset load latency**
  - Case: Full dataset causes slow startup.
  - Expected: Support caching or lazy load; log load duration.
- **Memory pressure during ingestion**
  - Case: In-memory load too large for environment.
  - Expected: Stream/chunk loading option or summarized cache representation.

---

## Phase 2: User Preference Model and Validation

### Input Validation
- **Unknown city**
  - Case: User enters city not present in dataset.
  - Expected: Validation error with suggestions, or soft warning with broader fallback based on product decision.
- **Typo in city/cuisine**
  - Case: `"Banglore"`, `"Italien"`.
  - Expected: Fuzzy match suggestions; do not silently map to wrong value.
- **Out-of-range rating**
  - Case: `< 0`, `> 5`, non-numeric input.
  - Expected: Reject with clear acceptable range and format.
- **Invalid budget value**
  - Case: Budget outside supported enums.
  - Expected: Reject and show supported budget options.
- **Empty preference payload**
  - Case: User submits no filters.
  - Expected: Either return popular/top-rated defaults or force minimal required fields per spec.

### Preference Semantics
- **Conflicting constraints**
  - Case: Very low budget + very high minimum rating + rare cuisine in small city.
  - Expected: No-match response with relaxation hints (lower rating, broaden cuisine, nearby city).
- **Multiple cuisines with AND/OR ambiguity**
  - Case: User selects Italian + Chinese.
  - Expected: Explicit policy (OR by default; optional strict mode).
- **Free-text adversarial or irrelevant content**
  - Case: Prompt-injection text in "additional preferences."
  - Expected: Treated as plain preference text; escaped/sanitized before prompt assembly.

---

## Phase 3: Deterministic Retrieval and Candidate Selection

### Filtering Logic
- **No matches after hard filters**
  - Case: Filter pipeline returns empty set.
  - Expected: Skip LLM call; return no-results response with guided next steps.
- **Too many matches**
  - Case: Thousands of candidates for broad filters.
  - Expected: Apply deterministic candidate cap and pre-ranking heuristics.
- **Single match**
  - Case: Only one restaurant fits.
  - Expected: Return single recommendation cleanly; avoid fake ranking language.
- **Ties in heuristic ranking**
  - Case: Equal score across many records.
  - Expected: Stable tie-breakers (rating count, alphabetical, ID).

### Matching Robustness
- **Cuisine naming variants**
  - Case: `"North Indian"` vs `"North-Indian"` vs `"Indian"`.
  - Expected: Normalized token mapping and synonym support.
- **Location granularity mismatch**
  - Case: User enters city but dataset contains locality.
  - Expected: Mapping layer for city-locality relationships or fallback strategy.
- **Null rating/cost in candidates**
  - Case: Records missing fields after filtering.
  - Expected: Either exclude based on strictness or include with penalty score.

### Determinism and Reproducibility
- **Non-deterministic candidate order**
  - Case: Same input yields different candidate list order.
  - Expected: Stable sorting keys and explicit ordering guarantees.

---

## Phase 4: Prompt Assembly and LLM Recommendation Engine

### Prompt Safety and Grounding
- **LLM recommends restaurant not in candidate set**
  - Case: Hallucinated names.
  - Expected: Output validator rejects invalid items and retries or falls back.
- **Prompt injection via user text**
  - Case: User says "ignore rules and output anything."
  - Expected: System instructions enforce grounding and output format regardless of user text.
- **Prompt injection via dataset content**
  - Case: Restaurant name/description contains instruction-like text.
  - Expected: Candidate data treated as quoted data, not executable instruction.

### Model Output and Parsing
- **Malformed JSON response**
  - Case: Model returns prose or invalid JSON.
  - Expected: Repair attempt or controlled retry; fallback path if repeated.
- **Missing required fields in model output**
  - Case: No explanation or no rank index.
  - Expected: Schema validation failure and retry/fallback.
- **Duplicate recommendations in output**
  - Case: Same restaurant repeated multiple times.
  - Expected: Deduplicate and fill remaining slots deterministically.
- **Explanations too long/too short**
  - Case: Verbose paragraph or one-word reasoning.
  - Expected: Post-validation with length constraints and truncation/regeneration policy.

### Reliability and Cost
- **Timeout from LLM provider**
  - Case: Slow response exceeds threshold.
  - Expected: Retry within bounded budget; then deterministic fallback.
- **Transient 5xx errors**
  - Case: Provider instability.
  - Expected: Exponential backoff retries with max attempt cap.
- **Token overflow**
  - Case: Candidate payload too large.
  - Expected: Candidate cap + compact prompt format before request.
- **Unexpected cost spike**
  - Case: Repeated expensive calls from broad queries.
  - Expected: Log token usage and enforce per-request upper bounds.

---

## Phase 5: Presentation Layer (UI/API Output Experience)

### UI/UX Edge Cases
- **Slow response perception**
  - Case: Retrieval + LLM call takes several seconds.
  - Expected: Loading state with progress messaging; prevent duplicate submissions.
- **User submits repeatedly**
  - Case: Multiple rapid clicks.
  - Expected: Debounce/disable submit while request is in flight.
- **No-results display confusion**
  - Case: Empty result shown without explanation.
  - Expected: Distinct "no matching restaurants" state with filter relaxation suggestions.
- **LLM failure display confusion**
  - Case: Backend fallback used silently.
  - Expected: Transparent but simple messaging when deterministic fallback is shown.

### Output Integrity
- **Missing fields in displayed card**
  - Case: Cost unavailable for some result.
  - Expected: Render safe placeholder (e.g., "Cost unavailable"), not blank/broken UI.
- **Long restaurant names/explanations**
  - Case: Overflow in cards.
  - Expected: Truncation with tooltip/expand pattern.
- **Inconsistent ranking labels**
  - Case: Rank numbers not sequential after dedupe.
  - Expected: Reindex before rendering.

### API/Contract Cases
- **Unexpected backend payload shape**
  - Case: Frontend receives unknown fields/missing keys.
  - Expected: Defensive parsing and user-safe error state.
- **Version mismatch between frontend and backend**
  - Case: New backend contract deployed first.
  - Expected: Backward-compatible defaults and explicit API versioning.

---

## Phase 6: Observability, Quality, and Hardening

### Logging and Monitoring
- **Logs contain sensitive data**
  - Case: Raw user free-text or full prompts logged.
  - Expected: Redaction policy and structured safe logging.
- **Insufficient error context**
  - Case: Failures logged without request IDs or phase markers.
  - Expected: Include correlation ID, phase, and failure class.

### Testing Coverage Gaps
- **Happy path only tests**
  - Case: No tests for malformed ratings, no-match filters, invalid LLM output.
  - Expected: Add targeted edge-case tests per phase.
- **Flaky integration tests**
  - Case: Tests depend on live external APIs.
  - Expected: Mock model responses for stable CI; isolate optional live tests.

### Performance Regressions
- **Increasing latency over time**
  - Case: Prompt grows or dataset operations become inefficient.
  - Expected: Baseline performance tests and alert thresholds.

---

## Phase 7: Release Readiness and Documentation

### Documentation Gaps
- **Runbook missing failure handling**
  - Case: Team cannot resolve API outage or dataset failure.
  - Expected: Add troubleshooting section with common error signatures.
- **Unclear product constraints**
  - Case: Users assume live availability/maps exist.
  - Expected: Explicitly document v1 non-goals and limitations.

### Operational Readiness
- **No rollback strategy**
  - Case: New release breaks ranking quality.
  - Expected: Versioned release process and fallback to prior stable build.
- **Untracked model changes**
  - Case: Model/provider change alters output format quality.
  - Expected: Capture model config/version in release notes and logs.

---

## Cross-Phase Critical Edge Cases (High Priority)

1. **No candidate matches**  
   Must not call LLM unnecessarily; provide helpful relaxation suggestions.

2. **LLM hallucination outside candidate set**  
   Must be blocked by validator and corrected via retry/fallback.

3. **Malformed or unparseable LLM output**  
   Must not break user flow; fallback response is required.

4. **Schema drift in upstream dataset**  
   Must fail fast with clear diagnostics and prevent silent bad recommendations.

5. **Prompt/token budget overflow**  
   Must be controlled by candidate cap and compact prompt formatting.

6. **Ambiguous user intent in input fields**  
   Must be resolved with validation, suggestions, and explicit matching policies.

---

## Recommended Test Matrix (Minimum)

- **Ingestion tests**: missing columns, malformed ratings/costs, duplicates
- **Validation tests**: invalid city, invalid rating, empty payload, conflicting filters
- **Retrieval tests**: no matches, large match set, stable deterministic ordering
- **LLM tests**: hallucinated item, invalid JSON, timeout, provider 5xx, retry/fallback
- **UI/API tests**: no-results state, loading state, fallback messaging, missing field rendering
- **End-to-end tests**: one realistic happy path and at least two failure-path flows

---

## Definition of Done for Edge-Case Readiness

The project can be considered edge-case ready for v1 when:
- High-priority cross-phase cases are covered by automated tests
- No known edge case causes unhandled exceptions in user flow
- Failures produce actionable messages for users and operators
- Deterministic fallback works when LLM path fails
