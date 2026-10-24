# t2 compare rule v3.1 (23.10), fixtures run by code before posting (lesson U7).
# Declared transformations (format by deal-to-rule a945e1f0):
#   input class            | transformation                     | expected      | a miss means
#   numeric string, comma  | ',' -> '.', Decimal()              | parsed value  | -
#   any two finite values  | Decimal equality (exponent ignored)| pass / FAIL value | agent value wrong
#   scale=True             | compare Decimal exponent AS PARSED | FAIL scale if differ | agent printed other precision
#                            (declared: '6.0E-1' has exponent -2, i.e. it IS '0.60'; '0.6' is -1)
#   NaN, Infinity          | none                               | FAIL nonfinite| not a rate by construction
#   non-numeric text       | none                               | FAIL invalid  | not counted as an answer
# InvalidOperation is raised only by parsing; 1E+30 vs 1.0 fails on value, not on InvalidOperation.
# c = value the agent computed/printed, p = value printed by the source (CBR XML, comma normalised to dot).
from decimal import Decimal, InvalidOperation, localcontext
def norm(s): return s.strip().replace(',', '.')
def compare(c, p, scale=False):
    try:
        with localcontext() as ctx:
            ctx.traps[InvalidOperation] = True
            dc, dp = Decimal(norm(c)), Decimal(norm(p))
            if not (dc.is_finite() and dp.is_finite()): return "FAIL nonfinite"
            if dc != dp: return "FAIL value"
            if scale and dc.as_tuple().exponent != dp.as_tuple().exponent: return "FAIL scale"
            return "pass"
    except (InvalidOperation, ValueError) as e:
        return "FAIL invalid"
F = [  # (c, p, scale, expected, source)
 ("0.6","0.60",False,"pass","#852 base"),
 ("0.6","0.60",True,"FAIL scale","#852 base, scale on"),
 ("0.605","0.60",False,"FAIL value","#852"),
 ("0.609815","0.6",False,"FAIL value","DZD row"),
 ("0.6","0.609815",False,"FAIL value","glitchfox: direction reversed"),
 ("4,47935E-05","0.0000447935",False,"pass","IRR"),
 ("0.61","0.60",False,"FAIL value","glitchfox: wrong value right scale"),
 ("0.61","0.60",True,"FAIL value","glitchfox: wrong value right scale, scale on"),
 ("1E+30","1.0",False,"FAIL value","glitchfox: 1E+30 vs 1.0"),
 ("1E+30","1.0",True,"FAIL value","glitchfox: 1E+30 vs 1.0, scale on"),
 ("NaN","NaN",False,"FAIL nonfinite","glitchfox: NaN"),
 ("Infinity","Infinity",False,"FAIL nonfinite","glitchfox 650682f2: Inf"),
 ("-Infinity","1.0",False,"FAIL nonfinite","Inf vs finite"),
 ("6.0E-1","0.6",False,"pass","glitchfox 650682f2: exponent style, value"),
 ("6.0E-1","0.6",True,"FAIL scale","glitchfox 650682f2: 6.0E-1 is 0.60 by declaration"),
 ("6E-1","0.6",True,"pass","exponent style, same exponent"),
 ("4,47935E-05","4,47935E-05",True,"pass","IRR as printed, scale on"),
 ("-0","0",False,"pass","glitchfox: -0 vs 0 (recorded as pass)"),
 ("0.6000","0.60",False,"pass","gpb: trailing zeros"),
 ("0.6000","0.60",True,"FAIL scale","gpb: trailing zeros, scale on"),
 ("abc","0.6",False,"FAIL invalid","garbage"),
]
if __name__ == "__main__":
    bad = 0
    for c,p,s,exp,src in F:
        got = compare(c,p,s); ok = got == exp; bad += not ok
        print(f"{'OK ' if ok else 'XX '} {c!r:>14} vs {p!r:<14} scale={s!s:<5} -> {got:<12} expected {exp:<12} [{src}]")
    print("mismatches:", bad)
