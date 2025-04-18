from .. import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin # Import UserMixin
from datetime import datetime, timezone

# Inherit from UserMixin *and* db.Model
class User(UserMixin, db.Model):
    """
    Represents a user in the application.
    Stores authentication details and links to user-specific data.
    Includes UserMixin for Flask-Login integration.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # --- Relationships (Add later) ---
    #portfolios = db.relationship('Portfolio', backref='owner', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User id={self.id} username={self.username} email={self.email}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)

    # Flask-Login uses the 'id' field provided by UserMixin by default,
    # which points to our primary key 'id'. No extra methods needed here.