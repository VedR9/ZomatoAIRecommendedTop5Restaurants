import React from 'react';

const Requirement = ({ number, title, children }) => (
  <div style={{
    borderLeft: '3px solid var(--primary-accent)',
    paddingLeft: '1rem',
    marginBottom: '1.5rem',
  }}>
    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.4rem' }}>
      <span style={{
        background: 'var(--primary-accent)',
        color: 'white',
        borderRadius: '50%',
        width: '24px',
        height: '24px',
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: '0.75rem',
        fontWeight: 700,
        flexShrink: 0,
      }}>{number}</span>
      <strong style={{ fontSize: '1rem' }}>{title}</strong>
    </div>
    <div style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.7 }}>{children}</div>
  </div>
);

export default function ProblemStatementPage() {
  return (
    <div>
      <h1 style={{ margin: 0, fontSize: '2rem', fontWeight: 800 }}>Problem Statement</h1>
      <p style={{ color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
        The goal, constraints, and success criteria for this project.
      </p>

      <section style={{ marginTop: '2.5rem' }}>
        <h2 style={{ fontSize: '1.3rem', marginBottom: '0.75rem' }}>Overview</h2>
        <p style={{ color: 'var(--text-secondary)', lineHeight: 1.7 }}>
          Build an AI-powered restaurant recommendation service inspired by Zomato.
          The system combines structured restaurant data with a large language model to produce
          personalised, trustworthy recommendations based on user preferences — not generic suggestions.
        </p>
      </section>

      <section style={{ marginTop: '2.5rem' }}>
        <h2 style={{ fontSize: '1.3rem', marginBottom: '1rem' }}>Data Source</h2>
        <div style={{
          background: 'rgba(99,102,241,0.08)',
          border: '1px solid rgba(99,102,241,0.25)',
          borderRadius: '8px',
          padding: '1rem 1.25rem',
        }}>
          <p style={{ margin: '0 0 0.25rem 0', fontWeight: 600 }}>ManikaSaini/zomato-restaurant-recommendation</p>
          <p style={{ margin: '0 0 0.75rem 0', color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
            ~12,000 real restaurant listings from Zomato India, hosted on Hugging Face.
          </p>
          <p style={{ margin: 0, color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
            Key fields extracted and normalised: <strong style={{ color: 'var(--text-primary)' }}>name, location, cuisines, estimated cost, rating</strong>
          </p>
        </div>
      </section>

      <section style={{ marginTop: '2.5rem' }}>
        <h2 style={{ fontSize: '1.3rem', marginBottom: '1.25rem' }}>Functional Requirements</h2>
        <Requirement number="1" title="User Input">
          Accept four structured preference fields from the user:
          <ul style={{ marginTop: '0.5rem', paddingLeft: '1.25rem' }}>
            <li><strong style={{ color: 'var(--text-primary)' }}>Location</strong> — city or neighbourhood (e.g., Indiranagar, Delhi)</li>
            <li><strong style={{ color: 'var(--text-primary)' }}>Budget band</strong> — low (≤₹500), medium (₹500–₹1,200), or high ({'>'} ₹1,200)</li>
            <li><strong style={{ color: 'var(--text-primary)' }}>Preferred cuisines</strong> — one or more (e.g., Italian, Café)</li>
            <li><strong style={{ color: 'var(--text-primary)' }}>Minimum rating</strong> — 0.0 to 5.0</li>
          </ul>
        </Requirement>
        <Requirement number="2" title="Candidate Retrieval">
          Filter the dataset deterministically using the user preferences before involving the LLM.
          Handle no-match scenarios gracefully with a clear message rather than an error.
        </Requirement>
        <Requirement number="3" title="LLM-Based Recommendation">
          Provide the filtered candidates and user preferences to an LLM.
          The model must rank options and provide concise explanations grounded strictly in the provided candidate list —
          it must not invent restaurants.
        </Requirement>
        <Requirement number="4" title="Output Display">
          Show top recommendations with all required fields: restaurant name, cuisine, rating,
          estimated cost, and an AI-generated explanation for the ranking.
        </Requirement>
      </section>

      <section style={{ marginTop: '2.5rem' }}>
        <h2 style={{ fontSize: '1.3rem', marginBottom: '1rem' }}>Non-Goals (v1)</h2>
        <ul style={{ color: 'var(--text-secondary)', lineHeight: 2, paddingLeft: '1.25rem' }}>
          <li>User accounts and personalisation history</li>
          <li>Live third-party restaurant APIs (Google Maps, Zomato live feed)</li>
          <li>Map integration and real-time operating hours</li>
          <li>Semantic / vector search over menu descriptions</li>
        </ul>
      </section>

      <section style={{ marginTop: '2.5rem' }}>
        <h2 style={{ fontSize: '1.3rem', marginBottom: '1rem' }}>Success Criteria</h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginBottom: '1rem' }}>
          The project is successful when a user can complete the following flow end-to-end in a single run:
        </p>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          {[
            'Enter preferences in the UI (location, budget, cuisines, rating)',
            'Receive grounded recommendations sourced from the real dataset',
            'Read a clear AI-generated rationale for each recommendation',
            'See helpful feedback when no restaurants match (not a crash)',
            'Get a result even when the LLM API is unavailable (graceful fallback)',
          ].map((criterion, i) => (
            <div key={i} style={{
              display: 'flex',
              alignItems: 'flex-start',
              gap: '0.75rem',
              background: 'rgba(255,255,255,0.03)',
              border: '1px solid var(--border-color)',
              borderRadius: '8px',
              padding: '0.75rem 1rem',
            }}>
              <span style={{ color: '#22c55e', fontSize: '1rem', flexShrink: 0 }}>✓</span>
              <span style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>{criterion}</span>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
