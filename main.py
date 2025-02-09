import sys

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QComboBox, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        mnu_file = self.menuBar().addMenu("&File")
        mnu_help = self.menuBar().addMenu("&Help")

        add_student_action = QAction('Add Student', self)
        mnu_file.addAction(add_student_action)

        about_action = QAction('About', self)
        mnu_help.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)



app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())