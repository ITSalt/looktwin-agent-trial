def dedupe_events(events: list[dict]) -> list[dict]:
    # For each id, remember (input_index, event) of the best event:
    # the latest ts, and on equal ts the one that appeared first.
    best: dict[str, tuple[int, dict]] = {}
    for idx, event in enumerate(events):
        eid = event['id']
        current = best.get(eid)
        if current is None or event['ts'] > current[1]['ts']:
            best[eid] = (idx, event)

    # Sort by ts ascending; ties are broken by the position of the kept
    # event in the input (i.e. a stable order by first appearance).
    kept = sorted(best.values(), key=lambda pair: (pair[1]['ts'], pair[0]))

    # Return shallow copies so the input dicts are never shared or mutated.
    return [dict(event) for _, event in kept]
