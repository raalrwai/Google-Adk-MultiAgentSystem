# fastmcp_server.py
from fastmcp import FastMCP
from agents.agent import root_agent  

mcp = FastMCP(name="Stock MCP Server")

@mcp.tool
def get_stock_price_tool(ticker: str):
    return root_agent.tools[0](ticker)  

if __name__ == "__main__":
    print("Starting FastMCP server on default port 5000...")
    mcp.run()

