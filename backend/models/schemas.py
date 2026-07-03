"""
SEBI CyberShield — Pydantic Schemas
All request/response models for type safety and validation.
"""
from pydantic import BaseModel, HttpUrl, Field, field_validator
from typing import Optional, List, Any
from enum import Enum


# ── Enums ────────────────────────────────────────────────────────────────────

class ThreatLevel(str, Enum):
    SAFE = "Safe"
    LOW = "Low Risk"
    MEDIUM = "Medium Risk"
    HIGH = "High Risk"
    CRITICAL = "Critical"


class ScanType(str, Enum):
    EMAIL = "email"
    URL = "url"
    SOCIAL = "social"
    IMAGE = "image"


class ModelChoice(str, Enum):
    FLASH = "flash"
    PRO = "pro"


# ── Base Response ─────────────────────────────────────────────────────────────

class ThreatAnalysis(BaseModel):
    risk_score: int = Field(..., ge=0, le=100, description="Risk score 0-100")
    threat: str = Field(..., description="Threat level label")
    summary: str = Field(..., description="Brief threat summary")
    reasons: List[str] = Field(default_factory=list, description="Detected threat indicators")
    recommendations: List[str] = Field(default_factory=list, description="Recommended actions")
    evidence: List[str] = Field(default_factory=list, description="Specific evidence from content")
    confidence: float = Field(default=0.85, ge=0.0, le=1.0, description="AI confidence score")
    scan_type: Optional[str] = None
    model_used: Optional[str] = None


# ── Email Scan ────────────────────────────────────────────────────────────────

class EmailScanRequest(BaseModel):
    email_text: str = Field(..., min_length=10, max_length=50000, description="Full email text to analyze")
    model: ModelChoice = Field(default=ModelChoice.FLASH)

    @field_validator("email_text")
    @classmethod
    def strip_email_text(cls, v: str) -> str:
        return v.strip()


class EmailScanResponse(ThreatAnalysis):
    phishing_probability: float = Field(default=0.0, ge=0.0, le=1.0)
    social_engineering_indicators: List[str] = Field(default_factory=list)
    suspicious_links: List[str] = Field(default_factory=list)
    urgency_manipulation: bool = False
    grammar_anomalies: List[str] = Field(default_factory=list)
    financial_scam_indicators: List[str] = Field(default_factory=list)


# ── URL Scan ──────────────────────────────────────────────────────────────────

class URLScanRequest(BaseModel):
    url: str = Field(..., description="URL to analyze")
    model: ModelChoice = Field(default=ModelChoice.FLASH)

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        v = v.strip()
        if not v.startswith(("http://", "https://")):
            v = "https://" + v
        return v


class URLScanResponse(ThreatAnalysis):
    page_title: Optional[str] = None
    domain: Optional[str] = None
    fake_investment_promises: List[str] = Field(default_factory=list)
    sebi_impersonation: bool = False
    scam_keywords: List[str] = Field(default_factory=list)
    urgency_tactics: List[str] = Field(default_factory=list)


# ── Social Media Scan ─────────────────────────────────────────────────────────

class SocialSource(str, Enum):
    WHATSAPP = "WhatsApp"
    TELEGRAM = "Telegram"
    TWITTER = "X (Twitter)"
    FACEBOOK = "Facebook"
    INSTAGRAM = "Instagram"
    OTHER = "Other"


class SocialScanRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=20000, description="Social media post text")
    source: SocialSource = Field(default=SocialSource.OTHER)
    model: ModelChoice = Field(default=ModelChoice.FLASH)

    @field_validator("text")
    @classmethod
    def strip_text(cls, v: str) -> str:
        return v.strip()


class SocialScanResponse(ThreatAnalysis):
    threat_category: Optional[str] = None
    pump_dump_indicators: List[str] = Field(default_factory=list)
    fake_ipo_indicators: List[str] = Field(default_factory=list)
    guaranteed_returns: bool = False
    authority_impersonation: List[str] = Field(default_factory=list)
    crypto_fraud_indicators: List[str] = Field(default_factory=list)
    recommended_action: Optional[str] = None


# ── Image Scan ────────────────────────────────────────────────────────────────

class ImageScanResponse(ThreatAnalysis):
    extracted_text: Optional[str] = None
    text_length: int = 0


# ── Chat ──────────────────────────────────────────────────────────────────────

class ChatMessage(BaseModel):
    role: str = Field(..., description="'user' or 'assistant'")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)
    history: List[ChatMessage] = Field(default_factory=list, max_length=20)
    model: ModelChoice = Field(default=ModelChoice.FLASH)


class ChatResponse(BaseModel):
    reply: str
    model_used: str


# ── Report ────────────────────────────────────────────────────────────────────

class ReportRequest(BaseModel):
    scan_result: dict = Field(..., description="The scan result to generate a report for")
    scan_type: ScanType
    user_input: str = Field(..., description="Original content that was scanned")
    include_recommendations: bool = True
    model: ModelChoice = Field(default=ModelChoice.FLASH)


# ── Health ────────────────────────────────────────────────────────────────────

class HealthResponse(BaseModel):
    status: str
    version: str
    gemini_available: bool
    supabase_available: bool
    environment: str
