from database import db
from models.marks import Mark
from models.academic import Subject, Exam
from services.notification_service import NotificationService

class MarksService:
    @staticmethod
    def save_marks(class_id, subject_id, exam_id, student_marks_data, teacher_id=None):
        """
        Saves or updates marks for multiple students in a class/subject/exam.
        student_marks_data: list of dicts {student_id, score, max_score, remarks}
        """
        for data in student_marks_data:
            s_id = data['student_id']
            score = data['score']
            max_score = data.get('max_score', 100.0)
            remarks = data.get('remarks', '').strip()
            
            if score is not None and score != '':
                mark = Mark.query.filter_by(
                    student_id=s_id, subject_id=subject_id, exam_id=exam_id
                ).first()
                
                if mark:
                    mark.marks_obtained = float(score)
                    mark.max_marks = float(max_score)
                    mark.remarks = remarks
                    if teacher_id:
                        mark.entered_by = teacher_id
                else:
                    db.session.add(Mark(
                        student_id=s_id,
                        subject_id=subject_id,
                        exam_id=exam_id,
                        marks_obtained=float(score),
                        max_marks=float(max_score),
                        remarks=remarks,
                        entered_by=teacher_id,
                    ))
        
        db.session.commit()
        
        # Trigger Notifications
        exam = db.session.get(Exam, exam_id)
        subject = db.session.get(Subject, subject_id)
        NotificationService.notify_marks_published(
            class_id=class_id,
            exam_name=exam.name if exam else 'an exam',
            subject_name=subject.name if subject else 'a subject'
        )
        return True

    @staticmethod
    def get_student_marks_report(student_id):
        """Generates comprehensive marks analytics for a student."""
        marks = (
            Mark.query
            .filter_by(student_id=student_id)
            .join(Subject).join(Exam)
            .order_by(Exam.name, Subject.name)
            .all()
        )

        if not marks:
            return {
                'marks': [], 'overall_avg': 0, 'total_subjects': 0, 'total_exams': 0,
                'best_subject': None, 'exams_grouped': {}, 'exams_summary': {},
                'subject_avg': [], 'grade_dist': {}, 'grade_chart_data': {'labels': [], 'values': []}
            }

        # Grouping
        exams_grouped = {}
        for m in marks:
            exams_grouped.setdefault(m.exam.name, []).append(m)

        exams_summary = {}
        for exam_name, exam_marks in exams_grouped.items():
            exams_summary[exam_name] = {
                'obtained': sum(m.marks_obtained for m in exam_marks),
                'max': sum(m.max_marks for m in exam_marks),
            }

        subject_buckets = {}
        for m in marks:
            subject_buckets.setdefault(m.subject.name, []).append(m.percentage)
        
        subject_avg = [
            {'name': name, 'avg': round(sum(pcts) / len(pcts), 1)}
            for name, pcts in subject_buckets.items()
        ]
        subject_avg.sort(key=lambda x: x['avg'], reverse=True)

        best_subject = max(marks, key=lambda m: m.percentage)
        overall_avg = round(sum(m.percentage for m in marks) / len(marks), 1)

        grade_order = ['A+', 'A', 'B+', 'B', 'C', 'D', 'F']
        grade_dist = {g: 0 for g in grade_order}
        for m in marks:
            grade_dist[m.grade] = grade_dist.get(m.grade, 0) + 1
            
        grade_chart_data = {
            'labels': [g for g in grade_order if grade_dist[g] > 0],
            'values': [grade_dist[g] for g in grade_order if grade_dist[g] > 0],
        }

        return {
            'marks': marks,
            'overall_avg': overall_avg,
            'total_subjects': len(subject_buckets),
            'total_exams': len(exams_grouped),
            'best_subject': best_subject,
            'exams_grouped': exams_grouped,
            'exams_summary': exams_summary,
            'subject_avg': subject_avg,
            'grade_dist': grade_dist,
            'grade_chart_data': grade_chart_data,
        }
