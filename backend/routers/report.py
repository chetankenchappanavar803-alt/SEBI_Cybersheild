"""
SEBI CyberShield — Report API Router
Generates and downloads AI-enhanced PDF threat reports.
"""
import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import Response

from middleware.auth import get_current_user
from models.schemas import ReportRequest
from services import gemini_service
from services.report_service import generate_threat_report_pdf

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Report"])


@router.post("/report", summary="Generate AI-enhanced PDF threat report")
async def generate_report(
    request: ReportRequest,
    current_user: Optional[dict] = Depends(get_current_user)
):
    """
    Generate a professional PDF threat report from a scan result.
    Returns a downloadable PDF file.
    """
    try:
        # Step 1: Have Gemini enhance the report content
        report_content = await gemini_service.generate_report_content(
            scan_result=request.scan_result,
            scan_type=request.scan_type.value,
            user_input=request.user_input,
            model_choice=request.model.value
        )

        # Step 2: Generate PDF
        pdf_bytes = generate_threat_report_pdf(
            scan_result=request.scan_result,
            report_content=report_content,
            scan_type=request.scan_type.value,
            user_input_preview=request.user_input[:200]
        )

        # Step 3: Return as downloadable PDF
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cybershield_threat_report_{request.scan_type.value}_{timestamp}.pdf"

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Content-Length": str(len(pdf_bytes)),
            }
        )

    except ImportError as e:
        logger.error(f"ReportLab not installed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="PDF generation unavailable — reportlab package not installed"
        )
    except Exception as e:
        logger.error(f"Report generation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Report generation failed: {str(e)}"
        )
