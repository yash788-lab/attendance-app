from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from models.academic import Class, Subject, Exam
from models.student import Student
from models.marks import Mark
from database import db
from . import main
from utils.decorators import admin_or_teacher_required


@main.route('/marks/manage', methods=['GET', 'POST'])
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

    if request.method == 'POST':
        cls_id = request.form.get('class_id', type=int)
        sub_id = request.form.get('subject_id', type=int)
        ex_id = request.form.get('exam_id', type=int)

        # Determine who is entering marks
        teacher_id = None
        if current_user.role == 'teacher' and current_user.teacher_profile:
            teacher_id = current_user.teacher_profile.id

        students = (
            Student.query
            .filter_by(class_id=cls_id)
            .order_by(Student.roll_number)
            .all()
        )
        for s in students:
            score = request.form.get(f'marks_{s.id}')
            max_score = request.form.get(f'max_marks_{s.id}', 100.0, type=float)
            if score:
                mark = Mark.query.filter_by(
                    student_id=s.id, subject_id=sub_id, exam_id=ex_id
                ).first()
                if mark:
                    mark.marks_obtained = float(score)
                    mark.max_marks = float(max_score)
                    if teacher_id:
                        mark.entered_by = teacher_id
                else:
                    db.session.add(Mark(
                        student_id=s.id,
                        subject_id=sub_id,
                        exam_id=ex_id,
                        marks_obtained=float(score),
                        max_marks=float(max_score),
                        entered_by=teacher_id,
                    ))

        db.session.commit()
        flash('Marks updated successfully!', 'success')

    return render_template('teacher/manage_marks.html', **locals())


@main.route('/marks/student')
@login_required
def student_marks():
    student = current_user.student_profile
    if not student:
        from flask import abort
        abort(403)

    marks = (
        Mark.query
        .filter_by(student_id=student.id)
        .join(Subject).join(Exam)
        .order_by(Exam.name, Subject.name)
        .all()
    )
    return render_template('student/marks.html', marks=marks, student=student)