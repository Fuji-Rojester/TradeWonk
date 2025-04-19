# backend/models/lot.py
from __future__ import annotations  # Ensure forward references work smoothly

from .. import db
from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy import Numeric, ForeignKey, CheckConstraint, String, Text, Integer, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, Optional  # Import Optional

if TYPE_CHECKING:
    from .account import Account
    from .asset import Asset
    from .transaction import Transaction

class Lot(db.Model):
    __tablename__ = 'lots'

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey('accounts.id'), nullable=False, index=True)
    asset_id: Mapped[Optional[int]] = mapped_column(ForeignKey('assets.id'), nullable=True, index=True)  # Use Optional

    buy_transaction_id: Mapped[int] = mapped_column(ForeignKey('transactions.id'), unique=True, nullable=False, index=True)

    purchase_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    purchase_quantity: Mapped[Decimal] = mapped_column(Numeric(24, 8), nullable=False)
    quantity_remaining: Mapped[Decimal] = mapped_column(Numeric(24, 8), nullable=False, index=True)
    cost_basis_per_unit: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False)
    is_open: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)

    # --- Relationships ---
    account: Mapped["Account"] = relationship()  # Define relationship to Account
    asset: Mapped[Optional["Asset"]] = relationship()  # Use Optional for nullable relationship

    buy_transaction: Mapped["Transaction"] = relationship(back_populates='lot_created')

    # --- Constraints ---
    __table_args__ = (
        CheckConstraint('quantity_remaining >= 0', name='ck_lot_quantity_remaining_non_negative'),
        CheckConstraint('quantity_remaining <= purchase_quantity', name='ck_lot_quantity_remaining_lte_purchase'),
    )

    def __repr__(self):
        status = "Open" if self.is_open else "Closed"
        return f'<Lot id={self.id} asset_id={self.asset_id} qty_rem={self.quantity_remaining}/{self.purchase_quantity} cost_pu={self.cost_basis_per_unit} status={status}>'
