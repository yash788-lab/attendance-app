from flask import render_template
from flask_login import login_required, current_user
from models.student import Student
from models.academic import Class
from models.notification import Notification
from . import teacher_bp
from utils.decorators import teacher_required

@teacher_bp.route('/dashboard')
@login_required
@teacher_required
def dashboard():
    total_students = Student.query.count()
    total_classes = Class.query.count()
    pending_notifications = Notification.query.filter(
        (Notification.recipient_user_id == current_user.id) |
        (Notification.recipient_user_id == None)
    ).filter_by(is_read=False).count()
    
    return render_template(
        'teacher/dashboard.html',
        total_students=total_students,
        total_classes=total_classes,
        pending_notifications=pending_notifications,
    )
