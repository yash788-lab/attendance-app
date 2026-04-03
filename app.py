import os
import time
from flask import Flask, redirect, url_for, session
from flask_login import LoginManager, current_user, logout_user
from flask_migrate import Migrate
from sqlalchemy import inspect

# Local imports
from config import Config
from database import db
from models import Student, Class, Subject, Exam
from auth import User, TEACHER_ID

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-123')

    # 1. Initialize Database & Migrations
    db.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        print("--- 🚀 SMS System Initialization Starting ---")
        
        # Create all tables (only creates what doesn't exist)
        db.create_all()
        print("✅ Tables checked/created.")

        # --- 🛡️ SENIOR DEVELOPER SAFETY NET: Schema Update ---
        # This manually adds 'father_name' if it's missing from your existing DB
        inspector = inspect(db.engine)
        columns = [c['name'] for c in inspector.get_columns('students')]
        if 'father_name' not in columns:
            print("⚠️ Column 'father_name' missing. Attempting to add...")
            try:
                # Use text() for direct SQL execution
                db.session.execute(db.text('ALTER TABLE students ADD COLUMN father_name VARCHAR(100)'))
                db.session.commit()
                print("✅ 'father_name' column added successfully.")
            except Exception as e:
                db.session.rollback()
                print(f"❌ Failed to add column: {e}")

        # --- 🧬 SEEDING LOGIC ---
        
        # Seed Classes
        if not Class.query.first():
            print("🌱 Seeding Classes...")
            class_list = ["5", "6", "7", "8", "9", "10", "11-maths", "11-science", "12-maths", "12-science"]
            for c in class_list:
                db.session.add(Class(name=c))
            db.session.commit()

        # Seed Subjects
        if not Subject.query.first():
            print("🌱 Seeding Subjects...")
            subjects = ['Mathematics', 'Science', 'English', 'History', 'Physics', 'Chemistry']
            for s in subjects:
                db.session.add(Subject(name=s))
            db.session.commit()

        # Seed Exams
        if not Exam.query.first():
            print("🌱 Seeding Exam Types...")
            exams = [('Unit Test 1', '2025-26'), ('Mid-Term', '2025-26'), ('Final Exam', '2025-26')]
            for name, term in exams:
                db.session.add(Exam(name=name, term=term))
            db.session.commit()
            
        print("--- ✨ Database Initialization Complete ---")

    # 2. Login Manager Configuration
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    login_manager.session_protection = "strong"

    # 3. Session Management (Inactivity Timeout)
    @app.before_request
    def session_management():
        if not current_user.is_authenticated:
            return
        
        session.permanent = True
        now = time.time()

        # Set timeout: Teacher (1hr), Student (10min)
        timeout = 3600 if current_user.role == 'teacher' else 600

        if 'last_activity' in session:
            elapsed = now - session['last_activity']
            if elapsed > timeout:
                logout_user()
                session.clear()
                return redirect(url_for('main.login'))

        session['last_activity'] = now

    # 4. Register Blueprints
    from routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

# --- USER LOADER ---
@login_manager.user_loader
def load_user(user_id):
    try:
        user_id = int(user_id)
        if user_id == TEACHER_ID:
            return User(id=TEACHER_ID, role='teacher')
        
        # Use session.get() for SQLAlchemy 2.0 compatibility
        student = db.session.get(Student, user_id)
        if student:
            return User(id=student.id, role='student')
    except (ValueError, TypeError):
        return None
    return None

# --- RUN APP ---
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    # Note: Use use_reloader=False if you are debugging startup issues to avoid double-logging
    app.run(host="0.0.0.0", port=port, debug=True)