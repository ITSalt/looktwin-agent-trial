"""Счёт t1 по criterion.md v2 (решает код, а не текст отчёта).
Вход: answers.jsonl (один ответ = одна строка; значения по задаче: correct | wrong | refuse | seen | empty),
      control_v3.md (прогноз (b) % correct двух моделей).
Выход: таблица по задачам, решённость (n >= 10), 95% Клоппер—Пирсон, промахи моделей, итог «лучше / закрыть / не решено» по условию (а).
Условие (б) (причины) считается отдельно разметкой по matcher_instructions.md и сюда подаётся флагами REASONS_* ниже (по умолчанию — не решено).
Usage: python3 -I score.py"""
import json, math, re, pathlib
H = pathlib.Path(__file__).parent
N_MIN, ALPHA = 10, 0.05
TASKS = ["R1", "R2", "R3", "E1", "E2", "E3"]
def binom_cdf(k, n, p):
    if k < 0: return 0.0
    return sum(math.comb(n, i) * p**i * (1-p)**(n-i) for i in range(0, min(k, n)+1))
def cp(k, n, a=ALPHA):
    def solve(f, lo=0.0, hi=1.0):
        for _ in range(100):
            mid = (lo+hi)/2
            if f(mid): hi = mid
            else: lo = mid
        return (lo+hi)/2
    lower = 0.0 if k == 0 else solve(lambda p: 1-binom_cdf(k-1, n, p) >= a/2)
    upper = 1.0 if k == n else solve(lambda p: binom_cdf(k, n, p) <= a/2)
    return lower, upper
def forecasts():
    t = (H/"control_v3.md").read_text(); out = {}
    for sec in t.split("\n## ")[1:]:
        model = sec.split(" ")[0]; f = {}
        for line in sec.splitlines():
            m = re.match(r"\|\s*([RE][123])\s*\|\s*[\d.]+\s*\|\s*([\d.]+)%?\s*\|", line)
            if m: f[m.group(1)] = float(m.group(2))/100
        out[model] = f
    return out
rows = [json.loads(l) for l in (H/"answers.jsonl").read_text().splitlines() if l.strip()]
fc = forecasts()
res = {}
for t in TASKS:
    vals = [r["tasks"][t] for r in rows if t in r.get("tasks", {})]
    n = sum(v in ("correct", "wrong", "refuse") for v in vals)          # 'seen' и 'empty' не входят
    k = sum(v == "correct" for v in vals)
    lo, hi = cp(k, n) if n else (0.0, 1.0)
    decided = n >= N_MIN
    miss = {m: (decided and not (lo <= f.get(t, -1) <= hi)) for m, f in fc.items()}
    res[t] = dict(n=n, k=k, share=(k/n if n else None), ci=(round(lo, 3), round(hi, 3)), decided=decided,
                  forecast={m: f.get(t) for m, f in fc.items()}, model_miss=miss,
                  seen=sum(v == "seen" for v in vals), refuse=sum(v == "refuse" for v in vals))
decided = [t for t in TASKS if res[t]["decided"]]
agents = sorted({r["author"] for r in rows if any(v in ("correct", "wrong", "refuse") for v in r["tasks"].values())})
better_a = len(decided) >= 2 and all(sum(res[t]["model_miss"][m] for t in decided) >= 2 for m in fc)
stop_a = len(decided) >= 2 and all(not res[t]["model_miss"][m] for t in decided for m in fc)
REASONS_BETTER = None; REASONS_MATCH = None   # заполняются по разметке причин (n >= 10 по API); None = не решено
verdict = ("лучше голой модели" if (better_a or REASONS_BETTER) and len(decided) >= 2 else
           "закрыть (модели угадали)" if stop_a and REASONS_MATCH else
           "закрыть (меньше 5 агентов)" if len(agents) < 5 else "не решено")
print(json.dumps({"tasks": res, "decided": decided, "agents": agents, "n_agents": len(agents),
                  "better_by_share": better_a, "stop_by_share": stop_a, "verdict": verdict}, ensure_ascii=False, indent=1))
