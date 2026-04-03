from flask import render_template, request
from flask_login import login_required, current_user
from models import Student, Notification, Class, Attendance, Mark, Subject, Exam
from database import db
from . import main

@main.route('/')
@login_required
def index():
    if current_user.role == 'teacher':
        return render_template('index.html', Student=Student, Class=Class, Notification=Notification)
    student = db.session.get(Student, int(current_user.id))
    att_percent = student.get_attendance_percentage()

    # Recent attendance records (last 10)
    recent_records = Attendance.query.filter_by(student_id=student.id)\
        .order_by(Attendance.date.desc()).limit(10).all()

    # Full attendance with optional date filtering
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    att_query = Attendance.query.filter_by(student_id=student.id)
    if start_date:
        from datetime import datetime
        att_query = att_query.filter(Attendance.date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        from datetime import datetime
        att_query = att_query.filter(Attendance.date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    records = att_query.order_by(Attendance.date.desc()).all()

    # Notifications
    notifications = Notification.query.filter(
        (Notification.student_id == student.id) |
        (Notification.student_id == None)
    ).order_by(Notification.timestamp.desc()).limit(5).all()

    # Marks for student dashboard summary
    marks = Mark.query.filter_by(student_id=student.id)\
        .join(Subject).join(Exam)\
        .order_by(Exam.name, Subject.name).all()

    return render_template(
        'student_dashboard.html',
        student=student,
        att_percent=att_percent,
        recent_records=recent_records,
        records=records,
        notifications=notifications,
        marks=marks,
        start_date=start_date,
        end_date=end_date
    )