import os
from google import genai
from PIL import Image

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

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
- Structure the answer with: possible explanation(s), self-care tips (if safe),
  and a clear "see a doctor if..." section.
"""


def analyze_skin(image_path: str | None, patient_text: str) -> str:
    """
    Send a skin image + the patient's description to Gemini 2.5 Flash
    for a cautious, non-diagnostic explanation.
    If image_path is None, text-only analysis is performed.
    """
    contents = [
        SYSTEM_PROMPT,
        f"Patient's description of the problem: {patient_text}",
    ]
    if image_path is not None:
        image = Image.open(image_path)
        contents.append(image)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
    )
    return response.text
