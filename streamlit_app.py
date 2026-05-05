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


st.sidebar.header("Your Preferences")

# Load dataset and get locations/cuisines for dropdowns
@st.cache_resource(show_spinner=False)
def load_dataset_with_options():
    dataset = load_dataset()
    locations = sorted(set(r.location for r in dataset))
    cuisines = sorted(set(c for r in dataset for c in (r.cuisines or [])))
    return dataset, locations, cuisines

# Load dataset and options
dataset, locations, all_cuisines = load_dataset_with_options()

location = st.sidebar.selectbox("Location", options=locations, index=0)
budget = st.sidebar.selectbox("Budget Band", ["low", "medium", "high"], index=1)
cuisines_input = st.sidebar.multiselect("Cuisines (optional)", options=all_cuisines, placeholder="Any cuisine")
rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 4.2, 0.1)

if st.sidebar.button("Find Restaurants"):
    # Check API key only when user clicks the button
    if not (os.environ.get("GEMINI_API_KEY") or os.environ.get("LLM_API_KEY")):
        st.warning("Please provide a Gemini API Key to use the AI engine. (Otherwise, deterministic fallback will be used).")
        
    with st.spinner("Curating the best options using AI..."):
        cuisine_list = cuisines_input  # already a list from multiselect
        prefs = RetrievalPreferences(
            location=location,
            budget_band=budget,
            cuisines=cuisine_list if cuisine_list else None,
            minimum_rating=rating
        )
        
        # Show user preferences
        st.sidebar.markdown("---")
        st.sidebar.markdown("**Your Preferences:**")
        st.sidebar.write(f"📍 Location: {location}")
        st.sidebar.write(f"💰 Budget: {budget}")
        st.sidebar.write(f"🍽️ Cuisines: {cuisine_list if cuisine_list else 'Any'}")
        st.sidebar.write(f"⭐ Min Rating: {rating}")
        
        candidates = retrieve_candidates(dataset, prefs, candidate_cap=25)
        restaurant_lookup = {c.id: c for c in candidates}

        st.info(f"Found {len(candidates)} restaurants matching your criteria. Now using AI to recommend the best ones...")

        if not candidates:
            st.warning("No matches found. Try adjusting your filters.")
        else:
            try:
                result = generate_recommendations(prefs, candidates)
            except Exception as e:
                st.error(f"AI engine error: {e}")
                st.stop()

            if result and result.recommendations:
                st.success(f"🎯 AI recommends {len(result.recommendations)} restaurants from {len(candidates)} matches:")
                for rec in result.recommendations:
                    st.markdown(f"### #{rec.rank} {rec.restaurant_name}")
                    st.write(rec.reasoning)
                    r = restaurant_lookup.get(rec.restaurant_id)
                    if r:
                        if r.rating:
                            st.write(f"⭐ Rating: {r.rating}")
                        if r.cuisines:
                            st.write(f"🍴 Cuisines: {', '.join(r.cuisines)}")
                        if r.location:
                            st.write(f"📍 Location: {r.location}")
                        if r.cost_for_two:
                            st.write(f"💰 Approximate price for two: ₹{int(r.cost_for_two)}")
                    st.markdown("---")
            else:
                st.error("AI couldn't generate recommendations. Please try again.")
