import streamlit as st
import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from my_agent.agent import root_agent  # adjust this import path

# --- Page Config ---
st.set_page_config(page_title="Enterprise ADK Chat", layout="wide")

# --- Top Panel — ALWAYS visible ---
top_panel = st.container()
with top_panel:
    st.markdown("<h1 style='text-align: center;'>📈 Enterprise Stock Price Chatbot</h1>", unsafe_allow_html=True)

# --- Set up message history ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Function to call ADK ---
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

# --- Scrollable Chat Body ---
chat_body = st.container()
with chat_body:
    # Apply a fixed height with overflow so only this area scrolls
    st.markdown(
        """
        <div style="
            max-height: 65vh;
            overflow-y: auto;
            padding: 8px;
            border: 1px solid #eee;
            border-radius: 8px;
            background: #fff;
        ">
        """,
        unsafe_allow_html=True,
    )

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div style='text-align: right; background:#4e8cff; color:white; padding:10px; border-radius:10px; margin:5px 0px; max-width:80%; margin-left:auto;'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align: left; background:#f1f0f0; color:#000; padding:10px; border-radius:10px; margin:5px 0px; max-width:80%; margin-right:auto;'>{msg['content']}</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# --- Input Box (standard chat input) ---
if prompt := st.text_input("Type your message here…", key="user_input", placeholder="Ask about stock prices…"):
    # record user
    st.session_state.messages.append({"role": "user", "content": prompt})

    # show user message right away
    # run agent
    with st.spinner("Thinking…"):
        bot_reply = asyncio.run(query_adk(prompt))
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    # clear input (so new messages can be typed)
    st.session_state.user_input = ""



# import asyncio

# from google.adk.runners import Runner
# from google.adk.sessions import InMemorySessionService
# from google.genai.types import Content, Part

# from my_agent.agent import root_agent  # adjust import to your project

# async def main():
#     # Setup session and runner
#     session_service = InMemorySessionService()
#     await session_service.create_session(app_name="app", user_id="user1", session_id="s1")
    
#     runner = Runner(
#         agent=root_agent,
#         app_name="app",
#         session_service=session_service
#     )

#     # User message
#     user_msg = "Hello, how’s it going?"
#     content = Content(role="user", parts=[Part(text=user_msg)])
#     print("Sending:", user_msg)

#     final_text = None
    
#     async for event in runner.run_async(
#         user_id="user1",
#         session_id="s1",
#         new_message=content,
#     ):
#         # Print all events for debug if you want
#         print("EVENT:", event)

#         # Check if this event includes a final assistant message
#         if event.is_final_response():
#             if event.content and event.content.parts:
#                 final_text = event.content.parts[0].text

#     print("\nFinal assistant reply:", final_text)

# if __name__ == "__main__":
#     asyncio.run(main())
