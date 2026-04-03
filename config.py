import os

class Config:
    db_url = os.getenv("DATABASE_URL")

    # Render uses "postgres://", but SQLAlchemy 1.4+ requires "postgresql://"
    if db_url:
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql+pg8000://", 1)
        elif db_url.startswith("postgresql://"):
            db_url = db_url.replace("postgresql://", "postgresql+pg8000://", 1)

    SQLALCHEMY_DATABASE_URI = db_url or "sqlite:///attendance.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False