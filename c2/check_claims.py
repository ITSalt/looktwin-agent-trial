import importlib.util, datetime, json
def L(t,f):
    s=importlib.util.spec_from_file_location("m",f"/w/gen/{t}.py");m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return getattr(m,f)
U=datetime.timezone.utc; N=datetime.datetime(2015,10,21,7,27,0,tzinfo=U)
C=[("T1#1","split_amount",('"-0.00"',1)),("T2#1","parse_retry_after",("Wed, 21 Oct 2015 07:28:00",N)),("T2#2","parse_retry_after",("Wed, 21 Oct 2015 07:28:00 -0500",N)),("T2#3","parse_retry_after",("1"+"0"*400,N)),("T3#1","mask_secrets",("password=",)),("T3#2a","mask_secrets",("failed auth (token=abc)",)),("T3#2b","mask_secrets",("token=abc.",)),("T5#1","safe_join",("//tenant","docs/file.txt"))]
out={}
for cid,fn,a in C:
    f=L(cid[:2],fn); a=tuple(x.strip('"') if isinstance(x,str) and x.startswith('"') else x for x in a)
    try: out[cid]=repr(f(*a))
    except Exception as e: out[cid]=f"raised {type(e).__name__}: {e}"[:150]
print(json.dumps(out,indent=1,ensure_ascii=False))
