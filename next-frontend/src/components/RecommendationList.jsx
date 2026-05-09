"use client";

import React from 'react';
import { Utensils, AlertCircle, Copy } from 'lucide-react';

export default function RecommendationList({ results, isLoading, error }) {
  
  if (isLoading) {
    return (
      <div className="glass-panel results-panel loading-state">
        <div className="spinner"></div>
        <p>Curating the best options using AI...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="glass-panel results-panel error-state">
        <AlertCircle size={48} color="#ef4444" />
        <h3>Connection Error</h3>
        <p>{error}</p>
      </div>
    );
  }

  if (!results) {
    return (
      <div className="glass-panel results-panel empty-state">
        <Utensils size={48} opacity={0.5} />
        <h3>Awaiting Your Preferences</h3>
        <p>Fill out the form to discover amazing restaurants.</p>
      </div>
    );
  }

  if (results.length === 0) {
    return (
      <div className="glass-panel results-panel empty-state">
        <h3>No matches found</h3>
        <p>No filter match found. Try adjusting your filters for better results.</p>
      </div>
    );
  }

  const copyAsMarkdown = () => {
    const markdown = results.map(rec => 
      `# ${rec.rank}. ${rec.restaurant_name}\n\n${rec.reasoning}\n\n---`
    ).join('\n\n');
    
    navigator.clipboard.writeText(markdown);
    alert('Copied as Markdown!');
  };

  return (
    <div className="results-panel">
      <div className="results-header">
        <h3>AI Recommendations</h3>
        <button 
          onClick={copyAsMarkdown}
          className="copy-btn"
          title="Copy as Markdown"
        >
          <Copy size={16} />
        </button>
      </div>
      
      <div className="results-container">
        {results.map((rec, idx) => (
          <div key={idx} className="glass-panel recommendation-card" style={{animationDelay: `${idx * 0.1}s`}}>
            <div className="card-header">
              <span className="rank">#{rec.rank}</span>
              <h3>{rec.restaurant_name}</h3>
            </div>
            <p className="reasoning">{rec.reasoning}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
