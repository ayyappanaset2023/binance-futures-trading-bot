from __future__ import annotations

from decimal import Decimal, InvalidOperation

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP_MARKET"}


class ValidationError(ValueError):
    """Raised when CLI inputs are invalid."""


def normalize_symbol(symbol: str) -> str:
    clean = symbol.strip().upper()
    if not clean or not clean.isalnum():
        raise ValidationError("symbol must be a non-empty alphanumeric value, e.g. BTCUSDT")
    return clean


def validate_side(side: str) -> str:
    clean = side.strip().upper()
    if clean not in VALID_SIDES:
        raise ValidationError(f"side must be one of: {', '.join(sorted(VALID_SIDES))}")
    return clean


def validate_order_type(order_type: str) -> str:
    clean = order_type.strip().upper()
    if clean not in VALID_ORDER_TYPES:
        raise ValidationError(
            f"order type must be one of: {', '.join(sorted(VALID_ORDER_TYPES))}"
        )
    return clean


def validate_positive_decimal(value: str | float, field_name: str) -> str:
    try:
        decimal_value = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValidationError(f"{field_name} must be a valid number") from exc

    if decimal_value <= 0:
        raise ValidationError(f"{field_name} must be greater than 0")
    return format(decimal_value.normalize(), "f")


def validate_price(price: str | float | None, order_type: str) -> str | None:
    if order_type == "LIMIT" and price is None:
        raise ValidationError("price is required for LIMIT orders")
    if order_type != "LIMIT" and price is None:
        return None
    return validate_positive_decimal(price, "price")


def validate_stop_price(stop_price: str | float | None, order_type: str) -> str | None:
    if order_type == "STOP_MARKET" and stop_price is None:
        raise ValidationError("stop-price is required for STOP_MARKET orders")
    if stop_price is None:
        return None
    return validate_positive_decimal(stop_price, "stop-price")
