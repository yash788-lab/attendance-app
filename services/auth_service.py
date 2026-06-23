from models.user import User
from database import db
from flask_login import login_user, logout_user

class AuthService:
    @staticmethod
    def authenticate(email, password):
        """Standard credential check. Returns (User, error_message)."""
        user = User.query.filter_by(email=email.strip().lower()).first()
        if not user or not user.check_password(password):
            return None, 'Invalid email or password.'
        if not user.is_active:
            return None, 'Your account is inactive. Please contact the admin.'
        return user, None

    @staticmethod
    def login(user, remember=False):
        login_user(user, remember=remember)

    @staticmethod
    def logout():
        logout_user()

    @staticmethod
    def register_teacher(name, email, phone, password):
        """Initial inactive teacher registration."""
        if User.query.filter_by(email=email).first():
            return None, 'An account with this email already exists.'
        
        user = User(email=email, role='teacher', is_active=False)
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        from models.teacher import Teacher
        teacher = Teacher(user_id=user.id, name=name, phone=phone, is_approved=False)
        db.session.add(teacher)
        db.session.commit()
        return user, None
