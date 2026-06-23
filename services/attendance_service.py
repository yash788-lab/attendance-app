from database import db
from models.attendance import Attendance
from datetime import date

class AttendanceService:
    @staticmethod
    def get_attendance_for_class_on_date(class_id, selected_date):
        """Returns a mapping of student_id -> Attendance record."""
        # This part is still mostly used for display, could stay in route or move here.
        pass

    @staticmethod
    def save_attendance(student_id_status_map, selected_date, teacher_id=None):
        """
        Saves or updates attendance for multiple students.
        student_id_status_map: dict of {student_id: (status, remarks)}
        """
        for student_id, (status, remarks) in student_id_status_map.items():
            if not status:
                continue
                
            existing = Attendance.query.filter_by(
                student_id=student_id, date=selected_date
            ).first()
            
            if existing:
                existing.status = status
                existing.remarks = remarks
                if teacher_id:
                    existing.marked_by = teacher_id
            else:
                db.session.add(Attendance(
                    student_id=student_id,
                    date=selected_date,
                    status=status,
                    remarks=remarks,
                    marked_by=teacher_id,
                ))
        
        db.session.commit()
        return True
