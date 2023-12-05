# Ease Inventory Tracker

---

## Overview

The Ease Inventory Tracker is a simple Flask web application designed to help users manage their inventory of materials. This README.md file provides comprehensive information about the project, including its purpose, structure, setup instructions, and functionalities.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Database Setup](#database-setup)
6. [Contributing](#contributing)
7. [Contact Information](#contact-information)

---

## 1. Introduction

The Ease Inventory Tracker is built using the Flask web framework and SQLite database. It allows users to register, log in, and manage their inventory of materials, including adding, updating, and deleting materials. The project aims to provide a straightforward solution for individuals or small businesses to keep track of their inventory.

---

## 2. Project Structure

The project structure is organized as follows:

- `app.py`: The main Flask application file containing the routes and logic.
- `db_setup.py`: Script to create the SQLite database file (`inventory.db`) and set up the SQL schema for the app.
- `static/`: Directory containing static files (CSS, JS).
- `templates/`: Directory containing HTML templates.
- `/static/styles/`: Directory containing CSS files.
- `/static/scripts/`: Directory containing JavaScript files.
- `README.md`: Comprehensive documentation for the project.

---

## 3. Installation

Follow the steps below to set up the Ease Inventory Tracker on your local machine:

1. Clone the repository:

   ```bash
   git clone https://github.com/phila-hh/ease_inventory_tracker.git
   ```

2. Navigate to the project directory:

   ```bash
   cd ease_inventory_tracker
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## 4. Usage

To run the Ease Inventory Tracker application, execute the following command:

```bash
python3 app.py
```

Access the application in your web browser at `http://localhost:5000`.

---

## 5. Database Setup

Before running the application, set up the SQLite database using the provided scripts:

1. Run `db_setup.py` to create the database and necessary tables:

   ```bash
   python3 db_setup.py
   ```

---

## 6. Contributing

Contributions to the Ease Inventory Tracker project are welcome. Follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Implement your changes.
4. Test thoroughly.
5. Create a pull request.

---

## 7. Contact Information

For any inquiries or feedback, please contact:

- **Author**: Filimon Haftom
- **Email**: filimon.haftomh@gmail.com
- **GitHub**: [phila-hh](https://github.com/phila-hh)
- **Twitter**: [@phila_hh](https://twitter.com/phila_hh)

Feel free to reach out for assistance, feedback, or collaboration!
