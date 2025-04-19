from __future__ import annotations  # Ensure forward references work smoothly

from .. import db
from datetime import datetime, timezone
from typing import List, TYPE_CHECKING, Optional  # <-- Add Optional here
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Integer, DateTime, ForeignKey

if TYPE_CHECKING:
    from .user import User
    from .account import Account

class Portfolio(db.Model):
    __tablename__ = 'portfolios'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Use Optional here
    base_currency: Mapped[str] = mapped_column(String(3), nullable=False, default='USD', index=True)
    benchmark_ticker: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, index=True)  # Use Optional here
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False, index=True)

    # --- Relationships ---
    user: Mapped["User"] = relationship(back_populates='portfolios')
    accounts: Mapped[List["Account"]] = relationship(back_populates='portfolio', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Portfolio id={self.id} name={self.name} user_id={self.user_id}>'
