import mysql.connector

class DatabaseConnection:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None

    def __enter__(self):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

# Use the custom context manager to perform a query
with DatabaseConnection(
    host='localhost',
    user='root',
    password='Immamanu1234!',
    database='ALX_prodev'
) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data")
    results = cursor.fetchall()
    for row in results:
        print(row)
    cursor.close()
