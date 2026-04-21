from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from .client import BinanceFuturesClient


@dataclass
class OrderRequest:
    symbol: str
    side: str
    order_type: str
    quantity: str
    price: str | None = None
    stop_price: str | None = None
    time_in_force: str = "GTC"


def build_payload(order: OrderRequest) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "symbol": order.symbol,
        "side": order.side,
        "type": order.order_type,
        "quantity": order.quantity,
        "newOrderRespType": "RESULT",
    }

    if order.order_type == "LIMIT":
        payload["price"] = order.price
        payload["timeInForce"] = order.time_in_force
    elif order.order_type == "STOP_MARKET":
        payload["stopPrice"] = order.stop_price
        payload["workingType"] = "MARK_PRICE"

    return payload


def place_order(client: BinanceFuturesClient, order: OrderRequest, logger: logging.Logger) -> dict[str, Any]:
    payload = build_payload(order)
    logger.info("Order request payload: %s", payload)
    response = client.place_order(payload)
    logger.info("Order response payload: %s", response)
    return response


def format_order_summary(order: OrderRequest) -> str:
    lines = [
        "Order Request Summary",
        "---------------------",
        f"Symbol     : {order.symbol}",
        f"Side       : {order.side}",
        f"Order Type : {order.order_type}",
        f"Quantity   : {order.quantity}",
    ]
    if order.price:
        lines.append(f"Price      : {order.price}")
    if order.stop_price:
        lines.append(f"Stop Price : {order.stop_price}")
    return "\n".join(lines)


def format_order_response(response: dict[str, Any]) -> str:
    avg_price = response.get("avgPrice") or response.get("price") or "N/A"
    return "\n".join(
        [
            "Order Response Details",
            "----------------------",
            f"orderId     : {response.get('orderId', 'N/A')}",
            f"status      : {response.get('status', 'N/A')}",
            f"executedQty : {response.get('executedQty', 'N/A')}",
            f"avgPrice    : {avg_price}",
        ]
    )
