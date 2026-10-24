#!/bin/bash
# 3 прогона × 6 задач, gemini-3.8-flash, стоп при $0.10
cd "$(dirname "$0")"; total=0; maxrun=0.02  # потолок цены одного прогона (наблюдённый максимум 21.10 — $0.018)
for run in 1 2 3; do for t in R1 R2 R3 E1 E2 E3; do
  python3 -c "import sys; sys.exit(0 if $total+$maxrun<=0.10 else 1)" || { echo "CAP: остаток меньше цены прогона, не начинаю $t/$run"; exit 0; }
  out=$(timeout 300 python3 -I mass_agent.py google/gemini-3.8-flash $t $run 2>&1 | tail -1); echo "$out"
  c=$(echo "$out" | python3 -c 'import json,sys
try: print(json.loads(sys.stdin.read())["cost"])
except Exception: print(0)')
  total=$(python3 -c "print($total+$c)"); echo "TOTAL $total"
  python3 -c "import sys; sys.exit(0 if $total<0.10 else 1)" || { echo "CAP REACHED"; exit 0; }
done; done; echo DONE
