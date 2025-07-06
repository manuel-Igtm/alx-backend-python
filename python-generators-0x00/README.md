# README.md

## Project: Python SQL Seeder with Streaming Generator

This project sets up a MySQL database and populates it with sample user data from a CSV file. It uses a Python script `seed.py` for all the setup and seeding operations, and `0-main.py` to execute and test these operations.

---

## 📁 File Structure

```
alx-backend-python/
├── python-generators-0x00/
│   ├── seed.py
│   ├── 0-main.py
│   ├── user_data.csv
│   └── README.md
```

---

## 📜 `seed.py`

A helper module that:

* Connects to a MySQL server
* Creates a database named `ALX_prodev` if it doesn't exist
* Connects to the `ALX_prodev` database
* Creates a table `user_data` with specified fields
* Loads and inserts data from a CSV file

### Database Schema

```sql
CREATE TABLE user_data (
    user_id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    age DECIMAL NOT NULL
);
```

### Functions

```python
def connect_db():
    """Connects to MySQL server."""

def create_database(connection):
    """Creates database 'ALX_prodev' if it does not exist."""

def connect_to_prodev():
    """Connects to the 'ALX_prodev' database."""

def create_table(connection):
    """Creates the 'user_data' table if it does not exist."""

def insert_data(connection, csv_file):
    """Reads user_data.csv and inserts unique rows into the database."""
```

---

## ▶️ `0-main.py`

This script runs the `seed.py` functions to:

1. Connect to the server
2. Create the database
3. Reconnect to the database
4. Create the table
5. Insert sample data from `user_data.csv`
6. Confirm database and table setup
7. Display the first 5 records

---

## 📂 `user_data.csv`

A sample data file used to seed the `user_data` table.
Ensure it is in the same folder as `seed.py` or use the correct path.

CSV format:

```
user_id,name,email,age
uuid1,Name1,email1@example.com,25
...
```

---

## ✅ Requirements

* Python 3.x
* MySQL server installed and running (e.g., MySQL Community Server or XAMPP)
* Python packages:

  * `mysql-connector-python`

Install required Python package:

```bash
pip install mysql-connector-python
```

---

## 💡 Notes

* Update the MySQL user credentials in `seed.py` accordingly (default is `root` with password).
* Ensure MySQL is running on `localhost:3306`.
* `user_data.csv` must be well-formatted and contain unique `user_id`s.

---

## 🛠️ Example Usage

```bash
python 0-main.py
```

---


📤 Stream User Data with Generator
The 0-stream_users.py script defines a generator function to stream user records one by one from the database.

Function: stream_users()
Prototype: def stream_users()

Description: Connects to the ALX_prodev MySQL database and yields each row from the user_data table as a dictionary.

Usage:

python
Copy
Edit
from itertools import islice
from 0-stream_users import stream_users

for user in islice(stream_users(), 6):
    print(user)
Sample Output:

bash
Copy
Edit
{'user_id': '...', 'name': '...', 'email': '...', 'age': ...}
✅ Efficient for handling large datasets without loading everything into memory.


## 🧑‍💻 Author

Immanuel Njogu
