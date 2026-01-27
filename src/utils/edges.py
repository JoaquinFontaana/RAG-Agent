from src.utils import AgentState

def routing_after_classification(state:AgentState):
    if state.get("error"):
        return "handle_technical_error"
    category = state.get("classification_query").category
    if category == "appropriate":
        if state.get("classification_query").needs_retrieval:
            return "retrieve"
        else:
            return "generate_response"
    else:
        if category == "needs_human":
            return "human"
        else:
            return "handle_classification_error"
    
def routing_after_retrieve(state:AgentState):
    if state.get("error"):
        return "handle_technical_error"
    return "generate_response"