import sys
import sqlite3
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QComboBox, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        mnu_file = self.menuBar().addMenu("&File")
        mnu_help = self.menuBar().addMenu("&Help")

        action_add_student = QAction('Add Student', self)
        action_add_student.triggered.connect(self.insert)
        mnu_file.addAction(action_add_student)

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

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Add a student')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        self.txtName = QLineEdit()
        self.txtName.setPlaceholderText('Name')
        layout.addWidget(self.txtName)

        self.cboCourse = QComboBox()
        courses = ['Biology', 'Astronomy', 'Math', 'Physics']
        self.cboCourse.addItems(courses)
        layout.addWidget(self.cboCourse)

        self.txtMobile = QLineEdit()
        self.txtMobile.setPlaceholderText('Mobile nr')
        layout.addWidget(self.txtMobile)

        btnSubmit = QPushButton('Submit')
        btnSubmit.clicked.connect(self.add_student)
        layout.addWidget(btnSubmit)

        self.setLayout(layout)

    def add_student(self):
        name = self.txtName.text()
        course = self.cboCourse.currentText()
        mobile = self.txtMobile.text()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)',
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()




app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())