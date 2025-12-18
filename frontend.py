import streamlit as st
import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from my_agent.agent import root_agent  # adjust path if needed

# --- PAGE SETUP ---
st.set_page_config(page_title="📈 ADK Chat", layout="wide")

# --- GLOBAL CSS STYLING ---
st.markdown(
    """
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

    /* CHAT MESSAGES BACKGROUND */
    .stChatMessage > div {
        background-color: #FAFBF5 !important;
        color: #2C3E2E !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# --- SIDEBAR CONTENT ---
with st.sidebar:
    st.title("📊 ADK Advanced Chatbot")
    st.markdown("""
    Ask about the news or get stock info  
    using ADK + FastMCP.
    """)
    st.markdown("---")
    st.markdown("**Instructions:**")
    st.markdown("""
    - Ask about AAPL, GOOGL, TSLA, etc.  
    - Ask general questions too  
    - Results will show in chat below
    """)
    st.markdown("---")
    st.markdown("**About:**")
    st.markdown("Built with ADK, Gemma, and FastMCP backend.")

# --- CHAT HISTORY STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- FUNCTION TO CALL THE ADK AGENT ---
async def query_adk(message: str):
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

# --- RENDER PREVIOUS MESSAGES ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- CHAT INPUT BOX ---
if prompt := st.chat_input("Type your message here…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            bot_resp = asyncio.run(query_adk(prompt))
            st.markdown(bot_resp)

    st.session_state.messages.append({"role": "assistant", "content": bot_resp})

