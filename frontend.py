import streamlit as st
import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from my_agent.agent import root_agent  

st.set_page_config(page_title="📈 ADK Chat", layout="wide")

st.markdown("""
<style>
/* SIDEBAR (dark olive) */
section[data-testid="stSidebar"] > div:first-child {
    background-color: #3B4A2B !important;
    color: white !important;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] a {
    color: white !important;
}

/* MAIN AREA BACKGROUND (light olive) */
.main .block-container {
    background-color: #EDF5E1 !important;
    color: #2C3E2E !important;
}

/* INPUT TEXT BOX */
div[data-testid="stTextInput"] input {
    background-color: #F7FAF2 !important;
    border: 1px solid #6F7F49 !important;
}
div[data-testid="stTextInput"] label {
    color: #2C3E2E !important;
}

/* CHAT MESSAGE BACKGROUND */
.stChatMessage > div {
    background-color: #FAFBF5 !important;
    color: #2C3E2E !important;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("📊 ADK Advanced Chatbot")
    st.markdown("""
    Chat with stock prices, web search, and sentiment analysis  
    all powered by ADK + FastMCP.
    """)
    st.markdown("---")
    st.markdown("**Instructions:**")
    st.markdown("""
    - Ask about stocks: AAPL, GOOG, TSLA  
    - Ask general questions  
    - Sentiment analysis runs automatically (manager determines when)
    """)
    st.markdown("---")
    st.markdown("**About:** Built with ADK, Gemma, FastMCP backend.")

# --- INIT CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

async def query_adk(message: str):
    session_service = InMemorySessionService()

    await session_service.create_session(
        app_name="agents",
        user_id="user1",
        session_id="sess1"
    )

    runner = Runner(
        agent=root_agent,
        app_name="agents",
        session_service=session_service,
    )

    out_text = ""
    new_msg = Content(role="user", parts=[Part(text=message)])

    async for event in runner.run_async(
        user_id="user1",
        session_id="sess1",
        new_message=new_msg,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            out_text = event.content.parts[0].text

    return out_text

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Type your message here…"):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            bot_reply = asyncio.run(query_adk(prompt))
            st.markdown(bot_reply)

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})


