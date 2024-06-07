
from fastapi import FastAPI, UploadFile, Form, Depends, HTTPException, Header
from fastapi.security.api_key import APIKeyHeader
from faster_whisper import WhisperModel
import moviepy.editor as mp
import os
import concurrent.futures
import asyncio
from fastapi.responses import FileResponse
app = FastAPI()
model_size = r"D:\Forbmax User Data\waqar sahi\smart-media-monitoring-ai\AI Models\whisper-large-v2-ct2"
model = WhisperModel(model_size, device="cuda", compute_type="float16")

# Define a directory to store uploaded videos and audio
upload_dir = "audio_uploads"
os.makedirs(upload_dir, exist_ok=True)
# Define a list of allowed audio file formats (extensions)
# allowed_formats = ["mp3", "wav", "aac", "flac", "ogg", "aiff", "m4a", "wma", "ogg", "opus", "ac3", "mid", "midi"]

# def is_allowed_format(file_name):
#     # Check if the file format is in the list of allowed formats
#     file_format = file_name.split(".")[-1]
#     return file_format in allowed_formats

def process_audio(audio_file: UploadFile,language: str):
    try:
        # print("check audio name")
        # print(audio_file.filename)
        # print("audio name don")
        # if not is_allowed_format(audio_file.filename):
        #     raise HTTPException(status_code=400, detail="Unsupported file format")

        # Read the uploaded audio file into memory
        audio_content = audio_file.file.read()
        audio_name = os.path.splitext(audio_file.filename)[0]
        print(audio_name)
        # Create a folder for the audio inside the "uploads" directory
        # audio_folder = os.path.join(upload_dir, audio_name)
        # os.makedirs(audio_folder, exist_ok=True)

        # Save the uploaded audio in the audio folder
        audio_file_path = os.path.join(upload_dir, f"{audio_name}.mp3")
        with open(audio_file_path, "wb") as temp_audio_file:
            temp_audio_file.write(audio_content)

        # language = language.lower()  # Make sure it's in lowercase

        # # Perform transcription based on the language
        # if language == "english":
        #     lang='eng'
        # print("transcription start")
        try:
            # Transcribe the extracted audio
            segments, info = model.transcribe(audio_file_path, beam_size=1)
            
            # full_text = " ".join(segment.text for segment in segments)
            # for segment in segments:
            #     print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
            # print("generating srt file")
            srt_content = ""
            i=1
            for segment in segments:
                # print("loop")
                start_time = segment.start
                end_time = segment.end
                text = segment.text

                # Convert start and end times to the SRT format
                start_time_str = f"{int(start_time // 3600):02d}:{int((start_time % 3600) // 60):02d}:{start_time % 60:06.3f}"
                end_time_str = f"{int(end_time // 3600):02d}:{int((end_time % 3600) // 60):02d}:{end_time % 60:06.3f}"

                srt_content += f"{i}\n"
                srt_content += f"{start_time_str} --> {end_time_str}\n"
                srt_content += f"{text}\n\n"
                i=i+1
            # print("srt data ready")
            # print(srt_content)
            # Save the SRT content to a file
            srt_file_path=os.path.join(upload_dir, f"{audio_name}.srt")
            with open(srt_file_path, "w", encoding="utf-8") as srt_file:
                srt_file.write(srt_content)

        except Exception as e:
            return {"error": f"Transcription error: {str(e)}"}

        try:
            os.remove(audio_file_path)
        except Exception as e:
            return {"error": f"File delete error: {str(e)}"}

        # response=FileResponse(f"{video_folder}.zip", filename=f'{video_name}.zip')
        # os.remove(f"{video_folder}.zip")
        # return response
        # Return the SRT file as a response
        # response = FileResponse(srt_file_path, media_type="application/x-subrip")
        response=FileResponse(srt_file_path, filename=f'{audio_name}.srt')
        return response
    except Exception as e:
        return {"error": str(e)}
@app.post("/v1/audio/transcriptions")
async def transcribe_audio(
    file: UploadFile = Form(...),
    language: str = Form(...),
):
    # Create a new thread for processing each user's video
    with concurrent.futures.ThreadPoolExecutor() as executor:
        result = await asyncio.get_event_loop().run_in_executor(
            executor,
            lambda: process_audio(file,language)
        )
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1006,reload=True)
    
# run command in cmd 
# uvicorn actus_api:app --host 0.0.0.0 --port 1005 --reload
# "testing"
# curl http://192.168.18.83:1006/v1/audio/transcriptions -H "Content-Type: multipart/form-data" -F "file=@D:\shehbaz.wav" -F "language=English"