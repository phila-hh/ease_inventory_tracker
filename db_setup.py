"""
This script serves the purpose of creating an SQLite database file (inventory.db) for the Ease Inventory Tracker app. Also, it sets up the SQL schema for the Ease Inventory Tracker app by creating the necessary tables (users and materials) in the SQLite database.

"""

import sqlite3
import os

def create_database():
    try:
        db = sqlite3.connect("inventory.db")
        db.commit()
        db.close()
        print("Database and tables created successfully.")
    except sqlite3.Error as e:
        print(e)


def create_schema():
    try:
        db = sqlite3.connect("inventory.db")
        c = db.cursor()

        # Create the users table
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT UNIQUE,
                      email TEXT UNIQUE,
                      password TEXT)''')

        # Create the materials table
        c.execute('''CREATE TABLE IF NOT EXISTS materials
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id INTEGER,
                      material_name TEXT,
                      quantity INTEGER,
                      price REAL,
                      UNIQUE(user_id, material_name),
                      FOREIGN KEY (user_id) REFERENCES users(id))''')

        db.commit()
        db.close()
        print("Schema created successfully.")
    except sqlite3.Error as e:
        print(e)


if __name__ == "__main__":
    # Check if the database file already exists
    if not os.path.exists("inventory.db"):
        create_database()
    else:
        print("Database already exists.")

    create_schema()
