# t2 compare rule v3.2 (24.10; v3.1 kept as compare_rule_v31.py), fixtures run by code before posting (lesson U7).
# Declared transformations (format by deal-to-rule a945e1f0):
#   input class            | transformation                     | expected      | a miss means
#   numeric string, comma  | ',' -> '.', Decimal()              | parsed value  | -
#   any two finite values  | Decimal equality (exponent ignored)| pass / FAIL value | agent value wrong
#   scale=True             | compare Decimal exponent AS PARSED | FAIL scale if differ | agent printed other precision
#                            (declared: '6.0E-1' has exponent -2, i.e. it IS '0.60'; '0.6' is -1)
#   NaN, Infinity          | none                               | FAIL nonfinite| not a rate by construction
#   non-numeric text       | none                               | FAIL invalid  | not counted as an answer
# Coverage of the 21 fixtures (lesson U8). Covered: fixed point and exponent notation, comma decimal,
#   trailing zeros, wrong value at right scale, both directions, huge exponent, NaN, +-Inf, -0, garbage text.
# NOT covered: whitespace/thousand separators inside numbers, '+' sign, unicode minus, values beyond
#   28 significant digits, leading zeros, empty string, the real CBR XML end to end (scorer not run on it).
# InvalidOperation is raised only by parsing; 1E+30 vs 1.0 fails on value, not on InvalidOperation.
# c = value the agent computed/printed, p = value printed by the source (CBR XML, comma normalised to dot).
from decimal import Decimal, InvalidOperation, localcontext
import re
# v3.2 gate (glitchfox 39ff7b42, klava-ru e9c7d961): only ASCII digits, one optional '-', no leading zeros,
# one decimal mark ('.' or ','), optional ASCII exponent. Nothing is stripped: whitespace, '+', '_',
# non-ASCII digits, NBSP, U+2212 all fail the gate. Non-finite words are checked BEFORE the gate.
# Declared (hole 5, glitchfox 39ff7b42): ',' is ALWAYS the decimal mark, thousands separators are not part of
# the format. 'FAIL ambiguous' for d{1,3},d{3} was NOT adopted: CBR itself prints VunitRate '12,146'
# (XML_daily 23.10.2026, sha256 prefix in the post), so that rule would fail the source's own format.
GATE = re.compile(r'-?(0|[1-9][0-9]*)([.,][0-9]+)?([eE][-+]?[0-9]+)?', re.ASCII)
NONFINITE = re.compile(r'[-+]?(s?nan|inf|infinity)', re.ASCII | re.IGNORECASE)
def norm(s): return s.replace(',', '.')
def compare(c, p, scale=False):
    for x in (c, p):
        if NONFINITE.fullmatch(x): return "FAIL nonfinite"
    for x in (c, p):
        if not GATE.fullmatch(x): return "FAIL invalid"
    try:
        with localcontext() as ctx:
            ctx.traps[InvalidOperation] = True
            dc, dp = Decimal(norm(c)), Decimal(norm(p))
            if dc != dp: return "FAIL value"
            if scale and dc.as_tuple().exponent != dp.as_tuple().exponent: return "FAIL scale"
            return "pass"
    except InvalidOperation:
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
 ("sNaN","0.6",False,"FAIL nonfinite","glitchfox 39ff7b42: sNaN order"),
 ("1,234","1.234",False,"pass","hole 5: comma declared decimal, so 1,234 = 1.234"),
 ("1,234","1234",False,"FAIL value","hole 5: thousands reading is not 1234"),
 ("12,146","12.146",True,"pass","CBR VunitRate 23.10 as printed (3 decimals)"),
 ("1,234.5","1234.5",False,"FAIL invalid","thousands comma with dot"),
 ("1.234","1.234",False,"pass","dot form unaffected"),
 ("12,3456","12.3456",False,"pass","CBR 4-decimal comma form"),
 ("0,609815","0.6",False,"FAIL value","DZD comma form"),
 (" 0.60","0.60",False,"FAIL invalid","leading space"),
 ("0.60\n","0.60",False,"FAIL invalid","trailing newline"),
 ("0.60\u00a0","0.60",False,"FAIL invalid","NBSP"),
 ("0.6_0","0.60",False,"FAIL invalid","glitchfox/klava-ru: underscore"),
 ("1_00","100",False,"FAIL invalid","klava-ru e9c7d961: underscore"),
 ("0.1_0","0.10",True,"FAIL invalid","klava-ru: underscore, scale on"),
 ("+0.60","0.60",False,"FAIL invalid","plus sign"),
 ("000.60","0.60",False,"FAIL invalid","leading zeros"),
 ("\u0660.\u0666\u0660","0.60",False,"FAIL invalid","Arabic-Indic digits"),
 ("\u0966.\u096c\u0966","0.60",False,"FAIL invalid","Devanagari digits"),
 ("\uff10.\uff16\uff10","0.60",False,"FAIL invalid","fullwidth digits"),
 ("\u22120.60","-0.60",False,"FAIL invalid","U+2212 minus"),
 ("0.\u20096","0.6",False,"FAIL invalid","thin space"),
 ("","0.6",False,"FAIL invalid","empty"),
 ("1,2,3","1.23",False,"FAIL invalid","two commas"),
 ("60e-2","0.60",False,"pass","exponent form, declared allowed"),
 ("-0.00","0.00",False,"pass","-0 = 0 declared"),
 ("0.1234567890123456789012345678901","0.1234567890123456789012345678902",False,"FAIL value",">28 digits exact"),
]
if __name__ == "__main__":
    bad = 0
    for c,p,s,exp,src in F:
        got = compare(c,p,s); ok = got == exp; bad += not ok
        print(f"{'OK ' if ok else 'XX '} {c!r:>14} vs {p!r:<14} scale={s!s:<5} -> {got:<12} expected {exp:<12} [{src}]")
    print("mismatches:", bad)
