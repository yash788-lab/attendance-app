from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required

from models.user import User
from models.teacher import Teacher
from models.student import Student
from models.academic import Class, Subject, Exam
from database import db
from . import admin_bp
from utils.decorators import admin_required
from services.admin_service import AdminService


# ─────────────────────────────────────────────────────────────────────────────
# ADMIN DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
@admin_bp.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    total_students = Student.query.count()
    total_teachers = Teacher.query.filter_by(is_approved=True).count()
    pending_teachers = Teacher.query.filter_by(is_approved=False).count()
    total_classes = Class.query.count()
    recent_registrations = (
        Teacher.query
        .filter_by(is_approved=False)
        .order_by(Teacher.created_at.desc())
        .limit(10)
        .all()
    )
    return render_template(
        'admin/dashboard.html',
        total_students=total_students,
        total_teachers=total_teachers,
        pending_teachers=pending_teachers,
        total_classes=total_classes,
        recent_registrations=recent_registrations,
    )


# ─────────────────────────────────────────────────────────────────────────────
# TEACHER APPROVAL
# ─────────────────────────────────────────────────────────────────────────────
@admin_bp.route('/admin/teachers')
@login_required
@admin_required
def admin_teachers():
    approved = Teacher.query.filter_by(is_approved=True).order_by(Teacher.name).all()
    pending = Teacher.query.filter_by(is_approved=False).order_by(Teacher.created_at.desc()).all()
    return render_template('admin/teachers.html', approved=approved, pending=pending)


@admin_bp.route('/admin/teacher/<int:teacher_id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_teacher(teacher_id):
    success, teacher = AdminService.approve_teacher(teacher_id)
    if success:
        flash(f'{teacher.name} has been approved and can now log in.', 'success')
    else:
        flash('Teacher not found.', 'error')
    return redirect(url_for('admin.admin_teachers'))


@admin_bp.route('/admin/teacher/<int:teacher_id>/reject', methods=['POST'])
@login_required
@admin_required
def reject_teacher(teacher_id):
    if AdminService.reject_teacher(teacher_id):
        flash('Teacher registration rejected and removed.', 'info')
    else:
        flash('Teacher not found.', 'error')
    return redirect(url_for('admin.admin_teachers'))


@admin_bp.route('/admin/teacher/<int:teacher_id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_delete_teacher(teacher_id):
    success, result = AdminService.delete_teacher(teacher_id)
    if success:
        flash(f'Teacher {result} has been permanently removed.', 'success')
    else:
        flash(result, 'error')
    return redirect(url_for('admin.admin_teachers'))


# ─────────────────────────────────────────────────────────────────────────────
# STUDENT MANAGEMENT (admin view)
# ─────────────────────────────────────────────────────────────────────────────
@admin_bp.route('/admin/students')
@login_required
@admin_required
def admin_students():
    class_id = request.args.get('class_id', type=int)
    classes = Class.query.order_by(Class.name).all()
    query = Student.query.join(Class).order_by(Class.name, Student.roll_number)
    if class_id:
        query = query.filter(Student.class_id == class_id)
    students = query.all()
    return render_template('admin/students.html', students=students,
                           classes=classes, selected_class=class_id)


@admin_bp.route('/admin/student/add', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_add_student():
    classes = Class.query.order_by(Class.name).all()
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        father_name = request.form.get('father_name', '').strip()
        class_id = request.form.get('class_id', type=int)
        roll_number = request.form.get('roll_number', '').strip()
        email = request.form.get('email', '').strip().lower()
        phone = request.form.get('phone', '').strip()

        AdminService.add_student(
            name=name, father_name=father_name, class_id=class_id,
            roll_number=roll_number, email=email, phone=phone
        )
        flash(f'Student {name} added. Default password is their roll number.', 'success')
        return redirect(url_for('admin.admin_students'))

    return render_template('admin/add_student.html', classes=classes)


@admin_bp.route('/admin/student/<int:student_id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_delete_student(student_id):
    success, name = AdminService.delete_student(student_id)
    if success:
        flash(f'Student {name} deleted.', 'success')
    else:
        flash('Student not found.', 'error')
    return redirect(url_for('admin.admin_students'))


# ─────────────────────────────────────────────────────────────────────────────
# SYSTEM MANAGEMENT (Classes, Subjects, Exams)
# ─────────────────────────────────────────────────────────────────────────────
@admin_bp.route('/admin/classes')
@login_required
@admin_required
def admin_classes():
    classes = Class.query.order_by(Class.name).all()
    return render_template('admin/classes.html', classes=classes)


@admin_bp.route('/admin/class/add', methods=['POST'])
@login_required
@admin_required
def admin_add_class():
    name = request.form.get('name', '').strip()
    academic_year = request.form.get('academic_year', '2025-26').strip()
    if name:
        if AdminService.add_class(name, academic_year):
            flash(f'Class "{name}" added.', 'success')
        else:
            flash(f'Class "{name}" already exists.', 'error')
    return redirect(url_for('admin.admin_classes'))


@admin_bp.route('/admin/class/<int:class_id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_delete_class(class_id):
    class_ = db.session.get(Class, class_id)
    if not class_:
        flash('Class not found.', 'error')
        return redirect(url_for('admin.admin_classes'))

    if class_.students:
        flash(f'Cannot delete class "{class_.name}" because it contains enrolled students. Please reassign or remove the students first.', 'error')
        return redirect(url_for('admin.admin_classes'))

    # Clean up related records
    from models.academic import ClassSubject
    from models.homework import Homework
    from models.communication import Announcement

    ClassSubject.query.filter_by(class_id=class_.id).delete()
    Homework.query.filter_by(class_id=class_.id).delete()
    Announcement.query.filter_by(target_class_id=class_.id).update({Announcement.target_class_id: None})

    name = class_.name
    db.session.delete(class_)
    db.session.commit()
    flash(f'Class "{name}" deleted successfully.', 'success')
    return redirect(url_for('admin.admin_classes'))


@admin_bp.route('/admin/subjects')
@login_required
@admin_required
def admin_subjects():
    subjects = Subject.query.order_by(Subject.name).all()
    return render_template('admin/subjects.html', subjects=subjects)


@admin_bp.route('/admin/subject/add', methods=['POST'])
@login_required
@admin_required
def admin_add_subject():
    name = request.form.get('name', '').strip()
    code = request.form.get('code', '').strip().upper() or None
    if name:
        AdminService.add_subject(name, code)
        flash(f'Subject "{name}" added.', 'success')
    return redirect(url_for('admin.admin_subjects'))


@admin_bp.route('/admin/exams')
@login_required
@admin_required
def admin_exams():
    exams = Exam.query.order_by(Exam.term, Exam.name).all()
    return render_template('admin/exams.html', exams=exams)


@admin_bp.route('/admin/exam/add', methods=['POST'])
@login_required
@admin_required
def admin_add_exam():
    name = request.form.get('name', '').strip()
    term = request.form.get('term', '2025-26').strip()
    if name and term:
        AdminService.add_exam(name, term)
        flash(f'Exam "{name}" added.', 'success')
    return redirect(url_for('admin.admin_exams'))
