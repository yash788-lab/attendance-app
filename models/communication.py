from database import db
from datetime import datetime


class Announcement(db.Model):
    """School-wide or class-specific announcement created by admin or teacher."""
    __tablename__ = 'announcements'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # 'all', 'student', 'teacher' — NULL means all roles
    target_role = db.Column(db.String(20), default='all')
    # NULL = school-wide; set class_id to target a specific class
    target_class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=True)
    is_pinned = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    creator = db.relationship('User', back_populates='announcements', foreign_keys=[created_by])
    target_class = db.relationship(
        'Class', back_populates='announcements', foreign_keys=[target_class_id]
    )

    def __repr__(self):
        return f'<Announcement "{self.title}">'


class Event(db.Model):
    """A school event or calendar entry."""
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(200))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    creator = db.relationship('User', back_populates='events', foreign_keys=[created_by])

    def __repr__(self):
        return f'<Event "{self.title}" on {self.event_date}>'


class Poll(db.Model):
    """A poll created by admin or teacher."""
    __tablename__ = 'polls'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    creator = db.relationship('User', back_populates='polls', foreign_keys=[created_by])
    options = db.relationship(
        'PollOption', back_populates='poll',
        lazy=True, cascade='all, delete-orphan'
    )
    votes = db.relationship(
        'PollVote', back_populates='poll',
        lazy=True, cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<Poll "{self.question[:40]}">'


class PollOption(db.Model):
    """One answer choice within a Poll."""
    __tablename__ = 'poll_options'

    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(
        db.Integer, db.ForeignKey('polls.id', ondelete='CASCADE'), nullable=False
    )
    option_text = db.Column(db.String(300), nullable=False)

    # Relationships
    poll = db.relationship('Poll', back_populates='options')
    votes = db.relationship('PollVote', back_populates='option', lazy=True)

    def __repr__(self):
        return f'<PollOption "{self.option_text[:30]}">'


class PollVote(db.Model):
    """A user's single vote in a poll (one vote per user per poll enforced)."""
    __tablename__ = 'poll_votes'

    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(
        db.Integer, db.ForeignKey('polls.id', ondelete='CASCADE'), nullable=False
    )
    option_id = db.Column(
        db.Integer, db.ForeignKey('poll_options.id', ondelete='CASCADE'), nullable=False
    )
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('poll_id', 'user_id', name='_poll_user_vote_uc'),
    )

    # Relationships
    poll = db.relationship('Poll', back_populates='votes')
    option = db.relationship('PollOption', back_populates='votes')
    voter = db.relationship('User', back_populates='poll_votes')

    def __repr__(self):
        return f'<PollVote user:{self.user_id} poll:{self.poll_id}>'
