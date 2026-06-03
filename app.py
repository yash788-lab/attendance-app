import os
import time
from flask import Flask, redirect, url_for, session
from flask_login import current_user, logout_user

# ── Local imports ─────────────────────────────────────────────────────────────
from config import Config
from database import db
from extensions import login_manager, migrate
from utils.seed import register_seed_commands

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 1. Init DB
    db.init_app(app)

    # Import ALL models here so SQLAlchemy registers them in metadata
    # and Alembic can detect the full schema during `flask db migrate`
    import models  # noqa: F401 — side-effect import registers all tables

    # 2. Init Migrations (must come AFTER models are imported so Alembic sees them)
    migrate.init_app(app, db)

    # 3. Login Manager
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'
    # Use 'basic' instead of 'strong' — Render runs behind a reverse proxy which
    # can change the apparent client IP, causing 'strong' to invalidate sessions.
    login_manager.session_protection = 'basic'

    # 4. Session / inactivity timeout
    @app.before_request
    def session_management():
        if not current_user.is_authenticated:
            return
        session.permanent = True
        now = time.time()
        # Admin/Teacher: 2 hrs | Student: 20 min (Keeping original as requested)
        timeout = 7200 if current_user.role in ('admin', 'teacher') else 1200
        if 'last_activity' in session:
            if now - session['last_activity'] > timeout:
                logout_user()
                session.clear()
                return redirect(url_for('auth.login'))
        session['last_activity'] = now

    @app.context_processor
    def inject_global_data():
        """Inject variables into all templates"""
        data = {}
        if current_user.is_authenticated:
            from models.notification import Notification
            data['unread_notifications'] = Notification.query.filter(
                (Notification.recipient_user_id == current_user.id) |
                (Notification.recipient_user_id == None),
                Notification.is_read == False
            ).count()
            
            if current_user.role == 'admin':
                from models.teacher import Teacher
                data['pending_teachers_count'] = Teacher.query.filter_by(is_approved=False).count()
        return data

    # 5. Register Blueprints
    from routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from routes.admin import admin_bp
    app.register_blueprint(admin_bp)

    from routes.teacher import teacher_bp
    app.register_blueprint(teacher_bp)

    from routes.student import student_bp
    app.register_blueprint(student_bp)

    from routes.public_routes import public_bp
    app.register_blueprint(public_bp)

    # 6. Register CLI commands
    register_seed_commands(app, db)

    return app


# ── USER LOADER ───────────────────────────────────────────────────────────────
@login_manager.user_loader
def load_user(user_id):
    """Load a User from the database by primary key (string from session)."""
    from models.user import User
    try:
        return db.session.get(User, int(user_id))
    except Exception:
        # Catch all exceptions (including DB missing tables) so the app doesn't crash on stale cookies
        return None


# ── ENTRY POINT ───────────────────────────────────────────────────────────────
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)