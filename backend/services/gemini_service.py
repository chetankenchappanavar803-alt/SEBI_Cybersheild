"""
SEBI CyberShield — Core Gemini AI Service Module
All Gemini API interactions are centralized here.
Implements: retry logic, caching, timeout handling, graceful fallback.
"""
import asyncio
import json
import logging
import re
import time
from functools import wraps
from typing import Any, Optional
from cachetools import TTLCache

from config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()

# ── In-memory response cache (hash → result, TTL = 5 min) ────────────────────
_cache: TTLCache = TTLCache(maxsize=500, ttl=settings.cache_ttl)

# ── System Prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are an AI cybersecurity analyst specializing in India's securities market and financial fraud detection.
Your expertise covers:
- Phishing and social engineering attacks targeting retail investors
- Impersonation of SEBI (Securities and Exchange Board of India), NSE, BSE, and RBI
- Investment scams: fake IPOs, pump-and-dump schemes, guaranteed return frauds
- Cryptocurrency fraud and manipulation
- Deepfake and synthetic media indicators in financial communications
- WhatsApp/Telegram investment group manipulation
- Regulatory violations in financial communication

Always analyze communications with these principles:
1. Assume the perspective of an Indian retail investor who may be vulnerable
2. Look for urgency tactics, authority impersonation, and too-good-to-be-true promises
3. Identify regulatory red flags (unregistered investment advisors, fake SEBI registration numbers)
4. Consider linguistic patterns common in Indian financial scams

CRITICAL: Always return ONLY valid JSON with no markdown formatting, no code blocks, no extra text.
The JSON must match the exact schema requested in the user message."""

# ── Retry decorator ───────────────────────────────────────────────────────────
def async_retry(max_attempts: int = 3, base_delay: float = 1.0, exceptions=(Exception,)):
    """Exponential backoff retry decorator for async functions."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    if attempt < max_attempts - 1:
                        delay = base_delay * (2 ** attempt)
                        logger.warning(f"Gemini attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                        await asyncio.sleep(delay)
                    else:
                        logger.error(f"Gemini failed after {max_attempts} attempts: {e}")
            raise last_exc
        return wrapper
    return decorator


# ── Cache key helper ──────────────────────────────────────────────────────────
def _cache_key(prefix: str, content: str, model: str) -> str:
    import hashlib
    h = hashlib.md5(f"{prefix}:{model}:{content}".encode()).hexdigest()
    return h


# ── Gemini client getter ──────────────────────────────────────────────────────
def _get_client():
    """Get Gemini client. Returns None if API key not configured."""
    if not settings.gemini_available:
        return None
    try:
        from google import genai
        return genai.Client(api_key=settings.gemini_api_key)
    except ImportError:
        logger.error("google-genai package not installed. Run: pip install google-genai")
        return None
    except Exception as e:
        logger.error(f"Failed to initialize Gemini client: {e}")
        return None


def _get_model_name(model_choice: str) -> str:
    """Resolve model choice to actual model name."""
    if model_choice == "pro":
        return settings.gemini_pro_model
    return settings.gemini_default_model


# ── Fallback responses ────────────────────────────────────────────────────────
def _fallback_threat_response(scan_type: str, reason: str = "AI service temporarily unavailable") -> dict:
    return {
        "risk_score": 0,
        "threat": "Unknown",
        "summary": f"Analysis could not be completed: {reason}. Please configure GEMINI_API_KEY.",
        "reasons": [reason],
        "recommendations": [
            "Configure your GEMINI_API_KEY in the .env file",
            "Restart the backend server",
            "Contact support if the issue persists"
        ],
        "evidence": [],
        "confidence": 0.0,
        "scan_type": scan_type,
        "model_used": "fallback",
        "error": True
    }


# ── JSON parser ───────────────────────────────────────────────────────────────
def _parse_json_response(text: str) -> dict:
    """Robustly parse JSON from Gemini response, handling markdown code blocks."""
    text = text.strip()
    # Remove markdown code blocks if present
    if "```json" in text:
        text = re.sub(r"```json\s*", "", text)
        text = re.sub(r"```\s*$", "", text)
    elif "```" in text:
        text = re.sub(r"```\s*", "", text)
    text = text.strip()
    return json.loads(text)


# ── Core generate function ────────────────────────────────────────────────────
@async_retry(max_attempts=3, base_delay=1.5)
async def _generate(client, model_name: str, prompt: str, system: str = SYSTEM_PROMPT) -> str:
    """Send a prompt to Gemini and return the text response."""
    from google.genai import types

    response = await asyncio.wait_for(
        asyncio.get_event_loop().run_in_executor(
            None,
            lambda: client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system,
                    temperature=0.1,   # Low temperature for consistent, deterministic analysis
                    max_output_tokens=4096,
                )
            )
        ),
        timeout=settings.gemini_timeout
    )
    return response.text


@async_retry(max_attempts=3, base_delay=1.5)
async def _generate_with_image(client, model_name: str, prompt: str, image_bytes: bytes, mime_type: str) -> str:
    """Send an image + prompt to Gemini Vision."""
    from google.genai import types

    response = await asyncio.wait_for(
        asyncio.get_event_loop().run_in_executor(
            None,
            lambda: client.models.generate_content(
                model=model_name,
                contents=[
                    types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                    prompt
                ],
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.1,
                    max_output_tokens=4096,
                )
            )
        ),
        timeout=settings.gemini_timeout
    )
    return response.text


# ══════════════════════════════════════════════════════════════════════════════
# PUBLIC AI SERVICE FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

async def analyze_email(email_text: str, model_choice: str = "flash") -> dict:
    """Analyze an email for phishing and financial fraud indicators."""
    cache_key = _cache_key("email", email_text[:500], model_choice)
    if cache_key in _cache:
        logger.info("Cache hit: email analysis")
        return _cache[cache_key]

    client = _get_client()
    if not client:
        return _fallback_threat_response("email")

    model_name = _get_model_name(model_choice)

    prompt = f"""Analyze the following email for phishing, social engineering, and financial fraud indicators targeting Indian investors.

EMAIL TEXT:
{email_text}

Return ONLY this JSON schema (no other text):
{{
  "risk_score": <integer 0-100>,
  "threat": <"Safe"|"Low Risk"|"Medium Risk"|"High Risk"|"Critical">,
  "summary": <string, 1-2 sentences>,
  "reasons": [<list of detected threat indicators>],
  "recommendations": [<list of recommended actions for the recipient>],
  "evidence": [<list of exact suspicious phrases from the email>],
  "confidence": <float 0.0-1.0>,
  "phishing_probability": <float 0.0-1.0>,
  "social_engineering_indicators": [<list of social engineering tactics found>],
  "suspicious_links": [<list of suspicious URLs found>],
  "urgency_manipulation": <boolean>,
  "grammar_anomalies": [<list of grammar/spelling errors suggesting non-native authorship>],
  "financial_scam_indicators": [<list of financial fraud indicators>],
  "scan_type": "email"
}}"""

    try:
        raw = await _generate(client, model_name, prompt)
        result = _parse_json_response(raw)
        result["model_used"] = model_name
        result["scan_type"] = "email"
        _cache[cache_key] = result
        logger.info(f"Email analysis complete: risk_score={result.get('risk_score')}")
        return result
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error in email analysis: {e}")
        return _fallback_threat_response("email", "AI returned malformed response")
    except asyncio.TimeoutError:
        return _fallback_threat_response("email", "Request timed out")
    except Exception as e:
        logger.error(f"Email analysis failed: {e}")
        return _fallback_threat_response("email", str(e))


async def analyze_url(url: str, page_content: str, model_choice: str = "flash") -> dict:
    """Analyze a website's content for investment scam indicators."""
    cache_key = _cache_key("url", url + page_content[:300], model_choice)
    if cache_key in _cache:
        logger.info("Cache hit: URL analysis")
        return _cache[cache_key]

    client = _get_client()
    if not client:
        return _fallback_threat_response("url")

    model_name = _get_model_name(model_choice)

    prompt = f"""Analyze the following website content for investment scams, SEBI impersonation, and financial fraud.

URL: {url}
PAGE CONTENT (first 3000 chars):
{page_content[:3000]}

Return ONLY this JSON schema:
{{
  "risk_score": <integer 0-100>,
  "threat": <"Safe"|"Low Risk"|"Medium Risk"|"High Risk"|"Critical">,
  "summary": <string>,
  "reasons": [<threat indicators>],
  "recommendations": [<recommended actions>],
  "evidence": [<exact suspicious text snippets from the page>],
  "confidence": <float 0.0-1.0>,
  "page_title": <string or null>,
  "domain": <extracted domain string>,
  "fake_investment_promises": [<list of fake investment claims found>],
  "sebi_impersonation": <boolean>,
  "scam_keywords": [<list of scam-related keywords found>],
  "urgency_tactics": [<list of urgency manipulation tactics>],
  "scan_type": "url"
}}"""

    try:
        raw = await _generate(client, model_name, prompt)
        result = _parse_json_response(raw)
        result["model_used"] = model_name
        result["scan_type"] = "url"
        _cache[cache_key] = result
        return result
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error in URL analysis: {e}")
        return _fallback_threat_response("url", "AI returned malformed response")
    except asyncio.TimeoutError:
        return _fallback_threat_response("url", "Request timed out")
    except Exception as e:
        logger.error(f"URL analysis failed: {e}")
        return _fallback_threat_response("url", str(e))


async def analyze_social(text: str, source: str = "Unknown", model_choice: str = "flash") -> dict:
    """Analyze social media post for financial scam indicators."""
    cache_key = _cache_key("social", text[:500], model_choice)
    if cache_key in _cache:
        logger.info("Cache hit: social media analysis")
        return _cache[cache_key]

    client = _get_client()
    if not client:
        return _fallback_threat_response("social")

    model_name = _get_model_name(model_choice)

    prompt = f"""Analyze the following social media message for financial scams targeting Indian investors.

SOURCE PLATFORM: {source}
MESSAGE TEXT:
{text}

Return ONLY this JSON schema:
{{
  "risk_score": <integer 0-100>,
  "threat": <"Safe"|"Low Risk"|"Medium Risk"|"High Risk"|"Critical">,
  "threat_category": <"Investment Scam"|"Crypto Fraud"|"Pump & Dump"|"Fake IPO"|"Authority Impersonation"|"Phishing"|"Safe"|"Other">,
  "summary": <string>,
  "reasons": [<threat indicators>],
  "recommendations": [<recommended actions>],
  "evidence": [<exact suspicious phrases from the message>],
  "confidence": <float 0.0-1.0>,
  "pump_dump_indicators": [<list of pump-and-dump signals>],
  "fake_ipo_indicators": [<list of fake IPO signals>],
  "guaranteed_returns": <boolean>,
  "authority_impersonation": [<list of impersonated authorities e.g. "SEBI", "RBI">],
  "crypto_fraud_indicators": [<list of crypto scam signals>],
  "investment_manipulation": [<list of investment manipulation tactics>],
  "recommended_action": <string, one clear recommended action>,
  "scan_type": "social"
}}"""

    try:
        raw = await _generate(client, model_name, prompt)
        result = _parse_json_response(raw)
        result["model_used"] = model_name
        result["scan_type"] = "social"
        _cache[cache_key] = result
        return result
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error in social analysis: {e}")
        return _fallback_threat_response("social", "AI returned malformed response")
    except asyncio.TimeoutError:
        return _fallback_threat_response("social", "Request timed out")
    except Exception as e:
        logger.error(f"Social analysis failed: {e}")
        return _fallback_threat_response("social", str(e))


async def analyze_image(image_bytes: bytes, mime_type: str, model_choice: str = "flash") -> dict:
    """Analyze an image using Gemini Vision for scam content."""
    client = _get_client()
    if not client:
        return {**_fallback_threat_response("image"), "extracted_text": None, "text_length": 0}

    model_name = _get_model_name(model_choice)

    prompt = """First, extract ALL text visible in this image (OCR).
Then analyze the extracted text for financial scams, phishing, investment fraud, or SEBI impersonation targeting Indian investors.

Return ONLY this JSON schema:
{
  "risk_score": <integer 0-100>,
  "threat": <"Safe"|"Low Risk"|"Medium Risk"|"High Risk"|"Critical">,
  "summary": <string>,
  "reasons": [<threat indicators>],
  "recommendations": [<recommended actions>],
  "evidence": [<exact suspicious phrases extracted from the image>],
  "confidence": <float 0.0-1.0>,
  "extracted_text": <all text extracted from the image>,
  "text_length": <number of characters extracted>,
  "scan_type": "image"
}"""

    try:
        raw = await _generate_with_image(client, model_name, prompt, image_bytes, mime_type)
        result = _parse_json_response(raw)
        result["model_used"] = model_name
        result["scan_type"] = "image"
        return result
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error in image analysis: {e}")
        return {**_fallback_threat_response("image", "AI returned malformed response"), "extracted_text": None, "text_length": 0}
    except asyncio.TimeoutError:
        return {**_fallback_threat_response("image", "Request timed out"), "extracted_text": None, "text_length": 0}
    except Exception as e:
        logger.error(f"Image analysis failed: {e}")
        return {**_fallback_threat_response("image", str(e)), "extracted_text": None, "text_length": 0}


async def chat(message: str, history: list, model_choice: str = "flash") -> str:
    """AI Financial Safety Chatbot powered by Gemini."""
    client = _get_client()
    if not client:
        return ("I'm unable to process your request right now because the Gemini API is not configured. "
                "Please add your GEMINI_API_KEY to the .env file and restart the server.")

    model_name = _get_model_name(model_choice)

    # Build conversation context
    history_text = ""
    for msg in history[-10:]:  # Last 10 messages for context
        role = "User" if msg.get("role") == "user" else "Assistant"
        history_text += f"{role}: {msg.get('content', '')}\n"

    chat_system = """You are CyberShield AI — a friendly, expert financial safety assistant for Indian investors.
You help users understand:
- How to identify phishing emails, scam messages, and fake investment offers
- SEBI regulations and how to verify legitimate financial advisors
- Common scam tactics targeting Indian retail investors
- How to report financial fraud to SEBI, NSE, BSE, or Cybercrime Cell
- Safe investing practices and red flags to avoid

IMPORTANT RULES:
- Always respond in simple, clear language that a non-technical user can understand
- If asked about a specific investment opportunity, advise caution and suggest verification steps
- Never provide specific investment advice (stock picks, returns predictions)
- Always recommend reporting suspicious activity to SEBI SCORES portal (scores.sebi.gov.in)
- Be empathetic — users may have already been scammed
- Keep responses concise (under 300 words) unless detailed explanation is explicitly needed"""

    prompt = f"""Previous conversation:
{history_text}

User's current question: {message}

Provide a helpful, empathetic response about financial safety."""

    try:
        from google.genai import types
        response = await asyncio.wait_for(
            asyncio.get_event_loop().run_in_executor(
                None,
                lambda: client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=chat_system,
                        temperature=0.4,
                        max_output_tokens=1024,
                    )
                )
            ),
            timeout=settings.gemini_timeout
        )
        return response.text
    except asyncio.TimeoutError:
        return "I'm experiencing a delay. Please try again in a moment."
    except Exception as e:
        logger.error(f"Chat failed: {e}")
        return "I encountered an issue processing your message. Please try again."


async def generate_report_content(scan_result: dict, scan_type: str, user_input: str, model_choice: str = "flash") -> dict:
    """Generate a structured threat report from scan results using Gemini."""
    client = _get_client()
    if not client:
        return {
            "executive_summary": "Report generation unavailable — Gemini API not configured.",
            "threat_analysis": "",
            "evidence": [],
            "risk_level": scan_result.get("threat", "Unknown"),
            "recommendations": scan_result.get("recommendations", []),
            "incident_response": ""
        }

    model_name = _get_model_name(model_choice)

    prompt = f"""Based on this cybersecurity threat analysis, generate a professional threat report.

SCAN TYPE: {scan_type.upper()}
ANALYSIS RESULT: {json.dumps(scan_result, indent=2)}
ORIGINAL CONTENT SCANNED: {user_input[:500]}

Return ONLY this JSON:
{{
  "executive_summary": <2-3 paragraph executive summary for a non-technical audience>,
  "threat_analysis": <detailed technical analysis of the threat>,
  "evidence": [<list of key evidence points with explanation>],
  "risk_level": <overall risk assessment>,
  "incident_response_steps": [<ordered list of immediate actions to take>],
  "regulatory_implications": <SEBI/RBI/legal implications if any>,
  "prevention_measures": [<list of preventive measures for the future>]
}}"""

    try:
        raw = await _generate(client, model_name, prompt)
        result = _parse_json_response(raw)
        return result
    except Exception as e:
        logger.error(f"Report generation failed: {e}")
        return {
            "executive_summary": scan_result.get("summary", "Analysis complete."),
            "threat_analysis": "\n".join(scan_result.get("reasons", [])),
            "evidence": scan_result.get("evidence", []),
            "risk_level": scan_result.get("threat", "Unknown"),
            "incident_response_steps": scan_result.get("recommendations", []),
            "regulatory_implications": "",
            "prevention_measures": []
        }
