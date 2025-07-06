import mysql.connector
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    """Generator function that yields user records in batches."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='ALX_prodev',
            user='root',
            password='Immamanu1234!'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) as total FROM user_data")
            total = cursor.fetchone()['total']
            
            for offset in range(0, total, batch_size):
                cursor.execute(
                    "SELECT * FROM user_data LIMIT %s OFFSET %s", (batch_size, offset))
                rows = cursor.fetchall()
                yield rows

    except Error as e:
        print(f"Error connecting to MySQL: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def batch_processing(batch_size):
    """Processes batches and filters users older than 25."""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
