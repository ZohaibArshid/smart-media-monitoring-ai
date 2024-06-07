# from fastapi.security.api_key import APIKeyHeader
# import concurrent.futures
# import asyncio
# from fastapi import FastAPI, Form,UploadFile
from datetime import datetime
import requests
from datetime import date
from channel_logo import *
import re
from English_Summary.test import summarize_text as english_summarize_text
from Urdu_Summary.test import summarize as urdu_summarize_text
from Title.test import title_generation 
from Sentiment.test import sentiment_analysis 
from thumbnail.test import save_video_thumbnail 
from STT.test import speech_to_text
# app = FastAPI()

# user_api_keys = {
#     "user1": "apikey1",
#     "user2": "apikey2",
#     # Add more users and their API keys as needed
# }

# Replace with the URL where your FastAPI server is running
# speech_url = "http://192.168.18.83:1003"
base_url = "http://192.168.18.83"
speech_port = 1009
summary_port = 1002
sentiment_port = 1004
title_port = 1008

speech_url = f"{base_url}:{speech_port}"
summary_url = f"{base_url}:{summary_port}"
sentiment_url = f"{base_url}:{sentiment_port}"
title_url = f"{base_url}:{title_port}"

# Replace with your API key
api_key = "apikey1"
headers = {'api_key': api_key}  # Include the API key in the header
def transcribe_video(file_path):
    try:
        with open(file_path, 'rb') as video_file:
            files = {'video_file': video_file}
            response = requests.post(f"{speech_url}/transcribe_video/", files=files, headers=headers)

        if response.status_code == 200:
            # print("Responce")
            # print(response)
            result = response.json()
            # print(result)
           
            # full_text = result.get("full_text")
            # print("Transcription:")
            # print(full_text)
            return result
        else:
            print("Error:", response.text)
    except Exception as e:
        print("Error:", str(e))

def Sentiment_Analysis(text_input):
    try:
        params = {"text": text_input}
        response = requests.post(f"{sentiment_url}/sentiment/",  params=params, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            print("Error:", response.text)
    except Exception as e:
        print("Error:", str(e))
        
def Summary_generation(file_path):
    try:
        # print(file_path)
        with open(file_path, 'r', encoding='utf-8') as file:
            text_input = file.read()
        params = {"text": text_input}
        response = requests.post(f"{summary_url}/SummaryGeneration/", params=params, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return (result)

        else:
            print("Error:", response.text)
    except Exception as e:
        print("Error:", str(e))



def Title_request(text_input):
    try:
        params = {"text": text_input}
        response = requests.post(f"{title_url}/TopicGeneration/",  params=params, headers=headers)
        # print("title responce:". response)
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            print("Error:", response.text)
    except Exception as e:
        print("Error:", str(e))
    
def process_video(channel_name,start_time,end_time,video_path,news_type,program_name,host_name,guest_name,remarks,duration,video_date):
    try:
        print(video_path)
        full_text=speech_to_text(video_path)
        # full_text=full_text[0]
        # print(full_text)
        full_text_urdu=full_text['urdu_full_text']
        full_text_english=full_text['english_full_text']
        urdu_summary=urdu_summarize_text(full_text_urdu)
        # print("sentiment in progess")
        sentiment=sentiment_analysis(urdu_summary)
        # print("sentiment:",sentiment)
        topic=title_generation(full_text_english)
        english_summary=english_summarize_text(full_text_english)
        # print("topic is: ", topic)
        # Parse the start and end times into datetime objects
    # # Convert the start and end times to datetime objects
    #     start_datetime = datetime.strptime(start_time, "%H:%M:%S")
    #     end_datetime = datetime.strptime(end_time, "%H:%M:%S")

    #     # Calculate the duration as a timedelta
    #     duration = end_datetime - start_datetime

    #     # Extract hours, minutes, and seconds from the duration
    #     duration_hours = duration.seconds // 3600
    #     duration_minutes = (duration.seconds // 60) % 60
    #     duration_seconds = duration.seconds % 60

    #     # Format the duration as "HH:MM:SS"
    #     duration = f"{duration_hours:02d}:{duration_minutes:02d}:{duration_seconds:02d}"

        # Calculate the duration
        # print("return values ")
        return {
            "topic":topic,
            "full_text" :full_text_urdu,
            "summary":urdu_summary,
            "sentiment":sentiment,
            "translation":full_text_english,
            "start_time": start_time,
            "end_time": end_time,
            "duration":duration,
            "channel_name": channel_name,
            "news_type": news_type,
            "video_link":video_path,
            "program_name":program_name,
            "host_name":host_name,
            "guest_name":guest_name,
            "remarks":remarks,
            "ChannelLogo" :get_channel_logo_path(channel_name),   # Add the new columns
            "VideoThumbnail": save_video_thumbnail(video_path), 
            "Date": video_date,
            "Translation_Summary":english_summary,  
        }
    except Exception as e:
        return {"error": str(e)}

# # Define the API route to accept input parameters and return them
# @app.post("/process_data/")
# async def process_data_endpoint(
#     channel_name: str = Form(...),
#     start_time: str = Form(...),
#     end_time: str = Form(...),
#     video_file: str = Form(...),
#     news_type: str = Form(...),
#     program_name: str = Form(None),  # Make it optional
#     host_name: str = Form(None),  # Make it optional
#     guest_name: str = Form(None),  # Make it optional
#     remarks: str = Form(None),  # Make it optional
# ):

#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         result = await asyncio.get_event_loop().run_in_executor(
#             executor,
#             lambda: process_video(channel_name,start_time,end_time,video_file,news_type,program_name,host_name,guest_name,remarks)
#         )
#     return result
    


# if __name__ == "__main__":
    # import uvicorn

    # Run the FastAPI app on port 1000
    # uvicorn.run(app, host="0.0.0.0", port=1000, reload=True)
# uvicorn app:app --host 0.0.0.0 --port 1000 --reload
    # channel_name = "CNN"
    # start_time = "08:00:00"
    # end_time = "08:30:00"
    # video_path = r"C:\Users\waqar\Downloads\Video\a.mp4"  # Replace with the actual video file path
    # news_type = "Breaking News"
    # program_name = "News Hour"
    # host_name = "John Doe"
    # guest_name = "Jane Smith"
    # remarks = "Important news"

    # print(process_video(channel_name,start_time,end_time,video_path,news_type,program_name,host_name,guest_name,remarks))