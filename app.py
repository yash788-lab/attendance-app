import os
import time
import click
from flask import Flask, redirect, url_for, session
from flask_login import LoginManager, current_user, logout_user
from flask_migrate import Migrate

# ── Local imports ─────────────────────────────────────────────────────────────
from config import Config
from database import db

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 1. Init DB
    db.init_app(app)

    # Import ALL models here so SQLAlchemy registers them in metadata
    # and Alembic can detect the full schema during `flask db migrate`
    import models  # noqa: F401 — side-effect import registers all tables

    # 2. Init Migrations (must come AFTER models are imported so Alembic sees them)
    migrate = Migrate(app, db)

    # 3. Login Manager
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
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
        # Admin/Teacher: 2 hrs | Student: 20 min
        timeout = 7200 if current_user.role in ('admin', 'teacher') else 1200
        if 'last_activity' in session:
            if now - session['last_activity'] > timeout:
                logout_user()
                session.clear()
                return redirect(url_for('main.login'))
        session['last_activity'] = now

    # 5. Register Blueprints
    from routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # 6. Register CLI commands
    _register_cli(app)

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


# ── CLI COMMANDS ──────────────────────────────────────────────────────────────
def _register_cli(app: Flask):

    @app.cli.command('seed-admin')
    @click.option('--name', default='Admin', help='Admin display name')
    @click.option('--email', prompt=True, help='Admin email address')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='Admin password')
    def seed_admin(name, email, password):
        """Create the first admin account (run once after initial migration)."""
        from models.user import User, Admin
        if User.query.filter_by(email=email).first():
            click.echo(f'⚠️  A user with email "{email}" already exists.')
            return
        user = User(email=email, role='admin', is_active=True)
        user.set_password(password)
        db.session.add(user)
        db.session.flush()
        admin = Admin(user_id=user.id, name=name)
        db.session.add(admin)
        db.session.commit()
        click.echo(f'✅ Admin account created: {email}')

    @app.cli.command('seed-student-accounts')
    def seed_student_accounts():
        """Create User accounts for all existing students who don't have one.
        Default password = roll_number. Students are prompted to change on first login.
        """
        from models.user import User
        from models.student import Student
        created = 0
        skipped = 0
        for student in Student.query.filter_by(user_id=None).all():
            # Check if email already taken by another user
            if User.query.filter_by(email=student.email).first():
                click.echo(f'  ⚠️  Skipping {student.name}: email already registered.')
                skipped += 1
                continue
            user = User(
                email=student.email,
                role='student',
                is_active=True,
                must_change_password=True
            )
            user.set_password(student.roll_number)
            db.session.add(user)
            db.session.flush()
            student.user_id = user.id
            created += 1
        db.session.commit()
        click.echo(f'✅ Done — {created} accounts created, {skipped} skipped.')

    @app.cli.command('seed-data')
    def seed_data():
        """Seed default Classes, Subjects, and Exam types if they don't exist."""
        from models.academic import Class, Subject, Exam
        if not Class.query.first():
            click.echo('🌱 Seeding classes...')
            for name in ['5', '6', '7', '8', '9', '10', '11-Maths', '11-Science', '12-Maths', '12-Science']:
                db.session.add(Class(name=name))
            db.session.commit()

        if not Subject.query.first():
            click.echo('🌱 Seeding subjects...')
            for name, code in [
                ('Mathematics', 'MATH'), ('Science', 'SCI'), ('English', 'ENG'),
                ('History', 'HIST'), ('Physics', 'PHY'), ('Chemistry', 'CHEM'),
            ]:
                db.session.add(Subject(name=name, code=code))
            db.session.commit()

        if not Exam.query.first():
            click.echo('🌱 Seeding exam types...')
            for name in ['Unit Test 1', 'Unit Test 2', 'Mid-Term', 'Final Exam']:
                db.session.add(Exam(name=name, term='2025-26'))
            db.session.commit()
        click.echo('✅ Seed data complete.')


# ── ENTRY POINT ───────────────────────────────────────────────────────────────
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)