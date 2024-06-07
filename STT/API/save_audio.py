from faster_whisper import WhisperModel
from pydub import AudioSegment

# Initialize the Whisper model
model = WhisperModel(r"D:\Forbmax User Data\waqar sahi\smart-media-monitoring-ai\AI Models\whisper-large-v2-ct2")

# Transcribe the audio file
segments, info = model.transcribe(r"STT\API\uploads\a\a.mp3")

# Specify the output directory for audio segments and text files
output_audio_directory = "audio_segments/"
output_text_directory = "text_segments/"

# Create the directories if they don't exist
import os
os.makedirs(output_audio_directory, exist_ok=True)
os.makedirs(output_text_directory, exist_ok=True)

# Loop through the segments and save them as audio and text files
for idx, segment in enumerate(segments):
    # Save the audio segment as a separate audio file
    audio_segment = AudioSegment.from_mp3(r"STT\API\uploads\a\a.mp3")
    audio_segment = audio_segment[segment.start * 1000:segment.end * 1000]  # Extract the segment
    audio_segment.export(os.path.join(output_audio_directory, f"segment_{idx}.mp3"), format="mp3")
    
    # Save the text segment to a text file
    with open(os.path.join(output_text_directory, f"segment_{idx}.txt"), "w") as text_file:
        text_file.write(segment.text)

# Print a message to confirm that the segments and text have been saved
print("Segments and text saved in separate files.")
