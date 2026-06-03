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
        teacher = db.session.get(Teacher, teacher_id)
        if teacher:
            user = teacher.user
            db.session.delete(teacher)
            db.session.delete(user)
            db.session.commit()
            return True
        return False

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
