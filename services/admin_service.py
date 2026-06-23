from models.user import User
from models.admin import Admin
from models.teacher import Teacher
from models.student import Student
from models.academic import Class, Subject, Exam
from database import db

class AdminService:
    @staticmethod
    def approve_teacher(teacher_id):
        teacher = db.session.get(Teacher, teacher_id)
        if teacher:
            teacher.is_approved = True
            teacher.user.is_active = True
            db.session.commit()
            return True, teacher
        return False, None

    @staticmethod
    def reject_teacher(teacher_id):
        """Used for rejecting a NEW registration (simple delete)."""
        teacher = db.session.get(Teacher, teacher_id)
        if teacher:
            user = teacher.user
            db.session.delete(teacher)
            if user:
                db.session.delete(user)
            db.session.commit()
            return True
        return False

    @staticmethod
    def delete_teacher(teacher_id):
        """Permanent removal of an APPROVED teacher with cleanup of relations."""
        teacher = db.session.get(Teacher, teacher_id)
        if not teacher:
            return False, "Teacher not found"
        
        name = teacher.name
        user = teacher.user

        # Circular dependencies cleanup
        from models.academic import ClassSubject
        from models.attendance import Attendance
        from models.marks import Mark
        from models.homework import Homework
        from models.communication import Announcement, Event, Poll, PollVote

        ClassSubject.query.filter_by(teacher_id=teacher.id).update({ClassSubject.teacher_id: None})
        Attendance.query.filter_by(marked_by=teacher.id).update({Attendance.marked_by: None})
        Mark.query.filter_by(entered_by=teacher.id).update({Mark.entered_by: None})
        Homework.query.filter_by(teacher_id=teacher.id).delete()

        if user:
            Announcement.query.filter_by(created_by=user.id).delete()
            Event.query.filter_by(created_by=user.id).delete()
            PollVote.query.filter_by(user_id=user.id).delete()
            Poll.query.filter_by(created_by=user.id).delete()
            db.session.delete(user)
        else:
            db.session.delete(teacher)

        db.session.commit()
        return True, name

    @staticmethod
    def add_student(name, father_name, class_id, roll_number, email, phone):
        student = Student(
            name=name, father_name=father_name, class_id=class_id,
            roll_number=roll_number, email=email, phone=phone
        )
        db.session.add(student)
        db.session.flush()

        if not User.query.filter_by(email=email).first():
            user = User(email=email, role='student', is_active=True, must_change_password=True)
            user.set_password(roll_number)
            db.session.add(user)
            db.session.flush()
            student.user_id = user.id

        db.session.commit()
        return student

    @staticmethod
    def delete_student(student_id):
        student = db.session.get(Student, student_id)
        if student:
            db.session.delete(student)
            db.session.commit()
            return True, student.name
        return False, None

    @staticmethod
    def add_class(name, academic_year):
        if Class.query.filter_by(name=name).first():
            return False
        db.session.add(Class(name=name, academic_year=academic_year))
        db.session.commit()
        return True

    @staticmethod
    def add_subject(name, code):
        db.session.add(Subject(name=name, code=code))
        db.session.commit()
        return True

    @staticmethod
    def add_exam(name, term):
        db.session.add(Exam(name=name, term=term))
        db.session.commit()
        return True
