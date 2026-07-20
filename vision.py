import os
from google import genai
from PIL import Image

SYSTEM_PROMPT = """
You are an AI assistant that helps describe possible skin conditions
based on an uploaded image and the patient's description of symptoms.

IMPORTANT RULES:
- You are NOT a licensed doctor and must NEVER give a definitive diagnosis.
- Always use cautious, informational language ("this may look like...",
  "could be consistent with...", "one possibility is...").
- Always recommend seeing a real dermatologist/doctor for confirmation and treatment.
- If the image or description suggests something urgent (rapid growth, bleeding,
  spreading redness, fever, signs of infection), clearly tell the user to seek
  medical care promptly, ideally same-day.
- Keep the response clear, empathetic, and easy to understand for a non-medical person.
- Reply in the same language the patient used, where possible.
- Structure the answer with:
  1. Possible explanation(s)
  2. Self-care tips (if safe)
  3. See a doctor if...
"""


def analyze_skin(image_path: str | None, patient_text: str) -> str:
    """
    Analyze skin image and patient description using Gemini.
    """

    # Read API key after user enters it in the sidebar
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "Gemini API key not found. Please enter your API key in the sidebar."
        )

    # Create client only when function is called
    client = genai.Client(api_key=api_key)

    contents = [
        SYSTEM_PROMPT,
        f"Patient's description of the problem: {patient_text}",
    ]

    if image_path:
        image = Image.open(image_path)
        contents.append(image)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
    )

    return response.text
