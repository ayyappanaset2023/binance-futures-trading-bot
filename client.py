from __future__ import annotations

import hashlib
import hmac
import os
import time
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode

import requests


class BinanceAPIError(Exception):
    """Raised when Binance returns an API error."""


class BinanceNetworkError(Exception):
    """Raised when network-related issues occur."""


@dataclass
class BinanceFuturesClient:
    api_key: str
    api_secret: str
    base_url: str = "https://testnet.binancefuture.com"
    timeout: int = 15

    @classmethod
    def from_env(cls) -> "BinanceFuturesClient":
        api_key = os.getenv("BINANCE_API_KEY", "").strip()
        api_secret = os.getenv("BINANCE_API_SECRET", "").strip()
        if not api_key or not api_secret:
            raise BinanceAPIError(
                "Missing BINANCE_API_KEY or BINANCE_API_SECRET environment variables"
            )
        return cls(api_key=api_key, api_secret=api_secret)

    def _sign_params(self, params: dict[str, Any]) -> dict[str, Any]:
        params = {k: v for k, v in params.items() if v is not None}
        params["timestamp"] = int(time.time() * 1000)
        query_string = urlencode(params, doseq=True)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = signature
        return params

    def _request(self, method: str, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        signed = self._sign_params(params or {})
        headers = {"X-MBX-APIKEY": self.api_key}
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=signed,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise BinanceNetworkError(f"Network error while calling Binance: {exc}") from exc

        try:
            data = response.json()
        except ValueError:
            data = {"raw": response.text}

        if response.status_code >= 400:
            msg = data.get("msg", response.text)
            code = data.get("code", response.status_code)
            raise BinanceAPIError(f"Binance API error {code}: {msg}")
        return data

    def place_order(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", "/fapi/v1/order", payload)

    def ping(self) -> dict[str, Any]:
        try:
            response = requests.get(f"{self.base_url}/fapi/v1/ping", timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            raise BinanceNetworkError(f"Unable to reach Binance Testnet: {exc}") from exc
