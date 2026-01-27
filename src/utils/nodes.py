from src.utils import get_llm, AgentState, ClassificationOutput,CLASSIFICATOR_PROMPT
from typing import cast
def classificate_query(state:AgentState):
    if not state.get("user_query"):
        return {"error": "Input query cannot be empty"}
    
    llm = get_llm()

    structured_llm = llm.with_structured_output(
        ClassificationOutput,
        method="function_calling"
        )

    chain = CLASSIFICATOR_PROMPT | structured_llm

    result = cast(ClassificationOutput,chain.invoke({"query": state['user_query']}))
    
    return {"classificate_query":result}


def retrieve():

def error():

def generate_response():

