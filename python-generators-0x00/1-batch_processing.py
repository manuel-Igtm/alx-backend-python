import mysql.connector


def stream_users_in_batches(batch_size):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Immamanu1234!",  # Replace with your actual MySQL password
        database="ALX_prodev"
    )

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch

    cursor.close()
    connection.close()
    return  # End of generator


def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user.get("age", 0) > 25:
                yield user
    return  # Optional: end generator (StopIteration will be raised)
