import psycopg2
from main import main_function
import time
import os 
def process_new_record(new_record):
    try:
        # Call the main function from main.py with the new record as an argument
        # print("Processing new record:", new_record)
        # new_record
        channel_name = new_record[1]
        start_time = new_record[2]
        end_time = new_record[3]
        video_path = new_record[4]
        news_type = new_record[6]
        # program_name = "News Hour",
        # host_name = "John Doe",
        # guest_name = "Jane Smith",
        # remarks = "Important news"
        duration=new_record[5]
        video_date=new_record[7]
        if os.path.exists(video_path):
            main_function(channel_name = channel_name,start_time =start_time,end_time = end_time,video_path = video_path,news_type =news_type,
            program_name = "News Hour",
            host_name = "John Doe",
            guest_name = "Jane Smith",
            remarks = "Important news",
            duration=duration,
            video_date=video_date)
        else:
            print(video_path," not exist")
        
    except Exception as e:
        print("Error while processing new record:", e)

def fetch_last_record_id(cursor):
    try:
        # Fetch the last available ID in the database
        cursor.execute("SELECT max(id) FROM news_videos;")
        last_record_id = cursor.fetchone()[0]
        return last_record_id
    except Exception as e:
        print("Error while fetching last record ID:", e)
        return None

def fetch_new_record(cursor, last_record_id):
    try:
        if last_record_id is None:
            # If this is the first run, fetch the last record
            cursor.execute("SELECT * FROM news_videos WHERE id = (SELECT max(id) FROM news_videos);")
        else:
            # Fetch the next record with an ID greater than the last processed record
            cursor.execute("SELECT * FROM news_videos WHERE id > %s ORDER BY id LIMIT 1;", (last_record_id,))
        
        new_record = cursor.fetchone()
        return new_record
    except Exception as e:
        print("Error while fetching new record:", e)
        return None

try:
    # Establish a connection to the PostgreSQL database
    db_conn = psycopg2.connect(
        user="postgres",
        password="ticker1234",
        host="localhost",
        port="5432",
        database="News_Videos"
    )
    print("Connected to the PostgreSQL database")

    # Create a cursor to interact with the database
    cursor = db_conn.cursor()
    print("Cursor created")

    last_record_id = None  # Initialize the last_record_id to None

    while True:
        new_record = fetch_new_record(cursor, last_record_id)

        if new_record:
            record_id = new_record[0]
            print(record_id)
            process_new_record(new_record)
            last_record_id = record_id  # Update the last_record_id

        # Sleep for a few seconds before checking for changes again
        # time.sleep(60)  # Adjust the interval as needed

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL:", error)
finally:
    cursor.close()
    db_conn.close()