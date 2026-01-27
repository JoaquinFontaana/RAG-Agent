from langchain_chroma import Chroma
from functools import lru_cache
from config import settings
from src.rag import get_embedding_function
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import logging

logger = logging.getLogger(__name__)

@lru_cache()
def get_vector_store() -> Chroma:
    return Chroma(
        collection_name="data",
        embedding_function=get_embedding_function(),
        persist_directory=settings.vector_store_path
        )

def add_documents(documents: list[Document]):
    try:
        # Validate input
        if not documents:
            logger.warning("No documents provided to add_documents")
            raise ValueError("No documents provided to add")
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=700,
            chunk_overlap=100
        )
        
        chunks = text_splitter.split_documents(documents)
        
        if not chunks:
            logger.warning("No chunks generated from documents")
            raise Exception("No chunks generated from documents")
        
        # Add chunks to vector store
        vector_store = get_vector_store()
        vector_store.add_documents(chunks)
        
        logger.info(f"Successfully added {len(chunks)} chunks from {len(documents)} documents")
        
    except Exception as e:
        logger.error(f"Error adding documents to vector store: {str(e)}", exc_info=True)

