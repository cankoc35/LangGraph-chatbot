from langchain_core.messages import AIMessage
from utils.promts import basic_rag_prompt
from llm import get_llm

llm = get_llm()  

def chatbot(state, streaming: bool = True):
    user_input = state["messages"][-1].content 
    prompt = basic_rag_prompt()
    history_text = "\n".join([f"{m.type}: {m.content}" for m in state["messages"][:-1]])
    formatted_prompt = prompt.invoke({
        "history": history_text,
        "question": user_input
    })
    
    print(f"🧠🧠history_text🧠🧠: {history_text}")

    if streaming:
        streamed_text = ""
        for token in llm.stream(formatted_prompt):
            print(token, end="", flush=True)
            streamed_text += token 
        return {"messages": [AIMessage(content=streamed_text)]}
    else:
        non_stream_llm = get_llm(streaming=False)
        response = non_stream_llm.invoke(formatted_prompt)
        return {"messages": [AIMessage(content=response)]}


