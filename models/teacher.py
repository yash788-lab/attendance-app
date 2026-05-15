from database import db
from datetime import datetime


class Teacher(db.Model):
    """Teacher profile — linked one-to-one with a User whose role='teacher'.
    is_approved controls whether the teacher can log in (set by Admin after review).
    """
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        unique=True,
        nullable=False
    )
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    is_approved = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='teacher_profile')
    class_subjects = db.relationship('ClassSubject', back_populates='teacher', lazy='dynamic')
    attendance_marked = db.relationship(
        'Attendance',
        back_populates='marker',
        lazy='dynamic',
        foreign_keys='Attendance.marked_by'
    )
    marks_entered = db.relationship(
        'Mark',
        back_populates='entered_by_teacher',
        lazy='dynamic',
        foreign_keys='Mark.entered_by'
    )
    homework_set = db.relationship('Homework', back_populates='teacher', lazy='dynamic')

    def __repr__(self):
        return f'<Teacher {self.name} [approved={self.is_approved}]>'
