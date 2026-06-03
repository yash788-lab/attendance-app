from flask import render_template
from flask_login import login_required, current_user

from models.notification import Notification
from database import db
from . import teacher_bp


@teacher_bp.route('/notifications')
@login_required
def view_notifications():
    # Fetch personal + broadcast notifications
    notifications = (
        Notification.query
        .filter(
            (Notification.recipient_user_id == current_user.id) |
            (Notification.recipient_user_id == None)
        )
        .order_by(Notification.timestamp.desc())
        .all()
    )

    # Mark unread as read
    for n in notifications:
        if not n.is_read and (
            n.recipient_user_id == current_user.id or n.recipient_user_id is None
        ):
            n.is_read = True
    db.session.commit()

    return render_template('shared/notifications.html', notifications=notifications)