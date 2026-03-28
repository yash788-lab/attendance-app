from flask import Flask, redirect, url_for, session
from config import Config
from database import db
from flask_login import LoginManager, UserMixin, current_user, logout_user
from models import Student, Class
from datetime import timedelta
import time

login_manager = LoginManager()

# 👤 User class
class User(UserMixin):
    def __init__(self, id, role):
        self.id = str(id)
        self.role = role

    def get_id(self):
        return self.id


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    app.config['SECRET_KEY'] = 'your-secret-key'

    # ⏱️ Session timeout config
    
    db.init_app(app)

    with app.app_context():
        db.create_all()
        if not Class.query.first():
            class_list = [
            "5", "6", "7", "8", "9", "10",
            "11-maths", "11-science", "11-commerce",
            "12-maths", "12-science", "12-commerce"
        ]

            for c in class_list:
                new_class = Class(name=c)
                db.session.add(new_class)

        db.session.commit()

    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    login_manager.session_protection = "strong"

    # ✅ THIS MUST BE INSIDE create_app()
    @app.before_request
    def session_management():
        if not current_user.is_authenticated:
            return
        
        session.permanent = True

        now = time.time()

        # ✅ Set timeout based on role
        if current_user.role == 'teacher':
            timeout = 3600   # 1 hour
        else:
            timeout = 600   # 10 minutes

        if 'last_activity' in session:
            elapsed = now - session['last_activity']

            if elapsed > timeout:
                logout_user()
                session.clear()
                return redirect(url_for('main.login'))

        session['last_activity'] = now

    # ✅ register routes
    from routes import main
    app.register_blueprint(main)

    return app


# 🔐 Teacher ID
TEACHER_ID = -1


@login_manager.user_loader
def load_user(user_id):
    user_id = int(user_id)

    if user_id == TEACHER_ID:
        return User(id=TEACHER_ID, role='teacher')

    student = Student.query.get(user_id)
    if student:
        return User(id=student.id, role='student')

    return None

app = create_app()
if __name__ == '__main__':
    app.run(debug=True)