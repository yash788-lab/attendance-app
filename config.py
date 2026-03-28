import os

class Config:
    db_url = os.getenv("DATABASE_URL")

    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql+psycopg2://", 1)

    SQLALCHEMY_DATABASE_URI = db_url or "sqlite:///attendance.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False