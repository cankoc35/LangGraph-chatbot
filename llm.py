from langchain_ollama import OllamaLLM
from config import OLLAMA_MODEL

def get_llm(model_name: str = OLLAMA_MODEL, streaming: bool = True):  
    """
    Returns an LLM instance configured to use an Ollama model.
    """
    return OllamaLLM(model=model_name, streaming=streaming)
