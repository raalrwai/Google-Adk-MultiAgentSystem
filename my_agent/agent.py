from google.adk.agents.llm_agent import Agent
from .agents.mcpSubAgent import mcp_sub_agent
from google.adk.tools.agent_tool import AgentTool
from .agents.sentimentSubAgent import sentiment_agent

ROOT_MANAGER_INSTR = """
You are the manager agent responsible for routing queries and invoking specialized tools.

You have access to:
- mcp_sub_agent: specialist sub‑agent that can call MCP tools (get_stock_price_tool and google_search_tool)
- sentiment_agent_tool: a tool that wraps a sentiment analysis agent

You also have access to the session state and session history (`session.events`).
session.events is a chronological list of all past message events (user and assistant).
session.state is a dictionary where you can store flags like sentiment_done.

Follow these rules exactly:

1. If the user’s query is about stock prices or tickers (e.g., “Price of AAPL?”),
   delegate to mcp_sub_agent using get_stock_price_tool.

2. If the user’s query involves a web search (e.g., “search for latest AI news”),
   delegate to mcp_sub_agent using google_search_tool.

3. If the total number of recorded messages in session.events (user + assistant) 
   is 10 or more, and session.state["sentiment_done"] is not True,
   then you MUST call sentiment_agent_tool with the full conversation transcript.
   After calling sentiment_agent_tool, update session.state["sentiment_done"] = True
   so sentiment analysis will only be run once per session.

4. Otherwise answer directly without making a tool or agent call.

When calling sentiment_agent_tool, use the named parameter:
- transcript: A single string containing the full conversation history
  (including both user and assistant messages, in chronological order).

Example invocation format:
CALL sentiment_agent_tool(transcript: "<full conversation text here>")

After tools return results, give a natural language response that incorporates
the tool’s output.

Do not generate raw JSON or code — only natural language text.
"""

manager_agent = Agent(
    name="manager_agent",
    description="Routes between stock, web search, and sentiment analysis.",
    model="gemma-3-27b-it",
    instruction=ROOT_MANAGER_INSTR,
    sub_agents=[mcp_sub_agent],
    tools=[sentiment_agent],
)

root_agent = manager_agent


# from google.adk.agents.llm_agent import Agent
# from .agents.mcpSubAgent import mcp_sub_agent
# from .agents.sentimentSubAgent import sentiment_agent

# ROOT_MANAGER_INSTR = """
# You are a manager agent that routes user queries to the appropriate tool or agent.

# You have access to two specialist sub‑agents:
# - mcp_sub_agent: calls remote MCP tools (get_stock_price_tool and google_search_tool)
# - sentiment_sub_agent: performs sentiment analysis on full conversation history

# The tools available on MCP are:
# - get_stock_price_tool(ticker: str) → returns stock price info
# - google_search_tool(query: str) → searches the internet and returns results

# Your job:
# 1. If the user’s query is about a **stock price or ticker query** (e.g., “Price of AAPL”), 
#    delegate to mcp_sub_agent and specify get_stock_price_tool.
# 2. If the user’s query is asking to **search something on the web** 
#    (e.g., “search for best ETFs”), delegate to mcp_sub_agent and specify google_search_tool.
# 3. If the conversation has reached 10 or more total messages in the current session,
#    and no sentiment summary has been generated yet, delegate to sentiment_sub_agent
#    with the full conversation history.
# 4. For any other user queries that do not require a tool or sentiment agent, respond directly.

# Important:
# - After calling a tool or sub‑agent, ensure the result is turned into a clear natural language reply.
# - Never transfer back and forth between sub‑agents infinitely.
# - Only transfer when necessary for tools or sentiment analysis.
# """

# manager_agent = Agent(
#     name="manager_agent",
#     description="Routes between stock, search, and sentiment analysis.",
#     model="gemma-3-27b-it",
#     instruction=ROOT_MANAGER_INSTR,
#     sub_agents=[mcp_sub_agent, sentiment_agent],
# )

# root_agent = manager_agent

