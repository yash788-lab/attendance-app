from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required

from models.user import User
from models.admin import Admin
from models.teacher import Teacher
from models.student import Student
from models.academic import Class, Subject, Exam
from database import db
from . import admin_bp
from utils.decorators import admin_required


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
    teacher = db.session.get(Teacher, teacher_id)
    if not teacher:
        flash('Teacher not found.', 'error')
        return redirect(url_for('admin.admin_teachers'))
    teacher.is_approved = True
    teacher.user.is_active = True
    db.session.commit()
    flash(f'{teacher.name} has been approved and can now log in.', 'success')
    return redirect(url_for('admin.admin_teachers'))


@admin_bp.route('/admin/teacher/<int:teacher_id>/reject', methods=['POST'])
@login_required
@admin_required
def reject_teacher(teacher_id):
    teacher = db.session.get(Teacher, teacher_id)
    if not teacher:
        flash('Teacher not found.', 'error')
        return redirect(url_for('admin.admin_teachers'))
    user = teacher.user
    db.session.delete(teacher)
    db.session.delete(user)
    db.session.commit()
    flash('Teacher registration rejected and removed.', 'info')
    return redirect(url_for('admin.admin_teachers'))


@admin_bp.route('/admin/teacher/<int:teacher_id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_delete_teacher(teacher_id):
    teacher = db.session.get(Teacher, teacher_id)
    if not teacher:
        flash('Teacher not found.', 'error')
        return redirect(url_for('admin.admin_teachers'))
    name = teacher.name
    user = teacher.user

    # Clean up assignments, attendance marked reference, marks entered reference, and homework
    from models.academic import ClassSubject
    from models.attendance import Attendance
    from models.marks import Mark
    from models.homework import Homework
    from models.communication import Announcement, Event, Poll, PollVote

    ClassSubject.query.filter_by(teacher_id=teacher.id).update({ClassSubject.teacher_id: None})
    Attendance.query.filter_by(marked_by=teacher.id).update({Attendance.marked_by: None})
    Mark.query.filter_by(entered_by=teacher.id).update({Mark.entered_by: None})
    Homework.query.filter_by(teacher_id=teacher.id).delete()

    if user:
        Announcement.query.filter_by(created_by=user.id).delete()
        Event.query.filter_by(created_by=user.id).delete()
        PollVote.query.filter_by(user_id=user.id).delete()
        Poll.query.filter_by(created_by=user.id).delete()
        db.session.delete(user)
    else:
        db.session.delete(teacher)

    db.session.commit()
    flash(f'Teacher {name} has been permanently removed.', 'success')
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

        # Create Student record
        student = Student(
            name=name, father_name=father_name, class_id=class_id,
            roll_number=roll_number, email=email, phone=phone
        )
        db.session.add(student)
        db.session.flush()

        # Auto-create User account (password = roll_number), or link existing one
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            # Link student to the already-existing user account
            student.user_id = existing_user.id
        else:
            user = User(email=email, role='student', is_active=True, must_change_password=True)
            user.set_password(roll_number)
            db.session.add(user)
            db.session.flush()
            student.user_id = user.id

        db.session.commit()
        flash(f'Student {name} added. Default password is their roll number.', 'success')
        return redirect(url_for('admin.admin_students'))

    return render_template('admin/add_student.html', classes=classes)


@admin_bp.route('/admin/student/<int:student_id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_delete_student(student_id):
    student = db.session.get(Student, student_id)
    if not student:
        flash('Student not found.', 'error')
        return redirect(url_for('admin.admin_students'))
    name = student.name
    # Cascade deletes attendance + marks via relationship
    db.session.delete(student)
    db.session.commit()
    flash(f'Student {name} deleted.', 'success')
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
        if Class.query.filter_by(name=name).first():
            flash(f'Class "{name}" already exists.', 'error')
        else:
            db.session.add(Class(name=name, academic_year=academic_year))
            db.session.commit()
            flash(f'Class "{name}" added.', 'success')
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
        db.session.add(Subject(name=name, code=code))
        db.session.commit()
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
        db.session.add(Exam(name=name, term=term))
        db.session.commit()
        flash(f'Exam "{name}" added.', 'success')
    return redirect(url_for('admin.admin_exams'))
