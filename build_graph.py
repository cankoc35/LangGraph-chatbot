from langgraph.graph import StateGraph
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from chatbot import chatbot
from summarizer import summarizer

class State(TypedDict):
    messages: Annotated[list, add_messages]
    user_id: str

# def build_graph():
#     graph_builder = StateGraph(State)
#     graph_builder.add_node("summarizer", summarizer)
#     graph_builder.add_node("chatbot", chatbot)

#     # Logic: always start with summarizer → chatbot
#     graph_builder.set_entry_point("summarizer")
#     graph_builder.add_edge("summarizer", "chatbot")
#     graph_builder.set_finish_point("chatbot")

#     return graph_builder

def build_graph():
    graph_builder = StateGraph(State)
    
    # Only using chatbot for now
    graph_builder.add_node("chatbot", chatbot)
    
    # Start and finish with chatbot
    graph_builder.set_entry_point("chatbot")
    graph_builder.set_finish_point("chatbot")

    return graph_builder