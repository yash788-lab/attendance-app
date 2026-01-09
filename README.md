# 📚 Attendance Tracking System

A comprehensive web-based attendance tracking application built with Python, Flask, and SQLite. This system enables efficient student attendance management with automated percentage calculations and detailed report generation.

## ✨ Features

- **Student Management**
  - Add, view, and delete students
  - Store student information (name, roll number, email)
  
- **Attendance Tracking**
  - Mark daily attendance (Present/Absent/Late)
  - Add remarks for each attendance record
  - View attendance history with filtering options
  
- **Automated Calculations**
  - Real-time attendance percentage calculation
  - Period-based statistics (daily, weekly, monthly)
  
- **Report Generation**
  - Generate comprehensive attendance reports
  - Export reports to Excel format (.xlsx)
  - Filter reports by date range
  - Visual indicators for attendance percentages

## 🛠️ Tech Stack

- **Backend**: Python 3.x, Flask
- **Database**: SQLite
- **ORM**: Flask-SQLAlchemy
- **Excel Export**: OpenPyXL
- **Frontend**: HTML5, CSS3 (embedded styling)

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## 🚀 Installation & Setup

1. **Clone or download this project**
   ```bash
   cd "Attendence tracker Application"
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open your web browser
   - Navigate to: `http://127.0.0.1:5000`

## 📖 Usage Guide

### Adding Students
1. Navigate to "Students" from the main menu
2. Click "Add Student"
3. Fill in student details (name, roll number, email)
4. Submit the form

### Marking Attendance
1. Go to "Mark Attendance"
2. Select the date (defaults to today)
3. Mark status for each student (Present/Absent/Late)
4. Add optional remarks
5. Save attendance

### Viewing Records
1. Click on "View Records"
2. Apply filters:
   - Filter by student
   - Filter by date range
3. View detailed attendance history

### Generating Reports
1. Navigate to "Reports"
2. Select start and end dates
3. Click "Generate Report" to view summary
4. Click "Export Excel" to download the report

## 📊 Database Schema

### Students Table
- `id`: Primary key
- `name`: Student name
- `roll_number`: Unique roll number
- `email`: Email address
- `created_at`: Timestamp

### Attendance Table
- `id`: Primary key
- `student_id`: Foreign key to Students
- `date`: Attendance date
- `status`: Present/Absent/Late
- `remarks`: Optional notes
- `created_at`: Timestamp

## 🎯 Resume-Ready Description

**Attendance Tracking System | Python, Flask, SQLite**
• Built a web-based attendance tracking application with automated percentage calculation
• Implemented CRUD operations for student management and attendance records
• Developed report generation system with Excel export functionality using OpenPyXL
• Designed responsive UI with real-time statistics and visual indicators
• Utilized Flask-SQLAlchemy ORM for efficient database operations

## 📁 Project Structure

```
Attendence tracker Application/
├── app.py                 # Main application file
├── config.py             # Configuration settings
├── models.py             # Database models
├── routes.py             # Application routes
├── requirements.txt      # Python dependencies
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   ├── index.html       # Dashboard
│   ├── students.html    # Students list
│   ├── add_student.html # Add student form
│   ├── mark_attendance.html  # Mark attendance
│   ├── view_attendance.html  # View records
│   └── reports.html     # Reports page
└── attendance.db        # SQLite database (created on first run)
```

## 🔧 Configuration

Edit `config.py` to customize:
- Database URI
- Secret key
- Other Flask configurations

## 🌟 Key Learning Points

- Flask web framework and routing
- SQLAlchemy ORM for database operations
- Database design and relationships
- CRUD operations implementation
- Form handling and validation
- File generation and downloads
- Date and time handling
- Report generation and data export

## 🐛 Troubleshooting

**Database errors**: Delete `attendance.db` and restart the application to recreate the database.

**Port already in use**: Change the port in `app.py`:
```python
app.run(debug=True, port=5001)
```

**Module not found**: Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## 📝 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Feel free to fork this project and add your own features!

## 👨‍💻 Author

Built as a learning project to demonstrate proficiency in Flask web development and database management.

---

**Note**: This is a beginner-friendly project perfect for learning web development fundamentals and demonstrating practical programming skills in job interviews.
