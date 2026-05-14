import sys
import sqlite3
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QStackedWidget, QFrame, QScrollArea,
    QTableWidget, QTableWidgetItem, QFormLayout, QDialog, QMessageBox,
    QLineEdit, QComboBox, QHeaderView, QCalendarWidget
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

DB_NAME = r"f:\DataBase SQLite\College Database.db"

def init_db():
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.close()
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Database error:\n{e}")

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Login - School Management System")
        self.resize(500, 400)
        self.setWindowFlags(Qt.Window | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.setStyleSheet("""
            QDialog { 
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #74ebd5, stop:1 #ACB6E5);
            }
            QLabel { color: #212529; font-weight: bold; font-size: 16px; }
            QLineEdit { padding: 10px; border-radius: 10px; border: 2px solid #dee2e6; font-size: 16px; }
            QPushButton { background-color: #007bff; color: white; padding: 12px; font-size: 16px; border-radius: 10px; }
            QPushButton:hover { background-color: #0056b3; }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        self.title = QLabel("Welcome, Admin")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 28px; font-weight: bold; color: #fff; margin-bottom: 30px;")
        layout.addWidget(self.title)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Username")
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.user_input)

        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setPlaceholderText("Password")
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.pass_input)

        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.check_login)
        layout.addWidget(self.login_btn)

        self.role = "viewer"

    def check_login(self):
        user = self.user_input.text()
        pwd = self.pass_input.text()

        if user == "admin" and pwd == "admin123":
            self.role = "admin"
            self.accept()
        else:
            QMessageBox.warning(self, "Access Denied", "Invalid credentials")


# ---------------- Admission Dialog ----------------
class DepartmentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add Department")
        self.setGeometry(200, 100, 600, 600)
        self.setStyleSheet("font-size:16px;background-color:#f8f9fa;")
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        scroll.setWidget(content)
        layout = QFormLayout(content)
        layout.setLabelAlignment(Qt.AlignRight)
        layout.setSpacing(25)
        layout.setContentsMargins(40,40,40,40)

        # Fields
        self.name_input = QLineEdit(); self.name_input.setMinimumHeight(45)
        layout.addRow(QLabel("<b>Department Name:</b>"), self.name_input)

        self.head_input = QLineEdit(); self.head_input.setMinimumHeight(45)
        layout.addRow(QLabel("<b>Department Head:</b>"), self.head_input)

        self.off_input = QLineEdit(); self.off_input.setMinimumHeight(45)
        layout.addRow(QLabel("<b>Department Office:</b>"), self.off_input)

        btns = QHBoxLayout()
        save_btn = QPushButton("Save Record"); save_btn.setStyleSheet("background-color:#28a745;color:white;padding:15px 30px;font-size:18px;border-radius:10px;")
        save_btn.clicked.connect(self.save_department)

        btns.addStretch(); btns.addWidget(save_btn); btns.addStretch()
        layout.addRow(btns)

        main_layout = QVBoxLayout(self); main_layout.addWidget(scroll)

        # self.setWindowTitle("Add Department")
        # self.resize(500, 400)

        # layout = QFormLayout(self)

        # self.name_input = QLineEdit()
        # layout.addRow("Department Name:", self.name_input)

        # btn = QPushButton("Save Department")
        # btn.clicked.connect(self.save_department)
        # layout.addRow(btn)

    # def save_course(self):
    #     name=self.name_input.text().strip(); fee=self.fee_input.text().strip();dur=self.dur_input.text().strip(); dept=self.dept_combo.currentText()
    #     if not all([name,fee,dur,dept]): QMessageBox.warning(self,"Error","Fill all fields"); return
    #     conn = sqlite3.connect(DB_NAME); cur=conn.cursor()
    #     cur.execute("SELECT D_id FROM Department WHERE D_Name=?",(dept,))
    #     d_id = cur.fetchone()[0]
    #     cur.execute("INSERT INTO Courses (C_name,C_Fee,C_Duration,D_id) VALUES (?,?,?,?)",(name,fee,dur,d_id))
    #     conn.commit(); conn.close(); QMessageBox.information(self,"Success","Course Added"); self.accept()


    def save_department(self):
        name = self.name_input.text().strip(); 
        head = self.head_input.text().strip(); 
        office = self.off_input.text().strip()
        if not all([name,head,office]):
            QMessageBox.warning(self, "Error", "Please Fill All"); 
            return 
    
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("INSERT INTO Department (D_Name,D_Head,D_Office) VALUES (?,?,?)", (name,head,office,))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Success", "Department added successfully!")
        self.accept()
        # except Exception as e:
        # QMessageBox.critical(self, "Error", str(e))


# class AdmissionDialog(QDialog):
#     def __init__(self, parent=None, is_student=True):
#         super().__init__(parent)
#         self.is_student = is_student
#         self.setWindowTitle("Student Admission" if is_student else "Teacher Admission")
#         self.setGeometry(200, 100, 600, 600)
#         self.setStyleSheet("font-size:16px;background-color:#f8f9fa;")
        
#         scroll = QScrollArea()
#         scroll.setWidgetResizable(True)
#         content = QWidget()
#         scroll.setWidget(content)
#         layout = QFormLayout(content)
#         layout.setLabelAlignment(Qt.AlignRight)
#         layout.setSpacing(25)
#         layout.setContentsMargins(40,40,40,40)

#         # Fields
#         self.name_input = QLineEdit(); self.name_input.setMinimumHeight(45)
#         layout.addRow(QLabel("<b>Name:</b>"), self.name_input)

#         self.father_input = QLineEdit(); self.father_input.setMinimumHeight(45)
#         layout.addRow(QLabel("<b>Father's Name:</b>"), self.father_input)

#         self.contact_input = QLineEdit(); self.contact_input.setMinimumHeight(45)
#         layout.addRow(QLabel("<b>Contact:</b>"), self.contact_input)

#         self.email_input = QLineEdit(); self.email_input.setMinimumHeight(45)
#         layout.addRow(QLabel("<b>Email:</b>"), self.email_input)

#         self.address_input = QLineEdit(); self.address_input.setMinimumHeight(45)
#         layout.addRow(QLabel("<b>Address:</b>"), self.address_input)

#         self.gender_combo = QComboBox()
#         self.gender_combo.addItems(["Male","Female","Other"])
#         self.gender_combo.setMinimumHeight(45)
#         layout.addRow(QLabel("<b>Gender:</b>"), self.gender_combo)

#         self.dept_combo = QComboBox(); self.dept_combo.setMinimumHeight(45)
#         self.load_departments()
#         self.dept_combo.currentIndexChanged.connect(self.load_courses if is_student else lambda: None)
#         layout.addRow(QLabel("<b>Department:</b>"), self.dept_combo)

#         self.course_combo = QComboBox(); self.course_combo.setMinimumHeight(45)
#         layout.addRow(QLabel("<b>Course:</b>"), self.course_combo)
#         self.load_courses()

#         # Buttons
#         btns = QHBoxLayout()
#         save_btn = QPushButton("Save Record"); save_btn.setStyleSheet("background-color:#28a745;color:white;padding:15px 30px;font-size:18px;border-radius:10px;")
#         save_btn.clicked.connect(self.save)
#         cancel_btn = QPushButton("Cancel"); cancel_btn.setStyleSheet("background-color:#dc3545;color:white;padding:15px 30px;font-size:18px;border-radius:10px;")
#         cancel_btn.clicked.connect(self.reject)
#         btns.addStretch(); btns.addWidget(save_btn); btns.addWidget(cancel_btn); btns.addStretch()
#         layout.addRow(btns)

#         main_layout = QVBoxLayout(self); main_layout.addWidget(scroll)

#     def load_departments(self):
#         try:
#             conn = sqlite3.connect(DB_NAME)
#             depts = conn.execute("SELECT D_Name FROM Department").fetchall()
#             conn.close()
#             self.dept_combo.clear()
#             for d in depts: self.dept_combo.addItem(d[0])
#         except: self.dept_combo.addItem("No departments")

#     def load_courses(self):
#         if not hasattr(self,'course_combo'): return
#         dept_name = self.dept_combo.currentText()
#         if not dept_name:
#             self.course_combo.clear(); self.course_combo.addItem("No courses"); return
#         try:
#             conn = sqlite3.connect(DB_NAME)
#             cur = conn.cursor()
#             cur.execute("""
#                 SELECT C_name FROM Courses
#                 JOIN Department ON Courses.D_id = Department.D_id
#                 WHERE Department.D_Name=?
#             """,(dept_name,))
#             courses = cur.fetchall()
#             conn.close()
#             self.course_combo.clear()
#             if courses:
#                 for c in courses: self.course_combo.addItem(c[0])
#             else: self.course_combo.addItem("No courses")
#         except: self.course_combo.addItem("Error loading courses")

#     def save(self):
#         name = self.name_input.text().strip()
#         contact = self.contact_input.text().strip()
#         gender = self.gender_combo.currentText()
#         dept = self.dept_combo.currentText()
#         if not all([name, contact, gender, dept]):
#             QMessageBox.warning(self,"Missing Data","Fill all required fields"); return
#         try:
#             conn = sqlite3.connect(DB_NAME)
#             cursor = conn.cursor()
#             cursor.execute("SELECT D_id FROM Department WHERE D_Name=?",(dept,))
#             d_id = cursor.fetchone()[0]

#             if self.is_student:
#                 father = self.father_input.text().strip()
#                 course = self.course_combo.currentText()
#                 cursor.execute("SELECT C_id FROM Courses WHERE C_name=?",(course,))
#                 c_id = cursor.fetchone()[0]
#                 cursor.execute("""
#                     INSERT INTO Student (Name,Father_Name,Contact,Gender,D_id,C_id)
#                     VALUES (?,?,?,?,?,?)
#                 """,(name,father,contact,gender,d_id,c_id))
#             else:
#                 cursor.execute("""
#                     INSERT INTO Teachers (Name,Contact,Gender,D_id)
#                     VALUES (?,?,?,?)
#                 """,(name,contact,gender,d_id))
#             conn.commit(); conn.close()
#             QMessageBox.information(self,"Success","Record saved successfully!"); self.accept()
#         except Exception as e:
#             QMessageBox.critical(self,"Database Error",str(e))


class StudentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Student Admission")
        self.setGeometry(200, 100, 600, 600)
        self.setStyleSheet("font-size:16px;background-color:#f8f9fa;")
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        scroll.setWidget(content)
        layout = QFormLayout(content)
        layout.setLabelAlignment(Qt.AlignRight)
        layout.setSpacing(25)
        layout.setContentsMargins(40,40,40,40)

        # Fields
        self.name_input = QLineEdit(); self.name_input.setMinimumHeight(45)
        layout.addRow(QLabel("<b>Student Name:</b>"), self.name_input)

        self.father_input = QLineEdit(); self.father_input.setMinimumHeight(45)
        layout.addRow(QLabel("<b>Father's Name:</b>"), self.father_input)

        self.contact_input = QLineEdit(); self.contact_input.setMinimumHeight(45)
        layout.addRow(QLabel("<b>Contact:</b>"), self.contact_input)

        self.email_input = QLineEdit(); self.email_input.setMinimumHeight(45)
        layout.addRow(QLabel("<b>Email:</b>"), self.email_input)

        self.address_input = QLineEdit(); self.address_input.setMinimumHeight(45)
        layout.addRow(QLabel("<b>Address:</b>"), self.address_input)

        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Male","Female","Other"])
        self.gender_combo.setMinimumHeight(45)
        layout.addRow(QLabel("<b>Gender:</b>"), self.gender_combo)

        self.dept_combo = QComboBox(); self.dept_combo.setMinimumHeight(45)
        self.load_departments()
        self.dept_combo.currentIndexChanged.connect(self.load_courses)
        layout.addRow(QLabel("<b>Department:</b>"), self.dept_combo)

        self.course_combo = QComboBox(); self.course_combo.setMinimumHeight(45)
        layout.addRow(QLabel("<b>Course:</b>"), self.course_combo)
        self.load_courses()
        btns = QHBoxLayout()
        save_btn = QPushButton("Save Record"); save_btn.setStyleSheet("background-color:#28a745;color:white;padding:15px 30px;font-size:18px;border-radius:10px;")
        save_btn.clicked.connect(self.save_student)
        cancel_btn = QPushButton("Cancel"); cancel_btn.setStyleSheet("background-color:#dc3545;color:white;padding:15px 30px;font-size:18px;border-radius:10px;")
        cancel_btn.clicked.connect(self.reject)
        btns.addStretch(); btns.addWidget(save_btn);btns.addWidget(cancel_btn); btns.addStretch()
        layout.addRow(btns)

        main_layout = QVBoxLayout(self); main_layout.addWidget(scroll)


        # self.setWindowTitle("Student Admission")
        # self.setGeometry(200, 100, 600, 650)

        # layout = QFormLayout(self)
        # layout.setSpacing(20)

        # self.name = QLineEdit()
        # self.father = QLineEdit()
        # self.contact = QLineEdit()
        # self.email = QLineEdit()
        # self.address = QLineEdit()

        # self.gender = QComboBox()
        # self.gender.addItems(["Male", "Female", "Other"])

        # self.department = QComboBox()
        # self.course = QComboBox()

        # self.load_departments()
        # self.department.currentIndexChanged.connect(self.load_courses)

        # layout.addRow("Name:", self.name)
        # layout.addRow("Father Name:", self.father)
        # layout.addRow("Contact:", self.contact)
        # layout.addRow("Email:", self.email)
        # layout.addRow("Address:", self.address)
        # layout.addRow("Gender:", self.gender)
        # layout.addRow("Department:", self.department)
        # layout.addRow("Course:", self.course)

        # save_btn = QPushButton("Save Student")
        # save_btn.clicked.connect(self.save_student)
        # layout.addRow(save_btn)

    def load_departments(self):
        conn = sqlite3.connect(DB_NAME)
        rows = conn.execute("SELECT D_id, D_Name FROM Department").fetchall()
        conn.close()
        self.dept_combo.clear()
        for d_id, name in rows:
            self.dept_combo.addItem(name, d_id)

    def load_courses(self):
        d_id = self.dept_combo.currentData()
        if d_id is None:
            self.course_combo.clear()
            return
        conn = sqlite3.connect(DB_NAME)
        rows = conn.execute(
            "SELECT C_id, C_name FROM Courses WHERE D_id=?", (d_id,)
        ).fetchall()


        # d_id = self.dept_combo.currentData()
        # conn = sqlite3.connect(DB_NAME)
        # rows = conn.execute(
        #     "SELECT C_id, C_name FROM Courses WHERE D_id=?", (d_id,)
        # ).fetchall()
        conn.close()
        self.course_combo.clear()
        for c_id, name in rows:
            self.course_combo.addItem(name, c_id)

    def save_student(self):
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Student
            (Name, Father_Name, Contact, Email, Address, Gender, D_id, C_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            self.name_input.text(),
            self.father_input.text(),
            self.contact_input.text(),
            self.email_input.text(),
            self.address_input.text(),
            self.gender_combo.currentText(),
            self.dept_combo.currentData(),
            self.course_combo.currentData()
        ))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", "Student admitted successfully")
        self.accept()


class TeacherDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Teacher Admission")
        self.setGeometry(200, 100, 600, 600)
        self.setStyleSheet("font-size:16px;background-color:#f8f9fa;")
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        scroll.setWidget(content)
        layout = QFormLayout(content)
        layout.setLabelAlignment(Qt.AlignRight)
        layout.setSpacing(25)
        layout.setContentsMargins(40,40,40,40)

        # Fields
        self.name_input = QLineEdit(); self.name_input.setMinimumHeight(45)
        layout.addRow(QLabel("<b>Teacher Name:</b>"), self.name_input)

        self.father_input = QLineEdit(); self.father_input.setMinimumHeight(45)
        layout.addRow(QLabel("<b>Father's Name:</b>"), self.father_input)

        self.contact_input = QLineEdit(); self.contact_input.setMinimumHeight(45)
        layout.addRow(QLabel("<b>Contact:</b>"), self.contact_input)

        self.email_input = QLineEdit(); self.email_input.setMinimumHeight(45)
        layout.addRow(QLabel("<b>Email:</b>"), self.email_input)

        self.address_input = QLineEdit(); self.address_input.setMinimumHeight(45)
        layout.addRow(QLabel("<b>Address:</b>"), self.address_input)

        self.qual_input = QLineEdit(); self.qual_input.setMinimumHeight(45)
        layout.addRow(QLabel("<b>Qualification:</b>"), self.qual_input)

        self.sub_input = QLineEdit(); self.sub_input.setMinimumHeight(45)
        layout.addRow(QLabel("<b>Subject:</b>"), self.sub_input)

        self.exp_input = QLineEdit(); self.exp_input.setMinimumHeight(45)
        layout.addRow(QLabel("<b>Experience:</b>"), self.exp_input)

        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Male","Female","Other"])
        self.gender_combo.setMinimumHeight(45)
        layout.addRow(QLabel("<b>Gender:</b>"), self.gender_combo)

        self.dept_combo = QComboBox(); self.dept_combo.setMinimumHeight(45)
        self.load_departments()
        self.dept_combo.currentIndexChanged.connect(self.load_courses)
        layout.addRow(QLabel("<b>Department:</b>"), self.dept_combo)

        self.course_combo = QComboBox(); self.course_combo.setMinimumHeight(45)
        layout.addRow(QLabel("<b>Course:</b>"), self.course_combo)
        self.load_courses()

        btns = QHBoxLayout()
        save_btn = QPushButton("Save Record"); save_btn.setStyleSheet("background-color:#28a745;color:white;padding:15px 30px;font-size:18px;border-radius:10px;")
        save_btn.clicked.connect(self.save_teacher)
        cancel_btn = QPushButton("Cancel"); cancel_btn.setStyleSheet("background-color:#dc3545;color:white;padding:15px 30px;font-size:18px;border-radius:10px;")
        cancel_btn.clicked.connect(self.reject)
        btns.addStretch(); btns.addWidget(save_btn);btns.addWidget(cancel_btn); btns.addStretch()
        layout.addRow(btns)

        main_layout = QVBoxLayout(self); main_layout.addWidget(scroll)


        # self.setWindowTitle("Teacher Admission")
        # self.setGeometry(200, 100, 600, 650)

        # layout = QFormLayout(self)
        # layout.setSpacing(20)

        # self.name = QLineEdit()
        # self.contact = QLineEdit()
        # self.email = QLineEdit()
        # self.address = QLineEdit()
        # self.qualification = QLineEdit()
        # self.experience = QLineEdit()

        # self.gender = QComboBox()
        # self.gender.addItems(["Male", "Female", "Other"])

        # self.department = QComboBox()
        # self.load_departments()

        # layout.addRow("Name:", self.name)
        # layout.addRow("Contact:", self.contact)
        # layout.addRow("Email:", self.email)
        # layout.addRow("Address:", self.address)
        # layout.addRow("Qualification:", self.qualification)
        # layout.addRow("Experience (Years):", self.experience)
        # layout.addRow("Gender:", self.gender)
        # layout.addRow("Department:", self.department)

        # save_btn = QPushButton("Save Teacher")
        # save_btn.clicked.connect(self.save_teacher)
        # layout.addRow(save_btn)

    def load_departments(self):
        conn = sqlite3.connect(DB_NAME)
        rows = conn.execute("SELECT D_id, D_Name FROM Department").fetchall()
        conn.close()
        self.dept_combo.clear()
        for d_id, name in rows:
            self.dept_combo.addItem(name, d_id)

    def load_courses(self):

        d_id = self.dept_combo.currentData()
        if d_id is None:
            self.course_combo.clear()
            return
        conn = sqlite3.connect(DB_NAME)
        rows = conn.execute(
            "SELECT C_id, C_name FROM Courses WHERE D_id=?", (d_id,)
        ).fetchall()

        # d_id = self.dept_combo.currentData()
        # conn = sqlite3.connect(DB_NAME)
        # rows = conn.execute(
        #     "SELECT C_id, C_name FROM Courses WHERE D_id=?", (d_id,)
        # ).fetchall()
        conn.close()
        self.course_combo.clear()
        for c_id, name in rows:
            self.course_combo.addItem(name, c_id)

    def save_teacher(self):
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Teachers
            (Name,Father_Name, Contact, Email, Address, Qualification,Subject, Experience, Gender,C_id, D_id)
            VALUES (?, ?, ?,?, ?, ?, ?, ?,?,?,?)
        """, (
            self.name_input.text(),
            self.father_input.text(),
            self.contact_input.text(),
            self.email_input.text(),
            self.address_input.text(),
            self.qual_input.text(),
            self.sub_input.text(),
            self.exp_input.text(),
            self.gender_combo.currentText(),
            self.course_combo.currentData(),
            self.dept_combo.currentData()
        ))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", "Teacher admitted successfully")
        self.accept()




# ---------------- Charts ----------------
class ChartCanvas(FigureCanvas):
    def __init__(self,parent=None,chart_type='bar'):
        fig = Figure(figsize=(10,6),facecolor='#f8f9fa')
        self.axes = fig.add_subplot(111)
        super().__init__(fig); self.setParent(parent)
        self.chart_type = chart_type
        self.plot()

    def plot(self):
        self.axes.clear()
        try:
            conn = sqlite3.connect(DB_NAME)
            if self.chart_type=='bar':
                cur = conn.cursor()
                cur.execute("""
                    SELECT D_Name,COUNT(DISTINCT Student_id),COUNT(DISTINCT Teacher_id)
                    FROM Department
                    LEFT JOIN Student ON Student.D_id=Department.D_id
                    LEFT JOIN Teachers ON Teachers.D_id=Department.D_id
                    GROUP BY D_Name
                """)
                data = cur.fetchall()
                if data:
                    depts = [r[0] for r in data]
                    students = [r[1] for r in data]
                    teachers = [r[2] for r in data]
                    x=range(len(depts)); width=0.35
                    self.axes.bar([i-width/2 for i in x],students,width,label='Students',color='#28a745')
                    self.axes.bar([i+width/2 for i in x],teachers,width,label='Teachers',color='#17a2b8')
                    self.axes.set_xticks(x); self.axes.set_xticklabels(depts,rotation=30)
                    self.axes.set_title("Students & Teachers by Department")
                else: self.axes.text(0.5,0.5,"No data",ha='center',fontsize=14)
            elif self.chart_type=='line':
                months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
                admissions=[120,180,220,250,280,320,350,380,400,420,450,500]
                self.axes.plot(months,admissions,marker='o',color='#ffc107',linewidth=3,markersize=8)
                self.axes.set_title("Monthly Student Admissions Trend")
        except: self.axes.text(0.5,0.5,"No data",ha='center',fontsize=14)
        if self.axes.get_legend_handles_labels()[0]: self.axes.legend()
        self.axes.grid(True,linestyle='--',alpha=0.7)
        self.draw()

class NoticeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add Notice")
        self.setGeometry(200, 100, 600, 600)
        self.setStyleSheet("font-size:16px;background-color:#f8f9fa;")
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        scroll.setWidget(content)
        layout = QFormLayout(content)
        layout.setLabelAlignment(Qt.AlignRight)
        layout.setSpacing(25)
        layout.setContentsMargins(40,40,40,40)

        # Fields
        self.title_input = QLineEdit(); self.title_input.setMinimumHeight(45)
        layout.addRow(QLabel("<b>Title:</b>"), self.title_input)

        self.desc_input = QLineEdit(); self.desc_input.setMinimumHeight(45)
        layout.addRow(QLabel("<b>Description:</b>"), self.desc_input)


        # self.setWindowTitle("Add Notice")
        # self.setFixedSize(400, 250)
        # layout = QFormLayout(self)

        # self.title_input = QLineEdit()
        # self.title_input.setPlaceholderText("Enter notice title")
        # layout.addRow("Title:", self.title_input)

        # self.desc_input = QLineEdit()
        # self.desc_input.setPlaceholderText("Enter notice description")
        # layout.addRow("Description:", self.desc_input)

        # Buttons
        btns = QHBoxLayout()
        save_btn = QPushButton("Save Record"); save_btn.setStyleSheet("background-color:#28a745;color:white;padding:15px 30px;font-size:18px;border-radius:10px;")
        save_btn.clicked.connect(self.save)
        cancel_btn = QPushButton("Cancel"); cancel_btn.setStyleSheet("background-color:#dc3545;color:white;padding:15px 30px;font-size:18px;border-radius:10px;")
        cancel_btn.clicked.connect(self.reject)
        btns.addStretch(); btns.addWidget(save_btn); btns.addWidget(cancel_btn); btns.addStretch()
        layout.addRow(btns)

        main_layout = QVBoxLayout(self); main_layout.addWidget(scroll)

    def save(self):
        title = self.title_input.text().strip()
        desc = self.desc_input.text().strip()
        if not title or not desc:
            QMessageBox.warning(self, "Missing Data", "Please fill all fields")
            return
        try:
            conn = sqlite3.connect(DB_NAME)
            cur = conn.cursor()
            cur.execute("INSERT INTO NoticeBoard (Title, Description) VALUES (?, ?)", (title, desc))
            conn.commit(); conn.close()
            QMessageBox.information(self, "Success", "Notice added successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))


class NoticePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)

        header = QLabel("Notice Board")
        header.setStyleSheet("font-size:32px;color:#10121a;margin-bottom:10px;")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        add_btn = QPushButton("Add Notice")
        add_btn.setStyleSheet("background-color:#28a745;color:white;padding:15px;font-size:18px;border-radius:10px;")
        add_btn.clicked.connect(self.add_notice)
        layout.addWidget(add_btn)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["ID", "Title", "Description"])
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table_widget)

        delete_btn = QPushButton("Delete Selected")
        delete_btn.setStyleSheet("background-color:#dc3545;color:white;padding:10px;")
        delete_btn.clicked.connect(self.delete_notice)
        layout.addWidget(delete_btn)

        self.load_data()

    def load_data(self):
        try:
            conn = sqlite3.connect(DB_NAME)
            data = conn.execute("SELECT N_id, Title, Description FROM NoticeBoard").fetchall()
            conn.close()
            self.table_widget.setRowCount(len(data))
            for r, record in enumerate(data):
                for c, val in enumerate(record):
                    self.table_widget.setItem(r, c, QTableWidgetItem(str(val)))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def add_notice(self):
        dialog = NoticeDialog(self)
        if dialog.exec():
            self.load_data()

    def delete_notice(self):
        row = self.table_widget.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Error", "Select a notice to delete")
            return
        n_id = self.table_widget.item(row, 0).text()
        reply = QMessageBox.question(self, "Confirm", "Delete this notice?")
        if reply == QMessageBox.Yes:
            try:
                conn = sqlite3.connect(DB_NAME)
                cur = conn.cursor()
                cur.execute("DELETE FROM NoticeBoard WHERE N_id=?", (n_id,))
                conn.commit(); conn.close()
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

# ---------------- Course Dialog ----------------
class CourseDialog(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add Course")
        self.setGeometry(200, 100, 600, 600)
        self.setStyleSheet("font-size:16px;background-color:#f8f9fa;")
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        scroll.setWidget(content)
        layout = QFormLayout(content)
        layout.setLabelAlignment(Qt.AlignRight)
        layout.setSpacing(25)
        layout.setContentsMargins(40,40,40,40)

        # Fields
        self.name_input = QLineEdit(); self.name_input.setMinimumHeight(45)
        layout.addRow(QLabel("<b>Course Name:</b>"), self.name_input)

        self.fee_input = QLineEdit(); self.fee_input.setMinimumHeight(45)
        layout.addRow(QLabel("<b>Course Fee:</b>"), self.fee_input)

        self.dur_input = QLineEdit(); self.dur_input.setMinimumHeight(45)
        layout.addRow(QLabel("<b>Course Duration:</b>"), self.dur_input)

        self.dept_combo = QComboBox(); self.dept_combo.setMinimumHeight(45)
        self.load_departments()
        layout.addRow(QLabel("<b>Department Name:</b>"), self.dept_combo)

        btns = QHBoxLayout()
        save_btn = QPushButton("Save Record"); save_btn.setStyleSheet("background-color:#28a745;color:white;padding:15px 30px;font-size:18px;border-radius:10px;")
        save_btn.clicked.connect(self.save_course)

        btns.addStretch(); btns.addWidget(save_btn); btns.addStretch()
        layout.addRow(btns)

        main_layout = QVBoxLayout(self); main_layout.addWidget(scroll)
   

        # self.name_input = QLineEdit(); self.fee_input=QLineEdit(); self.dept_combo=QComboBox()
        # self.load_departments()
        # layout.addRow("Course Name:",self.name_input)
        # layout.addRow("Course Fee:",self.fee_input)
        # layout.addRow("Department:",self.dept_combo)
        # btn=QPushButton("Save Course"); btn.clicked.connect(self.save_course)
        # layout.addRow(btn)

    def load_departments(self):
        conn = sqlite3.connect(DB_NAME)
        depts = conn.execute("SELECT D_Name FROM Department").fetchall()
        conn.close()
        self.dept_combo.clear()
        for d in depts:
            self.dept_combo.addItem(d[0])


    def save_course(self):
        name=self.name_input.text().strip(); fee=self.fee_input.text().strip();dur=self.dur_input.text().strip(); dept=self.dept_combo.currentText()
        if not all([name,fee,dur,dept]): QMessageBox.warning(self,"Error","Fill all fields"); return
        conn = sqlite3.connect(DB_NAME); cur=conn.cursor()
        cur.execute("SELECT D_id FROM Department WHERE D_Name=?",(dept,))
        d_id = cur.fetchone()[0]
        cur.execute("INSERT INTO Courses (C_name,C_Fee,C_Duration,D_id) VALUES (?,?,?,?)",(name,fee,dur,d_id))
        conn.commit(); conn.close(); QMessageBox.information(self,"Success","Course Added"); self.accept()

# ---------------- CRUD Page ----------------
class CRUDPage(QWidget):
    def __init__(self,table,columns,title):
        super().__init__()
        self.table,self.columns=table,columns
        layout=QVBoxLayout(self); layout.setContentsMargins(40,40,40,40)
        header=QLabel(title); header.setStyleSheet("font-size:32px;color:#10121a;margin-bottom:10px;"); header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        add_btn=QPushButton(f"Add New {title}"); add_btn.setStyleSheet("background-color:#28a745;color:white;padding:15px;font-size:18px;border-radius:10px;")
        add_btn.clicked.connect(self.add_record)
        layout.addWidget(add_btn)
        refresh_btn = QPushButton("Refresh List")
        refresh_btn.setStyleSheet(
            "background-color: #17a2b8; color: white; padding: 15px; font-size: 16px; border-radius: 10px;"
            )
        refresh_btn.clicked.connect(self.load_data)
        layout.addWidget(refresh_btn)

        self.table_widget=QTableWidget(); self.table_widget.setColumnCount(len(columns))
        self.table_widget.setHorizontalHeaderLabels(columns)
        self.table_widget.horizontalHeader().setStyleSheet("QHeaderView::section { font-size: 12px; padding: 2px; background-color: #f1f1f1; }")
        layout.addWidget(self.table_widget)
        delete_btn=QPushButton("Delete Selected"); delete_btn.setStyleSheet("background-color:#dc3545;color:white;padding:10px;")
        delete_btn.clicked.connect(self.delete_record)
        layout.addWidget(delete_btn)
        self.load_data()
        # main_window = self.window()
        # is_admin = getattr(main_window, "user_role", "viewer") == "admin"
        # add_btn.setEnabled(is_admin)
        # delete_btn.setEnabled(is_admin)

    def load_data(self):
        try:
            conn=sqlite3.connect(DB_NAME)
            data=conn.execute(f"SELECT {','.join(self.columns)} FROM {self.table}").fetchall()
            conn.close()
            self.table_widget.setRowCount(len(data))
            for r,record in enumerate(data):
                for c,val in enumerate(record):
                    self.table_widget.setItem(r,c,QTableWidgetItem(str(val)))
        except Exception as e: QMessageBox.critical(self,"Error",str(e))

    def add_record(self):
        if self.table=="Student": dialog=StudentDialog(self)
        elif self.table=="Teachers": dialog=TeacherDialog(self)
        elif self.table=="Courses": dialog=CourseDialog(self)
        elif self.table == "Department":dialog = DepartmentDialog(self)
        else: QMessageBox.information(self,"Info","Add form not implemented"); return
        if dialog.exec(): self.load_data()


    def delete_record(self):
        row=self.table_widget.currentRow()
        if row==-1: QMessageBox.warning(self,"Error","Select a record to delete"); return
        id_val=self.table_widget.item(row,0).text()
        reply=QMessageBox.question(self,"Confirm","Delete this record?")
        if reply==QMessageBox.Yes:
            try:
                conn=sqlite3.connect(DB_NAME); cur=conn.cursor()
                cur.execute(f"DELETE FROM {self.table} WHERE {self.columns[0]}=?",(id_val,))
                conn.commit(); conn.close(); self.load_data()
            except Exception as e: QMessageBox.critical(self,"Error",str(e))

# ---------------- Main Window ----------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.user_role = "viewer"
        self.setWindowTitle("School Management System"); self.setGeometry(50,50,1400,900)
        init_db()
        central=QWidget(); self.setCentralWidget(central)
        main_layout=QVBoxLayout(central)
        



        # Header
        header = QFrame()
        header.setStyleSheet("""
            background-color: qlineargradient(
                spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 #74ebd5, stop:1 #ACB6E5
                    );
                border-radius: 1px;
                padding: 1px;
                margin: 1px;
            """)
        h_layout=QVBoxLayout(header)
        welcome=QLabel("Welcome to School Management System"); welcome.setStyleSheet("font-size:28px;font-weight:bold;color:#212529;"); welcome.setAlignment(Qt.AlignCenter)
        date=QLabel(f"Today is {datetime.now().strftime('%A, %B %d, %Y')}"); date.setStyleSheet("font-size:18px;color:#495057;"); date.setAlignment(Qt.AlignCenter)
        h_layout.addWidget(welcome); h_layout.addWidget(date); main_layout.addWidget(header)

        # Scroll Content
        scroll=QScrollArea(); scroll.setWidgetResizable(True)
        content=QWidget(); scroll.setWidget(content); content_layout=QHBoxLayout(content); main_layout.addWidget(scroll)

        # Sidebar
        sidebar=QFrame(); sidebar.setFixedWidth(300); sidebar.setStyleSheet("background-color:#001f3f;padding:20px;border-radius:10px;")
        s_layout=QVBoxLayout(sidebar); s_layout.addWidget(QLabel("MENU",styleSheet="color:white;font-size:22px;font-weight:bold;margin-bottom:30px;"))
        menus=["Dashboard","Students","Teachers","Courses","Departments","Admission","Notice Board"]

        for m in menus:
            btn=QPushButton(m); btn.setStyleSheet("background-color:#007bff;color:white;padding:15px;margin:5px 0;border-radius:8px;font-size:16px;text-align:left;")
            btn.clicked.connect(lambda _,t=m:self.show_page(t)); s_layout.addWidget(btn)
        s_layout.addStretch(); content_layout.addWidget(sidebar)

        # Pages
        self.pages=QStackedWidget(); content_layout.addWidget(self.pages,1)
        dashboard=QWidget(); d_layout=QVBoxLayout(dashboard); d_layout.setContentsMargins(40,40,40,40)
        d_layout.addWidget(QLabel("Dashboard",styleSheet="font-size:36px;color:#2c3e50;margin:5px;",alignment=Qt.AlignCenter))
        conn=sqlite3.connect(DB_NAME)
        stats = {
            "students": conn.execute(
                "SELECT COUNT(*) FROM Student"
            ).fetchone()[0] if conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='Student'"
            ).fetchone() else 0,

            "teachers": conn.execute(
                "SELECT COUNT(*) FROM Teachers"
            ).fetchone()[0] if conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='Teachers'"
            ).fetchone() else 0,

            "courses": conn.execute(
                "SELECT COUNT(*) FROM Courses"
            ).fetchone()[0] if conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='Courses'"
            ).fetchone() else 0,

            "departments": conn.execute(
                "SELECT COUNT(*) FROM Department"
            ).fetchone()[0] if conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='Department'"
            ).fetchone() else 0
        }
        conn.close()
        cards=QHBoxLayout(); card_data=[("Total Students",str(stats['students']),"#28a745"),
                                        ("Total Teachers",str(stats['teachers']),"#17a2b8"),
                                        ("Total Courses",str(stats['courses']),"#ffc107"),
                                        ("Total Departments",str(stats['departments']),"#dc3545")]
        for t,v,c in card_data:
            card=QFrame(); card.setStyleSheet(f"background-color:{c};color:white;border-radius:20px;padding:10px;margin:5px;")
            cl=QVBoxLayout(card); cl.addWidget(QLabel(t,styleSheet="font-size:20px;")); cl.addWidget(QLabel(v,styleSheet="font-size:48px;font-weight:bold;"))
            cards.addWidget(card)
        d_layout.addLayout(cards)
        charts_cal_layout=QHBoxLayout(); charts_left=QVBoxLayout()
        charts_left.addWidget(ChartCanvas(chart_type='bar')); charts_left.addWidget(ChartCanvas(chart_type='line')); charts_cal_layout.addLayout(charts_left,stretch=3)
        calendar_frame=QFrame(); calendar_frame.setStyleSheet("background-color:white;border-radius:15px;padding:20px;")
        cal_layout=QVBoxLayout(calendar_frame); cal_layout.addWidget(QLabel("Calendar",styleSheet="font-size:24px;font-weight:bold;margin-bottom:10px;")); cal_layout.addWidget(QCalendarWidget())
        charts_cal_layout.addWidget(calendar_frame,stretch=1); d_layout.addLayout(charts_cal_layout); d_layout.addStretch()
        self.pages.addWidget(dashboard)

        # CRUD Pages
        self.pages.addWidget(
            CRUDPage(
            "Student",
            [
                "Student_id",
                "Name",
                "Father_Name",
                "Contact",
                "Email",
                "Address",
                "Gender",
                "D_id",
                "C_id"
            ],
            "Students"
        )
)

        self.pages.addWidget(
    CRUDPage(
        "Teachers",
        [
            "Teacher_id",
            "Name",
            "Father_Name",
            "Contact",
            "Email",
            "Address",
            "Qualification",
            "Subject",
            "Experience",
            "Gender",
            "C_id",
            "D_id"
        ],
        "Teachers"
    )
)

        self.pages.addWidget(CRUDPage("Courses",["C_id","C_name","C_Fee","C_Duration"],"Courses"))
        self.pages.addWidget(CRUDPage("Department",["D_id","D_Name","D_Head","D_Office"],"Departments"))
        self.pages.addWidget(NoticePage())

        # Admission
        admission=QWidget(); a_layout=QVBoxLayout(admission); a_layout.addWidget(QLabel("Admission Portal",styleSheet="font-size:36px;color:#2c3e50;margin:50px;"))
        btns=QHBoxLayout(); s_btn=QPushButton("Admit New Student"); s_btn.setStyleSheet("background-color:#28a745;color:white;padding:30px;font-size:24px;border-radius:15px;")
        s_btn.clicked.connect(lambda: StudentDialog(self).exec())
        t_btn=QPushButton("Admit New Teacher"); t_btn.setStyleSheet("background-color:#17a2b8;color:white;padding:30px;font-size:24px;border-radius:15px;")
        t_btn.clicked.connect(lambda: TeacherDialog(self).exec())
        btns.addStretch(); btns.addWidget(s_btn); btns.addWidget(t_btn); btns.addStretch(); a_layout.addLayout(btns); a_layout.addStretch()
        self.pages.addWidget(admission)

    def show_page(self,name):
        pages=["Dashboard","Students","Teachers","Courses","Departments","Notice Board","Admission"]
        self.pages.setCurrentIndex(pages.index(name))

if __name__=="__main__":
    app=QApplication(sys.argv)
    login = LoginDialog()
    if login.exec():
        window = MainWindow()
        window.user_role = login.role
        window.show()
        sys.exit(app.exec())
