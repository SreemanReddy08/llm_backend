from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_audio(audio_path):
    try:
        with open(audio_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",   # you can also use gpt-4o-transcribe
                file=audio_file
            )
        return transcription.text   # ✅ return only text
    except Exception as e:
        print(f"Transcription error: {e}")
        return None