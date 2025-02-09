import sys
import sqlite3
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QComboBox, QMainWindow, \
    QTableWidget, QTableWidgetItem


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

        self.tblStudents = QTableWidget()
        self.tblStudents.setColumnCount(4)
        self.tblStudents.setHorizontalHeaderLabels(('Id', 'Name', 'Course', 'Mobile'))
        self.tblStudents.verticalHeader().setVisible(False)
        self.setCentralWidget(self.tblStudents)

    def load_data(self):
        connection = sqlite3.connect('database.db')
        content = connection.execute("SELECT * FROM students")
        self.tblStudents.setRowCount(0)
        for row_id, row_data in enumerate(content):
            self.tblStudents.insertRow(row_id)
            for col_id, data in enumerate(row_data):
                self.tblStudents.setItem(row_id, col_id, QTableWidgetItem(str(data)))

        connection.close()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())