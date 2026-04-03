from flask import render_template
from flask_login import login_required, current_user

from models import Notification
from . import main


@main.route('/notifications')
@login_required
def view_notifications():
    if current_user.role == 'student':
        notifications = Notification.query.filter(
            (Notification.student_id == int(current_user.id)) |
            (Notification.student_id == None)
        ).order_by(Notification.timestamp.desc()).all()
    else:
        notifications = Notification.query.order_by(
            Notification.timestamp.desc()
        ).all()

    return render_template('notifications.html', notifications=notifications)