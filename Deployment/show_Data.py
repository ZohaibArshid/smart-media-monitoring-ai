import mysql.connector
from tabulate import tabulate  # Import the tabulate library

# MySQL database connection parameters
db_params = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "CPU@23",
    "database": "ReportGenerate",
}

try:
    connection = mysql.connector.connect(**db_params)
    cursor = connection.cursor()

    # Select all data from the "data" table
    select_query = "SELECT * FROM data"
    cursor.execute(select_query)

    # Fetch all the rows of data
    all_data = cursor.fetchall()

    # Format the data as a table and print it to the console
    table = tabulate(all_data, headers=cursor.column_names, tablefmt="pretty")
    # table = tabulate(all_data, headers=cursor.column_names, tablefmt="grid")
    # custom_headers = ["Topic", "Full Text", "Summary", "Sentiment", "Translation", "Start Time", "End Time", "Duration", "Channel Name", "News Type", "Video Link", "Program Name", "Host Name", "Guests Name", "Remarks"]
    # table = tabulate(all_data, headers=custom_headers, tablefmt="pretty")


    print(table)

except mysql.connector.Error as e:
    print(f"Error: {e}")

finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()
