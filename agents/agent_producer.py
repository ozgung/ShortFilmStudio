from typing import Dict, Any
from google.adk.agents.llm_agent import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.tool_context import ToolContext
from google.adk.agents.loop_agent import LoopAgent
from google.adk.agents.sequential_agent import SequentialAgent

from .agent_director import director, cinematographer
from .agent_writer import (
    concept_ideation_writer,
    script_writer,
    synopsis_writer,
    treatment_writer,
)

writing_pipeline  = SequentialAgent(
    name="WritingPipeline",
    sub_agents=[synopsis_writer, treatment_writer, script_writer],
)

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
        Use the `writing_pipeline` to generate the script.
    3. Storyboard:
        Use `cinematographer` tool to call the cinematographer agent to generate shooting script for the movie and storyboard. It will return a shooting_script, as a table of shots.

    Show the generated shooting script to the user.
    ''',
    #sub_agents=[writing_pipeline],
    tools=[AgentTool(concept_ideation_writer), save_brief, AgentTool(writing_pipeline), AgentTool(cinematographer)]
)
