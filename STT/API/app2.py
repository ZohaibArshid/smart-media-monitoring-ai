from fastapi import FastAPI
from faster_whisper import WhisperModel
import moviepy.editor as mp
app = FastAPI()
model_size = "large-v2"
# Initialize the WhisperModel (load the model)
model = WhisperModel(model_size, device="cuda", compute_type="float16")

@app.get("/transcribe_video/")
async def transcribe_audio(video_path: str):
    try:
        # print(video_path)
        # Load the MP4 video
        video_clip = mp.VideoFileClip(video_path)

        # Extract the audio
        audio_clip = video_clip.audio

        # Specify the output audio file name and format (e.g., WAV)
        audio_file = "audio.wav"

        # Save the extracted audio as a separate audio file
        audio_clip.write_audiofile(audio_file)

        # Close the audio clip
        audio_clip.close()
        # Transcribe the audio
        segments, info = model.transcribe(audio_file, beam_size=1, language='ur')
        full_text = " ".join(segment.text for segment in segments)
        # # Record the end time
        # end_time = time.time()

        # # Calculate and print the execution time
        # execution_time = end_time - start_time

        # transcribed_data = {
        #     "detected_language": info.language,
        #     "language_probability": info.language_probability,
        #     "execution_time_seconds": execution_time,
        #     "transcription_segments": [{"start": segment.start, "end": segment.end, "text": segment.text} for segment in segments]
        # }

        return full_text

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=1000)
