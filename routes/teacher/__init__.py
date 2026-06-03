from flask import Blueprint

teacher_bp = Blueprint('teacher', __name__)

from . import dashboard, attendance, marks, students, notifications, homework
