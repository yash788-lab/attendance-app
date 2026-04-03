from flask import Blueprint

main = Blueprint('main', __name__)

from . import auth_routes
from . import dashboard_routes
from . import student_routes
from . import attendance_routes
from . import marks_routes
from . import notification_routes