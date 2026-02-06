from agno.models.google import Gemini
import os


def get_llm():
    return Gemini(
        id="gemini-2.5-flash-lite-preview-09-2025",
        api_key=os.getenv("GOOGLE_API_KEY"),
    )
