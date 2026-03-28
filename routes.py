from flask import Blueprint, render_template, session, request, redirect, url_for, flash, abort
from database import db
from models import Student, Attendance, Class
from datetime import datetime, date
from flask_login import current_user, login_user, logout_user, login_required
from app import User, TEACHER_ID  # ✅ IMPORTANT
from functools import wraps

main = Blueprint('main', __name__)

# ✅ ADMIN KEYS
ADMIN_KEYS = ['12345678', '87654321', '11223344']

# ✅ SAFE TEACHER ID (must match app.py)
TEACHER_ID = -1


# =========================
# 🔐 ROLE-BASED DECORATOR
# =========================
def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'teacher':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


# =========================
# 🔐 STUDENT LOGIN
@main.route('/login', methods=['GET', 'POST'])
def login():
    from models import Class

    classes = Class.query.all()

    if request.method == 'POST':
        class_id = request.form.get('class_id')
        roll_number = request.form.get('roll_number')
        email = request.form.get('email')

        if not class_id or not roll_number or not email:
            flash("All fields are required", "error")
            return redirect(url_for('main.login'))

        student = Student.query.filter_by(
            class_id=class_id,
            roll_number=roll_number,
            email=email
        ).first()

        if student:
            user = User(id=student.id, role='student')
            login_user(user)

            return redirect(url_for('main.index'))
        else:
            flash("Invalid credentials", "error")

    return render_template('student_login.html', classes=classes)

# =========================
# 🔐 ADMIN LOGIN
# =========================
@main.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    # ✅ Prevent accessing login if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        password = request.form.get('password')
        print("Entered password:", password)

        if password == "admin123":   # replace later with secure method
            user = User(id=TEACHER_ID, role='teacher')

            remember = True if request.form.get('remember') else False
            login_user(user, remember=remember)

            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        else:
            flash("Invalid Admin Password", "error")

    return render_template('admin_login.html')
# =========================
# 🚪 LOGOUT
# =========================
@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


# =========================
# 🏠 DASHBOARD
# =========================
@main.route('/')
@login_required
def index():

    # 👨‍🏫 TEACHER DASHBOARD
    if current_user.role == 'teacher':
        return render_template('index.html')

    # 👨‍🎓 STUDENT DASHBOARD
    elif current_user.role == 'student':
        student = Student.query.get(int(current_user.id))

    # 🔹 Get filter inputs
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        query = Attendance.query.filter_by(student_id=student.id)

        if start_date:
            query = query.filter(
                Attendance.date >= datetime.strptime(start_date, '%Y-%m-%d').date()
        )

        if end_date:
            query = query.filter(
            Attendance.date <= datetime.strptime(end_date, '%Y-%m-%d').date()
        )

    # 🔹 Full records (filtered or all)
        records = query.order_by(Attendance.date.desc()).all()

    # 🔹 Last 10 records (no filter)
        recent_records = Attendance.query.filter_by(
            student_id=student.id
        ).order_by(Attendance.date.desc()).limit(10).all()

        return render_template(
            'student_dashboard.html',
            records=records,
            recent_records=recent_records,
            start_date=start_date,
            end_date=end_date
    )
# =========================
# 👥 VIEW STUDENTS
# =========================
@main.route('/students')
@login_required
@teacher_required
def students():
    all_students = Student.query.join(Class).order_by(
        Class.name,
        Student.roll_number
    ).all()

    return render_template('students.html', students=all_students)


# =========================
# ➕ ADD STUDENT
# =========================
@main.route('/student/add', methods=['GET', 'POST'])
@login_required
@teacher_required
def add_student():
    if request.method == 'POST':
        name = request.form.get('name')
        class_id = request.form.get('class_id')
        roll_number = request.form.get('roll_number')
        email = request.form.get('email')

        if not name or not class_id or not roll_number or not email:
            flash('All fields are required!', 'error')
            return redirect(url_for('main.add_student'))

        existing_student = Student.query.filter_by(
            class_id=class_id,
            roll_number=roll_number
        ).first()

        if existing_student:
            flash('Student already exists!', 'error')
            return redirect(url_for('main.add_student'))

        new_student = Student(
            name=name,
            class_id=class_id,
            roll_number=roll_number,
            email=email
        )

        db.session.add(new_student)
        db.session.commit()

        flash(f'Student {name} added!', 'success')
        return redirect(url_for('main.students'))
    classes = Class.query.all()

    return render_template('add_student.html', classes=classes)


# =========================
# ❌ DELETE STUDENT
# =========================
@main.route('/student/delete/<int:student_id>')
@login_required
@teacher_required
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)

    db.session.delete(student)
    db.session.commit()

    flash(f'Student {student.name} deleted!', 'success')
    return redirect(url_for('main.students'))

@main.route('/select-class', methods=['POST'])
@login_required
@teacher_required
def select_class():
    selected_class = request.form.get('class_id')

    # Store in session (easy way)
    session['selected_class'] = selected_class

    flash(f"Class {selected_class} selected", "success")

    return redirect(url_for('main.index'))


# =========================
# ✅ MARK ATTENDANCE
# =========================
@main.route('/attendance/mark', methods=['GET', 'POST'])
@login_required
@teacher_required
def mark_attendance():

    classes = Class.query.all()

    selected_class_id = request.args.get('class_id', type=int)

    if request.method == 'POST':
        attendance_date = request.form.get('date')
        selected_class_id = request.form.get('class_id', type=int)

        if attendance_date:
            attendance_date = datetime.strptime(attendance_date, '%Y-%m-%d').date()
        else:
            attendance_date = date.today()

        # ✅ FILTER STUDENTS BY CLASS
        students = Student.query.filter_by(class_id=selected_class_id).all()

        for student in students:
            status = request.form.get(f'status_{student.id}')
            remarks = request.form.get(f'remarks_{student.id}')

            if status:
                existing = Attendance.query.filter_by(
                    student_id=student.id,
                    date=attendance_date
                ).first()

                if existing:
                    existing.status = status
                    existing.remarks = remarks
                else:
                    new_attendance = Attendance(
                        student_id=student.id,
                        date=attendance_date,
                        status=status,
                        remarks=remarks
                    )
                    db.session.add(new_attendance)

        db.session.commit()
        flash('Attendance marked successfully!', 'success')

        return redirect(url_for('main.mark_attendance', class_id=selected_class_id))

    # ✅ GET request
    students = []
    existing_attendance = {}

    if selected_class_id:
        students = Student.query.filter_by(class_id=selected_class_id).order_by(
            Student.roll_number
        ).all()

        selected_date = request.args.get('date')
        if selected_date:
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        else:
            selected_date = date.today()

        for student in students:
            record = Attendance.query.filter_by(
                student_id=student.id,
                date=selected_date
            ).first()

            if record:
                existing_attendance[student.id] = record
    else:
        selected_date = date.today()

    return render_template(
        'mark_attendance.html',
        students=students,
        classes=classes,
        selected_class_id=selected_class_id,
        selected_date=selected_date,
        existing_attendance=existing_attendance
    )
# =========================
# 📋 VIEW ATTENDANCE
# =========================
@main.route('/attendance/view')
@login_required
def view_attendance():

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    class_id = request.args.get('class_id', type=int)

    if current_user.role == 'student':
        query = Attendance.query.filter_by(student_id=int(current_user.id))
        students = None
        classes = None
    else:
        query = Attendance.query

        student_id = request.args.get('student_id', type=int)

        if student_id:
            query = query.filter_by(student_id=student_id)

        if class_id:
            query = query.join(Student).filter(Student.class_id == class_id)

        students = Student.query.order_by(Student.name).all()
        classes = Class.query.all()

    if start_date:
        query = query.filter(
            Attendance.date >= datetime.strptime(start_date, '%Y-%m-%d').date()
        )

    if end_date:
        query = query.filter(
            Attendance.date <= datetime.strptime(end_date, '%Y-%m-%d').date()
        )

    records = query.order_by(Attendance.date.desc()).all()

    return render_template(
        'view_attendance.html',
        records=records,
        students=students,
        classes=classes,
        start_date=start_date,
        end_date=end_date
    )