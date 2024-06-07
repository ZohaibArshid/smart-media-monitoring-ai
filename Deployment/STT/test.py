from faster_whisper import WhisperModel
model_size = r"D:\Forbmax User Data\waqar sahi\smart-media-monitoring-ai\AI Models\whisper-large-v2-ct2"
model = WhisperModel(model_size, device="cuda", compute_type="float16")


def speech_to_text(audio_file_path):
    try:
        # Transcribe the extracted audio
        segments, info = model.transcribe(audio_file_path, beam_size=1, language='ur')
        full_text_urdu = " ".join(segment.text for segment in segments)
        segments, info  = model.transcribe(audio_file_path, beam_size=1, language='ur', task="translate")
        full_text_english = " ".join(segment.text for segment in segments)
        return {"urdu_full_text":full_text_urdu,"english_full_text":full_text_english}
    except Exception as e:
        return {"error": f"Transcription error: {str(e)}"}
    
# audio_file_path=r"D:\a.mp4"
# print(process_video(audio_file_path))