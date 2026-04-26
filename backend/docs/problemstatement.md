# Problem Statement: AI-Powered Restaurant Recommendation System

## Overview
Build an AI-powered restaurant recommendation service inspired by Zomato. The system should combine structured restaurant data with an LLM to produce personalized, trustworthy recommendations based on user preferences.

## Goal
Design and implement an application that:
- Accepts user preferences such as location, budget, cuisine, and minimum rating
- Uses a real-world restaurant dataset
- Generates ranked recommendations with clear reasoning using an LLM
- Presents results in a user-friendly format

## Data Source
Use the Hugging Face dataset:
- `ManikaSaini/zomato-restaurant-recommendation`
- URL: https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation

From this dataset, extract and normalize key fields such as:
- Restaurant name
- Location
- Cuisine(s)
- Estimated cost
- Rating

## Functional Requirements

### 1) User Input
Collect the following preferences:
- Location (e.g., Delhi, Bangalore)
- Budget (low, medium, high)
- Preferred cuisine(s) (e.g., Italian, Chinese)
- Minimum acceptable rating
- Optional free-text preferences (e.g., family-friendly, quick service)

### 2) Candidate Retrieval
- Filter restaurants deterministically using user preferences
- Keep only relevant candidates for downstream LLM ranking
- Handle no-match scenarios gracefully

### 3) LLM-Based Recommendation
- Provide the filtered candidates and user preferences to an LLM
- Ask the model to rank suitable options
- Require concise explanations for why each recommendation fits
- Ensure recommendations are grounded in the candidate list

### 4) Output Display
Show top recommendations with:
- Restaurant name
- Cuisine
- Rating
- Estimated cost
- AI-generated explanation

## Expected User Experience
- Input preferences in a simple interface
- Receive high-quality, readable recommendations
- Understand why each option is suggested
- See helpful feedback when no suitable restaurants are found

## Non-Goals (for v1)
- User accounts and personalization history
- Live third-party restaurant APIs
- Map integration and real-time availability

## Success Criteria
The project is successful when a user can:
1. Enter preferences
2. Receive grounded, relevant recommendations
3. See clear ranking rationale for each recommendation
4. Complete the flow end-to-end in a single run
