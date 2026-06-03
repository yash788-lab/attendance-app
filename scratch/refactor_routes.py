import os
import re

base_dir = r"c:\Users\dmand\OneDrive\Documents\attendance-app\routes"

def move_and_replace(filename, dest_dir, dest_filename, bp_name):
    src = os.path.join(base_dir, filename)
    dest_path = os.path.join(base_dir, dest_dir, dest_filename)
    
    if not os.path.exists(src):
        return
        
    with open(src, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace from . import main -> from . import bp_name
    content = re.sub(r'from \.\s+import main', f'from . import {bp_name}_bp', content)
    
    # Replace @main.route -> @bp_name.route
    content = content.replace('@main.route', f'@{bp_name}_bp.route')
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    os.remove(src)

# auth
move_and_replace('auth_routes.py', 'auth', 'routes.py', 'auth')

# admin
move_and_replace('admin_routes.py', 'admin', 'routes.py', 'admin')

# teacher
move_and_replace('attendance_routes.py', 'teacher', 'attendance.py', 'teacher')
move_and_replace('marks_routes.py', 'teacher', 'marks.py', 'teacher')
move_and_replace('student_routes.py', 'teacher', 'students.py', 'teacher')
move_and_replace('notification_routes.py', 'teacher', 'notifications.py', 'teacher')

# remove dashboard_routes since we extracted it manually
dashboard_src = os.path.join(base_dir, 'dashboard_routes.py')
if os.path.exists(dashboard_src):
    os.remove(dashboard_src)

print("Routes moved successfully.")
