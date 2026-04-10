from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil
import os
from fastapi.middleware.cors import CORSMiddleware

from app.video_to_mp3 import convert_video_to_audio
from app.audio_to_text import transcribe_audio
from app.llm_notes_gen import generate_notes

app = FastAPI()

# 👇 Add this CORS configuration 👇
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allows all headers
)
# 👆 End CORS configuration 👆


VIDEO_DIR = "app/data/videos"
os.makedirs(VIDEO_DIR, exist_ok=True)


# 1. Upload only
@app.post("/upload/")
async def upload_video(file: UploadFile = File(...)):
    try:
        video_path = os.path.join(VIDEO_DIR, file.filename)

        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "message": "Video uploaded successfully",
            "filename": file.filename
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload error: {str(e)}")


# 2. Process video
@app.post("/process/")
async def process_video(filename: str):

    video_path = os.path.join(VIDEO_DIR, filename)
    audio_path = video_path.replace(".mp4", ".mp3")

    try:
        # Check file exists
        if not os.path.exists(video_path):
            raise HTTPException(status_code=404, detail="File not found")

        # Convert video → audio
        convert_video_to_audio(video_path, audio_path)

        # Audio → text
        transcript = transcribe_audio(audio_path)
        if not transcript:
            raise HTTPException(status_code=500, detail="Transcription failed")

        # Text -> notes
        notes = generate_notes(transcript)
        if not notes:
            raise HTTPException(status_code=500, detail="Notes generation failed")

        return {
            "filename": filename,
            "transcript": transcript,
            "notes": notes
        }

    except HTTPException as e:
        raise e  # keep original error

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

    finally:
        # ✅ Always cleanup audio
        if os.path.exists(audio_path):
            os.remove(audio_path)
        if os.path.exists(video_path):
            os.remove(video_path)