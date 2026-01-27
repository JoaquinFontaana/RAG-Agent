from langchain_google_genai import ChatGoogleGenerativeAI
from config.configuration import settings
from functools import lru_cache

@lru_cache()
def get_llm(temperature:float=0.5):
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=temperature,
        google_api_key=settings.google_api_key
    )

