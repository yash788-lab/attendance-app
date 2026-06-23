from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime

from models.academic import Class, Subject
from services.homework_service import HomeworkService
from services.notification_service import NotificationService
from . import teacher_bp
from utils.decorators import admin_or_teacher_required


@teacher_bp.route('/homework')
@login_required
@admin_or_teacher_required
def manage_homework():
    """Teacher views their own active homework assignments."""
    teacher = current_user.teacher_profile
    teacher_id = teacher.id if teacher else None

    if current_user.role == 'admin':
        homework_list = HomeworkService.get_all_active()
    else:
        homework_list = HomeworkService.get_for_teacher(teacher_id)

    classes = Class.query.order_by(Class.name).all()
    subjects = Subject.query.order_by(Subject.name).all()
    return render_template(
        'teacher/manage_homework.html',
        homework_list=homework_list,
        classes=classes,
        subjects=subjects,
    )


@teacher_bp.route('/homework/assign', methods=['POST'])
@login_required
@admin_or_teacher_required
def assign_homework():
    """Handle homework assignment form submission."""
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    class_id = request.form.get('class_id', type=int)
    subject_id = request.form.get('subject_id', type=int)
    due_date_str = request.form.get('due_date', '').strip()

    if not title or not class_id or not subject_id:
        flash('Title, class, and subject are required.', 'error')
        return redirect(url_for('teacher.manage_homework'))

    teacher = current_user.teacher_profile
    teacher_id = teacher.id if teacher else None
    if not teacher_id:
        flash('Only an approved teacher account can assign homework.', 'error')
        return redirect(url_for('teacher.manage_homework'))

    due_date = None
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        except ValueError:
            pass

    hw = HomeworkService.create(
        title=title,
        description=description,
        class_id=class_id,
        subject_id=subject_id,
        teacher_id=teacher_id,
        due_date=due_date,
    )

    # Notify students in the class
    subject = Subject.query.get(subject_id)
    NotificationService.notify_homework_assigned(
        class_id=class_id,
        subject_name=subject.name if subject else 'a subject',
        teacher_name=teacher.name,
    )

    flash(f'Homework "{title}" assigned successfully and students notified.', 'success')
    return redirect(url_for('teacher.manage_homework'))


@teacher_bp.route('/homework/<int:hw_id>/delete', methods=['POST'])
@login_required
@admin_or_teacher_required
def delete_homework(hw_id):
    """Delete a homework assignment (teacher who created it, or admin)."""
    # Quick check for ownership
    from models.homework import Homework
    hw = Homework.query.get(hw_id)
    if not hw:
        flash('Homework not found.', 'error')
        return redirect(url_for('teacher.manage_homework'))

    teacher = current_user.teacher_profile
    if current_user.role != 'admin' and (not teacher or hw.teacher_id != teacher.id):
        flash('You can only delete your own homework assignments.', 'error')
        return redirect(url_for('teacher.manage_homework'))

    HomeworkService.delete(hw_id)
    flash('Homework deleted.', 'success')
    return redirect(url_for('teacher.manage_homework'))
