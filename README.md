# What is this project?

This is a Python-based Student Management System built with PyQt6 and MySQL. The application provides functionalities for managing student data, including adding, updating, searching, and deleting records.

## Overview

The Student Management System allows users to perform various operations on student records, including:

- **Add Student:** Add a new student to the database.
- **Search Student:** Search for a student by name.
- **Update Student:** Modify student details like name, course, or mobile number.
- **Delete Student:** Remove a student's record from the database.

## Setup
1. Clone the repository.
2. Install the required packages using `pip install -r requirements.txt`.
3. Create a MYSQL database and run `db_script.sql` to create table.
4. Create a `.env` file and save database password as DB_PASSWORD="<password>"
5. Run the app using `python main.py`.
