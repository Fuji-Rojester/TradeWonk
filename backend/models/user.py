from __future__ import annotations  # Ensures forward references work smoothly

from .. import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    # Use Mapped and mapped_column for primary key
    id: Mapped[int] = mapped_column(primary_key=True)
    # Use Mapped and mapped_column for other columns, specifying type hints
    username: Mapped[str] = mapped_column(db.String(64), index=True, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(db.String(120), index=True, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(db.String(256), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc), nullable=False)
    email_verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    last_login_at: Mapped[datetime | None] = mapped_column(nullable=True)

    # --- Relationships ---
    # Use Mapped for relationship type hint
    portfolios: Mapped[List["Portfolio"]] = relationship("Portfolio", back_populates="user", lazy="dynamic", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User id={self.id} username={self.username} email={self.email}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_email=True):
        user_data = {
            "id": self.id,
            "username": self.username,
            "created_at": self.created_at.isoformat() + 'Z' if self.created_at else None,
            "email_verified": self.email_verified,
            "last_login_at": self.last_login_at.isoformat() + 'Z' if self.last_login_at else None
        }
        if include_email:
            user_data["email"] = self.email
        return user_data
