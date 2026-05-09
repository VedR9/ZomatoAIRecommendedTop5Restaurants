import React from 'react';

const Section = ({ title, children }) => (
  <section style={{ marginTop: '2.5rem' }}>
    <h2 style={{ fontSize: '1.3rem', marginBottom: '1rem', color: 'var(--text-primary)' }}>{title}</h2>
    {children}
  </section>
);

const CodeBlock = ({ children }) => (
  <pre style={{
    background: 'rgba(0,0,0,0.4)',
    border: '1px solid var(--border-color)',
    padding: '1.25rem',
    borderRadius: '8px',
    marginTop: '0.75rem',
    overflowX: 'auto',
    fontSize: '0.875rem',
    lineHeight: 1.6,
    color: '#e2e8f0',
  }}>
    <code>{children}</code>
  </pre>
);

const Note = ({ children }) => (
  <p style={{
    background: 'rgba(99,102,241,0.1)',
    border: '1px solid rgba(99,102,241,0.3)',
    borderRadius: '8px',
    padding: '0.75rem 1rem',
    color: 'var(--text-secondary)',
    fontSize: '0.875rem',
    marginTop: '0.75rem',
  }}>
    {children}
  </p>
);

export default function SetupPage() {
  return (
    <div>
      <h1 style={{ margin: 0, fontSize: '2rem', fontWeight: 800 }}>Setup Guide</h1>
      <p style={{ color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
        Get the AI Restaurant Recommendation System running locally in under 5 minutes.
      </p>

      <Section title="Prerequisites">
        <ul style={{ color: 'var(--text-secondary)', lineHeight: 2, paddingLeft: '1.25rem' }}>
          <li>Python <strong style={{ color: 'var(--text-primary)' }}>3.11+</strong></li>
          <li>Node.js <strong style={{ color: 'var(--text-primary)' }}>18+</strong></li>
          <li>A <strong style={{ color: 'var(--text-primary)' }}>Google Gemini API key</strong> — obtain one free at <a href="https://aistudio.google.com/app/apikey" target="_blank" rel="noopener noreferrer" style={{ color: 'var(--primary-accent)' }}>aistudio.google.com</a></li>
        </ul>
      </Section>

      <Section title="1. Clone & Configure Environment">
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
          Copy the example env file and add your Gemini API key.
        </p>
        <CodeBlock>{`cd backend
cp .env.example .env`}</CodeBlock>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginTop: '0.75rem' }}>
          Open <code style={{ background: 'rgba(255,255,255,0.1)', padding: '0.1rem 0.3rem', borderRadius: '4px' }}>.env</code> and set:
        </p>
        <CodeBlock>{`LLM_API_KEY=your_gemini_api_key_here`}</CodeBlock>
        <Note>
          💡 The system degrades gracefully without an API key — it falls back to deterministic rating-based ranking.
        </Note>
      </Section>

      <Section title="2. Install Backend Dependencies">
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
          Create a virtual environment and install the package in editable mode.
        </p>
        <CodeBlock>{`cd backend
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\\Scripts\\activate
pip install -e ".[dev]"`}</CodeBlock>
      </Section>

      <Section title="3. Start the FastAPI Backend">
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
          The backend loads ~12,000 restaurant records from Hugging Face on first startup (takes ~10s).
        </p>
        <CodeBlock>{`uvicorn milestone0.app.main:app --app-dir src --reload --port 8000`}</CodeBlock>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginTop: '0.75rem' }}>
          Verify it is running:
        </p>
        <CodeBlock>{`curl http://localhost:8000/health
# → {"status": "ok"}`}</CodeBlock>
      </Section>

      <Section title="4. Start the Next.js Frontend">
        <CodeBlock>{`cd next-frontend
npm install
npm run dev`}</CodeBlock>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginTop: '0.75rem' }}>
          Open <a href="http://localhost:3000" target="_blank" rel="noopener noreferrer" style={{ color: 'var(--primary-accent)' }}>http://localhost:3000</a> to use the app.
        </p>
      </Section>

      <Section title="5. Run Tests">
        <CodeBlock>{`cd backend
pytest                          # all unit tests
pytest -m integration           # end-to-end flow (requires LLM_API_KEY)
ruff check .                    # linting`}</CodeBlock>
      </Section>

      <Section title="Common Issues">
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {[
            {
              problem: 'HuggingFace download fails on startup',
              fix: 'Ensure you have internet access. The dataset is ~6MB. Subsequent starts use an in-memory cache.',
            },
            {
              problem: 'CORS error from frontend',
              fix: 'Confirm the backend is running on port 8000. The frontend is hardcoded to http://localhost:8000.',
            },
            {
              problem: '"LLM API Key is not configured" warning',
              fix: 'Add LLM_API_KEY to your .env file. Without it, recommendations fall back to deterministic top-rated results.',
            },
          ].map(({ problem, fix }) => (
            <div key={problem} style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid var(--border-color)', borderRadius: '8px', padding: '1rem' }}>
              <p style={{ margin: '0 0 0.25rem 0', fontWeight: 600, color: 'var(--text-primary)', fontSize: '0.9rem' }}>⚠ {problem}</p>
              <p style={{ margin: 0, color: 'var(--text-secondary)', fontSize: '0.875rem' }}>{fix}</p>
            </div>
          ))}
        </div>
      </Section>
    </div>
  );
}
