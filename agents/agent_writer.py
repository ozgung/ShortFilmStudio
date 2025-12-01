from typing import Any, Dict
from google.adk.agents.llm_agent import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.tool_context import ToolContext
from .agent_director import script_director

concept_ideation_writer = Agent(
    model='gemini-2.5-flash',
    name='ConceptWriter',
    description='Takes the film brief and comes up with Concept ideas.',
    instruction='''
    You are a writer in a short film studio making a 2 minute short film.
    Given the brief/subject/idea/theme of the film as the initial prompt come up with a list of  5 different ONE SENTENCE PITCH around the given subject/theme.
    Return just the list of the items.
    ''',
    output_key="concepts_list"
)

synopsis_writer = Agent(
    model='gemini-2.5-flash',
    name='SynopsisWriter',
    description='Takes the brief and the Concept idea to write a Synopsis.',
    instruction='''
    You are a writer in a short film studio making a 2 minute short film. There must be 4 characters in the film.
    Your task is to write the short synopsis given the brief. Keep it short to a single paragraph. You can get greative when adding details.

    Title: {title}
    Brief: {brief}
    ''',
    output_key="synopsis"
)


treatment_writer = Agent(
    model='gemini-2.5-flash',
    name='TreatmentWriter',
    description='Takes the brief and the Concept idea to write a Treatment.',
    instruction='''
    You are a writer in a short film studio making a 2 minute short film.

    Your task is to write a treatment, given the accepted brief and sysnopsis. 
    
    Title: {title}
    Synopsis: {synopsis}
    
    Generate a Treatment text for the 2 minute film. 
    This tratment should have the main story arc. The film must have 4 main characters. EXPLICITLY name these characters to different names if not already named. Write a separate section for Character Profiles depicting all 4 main characters in detail.
    ''',
    output_key="treatment"
)


# Saves the Script to state
def update_script(tool_context: ToolContext, script: str
) -> Dict[str, Any]:
    """
    Save or update the script to the session state.

    Args:
        script: script str in standard markdown format
    """
    tool_context.state["script"] = script
    return {"status": "success"}

# Read script from session state.
def retrieve_script(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Tool to retrieve the most recent saved draft of the script from session state.
    """
    # Read from session state
    script = tool_context.state.get("script", "Script not found")

    return {"status": "success", "script": script}

script_writer = Agent(
    model='gemini-2.5-flash',
    name='ScriptWriter',
    description='Script Writer, writing the first draft of the script and revisions.',
    instruction='''
    You are a writer in a short film studio. Given a short film Treatment you write a 2 minute short film iteratively.

    # The stages of script:
    1. Concept
    2. Treatment
    3. First Draft
    4. Revisions
    5. Final Draft

    You start at the First Draft stage.

    At this stage you will be provided with a text depicting each of the four main characters in detail. You also have the treatment. Write a first draft script for the 2 minute short film. Add dialogs, actions and scene descriptions.

    Use `update_script` tool save/update your script first draft and revisions.
    After saving the first draft call `script_director` tool for revision on the latest draft. Just do a single revision iteration. Return the Final draft of the script.

    Use `retrieve_script` tool to load the latest saved draft of the script it needed.

    ---

    Title: {title}
    Synopsis: {synopsis}
    Treatment: {treatment}
    
    
    ''',
    output_key="script",
    tools=[AgentTool(script_director), update_script, retrieve_script]
)

# revision_script_writer = Agent(
#     model='gemini-2.5-flash',
#     name='RevisionScriptWriter',
#     description='Script Writer, writing the revision for the script with given comments and revision requests.',
#     instruction='''
#     You are a writer in a short film studio. Given a short film Treatment you write a 2 minute short film iteratively.

#     At this stage you will be provided with a text depicting each of the four main characters in detail. You also have the treatment. Write a first draft script for the 2 minute short film. Add dialogs, actions and scene descriptions.

#     Title: {title}
#     Script: {script}
#     ''',
#     output_key='script'
# )