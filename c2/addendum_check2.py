# Run from the repo root (c2 mounted read-only at /w, no network):
#   docker run --rm --network none --read-only --cap-drop ALL --tmpfs /tmp -v "$PWD/c2:/w:ro" python:3.12-slim python3 -I /w/addendum_check2.py
# Any image with Python 3.12+ works.
import importlib.util, datetime
def L(d,t,f):
    s=importlib.util.spec_from_file_location("m",f"/w/{d}/{t}.py");m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return getattr(m,f)
N=datetime.datetime(2026,10,22,12,0,0,tzinfo=datetime.timezone.utc)
C=[('T5','safe_join',("/","a")),('T2','parse_retry_after',("Wed, 21 Oct 2026 07:28:00 -0000",datetime.datetime(2026,10,21,7,0,0,tzinfo=datetime.timezone.utc))),('T2','parse_retry_after',("--5",N)),('T3','mask_secrets',('{"token": "abc',)),
   ('T3','mask_secrets',('{"token":"abc"}',)),('T3','mask_secrets',('token : x',)),('T3','mask_secrets',('token = abc123',)),('T3','mask_secrets',('mytoken=abc',))]
for d in ('ref','gen'):
    out=[]
    for t,f,a in C:
        try: out.append(repr(L(d,t,f)(*a)))
        except Exception as e: out.append(type(e).__name__)
    print(d,out)
