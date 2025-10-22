from __future__ import annotations

import time
from collections import deque
from typing import Deque, Dict, Tuple

from ..config import settings

# Simple in-process sliding window rate limiter per user id
# For production, move to Redis. This is a lightweight fallback.

_window_seconds = 60
_max_requests = settings.rate_limit_per_minute
_requests_by_user: Dict[str, Deque[float]] = {}


def rate_limit_allow(user_id: str) -> Tuple[bool, int]:
    now = time.time()
    window_start = now - _window_seconds
    dq = _requests_by_user.setdefault(user_id, deque())

    # Evict old timestamps
    while dq and dq[0] < window_start:
        dq.popleft()

    if len(dq) >= _max_requests:
        retry_after = int(max(1, _window_seconds - (now - dq[0])))
        return False, retry_after

    dq.append(now)
    return True, 0
