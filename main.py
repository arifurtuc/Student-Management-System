from PyQt6.QtWidgets import QBoxLayout, QApplication, QWidget, QLabel, \
    QGridLayout, QLineEdit, QPushButton, QMainWindow, QTableWidget
from PyQt6.QtGui import QAction
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        # Creating File and Help menus in the menu bar
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")

        # Adding actions to File menu
        add_student_action = QAction("Add Student", self)
        file_menu_item.addAction(add_student_action)

        # Adding actions to Help menu
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        # Creating a table widget for student data display
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.setCentralWidget(self.table)

    def load_data(self):
        pass


# Creating the application and main window
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
