import os
import subprocess

from pytube import YouTube


from pytube import YouTube
import youtube_dl

def download_video(url, output_path='downloads'):
    ydl_opts = {
        'format': 'best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Example usage
download_video("https://www.youtube.com/watch?v=WBmACnegCQU&ab_channel=shfashowIndia")


# def save_segment(video_path, audio_output_path, start, end):
#     ffmpeg_cmd = [
#     'ffmpeg',
#     '-y',            
#     '-i', video_path,   # Input video file
#     '-ss', str(start),
#     '-to' ,str(end),  # Start and End times of clip
#     '-vn',               # Disable video recording
#     '-acodec', 'libmp3lame',   # Use the same audio codec as the input
#     audio_output_path   # Output audio file
#     ]
#     subprocess.run(ffmpeg_cmd, check=True)
    
    
    
# start_time = 30 # Start time of the segment
# end_time = 60.5      # End time of the segment

# video_file_path=r"videoplayback.mp4"
# # Save the audio segment to a file
# audio_segment_file_name= os.path.join('uploads','audio_segments',"a.wav")
# save_segment(video_file_path, audio_segment_file_name, start_time, end_time)