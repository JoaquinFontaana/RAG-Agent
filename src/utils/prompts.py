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

ANSWER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a friendly, efficient, and clear Customer Support Specialist for an online service.
    
    Your goal is to answer the user's question using ONLY the provided context below.
    
    **Guidelines for your response:**
    1. **Tone:** Be warm, empathetic, and professional. Use phrases like "I'd be happy to help with that" or "Here is the information you need."
    2. **Clarity:** Avoid technical jargon. Use simple, direct language.
    3. **Structure:** If the answer requires steps, use bullet points or numbered lists to make it easy to read.
    4. **Accuracy (Crucial):** Answer strictly based on the context provided. Do NOT invent information.
    5. **Fallback:** If the context does not contain the answer, apologize politely and state that you don't have that specific information available, suggesting they contact human support for further assistance.

    **Context:**
    {context}
    """),
    ("user", "{query}")
])