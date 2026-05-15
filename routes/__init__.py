from flask import Blueprint

main = Blueprint('main', __name__)

from . import auth_routes        # noqa: E402, F401
from . import dashboard_routes   # noqa: E402, F401
from . import admin_routes       # noqa: E402, F401
from . import attendance_routes  # noqa: E402, F401
from . import marks_routes       # noqa: E402, F401
from . import notification_routes  # noqa: E402, F401
from . import student_routes     # noqa: E402, F401