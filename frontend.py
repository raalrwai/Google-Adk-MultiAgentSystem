import streamlit as st
import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from my_agent.agent import root_agent  # adjust path

st.set_page_config(
    page_title="📈 ADK Chat",
    layout="wide",
)

st.header("Lets Talk Stocks")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to call ADK agent
async def query_adk(message):
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name="agents", user_id="user1", session_id="sess1"
    )

    runner = Runner(
        agent=root_agent,
        app_name="agents",
        session_service=session_service,
    )

    final_text = ""
    content = Content(role="user", parts=[Part(text=message)])
    async for event in runner.run_async(
        user_id="user1",
        session_id="sess1",
        new_message=content,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            final_text = event.content.parts[0].text

    return final_text

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Get new user input
if prompt := st.chat_input("Type your message here…"):
    # Show the user message immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call the agent
    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            bot_reply = asyncio.run(query_adk(prompt))
            st.markdown(bot_reply)

    # Save bot response
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
