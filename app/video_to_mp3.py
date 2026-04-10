import ffmpeg

def convert_video_to_audio(video_path, audio_path):
    try:
        (
            ffmpeg
            .input(video_path)
            .output(audio_path)
            .run(overwrite_output=True, quiet=True)
        )
        return audio_path
    except Exception as e:
        print(f"FFmpeg error: {e}")
        return None