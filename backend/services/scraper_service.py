"""
SEBI CyberShield — Web Scraper Service
Async URL content extraction using httpx + BeautifulSoup.
"""
import logging
import re
from typing import Tuple, Optional
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup

from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Browser-like headers to avoid blocks
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}

# Max characters of visible text to send to Gemini
MAX_TEXT_LENGTH = 5000


async def fetch_webpage(url: str) -> Tuple[str, str, str]:
    """
    Fetch a webpage and extract title, meta description, and visible text.
    
    Returns:
        Tuple of (title, meta_description, visible_text)
    Raises:
        httpx.HTTPError on network errors
        ValueError on invalid URLs
    """
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL: {url}")

    async with httpx.AsyncClient(
        headers=HEADERS,
        follow_redirects=True,
        timeout=settings.request_timeout,
        verify=False,  # Some scam sites have invalid SSL — still analyze content
    ) as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            html = response.text
        except httpx.TimeoutException:
            raise ValueError("Request timed out — website took too long to respond")
        except httpx.ConnectError:
            raise ValueError("Could not connect to website — it may be offline or blocking requests")
        except httpx.HTTPStatusError as e:
            raise ValueError(f"Website returned error: {e.response.status_code}")

    soup = BeautifulSoup(html, "html.parser")

    # Extract title
    title = ""
    if soup.title and soup.title.string:
        title = soup.title.string.strip()

    # Extract meta description
    meta_desc = ""
    meta_tag = soup.find("meta", attrs={"name": "description"})
    if meta_tag and meta_tag.get("content"):
        meta_desc = meta_tag["content"].strip()

    # Extract visible text (remove scripts, styles, nav, footer noise)
    for tag in soup(["script", "style", "noscript", "nav", "footer", "header", "aside"]):
        tag.decompose()

    visible_text = soup.get_text(separator=" ", strip=True)
    # Collapse whitespace
    visible_text = re.sub(r"\s+", " ", visible_text).strip()
    visible_text = visible_text[:MAX_TEXT_LENGTH]

    logger.info(f"Scraped URL {url}: title='{title[:50]}', text_len={len(visible_text)}")
    return title, meta_desc, visible_text


def build_page_content_for_analysis(url: str, title: str, meta_desc: str, visible_text: str) -> str:
    """Format extracted webpage data into a structured string for Gemini analysis."""
    parts = [
        f"URL: {url}",
        f"Page Title: {title}" if title else "",
        f"Meta Description: {meta_desc}" if meta_desc else "",
        f"Visible Content:\n{visible_text}" if visible_text else "",
    ]
    return "\n".join(p for p in parts if p)
