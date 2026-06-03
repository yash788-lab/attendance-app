from database import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    """Central authentication model. Every person in the system has a User record."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'teacher', 'student'
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    must_change_password = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Role-specific profiles (one-to-one)
    admin_profile = db.relationship(
        'Admin', back_populates='user', uselist=False, cascade='all, delete-orphan'
    )
    teacher_profile = db.relationship(
        'Teacher', back_populates='user', uselist=False, cascade='all, delete-orphan'
    )
    student_profile = db.relationship(
        'Student', back_populates='user', uselist=False
    )

    # Notifications addressed to this user
    notifications = db.relationship(
        'Notification',
        back_populates='recipient',
        lazy='dynamic',
        foreign_keys='Notification.recipient_user_id',
        cascade='all, delete-orphan'
    )

    # Content created by this user
    announcements = db.relationship('Announcement', back_populates='creator', lazy='dynamic')
    events = db.relationship('Event', back_populates='creator', lazy='dynamic')
    polls = db.relationship('Poll', back_populates='creator', lazy='dynamic')
    poll_votes = db.relationship('PollVote', back_populates='voter', lazy='dynamic')

    # --- Auth helpers ---
    def set_password(self, raw_password: str):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password_hash(self.password_hash, raw_password)

    def get_profile(self):
        """Returns the role-specific profile (Admin / Teacher / Student)."""
        mapping = {
            'admin': self.admin_profile,
            'teacher': self.teacher_profile,
            'student': self.student_profile,
        }
        return mapping.get(self.role)

    def __repr__(self):
        return f'<User {self.email} [{self.role}]>'

