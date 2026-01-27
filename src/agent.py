from langgraph.types import RetryPolicy
from langgraph.graph import START, END, StateGraph
from functools import lru_cache
from src.utils import AgentState,handle_classification_error,handle_technical_error,generate_response,retrieve,classification_query, routing_after_classification, routing_after_retrieve

@lru_cache()
def get_workflow():
    workflow = StateGraph(AgentState)

    workflow.add_node(classification_query)
    workflow.add_node(handle_classification_error)
    workflow.add_node(handle_technical_error)
    workflow.add_node(generate_response)
    workflow.add_node("retrieve",
                      retrieve,
                      retry_policy=RetryPolicy()
                      )

    workflow.add_edge(START,"classificate_query")
    workflow.add_edge(END,"generate_response")
    workflow.add_edge(END,"handle_technical_error")
    workflow.add_edge(END,"handle_classification_error")
    
    workflow.add_conditional_edges("classification_query",routing_after_classification)
    workflow.add_conditional_edges("retrieve",routing_after_retrieve)
    return workflow.compile()