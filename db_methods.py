"""
Ease Inventory Tracker Application

This application manages inventory by allowing users to register,
log in, add, edit, and delete materials, and view their inventory.

This module contains all the methods used to store, update and delete
user information on the database.

Dependencies:
- Flask: Web framework for handling HTTP requests.
- sqlite3: SQLite database for storing user and material information.
- hashlib: Used for hashing passwords.

"""

import sqlite3
import hashlib
import os
from flask import g, Flask

app = Flask(__name__)


# Function to create a connection to the SQLite database
def get_db():
    db = getattr(g, '_database', None)

    if db is None:
        if not os.path.exists("inventory.db"):
            # Create a new database file if it doesn't exist
            initialize_database()

        db = g._database = sqlite3.connect("inventory.db")
        print("Connected to SQLite database")

    return db


# Add a function to initialize the database if it doesn't exist
def initialize_database():
    db = sqlite3.connect("inventory.db")
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


# Function to initialize the app
def init_app():
    with app.app_context():
        db = get_db()
        if not os.path.isfile("inventory.db"):
            # The database file doesn't exist, create the tables
            create_user_table(db)
            create_materials_table(db)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# Function to create the user table in the database
def create_user_table():
    try:
        db = get_db()
        c = db.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT UNIQUE,
                      email TEXT UNIQUE,
                      password TEXT)''')
        print("User table created successfully")
        return True
    except sqlite3.Error as e:
        print(True)
        return False


# Function to create the materials table in the database
def create_materials_table():
    try:
        db = get_db()
        c = db.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS materials
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id INTEGER,
                      material_name TEXT,
                      quantity INTEGER,
                      price REAL,
                      UNIQUE(user_id, material_name),
                      FOREIGN KEY (user_id) REFERENCES users(id))''')
        print("Materials table created successfully")
        return True
    except sqlite3.Error as e:
        print(e)
        return False


# Function to check if a username or email already exists
def check_existing_user(username, email):
    try:
        db = get_db()
        c = db.cursor()
        c.execute("SELECT id FROM users WHERE username=? OR email=?",
                  (username, email))
        existing_user = c.fetchone()
        return existing_user is not None
    except sqlite3.Error as e:
        print(e)
        return False


# Function to register a new user
def register_user(username, email, password):
    try:
        db = get_db()
        c = db.cursor()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        c.execute("INSERT INTO users (username, email, password)
                  VALUES (?, ?, ?)", (username, email, hashed_password))
        db.commit()
        print("User registered successfully")
        return True
    except sqlite3.Error as e:
        print(e)
        return False


# Function to log in a user
def login_user(username, password):
    try:
        db = get_db()
        c = db.cursor()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        c.execute("SELECT * FROM users WHERE username=? AND password=?",
                  (username, hashed_password))
        user = c.fetchone()
        if user:
            print("Login successful")
            return user[0]  # Return the user ID
        else:
            print("Invalid username or password")
            return None
    except sqlite3.Error as e:
        print(e)
        return None


# Function to add a material to the user's inventory
def add_material_to_db(user_id, material_name, quantity, price):
    try:
        db = get_db()
        c = db.cursor()
        # Check if the material already exists for the user
        c.execute("SELECT * FROM materials WHERE user_id=? AND
                  material_name=?", (user_id, material_name))
        existing_material = c.fetchone()

        if existing_material:
            # Material already exists for the user, you can choose to update it
            # or display an error message
            print("Material with name '{}' already exists in your inventory."
                  .format(material_name))
            return False
        else:
            # If the material doesn't exist, insert a new recor
            print("line 115")
            c.execute("INSERT INTO materials (user_id, material_name,
                      quantity, price) VALUES (?, ?, ?, ?)",
                      (user_id, material_name, quantity, price))
            print("Material added successfully")
        db.commit()
        print("Material added successfully")
        return True
    except sqlite3.Error as e:
        print("line 122")
        print(e)
        return False


# Function to delete a material from the user's inventory
def delete_material(user_id, material_name):
    try:
        db = get_db()
        c = db.cursor()
        c.execute("DELETE FROM materials WHERE user_id=? AND material_name=?",
                  (user_id, material_name))
        db.commit()
        print("Material deleted successfully")
        return True
    except sqlite3.Error as e:
        print(e)
        return False


# Function to update the price of a material in the user's inventory
def update_material_price(user_id, material_name, new_price):
    try:
        db = get_db()
        c = db.cursor()
        c.execute("UPDATE materials SET price=? WHERE user_id=? AND
                  material_name=?", (new_price, user_id, material_name))
        db.commit()
        print("Material price updated successfully")
        return True
    except sqlite3.Error as e:
        print(e)
        return False


# Function to update the quantity of a material in the user's inventory
def update_material_quantity(user_id, material_name, new_quantity):
    try:
        db = get_db()
        c = db.cursor()
        c.execute("UPDATE materials SET quantity=? WHERE user_id=? AND
                  material_name=?", (new_quantity, user_id, material_name))
        db.commit()
        print("Material quantity updated successfully")
        return True
    except sqlite3.Error as e:
        print(e)
        return False


# Function to update the name of a material in the user's inventory
def update_material_name2(user_id, material_name, new_name):
    try:
        db = get_db()
        c = db.cursor()
        c.execute("UPDATE materials SET material_name=? WHERE user_id=? AND
                  material_name=?", (new_name, user_id, material_name))
        db.commit()
        print("Material name updated successfully")
        return True
    except sqlite3.Error as e:
        print(e)
        return False


# Function to update the name of a material in the user's inventory
def update_material_name_in_db(material_id, new_name):
    try:
        db = get_db()
        c = db.cursor()
        c.execute("UPDATE materials SET material_name=? WHERE id=?",
                  (new_name, material_id))
        db.commit()
        print("Material name updated successfully")
        return True
    except sqlite3.Error as e:
        print(e)
        return False


# Function to fetch the price of a material in a user's inventory
def fetch_price(user_id, material_name):
    try:
        db = get_db()
        c = db.cursor()
        c.execute("SELECT price FROM materials WHERE user_id=? AND
                  material_name=?", (user_id, material_name))
        price = c.fetchone()
        return price[0]
    except sqlite3.Error as e:
        print(e)
        return None


# Function to fetch the quantity of a material in a user's inventory
def fetch_quantity(user_id, material_name):
    try:
        db = get_db()
        c = db.cursor()
        c.execute("SELECT quantity FROM materials WHERE user_id=? AND
                  material_name=?", (user_id, material_name))
        quantity = c.fetchone()
        return quantity[0]
    except sqlite3.Error as e:
        print(e)
        return None


# Function to fetch a users username
def fetch_username(user_id):
    try:
        db = get_db()
        c = db.cursor()
        c.execute("SELECT username FROM users WHERE id=?", (user_id,))
        username = c.fetchone()
        return username[0]
    except sqlite3.Error as e:
        print(e)
        return None


# Function to fetch the ID of a material in a user's inventory
def fetch_material_id(user_id, material_name):
    try:
        db = get_db()
        c = db.cursor()
        c.execute("SELECT id FROM materials WHERE user_id=? AND
                  material_name=?", (user_id, material_name))
        material_id = c.fetchone()
        return material_id[0] if material_id else None
    except sqlite3.Error as e:
        print(e)
        return None


# Function to fetch material information based on material_id
def fetch_material_info(material_id):
    try:
        db = get_db()
        c = db.cursor()
        c.execute("SELECT * FROM materials WHERE id=?", (material_id,))
        material_info = c.fetchone()
        if material_info:
            # Convert the material_info tuple to a dictionary
            material_dict = {
                    'id': material_info[0],
                    'user_id': material_info[1],
                    'material_name': material_info[2],
                    'quantity': material_info[3],
                    'price': material_info[4]
                    }
            return material_dict
        else:
            return None
    except sqlite3.Error as e:
        print(e)
        return None


# Function to update material information in the database
def update_material_info(material_id, updated_name,
                         updated_quantity, updated_price):
    try:
        db = get_db()
        c = db.cursor()
        c.execute("UPDATE materials SET material_name=?, quantity=?,
                  price=? WHERE id=?", (updated_name, updated_quantity,
                                        updated_price, material_id))
        db.commit()
        print("Material info updated successfully")
        return True
    except sqlite3.Error as e:
        print(e)
        return False


# Function to fetch all the materials in a user's inventory
def fetch_all_materials(user_id):
    material_names_list = []
    try:
        db = get_db()
        c = db.cursor()
        c.execute("SELECT material_name FROM materials WHERE user_id=?",
                  (user_id,))
        materials = c.fetchall()
        for m in materials:
            material_names_list.append(m[0])
    except sqlite3.Error as e:
        print(e)

    return material_names_list


# Function that returns all of a user's info
def get_all_data(user_id):
    info = {}
    materials = fetch_all_materials(user_id)
    for m in materials:
        material_id = fetch_material_id(user_id, m)
        p = fetch_price(user_id, m)  # unit price of the material
        q = fetch_quantity(user_id, m)  # quantity of the material
        t = p * q  # total price for the material
        info[m] = {'id': material_id, 'quantity': q, 'price': p, 'total': t}

    return info
