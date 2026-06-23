from database import db

class SiteConfig(db.Model):
    """
    Key-value store for site-wide configuration settings managed by admin.
    """
    __tablename__ = 'site_config'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False, index=True)
    value = db.Column(db.Text, nullable=True)
    
    @classmethod
    def get(cls, key, default=None):
        record = cls.query.filter_by(key=key).first()
        return record.value if record else default
    
    @classmethod
    def set(cls, key, value):
        record = cls.query.filter_by(key=key).first()
        if record:
            record.value = value
        else:
            record = cls(key=key, value=value)
            db.session.add(record)
        db.session.commit()
    
    @classmethod
    def get_all_as_dict(cls):
        return {r.key: r.value for r in cls.query.all()}

    def __repr__(self):
        return f'<SiteConfig {self.key}: {self.value}>'
