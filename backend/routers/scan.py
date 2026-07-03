"""
SEBI CyberShield — Scan API Routers
All /api/scan/* endpoints for AI-powered threat analysis.
"""
import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends, status
from fastapi.responses import JSONResponse

from config import get_settings
from middleware.auth import get_current_user
from models.schemas import (
    EmailScanRequest, EmailScanResponse,
    URLScanRequest, URLScanResponse,
    SocialScanRequest, SocialScanResponse,
    ImageScanResponse, ModelChoice
)
from services import gemini_service
from services.scraper_service import fetch_webpage, build_page_content_for_analysis
from database.supabase_client import log_scan

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter(prefix="/api/scan", tags=["Scan"])

# ── Allowed image MIME types ──────────────────────────────────────────────────
ALLOWED_IMAGE_TYPES = {
    "image/jpeg", "image/png", "image/webp",
    "image/gif", "image/bmp", "image/tiff"
}


# ── POST /api/scan/email ──────────────────────────────────────────────────────
@router.post("/email", response_model=dict, summary="Analyze email for phishing")
async def scan_email(
    request: EmailScanRequest,
    current_user: Optional[dict] = Depends(get_current_user)
):
    """
    Analyze email text for phishing, social engineering, and financial fraud.
    Returns structured risk assessment with score 0-100.
    """
    try:
        result = await gemini_service.analyze_email(
            email_text=request.email_text,
            model_choice=request.model.value
        )

        # Log to DB (fire-and-forget)
        user_id = current_user.get("sub") if current_user else None
        await log_scan(
            user_id=user_id,
            scan_type="email",
            risk_score=result.get("risk_score", 0),
            threat_level=result.get("threat", "Unknown"),
            summary=result.get("summary", "")
        )

        return result

    except Exception as e:
        logger.error(f"Email scan endpoint error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


# ── POST /api/scan/url ────────────────────────────────────────────────────────
@router.post("/url", response_model=dict, summary="Analyze website for investment scams")
async def scan_url(
    request: URLScanRequest,
    current_user: Optional[dict] = Depends(get_current_user)
):
    """
    Fetch and analyze a website for investment scams, SEBI impersonation,
    and financial fraud indicators.
    """
    try:
        # Fetch webpage content
        try:
            title, meta_desc, visible_text = await fetch_webpage(request.url)
        except ValueError as e:
            # Can still analyze just the URL structure
            logger.warning(f"Could not fetch URL {request.url}: {e}")
            title, meta_desc, visible_text = "", "", f"Could not fetch page content: {e}"

        page_content = build_page_content_for_analysis(
            request.url, title, meta_desc, visible_text
        )

        result = await gemini_service.analyze_url(
            url=request.url,
            page_content=page_content,
            model_choice=request.model.value
        )

        # Enrich with scraped title if Gemini didn't capture it
        if not result.get("page_title") and title:
            result["page_title"] = title

        user_id = current_user.get("sub") if current_user else None
        await log_scan(
            user_id=user_id,
            scan_type="url",
            risk_score=result.get("risk_score", 0),
            threat_level=result.get("threat", "Unknown"),
            summary=result.get("summary", "")
        )

        return result

    except Exception as e:
        logger.error(f"URL scan endpoint error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


# ── POST /api/scan/social ─────────────────────────────────────────────────────
@router.post("/social", response_model=dict, summary="Analyze social media post for scams")
async def scan_social(
    request: SocialScanRequest,
    current_user: Optional[dict] = Depends(get_current_user)
):
    """
    Analyze text from WhatsApp/Telegram/X/Facebook/Instagram for
    pump-and-dump, fake IPO, crypto fraud, and investment manipulation.
    """
    try:
        result = await gemini_service.analyze_social(
            text=request.text,
            source=request.source.value,
            model_choice=request.model.value
        )

        user_id = current_user.get("sub") if current_user else None
        await log_scan(
            user_id=user_id,
            scan_type="social",
            risk_score=result.get("risk_score", 0),
            threat_level=result.get("threat", "Unknown"),
            summary=result.get("summary", "")
        )

        return result

    except Exception as e:
        logger.error(f"Social scan endpoint error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


# ── POST /api/scan/image ──────────────────────────────────────────────────────
@router.post("/image", response_model=dict, summary="Analyze image/screenshot for scam content")
async def scan_image(
    file: UploadFile = File(..., description="Screenshot or image to analyze (PNG/JPEG/WEBP)"),
    model: str = Form(default="flash"),
    current_user: Optional[dict] = Depends(get_current_user)
):
    """
    Upload a screenshot (WhatsApp, investment message, etc.).
    Gemini Vision extracts text via OCR and analyzes for scam content.
    Max file size: 5MB.
    """
    # Validate MIME type
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unsupported file type: {file.content_type}. Allowed: JPEG, PNG, WEBP, GIF, BMP, TIFF"
        )

    # Validate size
    image_bytes = await file.read()
    if len(image_bytes) > settings.max_upload_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size: {settings.max_upload_size // (1024*1024)}MB"
        )

    if len(image_bytes) < 100:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="File appears to be empty or corrupt"
        )

    try:
        result = await gemini_service.analyze_image(
            image_bytes=image_bytes,
            mime_type=file.content_type,
            model_choice=model
        )

        user_id = current_user.get("sub") if current_user else None
        await log_scan(
            user_id=user_id,
            scan_type="image",
            risk_score=result.get("risk_score", 0),
            threat_level=result.get("threat", "Unknown"),
            summary=result.get("summary", "")
        )

        return result

    except Exception as e:
        logger.error(f"Image scan endpoint error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Image analysis failed: {str(e)}"
        )
