import mysql.connector
import functools

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Immamanu1234!',
            database='ALX_prodev'
        )
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    return cursor.fetchone()

#### Fetch user by ID with automatic connection handling
user = get_user_by_id(user_id=1)
print(user)
