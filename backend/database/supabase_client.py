"""
SEBI CyberShield — Supabase Database Client
Handles database initialization and connection.
"""
import logging
from typing import Optional

from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

_supabase_client = None


def get_supabase():
    """
    Get Supabase client. Returns None if Supabase is not configured.
    Uses service role key for backend operations.
    """
    global _supabase_client
    if _supabase_client is not None:
        return _supabase_client

    if not settings.supabase_available:
        logger.warning("Supabase not configured — running without database.")
        return None

    try:
        from supabase import create_client
        _supabase_client = create_client(
            settings.supabase_url,
            settings.supabase_service_role_key or settings.supabase_anon_key
        )
        logger.info("Supabase client initialized successfully.")
        return _supabase_client
    except ImportError:
        logger.error("supabase package not installed. Run: pip install supabase")
        return None
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {e}")
        return None


async def log_scan(
    user_id: Optional[str],
    scan_type: str,
    risk_score: int,
    threat_level: str,
    summary: str
) -> None:
    """Log a scan result to Supabase for audit trail."""
    client = get_supabase()
    if not client:
        return  # Silently skip if no DB

    try:
        client.table("scan_logs").insert({
            "user_id": user_id,
            "scan_type": scan_type,
            "risk_score": risk_score,
            "threat_level": threat_level,
            "summary": summary,
        }).execute()
    except Exception as e:
        logger.warning(f"Failed to log scan to Supabase: {e}")
