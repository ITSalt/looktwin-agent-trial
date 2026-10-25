# Run from the repo root (c2 mounted read-only at /w, no network):
#   docker run --rm --network none --read-only --cap-drop ALL --tmpfs /tmp -v "$PWD/c2:/w:ro" python:3.12-slim python3 -I /w/addendum_check.py
# Any image with Python 3.12+ works.
import importlib.util, datetime
def L(d,t,f):
    s=importlib.util.spec_from_file_location("m",f"/w/{d}/{t}.py");m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return getattr(m,f)
N=datetime.datetime(2026,10,22,12,0,0,tzinfo=datetime.timezone.utc)
for d in ('ref','gen'):
    out=[]
    for args,t,f in ((("1"+"0"*309,N),'T2','parse_retry_after'),(("1"+"0"*308,N),'T2','parse_retry_after'),(("TOKEN=-;",),'T3','mask_secrets'),(("failed auth (token=abc)",),'T3','mask_secrets'),(([{'id':'d','ts':0,'payload':1},{'id':'b','ts':2,'payload':2},{'id':'d','ts':2,'payload':3}],),'T4','dedupe_events')):
        try: r=L(d,t,f)(*args); r=[e['id'] for e in r] if t=='T4' else r
        except Exception as e: r=type(e).__name__
        out.append(repr(r))
    print(d,out)
