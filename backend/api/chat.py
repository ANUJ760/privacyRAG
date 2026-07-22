from fastapi import APIRouter, HTTPException
from backend.services.chat_service import ChatService
from backend.models.chat import ChatRequest, ChatResponse

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
) # create a router for the chat endpoint with prefix /chat and tag Chat.

chat_service = ChatService()

@router.post("/", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    """
    Query the RAG system with a question and get an answer along with sources.
    """

    try:
        answer = chat_service.chat(req.collection_name, req.question)
        return ChatResponse(answer=answer)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

