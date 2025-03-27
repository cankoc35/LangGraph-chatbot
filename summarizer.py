from langchain_core.messages import SystemMessage
from langgraph.graph.message import add_messages
from llm import get_llm

llm = get_llm(streaming=False) 

def summarizer(state):
    messages = state["messages"]

    # Only summarize if more than 5 messages
    if len(messages) <= 5:
        return state

    # Select messages to summarize (all except last 5)
    old_messages = messages[:-5]
    recent_messages = messages[-5:]

    # Join old content to one string
    history_text = "\n".join([f"{m.type}: {m.content}" for m in old_messages])

    # Ask LLM to summarize
    summary_prompt = f"""
        You are summarizing a logistics chatbot conversation.

        Your summary **must** extract and clearly retain:
        - Plate numbers mentioned by the user (e.g., "35 BHJ 99")
        - Shipment numbers or tracking IDs (e.g., "44556")

        Only summarize messages that are relevant to logistics, tracking, or user-provided info.

        Conversation:

    {history_text}
    """
    
    summary = llm.invoke(summary_prompt)

    # Create a new SystemMessage with the summary
    summary_message = SystemMessage(content=f"Previous conversation summary:\n{summary}")
    print(f"🧠🧠Summary🧠🧠: {summary}")

    # Return updated state with summary + last messages
    return {
        "messages": [summary_message] + recent_messages,
        "user_id": state["user_id"]
    }
