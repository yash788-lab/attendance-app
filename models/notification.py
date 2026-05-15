from database import db
from datetime import datetime


class Notification(db.Model):
    """In-app notification. recipient_user_id=None means broadcast to all users."""
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)

    # NULL = broadcast to all; set to a User.id to target a specific user
    recipient_user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=True,
        index=True
    )

    title = db.Column(db.String(200), nullable=False, default='Notification')
    message = db.Column(db.Text, nullable=False)

    # 'info', 'warning', 'success', 'alert'
    notification_type = db.Column(db.String(20), default='info', nullable=False)

    is_read = db.Column(db.Boolean, default=False, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # Relationship back to User
    recipient = db.relationship('User', back_populates='notifications', foreign_keys=[recipient_user_id])

    def __repr__(self):
        target = f'user:{self.recipient_user_id}' if self.recipient_user_id else 'broadcast'
        return f'<Notification [{target}] "{self.title}">'
