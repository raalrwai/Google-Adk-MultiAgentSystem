from fastmcp import FastMCP
from tools.getStockPrice import get_stock_price
from tools.searchGoogle import google_search

mcp = FastMCP(name="Stock MCP Server")

@mcp.tool
def get_stock_price_tool(ticker: str):
    print("[FastMCP] Tool invoked:", ticker)
    return get_stock_price(ticker)

@mcp.tool
def google_search_tool(query: str):
    print("[FastMCP] Tool invoked:", query)
    return google_search(query)

if __name__ == "__main__":
    # NOTE: Specify HTTP transport here
    print("Starting FastMCP HTTP server on http://127.0.0.1:5000/mcp …")
    mcp.run(transport="http", host="127.0.0.1", port=5000)

