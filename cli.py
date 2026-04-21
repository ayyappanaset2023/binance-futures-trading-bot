from __future__ import annotations

import argparse
import sys

from bot.client import BinanceAPIError, BinanceFuturesClient, BinanceNetworkError
from bot.logging_config import setup_logging
from bot.orders import OrderRequest, format_order_response, format_order_summary, place_order
from bot.validators import (
    ValidationError,
    normalize_symbol,
    validate_order_type,
    validate_positive_decimal,
    validate_price,
    validate_side,
    validate_stop_price,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Place Binance Futures Testnet orders from the command line."
    )
    parser.add_argument("--symbol", required=True, help="Trading symbol, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, help="BUY or SELL")
    parser.add_argument(
        "--order-type",
        required=True,
        choices=["MARKET", "LIMIT", "STOP_MARKET"],
        help="Order type",
    )
    parser.add_argument("--quantity", required=True, help="Order quantity")
    parser.add_argument("--price", help="Price for LIMIT orders")
    parser.add_argument("--stop-price", help="Stop price for STOP_MARKET orders")
    return parser


def parse_order(args: argparse.Namespace) -> OrderRequest:
    order_type = validate_order_type(args.order_type)
    return OrderRequest(
        symbol=normalize_symbol(args.symbol),
        side=validate_side(args.side),
        order_type=order_type,
        quantity=validate_positive_decimal(args.quantity, "quantity"),
        price=validate_price(args.price, order_type),
        stop_price=validate_stop_price(args.stop_price, order_type),
    )


def main() -> int:
    logger = setup_logging()
    parser = build_parser()
    args = parser.parse_args()

    try:
        order = parse_order(args)
        client = BinanceFuturesClient.from_env()
        client.ping()

        print(format_order_summary(order))
        response = place_order(client, order, logger)
        print()
        print(format_order_response(response))
        print("\nSUCCESS: Order placed successfully.")
        return 0

    except ValidationError as exc:
        logger.error("Validation error: %s", exc)
        print(f"FAILED: Invalid input - {exc}", file=sys.stderr)
        return 2
    except BinanceAPIError as exc:
        logger.error("API error: %s", exc)
        print(f"FAILED: Binance API error - {exc}", file=sys.stderr)
        return 3
    except BinanceNetworkError as exc:
        logger.error("Network error: %s", exc)
        print(f"FAILED: Network error - {exc}", file=sys.stderr)
        return 4
    except Exception as exc:  # pragma: no cover
        logger.exception("Unexpected error")
        print(f"FAILED: Unexpected error - {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
