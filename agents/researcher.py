# researcher.py
from crewai import Agent
from autogen import ConversableAgent
from agents.config import llm_config
from tools.search_tool import web_search

# 1. CrewAI defines the identity
crew_researcher = Agent(
    role='Senior Research Analyst',
    goal='Uncover comprehensive, accurate, and up-to-date information on the given topic.',
    backstory='You are a meticulous researcher with a knack for finding the most relevant data. You organize raw data efficiently.',
    allow_delegation=False,
    verbose=True
)

# 2. AutoGen powers the communication
autogen_researcher = ConversableAgent(
    name="Researcher",
    system_message=f"{crew_researcher.backstory} Your Role: {crew_researcher.role}. Your Goal: {crew_researcher.goal}\n"
                   "You must use the web_search tool to gather information. Once you have enough data, pass the raw findings to the Summarizer.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

# Register the search tool with AutoGen
autogen_researcher.register_for_llm(name="web_search", description="Search web for info")(web_search)