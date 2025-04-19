# backend/models/__init__.py

# Import all the models defined in this directory
# This makes them known to SQLAlchemy/Flask-Migrate when the 'models' package is imported

from .user import User
from .portfolio import Portfolio
from .account import Account
# Import the base Asset and all specific asset types AND Enums defined in asset.py
from .asset import (
    Asset, Stock, CryptoCurrency, ETF,
    OptionContract, OptionTypeEnum, # <-- Import OptionTypeEnum here
    Bond, CashCurrency
)
# Import Transaction model and its specific Enum
from .transaction import Transaction, TransactionTypeEnum
from .lot import Lot

# Optional: Define __all__ to control what 'from .models import *' imports
__all__ = [
    'User',
    'Portfolio',
    'Account',
    'Asset',
    'Stock',
    'CryptoCurrency',
    'ETF',
    'OptionContract',
    'OptionTypeEnum', # <-- Added OptionTypeEnum here
    'Bond',
    'CashCurrency',
    'Transaction',
    'TransactionTypeEnum',
    'Lot'
]

