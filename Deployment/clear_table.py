import mysql.connector

# MySQL database connection parameters
db_params = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "CPU@23",
    "database": "ReportGenerate",
}

table_name = "data"  # Specify the name of the table you want to delete

try:
    connection = mysql.connector.connect(**db_params)
    cursor = connection.cursor()

    # Construct the DROP TABLE query
    drop_table_query = f"DROP TABLE {table_name}"

    # Execute the DROP TABLE query
    cursor.execute(drop_table_query)
    print(f"Table {table_name} has been deleted.")

except mysql.connector.Error as e:
    print(f"Error: {e}")

finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()
