# backend/models/asset.py
from __future__ import annotations # Ensure forward references work smoothly

from .. import db
from datetime import datetime, timezone, date
from decimal import Decimal
import enum
# Import Mapped related components from SQLAlchemy ORM
from sqlalchemy.orm import Mapped, mapped_column, relationship
# Import specific SQL types
from sqlalchemy import Numeric, BigInteger, Date, Enum as SQLAlchemyEnum, String, Text, Integer, DateTime, ForeignKey, Boolean
from typing import List, TYPE_CHECKING # Import List

# Prevent circular imports for type hinting
if TYPE_CHECKING:
    from .transaction import Transaction # Needed if adding relationship back from Asset
    from .lot import Lot # Needed if adding relationship back from Asset

class Asset(db.Model):
    """
    Base model for all types of assets. Uses joined table inheritance
    and SQLAlchemy 2.0 Mapped annotation syntax.
    """
    __tablename__ = 'assets'

    id: Mapped[int] = mapped_column(primary_key=True)
    asset_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # Discriminator
    symbol: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, index=True)
    exchange: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    icon_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships back from Transaction/Lot will define access
    # transactions: Mapped[List["Transaction"]] = relationship(back_populates='asset')
    # lots: Mapped[List["Lot"]] = relationship(back_populates='asset')

    __mapper_args__ = {
        'polymorphic_identity': 'asset',
        'polymorphic_on': asset_type
    }

    def __repr__(self):
        display_type = self.asset_type.capitalize() if self.asset_type else 'Asset'
        return f'<{display_type} id={self.id} symbol={self.symbol}>'

# --- Specific Asset Type Subclasses ---

class Stock(Asset):
    __tablename__ = 'stocks'
    id: Mapped[int] = mapped_column(ForeignKey('assets.id'), primary_key=True)
    sector: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    industry: Mapped[str | None] = mapped_column(String(100), nullable=True)
    market_cap: Mapped[Decimal | None] = mapped_column(Numeric(20, 2), nullable=True)
    country: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)

    __mapper_args__ = {'polymorphic_identity': 'STOCK'}

    def __repr__(self):
        base_repr = super().__repr__()
        return f'{base_repr[:-1]}, sector={self.sector}>'

class CryptoCurrency(Asset):
    __tablename__ = 'cryptocurrencies'
    id: Mapped[int] = mapped_column(ForeignKey('assets.id'), primary_key=True)
    algorithm: Mapped[str | None] = mapped_column(String(50), nullable=True)
    circulating_supply: Mapped[Decimal | None] = mapped_column(Numeric(30, 8), nullable=True)
    max_supply: Mapped[Decimal | None] = mapped_column(Numeric(30, 8), nullable=True)

    __mapper_args__ = {'polymorphic_identity': 'CRYPTO'}

class ETF(Asset):
    __tablename__ = 'etfs'
    id: Mapped[int] = mapped_column(ForeignKey('assets.id'), primary_key=True)
    issuer: Mapped[str | None] = mapped_column(String(100), nullable=True)
    expense_ratio: Mapped[Decimal | None] = mapped_column(Numeric(6, 4), nullable=True)
    underlying_index: Mapped[str | None] = mapped_column(String(100), nullable=True)
    asset_class: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)

    __mapper_args__ = {'polymorphic_identity': 'ETF'}

class OptionTypeEnum(enum.Enum):
    CALL = 'CALL'
    PUT = 'PUT'

class OptionContract(Asset):
    __tablename__ = 'option_contracts'
    id: Mapped[int] = mapped_column(ForeignKey('assets.id'), primary_key=True)
    underlying_asset_id: Mapped[int] = mapped_column(ForeignKey('assets.id'), nullable=False, index=True)
    option_type: Mapped[OptionTypeEnum] = mapped_column(SQLAlchemyEnum(OptionTypeEnum, name="option_type_enum"), nullable=False)
    strike_price: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False)
    expiration_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    delta: Mapped[Decimal | None] = mapped_column(Numeric(10, 8), nullable=True)
    gamma: Mapped[Decimal | None] = mapped_column(Numeric(10, 8), nullable=True)
    theta: Mapped[Decimal | None] = mapped_column(Numeric(10, 8), nullable=True)
    vega: Mapped[Decimal | None] = mapped_column(Numeric(10, 8), nullable=True)
    implied_volatility: Mapped[Decimal | None] = mapped_column(Numeric(10, 8), nullable=True)

    # Define relationship to the underlying asset
    underlying: Mapped["Asset"] = relationship('Asset', foreign_keys=[underlying_asset_id])

    # --- UPDATED __mapper_args__ ---
    __mapper_args__ = {
        'polymorphic_identity': 'OPTION',
        # Explicitly tell SQLAlchemy how to join assets and option_contracts for inheritance
        'inherit_condition': (id == Asset.id) # Use the 'id' column from both tables
    }
    # --- END UPDATE ---


class Bond(Asset):
    __tablename__ = 'bonds'
    id: Mapped[int] = mapped_column(ForeignKey('assets.id'), primary_key=True)
    issuer: Mapped[str | None] = mapped_column(String(100), nullable=True)
    maturity_date: Mapped[date | None] = mapped_column(Date, nullable=True, index=True)
    coupon_rate: Mapped[Decimal | None] = mapped_column(Numeric(8, 5), nullable=True)
    credit_rating: Mapped[str | None] = mapped_column(String(10), nullable=True)
    bond_type: Mapped[str | None] = mapped_column(String(50), nullable=True)

    __mapper_args__ = {'polymorphic_identity': 'BOND'}

class CashCurrency(Asset):
    __tablename__ = 'cash_currencies'
    id: Mapped[int] = mapped_column(ForeignKey('assets.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'CASH'}

