from fastapi import APIRouter
from src.models.chat_request import ChatRequest
from src.agent import invoke_workflow

router = APIRouter(
    prefix="/chats",
    tags=["Chat"],
    responses={404: {"description": "Not found"}}
)

@router.post("", summary="Send a chat message", description="Send a message to the RAG agent and get a response")
async def chat_endpoint(request: ChatRequest):
    
    result = invoke_workflow(request)
    
    return {
        "thread_id": request.thread_id,
        "response": result["response"]
    }