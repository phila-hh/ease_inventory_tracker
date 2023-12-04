"""
Ease Inventory Tracker - Flask Web Application

This Flask web application serves as an inventory tracker
with user authentication.

Dependencies:
- Flask
- SQLite (for the database)
- db_methods module (contains database methods)

To run the application:
1. Install the required dependencies by running: pip install Flask
2. Create the database by running the setup script: python3 db_setup.py
3. Run this script: python3 ease_inventory_tracker.py

"""

from flask import Flask, render_template, request, redirect, session, flash, g
from db_methods import (
    check_existing_user,
    register_user,
    login_user,
    add_material_to_db,
    fetch_material_info,
    update_material_info,
    get_all_data,
    fetch_username
)
import secrets

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = secrets.token_hex(32)

app.static_folder = 'static'


# Teardown app context to close the database connection
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# Index route to render the login page
@app.route('/')
def index():
    return render_template('login.html', value=None)


# Login route for handling user login
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_id = login_user(username, password)
        if user_id is not None:
            session['user_id'] = user_id
            return redirect('/dashboard')
        else:
            flash('Invalid username or password. Please try again.', 'error')
            return render_template('login.html', value=True)

    return render_template('login.html')


# Signup route for handling user registration
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if check_existing_user(username, email):
            flash('Username or email already exists. Please choose another.',
                  'error')
            return render_template('signup.html', value=True)

        registered = register_user(username, email, password)

        if registered:
            user_id = login_user(username, password)

            if user_id is not None:
                session['user_id'] = user_id
                flash('Account created successfully!', 'success')
                return redirect('/dashboard')
            else:
                flash('Error during login. Please try again.', 'error')
                return render_template('login.html', value=True)
        else:
            flash('Error during registration. Please try again.', 'error')
            return render_template('signup.html', value=True)
    return render_template('signup.html')


# Route to handle adding materials
@app.route('/add_material', methods=['GET', 'POST'])
def add_material():
    if request.method == 'POST':
        material_name = request.form['material_name']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])

        user_id = session.get('user_id')

        added_successfully = add_material_to_db(user_id, material_name,
                                                quantity, price)

        if added_successfully:
            flash('Material added successfully!', 'success')
            return redirect('/dashboard')
        else:
            flash('Error adding material. Please try again.', 'error')

    return render_template('add_material.html')


# Route to handle editing materials
@app.route('/edit_material/<int:material_id>', methods=['GET', 'POST'])
def edit_material(material_id):
    material_info = fetch_material_info(material_id)

    if request.method == 'POST':
        updated_name = request.form['material_name']
        updated_quantity = int(request.form['quantity'])
        updated_price = float(request.form['price'])

        update_material_info(material_id, updated_name,
                             updated_quantity, updated_price)

        flash('Material updated successfully!', 'success')
        return redirect('/dashboard')

    return render_template('edit_material.html', material_info=material_info)


# Dashboard route to render the user dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        info = get_all_data(user_id)
        username = fetch_username(user_id)
        return render_template('inventory_list.html', info=info,
                               username=username)
    else:
        return redirect('/')


# Logout route to handle user loging out
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
