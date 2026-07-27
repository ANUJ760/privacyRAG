from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    collection_name: str
    question: str
    history: list[ChatMessage] = Field(default_factory=list)
    model_name: str | None = None


class ChatResponse(BaseModel):
    answer: str


class ModelOptionsResponse(BaseModel):
    default_model: str
    models: list[str]
