import streamlit as st
import os
import sys

# Add the backend src directory to the path so we can import our modules directly
sys.path.append(os.path.join(os.path.dirname(__file__), "backend", "src"))

from milestone1.ingestion.loader import load_restaurants_from_huggingface
from milestone3.retrieval.models import RetrievalPreferences
from milestone3.retrieval.filters import retrieve_candidates
from milestone4.recommendation.engine import generate_recommendations

st.set_page_config(page_title="Zomato AI Guide", page_icon="🍽️", layout="centered")

st.title("Zomato AI Guide 🍽️")
st.write("Discover your next favorite meal, powered by Gemini. (Streamlit Version)")

@st.cache_resource(show_spinner=False)
def load_dataset():
    # Cache the dataset in memory so it doesn't reload on every UI interaction
    return load_restaurants_from_huggingface()

with st.spinner("Loading Zomato dataset (this happens once)..."):
    dataset = load_dataset()

# Provide an option to input the API key securely if not in environment or Streamlit Secrets
api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("LLM_API_KEY")
if not api_key:
    api_key = st.text_input("Enter your Gemini API Key:", type="password")
    if api_key:
        os.environ["GEMINI_API_KEY"] = api_key

st.sidebar.header("Your Preferences")
location = st.sidebar.text_input("Location", value="Indiranagar")
budget = st.sidebar.selectbox("Budget Band", ["low", "medium", "high"], index=1)
cuisines_input = st.sidebar.text_input("Cuisines (comma separated)", value="")
rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 4.2, 0.1)

if st.sidebar.button("Find Restaurants"):
    if not (os.environ.get("GEMINI_API_KEY") or os.environ.get("LLM_API_KEY")):
        st.warning("Please provide a Gemini API Key to use the AI engine. (Otherwise, the deterministic fallback will be used).")
        
    with st.spinner("Curating the best options using AI..."):
        cuisine_list = [c.strip() for c in cuisines_input.split(',')] if cuisines_input else []
        prefs = RetrievalPreferences(
            location=location,
            budget_band=budget,
            cuisines=cuisine_list if cuisine_list else None,
            minimum_rating=rating
        )
        
        candidates = retrieve_candidates(dataset, prefs, candidate_cap=25)
        
        if not candidates:
            st.warning("No matches found. Try adjusting your filters.")
        else:
            # We call our Phase 4 Engine directly!
            result = generate_recommendations(prefs, candidates)
            
            if result and result.recommendations:
                for rec in result.recommendations:
                    st.markdown(f"### #{rec.rank} {rec.restaurant_name}")
                    st.write(rec.reasoning)
                    st.markdown("---")
            else:
                st.error("Failed to generate recommendations.")
