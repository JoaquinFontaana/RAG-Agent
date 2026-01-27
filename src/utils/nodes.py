from src.utils import get_llm, AgentState, ClassificationOutput,CLASSIFICATOR_PROMPT, ANSWER_PROMPT
from typing import cast
from src.rag import retrieve_documents
from logging import getLogger

logger = getLogger(__name__)

def classification_query(state:AgentState):
    if not state.get("user_query"):
        logger.error("The user query was empty in the classificate node")
        return {"error": "Input query cannot be empty"}
    try:
        llm = get_llm()

        structured_llm = llm.with_structured_output(
            ClassificationOutput,
            method="function_calling"
            )
        
        chain = CLASSIFICATOR_PROMPT | structured_llm

        result = cast(ClassificationOutput,chain.invoke({"query": state['user_query']}))
        logger.info(f"Classification query result: {str(result)}")

        return {"classification_query":result}
    except Exception as e:
            logger.error(f"LLM Classification Error: {e}")
            return {"error": f"Error classifying query: {str(e)}"}


def retrieve(state:AgentState):
    try:
        docs = retrieve_documents(state["user_query"])
        return {"retrieved_docs":docs}
    except Exception as ex:
        msg = f"An error occurred in the retriever node. {str(ex)}"
        logger.error(f"Error in retrieve node: {msg}")
        return {"error":msg}

def handle_classification_error(state: AgentState):
    """Handles inappropriate queries."""

    classification = state["classification_query"]

    error_messages = {
        "inappropriate": "I cannot help you with that type of query. Please keep the conversation appropriate.",
        "out_of_scope": f"Query out of scope: {classification.reason}. Please ask about our services.",
    }

    message = error_messages.get(
        classification.category,
        f"Could not process your query: {classification.reason}"
    )
    return {"response": message}

def handle_technical_error(state: AgentState):
    """Handles technical errors (retrieval failures, etc)."""
    error_msg = state.get("error", "An unexpected error occurred")

    user_message = (
        "I'm experiencing technical difficulties accessing the knowledge base. "
        "Please try again in a moment, or rephrase your question."
    )
    
    logger.error(f"Technical error: {error_msg}")
    
    return {"response": user_message}

def generate_response(state:AgentState):
    try:
        llm = get_llm()
        docs = state.get("retrieved_docs")

        if docs:
            context = "\n\n".join([doc.page_content for doc in docs])
        else:
            context = ""
        chain = ANSWER_PROMPT | llm

        response = chain.invoke({
            "query":state["user_query"],
            "context":context
            }).content
        
        return {"response":response}
    
    except Exception as ex:
        logger.error(f"Generate response node: An exceptions has ocurred {str(ex)}")
        return {"error": ex}