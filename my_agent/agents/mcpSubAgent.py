from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams

MCP_SERVER_URL = "http://127.0.0.1:5000/mcp"  

mcp_sub_agent = Agent(
    name="mcp_sub_agent",
    description="A sub‑agent that calls tools from a FastMCP server.",
    model="gemma-3-27b-it",  
    instruction="""
        You are a specialist agent that must use remote MCP tools.

        You have access to the following tools on the MCP server:
        - get_stock_price_tool(ticker: str): returns stock price info
        - google_search_tool(query: str): performs a web search for a query

        Your task: ALWAYS follow exactly this pattern:
        1. Determine the best single tool to call for the user’s request.
        2. Call that tool using the correct parameter(s).
        3. Once the tool returns, you must produce *exactly ONE* natural language response
           that incorporates the tool’s returned information.
        4. DO NOT stop after generating the function call — the function call must be
           executed by MCP and the result used to write your final answer.

        Important:
        - If the user’s request clearly asks for a stock price, call get_stock_price_tool.
        - If the user’s request clearly asks you to look something up, call google_search_tool.
        - Do not call more than one tool per user query.
        - Do not generate further transfer_to_agent actions.
        - Do not return raw JSON — you must produce a human-readable sentence.
    """,
    tools=[
        MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url=MCP_SERVER_URL
            ),
        )
    ]
)
