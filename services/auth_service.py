from models.user import User
from database import db
from flask_login import login_user, logout_user

class AuthService:
    @staticmethod
    def login(email, password, remember=False):
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            return True, user
        return False, None

    @staticmethod
    def logout():
        logout_user()
