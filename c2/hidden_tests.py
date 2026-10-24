# Hidden tests + defect ids. Fixed BEFORE code generation (22.10 ~21:55 MSK).
import datetime, json, sys, importlib.util
def load(path, func):
    spec = importlib.util.spec_from_file_location("m", path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return getattr(m, func)
def raises(f, *a):
    try: f(*a); return False
    except ValueError: return True
    except Exception: return False
UTC = datetime.timezone.utc
NOW = datetime.datetime(2026,10,22,12,0,0,tzinfo=UTC)
TESTS = {
 "T1": [
  ("D1.1 float rounding: sum exact for 0.10/3", lambda f: sum(int(x.replace('.','')) for x in f("0.10",3)) == 10 and f("0.10",3)==["0.04","0.03","0.03"]),
  ("D1.2 large amount precision", lambda f: f("10000000000000000.01",2)==["5000000000000000.01","5000000000000000.00"]),
  ("D1.3 n<1 raises", lambda f: raises(f,"1.00",0)),
  ("D1.4 negative raises", lambda f: raises(f,"-1.00",2)),
  ("D1.5 zero total ok", lambda f: f("0.00",2)==["0.00","0.00"]),
 ],
 "T2": [
  ("D2.1 delta seconds", lambda f: f("120",NOW)==120.0),
  ("D2.2 past date -> 0", lambda f: f("Wed, 21 Oct 2026 07:28:00 GMT",NOW)==0.0),
  ("D2.3 future date", lambda f: f("Thu, 22 Oct 2026 12:01:00 GMT",NOW)==60.0),
  ("D2.4 negative delta -> 0", lambda f: f("-5",NOW)==0.0),
  ("D2.5 garbage -> 0", lambda f: f("soon",NOW)==0.0 and f("",NOW)==0.0),
 ],
 "T3": [
  ("D3.1 key=value", lambda f: f("user=bob password=hunter2 ok=1")=="user=bob password=*** ok=1"),
  ("D3.2 case-insensitive", lambda f: "abc123" not in f("Token: abc123")),
  ("D3.3 JSON value", lambda f: "s3cr3t" not in f('{"api_key": "s3cr3t", "n": 1}') and '"n": 1' in f('{"api_key": "s3cr3t", "n": 1}')),
  ("D3.4 no over-masking of similar keys", lambda f: f("tokens_used=42")=="tokens_used=42"),
  ("D3.5 JSON value with escaped quote", lambda f: "xy" not in f('{"secret": "ab\\"xy", "k": 2}')),
 ],
 "T4": [
  ("D4.1 latest ts kept", lambda f: [e['payload'] for e in f([{'id':'a','ts':1,'payload':1},{'id':'a','ts':5,'payload':2}])]==[2]),
  ("D4.2 equal ts keeps first", lambda f: [e['payload'] for e in f([{'id':'a','ts':3,'payload':'x'},{'id':'a','ts':3,'payload':'y'}])]==['x']),
  ("D4.3 input not mutated", lambda f: (lambda ev: (f(ev), ev==[{'id':'b','ts':2,'payload':0},{'id':'b','ts':1,'payload':1}])[1])([{'id':'b','ts':2,'payload':0},{'id':'b','ts':1,'payload':1}])),
  ("D4.4 stable order for equal ts", lambda f: [e['id'] for e in f([{'id':'z','ts':1,'payload':0},{'id':'y','ts':1,'payload':0}])]==['z','y']),
 ],
 "T5": [
  ("D5.1 dotdot escape", lambda f: raises(f,"/srv/files","../etc/passwd")),
  ("D5.2 absolute user path", lambda f: raises(f,"/srv/files","/etc/passwd")),
  ("D5.3 prefix sibling", lambda f: raises(f,"/srv/files","../files2/x")),
  ("D5.4 normal path ok", lambda f: f("/srv/files","a/b.txt")=="/srv/files/a/b.txt"),
  ("D5.5 inner dotdot ok", lambda f: f("/srv/files","a/../b.txt")=="/srv/files/b.txt"),
 ],
}
if __name__ == "__main__":
    tid, path, func = sys.argv[1:4]
    out = {}
    try: f = load(path, func)
    except Exception as e:
        print(json.dumps({t[0]: f"LOAD_ERROR {e}" for t in TESTS[tid]})); sys.exit()
    for name, t in TESTS[tid]:
        try: out[name] = "pass" if t(f) else "FAIL"
        except Exception as e: out[name] = f"FAIL {type(e).__name__}: {e}"[:200]
    print(json.dumps(out))
