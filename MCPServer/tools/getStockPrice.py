# stock_tools.py

import yfinance as yf
import requests

def resolve_ticker(query: str) -> str | None:
    """
    Resolves a company name or query into a valid ticker symbol.
    Returns the ticker (uppercase) or None if not found.
    """
    query = query.strip()

    # If already looks like a ticker (all uppercase letters)
    if query.isalpha() and query.isupper():
        return query

    # Use Yahoo Finance search
    try:
        url = f"https://query2.finance.yahoo.com/v1/finance/search?q={query}"
        data = requests.get(url, timeout=5).json()
        if "quotes" in data and len(data["quotes"]) > 0:
            return data["quotes"][0]["symbol"].upper()
    except Exception:
        pass

    return None


def get_stock_price(ticker: str) -> dict:
    """
    Get the current stock price for a given ticker or company query.
    Returns a dict: {ok, ticker, price, error?}
    """
    symbol = resolve_ticker(ticker)
    if symbol is None:
        return {
            "ok": False,
            "ticker": ticker,
            "error": f"Could not find a ticker matching '{ticker}'."
        }

    try:
        stock = yf.Ticker(symbol)
        # fast_info.last_price is safe and clearer than nested attribute access
        price = getattr(stock.fast_info, "last_price", None)

        if price is None:
            return {
                "ok": False,
                "ticker": symbol,
                "error": f"No price data available for {symbol}."
            }

        return {
            "ok": True,
            "ticker": symbol,
            "price": price
        }
    except Exception as e:
        return {
            "ok": False,
            "ticker": symbol,
            "error": str(e)
        }
