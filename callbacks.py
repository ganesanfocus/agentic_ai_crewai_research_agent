# callbacks.py
import sys

def print_agent_chat(sender, receiver, message):
    """
    Custom callback to print live message passing between agents in the terminal.
    Handles both AutoGen dictionary messages and plain text strings.
    """
    print(f"\n[{'AGENT CHAT'}]")
    print(f"💬 {sender}  ──▶  {receiver}")
    
    # Check if the message is an AutoGen dictionary or a plain string
    if isinstance(message, dict):
        content = message.get("content", "")
    else:
        content = str(message)
    
    # Truncate long messages for cleaner terminal viewing
    if len(content) > 300:
         print(f'"{content[:300]}...\n[Content truncated for readability]"')
    else:
         print(f'"{content}"')
    
    print("-" * 50)
    sys.stdout.flush()