import psycopg2

try:
    # Establish a connection to the PostgreSQL database
    db_conn = psycopg2.connect(
        user="postgres",
        password="ticker1234",
        host="localhost",  # Replace with your actual database host
        port="5432",
        database="News_Videos"
    )
    print("Connected to the PostgreSQL database")

    # Create a cursor to interact with the database
    cursor = db_conn.cursor()
    print("Cursor created")

    # Clear data from the "news_videos" table
    cursor.execute("DELETE FROM news_videos;")

    # Commit the transaction to save the changes
    db_conn.commit()

    print("Data cleared from the 'news_videos' table.")

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL:", error)
finally:
    cursor.close()
    db_conn.close()
