from langgraph.types import RetryPolicy
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.postgres import PostgresSaver
from functools import lru_cache
from src.utils import (
    AgentState,
    handle_classification_error,
    handle_technical_error,
    generate_response,
    retrieve,
    classification_query,
    routing_after_classification,
    routing_after_retrieve,
    human_handoff,
    routing_after_human_handoff,
    OutputState,
    InputState
)
from .db import get_connection_pool
@lru_cache()
def get_workflow():
    workflow = StateGraph(AgentState,output_schema=OutputState,input_schema=InputState)

    # ========== NODOS ==========
    workflow.add_node(classification_query)
    workflow.add_node(retrieve, retry_policy=RetryPolicy())
    workflow.add_node(generate_response)
    workflow.add_node( handle_classification_error)
    workflow.add_node(handle_technical_error)
    workflow.add_node(human_handoff)
    # ========== EDGES ==========
    workflow.add_edge(START, "classification_query")
    
    workflow.add_conditional_edges(
        "classification_query",
        routing_after_classification,
        {
            "retrieve": "retrieve",
            "generate_response": "generate_response",
            "handle_technical_error": "handle_technical_error",
            "handle_classification_error": "handle_classification_error",
            "human_handoff": "human_handoff"
        }
    )
    
    workflow.add_conditional_edges(
        "retrieve",
        routing_after_retrieve,
        {
            "generate_response": "generate_response",
            "handle_technical_error": "handle_technical_error"
        }
    )
    
    workflow.add_conditional_edges(
        "human_handoff",
        routing_after_human_handoff,
        {
            "human_handoff": "human_handoff",
            "END": END
        }
    )
    workflow.add_edge("generate_response", END)
    workflow.add_edge("handle_technical_error", END)
    workflow.add_edge("handle_classification_error", END)
    
    pool = get_connection_pool()

    checkpointer = PostgresSaver(pool)
    checkpointer.setup()
    return workflow.compile(checkpointer=checkpointer)
