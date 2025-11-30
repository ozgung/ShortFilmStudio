import asyncio
from google.adk.runners import InMemoryRunner
from dotenv import load_dotenv
import agents

load_dotenv()

FILM_SUBJECT = "a sci-fi in a spaceship"
USER_PROMPT = f"Create preproduction assets for a short film about {FILM_SUBJECT}."

async def main():
    root_agent = agents.agent_producer.producer
    
    runner = InMemoryRunner(agent=root_agent)

    response = await runner.run_debug(
        USER_PROMPT
    )
    
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
