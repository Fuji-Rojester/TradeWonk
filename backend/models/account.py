# backend/models/account.py
from __future__ import annotations # Ensure forward references work smoothly

from .. import db
from datetime import datetime, timezone
from decimal import Decimal
# Import List for type hinting relationships, TYPE_CHECKING to avoid circular imports at runtime
from typing import List, TYPE_CHECKING
# Import Mapped related components from SQLAlchemy ORM
from sqlalchemy.orm import Mapped, mapped_column, relationship
# Import specific SQL types
from sqlalchemy import String, Text, Integer, DateTime, ForeignKey, Boolean, Numeric, CheckConstraint

# Prevent circular imports for type hinting
if TYPE_CHECKING:
    from .portfolio import Portfolio
    from .transaction import Transaction

class Account(db.Model):
    """
    Represents a specific financial account (brokerage, crypto exchange, bank, manual)
    belonging to a Portfolio. Uses SQLAlchemy 2.0 Mapped annotation syntax.
    """
    __tablename__ = 'accounts'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    account_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    custodian: Mapped[str | None] = mapped_column(String(100), nullable=True)
    account_number_masked: Mapped[str | None] = mapped_column(String(20), nullable=True)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, index=True)
    cash_balance: Mapped[Decimal] = mapped_column(Numeric(18, 8), default=Decimal('0.0'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    last_synced_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)

    # Foreign Key
    portfolio_id: Mapped[int] = mapped_column(ForeignKey('portfolios.id'), nullable=False, index=True)

    # --- Relationships ---
    # Use back_populates for explicit bidirectional linking
    portfolio: Mapped["Portfolio"] = relationship(back_populates='accounts')
    transactions: Mapped[List["Transaction"]] = relationship(back_populates='account', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Account id={self.id} name={self.name} type={self.account_type} portfolio_id={self.portfolio_id}>'

    # --- Optional: Add methods later ---
    def get_total_value(self, target_currency: str) -> Decimal:
        # Placeholder implementation
        total_value = self.cash_balance
        print(f"WARN: get_total_value for Account {self.id} not fully implemented.")
        if self.currency == target_currency:
            return total_value
        else:
            print(f"WARN: Forex conversion needed but not implemented in get_total_value for Account {self.id}.")
            return total_value # Return unconverted cash for now

    def update_cash_balance(self, amount: Decimal):
        # Basic implementation
        if isinstance(amount, Decimal):
             self.cash_balance += amount
        else:
             self.cash_balance += Decimal(str(amount))
        print(f"Account {self.id} cash balance updated by {amount}, new balance: {self.cash_balance}")
        # Note: db.session.commit() should happen in the service/route, not here.

