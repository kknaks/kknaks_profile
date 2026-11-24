"""JC3 확인 — r4 JSON 의 layers 를 self · inherit · sub 로 바꿔 셈(2차 6판): 토큰이 달라지는 턴 수. 호출 0."""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "token-cause")); sys.path.insert(0, str(HERE))
import common, measure as M, run4  # noqa: E402
M.RULES = 6
md = common.md_sets()
k = json.loads((HERE.parent / "token-cause/out/decompose.json").read_text())["k_tok_per_byte"]
sets = {"sample": M.load_turns(md), "outside": run4.outside_turns(md)}
diff = 0; n = 0
from collections import Counter
miss = Counter(); tok = Counter(); picked = Counter()
for name, ts in sets.items():
    res = [json.loads(x) for x in (HERE / f"out/understand_r4_{name}.jsonl").read_text().splitlines()]
    for t, u in zip(ts, res):
        j = dict(u["json"] or {}); vals = set()
        for lay in ("self", "inherit", "sub"):
            jj = {**j, "fetch": {**(j.get("fetch") or {}), "layers": lay}}
            sc = M.select(t, jj, k)
            vals.add(sc["new_tok"]); miss[lay] += sc["miss"]; tok[lay] += sc["new_tok"]
        picked[(j.get("fetch") or {}).get("layers")] += 1
        n += 1
        if len(vals) > 1:
            diff += 1; print(name, t["conv"][:4], t["turn"], sorted(vals))
print("turns", n, "layers changes tokens", diff, "picked", dict(picked), "miss", dict(miss), "tok", dict(tok))
