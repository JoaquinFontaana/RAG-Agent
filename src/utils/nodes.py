from src.utils import get_llm, AgentState, ClassificationOutput,CLASSIFICATOR_PROMPT, ANSWER_PROMPT
from typing import cast
from src.rag import retrieve_documents
from logging import getLogger
from langgraph.types import interrupt
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
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

        # No agregar HumanMessage aquí - ya viene del invoke inicial
        return {"classification_query": result}
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
    return {
        "response": message,
        "messages": [
            AIMessage(content=message)
        ] 
    }

def handle_technical_error(state: AgentState):
    """Handles technical errors (retrieval failures, etc)."""
    error_msg = state.get("error", "An unexpected error occurred")

    user_message = (
        "I'm experiencing technical difficulties accessing the knowledge base. "
        "Please try again in a moment, or rephrase your question."
    )
    
    logger.error(f"Technical error: {error_msg}")
    
    return {
        "response": user_message,
        "messages": [AIMessage(user_message)]
        }

def generate_response(state: AgentState):
    """Genera respuesta usando historial completo de conversación."""
    try:
        llm = get_llm()
        docs = state.get("retrieved_docs", [])

        # Construir mensajes para el LLM
        messages = []
        
        # 1. System message con contexto RAG si existe
        system_content = "You are a helpful customer support assistant."
        if docs:
            context = "\n\n".join([doc.page_content for doc in docs])
            system_content += f"\n\nUse this context to answer:\n{context}"
            logger.info(f"Generating response with {len(docs)} retrieved documents")
        else:
            logger.info("Generating response without retrieved documents")
        
        messages.append(SystemMessage(content=system_content))
        
        # 2. Agregar HISTORIAL COMPLETO de conversación
        messages.extend(state["messages"])
        
        # 3. Invocar LLM con todo el contexto
        response = llm.invoke(messages).content
        
        logger.info("Response generated successfully")
        
        return {
            "response": response,
            "messages": [AIMessage(content=response)]  # Se agrega al historial
        }
    
    except Exception as ex:
        logger.error(f"Generate response node: An exceptions has ocurred {str(ex)}")
        return {"error": str(ex)}
    
def human_handoff(state:AgentState):
    classification = state["classification_query"]
    logger.info(f"Handing off to human: {state['user_query']}")
    if not state.get("human_active"):

        human_response = interrupt({
            "type":"initial_handoff",
            "reason":classification.reason,
            "instruction": "Respond to user query",
            "query": state["user_query"]
        })

        return {
            "response": human_response,
            "messages": [
                SystemMessage(content="Transferred to human agent"),
                AIMessage(content=human_response)
            ],
            "human_active": True,
            "conversation_status": "active"
        }
    # Loop activo - esperar acción del humano
    human_action = interrupt({
        "type": "human_conversation_control",
        "instruction": "Respond to user or mark as resolved",
        "options": ["respond", "resolve"]
    })
    
    # Procesar acción
    if human_action["action"] == "resolve":
        return {
            "response": human_action.get("message"),
            "human_active": False,
            "messages": [
                AIMessage(human_action.get("message")),
                SystemMessage("Human intervention finalized")
                ]
        }
    
    else:  # respond
        response_message = human_action.get("message", "")
        return {
            "response": response_message,
            "human_active": True,
            "messages": [AIMessage(content=response_message)]
        }