#!/usr/bin/env python3
"""
Test script to verify LLM filtering and recommendations work correctly
"""

import sys
import os

# Add backend src to path
sys.path.append(os.path.join(os.getcwd(), 'backend', 'src'))

from milestone1.ingestion.models import Restaurant
from milestone3.retrieval.models import RetrievalPreferences
from milestone3.retrieval.filters import retrieve_candidates
from milestone4.recommendation.engine import generate_recommendations

def create_sample_data():
    """Create sample restaurant data for testing"""
    restaurants = [
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
    return restaurants

def test_filtering():
    """Test the filtering logic"""
    print("🔍 Testing Filtering Logic")
    print("=" * 50)
    
    restaurants = create_sample_data()
    print(f"📊 Total restaurants: {len(restaurants)}")
    
    # Test Case 1: Italian in Indiranagar, Medium Budget, 4.2+ Rating
    print("\n📋 Test Case 1: Italian in Indiranagar, Medium Budget, 4.2+ Rating")
    prefs1 = RetrievalPreferences(
        location="Indiranagar",
        budget_band="medium",
        cuisines=["Italian"],
        minimum_rating=4.2
    )
    
    candidates1 = retrieve_candidates(restaurants, prefs1, candidate_cap=25)
    print(f"🎯 Found {len(candidates1)} candidates:")
    for c in candidates1:
        print(f"  - {c.name} ({c.location}) - {c.cuisines} - ₹{c.cost_for_two} - {c.rating}⭐")
    
    # Test Case 2: North Indian in Bellandur, High Budget, 4.0+ Rating
    print("\n📋 Test Case 2: North Indian in Bellandur, High Budget, 4.0+ Rating")
    prefs2 = RetrievalPreferences(
        location="Bellandur",
        budget_band="high",
        cuisines=["North Indian"],
        minimum_rating=4.0
    )
    
    candidates2 = retrieve_candidates(restaurants, prefs2, candidate_cap=25)
    print(f"🎯 Found {len(candidates2)} candidates:")
    for c in candidates2:
        print(f"  - {c.name} ({c.location}) - {c.cuisines} - ₹{c.cost_for_two} - {c.rating}⭐")
    
    return candidates1, candidates2

def test_llm_recommendations(candidates1, candidates2):
    """Test LLM recommendations"""
    print("\n\n🤖 Testing LLM Recommendations")
    print("=" * 50)
    
    # Check API key
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("LLM_API_KEY")
    if not api_key:
        print("❌ No API key found. Set GEMINI_API_KEY or LLM_API_KEY environment variable.")
        return
    
    print(f"✅ API key found: {'*' * (len(api_key) - 4)}{api_key[-4:]}")
    
    # Test Case 1: Italian recommendations
    if candidates1:
        print("\n📋 LLM Test Case 1: Italian Restaurants")
        prefs1 = RetrievalPreferences(
            location="Indiranagar",
            budget_band="medium",
            cuisines=["Italian"],
            minimum_rating=4.2
        )
        
        try:
            result1 = generate_recommendations(prefs1, candidates1)
            if result1 and result1.recommendations:
                print(f"🎯 LLM recommended {len(result1.recommendations)} restaurants from {len(candidates1)} candidates:")
                for rec in result1.recommendations:
                    print(f"  #{rec.rank} {rec.restaurant_name}")
                    print(f"     {rec.reasoning}")
                    print()
            else:
                print("❌ LLM failed to generate recommendations for Test Case 1")
        except Exception as e:
            print(f"❌ LLM error for Test Case 1: {e}")
    
    # Test Case 2: North Indian recommendations
    if candidates2:
        print("\n📋 LLM Test Case 2: North Indian Restaurants")
        prefs2 = RetrievalPreferences(
            location="Bellandur",
            budget_band="high",
            cuisines=["North Indian"],
            minimum_rating=4.0
        )
        
        try:
            result2 = generate_recommendations(prefs2, candidates2)
            if result2 and result2.recommendations:
                print(f"🎯 LLM recommended {len(result2.recommendations)} restaurants from {len(candidates2)} candidates:")
                for rec in result2.recommendations:
                    print(f"  #{rec.rank} {rec.restaurant_name}")
                    print(f"     {rec.reasoning}")
                    print()
            else:
                print("❌ LLM failed to generate recommendations for Test Case 2")
        except Exception as e:
            print(f"❌ LLM error for Test Case 2: {e}")

def main():
    """Main test function"""
    print("🧪 Testing LLM Filtering and Recommendations")
    print("=" * 60)
    
    # Test filtering
    candidates1, candidates2 = test_filtering()
    
    # Test LLM recommendations
    test_llm_recommendations(candidates1, candidates2)
    
    print("\n✅ Test completed!")

if __name__ == "__main__":
    main()
