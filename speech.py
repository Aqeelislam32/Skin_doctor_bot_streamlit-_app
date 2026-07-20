import os
from groq import Groq


def transcribe_audio(audio_path):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY not found.")

    client = Groq(api_key=api_key)

    with open(audio_path, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(audio_path, file.read()),
            model="whisper-large-v3"
        )

    return transcription.text
