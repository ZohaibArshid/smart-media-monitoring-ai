
from fastapi import FastAPI, UploadFile, Depends, HTTPException, Header
from fastapi.security.api_key import APIKeyHeader
from faster_whisper import WhisperModel
import moviepy.editor as mp
import os
import concurrent.futures
import asyncio

app = FastAPI()
model_size = r"D:\Forbmax User Data\waqar sahi\smart-media-monitoring-ai\AI Models\whisper-large-v2-ct2"
model = WhisperModel(model_size, device="cuda", compute_type="float16")

# Define a directory to store uploaded videos and audio
upload_dir = "uploads"
os.makedirs(upload_dir, exist_ok=True)


# Define a list of valid API keys (replace with your actual API keys)
# VALID_API_KEYS = ["forbmaxspeechmodeluser1", "forbmaxspeechmodeluser2"]
# Create a dictionary that maps users to their API keys
user_api_keys = {
    "user1": "apikey1",
    "user2": "apikey2",
    # Add more users and their API keys as needed
}
# from mtranslate import translate

# def translate_urdu_to_english(urdu_text):
#     try:
#         english_translation = translate(urdu_text, "en", "ur")
#         return english_translation
#     except Exception as e:
#         return str(e)
def process_video(video_file: UploadFile):
    try:
        # Read the uploaded video file into memory
        video_content = video_file.file.read()

        # Create a temporary file to save the uploaded video
        video_file_path = os.path.join(upload_dir, video_file.filename)
        with open(video_file_path, "wb") as temp_video_file:
            temp_video_file.write(video_content)

        # Use moviepy to process the saved video file
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
            full_text_urdu = " ".join(segment.text for segment in segments)
            segments, info  = model.transcribe(audio_file_path, beam_size=1, language='ur', task="translate")
            full_text_english = " ".join(segment.text for segment in segments)
        except Exception as e:
            return {"error": f"Transcription error: {str(e)}"}

        try:
            # Remove the uploaded video and audio files
            video_clip.close()
            os.remove(audio_file_path)
            os.remove(video_file_path)
        except Exception as e:
            return {"error": f"File delete error: {str(e)}"}

        return {"urdu_full_text":full_text_urdu,"english_full_text":full_text_english}
        # return {full_text_urdu}
    except Exception as e:
        return {"error": str(e)}
# Dependency to validate the API key
async def get_api_key(api_key: str = Header(None, convert_underscores=False)):
    if api_key not in user_api_keys.values():
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key
@app.post("/transcribe_video/")
async def transcribe_video_endpoint(
    video_file: UploadFile,
    api_key: str = Depends(get_api_key),  # Require API key for this route
):
    # Create a new thread for processing each user's video
    with concurrent.futures.ThreadPoolExecutor() as executor:
        result = await asyncio.get_event_loop().run_in_executor(
            executor,
            lambda: process_video(video_file)
        )
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1009,reload=True)
    
# run command in cmd 
# uvicorn finalll_api:app --host 0.0.0.0 --port 1009 --reload