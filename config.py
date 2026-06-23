import os


class Config:
    # ── Security ──────────────────────────────────────────────────────────────
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-prod')

    # ── Database ──────────────────────────────────────────────────────────────
    _db_url = os.getenv('DATABASE_URL', '')

    # Render provides "postgres://..." — SQLAlchemy 1.4+ requires "postgresql://"
    # We also force the pg8000 driver which is pure-Python (no libpq needed on Render)
    if _db_url.startswith('postgres://'):
        _db_url = _db_url.replace('postgres://', 'postgresql+pg8000://', 1)
    elif _db_url.startswith('postgresql://') and '+' not in _db_url.split('://')[0]:
        _db_url = _db_url.replace('postgresql://', 'postgresql+pg8000://', 1)

    SQLALCHEMY_DATABASE_URI = _db_url or 'sqlite:///attendance.db'
    
    # Vercel Compatibility: Serverless environments are read-only.
    # If we are on Vercel and using SQLite, we must use /tmp
    if os.environ.get('VERCEL') == '1' and SQLALCHEMY_DATABASE_URI.startswith('sqlite:///'):
        SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/attendance.db'
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False