from database import db
from datetime import datetime, date


class Attendance(db.Model):
    """Daily attendance record for a student."""
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    status = db.Column(db.String(20), nullable=False)   # present, absent, late
    remarks = db.Column(db.String(200))
    marked_by = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('student_id', 'date', name='_student_date_uc'),
    )

    # Relationships
    student = db.relationship('Student', back_populates='attendance_records')
    marker = db.relationship(
        'Teacher', back_populates='attendance_marked', foreign_keys=[marked_by]
    )

    def __repr__(self):
        return f'<Attendance student:{self.student_id} {self.date} [{self.status}]>'
