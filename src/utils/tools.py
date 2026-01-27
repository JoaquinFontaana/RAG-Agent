from langchain.tools import tool
from langchain_core.documents import Document
from src.rag import retrieve_documents

def handle_tool_error(exception:Exception):
    if isinstance(exception, ValueError):
     return f"Entrada inválida: {str(exception)}. Intenta reformular tu consulta."

    elif isinstance(exception, ConnectionError):
        return "Error de conexión temporal. Por favor reintenta."

    else:
        return f"Error inesperado: {str(exception)}. Intenta con otros parámetros."

@tool
def search_knowledge_base(query:str) -> list[Document]:
    """
    Search relevant information about the company polices
    
    :param query: related query about polices
    :type query: str
    :return: Most relevant documents for the query
    :rtype: list[Document]
    """
    return retrieve_documents(query)