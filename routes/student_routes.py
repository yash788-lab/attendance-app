from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required

from models import Student, Class
from database import db
from . import main
from utils.decorators import teacher_required


@main.route('/students')
@login_required
@teacher_required
def students():
    students = Student.query.join(Class).order_by(Class.name, Student.roll_number).all()
    return render_template('students.html', students=students)


@main.route('/student/add', methods=['GET', 'POST'])
@login_required
@teacher_required
def add_student():
    if request.method == 'POST':
        student = Student(
            name=request.form.get('name'),
            father_name=request.form.get('father_name'),
            class_id=request.form.get('class_id'),
            roll_number=request.form.get('roll_number'),
            email=request.form.get('email')
        )
        db.session.add(student)
        db.session.commit()

        flash(f'Student {student.name} added!', 'success')
        return redirect(url_for('main.students'))

    classes = Class.query.all()
    return render_template('add_student.html', classes=classes)

@main.route('/student/delete/<int:student_id>', methods=['POST'])
@login_required
@teacher_required
def delete_student(student_id):
    return "Delete Student Stub"