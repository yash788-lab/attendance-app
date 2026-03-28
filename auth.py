from flask_login import UserMixin


# 👤 User class
class User(UserMixin):
    def __init__(self, id, role):
        self.id = str(id)
        self.role = role

    def get_id(self):
        return self.id
    
# ✅ SAFE TEACHER ID (must match app.py)
TEACHER_ID = -1

