import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

CHAT_SYSTEM_PROMPT = """
You are a friendly AI health-information assistant (not a licensed doctor).
Answer general follow-up questions cautiously, avoid definitive diagnoses,
and encourage seeing a real doctor for anything serious or persistent.
"""


def ask_followup(question: str, context: str = "") -> str:
    """
    Handle text-only follow-up questions after the initial image analysis,
    e.g. 'what cream should I avoid?' or 'is this contagious?'.
    """
    prompt = f"{CHAT_SYSTEM_PROMPT}\n\nEarlier context: {context}\n\nPatient's question: {question}"
    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=[prompt],
    )
    return response.text
