import datetime
import re
from email.utils import parsedate_to_datetime


def parse_retry_after(value: str, now: datetime.datetime) -> float:
    """Parse an HTTP Retry-After header value.

    Accepts either delta-seconds (non-negative integer) or an HTTP-date.
    Returns the number of seconds to wait (never negative), or 0.0 if the
    input cannot be parsed.
    """
    if not isinstance(value, str):
        return 0.0

    value = value.strip()
    if not value:
        return 0.0

    # delta-seconds: 1*DIGIT (ASCII digits only)
    if re.fullmatch(r"[0-9]+", value):
        try:
            return max(0.0, float(int(value)))
        except (ValueError, OverflowError):
            return 0.0

    # HTTP-date
    try:
        dt = parsedate_to_datetime(value)
    except (TypeError, ValueError, IndexError, OverflowError):
        return 0.0

    if dt is None:
        return 0.0

    try:
        if dt.tzinfo is None:
            # HTTP-dates are GMT/UTC; treat naive results as UTC
            dt = dt.replace(tzinfo=datetime.timezone.utc)

        if now.tzinfo is None:
            now = now.replace(tzinfo=datetime.timezone.utc)

        delta = (dt - now).total_seconds()
    except (TypeError, ValueError, OverflowError):
        return 0.0

    return max(0.0, float(delta))
