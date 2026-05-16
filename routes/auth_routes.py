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


# ─────────────────────────────────────────────────────────────────────────────
# RENDER SETUP ROUTE (ONE-TIME USE)
# ─────────────────────────────────────────────────────────────────────────────
@main.route('/setup-render-db')
def setup_render_db():
    """
    Emergency route to reset and migrate the database on Render 
    without needing shell access. This will drop all tables and re-create them.
    """
    try:
        from database import db
        from sqlalchemy import text
        import traceback

        # 1. WIPE THE DATABASE (PostgreSQL specific)
        try:
            db.session.execute(text("DROP SCHEMA public CASCADE;"))
            db.session.execute(text("CREATE SCHEMA public;"))
            db.session.commit()
        except Exception:
            db.session.rollback()
            # Fallback for SQLite locally
            db.drop_all()
            try:
                db.session.execute(text("DROP TABLE IF EXISTS alembic_version;"))
                db.session.commit()
            except Exception:
                db.session.rollback()
        
        # 2. Run alembic upgrade
        from flask_migrate import upgrade
        upgrade()
        
        # 3. Seed data
        from models.academic import Class, Subject, Exam
        if not Class.query.first():
            for name in ['5', '6', '7', '8', '9', '10', '11-Maths', '11-Science', '12-Maths', '12-Science']:
                db.session.add(Class(name=name))
            db.session.commit()

        if not Subject.query.first():
            for name, code in [
                ('Mathematics', 'MATH'), ('Science', 'SCI'), ('English', 'ENG'),
                ('History', 'HIST'), ('Physics', 'PHY'), ('Chemistry', 'CHEM'),
            ]:
                db.session.add(Subject(name=name, code=code))
            db.session.commit()

        if not Exam.query.first():
            for name in ['Unit Test 1', 'Unit Test 2', 'Mid-Term', 'Final Exam']:
                db.session.add(Exam(name=name, term='2025-26'))
            db.session.commit()

        # 4. Seed admin
        from models.user import User, Admin
        if not User.query.filter_by(email='admin@school.edu').first():
            user = User(email='admin@school.edu', role='admin', is_active=True)
            user.set_password('admin123')
            db.session.add(user)
            db.session.flush()
            admin = Admin(user_id=user.id, name='Super Admin')
            db.session.add(admin)
            db.session.commit()

        return "✅ Render Setup Complete! Database has been reset, migrated, and seeded. You can now login at /login with admin@school.edu and password admin123."

    except Exception as e:
        import traceback
        return f"❌ Error during setup: {str(e)}<br><pre>{traceback.format_exc()}</pre>", 500