from database import db
from models.notification import Notification
from datetime import datetime


class NotificationService:
    """Centralized service for creating and managing in-app notifications.

    Architecture notes:
    - send_broadcast()   → creates one Notification row with recipient_user_id=None
    - send_to_user()     → creates one row targeted at a specific user
    - send_to_class()    → creates one row per student in the class

    Future-ready: each method accepts an optional `channels` kwarg so we can
    plug in email / WhatsApp / push adapters later without changing call-sites.
    """

    # ── Core senders ──────────────────────────────────────────────────────────

    @staticmethod
    def send_broadcast(title: str, message: str, notification_type: str = 'info'):
        """Send a notification visible to every logged-in user."""
        n = Notification(
            recipient_user_id=None,
            title=title,
            message=message,
            notification_type=notification_type,
            is_read=False,
            timestamp=datetime.utcnow(),
        )
        db.session.add(n)
        db.session.commit()
        return n

    @staticmethod
    def send_to_user(user_id: int, title: str, message: str, notification_type: str = 'info'):
        """Send a notification to one specific user."""
        n = Notification(
            recipient_user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            is_read=False,
            timestamp=datetime.utcnow(),
        )
        db.session.add(n)
        db.session.commit()
        return n

    @staticmethod
    def send_to_class(class_id: int, title: str, message: str, notification_type: str = 'info'):
        """Send a notification to every student in a class who has a User account."""
        from models.student import Student
        students = Student.query.filter_by(class_id=class_id).all()
        notifications = []
        for student in students:
            if student.user_id:
                n = Notification(
                    recipient_user_id=student.user_id,
                    title=title,
                    message=message,
                    notification_type=notification_type,
                    is_read=False,
                    timestamp=datetime.utcnow(),
                )
                db.session.add(n)
                notifications.append(n)
        db.session.commit()
        return notifications

    # ── Convenience triggers (called by routes/services) ──────────────────────

    @staticmethod
    def notify_homework_assigned(class_id: int, subject_name: str, teacher_name: str):
        """Triggered when a teacher assigns new homework to a class."""
        NotificationService.send_to_class(
            class_id=class_id,
            title='New Homework Assigned',
            message=f'New homework for {subject_name} has been assigned by {teacher_name}.',
            notification_type='info',
        )

    @staticmethod
    def notify_marks_published(class_id: int, exam_name: str, subject_name: str):
        """Triggered when marks are saved/updated for a class."""
        NotificationService.send_to_class(
            class_id=class_id,
            title='Marks Updated',
            message=f'Marks for {subject_name} ({exam_name}) have been updated.',
            notification_type='success',
        )

    @staticmethod
    def notify_announcement(title: str, message: str):
        """Triggered when admin posts a new announcement."""
        NotificationService.send_broadcast(
            title=f'📢 {title}',
            message=message,
            notification_type='info',
        )
