from fastapi import FastAPI, UploadFile
from faster_whisper import WhisperModel
import moviepy.editor as mp
import os

app = FastAPI()
model_size = "large-v2"
model = WhisperModel(model_size, device="cuda", compute_type="float16")

# Define a directory to store uploaded videos and audio
upload_dir = "uploads"
os.makedirs(upload_dir, exist_ok=True)

@app.post("/transcribe_video/")
async def transcribe_video(video_file: UploadFile):
    try:
        # Read the uploaded video file into memory
        video_content = await video_file.read()

        # Create a temporary file to save the uploaded video
        video_file_path = os.path.join(upload_dir, video_file.filename)
        with open(video_file_path, "wb") as temp_video_file:
            temp_video_file.write(video_content)
     
        video_clip = mp.VideoFileClip(video_file_path)
        # Extract audio from the video in memory
        audio_clip = video_clip.audio
        # Save the audio clip in the same directory as the video
        audio_file_path = os.path.join(upload_dir, f"{os.path.splitext(video_file.filename)[0]}.mp3")
        audio_clip.write_audiofile(audio_file_path)
        # Close the audio clip
        audio_clip.close()
        

        try:
            # Transcribe the extracted audio
            segments, info = model.transcribe(audio_file_path, beam_size=1, language='ur')
            full_text = " ".join(segment.text for segment in segments)
        except Exception as e:
            return {"error": f"Transcription error: {str(e)}"}

        try:
            # Remove the uploaded video and audio files
            video_clip.close()
            os.remove(audio_file_path)
            os.remove(video_file_path)
        except Exception as e:
            return {"error": f"file delete error: {str(e)}"}
        
        return {"full_text": full_text}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1000)
