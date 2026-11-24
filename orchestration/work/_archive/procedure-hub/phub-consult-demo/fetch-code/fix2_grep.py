"""고침 2 — 답의 내부 note · 목록 속사정 · 고침 1 꼴 문장 전 → 후 · 실물 답 앞 2 줄 · 숫자 대조(지어냄).

실행: python3 fix2_grep.py <이름=장부> ... --new <이번 장부> → markdown
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
NOTE = re.compile(r"확인 필요:|구성\s*1|KOS|기기 칸")
LIST = re.compile(r"조건 때문|좁혀|목록을 보고|목록이 비어|조건까지")
FIX1 = re.compile(r"없어요|없습니다|정보가 없|자료가 없|가져온")
FACT = re.compile(r"명동점|진료항목")
NUM = re.compile(r"\d+(?:[.,]\d+)?(?:\s*[-~]\s*\d+(?:[.,]\d+)?)?\s*(?:mm|cc|주|개월|일|회|시간|분|년|%|샷|유닛|U|원)")


def ends(p, since="2026-11-18"):
    out = []
    for x in Path(p).read_text().splitlines():
        if x.strip():
            r = json.loads(x)
            if r.get("phase") == "end" and (r.get("asked_at") or "")[:10] >= since and r.get("answer"):
                out.append(r)
    return out


def sents(t):
    return [s.strip() for s in re.split(r"(?<=[.?!요다])\s+|\n", t or "") if s.strip()]


def count(rows):
    c, ex = Counter(), []
    for r in rows:
        for s in sents(r["answer"]):
            k = None
            if NOTE.search(s):
                k = "내부 note"
            elif LIST.search(s):
                k = "목록 속사정"
            elif FIX1.search(s):
                k = "명동점 사실" if FACT.search(s) else "모름 · 앱 사정(고침 1)"
            if k:
                c[k] += 1
                if k != "명동점 사실":
                    ex.append((f"{r['conv_id'][:4]} T{r['turn']}", k, s[:130]))
    return c, ex


def table(h, rs):
    return "\n".join(["| " + " | ".join(h) + " |", "|" + "---|" * len(h)] + ["| " + " | ".join(str(x) for x in r) + " |" for r in rs])


def main():
    args = sys.argv[1:]
    i = args.index("--new")
    sets = [a.split("=", 1) for a in args[:i]] + [("이번 실물(고침 2)", args[i + 1])]
    rows, exs = [], []
    for name, p in sets:
        rs = ends(p)
        c, ex = count(rs)
        rows.append([name, len(rs), c["내부 note"], c["목록 속사정"], c["모름 · 앱 사정(고침 1)"], c["명동점 사실"]])
        exs += [(name, *e) for e in ex]
    print("### grep 전 → 후 — 문장 수\n")
    print(table(["모음", "답 수", "내부 note(확인 필요: · 구성1 · KOS · 기기 칸)", "목록 속사정(조건 때문 · 좁혀 · 목록을 보고 · 목록이 비어)",
                 "모름 · 앱 사정(고침 1 꼴)", "명동점 사실(말해도 됨)"], rows))
    if exs:
        print("\n걸린 문장(명동점 사실 빼고):\n")
        print(table(["모음", "턴", "갈래", "문장"], [[a, b, c, d.replace("|", "¦")] for a, b, c, d in exs]))
    names = json.loads((HERE / "out/live_fix2.json").read_text())
    new = {r["conv_id"]: [] for r in []}
    by = {}
    ctx = {}
    for r in sorted(ends(args[i + 1]), key=lambda r: r["turn"]):
        by[(r["conv_id"], r["turn"])] = r
        ctx[r["conv_id"]] = ctx.get(r["conv_id"], "") + (r.get("llm_user_message") or "")
    print("\n### 이번 실물 — 답 앞 2 줄 · 숫자 대조\n")
    out = []
    norm = lambda z: z.replace(" ", "").replace("~", "-").replace(",", "")
    for nm, v in names.items():
        for t in v["turns"]:
            r = by.get((v["conv_id"], t["turn"])) or {}
            nums = sorted({m.group(0) for m in NUM.finditer(r.get("answer") or "")})
            bad = [x for x in nums if norm(x) not in norm(ctx.get(v["conv_id"], ""))]
            first2 = " / ".join([x.strip() for x in (r.get("answer") or "").split("\n") if x.strip()][:2]).replace("|", "¦")[:200]
            c, _ = count([r]) if r else (Counter(), [])
            out.append([f"{nm} T{t['turn']}", t["q"][:20], c["내부 note"] + c["목록 속사정"] + c["모름 · 앱 사정(고침 1)"],
                        len(nums), ",".join(bad) or "0", first2])
    print(table(["턴", "말", "걸린 문장", "답 숫자", "자료 · 블록에 없는 숫자", "답 앞 2 줄"], out))


if __name__ == "__main__":
    main()
