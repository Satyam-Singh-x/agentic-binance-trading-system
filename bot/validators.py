import re
from typing import Optional


class ValidationError(Exception):
    """Custom validation exception."""
    pass


def validate_symbol(symbol: str):
    if not symbol:
        raise ValidationError("Symbol cannot be empty.")

    if not re.match(r"^[A-Z0-9]+$", symbol.upper()):
        raise ValidationError("Symbol must be uppercase and alphanumeric (e.g., BTCUSDT).")


def validate_side(side: str):
    if side.upper() not in ["BUY", "SELL"]:
        raise ValidationError("Side must be either BUY or SELL.")


def validate_order_type(order_type: str):
    if order_type.upper() not in ["MARKET", "LIMIT"]:
        raise ValidationError("Order type must be MARKET or LIMIT.")


def validate_quantity(quantity: float):
    if quantity is None or quantity <= 0:
        raise ValidationError("Quantity must be greater than 0.")


def validate_price(order_type: str, price: Optional[float]):
    if order_type.upper() == "LIMIT":
        if price is None:
            raise ValidationError("Price is required for LIMIT orders.")
        if price <= 0:
            raise ValidationError("Price must be greater than 0.")


def validate_order(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float] = None,
):
    """
    Master validation function.
    Call this before executing any order.
    """

    validate_symbol(symbol)
    validate_side(side)
    validate_order_type(order_type)
    validate_quantity(quantity)
    validate_price(order_type, price)

    return True