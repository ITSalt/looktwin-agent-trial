import os
import json, urllib.request, pathlib, hashlib, re, time, sys
key = os.environ["OPENROUTER_API_KEY"]
D = pathlib.Path(__file__).parent
cost = 0.0
def call(model, prompt):
    global cost
    body = {"model": model, "messages": [{"role":"user","content":prompt}], "usage":{"include":True}}
    r = json.load(urllib.request.urlopen(urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=json.dumps(body).encode(), headers={"Authorization":"Bearer "+key,"Content-Type":"application/json"}, method="POST"), timeout=300))
    c = r.get("usage",{}).get("cost",0) or 0; cost += c
    return r["choices"][0]["message"]["content"], r.get("model"), c
tasks = json.loads((D/"tasks.json").read_text())
(D/"gen").mkdir(exist_ok=True); (D/"review").mkdir(exist_ok=True)
log = []
for t in tasks:
    code, m1, c1 = call("anthropic/claude-sonnet-5.5", t["spec"] + "\n\nReturn only the Python code in one ```python block. Standard library only.")
    mm = re.search(r"```python\n(.*?)```", code, re.S); src = mm.group(1) if mm else code
    (D/"gen"/f"{t['id']}.py").write_text(src)
    rv, m2, c2 = call("openai/gpt-5.3-codex", f"You are reviewing a pull request. Task given to the author:\n\n{t['spec']}\n\nCode:\n```python\n{src}```\n\nReview it for correctness and security. List each concrete defect you find as a numbered item with the input that breaks it. If you find none, say NO DEFECTS. Do not rewrite the code.")
    (D/"review"/f"{t['id']}.md").write_text(rv)
    log.append({"task":t["id"],"gen_model":m1,"gen_cost":c1,"rev_model":m2,"rev_cost":c2,"code_sha":hashlib.sha256(src.encode()).hexdigest(),"review_sha":hashlib.sha256(rv.encode()).hexdigest(),"utc":time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime())})
    print(t["id"], m1, m2, round(c1+c2,4), flush=True)
    if cost > 0.6: print("cost cap"); break
(D/"run_log.json").write_text(json.dumps({"runs":log,"total_cost":cost},indent=1))
print("total", cost)
