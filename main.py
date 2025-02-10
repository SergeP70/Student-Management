import sys
import sqlite3
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QComboBox, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QMessageBox, QToolBar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setFixedWidth(600)
        self.setFixedHeight(600)

        mnu_file = self.menuBar().addMenu("&File")
        action_add_student = QAction('Add Student', self)
        action_add_student.triggered.connect(self.insert)
        mnu_file.addAction(action_add_student)

        mnu_edit = self.menuBar().addMenu("&Edit")
        action_search_student = QAction('Search', self)
        action_search_student.triggered.connect(self.search)
        mnu_edit.addAction(action_search_student)

        mnu_help = self.menuBar().addMenu("&Help")
        about_action = QAction('About', self)
        mnu_help.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(action_add_student)
        toolbar.addAction(action_search_student)


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

    def search(self):
        dialog = SearchDialog()
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

class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Search a student')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        self.txtName = QLineEdit()
        self.txtName.setPlaceholderText('Name')
        layout.addWidget(self.txtName)

        self.btnSearch = QPushButton('Search')
        self.btnSearch.clicked.connect(self.search)
        layout.addWidget(self.btnSearch)

        self.setLayout(layout)

    def search(self):
        main_window.tblStudents.setCurrentItem(None)
        lookup = self.txtName.text()
        matching_items = main_window.tblStudents.findItems(lookup, Qt.MatchFlag.MatchContains)
        if matching_items:
            for item in matching_items:
                item.setSelected(True)
        else:
            msg = QMessageBox.warning(self, 'Information', 'Data was not found',
                                      defaultButton=QMessageBox.StandardButton.Ok)
            msg.exec()




app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())