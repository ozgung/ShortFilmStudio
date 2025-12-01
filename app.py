from typing import Any, Dict
import asyncio
from google.adk.runners import InMemoryRunner, Runner
from google.genai import types
from dotenv import load_dotenv
import agents
from run_session import run_session



from google.adk.agents import Agent, LlmAgent
from google.adk.apps.app import App, EventsCompactionConfig
from google.adk.models.google_llm import Gemini
from google.adk.sessions import DatabaseSessionService
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.tools.tool_context import ToolContext
from google.genai import types

load_dotenv()


FILM_SUBJECT = "a sci-fi in a spaceship"
USER_PROMPT = f"Create preproduction assets for a short film about {FILM_SUBJECT}."

APP_NAME = "agents"  # Application
USER_ID = "default"  # User
SESSION = "default"  # Session

async def main():
    root_agent = agents.agent_producer.producer
    
    session_service = InMemorySessionService()

    runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)

    await run_session(runner, [USER_PROMPT], session_name=SESSION)

if __name__ == "__main__":
    asyncio.run(main())
