from fastapi import APIRouter, HTTPException

from backend.exceptions import (
    DocumentNotFoundError,
    LLMServiceError,
    VectorStoreError,
)
from backend.models.chat import ChatRequest, ChatResponse
from backend.services.chat_service import ChatService

# Router for the chat endpoint, mounted under /chat and tagged "Chat".
router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

chat_service = ChatService()


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        answer = chat_service.chat(
            collection_name=request.collection_name,
            question=request.question,
        )
        return ChatResponse(answer=answer)

    except DocumentNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))

    except VectorStoreError as error:
        raise HTTPException(status_code=500, detail=str(error))

    except LLMServiceError as error:
        raise HTTPException(status_code=503, detail=str(error))

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred.",
        )