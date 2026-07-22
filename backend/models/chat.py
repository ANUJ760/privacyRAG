from pydantic import BaseModel


class ChatRequest(BaseModel):
    collection_name: str
    question: str


class ChatResponse(BaseModel):
    answer: str