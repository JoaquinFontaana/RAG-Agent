from typing import TypedDict
from src.utils import ClassificationOutput
from langchain_core.documents import Document
class AgentState(TypedDict):
    user_query:str
    classification_query: ClassificationOutput
    retrieved_docs: list[Document]
    error:str
