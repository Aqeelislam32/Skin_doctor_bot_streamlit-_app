import os
from gtts import gTTS


def text_to_speech(text: str, out_path: str = "uploads/response.mp3", lang: str = "en") -> str:
    """Convert the AI's text response into an mp3 voice file using gTTS (free)."""
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    tts = gTTS(text=text, lang=lang)
    tts.save(out_path)
    return out_path
