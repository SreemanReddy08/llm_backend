from openai import OpenAI
from dotenv import load_dotenv
import os

# load env
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_notes(transcript):
    try:
        prompt = f"""
        You are an expert teacher.

        Convert this transcript into structured study notes.

        Requirements:
        - Add headings
        - Use bullet points
        - Keep it concise
        - Highlight key concepts
        - Add a short summary at the top
        - structure it for pdf type format 
        - define every concept with an example

        Transcript:
        {transcript}
        """

        response = client.chat.completions.create(
            model="gpt-5.4-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"Notes Generation error: {e}")
        return None