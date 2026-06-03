import click
from flask import Flask

def register_seed_commands(app: Flask, db):
    @app.cli.command('seed-admin')
    @click.option('--name', default='Admin', help='Admin display name')
    @click.option('--email', prompt=True, help='Admin email address')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='Admin password')
    def seed_admin(name, email, password):
        """Create the first admin account (run once after initial migration)."""
        from models.user import User
        from models.admin import Admin
        if User.query.filter_by(email=email).first():
            click.echo(f'⚠️  A user with email "{email}" already exists.')
            return
        user = User(email=email, role='admin', is_active=True)
        user.set_password(password)
        db.session.add(user)
        db.session.flush()
        admin = Admin(user_id=user.id, name=name)
        db.session.add(admin)
        db.session.commit()
        click.echo(f'✅ Admin account created: {email}')

    @app.cli.command('seed-student-accounts')
    def seed_student_accounts():
        """Create User accounts for all existing students who don't have one.
        Default password = roll_number. Students are prompted to change on first login.
        """
        from models.user import User
        from models.student import Student
        created = 0
        skipped = 0
        for student in Student.query.filter_by(user_id=None).all():
            if User.query.filter_by(email=student.email).first():
                click.echo(f'  ⚠️  Skipping {student.name}: email already registered.')
                skipped += 1
                continue
            user = User(
                email=student.email,
                role='student',
                is_active=True,
                must_change_password=True
            )
            user.set_password(student.roll_number)
            db.session.add(user)
            db.session.flush()
            student.user_id = user.id
            created += 1
        db.session.commit()
        click.echo(f'✅ Done — {created} accounts created, {skipped} skipped.')

    @app.cli.command('seed-data')
    def seed_data():
        """Seed default Classes, Subjects, and Exam types if they don't exist."""
        from models.academic import Class, Subject, Exam
        if not Class.query.first():
            click.echo('🌱 Seeding classes...')
            for name in ['5', '6', '7', '8', '9', '10', '11-Maths', '11-Science', '12-Maths', '12-Science']:
                db.session.add(Class(name=name))
            db.session.commit()

        if not Subject.query.first():
            click.echo('🌱 Seeding subjects...')
            for name, code in [
                ('Mathematics', 'MATH'), ('Science', 'SCI'), ('English', 'ENG'),
                ('History', 'HIST'), ('Physics', 'PHY'), ('Chemistry', 'CHEM'),
            ]:
                db.session.add(Subject(name=name, code=code))
            db.session.commit()

        if not Exam.query.first():
            click.echo('🌱 Seeding exam types...')
            for name in ['Unit Test 1', 'Unit Test 2', 'Mid-Term', 'Final Exam']:
                db.session.add(Exam(name=name, term='2025-26'))
            db.session.commit()
        click.echo('✅ Seed data complete.')
