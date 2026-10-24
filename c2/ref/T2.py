import email.utils
def parse_retry_after(value, now):
    v = (value or "").strip()
    if v.lstrip('-').isdigit(): return max(0.0, float(int(v)))
    try:
        d = email.utils.parsedate_to_datetime(v)
    except Exception: return 0.0
    if d is None: return 0.0
    return max(0.0, (d - now).total_seconds())
