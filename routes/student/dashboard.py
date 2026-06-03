from flask import render_template, request, abort
from flask_login import login_required, current_user
from datetime import datetime
from models.attendance import Attendance
from models.marks import Mark
from models.academic import Subject, Exam
from models.notification import Notification
from . import student_bp
from utils.decorators import student_required

@student_bp.route('/dashboard')
@login_required
@student_required
def dashboard():
    student = current_user.student_profile
    if not student:
        abort(403)

    att_percent = student.get_attendance_percentage()

    recent_records = (
        Attendance.query
        .filter_by(student_id=student.id)
        .order_by(Attendance.date.desc())
        .limit(10)
        .all()
    )

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    att_query = Attendance.query.filter_by(student_id=student.id)
    if start_date:
        att_query = att_query.filter(
            Attendance.date >= datetime.strptime(start_date, '%Y-%m-%d').date()
        )
    if end_date:
        att_query = att_query.filter(
            Attendance.date <= datetime.strptime(end_date, '%Y-%m-%d').date()
        )
    records = att_query.order_by(Attendance.date.desc()).all()

    notifications = (
        Notification.query
        .filter(
            (Notification.recipient_user_id == current_user.id) |
            (Notification.recipient_user_id == None)
        )
        .order_by(Notification.timestamp.desc())
        .limit(5)
        .all()
    )

    marks = (
        Mark.query
        .filter_by(student_id=student.id)
        .join(Subject).join(Exam)
        .order_by(Exam.name, Subject.name)
        .all()
    )

    return render_template(
        'student/dashboard.html',
        student=student,
        att_percent=att_percent,
        recent_records=recent_records,
        records=records,
        notifications=notifications,
        marks=marks,
        start_date=start_date,
        end_date=end_date,
    )
