from functools import wraps
from flask import abort, redirect, url_for, flash
from flask_login import current_user


def admin_required(f):
    """Restricts access to users with role='admin'."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated


def teacher_required(f):
    """Restricts access to users with role='teacher' (and approved)."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'teacher':
            abort(403)
        # Extra check: teacher must be approved by admin
        if current_user.teacher_profile and not current_user.teacher_profile.is_approved:
            flash('Your account is pending admin approval.', 'warning')
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated


def admin_or_teacher_required(f):
    """Restricts access to admin or approved teacher."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(403)
        if current_user.role not in ('admin', 'teacher'):
            abort(403)
        if current_user.role == 'teacher':
            if current_user.teacher_profile and not current_user.teacher_profile.is_approved:
                flash('Your account is pending admin approval.', 'warning')
                return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated


def student_required(f):
    """Restricts access to users with role='student'."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'student':
            abort(403)
        return f(*args, **kwargs)
    return decorated