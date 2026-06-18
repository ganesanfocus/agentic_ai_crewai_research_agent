from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal

class State(TypedDict):
    user_input: str
    response: str


# Node function
def router_node(state: State) -> State:
    print(state)
    return state


# Routing function
def router(state: State) -> Literal["greeting", "farewell", END]:
    text = state["user_input"].lower()

    if "hello" in text:
        return "greeting"
    elif "bye" in text:
        return "farewell"
    else:
        return END


def greeting_node(state: State) -> State:
    state["response"] = "Hello! How can I assist you today?"
    return state


def farewell_node(state: State) -> State:
    state["response"] = "Goodbye! Have a great day!"
    return state


graph = StateGraph(State)

graph.add_node("router", router_node)
graph.add_node("greeting", greeting_node)
graph.add_node("farewell", farewell_node)

graph.set_entry_point("router")

graph.add_conditional_edges(
    "router",
    router
)

graph.add_edge("greeting", END)
graph.add_edge("farewell", END)

app = graph.compile()

print(app.invoke({"user_input": "hello"})["response"])  # Should print greeting response
print(app.invoke({"user_input": "bye"})["response"])    # Should print farewell response