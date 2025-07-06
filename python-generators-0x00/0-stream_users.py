import mysql.connector
from mysql.connector import Error

def stream_users():
    """Generator that streams user data rows one at a time from the user_data table."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',     # 🔁 replace with your MySQL username
            password='Immamanu1234!', # 🔁 replace with your MySQL password
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data")

            for row in cursor:
                yield row

            cursor.close()
            connection.close()

    except Error as e:
        print(f"Error connecting to database: {e}")
        return
