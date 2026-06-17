# main.py
import os
from dotenv import load_dotenv
from graph import app

# Load environment variables first
load_dotenv()

def parse_user_intent(query: str) -> dict:
    """Simple parser to determine if a doc is needed and what format."""
    query_lower = query.lower()
    requires_doc = "doc" in query_lower or "pdf" in query_lower or "report" in query_lower
    
    doc_format = "pdf"
    if "docx" in query_lower or "word" in query_lower:
        doc_format = "docx"
        
    return {
        "query": query,
        "requires_doc": requires_doc,
        "doc_format": doc_format,
        "research_data": "",
        "summary_data": "",
        "final_output": ""
    }

def main():
    print("="*50)
    print("🤖 Agentic Framework: LangGraph + CrewAI + AutoGen")
    print("="*50)
    
    user_input = input("\nEnter your prompt (e.g., 'Research LangGraph and create a PDF'):\n> ")
    
    initial_state = parse_user_intent(user_input)
    
    print("\n[LangGraph] Kicking off State Machine...\n")
    
    # Run the graph
    app.invoke(initial_state)
    
    print("\n[LangGraph] Workflow Complete.")

if __name__ == "__main__":
    main()