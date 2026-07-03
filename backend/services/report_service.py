"""
SEBI CyberShield — PDF Report Service
Generates professional threat reports using ReportLab.
"""
import io
import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


def _get_risk_color(risk_score: int):
    """Return RGB color tuple based on risk score."""
    from reportlab.lib.colors import HexColor
    if risk_score >= 75:
        return HexColor("#EF4444")   # Red
    elif risk_score >= 45:
        return HexColor("#F59E0B")   # Amber
    else:
        return HexColor("#10B981")   # Green


def generate_threat_report_pdf(
    scan_result: dict,
    report_content: dict,
    scan_type: str,
    user_input_preview: str
) -> bytes:
    """
    Generate a professional PDF threat report.
    Returns raw PDF bytes.
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib.colors import HexColor, white, black
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
            HRFlowable, PageBreak
        )
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
        from reportlab.lib import colors
    except ImportError:
        logger.error("ReportLab not installed. Run: pip install reportlab")
        raise

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title="SEBI CyberShield Threat Report"
    )

    styles = getSampleStyleSheet()
    elements = []

    # ── Color palette ─────────────────────────────────────────────────────────
    DARK_BG = HexColor("#0F0F1A")
    ACCENT = HexColor("#6C63FF")
    DANGER_RED = HexColor("#EF4444")
    SAFE_GREEN = HexColor("#10B981")
    AMBER = HexColor("#F59E0B")
    LIGHT_GRAY = HexColor("#F3F4F6")
    TEXT_DARK = HexColor("#1F2937")
    SECTION_BG = HexColor("#EFF6FF")

    risk_score = scan_result.get("risk_score", 0)
    threat_level = scan_result.get("threat", "Unknown")
    risk_color = _get_risk_color(risk_score)

    # ── Custom Styles ─────────────────────────────────────────────────────────
    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontSize=24, textColor=white, spaceAfter=6,
        alignment=TA_CENTER, fontName="Helvetica-Bold"
    )
    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=11, textColor=HexColor("#CCCCDD"),
        alignment=TA_CENTER, spaceAfter=4
    )
    section_header_style = ParagraphStyle(
        "SectionHeader",
        parent=styles["Heading1"],
        fontSize=14, textColor=ACCENT,
        spaceBefore=16, spaceAfter=8,
        fontName="Helvetica-Bold"
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontSize=10, textColor=TEXT_DARK,
        leading=14, spaceAfter=8, alignment=TA_JUSTIFY
    )
    bullet_style = ParagraphStyle(
        "Bullet",
        parent=styles["Normal"],
        fontSize=10, textColor=TEXT_DARK,
        leading=14, spaceAfter=4,
        leftIndent=15, bulletIndent=0
    )

    # ── Header Banner ─────────────────────────────────────────────────────────
    header_data = [[
        Paragraph('<font color="white"><b>🛡 SEBI CyberShield</b></font>', title_style),
    ]]
    header_table = Table(header_data, colWidths=[17*cm])
    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DARK_BG),
        ("TOPPADDING", (0, 0), (-1, -1), 18),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 18),
        ("LEFTPADDING", (0, 0), (-1, -1), 20),
        ("RIGHTPADDING", (0, 0), (-1, -1), 20),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [DARK_BG]),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 8))

    subtitle_para = Paragraph(
        f"AI Threat Intelligence Report | Generated: {datetime.now().strftime('%d %B %Y, %H:%M IST')}",
        subtitle_style
    )
    sub_data = [[subtitle_para]]
    sub_table = Table(sub_data, colWidths=[17*cm])
    sub_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), HexColor("#1A1A2E")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(sub_table)
    elements.append(Spacer(1, 20))

    # ── Risk Score Summary Box ────────────────────────────────────────────────
    confidence_pct = int(scan_result.get("confidence", 0.85) * 100)
    risk_data = [
        [
            Paragraph(f'<font size="36" color="{risk_color.hexval()}"><b>{risk_score}</b></font>', ParagraphStyle("rs", alignment=TA_CENTER, fontName="Helvetica-Bold")),
            Paragraph(f'<font size="18" color="{risk_color.hexval()}"><b>{threat_level}</b></font><br/><font size="10" color="#6B7280">Threat Level</font>', ParagraphStyle("tl", alignment=TA_CENTER)),
            Paragraph(f'<font size="18" color="{ACCENT.hexval()}"><b>{confidence_pct}%</b></font><br/><font size="10" color="#6B7280">AI Confidence</font>', ParagraphStyle("conf", alignment=TA_CENTER)),
            Paragraph(f'<font size="12" color="#374151"><b>{scan_type.upper()}</b></font><br/><font size="10" color="#6B7280">Scan Type</font>', ParagraphStyle("st", alignment=TA_CENTER)),
        ]
    ]
    risk_table = Table(risk_data, colWidths=[4.25*cm, 4.25*cm, 4.25*cm, 4.25*cm])
    risk_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GRAY),
        ("BOX", (0, 0), (-1, -1), 1, HexColor("#E5E7EB")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, HexColor("#E5E7EB")),
        ("TOPPADDING", (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTBORDERPADDING", (0, 0), (0, -1), 2),
    ]))
    elements.append(risk_table)
    elements.append(Spacer(1, 20))

    # ── Executive Summary ─────────────────────────────────────────────────────
    elements.append(Paragraph("Executive Summary", section_header_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=8))
    exec_summary = report_content.get("executive_summary", scan_result.get("summary", ""))
    elements.append(Paragraph(exec_summary.replace("\n", "<br/>"), body_style))
    elements.append(Spacer(1, 12))

    # ── Threat Analysis ───────────────────────────────────────────────────────
    elements.append(Paragraph("Threat Analysis", section_header_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=8))
    threat_analysis = report_content.get("threat_analysis", "")
    if threat_analysis:
        elements.append(Paragraph(threat_analysis.replace("\n", "<br/>"), body_style))

    # Detected reasons
    reasons = scan_result.get("reasons", [])
    if reasons:
        elements.append(Paragraph("<b>Detected Threat Indicators:</b>", body_style))
        for reason in reasons:
            elements.append(Paragraph(f"• {reason}", bullet_style))
    elements.append(Spacer(1, 12))

    # ── Evidence ──────────────────────────────────────────────────────────────
    evidence = scan_result.get("evidence", []) or report_content.get("evidence", [])
    if evidence:
        elements.append(Paragraph("Evidence", section_header_style))
        elements.append(HRFlowable(width="100%", thickness=1, color=DANGER_RED, spaceAfter=8))
        for item in evidence:
            ev_para = Paragraph(f'<font color="{DANGER_RED.hexval()}">⚠</font> {item}', bullet_style)
            elements.append(ev_para)
        elements.append(Spacer(1, 12))

    # ── Incident Response ─────────────────────────────────────────────────────
    ir_steps = report_content.get("incident_response_steps", scan_result.get("recommendations", []))
    if ir_steps:
        elements.append(Paragraph("Incident Response Steps", section_header_style))
        elements.append(HRFlowable(width="100%", thickness=1, color=AMBER, spaceAfter=8))
        for i, step in enumerate(ir_steps, 1):
            elements.append(Paragraph(f"{i}. {step}", bullet_style))
        elements.append(Spacer(1, 12))

    # ── Prevention Measures ───────────────────────────────────────────────────
    prevention = report_content.get("prevention_measures", [])
    if prevention:
        elements.append(Paragraph("Prevention Measures", section_header_style))
        elements.append(HRFlowable(width="100%", thickness=1, color=SAFE_GREEN, spaceAfter=8))
        for item in prevention:
            elements.append(Paragraph(f"✓ {item}", bullet_style))
        elements.append(Spacer(1, 12))

    # ── Regulatory Note ───────────────────────────────────────────────────────
    reg_impl = report_content.get("regulatory_implications", "")
    if reg_impl:
        elements.append(Paragraph("Regulatory Implications", section_header_style))
        elements.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=8))
        elements.append(Paragraph(reg_impl, body_style))
        elements.append(Spacer(1, 12))

    # ── Footer ────────────────────────────────────────────────────────────────
    footer_text = (
        "This report was generated by SEBI CyberShield AI. "
        "Report financial fraud at: SEBI SCORES Portal (scores.sebi.gov.in) | "
        "Cybercrime Portal (cybercrime.gov.in) | Toll-free: 1930"
    )
    footer_data = [[Paragraph(f'<font size="8" color="{HexColor("#6B7280").hexval()}">{footer_text}</font>', ParagraphStyle("footer", alignment=TA_CENTER))]]
    footer_table = Table(footer_data, colWidths=[17*cm])
    footer_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GRAY),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("BOX", (0, 0), (-1, -1), 0.5, HexColor("#E5E7EB")),
    ]))
    elements.append(Spacer(1, 20))
    elements.append(footer_table)

    doc.build(elements)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    logger.info(f"PDF report generated: {len(pdf_bytes)} bytes")
    return pdf_bytes
