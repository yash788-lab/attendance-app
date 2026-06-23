# models/__init__.py
# Central import hub — import all models so SQLAlchemy can build the full relationship graph
# and Alembic can detect all tables.

from models.user import User
from models.admin import Admin
from models.teacher import Teacher
from models.student import Student
from models.academic import Class, Subject, ClassSubject, Exam
from models.attendance import Attendance
from models.marks import Mark
from models.homework import Homework
from models.communication import Announcement, Event, Poll, PollOption, PollVote
from models.notification import Notification
from models.site_config import SiteConfig

__all__ = [
    'User', 'Admin',
    'Teacher',
    'Student',
    'Class', 'Subject', 'ClassSubject', 'Exam',
    'Attendance',
    'Mark',
    'Homework',
    'Announcement', 'Event', 'Poll', 'PollOption', 'PollVote',
    'Notification',
    'SiteConfig',
]
