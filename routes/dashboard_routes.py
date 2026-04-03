from flask import render_template
from flask_login import login_required, current_user
from models import Student, Notification, Class
from database import db
from . import main

@main.route('/')
@login_required
def index():
    if current_user.role == 'teacher':
        return render_template('index.html', Student=Student, Class=Class, Notification=Notification)
    student = db.session.get(Student, int(current_user.id))
    att_percent = student.get_attendance_percentage()

    notifs = Notification.query.filter(
        (Notification.student_id == student.id) |
        (Notification.student_id == None)
    ).order_by(Notification.timestamp.desc()).limit(3).all()

    return render_template('student_dashboard.html', student=student, att_percent=att_percent, notifs=notifs)