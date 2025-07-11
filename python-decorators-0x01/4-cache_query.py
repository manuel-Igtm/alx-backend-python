import time
import mysql.connector
import functools

query_cache = {}

# Decorator to handle DB connection
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

# Decorator to cache query results
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print("Fetching from cache")
            return query_cache[query]
        else:
            print("Executing and caching query")
            start_time = time.time()
            result = func(conn, query, *args, **kwargs)
            duration = time.time() - start_time
            print(f"Query executed in {duration:.4f} seconds")
            query_cache[query] = result
            return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call - executes and caches
users = fetch_users_with_cache(query="SELECT * FROM user_data")
print(users)

# Second call - returns from cache
users_again = fetch_users_with_cache(query="SELECT * FROM user_data")
print(users_again)