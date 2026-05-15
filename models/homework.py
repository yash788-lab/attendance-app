from database import db
from datetime import datetime


class Homework(db.Model):
    """Homework assignment set by a teacher for a class+subject."""
    __tablename__ = 'homework'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    due_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    subject = db.relationship('Subject', back_populates='homework_list')
    class_ = db.relationship('Class', back_populates='homework_list')
    teacher = db.relationship('Teacher', back_populates='homework_set')

    def __repr__(self):
        return f'<Homework "{self.title}" class:{self.class_id}>'
