from database import db

class Admin(db.Model):
    """Admin profile — linked one-to-one with a User whose role='admin'."""
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        unique=True,
        nullable=False
    )
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))

    user = db.relationship('User', back_populates='admin_profile')

    def __repr__(self):
        return f'<Admin {self.name}>'
