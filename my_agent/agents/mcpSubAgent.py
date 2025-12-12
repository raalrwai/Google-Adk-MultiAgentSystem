from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams

MCP_SERVER_URL = "http://127.0.0.1:5000/mcp"  # Full endpoint URL for MCP

mcp_sub_agent = Agent(
    name="mcp_sub_agent",
    description="A sub‑agent that calls tools from a FastMCP server.",
    model="gemma-3-27b-it",  # or another model
    instruction="""
        You are a specialist agent that must use remote MCP tools.
        Use the tools exposed by the MCP server for any task that requires tool access.
    """,
    tools=[
        MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url=MCP_SERVER_URL
            ),
            # Optional: filter list of tools, e.g. ["get_stock_price_tool"]
        )
    ]
)
