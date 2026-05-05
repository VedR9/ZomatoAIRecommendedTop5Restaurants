import os
from google import genai

def get_client() -> genai.Client:
    # Read directly from os.environ to avoid lru_cache stale-settings issue on Streamlit
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("LLM_API_KEY")
    if not api_key:
        raise ValueError("Gemini API Key is not configured. Please set GEMINI_API_KEY in your environment.")

    return genai.Client(api_key=api_key)
