import sys
import sqlite3
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QComboBox, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QMessageBox, QToolBar, QStatusBar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(600, 400)

        mnu_file = self.menuBar().addMenu("&File")
        action_add_student = QAction(QIcon('icons/add.png'), 'Add Student', self)
        action_add_student.triggered.connect(self.insert)
        mnu_file.addAction(action_add_student)

        mnu_edit = self.menuBar().addMenu("&Edit")
        action_search_student = QAction(QIcon('icons/search.png'), 'Search', self)
        action_search_student.triggered.connect(self.search)
        mnu_edit.addAction(action_search_student)

        mnu_help = self.menuBar().addMenu("&Help")
        about_action = QAction('About', self)
        mnu_help.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        # create toolbar and elements
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

        # create status bar and elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect a cell click
        self.tblStudents.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        btnEdit = QPushButton('Edit record')
        btnEdit.clicked.connect(self.edit)
        btnDelete = QPushButton('Delete record')
        btnDelete.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child
                                            )
        self.statusbar.addWidget(btnEdit)
        self.statusbar.addWidget(btnDelete)


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

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
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

        btnCancel = QPushButton('Cancel')
        btnCancel.clicked.connect(self.closing)
        layout.addWidget(btnCancel)

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
        self.accept()

    def closing(self):
        self.accept()

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
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText('Data not found')
            msg.setWindowTitle('Warning')
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            button = msg.exec()

class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Edit a student')
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        layout = QVBoxLayout()

        # Get Student name from the selected row
        index = main_window.tblStudents.currentRow()
        student_name = main_window.tblStudents.item(index, 1).text()
        self.txtName = QLineEdit(student_name)
        self.txtName.setPlaceholderText('Name')
        layout.addWidget(self.txtName)

        self.student_id = main_window.tblStudents.item(index, 0).text()

        course_name = main_window.tblStudents.item(index, 2).text()
        self.cboCourse = QComboBox()
        courses = ['Biology', 'Astronomy', 'Math', 'Physics']
        self.cboCourse.addItems(courses)
        self.cboCourse.setCurrentText(course_name)
        layout.addWidget(self.cboCourse)

        mobile = main_window.tblStudents.item(index, 3).text()
        self.txtMobile = QLineEdit(mobile)
        self.txtMobile.setPlaceholderText('Mobile nr')
        layout.addWidget(self.txtMobile)

        btnSubmit = QPushButton('Update')
        btnSubmit.clicked.connect(self.update_student)
        layout.addWidget(btnSubmit)

        btnCancel = QPushButton('Cancel')
        btnCancel.clicked.connect(self.closing)
        layout.addWidget(btnCancel)

        self.setLayout(layout)

    def update_student(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        print(self.txtMobile.text())
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
                       (self.txtName.text(), self.cboCourse.currentText(), self.txtMobile.text(), self.student_id))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()

    def closing(self):
        self.accept()


class DeleteDialog(QDialog):
    pass


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())