from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required

from models import Class, Subject, Exam, Student, Mark
from database import db
from . import main
from utils.decorators import teacher_required


@main.route('/marks/manage', methods=['GET', 'POST'])
@login_required
@teacher_required
def manage_marks():
    classes = Class.query.all()
    subjects = Subject.query.all()
    exams = Exam.query.all()

    class_id = request.args.get('class_id', type=int)
    subject_id = request.args.get('subject_id', type=int)
    exam_id = request.args.get('exam_id', type=int)

    students_list = []
    existing_marks = {}

    if class_id and subject_id and exam_id:
        students_list = Student.query.filter_by(class_id=class_id).all()
        for s in students_list:
            m = Mark.query.filter_by(
                student_id=s.id,
                subject_id=subject_id,
                exam_id=exam_id
            ).first()
            if m:
                existing_marks[s.id] = m.marks_obtained

    if request.method == 'POST':
        cls_id = request.form.get('class_id')
        sub_id = request.form.get('subject_id')
        ex_id = request.form.get('exam_id')

        students = Student.query.filter_by(class_id=cls_id).all()

        for s in students:
            score = request.form.get(f'marks_{s.id}')
            if score:
                mark = Mark.query.filter_by(
                    student_id=s.id,
                    subject_id=sub_id,
                    exam_id=ex_id
                ).first()

                if mark:
                    mark.marks_obtained = float(score)
                else:
                    db.session.add(Mark(
                        student_id=s.id,
                        subject_id=sub_id,
                        exam_id=ex_id,
                        marks_obtained=float(score)
                    ))

        db.session.commit()
        flash("Marks updated!", "success")

    return render_template('manage_marks.html', **locals())