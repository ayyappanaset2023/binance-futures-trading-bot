# Binance Futures Testnet Trading Bot

A small Python CLI application that places **MARKET** and **LIMIT** orders on **Binance Futures Testnet (USDT-M)** with clean structure, input validation, logging, and error handling.

## Features

- Place **BUY** and **SELL** orders
- Supports:
  - `MARKET`
  - `LIMIT`
  - Bonus: `STOP_MARKET`
- CLI input validation using `argparse`
- Structured code with separate API/client, order logic, validation, and logging layers
- Logs API requests, responses, and errors to `logs/trading_bot.log`
- Handles invalid input, API failures, and network errors cleanly

## Project Structure

```text
trading_bot_project/
├── bot/
│   ├── __init__.py
│   ├── client.py
│   ├── logging_config.py
│   ├── orders.py
│   └── validators.py
├── logs/
│   ├── market_order.log
│   ├── limit_order.log
│   └── trading_bot.log
├── cli.py
├── .env.example
├── README.md
└── requirements.txt
```

## Setup

1. Create a Binance Futures Testnet account.
2. Generate Testnet API credentials.
3. Clone this repository or extract the zip.
4. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

5. Set your environment variables:

```bash
export BINANCE_API_KEY="your_testnet_api_key"
export BINANCE_API_SECRET="your_testnet_api_secret"
```

On Windows PowerShell:

```powershell
$env:BINANCE_API_KEY="your_testnet_api_key"
$env:BINANCE_API_SECRET="your_testnet_api_secret"
```

## How to Run

### 1) MARKET BUY order

```bash
python cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001
```

### 2) LIMIT SELL order

```bash
python cli.py --symbol BTCUSDT --side SELL --order-type LIMIT --quantity 0.001 --price 90000
```

### 3) Bonus: STOP_MARKET SELL order

```bash
python cli.py --symbol BTCUSDT --side SELL --order-type STOP_MARKET --quantity 0.001 --stop-price 85000
```

## Example Output

```text
Order Request Summary
---------------------
Symbol     : BTCUSDT
Side       : BUY
Order Type : MARKET
Quantity   : 0.001

Order Response Details
----------------------
orderId     : 123456789
status      : FILLED
executedQty : 0.001
avgPrice    : 84231.50

SUCCESS: Order placed successfully.
```

## Logging

Main logs are written to:

```text
logs/trading_bot.log
```

For submission convenience, copy or rename separate run logs as:

- `logs/market_order.log`
- `logs/limit_order.log`

Example commands:

```bash
cp logs/trading_bot.log logs/market_order.log
python cli.py --symbol BTCUSDT --side SELL --order-type LIMIT --quantity 0.001 --price 90000
cp logs/trading_bot.log logs/limit_order.log
```

## Assumptions

- The user will use valid Binance Futures Testnet credentials.
- Symbol and quantity precision depend on Binance symbol rules. This app validates general numeric correctness; Binance validates exchange-specific precision.
- Internet access is required to actually place orders.
- `avgPrice` may not always be populated depending on order state and API response.

## Submission Checklist

- Source code
- `README.md`
- `requirements.txt`
- `logs/market_order.log`
- `logs/limit_order.log`

## Notes

- Base URL used: `https://testnet.binancefuture.com`
- Order endpoint used: `POST /fapi/v1/order`
