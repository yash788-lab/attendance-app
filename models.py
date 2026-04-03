from database import db
from datetime import datetime
from flask_login import UserMixin

# --- 👤 LOGIN WRAPPER ---
class User(UserMixin):
    def __init__(self, id, role=None):
        self.id = id
        self.role = role

# --- 🏫 CLASS MODEL ---
class Class(db.Model):
    __tablename__ = 'classes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # Relationships
    students = db.relationship('Student', backref='class_info', lazy=True)

    def __repr__(self):
        return f'<Class {self.name}>'

# --- 📚 SUBJECT MODEL (New) ---
class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    
    # Relationship to marks
    marks = db.relationship('Mark', backref='subject', lazy=True)

    def __repr__(self):
        return f'<Subject {self.name}>'

# --- 📝 EXAM MODEL (New) ---
class Exam(db.Model):
    __tablename__ = 'exams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) # e.g., 'Midterm', 'Final'
    term = db.Column(db.String(50)) # e.g., '2025-2026'
    
    # Relationship to marks
    marks = db.relationship('Mark', backref='exam', lazy=True)

    def __repr__(self):
        return f'<Exam {self.name}>'

# --- 👨‍🎓 STUDENT MODEL ---
class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    # ✅ NEW FIELD for SMS Upgrade
    father_name = db.Column(db.String(100), nullable=True) 
    
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    roll_number = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    
    # Composite Unique Constraint (Prevents duplicate roll numbers in same class)
    __table_args__ = (
        db.UniqueConstraint('class_id', 'roll_number', name='_class_roll_uc'),
    )

    # Relationships
    attendance_records = db.relationship(
        'Attendance',
        backref='student',
        lazy=True,
        cascade='all, delete-orphan'
    )
    
    marks = db.relationship(
        'Mark', 
        backref='student', 
        lazy=True, 
        cascade='all, delete-orphan'
    )

    notifications = db.relationship(
        'Notification', 
        backref='student', 
        lazy=True, 
        cascade='all, delete-orphan'
    )
    
    def __repr__(self):
        return f'<Student {self.name} - Roll {self.roll_number}>'
    
    def get_attendance_percentage(self, start_date=None, end_date=None):
        """Calculate attendance percentage for a given date range"""
        query = Attendance.query.filter_by(student_id=self.id)
        if start_date:
            query = query.filter(Attendance.date >= start_date)
        if end_date:
            query = query.filter(Attendance.date <= end_date)
        
        records = query.all()
        if not records:
            return 0.0
        
        present_count = sum(1 for record in records if record.status == 'present')
        total_count = len(records)
        return round((present_count / total_count) * 100, 2)

# --- 📊 MARKS MODEL (New) ---
class Mark(db.Model):
    __tablename__ = 'marks'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False)
    
    marks_obtained = db.Column(db.Float, nullable=False)
    max_marks = db.Column(db.Float, default=100.0)
    remarks = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Ensures a student only has ONE mark entry per subject per exam
    __table_args__ = (
        db.UniqueConstraint('student_id', 'subject_id', 'exam_id', name='_student_subject_exam_uc'),
    )

# --- 📅 ATTENDANCE MODEL ---
class Attendance(db.Model):
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    status = db.Column(db.String(20), nullable=False)  # present, absent, late
    remarks = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    
    __table_args__ = (
        db.UniqueConstraint('student_id', 'date', name='_student_date_uc'),
    )
    
    def __repr__(self):
        return f'<Attendance {self.student_id} - {self.date}>'

# --- 🔔 NOTIFICATION MODEL (New) ---
class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=True) # Null = Broadcast
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)