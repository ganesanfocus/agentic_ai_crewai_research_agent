# doc_creator.py
from crewai import Agent
from autogen import ConversableAgent
from agents.config import llm_config
from tools.doc_generator import generate_document

crew_doc_creator = Agent(
    role='Document Formatting Specialist',
    goal='Take summarized text and output a highly professional document in the user\'s requested format.',
    backstory='You are an expert at formatting reports. You carefully read instructions to determine if a PDF or DOCX is required.',
    allow_delegation=False,
    verbose=True
)

autogen_doc_creator = ConversableAgent(
    name="Doc_Creator",
    system_message=f"{crew_doc_creator.backstory} Your Role: {crew_doc_creator.role}. Your Goal: {crew_doc_creator.goal}\n"
                   "You receive a summary. You must use the generate_document tool to save it. Decide the format (pdf/docx) based on the initial user request.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

# Register the document generation tool
autogen_doc_creator.register_for_llm(name="generate_document", description="Generates PDF or DOCX files")(generate_document)