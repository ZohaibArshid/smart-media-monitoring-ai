from DataBaseConnect import *
from apis import *  
def main_function(channel_name = "geo",start_time = "08:00:00",end_time = "08:30:00",video_path = r"D:\b.mp4",news_type = "Breaking News",
    program_name = "News Hour",
    host_name = "John Doe",
    guest_name = "Jane Smith",
    remarks = "Important news",
    duration="",
    video_date="2023-10-12"):


    data_to_insert=process_video(channel_name,start_time,end_time,video_path,news_type,program_name,host_name,guest_name,remarks,duration,video_date)
    # print(data_to_insert)
    try:
        connection = mysql.connector.connect(**db_params)
        print("Connected to MySQL server")
        cursor = connection.cursor()

        create_database(cursor, database_name)

        cursor.execute(f"USE {database_name}")
        print("Using database:", database_name)

        create_data_table(cursor)
        

        # Update the INSERT INTO query to include the new columns
        insert_query = """
        INSERT INTO data (Topic, Full_Text, Summary, Sentiment, Translation, StartTime, EndTime, Duration, ChannelName, News_Type, VideoLink, ProgramName, Hostname, GuestsName, Remarks, ChannelLogo, VideoThumbnail, Date,Translation_Summary)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
        """

        print("Topic:", data_to_insert['topic'])
        # print("Full Text:", data_to_insert['full_text'])
        # print("Summary:", data_to_insert['summary'])
        print("Sentiment:", data_to_insert['sentiment'])
        print("Translation:", data_to_insert['translation'])
        print("Start Time:", data_to_insert['start_time'])
        print("End Time:", data_to_insert['end_time'])
        print("Duration:", data_to_insert['duration'])
        print("Channel Name:", data_to_insert['channel_name'])
        print("News Type:", data_to_insert['news_type'])
        print("Video Link:", data_to_insert['video_link'])
        print("Program Name:", data_to_insert['program_name'])
        print("Host Name:", data_to_insert['host_name'])
        print("Guest Name:", data_to_insert['guest_name'])
        print("Remarks:", data_to_insert['remarks'])
        print("channellogo:", data_to_insert['ChannelLogo'])
        print("video_thunmbnil:", data_to_insert['VideoThumbnail'])
        print("date:", data_to_insert['Date'])
        print("Translation_Summary", data_to_insert['Translation_Summary'])

        # Execute the query with data from the dictionary
        cursor.execute(insert_query, (
            data_to_insert['topic'],
            data_to_insert['full_text'],
            data_to_insert['summary'],
            data_to_insert['sentiment'],
            data_to_insert['translation'],
            data_to_insert['start_time'],
            data_to_insert['end_time'],
            data_to_insert['duration'],
            data_to_insert['channel_name'],
            data_to_insert['news_type'],
            data_to_insert['video_link'],
            data_to_insert['program_name'],
            data_to_insert['host_name'],
            data_to_insert['guest_name'],
            data_to_insert['remarks'],
            data_to_insert['ChannelLogo'],
            data_to_insert['VideoThumbnail'],
            data_to_insert['Date'],
            data_to_insert['Translation_Summary'],
        ))
        print("data insert into datase")
        # Commit the changes
        connection.commit()
    except mysql.connector.Error as e:
        print(f"Error: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# main_function()