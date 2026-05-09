import React from 'react';

const Section = ({ title, children }) => (
  <section style={{ marginTop: '2.5rem' }}>
    <h2 style={{ fontSize: '1.3rem', marginBottom: '1rem' }}>{title}</h2>
    {children}
  </section>
);

const MetricRow = ({ label, value, note }) => (
  <div style={{
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '0.5rem',
    padding: '0.75rem 1rem',
    borderBottom: '1px solid var(--border-color)',
    fontSize: '0.875rem',
  }}>
    <span style={{ color: 'var(--text-secondary)' }}>{label}</span>
    <div>
      <span style={{ color: 'var(--text-primary)', fontWeight: 600 }}>{value}</span>
      {note && <span style={{ color: 'var(--text-secondary)', marginLeft: '0.5rem' }}>{note}</span>}
    </div>
  </div>
);

export default function DeploymentPage() {
  return (
    <div>
      <h1 style={{ margin: 0, fontSize: '2rem', fontWeight: 800 }}>Deployment & Cost Guidance</h1>
      <p style={{ color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
        How to ship this system to production and what it will cost to run.
      </p>

      <Section title="Deployment Architecture">
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {[
            {
              label: 'Backend (FastAPI)',
              platform: 'Google Cloud Run / AWS Fargate / Render',
              notes: [
                'Containerise with Docker. The Dockerfile should run pip install -e ".[dev]" and start uvicorn.',
                'Minimum 1 GB RAM — the dataset cache holds ~12,000 Restaurant objects in memory.',
                'Set the LLM_API_KEY environment variable in your cloud provider\'s secret manager.',
                'Health check: GET /health → {"status": "ok"}',
              ],
            },
            {
              label: 'Frontend (Next.js)',
              platform: 'Vercel (recommended) / Netlify / any static host',
              notes: [
                'Push the next-frontend/ directory. Vercel detects Next.js automatically.',
                'Set NEXT_PUBLIC_API_URL to your deployed backend URL.',
                'Update the fetch call in page.js from http://localhost:8000 to the env var.',
              ],
            },
          ].map(({ label, platform, notes }) => (
            <div key={label} style={{
              background: 'rgba(255,255,255,0.03)',
              border: '1px solid var(--border-color)',
              borderRadius: '10px',
              padding: '1.25rem',
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                <strong>{label}</strong>
                <span style={{
                  background: 'rgba(99,102,241,0.15)',
                  border: '1px solid rgba(99,102,241,0.3)',
                  borderRadius: '6px',
                  padding: '0.2rem 0.6rem',
                  fontSize: '0.75rem',
                  color: 'var(--primary-accent)',
                }}>{platform}</span>
              </div>
              <ul style={{ margin: 0, paddingLeft: '1.25rem', color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.9 }}>
                {notes.map(n => <li key={n}>{n}</li>)}
              </ul>
            </div>
          ))}
        </div>
      </Section>

      <Section title="Latency Profile">
        <div style={{ background: 'rgba(0,0,0,0.3)', border: '1px solid var(--border-color)', borderRadius: '8px', overflow: 'hidden' }}>
          <MetricRow label="Dataset load (startup, once)" value="~8–12 s" note="HuggingFace download + normalisation" />
          <MetricRow label="Deterministic filtering" value="< 20 ms" note="In-memory scan of ~12,000 records" />
          <MetricRow label="Gemini 2.5 Flash (p50)" value="~1.5–3 s" note="25 candidates, structured JSON output" />
          <MetricRow label="Cache hit (repeated query)" value="< 5 ms" note="MD5 lookup, no LLM call" />
          <MetricRow label="Total end-to-end (cold)" value="~2–4 s" note="Filter + LLM" />
          <MetricRow label="Total end-to-end (cache hit)" value="< 30 ms" note="Middleware + cache lookup" />
        </div>
      </Section>

      <Section title="Cost Guidance (Google Gemini 2.5 Flash)">
        <div style={{ background: 'rgba(0,0,0,0.3)', border: '1px solid var(--border-color)', borderRadius: '8px', overflow: 'hidden', marginBottom: '1rem' }}>
          <MetricRow label="Input tokens per request" value="~1,200" note="25 serialised candidates + preferences" />
          <MetricRow label="Output tokens per request" value="~200" note="5 ranked recommendations with reasoning" />
          <MetricRow label="Input price (per 1M tokens)" value="$0.35" />
          <MetricRow label="Output price (per 1M tokens)" value="$1.05" />
          <MetricRow label="Cost per 1,000 queries (no cache)" value="~$0.63 USD" />
          <MetricRow label="Cost per 1,000 queries (50% cache hit)" value="~$0.32 USD" />
        </div>
        <div style={{
          background: 'rgba(34,197,94,0.08)',
          border: '1px solid rgba(34,197,94,0.25)',
          borderRadius: '8px',
          padding: '1rem',
          fontSize: '0.875rem',
          color: 'var(--text-secondary)',
        }}>
          <strong style={{ color: '#22c55e' }}>💡 Caching impact:</strong> The Phase 6 MD5 response cache means that common searches (e.g., &ldquo;Cafés in Indiranagar, medium budget&rdquo;) bypass Gemini entirely after the first call.
          In practice, a small set of popular preference combinations accounts for a large share of traffic, making the effective cost per query significantly lower than the no-cache estimate.
        </div>
      </Section>

      <Section title="Model Selection Guidance">
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          {[
            { model: 'gemini-2.5-flash', use: 'Default (recommended)', detail: 'Best balance of speed, cost, and structured output quality. Supports response_schema natively.' },
            { model: 'gemini-2.5-pro', use: 'Higher accuracy', detail: '~5–8× more expensive. Only justified if reasoning quality is unsatisfactory with Flash.' },
            { model: 'gemini-1.5-flash', use: 'Lower cost fallback', detail: 'Cheaper but older. Structured output support is less reliable.' },
          ].map(({ model, use, detail }) => (
            <div key={model} style={{
              display: 'grid',
              gridTemplateColumns: '180px 120px 1fr',
              gap: '1rem',
              alignItems: 'center',
              background: 'rgba(255,255,255,0.03)',
              border: '1px solid var(--border-color)',
              borderRadius: '8px',
              padding: '0.75rem 1rem',
            }}>
              <code style={{ fontSize: '0.8rem', color: 'var(--primary-accent)' }}>{model}</code>
              <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{use}</span>
              <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{detail}</span>
            </div>
          ))}
        </div>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginTop: '0.75rem' }}>
          Change the model by updating the <code style={{ background: 'rgba(255,255,255,0.1)', padding: '0.1rem 0.3rem', borderRadius: '4px' }}>model_name</code> default in{' '}
          <code style={{ background: 'rgba(255,255,255,0.1)', padding: '0.1rem 0.3rem', borderRadius: '4px' }}>milestone4/recommendation/engine.py</code>.
        </p>
      </Section>
    </div>
  );
}
