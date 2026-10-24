# LookTwin agent trial: open data and scripts

Measurements from public "agent trials" on the agent board getpostingboard.dev, October 2026. AI agents on the board answered tasks against public APIs (Bank of Russia CBR, Frankfurter/ECB), and code scored their answers. Also here: noise checks of our own criteria, a compare rule that board agents broke and fixed several times, and a small "review vs execution" run.

**Most files are in Russian.** Code, fixtures and this README are in English.

## Folders
| Folder / file | What is in it |
|---|---|
| `t1/` | Trial 1: tasks (`tasks.md`), criterion written before the window (`criterion.md`; v1 kept as SUPERSEDED), agents' answers (`answers.jsonl`, `answers-log.md`), scorer `score.py` and its outputs, receipts (`receipts.md`), model forecasts (`control_*`), the mass-agent control (`mass/`), blind-check labels (`blind-check/`) |
| `t2/` | Round 2 rules: `compare_rule.py` (v3.2, fixtures inside), `compare_rule_v31.py` (v3.1), `criterion-closure.md` (when t2 may claim "models guessed") |
| `c2/` | Small run: Claude writes code, Codex reviews it, against hidden tests fixed before code generation |
| `c3/` | Pre-registered criterion for "review + receipt per claim", **not run yet** |
| `noise_check_t2_c3.py` | How often our thresholds fire by chance |

## Reading order
1. `t1/tasks.md`, then `t1/criterion.md`
2. `t1/result.md` (verdict: "not solved", n too small)
3. `noise_check_t2_c3.py` and `t2/criterion-closure.md` (why, and what n is needed)
4. `t2/compare_rule.py` and `t1/receipts.md` Q-005..Q-019 (how agents broke the rule)
5. `c2/result.md`, then `c3/criterion.md`

## Glossary
- **Receipt Q-NNN** (квитанция): a record of an agent's verified contribution: what, where, how we reproduced it.
- **«по зову»**: the agent answered after being called by name.
- **«рука» (arm)**: one condition of a comparison (A = review alone, B = review + run receipt).
- **«рой» (swarm)**: the board's agents taken together.
- **looktwin-feedback**: our account on the board. **«мы» / «я»**: the LookTwin team.
- **seq numbers** like #99435 are the board's own post numbers.

## What reproduces without a key
- No key, standard library only: `python3 t1/score.py` (must equal `t1/score-output-2026-10-22-rev1.json`), `python3 t2/compare_rule.py`, `python3 t2/compare_rule_v31.py` (0 mismatches), `python3 noise_check_t2_c3.py`, `python3 c3/power_mcnemar.py`.
- `c2/hidden_tests.py T<n> <file> <func>` runs the hidden tests on `c2/gen/` (model-generated code: run it in a sandbox).
- `c2/check_claims.py` expects the code at `/w/gen/` inside a container (`docker run --network none -v $PWD/c2:/w:ro …`).
- Needs a key: `c2/run_c2.py`, `t1/mass_agent.py` (they read `OPENROUTER_API_KEY` from the environment).

## Fixed files and hashes
- `t1/answers.json` is byte-identical to the file whose sha256 (c7ac0748…) was posted on the board. It keeps an internal note ("product review p.6") on purpose, so the hash still checks.
- `t2/compare_rule.py` (sha256 8a4f7090f6aa…, posted with v3.2) and `t2/compare_rule_v31.py` (7bb77fec3618…, the v3.1 file as it stood when post #99481 went out; its hash was recorded in `t1/receipts.md`, not in the post) are byte-identical to those versions. For that reason they keep our internal comments ("lesson U7/U8") and our internal post numbers in fixture labels: #852 = board #99435, #853 = #99446, #856 = #99481.
- Commit hashes refer to our working repository and cannot be checked from outside; file sha256 values can.

## Rights
Code: MIT (`LICENSE`). Our texts and data: CC BY 4.0 (`LICENSE-DATA`). Agents' quoted texts remain their authors'; scanner output (isitagentready.com) and CBR/ECB data belong to their sources. Receipts and nicknames are taken from public posts on the board.
