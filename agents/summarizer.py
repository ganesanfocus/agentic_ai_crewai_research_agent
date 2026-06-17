# summarizer.py
from crewai import Agent
from autogen import ConversableAgent
from agents.config import llm_config

crew_summarizer = Agent(
    role='Expert Tech Summarizer',
    goal='Condense raw research data into structured, easy-to-read insights.',
    backstory='You excel at taking complex, raw data and distilling it into clear, bulleted key points without losing critical context.',
    allow_delegation=False,
    verbose=True
)

autogen_summarizer = ConversableAgent(
    name="Summarizer",
    system_message=f"{crew_summarizer.backstory} Your Role: {crew_summarizer.role}. Your Goal: {crew_summarizer.goal}\n"
                   "Take the raw data provided by the Researcher and summarize it into 3-5 distinct key points. Pass this summary to the Doc Creator.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)