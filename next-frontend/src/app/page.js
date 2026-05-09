"use client";

import React, { useState, useEffect } from "react";
import { MapPin, Search, Star, DollarSign, Cpu, Heart, MapPinned, Zap } from "lucide-react";

const FOOD_EMOJIS = ["🍕", "🍜", "🍣", "🥘", "🍛", "🥗", "🍔", "🌮", "🍱", "🫕"];
const QUICK_PILLS = ["Chinese", "Indian", "Western", "American", "Mexican", "Italian", "Japanese", "Thai"];
const BUDGET_OPTIONS = [
  { value: "low",    label: "Low (≤ ₹500)" },
  { value: "medium", label: "Medium (₹500–₹1200)" },
  { value: "high",   label: "High (> ₹1200)" },
];
const FEATURES = [
  {
    icon: <Cpu size={20} />,
    title: "AI Powered",
    desc: "Our AI learns your taste, likes and habits to find your perfect restaurant match.",
  },
  {
    icon: <Heart size={20} />,
    title: "Personalized",
    desc: "From your favorite cuisines to your mood, we've got you covered every time.",
  },
  {
    icon: <MapPinned size={20} />,
    title: "Local & Trusted",
    desc: "Discover top rated local gems and hidden favorites near you.",
  },
  {
    icon: <Zap size={20} />,
    title: "Save Time",
    desc: "No more endless scrolling. Get the best recommendations, instantly.",
  },
];

function StarRating({ rating }) {
  if (!rating) return null;
  return (
    <span className="meta-pill">
      <Star size={11} fill="#facc15" color="#facc15" />
      {rating.toFixed(1)}
    </span>
  );
}

export default function Home() {
  const [location, setLocation]   = useState("");
  const [craving, setCraving]     = useState("");
  const [budget, setBudget]       = useState("medium");
  const [rating, setRating]       = useState(4.0);
  const [locations, setLocations] = useState([]);
  const [results, setResults]     = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError]         = useState(null);

  const API = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

  useEffect(() => {
    fetch(`${API}/api/locations`)
      .then((r) => r.json())
      .then((data) => {
        setLocations(data);
        if (data.length > 0) setLocation(data[0]);
      })
      .catch(() => {});
  }, []);

  const handleSearch = async () => {
    if (!location) return;
    setIsLoading(true);
    setError(null);
    try {
      const cuisineList = craving
        .split(",")
        .map((c) => c.trim())
        .filter(Boolean);
      const res = await fetch(`${API}/api/recommend`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          location,
          budget_band: budget,
          cuisines: cuisineList,
          minimum_rating: rating,
        }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setResults(data.recommendations || []);
    } catch {
      setError(`Failed to connect to backend at ${API}. Make sure it's running.`);
      setResults([]);
    } finally {
      setIsLoading(false);
    }
  };

  const topResult = results?.[0];

  return (
    <div>
      {/* ── Navbar ── */}
      <nav className="navbar">
        <div className="nav-inner">
          <a href="/" className="nav-logo">
            bite<span>AI</span>
          </a>
          <div className="nav-links">
            <a href="#">Explore</a>
            <a href="#">Collections</a>
            <a href="#">How it Works</a>
            <a href="#">For Restaurants</a>
          </div>
          <div className="nav-actions">
            <button className="btn-ghost">Login</button>
            <button className="btn-red">Sign Up</button>
          </div>
        </div>
      </nav>

      {/* ── Hero ── */}
      <section className="hero">
        <div className="hero-inner">
          <div className="hero-content">
            <h1>
              AI recommends.
              <br />
              You <em>enjoy.</em>
            </h1>
            <p className="hero-subtitle">
              Discover the best restaurants, personalized for your taste, mood
              and cravings — powered by AI.
            </p>

            {/* Search bar */}
            <div className="search-bar">
              <div className="search-field">
                <MapPin size={15} />
                <select
                  value={location}
                  onChange={(e) => setLocation(e.target.value)}
                >
                  {locations.map((loc) => (
                    <option key={loc} value={loc}>
                      {loc}
                    </option>
                  ))}
                </select>
              </div>
              <div className="search-divider" />
              <div className="search-field">
                <Search size={15} />
                <input
                  value={craving}
                  onChange={(e) => setCraving(e.target.value)}
                  placeholder="What are you craving?"
                  onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                />
              </div>
              <button
                className="search-btn"
                onClick={handleSearch}
                disabled={isLoading || !location}
              >
                {isLoading ? "Searching…" : "Find Restaurants"}
              </button>
            </div>

            {/* Budget chips + rating */}
            <div className="secondary-filters">
              <div className="budget-chips">
                {BUDGET_OPTIONS.map((opt) => (
                  <button
                    key={opt.value}
                    className={`chip ${budget === opt.value ? "active" : ""}`}
                    onClick={() => setBudget(opt.value)}
                  >
                    {opt.label}
                  </button>
                ))}
              </div>
              <div className="rating-filter">
                <span className="rating-filter-label">
                  <Star size={14} fill="#facc15" color="#facc15" />
                  Min. Rating
                </span>
                <input
                  type="range"
                  min="0"
                  max="5"
                  step="0.1"
                  value={rating}
                  onChange={(e) => setRating(parseFloat(e.target.value))}
                />
                <span className="rating-value">{rating.toFixed(1)}</span>
              </div>
            </div>

            {/* Quick category pills */}
            <div className="quick-pills">
              {QUICK_PILLS.map((pill) => (
                <button
                  key={pill}
                  className="quick-pill"
                  onClick={() => setCraving(pill)}
                >
                  {pill}
                </button>
              ))}
            </div>
          </div>

          {/* Right — featured card */}
          <div className="hero-visual">
            {topResult ? (
              <div className="featured-card">
                <div className="featured-image">
                  <span>{FOOD_EMOJIS[topResult.rank % FOOD_EMOJIS.length]}</span>
                  <div className="match-badge">99% Match</div>
                </div>
                <div className="featured-body">
                  <div className="featured-name">{topResult.restaurant_name}</div>
                  <div className="featured-meta">
                    {topResult.cuisines?.slice(0, 2).map((c) => (
                      <span key={c} className="featured-tag">{c}</span>
                    ))}
                    {topResult.rating && (
                      <span>⭐ {topResult.rating.toFixed(1)}</span>
                    )}
                    {topResult.cost_for_two && (
                      <span>₹{topResult.cost_for_two} for two</span>
                    )}
                  </div>
                  <div className="featured-reasoning">
                    <strong>Why we recommend this?</strong>
                    {topResult.reasoning}
                  </div>
                </div>
              </div>
            ) : (
              <div className="hero-placeholder">
                <div className="placeholder-image">🍽️</div>
                <div className="placeholder-body">
                  {[75, 50, 65, 40].map((w, i) => (
                    <div
                      key={i}
                      className="placeholder-line"
                      style={{ width: `${w}%`, animationDelay: `${i * 0.2}s` }}
                    />
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* ── Loading ── */}
      {isLoading && (
        <div className="loading-overlay">
          <div className="spinner" />
          <p>Curating the best options using AI…</p>
        </div>
      )}

      {/* ── Results ── */}
      {!isLoading && results !== null && (
        <section className="results-section">
          {error && <div className="error-banner">{error}</div>}
          <div className="section-header">
            <h2 className="section-title">Smart recommendations, just for you</h2>
            <p className="section-sub">
              {results.length > 0
                ? `${results.length} great match${results.length !== 1 ? "es" : ""} in ${location}`
                : "No restaurants matched your filters — try relaxing your criteria."}
            </p>
          </div>
          <div className="results-grid">
            {results.map((rec, idx) => (
              <div
                key={rec.restaurant_id}
                className="rec-card"
                style={{ animationDelay: `${idx * 0.07}s` }}
              >
                <div className="rec-card-image">
                  <span>{FOOD_EMOJIS[idx % FOOD_EMOJIS.length]}</span>
                  <div className="rec-rank">#{rec.rank}</div>
                </div>
                <div className="rec-body">
                  <div className="rec-name">{rec.restaurant_name}</div>
                  <div className="rec-meta">
                    <StarRating rating={rec.rating} />
                    {rec.location && (
                      <span className="meta-pill">
                        <MapPin size={10} />
                        {rec.location}
                      </span>
                    )}
                    {rec.cost_for_two && (
                      <span className="meta-pill">
                        <DollarSign size={10} />₹{rec.cost_for_two} for two
                      </span>
                    )}
                    {rec.cuisines?.slice(0, 3).map((c) => (
                      <span key={c} className="cuisine-tag">{c}</span>
                    ))}
                  </div>
                  <p className="rec-reasoning">{rec.reasoning}</p>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* ── Features (pre-search) ── */}
      {results === null && !isLoading && (
        <section className="features-section">
          <h2 className="section-title">Smart recommendations, just for you</h2>
          <div className="features-divider" />
          <div className="features-grid">
            {FEATURES.map((f) => (
              <div key={f.title} className="feature-card">
                <div className="feature-icon">{f.icon}</div>
                <div className="feature-title">{f.title}</div>
                <p className="feature-desc">{f.desc}</p>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
