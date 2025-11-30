from google.adk.agents.llm_agent import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.agents.loop_agent import LoopAgent
from google.adk.agents.sequential_agent import SequentialAgent
from agent_director import director
from agent_writer import writer


writing_loop = LoopAgent(
    name="ScriptWritingLoop",
    sub_agents=[director, writer],
    max_iterations=10
)

# The root agent is a SequentialAgent that defines the overall workflow: Initial Write -> Refinement Loop.
writing_pipeline  = SequentialAgent(
    name="WritingPipeline",
    sub_agents=[director, writer],
)


producer = Agent(
    model='gemini-2.5-flash',
    name='Producer',
    description='Producer.',
    instruction='''
    You are the main producer/production head in a short film studio. The studio produces 2 minute short films and you are responsible for managing the team.
    The user gives you a prompt for a new short film with the subject.
    

    Stages of Production:
    1. Pre-Production: Start the writing_pipeline with the Brief including the film subject/theme, which will assing the job to the director and director will wotk with the writer to complete the Final Draft of the script.
    
    ''',
    sub_agents=[writing_pipeline]
    
)
