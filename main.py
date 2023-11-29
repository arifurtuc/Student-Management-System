from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QGridLayout, QLineEdit, \
    QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, \
    QVBoxLayout, QComboBox, QMessageBox, QToolBar, QStatusBar

from PyQt6.QtGui import QAction, QIcon
import sys
import mysql.connector
import os
from dotenv import load_dotenv

# Load database password from environment variables
load_dotenv()
db_password = os.getenv("PASSWORD")


class DatabaseConnection:
    def __init__(
            self, host="localhost", user="root",
            password=db_password, database="sms_db"
    ):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        return connection


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(600, 400)

        # Creating File, Help, Edit menus in the menu bar
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        # Adding actions to File menu
        add_student_action = QAction(QIcon("icons/add.png"), "Add Student",
                                     self)
        file_menu_item.addAction(add_student_action)
        add_student_action.triggered.connect(self.insert_data)

        # Adding actions to Help menu
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)
        about_action.triggered.connect(self.about)

        # Adding actions to Edit menu
        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        edit_menu_item.addAction(search_action)
        search_action.triggered.connect(self.search_data)

        # Creating a table widget for student data display
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Creating toolbar and adding elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # Creating status bar and adding elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detecting cell click
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        """Handles the action when a cell is clicked in the table."""
        # Creating buttons for editing and deleting records
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit_data)
        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete_data)

        # Removing existing buttons from the status bar
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        # Adding edit and delete buttons to the status bar
        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def load_data(self):
        """Connecting to the SQLite database and fetching data."""
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students")
        result = cursor.fetchall()
        self.table.setRowCount(0)

        # Populating the table widget with data from the database
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(
                    row_number,
                    column_number,
                    QTableWidgetItem(str(data))
                )
        connection.close()

    def insert_data(self):
        dialog = InsertDialog()
        dialog.exec()

    def search_data(self):
        dialog = SearchDialog()
        dialog.exec()

    def edit_data(self):
        dialog = EditDialog()
        dialog.exec()

    def delete_data(self):
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        # Setting up layout for the dialog
        layout = QVBoxLayout()

        # Creating input fields for student name, course, and mobile
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # Adding a button to add student data to the database
        button = QPushButton("Add")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        # Set the layout for the dialog window
        self.setLayout(layout)

    def add_student(self):
        """Adding a new student to the database."""
        # Fetching data from input fields
        name = self.student_name.text()
        course = self.course_name.currentText()
        mobile = self.mobile.text()

        # Connecting to the database and inserting student data
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO students (name, course, mobile) VALUES (%s, %s, %s)",
            (name, course, mobile)
        )
        connection.commit()
        cursor.close()
        connection.close()

        # Updating the main window data after insertion
        main_window.load_data()

        # Close the current dialog window after successful insertion
        self.close()

        # Display a confirmation message
        title = "Success"
        message = "New student has been added successfully!"
        ConfirmationMessageBox(title, message)


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        # Setting up layout for the dialog
        layout = QVBoxLayout()

        # Creating input fields for student name
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Adding a button to search student data
        button = QPushButton("Search")
        button.clicked.connect(self.search_student)
        layout.addWidget(button)

        # Set the layout for the dialog window
        self.setLayout(layout)

    def search_student(self):
        """Searches for a student in the database by name."""
        name = self.student_name.text()

        # Connecting to the database and executing the search query
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM students WHERE name = %s", (name,)
        )
        result = cursor.fetchall()
        rows = list(result)

        # Highlighting the matching records in the table
        items = main_window.table.findItems(
            name, Qt.MatchFlag.MatchFixedString
        )
        for item in items:
            main_window.table.item(item.row(), 1).setSelected(True)

        # Handling the case where no matching records are found
        if not rows:
            title = "No Records"
            message = "No matching records found!"
            ConfirmationMessageBox(title, message)
        cursor.close()
        connection.close()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        # Setting up layout for the dialog
        layout = QVBoxLayout()

        # Retrieving selected student's data from the main window's table
        selected_index = main_window.table.currentRow()
        student_name = main_window.table.item(selected_index, 1).text()
        self.student_id = main_window.table.item(selected_index, 0).text()

        # Setting up input fields with existing student information for update
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        course_name = main_window.table.item(selected_index, 2).text()
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        mobile = main_window.table.item(selected_index, 3).text()
        self.mobile = QLineEdit(mobile)
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # Adding a button to update student data to the database
        button = QPushButton("Update")
        button.clicked.connect(self.update_student)
        layout.addWidget(button)

        # Set the layout for the dialog window
        self.setLayout(layout)

    def update_student(self):
        """Updates the student's data in the database."""
        # Connecting to the database and updating student data
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE students SET name = %s, course = %s, mobile = %s "
            "WHERE id = %s",
            (
                self.student_name.text(),
                self.course_name.currentText(),
                self.mobile.text(),
                self.student_id
            )
        )
        connection.commit()
        cursor.close()
        connection.close()

        # Refreshing the data displayed in the main window after update
        main_window.load_data()

        # Close the current dialog window after successful update
        self.close()

        # Display a confirmation message
        title = "Success"
        message = "Student data has been updated successfully!"
        ConfirmationMessageBox(title, message)


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Data")

        # Setting up layout for the dialog
        layout = QGridLayout()

        # Create a label to display the confirmation message
        confirmation = QLabel("Are you sure you want to delete?")

        # Create 'Yes' button and connect it to the delete_student method
        yes_button = QPushButton("Yes")
        yes_button.clicked.connect(self.delete_student)

        # Create 'No' button and connect it to the built-in reject method of
        # QDialog
        no_button = QPushButton("No")
        no_button.clicked.connect(self.reject)

        # Add the components to the layout in specific positions
        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes_button, 1, 0)
        layout.addWidget(no_button, 1, 1)

        # Set the layout for the dialog window
        self.setLayout(layout)

    def delete_student(self):
        """Deletes the student's data from database."""
        # Retrieving the student ID of the selected row
        selected_index = main_window.table.currentRow()
        student_id = main_window.table.item(selected_index, 0).text()

        # Connecting to the database and deleting student data
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute(
            "DELETE from students WHERE id = %s",
            (student_id,)
        )
        connection.commit()
        cursor.close()
        connection.close()

        # Refreshing the data displayed in the main window after delete
        main_window.load_data()

        # Close the current dialog window after successful deletion
        self.close()

        # Display a confirmation message
        title = "Success"
        message = "Student data has been deleted successfully!"
        ConfirmationMessageBox(title, message)


class AboutDialog(QMessageBox):
    def __init__(self):
        """Displays about using QMessageBox"""
        super().__init__()
        self.setWindowTitle("About")
        content = """This app allows user to manage student data by adding, 
        updating, deleting functionality."""
        self.setText(content)


class ConfirmationMessageBox(QMessageBox):
    def __init__(self, title, message):
        """Displays a confirmation message using QMessageBox"""
        super().__init__()
        self.setWindowTitle(title)
        self.setText(message)
        self.exec()


# Creating the application and main window
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())
