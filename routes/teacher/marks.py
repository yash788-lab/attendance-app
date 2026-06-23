from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from models.academic import Class, Subject, Exam
from models.student import Student
from models.marks import Mark
from database import db
from . import teacher_bp
from utils.decorators import admin_or_teacher_required
from services.marks_service import MarksService


@teacher_bp.route('/marks/manage', methods=['GET', 'POST'])
@login_required
@admin_or_teacher_required
def manage_marks():
    classes = Class.query.order_by(Class.name).all()
    subjects = Subject.query.order_by(Subject.name).all()
    exams = Exam.query.order_by(Exam.term, Exam.name).all()

    class_id = request.args.get('class_id', type=int)
    subject_id = request.args.get('subject_id', type=int)
    exam_id = request.args.get('exam_id', type=int)

    students_list = []
    existing_marks = {}
    existing_max_marks = {}
    existing_remarks = {}

    if class_id and subject_id and exam_id:
        students_list = (
            Student.query
            .filter_by(class_id=class_id)
            .order_by(Student.roll_number)
            .all()
        )
        for s in students_list:
            m = Mark.query.filter_by(
                student_id=s.id, subject_id=subject_id, exam_id=exam_id
            ).first()
            if m:
                existing_marks[s.id] = m.marks_obtained
                existing_max_marks[s.id] = m.max_marks
                existing_remarks[s.id] = m.remarks

    if request.method == 'POST':
        cls_id = request.form.get('class_id', type=int)
        sub_id = request.form.get('subject_id', type=int)
        ex_id = request.form.get('exam_id', type=int)
        teacher_id = current_user.teacher_profile.id if current_user.role == 'teacher' else None

        students = Student.query.filter_by(class_id=cls_id).all()
        marks_data = []
        for s in students:
            marks_data.append({
                'student_id': s.id,
                'score': request.form.get(f'marks_{s.id}'),
                'max_score': request.form.get(f'max_marks_{s.id}', 100.0, type=float),
                'remarks': request.form.get(f'remarks_{s.id}', '').strip()
            })

        MarksService.save_marks(cls_id, sub_id, ex_id, marks_data, teacher_id)
        flash('Marks updated successfully!', 'success')
        return redirect(url_for('teacher.manage_marks', class_id=cls_id, subject_id=sub_id, exam_id=ex_id))

    return render_template(
        'teacher/manage_marks.html',
        classes=classes,
        subjects=subjects,
        exams=exams,
        class_id=class_id,
        subject_id=subject_id,
        exam_id=exam_id,
        students_list=students_list,
        existing_marks=existing_marks,
        existing_max_marks=existing_max_marks,
        existing_remarks=existing_remarks,
    )


@teacher_bp.route('/marks/student')
@login_required
def student_marks():
    student = current_user.student_profile
    if not student:
        from flask import abort
        abort(403)

    report = MarksService.get_student_marks_report(student.id)

    return render_template(
        'student/marks.html',
        student=student,
        **report
    )