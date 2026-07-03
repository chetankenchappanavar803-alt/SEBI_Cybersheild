"""
SEBI CyberShield — FastAPI Application Entry Point
Enterprise AI cybersecurity platform for SEBI TechSprint.
"""
import logging
import sys
import io

# Fix UnicodeEncodeError on Windows terminals that don't support UTF-8
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from config import get_settings
from models.schemas import HealthResponse
from routers import scan, chat, report

# ── Logging Setup ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ]
)
logger = logging.getLogger(__name__)

settings = get_settings()

# ── Rate Limiter ──────────────────────────────────────────────────────────────
limiter = Limiter(key_func=get_remote_address, default_limits=[f"{settings.rate_limit_per_minute}/minute"])


# ── Application Lifespan ──────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle."""
    logger.info("=" * 60)
    logger.info("[SHIELD] SEBI CyberShield starting up...")
    logger.info(f"   Environment  : {settings.app_env}")
    logger.info(f"   Gemini Model : {settings.gemini_default_model}")
    logger.info(f"   Gemini API   : {'[OK] Configured' if settings.gemini_available else '[!!] NOT CONFIGURED'}")
    logger.info(f"   Supabase     : {'[OK] Configured' if settings.supabase_available else '[--] Not configured (running without DB)'}")
    logger.info("=" * 60)

    if not settings.gemini_available:
        logger.warning("[WARN] GEMINI_API_KEY not set. AI features will return fallback responses.")
        logger.warning("   Set GEMINI_API_KEY in backend/.env to enable AI analysis.")

    yield

    logger.info("[SHIELD] SEBI CyberShield shutting down.")


# ── FastAPI App ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="SEBI CyberShield",
    description=(
        "Enterprise AI cybersecurity platform for detecting financial scams, "
        "phishing, and investment fraud targeting Indian investors. "
        "Powered by Google Gemini 2.5 Flash."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# ── Rate Limiting ─────────────────────────────────────────────────────────────
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Global Exception Handler ──────────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred. Please try again."},
    )


# ── Health Check ──────────────────────────────────────────────────────────────
@app.get("/api/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Check API health and service availability."""
    return HealthResponse(
        status="operational",
        version="1.0.0",
        gemini_available=settings.gemini_available,
        supabase_available=settings.supabase_available,
        environment=settings.app_env,
    )


# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(scan.router)
app.include_router(chat.router)
app.include_router(report.router)


# ── Serve Frontend (optional — for production single-server deploy) ────────────
import os
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.isdir(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")


# ── Dev server entrypoint ─────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.is_development,
        log_level="info",
    )
