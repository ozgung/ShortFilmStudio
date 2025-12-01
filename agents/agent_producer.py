from typing import Dict, Any
from google.adk.agents.llm_agent import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.tool_context import ToolContext
from google.adk.agents.loop_agent import LoopAgent
from google.adk.agents.sequential_agent import SequentialAgent

from .agent_director import director
from .agent_writer import (
    concept_ideation_writer,
    first_draft_script_writer,
    synopsis_writer,
    treatment_writer,
)



writing_pipeline  = SequentialAgent(
    name="WritingPipeline",
    sub_agents=[synopsis_writer, treatment_writer, first_draft_script_writer],
)


# This demonstrates how tools can write to session state using tool_context.
# The 'user:' prefix indicates this is user-specific data.
def save_userinfo(
    tool_context: ToolContext, user_name: str, country: str
) -> Dict[str, Any]:
    """
    Tool to record and save user name and country in session state.

    Args:
        user_name: The username to store in session state
        country: The name of the user's country
    """
    # Write to session state using the 'user:' prefix for user data
    tool_context.state["user:name"] = user_name
    tool_context.state["user:country"] = country

    return {"status": "success"}


# This demonstrates how tools can read from session state.
def retrieve_userinfo(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Tool to retrieve user name and country from session state.
    """
    # Read from session state
    user_name = tool_context.state.get("user:name", "Username not found")
    country = tool_context.state.get("user:country", "Country not found")

    return {"status": "success", "user_name": user_name, "country": country}

# Saves the BRIEF to state
def save_brief(tool_context: ToolContext, title: str, brief: str
) -> Dict[str, Any]:
    """
    Tool to save project title and brief in session state.

    Args:
        title Title of the Short Film
        brief: 2 or 3-sentence brief for the creative team stating the main idea/concept of the film.
    """
    # Write to session state using the 'user:' prefix for user data
    tool_context.state["title"] = title
    tool_context.state["brief"] = brief

    return {"status": "success"}
    
    
producer = Agent(
    model='gemini-2.5-flash',
    name='Producer',
    description='Producer.',
    instruction='''
    You are the main producer/production head in a short film studio. The studio produces 2 minute short films and you are responsible for managing the team.
    
    The user gives you a prompt for a new short film with the subject.
    
    Stages of Production:
    1. Ideation:
        1.1 Use `concept_ideation_writer` tool to generate 5 film ideas/concepts on the subject, having 4 main characters.
        1.2 CHOOSE one concept from this list and convert that to a Brief for the writing team. Find a title for the film. Save title and brief to session by calling `save_brief` tool.
    2. Pre-Production: 
        Start the `writing_pipeline` to generate the script.
    ''',
    sub_agents=[writing_pipeline],
    tools=[AgentTool(concept_ideation_writer), save_brief, AgentTool(writing_pipeline)]
)
