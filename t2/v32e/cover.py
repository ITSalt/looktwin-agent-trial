import json, subprocess, itertools, sys
sys.path.insert(0, '.'); import ports as P
cands = P.cands
js = json.loads(subprocess.run(['node', 'ports_js.js'], input=json.dumps(cands), capture_output=True, text=True, check=True).stdout)
fa = dict(P.fa); fa.update({k: set(v) for k, v in js.items()})
leaky = {p: v for p, v in fa.items() if v}
print(json.dumps({p: len(v) for p, v in fa.items()}, ensure_ascii=False))
for k in range(1, 6):
    covers = [cb for cb in itertools.combinations(cands, k) if all(set(cb) & v for v in leaky.values())]
    if covers:
        print('MIN', k, 'covers', len(covers)); [print([repr(x) for x in cb]) for cb in covers[:5]]; break
nl = [s for s in cands if '\n' in s]
print('covers that contain a newline row:', sum(1 for cb in covers if set(cb) & set(nl)), 'of', len(covers))
