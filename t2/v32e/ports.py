# v3.2e: which candidate rows each port wrongly ACCEPTS, judged by OUR gate (compare_rule.py, soft oracle: 0.6 valid).
# Ports are our own minimal versions of the families named in thread 61ea0360; not the agents' scripts.
import sys, re, json, itertools
from decimal import Decimal
sys.path.insert(0, '..'); import compare_rule as c
def ok(f):
    def g(s):
        try: return bool(f(s))
        except Exception: return False
    return g
def split2(s, test):
    if s.count('.') != 1: return False
    a, b = s.split('.'); return test(a) and test(b)
PORTS = {
 'py float()':            ok(lambda s: float(s) == float(s) and abs(float(s)) != float('inf')),
 'py Decimal()':          ok(lambda s: Decimal(s).is_finite()),
 'py round-trip .2f':     ok(lambda s: f'{float(s):.2f}' == s),
 'py split+isdigit':      ok(lambda s: split2(s, str.isdigit)),
 'py split+isdecimal':    ok(lambda s: split2(s, str.isdecimal)),
 'py split+int,len<=2':   ok(lambda s: split2(s, lambda p: 1 <= len(p) <= 2 and 0 <= int(p) <= 99)),
 'py re.match \\d $':     ok(lambda s: re.match(r'\d+\.\d+$', s)),
 'py re.fullmatch [0-9]': ok(lambda s: re.fullmatch(r'[0-9]+\.[0-9]+', s)),
}
CANDS = ['0.6\n','0.60\n','0.60\r\n','\n0.60','0.60 ','0.6_0','﻿0.60','٠.٦٠','0.6٠',
 '0.-0','0. 6',' .60','0.6x','0.6 ','0.6²','0.٦0','0.٦','nan','NaN','inf','0.٦٦',
 '0.60_','0.6__0','0._60','_0.60','0_.60','1_0.60','0.6_0e0','0.²²','0.６０','0.+0']
def bad(s):  # our gate says the input is not a valid number
    return c.compare(s, '0.60') in ('FAIL invalid', 'FAIL nonfinite')
cands = [s for s in CANDS if bad(s)]
fa = {p: {s for s in cands if f(s)} for p, f in PORTS.items()}
leaky = {p: v for p, v in fa.items() if v}
print('ports with false accepts:', {p: len(v) for p, v in fa.items()})
for k in range(1, 5):
    covers = [combo for combo in itertools.combinations(cands, k) if all(set(combo) & v for v in leaky.values())]
    if covers:
        print('minimum cover size', k, 'count', len(covers)); print('example', [repr(x) for x in covers[0]]); break
