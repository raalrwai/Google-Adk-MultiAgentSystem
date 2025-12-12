from google.adk.agents.llm_agent import Agent
from .agents.stock_agent import stock_agent
from .agents.mcpSubAgent import mcp_sub_agent


ROOT_MANAGER_INSTR = """
You are a helpful stock price coordinator.

When the user asks about any stock price or ticker information,
delegate the task to the stock_agent.

Only respond directly if the question is not about stocks.
"""

manager_agent = Agent(
    name="manager_agent",
    description="Delegates stock price queries to stock_agent.",
    model="gemma-3-27b-it",
    instruction=ROOT_MANAGER_INSTR,
    # sub_agents=[stock_agent],  
    sub_agents=[mcp_sub_agent],  

)

root_agent = manager_agent