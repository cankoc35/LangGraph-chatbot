import uuid
from utils.saver import get_saver
from build_graph import build_graph

def chat_loop(graph):
    session_id = str(uuid.uuid4())  # 🧠 New session per run
    user_id = "user-1"

    while True:
        try:
            user_input = input("\nUser: ").strip()
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

        try:
            for _ in graph.stream(
                {"messages": [{"role": "user", "content": user_input}], "user_id": user_id},
                config={"configurable": {"thread_id": session_id}}
            ):
                pass 
        except Exception as e:
            print(f"⚠️ There was an error processing your request: {e}")


if __name__ == "__main__":
    with get_saver() as saver:
        graph = build_graph().compile(saver)
        chat_loop(graph)


