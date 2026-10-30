# ==============================================================================
# KAALCHAKRA COMPUTATION CORE (v7.0.0)
# Daily Quota Governor (20 Credits / Day)
# Resets automatically at 00:00 UTC every day.
# Formulas and source code download remain strictly 0-credit (always free).
# ==============================================================================

import threading
from datetime import datetime, timezone
from typing import Tuple, Dict, Any

DAILY_QUOTA_LIMIT = 20
_lock = threading.Lock()

# In-memory store: { client_id: { "date": "YYYY-MM-DD", "used": int } }
_quota_store: Dict[str, Dict[str, Any]] = {}

def get_current_utc_date() -> str:
    """Returns today's date in YYYY-MM-DD UTC format."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")

def check_and_consume_quota(client_id: str = "default", cost: int = 1) -> Tuple[bool, int, int]:
    """
    Checks if client has sufficient daily quota and consumes credits if allowed.
    Returns:
        (allowed: bool, remaining_credits: int, daily_limit: int)
    """
    today = get_current_utc_date()
    with _lock:
        client_data = _quota_store.get(client_id)
        if not client_data or client_data.get("date") != today:
            client_data = {"date": today, "used": 0}
            _quota_store[client_id] = client_data

        used = client_data["used"]
        remaining = max(0, DAILY_QUOTA_LIMIT - used)

        if cost <= 0:
            return True, remaining, DAILY_QUOTA_LIMIT

        if used + cost > DAILY_QUOTA_LIMIT:
            return False, remaining, DAILY_QUOTA_LIMIT

        client_data["used"] += cost
        remaining = DAILY_QUOTA_LIMIT - client_data["used"]
        return True, remaining, DAILY_QUOTA_LIMIT

def get_quota_status(client_id: str = "default") -> Dict[str, Any]:
    """Returns current daily quota balance and reset time."""
    today = get_current_utc_date()
    with _lock:
        client_data = _quota_store.get(client_id)
        if not client_data or client_data.get("date") != today:
            used = 0
        else:
            used = client_data["used"]
        remaining = max(0, DAILY_QUOTA_LIMIT - used)
        return {
            "date_utc": today,
            "daily_limit": DAILY_QUOTA_LIMIT,
            "credits_used": used,
            "credits_remaining": remaining,
            "resets_at": "00:00 UTC",
            "unlimited_source_download": "https://kalchakra-core.onrender.com/download/source.zip"
        }
