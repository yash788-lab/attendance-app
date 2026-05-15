from database import db
from datetime import datetime


class Student(db.Model):
    """Student profile — linked one-to-one with a User whose role='student'.
    user_id is nullable during migration; all students get a User after Phase 2 seeding.
    """
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)

    # Link to auth User (nullable during migration, required after seeding)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='SET NULL'),
        unique=True,
        nullable=True,
        index=True
    )

    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    father_name = db.Column(db.String(100))
    roll_number = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('class_id', 'roll_number', name='_class_roll_uc'),
    )

    # Relationships
    user = db.relationship('User', back_populates='student_profile')
    class_info = db.relationship('Class', back_populates='students')
    attendance_records = db.relationship(
        'Attendance', back_populates='student',
        lazy=True, cascade='all, delete-orphan'
    )
    marks = db.relationship(
        'Mark', back_populates='student',
        lazy=True, cascade='all, delete-orphan'
    )

    # --- Helpers ---
    def get_attendance_percentage(self, start_date=None, end_date=None) -> float:
        """Calculate attendance percentage, optionally filtered by date range."""
        from models.attendance import Attendance
        query = Attendance.query.filter_by(student_id=self.id)
        if start_date:
            query = query.filter(Attendance.date >= start_date)
        if end_date:
            query = query.filter(Attendance.date <= end_date)
        records = query.all()
        if not records:
            return 0.0
        present = sum(1 for r in records if r.status == 'present')
        return round((present / len(records)) * 100, 2)

    def __repr__(self):
        return f'<Student {self.name} Roll:{self.roll_number}>'
