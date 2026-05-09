"use client";

import React, { useState, useEffect } from 'react';
import { Search, MapPin, DollarSign, Utensils, Star } from 'lucide-react';

export default function PreferenceForm({ onSubmit, isLoading }) {
  const [location, setLocation] = useState('Indiranagar');
  const [budget, setBudget] = useState('medium');
  const [cuisines, setCuisines] = useState('');
  const [rating, setRating] = useState(4.2);
  const [locations, setLocations] = useState([]);
  const [validationError, setValidationError] = useState('');

  // Fetch available locations from backend
  useEffect(() => {
    const fetchLocations = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/health');
        if (response.ok) {
          // For now, use common Bangalore locations
          const commonLocations = [
            'Indiranagar', 'Koramangala', 'Bellandur', 'Whitefield', 
            'HSR Layout', 'Jayanagar', 'Marathahalli', 'Electronic City',
            'BTM Layout', 'Basavanagudi', 'Frazer Town', 'MG Road'
          ];
          setLocations(commonLocations);
        }
      } catch (err) {
        console.error('Failed to fetch locations:', err);
        // Fallback to common locations
        const fallbackLocations = [
          'Indiranagar', 'Koramangala', 'Bellandur', 'Whitefield', 
          'HSR Layout', 'Jayanagar', 'Marathahalli'
        ];
        setLocations(fallbackLocations);
      }
    };

    fetchLocations();
  }, []);

  const validateForm = () => {
    if (!location.trim()) {
      setValidationError('Please select a location');
      return false;
    }
    if (rating < 0 || rating > 5) {
      setValidationError('Rating must be between 0 and 5');
      return false;
    }
    setValidationError('');
    return true;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    const cuisineList = cuisines.split(',').map(c => c.trim()).filter(c => c.length > 0);
    
    onSubmit({ 
      location, 
      budget_band: budget, 
      cuisines: cuisineList.length > 0 ? cuisineList : null, 
      minimum_rating: parseFloat(rating) 
    });
  };

  return (
    <div className="glass-panel form-panel">
      <h2>Find Your Perfect Spot</h2>
      <p>Tell us your preferences and let AI find the best restaurants for you.</p>
      
      {validationError && (
        <div className="validation-error">
          <span>{validationError}</span>
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="preference-form">
        <div className="form-group">
          <label><MapPin size={16} /> Location</label>
          <select 
            value={location} 
            onChange={e => setLocation(e.target.value)} 
            required
            className="location-select"
          >
            <option value="">Select a location...</option>
            {locations.map(loc => (
              <option key={loc} value={loc}>{loc}</option>
            ))}
          </select>
        </div>
        
        <div className="form-group">
          <label><DollarSign size={16} /> Budget Band</label>
          <select value={budget} onChange={e => setBudget(e.target.value)}>
            <option value="low">Low (≤ ₹500)</option>
            <option value="medium">Medium (₹500 - ₹1200)</option>
            <option value="high">High (&gt; ₹1200)</option>
          </select>
        </div>
        
        <div className="form-group">
          <label><Utensils size={16} /> Cuisines (comma separated)</label>
          <input 
            type="text" 
            value={cuisines} 
            onChange={e => setCuisines(e.target.value)} 
            placeholder="e.g. Italian, Cafe, Chinese" 
            className="cuisines-input"
          />
          <small>Optional: Leave empty for all cuisines</small>
        </div>
        
        <div className="form-group">
          <label><Star size={16} /> Minimum Rating: {rating.toFixed(1)}</label>
          <input 
            type="range" 
            min="0" 
            max="5" 
            step="0.1" 
            value={rating} 
            onChange={e => setRating(parseFloat(e.target.value))} 
            className="rating-slider"
          />
          <div className="rating-labels">
            <span>0</span>
            <span>2.5</span>
            <span>5</span>
          </div>
        </div>
        
        <button type="submit" className="submit-btn" disabled={isLoading}>
          {isLoading ? 'Searching...' : <><Search size={18} /> Find Restaurants</>}
        </button>
      </form>
    </div>
  );
}
