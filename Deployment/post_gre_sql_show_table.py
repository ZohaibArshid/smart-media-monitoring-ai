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

    # Execute a query to fetch data from the "news_videos" table
    cursor.execute("SELECT * FROM news_videos;")
    records = cursor.fetchall()

    # Get the column names from the cursor's description
    column_names = [desc[0] for desc in cursor.description]

    # Print column names
    print("Column Names:", column_names)

    # Print the data
    for record in records:
        for i, column_name in enumerate(column_names):
            print(f"{column_name}: {record[i]}")
        print()

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL:", error)
finally:
    cursor.close()
    db_conn.close()
