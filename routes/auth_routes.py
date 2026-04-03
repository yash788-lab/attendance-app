from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_user, logout_user, login_required, current_user


from models import Student, Class
from auth import User, TEACHER_ID
from . import main


@main.route('/login', methods=['GET', 'POST'])
def login():
    classes = Class.query.all()
    if request.method == 'POST':
        student = Student.query.filter_by(
            class_id=request.form.get('class_id'),
            roll_number=request.form.get('roll_number'),
            email=request.form.get('email')
        ).first()

        if student:
            login_user(User(id=student.id, role='student'))
            return redirect(url_for('main.index'))

        flash("Invalid credentials", "error")

    return render_template('student_login.html', classes=classes)


@main.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        if request.form.get('password') == "admin123":
            login_user(User(id=TEACHER_ID, role='teacher'))
            return redirect(url_for('main.index'))

        flash("Invalid Admin Password", "error")

    return render_template('admin_login.html')


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))