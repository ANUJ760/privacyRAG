from fastapi import APIRouter, HTTPException
from backend.services.chat_service import ChatService
from backend.models.chat import ChatRequest, ChatResponse

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
) # create a router for the chat endpoint with prefix /chat and tag Chat.

chat_service = ChatService()


