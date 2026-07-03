"""
SEBI CyberShield — Chat API Router
AI Financial Safety Assistant powered by Gemini.
"""
import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse

from middleware.auth import get_current_user
from models.schemas import ChatRequest, ChatResponse
from services import gemini_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Chat"])


@router.post("/chat", response_model=ChatResponse, summary="AI Financial Safety Assistant")
async def chat(
    request: ChatRequest,
    current_user: Optional[dict] = Depends(get_current_user)
):
    """
    Conversational AI assistant for financial safety questions.
    Powered by Gemini — answers questions about scams, SEBI, phishing, etc.
    Maintains conversation history for context.
    """
    if not request.message.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Message cannot be empty"
        )

    try:
        history = [msg.model_dump() for msg in request.history]
        reply = await gemini_service.chat(
            message=request.message,
            history=history,
            model_choice=request.model.value
        )

        from config import get_settings
        settings = get_settings()
        model_name = settings.gemini_pro_model if request.model.value == "pro" else settings.gemini_default_model

        return ChatResponse(reply=reply, model_used=model_name)

    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat failed: {str(e)}"
        )
