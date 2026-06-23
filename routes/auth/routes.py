from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from models.user import User
from models.admin import Admin
from models.teacher import Teacher
from database import db
from . import auth_bp
from services.auth_service import AuthService


# ─────────────────────────────────────────────────────────────────────────────
# ADMIN LOGIN  (/admin/login)
# ─────────────────────────────────────────────────────────────────────────────
@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.admin_dashboard'))
        elif current_user.role == 'student':
            return redirect(url_for('student.dashboard'))
        else:
            return redirect(url_for('teacher.dashboard'))

    if request.method == 'POST':
        email    = request.form.get('email', '')
        password = request.form.get('password', '')

        user, err = AuthService.authenticate(email, password)
        if err:
            flash(err, 'error')
            return render_template('auth/admin_login.html')

        if user.role != 'admin':
            flash('This portal is for administrators only. Please use the correct login page.', 'error')
            return render_template('auth/admin_login.html')

        login_user(user, remember=False)
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('auth/admin_login.html')


# ─────────────────────────────────────────────────────────────────────────────
# STUDENT LOGIN  (/student/login)
# ─────────────────────────────────────────────────────────────────────────────
@auth_bp.route('/student/login', methods=['GET', 'POST'])
def student_login():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.admin_dashboard'))
        elif current_user.role == 'student':
            return redirect(url_for('student.dashboard'))
        else:
            return redirect(url_for('teacher.dashboard'))

    if request.method == 'POST':
        email    = request.form.get('email', '')
        password = request.form.get('password', '')

        user, err = AuthService.authenticate(email, password)
        if err:
            flash(err, 'error')
            return render_template('auth/student_login.html')

        if user.role != 'student':
            flash('This portal is for students only. Please use the correct login page.', 'error')
            return render_template('auth/student_login.html')

        login_user(user, remember=False)

        if user.must_change_password:
            flash('Please set a new password before continuing.', 'info')
            return redirect(url_for('auth.change_password'))

        return redirect(url_for('student.dashboard'))

    return render_template('auth/student_login.html')


# ─────────────────────────────────────────────────────────────────────────────
# UNIFIED LOGIN — teachers + fallback  (/login)
# ─────────────────────────────────────────────────────────────────────────────
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.admin_dashboard'))
        elif current_user.role == 'student':
            return redirect(url_for('student.dashboard'))
        else:
            return redirect(url_for('teacher.dashboard'))

    if request.method == 'POST':
        email    = request.form.get('email', '')
        password = request.form.get('password', '')

        user, err = AuthService.authenticate(email, password)
        if err:
            flash(err, 'error')
            return render_template('auth/login.html')

        # Redirect to dedicated portal if not a teacher
        if user.role == 'admin':
            flash('Please use the Admin Login page.', 'info')
            return redirect(url_for('auth.admin_login'))
        if user.role == 'student':
            flash('Please use the Student Login page.', 'info')
            return redirect(url_for('auth.student_login'))

        # Teacher: must be approved
        if not user.teacher_profile or not user.teacher_profile.is_approved:
            flash('Your teacher account is pending admin approval.', 'warning')
            return render_template('auth/login.html')

        login_user(user, remember=False)

        if user.must_change_password:
            flash('Please set a new password before continuing.', 'info')
            return redirect(url_for('auth.change_password'))

        return redirect(url_for('teacher.dashboard'))

    return render_template('auth/login.html')


# ─────────────────────────────────────────────────────────────────────────────
# TEACHER SELF-REGISTRATION
# ─────────────────────────────────────────────────────────────────────────────
@auth_bp.route('/teacher/register', methods=['GET', 'POST'])
def teacher_register():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.admin_dashboard'))
        elif current_user.role == 'student':
            return redirect(url_for('student.dashboard'))
        else:
            return redirect(url_for('teacher.dashboard'))

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

        user, err = AuthService.register_teacher(name, email, phone, password)
        if err:
            flash(err, 'error')
            return render_template('auth/teacher_register.html',
                                   name=name, email=email, phone=phone)

        flash('Registration submitted! You will be able to log in once approved by the admin.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/teacher_register.html')


# ─────────────────────────────────────────────────────────────────────────────
# CHANGE PASSWORD (first-login students / any user)
# ─────────────────────────────────────────────────────────────────────────────
@auth_bp.route('/change-password', methods=['GET', 'POST'])
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
        if current_user.role == 'admin':
            return redirect(url_for('admin.admin_dashboard'))
        elif current_user.role == 'student':
            return redirect(url_for('student.dashboard'))
        else:
            return redirect(url_for('teacher.dashboard'))

    return render_template('auth/change_password.html')


# ─────────────────────────────────────────────────────────────────────────────
# LOGOUT
# ─────────────────────────────────────────────────────────────────────────────
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


# ─────────────────────────────────────────────────────────────────────────────
# RENDER SETUP ROUTE (ONE-TIME USE — run after first deploy)
# ─────────────────────────────────────────────────────────────────────────────
@auth_bp.route('/setup-render-db')
def setup_render_db():
    """
    One-time setup route for Render deployments without shell access.
    Drops all tables, runs flask db upgrade, then seeds default data + admin.
    Visit /setup-render-db ONCE after first deploy, then never again.
    """
    from flask import current_app
    from database import db
    from sqlalchemy import text
    from flask_migrate import upgrade
    import traceback

    log = []

    def step(label, fn):
        try:
            fn()
            log.append(f'<li style="color:#10b981">✅ {label}</li>')
            return True
        except Exception as exc:
            log.append(
                f'<li style="color:#ef4444">❌ {label}: {exc}'
                f'<pre style="font-size:.75rem;white-space:pre-wrap">{traceback.format_exc()}</pre></li>'
            )
            return False

    # ── 1. Wipe schema ────────────────────────────────────────────────────────
    def wipe():
        try:
            db.session.execute(text('DROP SCHEMA public CASCADE;'))
            db.session.execute(text('CREATE SCHEMA public;'))
            db.session.commit()
        except Exception:
            db.session.rollback()
            # SQLite fallback
            db.drop_all()

    step('Wipe existing schema', wipe)

    # Close the current session cleanly so upgrade() gets a fresh connection
    db.session.remove()

    # ── 2. Run migrations ─────────────────────────────────────────────────────
    ok = step('Run flask db upgrade', lambda: upgrade())
    if not ok:
        html = f'<ul>{"".join(log)}</ul>'
        return f'<h2>Setup failed at migration step</h2>{html}', 500

    # ── 3. Seed Classes ───────────────────────────────────────────────────────
    def seed_classes():
        from models.academic import Class
        if not Class.query.first():
            for name in ['5', '6', '7', '8', '9', '10',
                         '11-Maths', '11-Science', '12-Maths', '12-Science']:
                db.session.add(Class(name=name))
            db.session.commit()

    step('Seed default classes', seed_classes)

    # ── 4. Seed Subjects ──────────────────────────────────────────────────────
    def seed_subjects():
        from models.academic import Subject
        if not Subject.query.first():
            for name, code in [
                ('Mathematics', 'MATH'), ('Science', 'SCI'), ('English', 'ENG'),
                ('History', 'HIST'), ('Physics', 'PHY'), ('Chemistry', 'CHEM'),
                ('Biology', 'BIO'), ('Computer Science', 'CS'),
            ]:
                db.session.add(Subject(name=name, code=code))
            db.session.commit()

    step('Seed default subjects', seed_subjects)

    # ── 5. Seed Exams ─────────────────────────────────────────────────────────
    def seed_exams():
        from models.academic import Exam
        if not Exam.query.first():
            for name in ['Unit Test 1', 'Unit Test 2', 'Mid-Term', 'Final Exam']:
                db.session.add(Exam(name=name, term='2025-26'))
            db.session.commit()

    step('Seed default exam types', seed_exams)

    # ── 6. Seed Admin account ─────────────────────────────────────────────────
    def seed_admin():
        from models.user import User
        from models.admin import Admin
        if not User.query.filter_by(email='admin@school.edu').first():
            user = User(email='admin@school.edu', role='admin', is_active=True)
            user.set_password('admin123')
            db.session.add(user)
            db.session.flush()
            db.session.add(Admin(user_id=user.id, name='Super Admin'))
            db.session.commit()

    step('Seed admin account (admin@school.edu / admin123)', seed_admin)

    # ── Done ──────────────────────────────────────────────────────────────────
    html = f'''<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<title>Render Setup</title>
<style>body{{font-family:system-ui;max-width:700px;margin:40px auto;padding:0 20px;}}
ul{{list-style:none;padding:0;line-height:2;}}
pre{{background:#f1f5f9;padding:8px;border-radius:4px;overflow:auto;}}
</style></head><body>
<h1>🏫 School ERP — Render Setup</h1>
<ul>{"".join(log)}</ul>
<hr>
<p>✅ Setup complete. <a href="/login">Go to Login →</a></p>
<p style="color:#64748b;font-size:.85rem">
  Default admin credentials: <strong>admin@school.edu</strong> / <strong>admin123</strong><br>
  ⚠️ Change the admin password immediately after first login.
</p>
</body></html>'''
    return html