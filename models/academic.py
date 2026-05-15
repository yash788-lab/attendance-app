from database import db
from datetime import datetime


class Class(db.Model):
    """Represents a school class/section, e.g. '10-A', '12-Science'."""
    __tablename__ = 'classes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    academic_year = db.Column(db.String(20), default='2025-26')

    # Relationships
    students = db.relationship('Student', back_populates='class_info', lazy=True)
    class_subjects = db.relationship('ClassSubject', back_populates='class_', lazy=True)
    homework_list = db.relationship('Homework', back_populates='class_', lazy=True)
    announcements = db.relationship(
        'Announcement', back_populates='target_class', lazy=True,
        foreign_keys='Announcement.target_class_id'
    )

    def __repr__(self):
        return f'<Class {self.name}>'


class Subject(db.Model):
    """A subject taught in the school, e.g. Mathematics, Physics."""
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=True)

    # Relationships
    class_subjects = db.relationship('ClassSubject', back_populates='subject', lazy=True)
    marks = db.relationship('Mark', back_populates='subject', lazy=True)
    homework_list = db.relationship('Homework', back_populates='subject', lazy=True)

    def __repr__(self):
        return f'<Subject {self.name}>'


class ClassSubject(db.Model):
    """Junction: which Subject is taught in which Class, and by which Teacher."""
    __tablename__ = 'class_subjects'

    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=True)

    __table_args__ = (
        db.UniqueConstraint('class_id', 'subject_id', name='_class_subject_uc'),
    )

    # Relationships
    class_ = db.relationship('Class', back_populates='class_subjects')
    subject = db.relationship('Subject', back_populates='class_subjects')
    teacher = db.relationship('Teacher', back_populates='class_subjects')

    def __repr__(self):
        return f'<ClassSubject class:{self.class_id} sub:{self.subject_id}>'


class Exam(db.Model):
    """An exam event, e.g. Mid-Term 2025-26."""
    __tablename__ = 'exams'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    term = db.Column(db.String(50), nullable=False, default='2025-26')
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    marks = db.relationship('Mark', back_populates='exam', lazy=True)

    def __repr__(self):
        return f'<Exam {self.name} [{self.term}]>'
