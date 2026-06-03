from database import db
from models.communication import Announcement, Event, Poll, PollOption
from models.notification import Notification
from datetime import datetime


class CommunicationService:
    """Service for admin-managed CMS content: Announcements, Events, Polls."""

    # ── Announcements ─────────────────────────────────────────────────────────

    @staticmethod
    def create_announcement(title, content, created_by_user_id,
                            target_role='all', target_class_id=None, is_pinned=False):
        ann = Announcement(
            title=title,
            content=content,
            created_by=created_by_user_id,
            target_role=target_role,
            target_class_id=target_class_id or None,
            is_pinned=is_pinned,
            created_at=datetime.utcnow(),
        )
        db.session.add(ann)
        db.session.commit()
        return ann

    @staticmethod
    def delete_announcement(ann_id):
        ann = db.session.get(Announcement, ann_id)
        if ann:
            db.session.delete(ann)
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_public_announcements(limit=5):
        """Pinned first, then newest — used on the public homepage."""
        return (
            Announcement.query
            .filter_by(target_role='all')
            .order_by(Announcement.is_pinned.desc(), Announcement.created_at.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_all_announcements():
        return (
            Announcement.query
            .order_by(Announcement.is_pinned.desc(), Announcement.created_at.desc())
            .all()
        )

    # ── Events ────────────────────────────────────────────────────────────────

    @staticmethod
    def create_event(title, description, event_date, location, created_by_user_id):
        ev = Event(
            title=title,
            description=description,
            event_date=event_date,
            location=location,
            created_by=created_by_user_id,
            created_at=datetime.utcnow(),
        )
        db.session.add(ev)
        db.session.commit()
        return ev

    @staticmethod
    def delete_event(event_id):
        ev = db.session.get(Event, event_id)
        if ev:
            db.session.delete(ev)
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_upcoming_events(limit=5):
        today = datetime.utcnow().date()
        return (
            Event.query
            .filter(Event.event_date >= today)
            .order_by(Event.event_date.asc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_all_events():
        return Event.query.order_by(Event.event_date.desc()).all()

    # ── Polls ─────────────────────────────────────────────────────────────────

    @staticmethod
    def create_poll(question, options_text, created_by_user_id, expires_at=None):
        poll = Poll(
            question=question,
            created_by=created_by_user_id,
            expires_at=expires_at,
            is_active=True,
        )
        db.session.add(poll)
        db.session.flush()
        for text in options_text:
            if text.strip():
                db.session.add(PollOption(poll_id=poll.id, option_text=text.strip()))
        db.session.commit()
        return poll

    @staticmethod
    def delete_poll(poll_id):
        poll = db.session.get(Poll, poll_id)
        if poll:
            db.session.delete(poll)
            db.session.commit()
            return True
        return False
