from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from models.academic import Class, Subject, Exam
from models.student import Student
from models.marks import Mark
from services.notification_service import NotificationService
from database import db
from . import teacher_bp
from utils.decorators import admin_or_teacher_required


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
            remarks = request.form.get(f'remarks_{s.id}', '').strip()
            
            if score:
                mark = Mark.query.filter_by(
                    student_id=s.id, subject_id=sub_id, exam_id=ex_id
                ).first()
                if mark:
                    mark.marks_obtained = float(score)
                    mark.max_marks = float(max_score)
                    mark.remarks = remarks
                    if teacher_id:
                        mark.entered_by = teacher_id
                else:
                    db.session.add(Mark(
                        student_id=s.id,
                        subject_id=sub_id,
                        exam_id=ex_id,
                        marks_obtained=float(score),
                        max_marks=float(max_score),
                        remarks=remarks,
                        entered_by=teacher_id,
                    ))

        db.session.commit()
        
        # Trigger notification
        exam = Exam.query.get(ex_id)
        subject = Subject.query.get(sub_id)
        NotificationService.notify_marks_published(
            class_id=cls_id,
            exam_name=exam.name if exam else 'an exam',
            subject_name=subject.name if subject else 'a subject'
        )
        
        flash('Marks updated successfully!', 'success')

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

    marks = (
        Mark.query
        .filter_by(student_id=student.id)
        .join(Subject).join(Exam)
        .order_by(Exam.name, Subject.name)
        .all()
    )

    if not marks:
        return render_template('student/marks.html', marks=[], student=student,
                               overall_avg=0, total_subjects=0, total_exams=0,
                               best_subject=None, exams_grouped={}, exams_summary={},
                               subject_avg=[], grade_dist={}, grade_chart_data={'labels':[], 'values':[]})

    # ── Group by exam ──────────────────────────────────────────────────────────
    exams_grouped = {}
    for m in marks:
        exams_grouped.setdefault(m.exam.name, []).append(m)

    # ── Exam-wise summary ──────────────────────────────────────────────────────
    exams_summary = {}
    for exam_name, exam_marks in exams_grouped.items():
        exams_summary[exam_name] = {
            'obtained': sum(m.marks_obtained for m in exam_marks),
            'max':      sum(m.max_marks for m in exam_marks),
        }

    # ── Subject-wise average ───────────────────────────────────────────────────
    subject_buckets = {}
    for m in marks:
        subject_buckets.setdefault(m.subject.name, []).append(m.percentage)
    subject_avg = [
        {'name': name, 'avg': round(sum(pcts) / len(pcts), 1)}
        for name, pcts in subject_buckets.items()
    ]
    subject_avg.sort(key=lambda x: x['avg'], reverse=True)

    # ── Best subject ───────────────────────────────────────────────────────────
    best_subject = max(marks, key=lambda m: m.percentage) if marks else None

    # ── Overall average ────────────────────────────────────────────────────────
    overall_avg = round(sum(m.percentage for m in marks) / len(marks), 1)

    # ── Grade distribution ─────────────────────────────────────────────────────
    grade_order = ['A+', 'A', 'B+', 'B', 'C', 'D', 'F']
    grade_dist = {g: 0 for g in grade_order}
    for m in marks:
        grade_dist[m.grade] = grade_dist.get(m.grade, 0) + 1
    grade_chart_data = {
        'labels': [g for g in grade_order if grade_dist[g] > 0],
        'values': [grade_dist[g] for g in grade_order if grade_dist[g] > 0],
    }

    return render_template(
        'student/marks.html',
        student=student,
        marks=marks,
        overall_avg=overall_avg,
        total_subjects=len(subject_buckets),
        total_exams=len(exams_grouped),
        best_subject=best_subject,
        exams_grouped=exams_grouped,
        exams_summary=exams_summary,
        subject_avg=subject_avg,
        grade_dist=grade_dist,
        grade_chart_data=grade_chart_data,
    )