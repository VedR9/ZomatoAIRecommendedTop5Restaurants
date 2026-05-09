import React from 'react';

const PhaseCard = ({ phase, title, module, description, dependsOn }) => (
  <div style={{
    background: 'rgba(255,255,255,0.03)',
    border: '1px solid var(--border-color)',
    borderRadius: '10px',
    padding: '1.25rem',
  }}>
    <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.5rem' }}>
      <span style={{
        background: 'var(--primary-accent)',
        color: 'white',
        borderRadius: '6px',
        padding: '0.2rem 0.6rem',
        fontSize: '0.75rem',
        fontWeight: 700,
        flexShrink: 0,
      }}>
        Phase {phase}
      </span>
      <strong style={{ fontSize: '1rem' }}>{title}</strong>
    </div>
    <code style={{ fontSize: '0.78rem', color: 'var(--primary-accent)', display: 'block', marginBottom: '0.5rem' }}>{module}</code>
    <p style={{ margin: 0, color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.6 }}>{description}</p>
    {dependsOn && (
      <p style={{ margin: '0.5rem 0 0 0', fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
        Depends on: <span style={{ color: 'var(--text-primary)' }}>{dependsOn}</span>
      </p>
    )}
  </div>
);

const FlowStep = ({ label, detail, arrow }) => (
  <>
    <div style={{
      background: 'rgba(99,102,241,0.1)',
      border: '1px solid rgba(99,102,241,0.3)',
      borderRadius: '8px',
      padding: '0.75rem 1rem',
      textAlign: 'center',
    }}>
      <div style={{ fontWeight: 600, fontSize: '0.9rem' }}>{label}</div>
      {detail && <div style={{ color: 'var(--text-secondary)', fontSize: '0.78rem', marginTop: '0.25rem' }}>{detail}</div>}
    </div>
    {arrow && (
      <div style={{ textAlign: 'center', color: 'var(--text-secondary)', fontSize: '1.2rem', lineHeight: 1 }}>↓</div>
    )}
  </>
);

export default function ArchitecturePage() {
  return (
    <div>
      <h1 style={{ margin: 0, fontSize: '2rem', fontWeight: 800 }}>System Architecture</h1>
      <p style={{ color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
        A layered, phase-gated design that separates deterministic retrieval from LLM ranking.
      </p>

      <section style={{ marginTop: '2.5rem' }}>
        <h2 style={{ fontSize: '1.3rem', marginBottom: '1.25rem' }}>Runtime Layers</h2>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          <FlowStep label="1. Data Layer" detail="HuggingFace dataset → ~12,000 canonical Restaurant records (Phase 1)" arrow />
          <FlowStep label="2. Preference Layer" detail="Raw user input → validated UserPreferences object (Phase 2)" arrow />
          <FlowStep label="3. Retrieval Layer" detail="Hard filters: location, rating, budget, cuisine → top N candidates (Phase 3)" arrow />
          <FlowStep label="4. LLM Layer" detail="Grounded prompt → Gemini 2.5 Flash → ranked JSON output (Phase 4)" arrow />
          <FlowStep label="5. Presentation Layer" detail="FastAPI endpoint + Next.js UI → recommendation cards (Phase 5)" />
        </div>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginTop: '1rem' }}>
          A <strong style={{ color: 'var(--text-primary)' }}>caching layer (Phase 6)</strong> sits between the API and the retrieval/LLM layers.
          Identical queries return instantly via MD5-hashed in-memory cache, bypassing Gemini entirely.
        </p>
      </section>

      <section style={{ marginTop: '2.5rem' }}>
        <h2 style={{ fontSize: '1.3rem', marginBottom: '1.25rem' }}>Phase-by-Phase Breakdown</h2>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <PhaseCard
            phase="0"
            title="Foundation"
            module="milestone0/app/"
            description="FastAPI scaffold with health check, environment configuration via pydantic-settings, and lifespan-managed dataset loading on startup."
          />
          <PhaseCard
            phase="1"
            title="Data Ingestion"
            module="milestone1/ingestion/"
            description="Loads ManikaSaini/zomato-restaurant-recommendation from HuggingFace. Normalises ratings (0–5), cost bands (low/medium/high), and cuisine arrays. Deduplicates by name + location."
          />
          <PhaseCard
            phase="2"
            title="Preference Validation"
            module="milestone2/preferences/"
            description="Parses and validates user input into a UserPreferences object. Enforces allowed cities, budget_band enum, non-empty cuisine list, and 0–5 rating range with actionable error messages."
            dependsOn="Phase 1 (allowed city list derived from dataset)"
          />
          <PhaseCard
            phase="3"
            title="Deterministic Retrieval"
            module="milestone3/retrieval/"
            description="Four hard filters applied in sequence: location → rating → budget → cuisine overlap. Results sorted by composite score (cuisine overlap × 2 + rating). Capped at 25 candidates. Logs input count, post-filter count, and post-cap count."
            dependsOn="Phase 1, Phase 2"
          />
          <PhaseCard
            phase="4"
            title="LLM Recommendation Engine"
            module="milestone4/recommendation/"
            description="Builds a structured prompt with user preferences + serialised candidates. Calls Gemini 2.5 Flash with response_schema=RecommendationResult for guaranteed JSON. Falls back to top-3 by rating if the API fails."
            dependsOn="Phase 3"
          />
          <PhaseCard
            phase="5"
            title="Presentation Layer"
            module="milestone5/presentation/ + next-frontend/"
            description="FastAPI /api/recommend endpoint wires all phases together. Next.js frontend provides a two-column glassmorphism UI: preference form (left) and animated recommendation cards (right)."
            dependsOn="Phase 4"
          />
          <PhaseCard
            phase="6"
            title="Observability & Hardening"
            module="milestone6/observability/"
            description="LoggingMiddleware records request latency per endpoint. cache.py provides MD5-keyed in-memory response caching. filters.py logs candidate counts at each stage. engine.py logs LLM call latency and success/failure."
          />
        </div>
      </section>

      <section style={{ marginTop: '2.5rem' }}>
        <h2 style={{ fontSize: '1.3rem', marginBottom: '1rem' }}>Key Design Decisions</h2>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          {[
            {
              title: 'Deterministic filter before LLM',
              detail: 'Narrowing 12,000 records to ≤25 candidates before calling Gemini keeps token costs predictable (~1,200 input tokens per request) and prevents the model from hallucinating restaurants.',
            },
            {
              title: 'Structured LLM output',
              detail: 'Using response_schema=RecommendationResult with response_mime_type="application/json" eliminates the need for fragile regex-based response parsing.',
            },
            {
              title: 'Graceful degradation',
              detail: 'If the Gemini API is unavailable or unconfigured, the engine falls back to deterministic top-3 by rating. The user always receives a result.',
            },
            {
              title: 'Dataset loaded once at startup',
              detail: 'The HuggingFace dataset is downloaded and normalised into app.state.dataset_cache during the FastAPI lifespan. All requests read from memory — no repeated I/O.',
            },
          ].map(({ title, detail }) => (
            <div key={title} style={{ borderLeft: '3px solid var(--primary-accent)', paddingLeft: '1rem' }}>
              <p style={{ margin: '0 0 0.25rem 0', fontWeight: 600, fontSize: '0.9rem' }}>{title}</p>
              <p style={{ margin: 0, color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.6 }}>{detail}</p>
            </div>
          ))}
        </div>
      </section>

      <section style={{ marginTop: '2.5rem' }}>
        <h2 style={{ fontSize: '1.3rem', marginBottom: '1rem' }}>Project Structure</h2>
        <pre style={{
          background: 'rgba(0,0,0,0.4)',
          border: '1px solid var(--border-color)',
          padding: '1.25rem',
          borderRadius: '8px',
          fontSize: '0.8rem',
          lineHeight: 1.8,
          color: '#e2e8f0',
          overflowX: 'auto',
        }}>
{`backend/
├── src/
│   ├── milestone0/app/          # FastAPI app, config, lifespan
│   ├── milestone1/ingestion/    # HF loader, normalisation, models
│   ├── milestone2/preferences/  # UserPreferences validation
│   ├── milestone3/retrieval/    # Hard filters, candidate cap
│   ├── milestone4/recommendation/ # Prompt, LLM client, engine
│   ├── milestone5/presentation/ # /api/recommend endpoint
│   └── milestone6/observability/ # Logging middleware, cache
├── tests/                       # Unit + integration tests
└── docs/                        # Architecture & problem statement

next-frontend/
├── src/app/                     # Next.js App Router pages
│   ├── page.js                  # Main app UI
│   └── docs/                    # Phase 7 documentation
└── src/components/
    ├── PreferenceForm.jsx
    └── RecommendationList.jsx`}
        </pre>
      </section>
    </div>
  );
}
