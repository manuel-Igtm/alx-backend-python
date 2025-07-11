import mysql.connector

class ExecuteQuery:
    def __init__(self, query, params=None):
        self.query = query
        self.params = params
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Immamanu1234!',
            database='ALX_prodev'
        )
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

# Usage example
query = "SELECT * FROM user_data WHERE age > %s"
params = (25,)

with ExecuteQuery(query, params) as result:
    for row in result:
        print(row)
