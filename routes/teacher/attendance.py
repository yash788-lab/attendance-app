from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime, date
from collections import defaultdict

from models.student import Student
from models.attendance import Attendance
from models.academic import Class
from database import db
from . import teacher_bp
from utils.decorators import admin_or_teacher_required, student_required


@teacher_bp.route('/attendance/mark', methods=['GET', 'POST'])
@login_required
@admin_or_teacher_required
def mark_attendance():
    classes = Class.query.order_by(Class.name).all()

    date_str = request.args.get('date') or request.form.get('date')
    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else date.today()
    except ValueError:
        selected_date = date.today()

    selected_class_id = request.args.get('class_id') or request.form.get('class_id')
    students = []
    existing_attendance = {}

    if selected_class_id:
        students = (
            Student.query
            .filter_by(class_id=selected_class_id)
            .order_by(Student.roll_number)
            .all()
        )
    else:
        students = Student.query.order_by(Student.roll_number).all()

    for s in students:
        record = Attendance.query.filter_by(student_id=s.id, date=selected_date).first()
        if record:
            existing_attendance[s.id] = record

    if request.method == 'POST':
        # Determine teacher_id if current user is a teacher
        teacher_id = None
        if current_user.role == 'teacher' and current_user.teacher_profile:
            teacher_id = current_user.teacher_profile.id

        for s in students:
            status = request.form.get(f'status_{s.id}')
            remarks = request.form.get(f'remarks_{s.id}', '')
            if status:
                existing = Attendance.query.filter_by(
                    student_id=s.id, date=selected_date
                ).first()
                if existing:
                    existing.status = status
                    existing.remarks = remarks
                    if teacher_id:
                        existing.marked_by = teacher_id
                else:
                    db.session.add(Attendance(
                        student_id=s.id,
                        date=selected_date,
                        status=status,
                        remarks=remarks,
                        marked_by=teacher_id,
                    ))

        db.session.commit()
        flash('Attendance saved successfully!', 'success')
        return redirect(url_for('teacher.mark_attendance',
                                date=selected_date.strftime('%Y-%m-%d'),
                                class_id=selected_class_id or ''))

    return render_template(
        'teacher/mark_attendance.html',
        classes=classes,
        students=students,
        selected_date=selected_date,
        selected_class_id=selected_class_id,
        existing_attendance=existing_attendance,
    )


@teacher_bp.route('/attendance/view')
@login_required
def view_attendance():
    if current_user.role == 'student':
        student = current_user.student_profile
        records = (
            Attendance.query
            .filter_by(student_id=student.id)
            .order_by(Attendance.date.desc())
            .all()
        ) if student else []
    else:
        records = Attendance.query.order_by(Attendance.date.desc()).limit(200).all()

    return render_template('shared/view_attendance.html', records=records)


@teacher_bp.route('/attendance/reports')
@login_required
@admin_or_teacher_required
def attendance_reports():
    classes = Class.query.order_by(Class.name).all()
    class_id = request.args.get('class_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    report_data = []
    if class_id:
        students = (
            Student.query
            .filter_by(class_id=class_id)
            .order_by(Student.roll_number)
            .all()
        )
        sd = datetime.strptime(start_date, '%Y-%m-%d').date() if start_date else None
        ed = datetime.strptime(end_date, '%Y-%m-%d').date() if end_date else None
        for s in students:
            pct = s.get_attendance_percentage(sd, ed)
            report_data.append({'student': s, 'percentage': pct})

    return render_template(
        'teacher/attendance_reports.html',
        classes=classes,
        class_id=class_id,
        start_date=start_date,
        end_date=end_date,
        report_data=report_data,
    )


# ─────────────────────────────────────────────────────────────────────────────
# STUDENT ATTENDANCE ANALYTICS
# ─────────────────────────────────────────────────────────────────────────────
@teacher_bp.route('/attendance/analytics')
@login_required
@student_required
def student_attendance():
    student = current_user.student_profile
    if not student:
        from flask import abort
        abort(403)

    start_date = request.args.get('start_date')
    end_date   = request.args.get('end_date')

    query = Attendance.query.filter_by(student_id=student.id)
    if start_date:
        try:
            query = query.filter(Attendance.date >= datetime.strptime(start_date, '%Y-%m-%d').date())
        except ValueError:
            start_date = None
    if end_date:
        try:
            query = query.filter(Attendance.date <= datetime.strptime(end_date, '%Y-%m-%d').date())
        except ValueError:
            end_date = None

    records = query.order_by(Attendance.date.desc()).all()

    # Overall counts
    present_count = sum(1 for r in records if r.status == 'present')
    absent_count  = sum(1 for r in records if r.status == 'absent')
    late_count    = sum(1 for r in records if r.status == 'late')
    total_count   = len(records)
    att_percent   = round((present_count / total_count) * 100, 1) if total_count else 0.0

    # Monthly breakdown
    monthly = defaultdict(lambda: {'present': 0, 'absent': 0, 'late': 0})
    for r in sorted(records, key=lambda x: x.date):
        key = r.date.strftime('%b %Y')
        monthly[key][r.status] = monthly[key].get(r.status, 0) + 1

    monthly_labels  = list(monthly.keys())
    monthly_present = [monthly[k]['present'] for k in monthly_labels]
    monthly_absent  = [monthly[k]['absent']  for k in monthly_labels]
    monthly_late    = [monthly[k]['late']    for k in monthly_labels]

    return render_template(
        'student/attendance.html',
        student=student,
        records=records,
        att_percent=att_percent,
        present_count=present_count,
        absent_count=absent_count,
        late_count=late_count,
        total_count=total_count,
        monthly_data=monthly,
        monthly_labels=monthly_labels,
        monthly_present=monthly_present,
        monthly_absent=monthly_absent,
        monthly_late=monthly_late,
        start_date=start_date,
        end_date=end_date,
    )



