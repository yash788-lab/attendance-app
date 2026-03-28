from database import db
from datetime import datetime
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id, role=None):
        self.id = id
        self.role = role

class Class(db.Model):
    __tablename__ = 'classes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    students = db.relationship('Student', backref='class_obj', lazy=True)

    def __repr__(self):
        return f'<Class {self.name}>'

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)

    # ✅ BASIC INFO
    name = db.Column(db.String(100), nullable=False)

    # ✅ NEW FIELD (IMPORTANT)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)

    # ❗ REMOVED unique=True (IMPORTANT CHANGE)
    roll_number = db.Column(db.String(50), nullable=False)

    # Used as password
    email = db.Column(db.String(100), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ✅ COMPOSITE UNIQUE CONSTRAINT
    __table_args__ = (
        db.UniqueConstraint('class_id', 'roll_number', name='_class_roll_uc'),
    )

    attendance_records = db.relationship(
        'Attendance',
        backref='student',
        lazy=True,
        cascade='all, delete-orphan'
    )
    
    def __repr__(self):
        return f'<Student {self.name} - Class {self.class_obj.name} Roll {self.roll_number}>'
    
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
        return f'<Attendance {self.student_id} - {self.date} - {self.status}>'