from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from models.student import Student
from models.academic import Class
from database import db
from . import main
from utils.decorators import admin_or_teacher_required


# Teacher/Admin: view all students (redirects admin to admin panel)
@main.route('/students')
@login_required
@admin_or_teacher_required
def students():
    if current_user.role == 'admin':
        return redirect(url_for('main.admin_students'))
    students = (
        Student.query
        .join(Class)
        .order_by(Class.name, Student.roll_number)
        .all()
    )
    return render_template('teacher/students.html', students=students)


# Legacy redirect: old /student/add goes to admin panel
@main.route('/student/add', methods=['GET', 'POST'])
@login_required
@admin_or_teacher_required
def add_student():
    return redirect(url_for('main.admin_add_student'))


# Legacy redirect: old /student/delete goes to admin panel
@main.route('/student/delete/<int:student_id>', methods=['POST'])
@login_required
@admin_or_teacher_required
def delete_student(student_id):
    return redirect(url_for('main.admin_delete_student', student_id=student_id))