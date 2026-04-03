from flask import render_template, request
from flask_login import login_required, current_user
from datetime import datetime

from models import Student, Attendance, Class
from . import main


@main.route('/attendance/mark', methods=['GET', 'POST'])
@login_required
def mark_attendance():
    # 1. Get filters
    class_id = request.args.get('class_id', type=int)
    student_id = request.args.get('student_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # 2. Base Query
    query = Attendance.query

    # 3. Role-Based Filtering
    if current_user.role == 'student':
        query = query.filter(Attendance.student_id == int(current_user.id))
    else:
        if class_id:
            query = query.join(Student).filter(Student.class_id == class_id)

        if student_id:
            query = query.filter(Attendance.student_id == student_id)

    # 4. Convert dates properly ✅
    if start_date:
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            query = query.filter(Attendance.date >= start_date_obj)
        except ValueError:
            pass

    if end_date:
        try:
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            query = query.filter(Attendance.date <= end_date_obj)
        except ValueError:
            pass

    # 5. Execute
    records = query.order_by(Attendance.date.desc()).all()

    # 6. Dropdown Data
    classes = []
    students = []

    if current_user.role == 'teacher':
        classes = Class.query.all()

        if class_id:
            students = Student.query.filter_by(class_id=class_id).all()
        else:
            students = Student.query.all()

    return render_template(
        'view_attendance.html',
        records=records,
        classes=classes,
        students=students,
        start_date=start_date,
        end_date=end_date
    )

@main.route('/attendance/view')
@login_required
def view_attendance():
    return "View Attendance Stub"