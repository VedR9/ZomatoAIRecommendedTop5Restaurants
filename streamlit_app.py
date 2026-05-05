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
    try:
        return load_restaurants_from_huggingface()
    except Exception as e:
        st.error(f"Failed to load dataset from Hugging Face: {str(e)}")
        st.info("Using sample data for demonstration. Please check your internet connection.")
        # Return sample data as fallback
        return get_sample_data()

def get_sample_data():
    """Return sample restaurant data for demo purposes"""
    from milestone1.ingestion.models import Restaurant
    
    sample_restaurants = [
        Restaurant(
            id="sample1",
            name="The Pizza Bakery",
            location="Indiranagar",
            cuisines=["Italian", "Pizza"],
            cost_for_two=800.0,
            rating=4.5
        ),
        Restaurant(
            id="sample2", 
            name="Bologna",
            location="Indiranagar",
            cuisines=["Italian", "Continental"],
            cost_for_two=1000.0,
            rating=4.3
        ),
        Restaurant(
            id="sample3",
            name="Pot-O-Noodles",
            location="Indiranagar", 
            cuisines=["Chinese", "Asian"],
            cost_for_two=600.0,
            rating=4.2
        ),
        Restaurant(
            id="sample4",
            name="Onesta",
            location="Bellandur",
            cuisines=["Italian", "Cafe"],
            cost_for_two=700.0,
            rating=4.1
        ),
        Restaurant(
            id="sample5",
            name="Tipsy Bull",
            location="Bellandur",
            cuisines=["North Indian", "Bar"],
            cost_for_two=1400.0,
            rating=4.4
        ),
        Restaurant(
            id="sample6",
            name="Smoor",
            location="Indiranagar",
            cuisines=["Continental", "Desserts"],
            cost_for_two=1200.0,
            rating=4.6
        ),
        Restaurant(
            id="sample7",
            name="Bangalore Mandarin",
            location="Bellandur",
            cuisines=["Chinese", "Asian"],
            cost_for_two=900.0,
            rating=4.2
        ),
        Restaurant(
            id="sample8",
            name="Glassy",
            location="Bellandur",
            cuisines=["North Indian", "Bar"],
            cost_for_two=1400.0,
            rating=4.2
        ),
        Restaurant(
            id="sample9",
            name="Chili's American Grill",
            location="Indiranagar",
            cuisines=["American", "Mexican"],
            cost_for_two=1500.0,
            rating=4.4
        ),
        Restaurant(
            id="sample10",
            name="MoMo Cafe",
            location="Bellandur",
            cuisines=["Asian", "Momos"],
            cost_for_two=800.0,
            rating=4.2
        )
    ]
    return sample_restaurants

with st.spinner("Loading Zomato dataset (this happens once)..."):
    dataset = load_dataset()
    st.success(f"Loaded {len(dataset)} restaurants!")

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
        
        # Show user preferences
        st.sidebar.markdown("---")
        st.sidebar.markdown("**Your Preferences:**")
        st.sidebar.write(f"📍 Location: {location}")
        st.sidebar.write(f"💰 Budget: {budget}")
        st.sidebar.write(f"🍽️ Cuisines: {cuisine_list if cuisine_list else 'Any'}")
        st.sidebar.write(f"⭐ Min Rating: {rating}")
        
        candidates = retrieve_candidates(dataset, prefs, candidate_cap=25)
        
        st.info(f"Found {len(candidates)} restaurants matching your criteria. Now using AI to recommend the best ones...")
        
        if not candidates:
            st.warning("No matches found. Try adjusting your filters.")
        else:
            # We call our Phase 4 Engine directly!
            result = generate_recommendations(prefs, candidates)
            
            if result and result.recommendations:
                st.success(f"🎯 AI recommends {len(result.recommendations)} restaurants from {len(candidates)} matches:")
                for rec in result.recommendations:
                    st.markdown(f"### #{rec.rank} {rec.restaurant_name}")
                    st.write(rec.reasoning)
                    st.markdown("---")
            else:
                st.error("AI couldn't generate recommendations. Please try again.")
