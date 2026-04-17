"""
Global rate limiter for all outbound HTTP requests.

PubMed's E-utilities allow 3 requests/second without an API key.
We use a token-bucket algorithm so bursts are smoothed and no single
second ever exceeds the cap, regardless of how many threads are running.

Usage
-----
    from rate_limiter import rate_limited_get

    response = rate_limited_get(url, params=params)

Or wrap an existing requests.Session:

    from rate_limiter import install_on_session
    install_on_session(session)
"""

from __future__ import annotations

import logging
import threading
import time
from typing import Any

import requests

log = logging.getLogger(__name__)


class TokenBucket:
    """Thread-safe token-bucket rate limiter.

    Args:
        rate:     Maximum requests per second.
        capacity: Maximum burst size (defaults to rate, i.e. no burst).
    """

    def __init__(self, rate: float = 3.0, capacity: float | None = None):
        self._rate = rate
        self._capacity = capacity if capacity is not None else rate
        self._tokens = self._capacity
        self._last_refill = time.monotonic()
        self._lock = threading.Lock()

    def acquire(self) -> None:
        """Block until a token is available, then consume one."""
        with self._lock:
            while True:
                now = time.monotonic()
                elapsed = now - self._last_refill
                self._tokens = min(
                    self._capacity,
                    self._tokens + elapsed * self._rate,
                )
                self._last_refill = now

                if self._tokens >= 1.0:
                    self._tokens -= 1.0
                    return

                # Sleep for the time needed to accumulate one token
                wait = (1.0 - self._tokens) / self._rate
                # Release the lock while sleeping so other threads can check
                self._lock.release()
                time.sleep(wait)
                self._lock.acquire()


# Module-level singleton — shared across all threads
_bucket = TokenBucket(rate=3.0)


def rate_limited_get(url: str, **kwargs: Any) -> requests.Response:
    """Drop-in replacement for requests.get that respects the rate limit."""
    _bucket.acquire()
    log.debug(f"rate_limited_get → {url}")
    return requests.get(url, **kwargs)


def install_on_session(session: requests.Session) -> None:
    """Wrap session.get so every call through this session is rate-limited."""
    original_get = session.get

    def _get(url, **kwargs):
        _bucket.acquire()
        log.debug(f"rate_limited session.get → {url}")
        return original_get(url, **kwargs)

    session.get = _get
