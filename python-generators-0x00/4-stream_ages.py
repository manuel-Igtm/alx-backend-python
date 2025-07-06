import seed

def stream_user_ages():
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:
        yield row['age']
    connection.close()

def calculate_average_age():
    total_age = 0
    count = 0
    for age in stream_user_ages():
        total_age += age
        count += 1
    if count == 0:
        print("Average age of users: 0")
    else:
        print(f"Average age of users: {total_age / count:.2f}")

if __name__ == '__main__':
    calculate_average_age()
