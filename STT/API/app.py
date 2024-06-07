from fastapi import FastAPI, UploadFile, Depends, HTTPException, Header
from fastapi.security.api_key import APIKeyHeader
from faster_whisper import WhisperModel
import moviepy.editor as mp
import os
import concurrent.futures
import asyncio
import zipfile
import shutil
from pydub import AudioSegment
from fastapi.responses import FileResponse
import datetime
                
def zip_folder(relative_folder_path):
    # Define the output zip file name based on the relative path
    output_zip_path = f"{os.path.basename(relative_folder_path)}.zip"

    with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(relative_folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, relative_folder_path)
                zipf.write(file_path, arcname)

app = FastAPI()
model_size = r"D:\Forbmax User Data\waqar sahi\smart-media-monitoring-ai\AI Models\whisper-large-v2-ct2"
model = WhisperModel(model_size, device="cuda", compute_type="float16")

# Define a directory to store uploaded videos
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
def process_video(video_file: UploadFile):
    try:
        # Read the uploaded video file into memory
        video_content = video_file.file.read()
        video_name = os.path.splitext(video_file.filename)[0]

        # Create a folder for the video inside the "uploads" directory
        video_folder = os.path.join(upload_dir, video_name)
        os.makedirs(video_folder, exist_ok=True)

        # Save the uploaded video in the video folder
        video_file_path = os.path.join(video_folder, f"{video_name}.mp4")
        with open(video_file_path, "wb") as temp_video_file:
            temp_video_file.write(video_content)

        # Use moviepy to process the saved video file
        video_clip = mp.VideoFileClip(video_file_path)

        # Extract audio from the video in memory
        audio_clip = video_clip.audio

        # Save the audio clip in the same directory as the video
        audio_file_path = os.path.join(video_folder, f"{video_name}.mp3")
        audio_clip.write_audiofile(audio_file_path)

        try:
            # Transcribe the extracted audio
            segments, info = model.transcribe(audio_file_path, beam_size=1, language='ur')
        except Exception as e:
            return {"error": f"Transcription error: {str(e)}"}
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")[:-3]


        # Process and save each segment along with the corresponding text file
        # results = []
        for i, segment in enumerate(segments):
             # Generate a unique video name based on the current timestamp
            # print(segment)
            segment_name = f"{timestamp}_{i}"
            wav_file_path = os.path.join(video_folder, f"{segment_name}.wav")
            txt_file_path = os.path.join(video_folder, f"{segment_name}.txt")
            
              # Save the transcribed text as a TXT file
            with open(txt_file_path, "w",encoding="utf-8") as text_file:
                text_file.write(segment.text)
                # Use FFmpeg command to extract the audio segment
                # Save the audio segment as a separate audio file
            audio_segment = AudioSegment.from_mp3(audio_file_path)
            audio_segment = audio_segment[segment.start * 1000:segment.end * 1000]  # Extract the segment
            audio_segment.export(wav_file_path, format="wav")

        try:
            # Remove the uploaded video and audio files
            video_clip.close()
            # Close the audio clip
            audio_clip.close()
            os.remove(audio_file_path)
            os.remove(video_file_path)
            # print(video_folder)
            zip_folder(os.path.join(upload_dir, video_name))
            shutil.rmtree(video_folder)
        except Exception as e:
            return {"error": f"File delete error: {str(e)}"}

        
        # return {"results": "done"}
        # Send the zip file as a response
        response=FileResponse(f"{video_name}.zip", filename=f'{video_name}.zip')
        # os.remove(f"{video_name}.zip")
        return response
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
    uvicorn.run(app, host="0.0.0.0", port=2000, reload=True)
# uvicorn app:app --host 0.0.0.0 --port 2000 --reload