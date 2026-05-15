from database import db
from datetime import datetime


class Mark(db.Model):
    """Marks scored by a student in a subject for a specific exam."""
    __tablename__ = 'marks'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False)
    marks_obtained = db.Column(db.Float, nullable=False)
    max_marks = db.Column(db.Float, default=100.0, nullable=False)
    remarks = db.Column(db.String(200))
    entered_by = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('student_id', 'subject_id', 'exam_id', name='_student_subject_exam_uc'),
    )

    # Relationships
    student = db.relationship('Student', back_populates='marks')
    subject = db.relationship('Subject', back_populates='marks')
    exam = db.relationship('Exam', back_populates='marks')
    entered_by_teacher = db.relationship(
        'Teacher', back_populates='marks_entered', foreign_keys=[entered_by]
    )

    @property
    def percentage(self) -> float:
        if self.max_marks and self.max_marks > 0:
            return round((self.marks_obtained / self.max_marks) * 100, 2)
        return 0.0

    @property
    def grade(self) -> str:
        p = self.percentage
        if p >= 90: return 'A+'
        if p >= 80: return 'A'
        if p >= 70: return 'B+'
        if p >= 60: return 'B'
        if p >= 50: return 'C'
        if p >= 40: return 'D'
        return 'F'

    def __repr__(self):
        return f'<Mark student:{self.student_id} sub:{self.subject_id} exam:{self.exam_id}>'
