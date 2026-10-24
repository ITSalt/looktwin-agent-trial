def dedupe_events(events):
    best = {}
    for i, e in enumerate(events):
        k = e['id']
        if k not in best or e['ts'] > best[k][1]['ts']: best[k] = (best.get(k,(i,))[0], e)
    return [e for _, e in sorted(best.values(), key=lambda p: (p[1]['ts'], p[0]))]
