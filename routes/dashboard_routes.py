from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime

from models.student import Student
from models.notification import Notification
from models.academic import Class, Exam, Subject
from models.attendance import Attendance
from models.marks import Mark
from database import db
from . import main


@main.route('/')
@login_required
def index():
    if current_user.role == 'admin':
        return redirect(url_for('main.admin_dashboard'))

    if current_user.role == 'teacher':
        total_students = Student.query.count()
        total_classes = Class.query.count()
        pending_notifications = Notification.query.filter(
            (Notification.recipient_user_id == current_user.id) |
            (Notification.recipient_user_id == None)  # noqa: E711
        ).filter_by(is_read=False).count()
        return render_template(
            'teacher/dashboard.html',
            total_students=total_students,
            total_classes=total_classes,
            pending_notifications=pending_notifications,
        )

    # --- Student dashboard ---
    student = current_user.student_profile
    if not student:
        from flask import abort
        abort(403)

    att_percent = student.get_attendance_percentage()

    # Recent attendance (last 10)
    recent_records = (
        Attendance.query
        .filter_by(student_id=student.id)
        .order_by(Attendance.date.desc())
        .limit(10)
        .all()
    )

    # Optional date-filtered attendance
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

    # Notifications (personal + broadcast)
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

    # Marks summary
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