from database import db
from models.homework import Homework
from models.academic import Class, Subject
from datetime import datetime, timedelta


class HomeworkService:
    """Service layer for homework CRUD and auto-cleanup (7-day retention)."""

    @staticmethod
    def create(title: str, description: str, class_id: int,
               subject_id: int, teacher_id: int, due_date=None) -> Homework:
        hw = Homework(
            title=title,
            description=description,
            class_id=class_id,
            subject_id=subject_id,
            teacher_id=teacher_id,
            due_date=due_date,
            created_at=datetime.utcnow(),
        )
        db.session.add(hw)
        db.session.commit()
        return hw

    @staticmethod
    def get_for_class(class_id: int):
        """Return active (≤7 days old) homework for a class, newest first."""
        cutoff = datetime.utcnow() - timedelta(days=7)
        return (
            Homework.query
            .filter_by(class_id=class_id)
            .filter(Homework.created_at >= cutoff)
            .order_by(Homework.created_at.desc())
            .all()
        )

    @staticmethod
    def get_for_teacher(teacher_id: int):
        """Return active (≤7 days old) homework assigned by this teacher."""
        cutoff = datetime.utcnow() - timedelta(days=7)
        return (
            Homework.query
            .filter_by(teacher_id=teacher_id)
            .filter(Homework.created_at >= cutoff)
            .order_by(Homework.created_at.desc())
            .all()
        )

    @staticmethod
    def delete(hw_id):
        """Delete homework by ID."""
        hw = db.session.get(Homework, hw_id)
        if hw:
            db.session.delete(hw)
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_all_active():
        """Return all active homework across all classes."""
        cutoff = datetime.utcnow() - timedelta(days=7)
        return (
            Homework.query
            .filter(Homework.created_at >= cutoff)
            .order_by(Homework.created_at.desc())
            .all()
        )

    @staticmethod
    def purge_old():
        """Delete homework older than 7 days. Call from a CLI command or scheduled task."""
        cutoff = datetime.utcnow() - timedelta(days=7)
        deleted = Homework.query.filter(Homework.created_at < cutoff).delete()
        db.session.commit()
        return deleted
