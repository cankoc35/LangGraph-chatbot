from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage
from langgraph.checkpoint.postgres import PostgresSaver

from config import DB_URI
saver_ctx = PostgresSaver.from_conn_string(DB_URI)
saver = saver_ctx.__enter__()

import logging
logging.basicConfig(level=logging.INFO)

from llm import get_llm
llm = get_llm()

class State(TypedDict):
    messages: Annotated[list, add_messages]
    user_id: str
    
def chatbot(state: State):
    response_text = llm.invoke(state["messages"])
    return {"messages": [AIMessage(content=response_text)]}

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.set_entry_point("chatbot")
graph_builder.set_finish_point("chatbot")
graph = graph_builder.compile(saver)

def stream_graph_updates(user_input: str, session_id: str = "default-1", user_id: str = "user-1"):
    try:
        for event in graph.stream(
            {"messages": [{"role": "user", "content": user_input}], "user_id": user_id},
            config={"configurable": {"thread_id": session_id}}
        ):
            for value in event.values():
                print("Assistant:", value["messages"][-1].content)
    except Exception as e:
        logging.error(f"Error while running the graph: {e}")
        print("⚠️ There was an error processing your request.")

def chat_loop():
    logging.info("Chatbot started. Type 'quit' to exit.")
    while True:
        try:
            user_input = input("User: ").strip()
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

        if not user_input:
            print("❗ Please enter something.")
            continue

        if user_input.lower() in ["quit", "exit", "q"]:
            print("👋 Goodbye!")
            break

        stream_graph_updates(user_input)

if __name__ == "__main__":
    from main import graph 
    chat_loop()
