import os
import re

base_dir = r"c:\Users\dmand\OneDrive\Documents\attendance-app\templates"
base_dir_routes = r"c:\Users\dmand\OneDrive\Documents\attendance-app\routes"

# Mappings of old function names to new blueprint namespaces
auth_funcs = ['login', 'logout', 'admin_login', 'student_login', 'teacher_register', 'change_password']
admin_funcs = ['admin_dashboard', 'admin_teachers', 'approve_teacher', 'reject_teacher', 
               'admin_students', 'admin_add_student', 'admin_delete_student', 'admin_classes', 
               'admin_add_class', 'admin_subjects', 'admin_add_subject', 'admin_exams', 'admin_add_exam']
teacher_funcs = ['students', 'add_student', 'delete_student', 'mark_attendance', 
                 'attendance_reports', 'manage_marks', 'view_notifications', 'dashboard'] # Assume teacher dashboard mostly
public_funcs = ['index', 'home', 'about', 'academics', 'facilities', 'gallery', 'contact']

def replace_in_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    def replacer(match):
        func = match.group(1)
        if func in auth_funcs:
            return f"url_for('auth.{func}'"
        elif func in admin_funcs:
            return f"url_for('admin.{func}'"
        elif func in teacher_funcs:
            if func == 'view_notifications':
                # Actually wait, view_notifications might be for both.
                pass
            return f"url_for('teacher.{func}'"
        elif func in public_funcs:
            if func == 'index':
                return f"url_for('public.home'"
            return f"url_for('public.{func}'"
        elif func == 'student_attendance':
            return f"url_for('student.attendance'"
        elif func == 'student_marks':
            return f"url_for('student.marks'"
        return match.group(0) # Keep original if not matched

    # The regex targets url_for('main.func_name'
    new_content = re.sub(r"url_for\(['\"]main\.([^'\"]+)['\"]", replacer, content)

    if new_content != original_content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {path}")

for directory in [base_dir, base_dir_routes]:
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html') or file.endswith('.py'):
                replace_in_file(os.path.join(root, file))

print("URL replacement complete.")
