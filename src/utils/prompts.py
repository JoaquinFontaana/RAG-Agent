from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import Literal
class ClassificationOutput(BaseModel):
    """Clasificación de la consulta del usuario."""
    
    category: Literal["appropriate", "inappropriate", "needs_human", "out_of_scope"] = Field(
        description="Category of the question."
    )
    reason: str = Field(
        description="Concise explanation about why you chose that category."
    )
    needs_retrieval: bool = Field(
        description="True if requires internal docs of the company for answer. False if is a gretting or trivial chatting."
    )

CLASSIFICATOR_PROMPT = ChatPromptTemplate([
    ("system","""You are an expert classifier and validator of user queries for a customer service system.

    You must classify each query into ONE of these categories and explain why you classificate in that category:

    1. **appropriate**: Valid customer service questions about products, services, policies, or general inquiries.
    - Examples: "How do I return a product?", "What are your business hours?"

    2. **inappropriate**: Spam, offensive content, or unrelated topics.
    - Examples: spam, insults, completely off-topic content

    3. **needs_human**: Requires human agent intervention - complaints, refunds, sensitive issues.
    - Examples: "I want to speak to a manager", "I need a refund", "complaint"

    4. **out_of_scope**: Private company information and not related to customer service.
    - Examples: employee salaries, internal policies, confidential data, general question no related to the customer service
     
    If the question is **appropiate** decide if need retrieve internal docs for answer
     
    CRITICAL DISTINCTION:
    - "How do I get a refund?" -> **appropriate** (It's an informational question about policy).
    - "I want a refund for order #123" -> **needs_human** (It's an action requiring an agent).
    """),
    ("user", "{query}")
])