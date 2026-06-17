# graph.py
import operator
from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, END
from autogen import UserProxyAgent

from agents.researcher import autogen_researcher
from agents.summarizer import autogen_summarizer
from agents.doc_creator import autogen_doc_creator
from callbacks import print_agent_chat
from tools.search_tool import web_search
from tools.doc_generator import generate_document

# Register tools for execution by the UserProxyAgent (standard AutoGen pattern)
user_proxy = UserProxyAgent(
    name="Executor",
    human_input_mode="NEVER",
    code_execution_config={"use_docker": False}
)
user_proxy.register_for_execution(name="web_search")(web_search)
user_proxy.register_for_execution(name="generate_document")(generate_document)

# Define State
class AgentState(TypedDict):
    query: str
    requires_doc: bool
    doc_format: str
    research_data: str
    summary_data: str
    final_output: str

# Node Functions
def research_node(state: AgentState):
    print_agent_chat("System", "Researcher", f"Starting research on: {state['query']}")
    
    # AutoGen chat: Proxy asks Researcher to research
    chat_res = user_proxy.initiate_chat(
        autogen_researcher,
        message=f"Research this topic and provide the raw data: {state['query']}",
        max_turns=2,
        summary_method="last_msg"
    )
    
    result = chat_res.summary
    print_agent_chat("Researcher", "Summarizer", result)
    return {"research_data": result}

def summarize_node(state: AgentState):
    # AutoGen chat: Proxy asks Summarizer to summarize
    chat_res = user_proxy.initiate_chat(
        autogen_summarizer,
        message=f"Summarize this raw data:\n\n{state['research_data']}",
        max_turns=1,
        summary_method="last_msg"
    )
    
    result = chat_res.summary
    print_agent_chat("Summarizer", "Doc_Creator", result)
    return {"summary_data": result}

def document_node(state: AgentState):
    format_req = state.get("doc_format", "pdf")
    message = f"Please save the following summary as a {format_req} document using your tool:\n\n{state['summary_data']}"
    
    chat_res = user_proxy.initiate_chat(
        autogen_doc_creator,
        message=message,
        max_turns=2, # Allow 2 turns so agent can call tool and proxy can execute
        summary_method="last_msg"
    )
    
    result = chat_res.summary
    print_agent_chat("Doc_Creator", "USER", result)
    return {"final_output": result}

# Conditional Logic
def route_document(state: AgentState):
    if state.get("requires_doc"):
        return "document_node"
    return END

# Build LangGraph
workflow = StateGraph(AgentState)

workflow.add_node("research_node", research_node)
workflow.add_node("summarize_node", summarize_node)
workflow.add_node("document_node", document_node)

workflow.set_entry_point("research_node")
workflow.add_edge("research_node", "summarize_node")
workflow.add_conditional_edges(
    "summarize_node",
    route_document,
    {
        "document_node": "document_node",
        END: END
    }
)
workflow.add_edge("document_node", END)

app = workflow.compile()