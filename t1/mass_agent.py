import os
"""«Массовый» агент для t1: модель с одним инструментом http_get (только GET, только два домена-API).
Usage: python3 -I mass_agent.py <model> <task_id> <run_no>   -> пишет mass/<model>_<task>_<run>.json
Инструмент исполняется здесь же: urllib, таймаут 20 с, ответ обрезается до 20 000 символов (ровно как увидел бы агент с небольшим окном), кодировка — как отдаёт сервер (cp1251 декодируется честно, по заголовку)."""
import json, sys, time, pathlib, urllib.request, urllib.parse, re, hashlib
ALLOW = {"www.cbr.ru", "cbr.ru", "api.frankfurter.dev", "frankfurter.dev"}
KEY = os.environ["OPENROUTER_API_KEY"]
TASKS = json.load(open(pathlib.Path(__file__).with_name("post_tasks.json")))
def http_get(url):
    u = urllib.parse.urlparse(url)
    if u.scheme != "https" or u.hostname not in ALLOW: return "ERROR: domain not allowed in this test"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "looktwin-agent-trial/0.1"}), timeout=20) as r:
            raw = r.read(); ct = r.headers.get("Content-Type", "")
            m = re.search(r"charset=([\w-]+)", ct); enc = m.group(1) if m else "utf-8"
            try: txt = raw.decode(enc)
            except Exception: txt = raw.decode("utf-8", "replace")
            return f"HTTP {r.status} {ct}\n" + txt[:20000]
    except Exception as e: return f"ERROR: {type(e).__name__}: {e}"[:500]
def chat(model, msgs):
    body = {"model": model, "messages": msgs, "usage": {"include": True},
            "tools": [{"type": "function", "function": {"name": "http_get", "description": "HTTP GET a URL and return status, content type and body text",
                       "parameters": {"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"]}}}]}
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=json.dumps(body).encode(),
                                 headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"}, method="POST")
    return json.load(urllib.request.urlopen(req, timeout=180))
def main(model, tid, run):
    t = TASKS[tid]
    msgs = [{"role": "user", "content": t["post_text"] + "\n\nReply with your final answer in one line starting with ANSWER:, or REFUSE: and your reason."}]
    cost, calls, log = 0.0, 0, []
    for step in range(6):
        r = chat(model, msgs); cost += r.get("usage", {}).get("cost") or 0
        m = r["choices"][0]["message"]; msgs.append({k: v for k, v in m.items() if k in ("role", "content", "tool_calls")})
        tcs = m.get("tool_calls") or []
        if not tcs: break
        for tc in tcs:
            url = json.loads(tc["function"]["arguments"] or "{}").get("url", ""); calls += 1
            out = http_get(url); log.append({"url": url, "head": out[:120]})
            msgs.append({"role": "tool", "tool_call_id": tc["id"], "content": out})
    final = (msgs[-1].get("content") or "") if msgs[-1]["role"] == "assistant" else ""
    rec = {"model": model, "task": tid, "run": run, "ts": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()), "cost": cost, "http_calls": calls, "urls": log, "final": final}
    p = pathlib.Path(__file__).with_name("mass"); p.mkdir(exist_ok=True)
    (p / f"{model.split('/')[1]}_{tid}_{run}.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1))
    print(json.dumps({k: rec[k] for k in ("task", "run", "cost", "http_calls", "final")}, ensure_ascii=False))
if __name__ == "__main__": main(sys.argv[1], sys.argv[2], sys.argv[3])
