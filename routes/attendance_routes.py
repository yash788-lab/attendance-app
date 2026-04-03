from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime, date

from models import Student, Attendance, Class
from database import db
from . import main
from utils.decorators import teacher_required


@main.route('/attendance/mark', methods=['GET', 'POST'])
@login_required
@teacher_required
def mark_attendance():
    classes = Class.query.all()

    # Get selected date (default: today)
    date_str = request.args.get('date') or request.form.get('date')
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = date.today()
    else:
        selected_date = date.today()

    # Get selected class
    selected_class_id = request.args.get('class_id') or request.form.get('class_id')

    # Fetch students for the selected class
    students = []
    existing_attendance = {}

    if selected_class_id:
        students = Student.query.filter_by(class_id=selected_class_id)\
            .order_by(Student.roll_number).all()

        # Load any existing attendance for this date
        for s in students:
            record = Attendance.query.filter_by(
                student_id=s.id,
                date=selected_date
            ).first()
            if record:
                existing_attendance[s.id] = record
    else:
        # If no class selected, show all students
        students = Student.query.order_by(Student.roll_number).all()
        for s in students:
            record = Attendance.query.filter_by(
                student_id=s.id,
                date=selected_date
            ).first()
            if record:
                existing_attendance[s.id] = record

    # Handle POST - save attendance
    if request.method == 'POST':
        for s in students:
            status = request.form.get(f'status_{s.id}')
            remarks = request.form.get(f'remarks_{s.id}', '')

            if status:
                # Check if record already exists
                existing = Attendance.query.filter_by(
                    student_id=s.id,
                    date=selected_date
                ).first()

                if existing:
                    existing.status = status
                    existing.remarks = remarks
                else:
                    db.session.add(Attendance(
                        student_id=s.id,
                        date=selected_date,
                        status=status,
                        remarks=remarks
                    ))

        db.session.commit()
        flash('Attendance saved successfully!', 'success')
        return redirect(url_for('main.mark_attendance',
                                date=selected_date.strftime('%Y-%m-%d'),
                                class_id=selected_class_id or ''))

    return render_template(
        'mark_attendance.html',
        classes=classes,
        students=students,
        selected_date=selected_date,
        selected_class_id=selected_class_id,
        existing_attendance=existing_attendance
    )


@main.route('/attendance/view')
@login_required
def view_attendance():
    """Student-facing attendance view"""
    if current_user.role == 'student':
        records = Attendance.query.filter_by(student_id=int(current_user.id))\
            .order_by(Attendance.date.desc()).all()
    else:
        records = Attendance.query.order_by(Attendance.date.desc()).limit(100).all()

    return render_template('view_attendance.html',
                           records=records,
                           classes=[],
                           students=[],
                           start_date=None,
                           end_date=None)