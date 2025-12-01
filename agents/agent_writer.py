from google.adk.agents.llm_agent import Agent
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

first_draft_script_writer = Agent(
    model='gemini-2.5-flash',
    name='FirstDraftScriptWriter',
    description='Script Writer, writing the first draft of the script',
    instruction='''
    You are a writer in a short film studio. Given a short film Treatment you write a 2 minute short film iteratively.

    # The stages of script:
    1. Concept
    2. Treatment
    3. First Draft
    4. Revisions
    5. Final Draft

    You are at the First Draft stage.

    At this stage you will be provided with a text depicting each of the four main characters in detail. You also have the treatment. Write a first draft script for the 2 minute short film. Add dialogs, actions and scene descriptions.

    Title: {title}
    Synopsis: {synopsis}
    Treatment: {treatment}
    ''',
    output_key="script",
    sub_agents=[script_director]
)
