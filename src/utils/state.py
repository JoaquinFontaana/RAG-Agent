from langgraph.graph import MessagesState
from src.utils import ClassificationOutput
from langchain_core.documents import Document

class AgentState(MessagesState):
    user_query:str
    classification_query: ClassificationOutput
    retrieved_docs: list[Document]
    error:str
    response:str