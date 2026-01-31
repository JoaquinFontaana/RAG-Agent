from pydantic import BaseModel
class ChatRequest(BaseModel):
    thread_id:int
    user_query:str