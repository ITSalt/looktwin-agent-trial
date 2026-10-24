# t1: контроль (а) v3 — ПОСЛЕДНЯЯ версия, в счёт идёт она

Запрос `control_prompt_v3.txt`, sha256 66383dcacdc779ea66957a88733f4a6a1f8320996ba01e3eb72bbc3a827df899

## openai/gpt-6.1-sol — 2026-10-21 06:29:16 UTC, $0.010190565, sha256 ответа 064aabe769aba3432e60e3dd169607bb521c3e0595c4aea63c2a3f31c7b29388

| Task | (a) Distinct agents replying | (b) Correct | (c) Refuse / cannot call | (d) Top three wrong-answer or failure reasons, ranked |
|---|---:|---:|---:|---|
| R1 | 28 | 35.7% | 50.0% | 1. Forum or operator rules prohibit external calls; 2. Missing HTTP tools or outbound network; 3. Wrong effective date or unsupported guessed rate |
| R2 | 12 | 41.7% | 41.7% | 1. Forum or operator rules prohibit external calls; 2. Missing HTTP tools or outbound network; 3. Failing to divide quoted yen rate by nominal |
| R3 | 10 | 30.0% | 40.0% | 1. Forum or operator rules prohibit external calls; 2. Confusing requested date with response's effective date; 3. Missing HTTP tools or outbound network |
| E1 | 30 | 46.7% | 40.0% | 1. Forum or operator rules prohibit external calls; 2. Missing HTTP tools or outbound network; 3. Returning inverse rate or wrong date |
| E2 | 14 | 42.9% | 35.7% | 1. Forum or operator rules prohibit external calls; 2. Incorrect cross-rate direction or thousand-yen scaling; 3. Missing HTTP tools or outbound network |
| E3 | 11 | 36.4% | 36.4% | 1. Forum or operator rules prohibit external calls; 2. Counting carried-forward weekend observations as publications; 3. Missing HTTP tools or outbound network |

## anthropic/claude-sonnet-5.5 — 2026-10-21 06:29:32 UTC, $0.02328282, sha256 ответа 8568fca0dbde67d1751da37f96727b4558376934a673be732925a7727e4623ba

| Task | (a) Replies | (b) % correct | (c) % refuse / can't call | (d) Top 3 failure reasons |
|---|---|---|---|---|
| R1 | 18 | 30 | 35 | 1) No outbound network or HTTP tool; 2) Guide forbids acting on third-party contact requests; 3) cbr.ru blocked, 403 or timeout |
| R2 | 8 | 40 | 15 | 1) Ignored Nominal=100, so value off 100×; 2) Decimal comma or windows-1251 parse error; 3) No network, guessed or skipped |
| R3 | 8 | 50 | 15 | 1) Wrong date or rate, or label mismatch; 2) No network, guessed or fabricated; 3) cbr.ru blocked or timeout |
| E1 | 20 | 45 | 30 | 1) No outbound network or HTTP tool; 2) Guide or operator forbids external calls; 3) Future date, so guessed or hallucinated rate |
| E2 | 9 | 40 | 12 | 1) Inverted direction or missed ×1000 scaling; 2) Arithmetic error via cross-rate; 3) No network, guessed |
| E3 | 8 | 35 | 12 | 1) Wrong count (included weekend or miscounted); 2) Average arithmetic or rounding error; 3) Time-series range misused or no network |
