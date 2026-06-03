from flask import render_template, abort
from flask_login import login_required, current_user

from services.homework_service import HomeworkService
from . import student_bp
from utils.decorators import student_required


@student_bp.route('/homework')
@login_required
@student_required
def view_homework():
    """Student views active homework for their class (last 7 days)."""
    student = current_user.student_profile
    if not student:
        abort(403)

    homework_list = HomeworkService.get_for_class(student.class_id)
    return render_template(
        'student/homework.html',
        homework_list=homework_list,
        student=student,
    )
