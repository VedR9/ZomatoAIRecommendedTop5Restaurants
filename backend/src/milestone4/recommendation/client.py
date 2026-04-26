from openai import OpenAI
from milestone0.app.config import get_settings

GROQ_BASE_URL = "https://api.groq.com/openai/v1"

def get_client() -> OpenAI:
    settings = get_settings()
    api_key = settings.groq_api_key or settings.llm_api_key
    if not api_key:
        raise ValueError("API key not configured. Set GROQ_API_KEY in your environment.")
    return OpenAI(api_key=api_key, base_url=GROQ_BASE_URL)
