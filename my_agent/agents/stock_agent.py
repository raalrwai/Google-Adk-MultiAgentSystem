
from google.adk.agents.llm_agent import Agent
import yfinance as yf
import requests

def resolve_ticker(query: str):
    query = query.strip()

    if query.isalpha() and query.isupper():
        return query

    try:
        url = f"https://query2.finance.yahoo.com/v1/finance/search?q={query}"
        data = requests.get(url, timeout=5).json()
        if "quotes" in data and len(data["quotes"]) > 0:
            return data["quotes"][0]["symbol"].upper()
    except Exception:
        pass

    return None

def get_stock_price(ticker: str) -> dict:
    symbol = resolve_ticker(ticker)
    if symbol is None:
        return {"ok": False, "ticker": ticker, "error": f"No ticker for '{ticker}'."}

    try:
        stock = yf.Ticker(symbol)
        price = getattr(stock.fast_info, "last_price", None)
        if price is None:
            return {"ok": False, "ticker": symbol, "error": "No price available."}
        return {"ok": True, "ticker": symbol, "price": price}
    except Exception as e:
        return {"ok": False, "ticker": symbol, "error": str(e)}

stock_agent = Agent(
    name="stock_agent",
    description="Specialist for stock price lookups.",
    model="gemma-3-27b-it",
    instruction="""
You are the stock specialist. When asked about a stock price or ticker,
use get_stock_price to fetch the price and return a structured result.
""",
    tools=[get_stock_price]
)
