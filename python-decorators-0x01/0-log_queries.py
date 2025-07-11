from datetime import datetime
import mysql.connector
import functools

#### decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') or (args[0] if args else None)
        if query:
            print(f"[{datetime.now()}] [SQL LOG] Executing query: {query}")
        else:
            print(f"[{datetime.now()}] [SQL LOG] No SQL query found in arguments.")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Immamanu1234!',
        database='ALX_prodev'
    )
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
