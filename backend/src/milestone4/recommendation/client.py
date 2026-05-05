from google import genai
from milestone0.app.config import get_settings

def get_client() -> genai.Client:
    settings = get_settings()
    # Try GEMINI_API_KEY first, then fallback to LLM_API_KEY
    api_key = settings.gemini_api_key or settings.llm_api_key
    if not api_key:
        raise ValueError("Gemini API Key is not configured. Please set GEMINI_API_KEY in your environment.")
    
    return genai.Client(api_key=api_key)
