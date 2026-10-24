from decimal import Decimal
def split_amount(total, n):
    if n < 1: raise ValueError
    c = Decimal(total)
    if c < 0: raise ValueError
    cents = int((c*100).to_integral_value())
    q, r = divmod(cents, n)
    parts = [q+1]*r + [q]*(n-r)
    return [f"{p//100}.{p%100:02d}" for p in parts]
