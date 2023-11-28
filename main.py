from PyQt6.QtWidgets import QBoxLayout, QApplication, QWidget, QLabel, \
    QGridLayout, QLineEdit, QPushButton, QMainWindow, QTableWidget, \
    QTableWidgetItem, QDialog, QVBoxLayout, QComboBox
from PyQt6.QtGui import QAction
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        # Creating File and Help menus in the menu bar
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")

        # Adding actions to File menu
        add_student_action = QAction("Add Student", self)
        add_student_action.triggered.connect(self.insert_data)
        file_menu_item.addAction(add_student_action)

        # Adding actions to Help menu
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        # Creating a table widget for student data display
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    def load_data(self):
        """Connecting to the SQLite database and fetching data."""
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
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

        self.setLayout(layout)

    def add_student(self):
        """Adding a new student to the database."""
        # Fetching data from input fields
        name = self.student_name.text()
        course = self.course_name.currentText()
        mobile = self.mobile.text()

        # Connecting to the database and inserting student data
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
            (name, course, mobile)
        )
        connection.commit()
        cursor.close()
        connection.close()

        # Updating the main window data after insertion
        main_window.load_data()


# Creating the application and main window
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())
