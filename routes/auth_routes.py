from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from models.user import User, Admin
from models.teacher import Teacher
from database import db
from . import main


# ─────────────────────────────────────────────────────────────────────────────
# UNIFIED LOGIN (Admin + Teacher + Student)
# ─────────────────────────────────────────────────────────────────────────────
@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash('Invalid email or password.', 'error')
            return render_template('auth/login.html')

        if not user.is_active:
            flash('Your account is inactive. Please contact the admin.', 'warning')
            return render_template('auth/login.html')

        # Teacher: must be approved
        if user.role == 'teacher':
            if not user.teacher_profile or not user.teacher_profile.is_approved:
                flash('Your teacher account is pending admin approval.', 'warning')
                return render_template('auth/login.html')

        login_user(user, remember=False)

        # Redirect students who must change their password
        if user.must_change_password:
            flash('Please set a new password before continuing.', 'info')
            return redirect(url_for('main.change_password'))

        return redirect(url_for('main.index'))

    return render_template('auth/login.html')


# ─────────────────────────────────────────────────────────────────────────────
# TEACHER SELF-REGISTRATION
# ─────────────────────────────────────────────────────────────────────────────
@main.route('/teacher/register', methods=['GET', 'POST'])
def teacher_register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        # Validation
        errors = []
        if not name:
            errors.append('Name is required.')
        if not email:
            errors.append('Email is required.')
        if len(password) < 6:
            errors.append('Password must be at least 6 characters.')
        if password != confirm:
            errors.append('Passwords do not match.')
        if User.query.filter_by(email=email).first():
            errors.append('An account with this email already exists.')

        if errors:
            for e in errors:
                flash(e, 'error')
            return render_template('auth/teacher_register.html',
                                   name=name, email=email, phone=phone)

        # Create User (inactive until approved)
        user = User(email=email, role='teacher', is_active=False)
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        teacher = Teacher(user_id=user.id, name=name, phone=phone, is_approved=False)
        db.session.add(teacher)
        db.session.commit()

        flash('Registration submitted! You will be able to log in once approved by the admin.', 'success')
        return redirect(url_for('main.login'))

    return render_template('auth/teacher_register.html')


# ─────────────────────────────────────────────────────────────────────────────
# CHANGE PASSWORD (first-login students / any user)
# ─────────────────────────────────────────────────────────────────────────────
@main.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_pw = request.form.get('current_password', '')
        new_pw = request.form.get('new_password', '')
        confirm_pw = request.form.get('confirm_password', '')

        if not current_user.check_password(current_pw):
            flash('Current password is incorrect.', 'error')
            return render_template('auth/change_password.html')

        if len(new_pw) < 6:
            flash('New password must be at least 6 characters.', 'error')
            return render_template('auth/change_password.html')

        if new_pw != confirm_pw:
            flash('Passwords do not match.', 'error')
            return render_template('auth/change_password.html')

        current_user.set_password(new_pw)
        current_user.must_change_password = False
        db.session.commit()
        flash('Password updated successfully!', 'success')
        return redirect(url_for('main.index'))

    return render_template('auth/change_password.html')


# ─────────────────────────────────────────────────────────────────────────────
# LOGOUT
# ─────────────────────────────────────────────────────────────────────────────
@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))