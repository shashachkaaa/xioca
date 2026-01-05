# 📦 Xioca UserBot
# Inline form stash (shared between userbot and inline bot)
#
# Stores short-lived payloads for universal inline forms.
# This avoids per-module inline handlers/decorators.

from __future__ import annotations

import time
import secrets
from typing import Any, Dict, Optional, Tuple

# token -> (expires_at, payload)
_STASH: Dict[str, Tuple[float, Dict[str, Any]]] = {}

DEFAULT_TTL = 120  # seconds


def put(payload: Dict[str, Any], ttl: int = DEFAULT_TTL) -> str:
    """Store payload and return a short token."""
    now = time.time()
    # cleanup on write (cheap)
    cleanup(now)
    token = secrets.token_urlsafe(10)
    _STASH[token] = (now + max(5, int(ttl)), payload)
    return token


def get(token: str) -> Optional[Dict[str, Any]]:
    """Get payload without removing it (returns None if expired)."""
    now = time.time()
    item = _STASH.get(token)
    if not item:
        return None
    exp, payload = item
    if exp < now:
        _STASH.pop(token, None)
        return None
    return payload


def pop(token: str) -> Optional[Dict[str, Any]]:
    """Get payload and remove it."""
    payload = get(token)
    _STASH.pop(token, None)
    return payload


def cleanup(now: Optional[float] = None) -> None:
    """Remove expired items."""
    if now is None:
        now = time.time()
    expired = [k for k, (exp, _) in _STASH.items() if exp < now]
    for k in expired:
        _STASH.pop(k, None)
