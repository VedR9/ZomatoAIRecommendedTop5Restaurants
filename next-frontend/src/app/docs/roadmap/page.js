import React from 'react';

export default function RoadmapPage() {
  return (
    <div className="glass-panel" style={{ padding: '2rem' }}>
      <h1>Roadmap & Acceptance Checklist</h1>
      
      <h3 style={{ marginTop: '2rem' }}>Phase 7 Milestone Checklist</h3>
      <ul style={{ listStyleType: 'none', paddingLeft: 0 }}>
        <li style={{ marginBottom: '0.5rem' }}>✅ <strong>Phase 1:</strong> Data Ingestion & Deduplication</li>
        <li style={{ marginBottom: '0.5rem' }}>✅ <strong>Phase 3:</strong> Deterministic Candidate Retrieval</li>
        <li style={{ marginBottom: '0.5rem' }}>✅ <strong>Phase 4:</strong> LLM Integration & Graceful Fallback</li>
        <li style={{ marginBottom: '0.5rem' }}>✅ <strong>Phase 5:</strong> Next.js Presentation Layer</li>
        <li style={{ marginBottom: '0.5rem' }}>✅ <strong>Phase 6:</strong> Observability & Request Caching</li>
        <li style={{ marginBottom: '0.5rem' }}>✅ <strong>Phase 7:</strong> Project Documentation & Handoff</li>
      </ul>

      <h3 style={{ marginTop: '2rem' }}>Known Limitations</h3>
      <ul>
        <li style={{ marginBottom: '0.5rem' }}><strong>Dataset Staleness:</strong> The Zomato dataset is static. Live restaurant closures or menu changes will not be reflected.</li>
        <li style={{ marginBottom: '0.5rem' }}><strong>Candidate Cap:</strong> We currently cap deterministic retrieval to 25 restaurants to fit within LLM context windows efficiently. If there are 100 perfect matches, the AI only evaluates the first 25.</li>
      </ul>

      <h3 style={{ marginTop: '2rem' }}>Future Roadmap</h3>
      <ul>
        <li>Implement vector-based semantic search for menus using embeddings.</li>
        <li>Connect to a live Google Maps API for real-time operating hours.</li>
        <li>Add a user authentication layer to save favorite recommendations.</li>
      </ul>
    </div>
  );
}
