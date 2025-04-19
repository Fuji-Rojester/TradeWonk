from __future__ import annotations  # Ensure forward references work smoothly

import enum
from .. import db
from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy import Enum as SQLAlchemyEnum, Numeric, ForeignKey, String, Text, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, Optional  # Import Optional

if TYPE_CHECKING:
    from .account import Account
    from .asset import Asset
    from .lot import Lot

class TransactionTypeEnum(enum.Enum):
    BUY = 'BUY'
    SELL = 'SELL'
    DIVIDEND_CASH = 'DIVIDEND_CASH'
    DIVIDEND_STOCK = 'DIVIDEND_STOCK'
    INTEREST = 'INTEREST'
    FEE = 'FEE'
    COMMISSION = 'COMMISSION'
    DEPOSIT = 'DEPOSIT'
    WITHDRAWAL = 'WITHDRAWAL'
    STOCK_SPLIT = 'STOCK_SPLIT'
    OPTION_BUY = 'OPTION_BUY'
    OPTION_SELL = 'OPTION_SELL'
    OPTION_EXPIRE = 'OPTION_EXPIRE'
    OPTION_ASSIGN = 'OPTION_ASSIGN'
    BOND_COUPON = 'BOND_COUPON'
    BOND_MATURITY = 'BOND_MATURITY'

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey('accounts.id'), nullable=False, index=True)
    asset_id: Mapped[Optional[int]] = mapped_column(ForeignKey('assets.id'), nullable=True, index=True)  # Use Optional

    transaction_type: Mapped[TransactionTypeEnum] = mapped_column(SQLAlchemyEnum(TransactionTypeEnum, name="transaction_type_enum"), nullable=False, index=True)
    transaction_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True, default=lambda: datetime.now(timezone.utc))
    quantity: Mapped[Optional[Decimal]] = mapped_column(Numeric(24, 8), nullable=True)  # Use Optional
    price_per_unit: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 8), nullable=True)  # Use Optional
    commission: Mapped[Decimal] = mapped_column(Numeric(12, 4), nullable=True, default=Decimal('0.0'))
    fees: Mapped[Decimal] = mapped_column(Numeric(12, 4), nullable=True, default=Decimal('0.0'))
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    strategy_tag: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)  # Use Optional
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Use Optional

    # --- Relationships ---
    account: Mapped["Account"] = relationship(back_populates='transactions')
    asset: Mapped[Optional["Asset"]] = relationship()  # Use Optional for nullable relationship

    lot_created: Mapped[Optional["Lot"]] = relationship("Lot", back_populates='buy_transaction')

    def __repr__(self):
        asset_symbol = self.asset.symbol if self.asset else 'N/A'
        return f'<Transaction id={self.id} type={self.transaction_type.name} account={self.account_id} asset={asset_symbol} qty={self.quantity} time={self.transaction_time}>'
