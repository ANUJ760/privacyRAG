import traceback

from fastapi import APIRouter, HTTPException

from backend.exceptions import (
    DocumentNotFoundError,
    InvalidModelError,
    LLMServiceError,
    VectorStoreError,
)
from backend.models.chat import ChatRequest, ChatResponse, ModelOptionsResponse
from backend.services.chat_service import ChatService

# Router for the chat endpoint, mounted under /chat and tagged "Chat".
router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

chat_service = ChatService()


@router.get("/models", response_model=ModelOptionsResponse)
async def get_models():
    return chat_service.get_model_options()


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        answer = chat_service.chat(
            collection_name=request.collection_name,
            question=request.question,
            history=request.history,
            model_name=request.model_name,
        )
        return ChatResponse(answer=answer)

    except InvalidModelError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except DocumentNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))

    except VectorStoreError as error:
        raise HTTPException(status_code=500, detail=str(error))

    except LLMServiceError as error:
        raise HTTPException(status_code=503, detail=str(error))

    except Exception as e:
        traceback.print_exc()   # Print full traceback to terminal
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
