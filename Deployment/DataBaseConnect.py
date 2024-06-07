import mysql.connector
import random
import string
from datetime import datetime, timedelta

# MySQL database connection parameters
# db_params = {
#     "host": "127.0.0.1",
#     "port": 3306,
#     "user": "root",
#     "password": "pakistan009",
# }
db_params = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "admin",
    # "password": "CPU@23",
}

# Database name to create/check
database_name = "ReportGenerate"

def create_database(cursor, database_name):
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"Database '{database_name}' created or already exists.")
    except mysql.connector.Error as e:
        print(f"Error creating database: {e}")

def table_exists(cursor, table_name):
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    return cursor.fetchone() is not None

def create_data_table(cursor):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS data (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        Topic VARCHAR(255) NOT NULL,
        Full_Text TEXT NOT NULL,
        Summary TEXT,
        Sentiment VARCHAR(50),
        Translation TEXT,
        StartTime TIME,
        EndTime TIME,
        Duration TIME,
        ChannelName VARCHAR(255),
        News_Type VARCHAR(255),
        VideoLink VARCHAR(255),
        ProgramName VARCHAR(255),
        Hostname VARCHAR(255),
        GuestsName VARCHAR(255),
        Remarks TEXT,
        ChannelLogo VARCHAR(255),   # Add the new columns
        VideoThumbnail VARCHAR(255), # Add the new columns
        Date DATE,
        Translation_Summary TEXT 
    )
    """
    
    try:
        cursor.execute(create_table_query)
        print("Table 'data' created or already exists.")
    except mysql.connector.Error as e:
        print(f"Error creating table: {e}")
# Function to generate random data
def generate_random_data():
    topic = ''.join(random.choices(string.ascii_letters, k=10))
    full_text = ''.join(random.choices(string.ascii_letters + string.digits, k=100))
    summary = ''.join(random.choices(string.ascii_letters + string.digits, k=50))
    sentiment = random.choice(["Positive", "Neutral", "Negative"])
    translation = ''.join(random.choices(string.ascii_letters + string.digits, k=50))
    start_time = datetime.now() - timedelta(days=random.randint(1, 365))
    end_time = start_time + timedelta(hours=random.randint(1, 24))
    duration = round(random.uniform(0.5, 2.5), 2)
    channel_name = random.choice(["Geo News", "Sama", "Ary", "Bol", "92 News"])
    news_type = random.choice(["Headline", "Bulletin News", "Breaking News", "Talkshow"])
    # Generating Urdu text for full text
    full_text_urdu = ''.join(random.choices(string.ascii_letters + ' اب پ بت ت ثج چ ح خ د ڈ س ش ف گ ہ ھ ج ک ل م ن ں ء و چ ے ی کے ',
                                            k=100))
    # Generating English translation for translation
    translation_english = ''.join(random.choices(string.ascii_letters + string.digits, k=50))
    
    program_name = ""
    hostname = ""
    guests_name = ""
    remarks = ""
    
    if news_type == "Talkshow":
        program_name = ''.join(random.choices(string.ascii_letters, k=10))
        hostname = ''.join(random.choices(string.ascii_letters, k=10))
        guests_name = ''.join(random.choices(string.ascii_letters, k=10))
        remarks = ''.join(random.choices(string.ascii_letters + string.digits, k=50))
    
    return (
        topic, full_text_urdu, summary, sentiment, translation_english, start_time, end_time,
        duration, channel_name, news_type, "https://example.com", program_name, hostname, guests_name, remarks
    )


