"""명동점 블록 줄 머리(kos.labels)별 바이트 · 진료항목 줄 안 칸별 바이트(지금 장부 · 0.5 턴). 실행: python3 kos_split.py"""
import json, sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import common
k = json.loads((common.W / "out/decompose.json").read_text())["k_tok_per_byte"]
lab, fld, n = Counter(), Counter(), 0
for r in common.answer_rows():
    sec = common.split_sections(r["llm_user_message"]).get("kos")
    if not sec:
        continue
    n += 1
    for ln in sec.split("\n")[1:]:
        if not ln.strip():
            continue
        head, _, js = ln.partition(" ")
        lab[head] += common.b(ln) + 1
        if head.startswith("진료항목") or head.startswith("진료"):
            try:
                o = json.loads(js)
            except ValueError:
                continue
            for it in (o if isinstance(o, list) else [o]):
                if isinstance(it, dict):
                    for kk, v in it.items():
                        fld[kk] += common.b(json.dumps(v, ensure_ascii=False)) + len(kk) + 4
tot = sum(lab.values())
print(f"턴 {n} · 블록 합 {round(tot * k):,} 토큰")
print("| 줄 머리 | 토큰 | 몫 |\n|---|---|---|")
for h, v in lab.most_common(12):
    print(f"| {h[:20]} | {round(v * k):,} | {100 * v / tot:.1f}% |")
ft = sum(fld.values())
print("\n| 진료항목 줄 칸 | 토큰 | 진료항목 줄 안 몫 |\n|---|---|---|")
for h, v in fld.most_common(12):
    print(f"| {h} | {round(v * k):,} | {100 * v / ft:.1f}% |")
