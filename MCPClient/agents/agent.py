from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
import yfinance as yf
import requests
def resolve_ticker(query: str):
    """
    Resolves company names or partial matches into a valid ticker.
    Args: query -> str
    """
    query = query.strip()

    # If user already provided a ticker
    if query.isalpha() and query.isupper():
        return query

    # Try direct yfinance search API
    try:
        url = f"https://query2.finance.yahoo.com/v1/finance/search?q={query}"
        data = requests.get(url, timeout=5).json()

        if "quotes" in data and len(data["quotes"]) > 0:
            ticker = data["quotes"][0]["symbol"]
            return ticker.upper()
    except Exception:
        pass

    return None  # Could not resolve


def get_stock_price(ticker: str) -> dict:
    """
    Fetch the current stock price for a given ticker or company name.
    """

    # First normalize to a real ticker
    symbol = resolve_ticker(ticker)

    if symbol is None:
        return {
            "ok": False,
            "ticker": ticker,
            "error": f"Could not find a ticker symbol matching '{ticker}'."
        }

    try:
        stock = yf.Ticker(symbol)

        # Use safe access — never throws KeyError
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


base_agent = Agent(
    name="root_agent",
    description="A helpful stock price assistant.",
    # model=LiteLlm(model="ollama_chat/gemma3:27b"),
    model = "gemma-3-27b-it",
    # model = "gemini-2.5-flash",
    instruction=(
        """
        You are a helpful stock price assistant. Your job is to answer questions user might have on stocks
        You have access to one tool:
        - get_stock_price: Takes one argument `ticker` as string and output a dict

        Standard of Operation:
        1. Call the get_stock_price tool.
        2. If the tool returned ok=True, summarize the ticker and price.
        3. If the tool returned ok=False or an error, return it back to the user.
        
        If you ar unsure or lose, just ask the user for more information.
        """
    ),
    tools=[get_stock_price],
)

root_agent = base_agent