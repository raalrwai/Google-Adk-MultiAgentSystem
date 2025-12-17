import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from my_agent.agent import root_agent  # adjust import to your project

async def main():
    # Setup session and runner
    session_service = InMemorySessionService()
    await session_service.create_session(app_name="app", user_id="user1", session_id="s1")
    
    runner = Runner(
        agent=root_agent,
        app_name="app",
        session_service=session_service
    )

    # User message
    user_msg = "Hello, how’s it going?"
    content = Content(role="user", parts=[Part(text=user_msg)])
    print("Sending:", user_msg)

    final_text = None
    
    async for event in runner.run_async(
        user_id="user1",
        session_id="s1",
        new_message=content,
    ):
        # Print all events for debug if you want
        print("EVENT:", event)

        # Check if this event includes a final assistant message
        if event.is_final_response():
            if event.content and event.content.parts:
                final_text = event.content.parts[0].text

    print("\nFinal assistant reply:", final_text)

if __name__ == "__main__":
    asyncio.run(main())
