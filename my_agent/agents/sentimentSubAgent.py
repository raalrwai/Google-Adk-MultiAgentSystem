from google.adk.agents.llm_agent import Agent

SENTIMENT_INSTR = """
You are a sentiment analysis agent.

You are given a conversation transcript.
Your task is to produce a sentiment summary that includes:

1. An overall sentiment label (Positive, Neutral, Negative)
2. A brief explanation of why
3. A simple score from -1.0 (very negative) to +1.0 (very positive)

Return ONLY the sentiment summary.
"""

sentiment_agent = Agent(
    name="sentiment_agent",
    description="Analyzes sentiment of a conversation.",
    model="gemma-3-27b-it",
    instruction=SENTIMENT_INSTR,
)
