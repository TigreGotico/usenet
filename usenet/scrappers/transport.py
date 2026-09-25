"""HTTP transport for the server-list scrapers.

Most of the directories these scrapers read are long dead, so requests are
routed through ``unblock_requests.CloudflareSession`` with the Wayback
fallback enabled: a dead host transparently resolves from archive.org. When
``unblock_requests`` is not installed the session degrades to plain
``requests``.
"""
from functools import lru_cache
from typing import Any

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    )
}

# directories are static archives; be polite and patient with slow mirrors
DEFAULT_TIMEOUT = 15


def _make_session() -> Any:
    try:
        from unblock_requests import CloudflareSession

        session = CloudflareSession(env_prefix="USENET", wayback_fallback=True)
    except ImportError:
        import requests

        session = requests.Session()
    session.headers.update(_HEADERS)
    return session


@lru_cache(maxsize=1)
def get_session() -> Any:
    """Return a process-wide session (anti-bot + Wayback fallback if available)."""
    return _make_session()


def get_html(url: str, timeout: int = DEFAULT_TIMEOUT) -> str:
    """Fetch ``url`` and return the decoded body text."""
    resp = get_session().get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.text
