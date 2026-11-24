"""out/jev_measure.json · out/jev_raw.jsonl → 리포트 표. 실행: python3 jev_tables.py > out/jev_tables.md"""

from __future__ import annotations

import json
import statistics
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
COLS = ["now", "det", "jev_0.3", "jev_0.5", "jev_0.7", "jev_0.3_forced", "jev_0.5_forced", "jev_0.7_forced",
        "det+jev_0.5_forced"]
NAME = {"now": "지금", "det": "결정론(KD9 끔·명동점 닿는 하위만·반복 제거)", "jev_0.3": "Jev ≥0.3", "jev_0.5": "Jev ≥0.5",
        "jev_0.7": "Jev ≥0.7", "jev_0.3_forced": "Jev ≥0.3 + 명시·안전 강제", "jev_0.5_forced": "Jev ≥0.5 + 강제",
        "jev_0.7_forced": "Jev ≥0.7 + 강제", "det+jev_0.5_forced": "결정론 ∩ Jev ≥0.5 + 강제"}


def table(head, rows):
    return "\n".join(["| " + " | ".join(head) + " |", "|" + "---|" * len(head)] +
                     ["| " + " | ".join(str(c) for c in r) + " |" for r in rows])


def main():
    J = json.loads((HERE / "out/jev_measure.json").read_text())
    raw = [json.loads(x) for x in (HERE / "out/jev_raw.jsonl").read_text().splitlines()]
    turns = [t for t in J if t["score"]["now"]["rows"]]
    tot = {c: sum(t["score"][c]["tok"] for t in turns) for c in COLS}
    cited = sum(t["score"]["now"]["cited"] for t in turns)
    print(f"### 전체(대화 10 · 자료 있는 턴 {len(turns)} · 후보 {sum(t['cands'] for t in J)} · 인용 줄 {cited})\n")
    rows = []
    for c in COLS:
        miss = sum(t["score"][c]["miss"] for t in turns)
        turns_miss = sum(1 for t in turns if t["score"][c]["miss"])
        rows.append([NAME[c], f"{tot[c]:,}", f"{100 * tot[c] / tot['now']:.1f}%", f"{100 - 100 * tot[c] / tot['now']:.1f}%",
                     f"{miss}/{cited} ({100 * miss / cited:.1f}%)" if cited else "-", turns_miss])
    print(table(["방식", "「## 자료」 토큰 합(추정)", "지금 대비", "감소", "빠짐(인용 줄 중 안 실림)", "빠짐 있는 턴"], rows))
    print("\n### 턴별(자료 있는 턴 · 토큰 / 빠짐)\n")
    rows = []
    for t in turns:
        s = t["score"]
        rows.append([t["tag"], (t["question"] or "")[:20], t["cands"], s["now"]["rows"], s["now"]["cited"],
                     f'{s["now"]["tok"]:,}'] + [f'{s[c]["tok"]:,} / {s[c]["miss"]}' for c in COLS[1:]] +
                    [t["req"], t["ms_max"], ",".join(t["models"])])
    print(table(["턴", "질문", "후보", "줄", "인용", "지금"] + [NAME[c] for c in COLS[1:]] + ["요청", "ms(최대)", "model"], rows))
    print("\n### Noul 분포(후보 전체)\n")
    allv = [v for x in raw for v in (x.get("nouls") or {}).values()]
    cited_v, other_v = [], []
    for t in J:
        for c in t["cand_sample"]:
            if c["noul"] >= 0:
                (cited_v if c["cited"] else other_v).append(c["noul"])
    rows = [["전체", len(allv), sum(v < 0.3 for v in allv), sum(0.3 <= v < 0.5 for v in allv), sum(0.5 <= v < 0.7 for v in allv),
             sum(v >= 0.7 for v in allv), round(statistics.median(allv), 3)]]
    for nm, vs in (("인용된 줄을 가진 후보", cited_v), ("인용 없는 후보", other_v)):
        rows.append([nm, len(vs), sum(v < 0.3 for v in vs), sum(0.3 <= v < 0.5 for v in vs), sum(0.5 <= v < 0.7 for v in vs),
                     sum(v >= 0.7 for v in vs), round(statistics.median(vs), 3) if vs else "-"])
    print(table(["", "수", "<0.3", "0.3~0.5", "0.5~0.7", "≥0.7", "중앙"], rows))
    print("\n### 지연 · 요청\n")
    ms = [x["ms"] for x in raw]
    by_tag = defaultdict(list)
    for x in raw:
        by_tag[x["tag"]].append(x["ms"])
    per_turn = [max(v) for v in by_tag.values()]
    models = sorted({x.get("model") for x in raw if x.get("model")})
    sb = [x["state_bytes"] for x in raw]
    usage = [x.get("usage") for x in raw if x.get("usage")]
    print(table(["요청", "오류", "요청 ms 중앙", "요청 ms 최대", "턴 ms(조각 동시 · 최대) 중앙", "턴 ms 최대", "state 바이트 최대", "응답 model", "usage 칸"],
                [[len(raw), sum(1 for x in raw if x["error"]), statistics.median(ms), max(ms), statistics.median(per_turn),
                  max(per_turn), max(sb), ",".join(models), (sorted(usage[0]) if usage else "없음")]]))
    print("\n### 표본 — 인용된 후보의 Noul(낮은 것 위로)\n")
    rows = []
    for t in J:
        for c in t["cand_sample"]:
            if c["cited"]:
                rows.append([t["tag"], (t["question"] or "")[:18], c["name"], c["facet"][:28], c["relation"][:60], c["noul"]])
    rows.sort(key=lambda x: x[-1])
    print(table(["턴", "질문", "후보", "칸", "연결", "Noul"], rows[:25]))


if __name__ == "__main__":
    main()
