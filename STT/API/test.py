import requests

# Replace with the URL where your FastAPI server is running
base_url = "http://192.168.18.83:1000"
# Replace with your API key
api_key = "apikey1"
def transcribe_video(file_path):
    try:
        with open(file_path, 'rb') as video_file:
            files = {'video_file': video_file}
            headers = {'api_key': api_key}  # Include the API key in the header
            response = requests.post(f"{base_url}/transcribe_video/", files=files, headers=headers)

        if response.status_code == 200:
            result = response.json()
            print(result)
           
            full_text = result.get("full_text")
            print("Transcription:")
            print(full_text)
        else:
            print("Error:", response.text)
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    video_path = r"D:\b.mp4"  # Replace with your video file path
    transcribe_video(video_path)
