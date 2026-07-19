import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def transcribe_audio(audio_path: str) -> str:
    """
    Convert a recorded voice message into text using Groq's hosted Whisper model.
    audio_path: local path to the recorded audio file (wav/mp3/m4a etc.)
    """
    with open(audio_path, "rb") as f:
        transcription = client.audio.transcriptions.create(
            file=f,
            model="whisper-large-v3-turbo",
            response_format="text",
            # language="ur"  # uncomment and set if you want to force a language
        )
    # response_format="text" already returns a plain string
    return transcription.strip() if isinstance(transcription, str) else str(transcription)
