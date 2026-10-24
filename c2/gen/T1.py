import re


def split_amount(total: str, n: int) -> list[str]:
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError("n must be an integer >= 1")
    if not isinstance(total, str):
        raise ValueError("total must be a string")

    m = re.fullmatch(r"\s*(-)?(\d+)\.(\d{2})\s*", total)
    if not m:
        raise ValueError("total must be a decimal string with exactly 2 decimal places")

    sign, whole, frac = m.groups()
    cents = int(whole) * 100 + int(frac)
    if sign and cents > 0:
        raise ValueError("total must not be negative")

    q, r = divmod(cents, n)
    parts = [q + 1] * r + [q] * (n - r)
    return [f"{c // 100}.{c % 100:02d}" for c in parts]
