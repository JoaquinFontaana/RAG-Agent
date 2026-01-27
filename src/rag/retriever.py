from functools import lru_cache
from src.rag import get_vector_store
from langchain_core.documents import Document
@lru_cache()
def get_retriever():
    return get_vector_store().as_retriever()

def retrieve_documents(query:str) -> list[Document]:
    try:  
        if not query:
            raise ValueError("The query for the retriever cant be empty")  
        return get_retriever().invoke(query)
    except Exception as ex:
        raise Exception(f"The retrieve invoke failed. {str(ex)}")