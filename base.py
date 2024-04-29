import sqlite3
import json
import os

# Define the path to the SQLite database file
DATABASE_FILE = "students.db"

# Function to initialize the database schema
def initialize_database():
    if not os.path.exists(DATABASE_FILE):
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE students (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            department TEXT NOT NULL,
                            matric_number TEXT NOT NULL,
                            level INTEGER NOT NULL,
                            image_path TEXT NOT NULL
                          )''')
        conn.commit()
        conn.close()

# Function to insert student data into the database
def insert_student_data(name, department, matric_number, level, image_path):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO students (name, department, matric_number, level, image_path)
                      VALUES (?, ?, ?, ?, ?)''', (name, department, matric_number, level, image_path))
    conn.commit()
    conn.close()

# Function to create seat identities for students
def create_seat_identities():
    seat_identities = {}
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT matric_number FROM students")
    rows = cursor.fetchall()
    for row in rows:
        seat_id = "A" + str(hash(row[0]) % 1000)  # Create a unique seat identity based on the hash of matric number
        seat_identities[row[0]] = seat_id
    conn.close()
    return seat_identities

# Example function to use in your application
def main():
    initialize_database()
    # Insert sample student data (replace with actual data)
    insert_student_data("John Doe", "Computer Science", "123456", 300, "images/john_doe.jpg")
    insert_student_data("Jane Smith", "Electrical Engineering", "789012", 200, "images/jane_smith.jpg")
    # Create seat identities for students
    seat_identities = create_seat_identities()
    print(json.dumps(seat_identities, indent=4))

if __name__ == "__main__":
    main()
