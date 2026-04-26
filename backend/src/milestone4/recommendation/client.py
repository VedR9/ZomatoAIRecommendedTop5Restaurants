from google import genai
from milestone0.app.config import get_settings

def get_client() -> genai.Client:
    settings = get_settings()
    if not settings.llm_api_key:
        raise ValueError("LLM API Key is not configured. Please set LLM_API_KEY in your environment.")
    
    return genai.Client(api_key=settings.llm_api_key)
