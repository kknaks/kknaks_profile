"""고침 1 — 답의 「없어요 · 없습니다 · 정보가 없 · 자료가 없 · 가져온」 꼴 문장 전 → 후 · 실물 3 대화 앞 2 줄 · 지어낸 상세(숫자 대조).

갈래: 「명동점 사실」(문장에 명동점 · 진료항목 · 목록 — 병원에 그 진료항목이 없다는 사실) · 「모름 · 앱 사정」(그 밖 — 이번 결정으로 0 이어야 함).
지어낸 상세: 답의 숫자 꼴(예 2-4주 · 6-12개월 · 1.5mm)이 그 대화의 턴 메시지(자료 · 명동점 블록) 어디에도 없으면 표시.
실행: python3 fix1_grep.py <본 장부> <앞 실물 장부(고침 전)> <이번 실물 장부(고침 후)> → 표준 출력 markdown
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAT = re.compile(r"없어요|없습니다|정보가 없|자료가 없|가져온")
FACT = re.compile(r"명동점|진료항목|목록")
NUM = re.compile(r"\d+(?:[.,]\d+)?(?:\s*[-~]\s*\d+(?:[.,]\d+)?)?\s*(?:mm|cc|주|개월|일|회|시간|분|년|%|샷|유닛|U)")


def rows(p):
    return [json.loads(x) for x in Path(p).read_text().splitlines() if x.strip()]


def ends(p, since="2026-11-18"):
    return [r for r in rows(p) if r.get("phase") == "end" and (r.get("asked_at") or "")[:10] >= since and r.get("answer")]


def sentences(t):
    return [s.strip() for s in re.split(r"(?<=[.?!요다])\s+|\n", t or "") if s.strip()]


def hits(answers):
    c = Counter()
    ex = []
    for tag, a in answers:
        for s in sentences(a):
            if PAT.search(s):
                k = "명동점 사실" if FACT.search(s) else "모름 · 앱 사정"
                c[k] += 1
                if k == "모름 · 앱 사정":
                    ex.append((tag, s[:120]))
    return c, ex


def table(head, rs):
    return "\n".join(["| " + " | ".join(head) + " |", "|" + "---|" * len(head)] + ["| " + " | ".join(str(x) for x in r) + " |" for r in rs])


def conv_tag(names, cid):
    return next((k for k, v in names.items() if v["conv_id"] == cid), cid[:4])


def main(main_p, prev_p, new_p):
    prev_names = json.loads((HERE / "out/live_on.json").read_text())
    new_names = json.loads((HERE / "out/live_fix1.json").read_text())
    m = ends(main_p)
    pv = ends(prev_p)
    nw = ends(new_p)
    sets = [("본 장부(11-18 ~ · 지금 시대 답 전부)", [(f"{r['conv_id'][:4]} T{r['turn']}", r["answer"]) for r in m]),
            ("앞 실물 3 대화(구현 판 · 고침 전)", [(f"{conv_tag(prev_names, r['conv_id'])} T{r['turn']}", r["answer"]) for r in pv]),
            ("이번 실물 3 대화(고침 후)", [(f"{conv_tag(new_names, r['conv_id'])} T{r['turn']}", r["answer"]) for r in nw])]
    out = []
    exs = {}
    for name, ans in sets:
        c, ex = hits(ans)
        exs[name] = ex
        out.append([name, len(ans), c["모름 · 앱 사정"], c["명동점 사실"]])
    print("### grep 「없어요 · 없습니다 · 정보가 없 · 자료가 없 · 가져온」 — 문장 수(전 → 후)\n")
    print(table(["모음", "답 수", "모름 · 앱 사정(0 이어야)", "명동점 사실(그 진료항목이 병원에 없음)"], out))
    for name, ex in exs.items():
        if ex:
            print(f"\n{name} — 「모름 · 앱 사정」 문장:\n")
            print(table(["턴", "문장"], [[t, s.replace("|", "¦")] for t, s in ex]))
    # 턴별 전 → 후 · 앞 2 줄 · 숫자 대조
    by_prev = {(conv_tag(prev_names, r["conv_id"]), r["turn"]): r for r in pv}
    by_new = {(conv_tag(new_names, r["conv_id"]), r["turn"]): r for r in nw}
    msgs: dict[str, str] = {}
    for r in sorted(nw, key=lambda r: r["turn"]):
        msgs[r["conv_id"]] = msgs.get(r["conv_id"], "") + (r.get("llm_user_message") or "")
    print("\n### 실물 3 대화 — 턴별(앞 = 고침 전 · 뒤 = 고침 후)\n")
    rs = []
    for nm in ("03b8", "ecc6", "73bd"):
        for t in new_names[nm]["turns"]:
            n = t["turn"]
            a, b = by_prev.get((nm, n)), by_new.get((nm, n))
            ca = hits([("", (a or {}).get("answer", ""))])[0]["모름 · 앱 사정"]
            cb = hits([("", (b or {}).get("answer", ""))])[0]["모름 · 앱 사정"]
            j = json.loads(((b or {}).get("llm_user_message") or "\n{}").split("\n")[1] or "{}")
            emp = ",".join(f"{x.get('about')}:{x.get('what')}" for x in j.get("empty") or []) or "-"
            first2 = " / ".join([x.strip() for x in ((b or {}).get("answer") or "").split("\n") if x.strip()][:2]).replace("|", "¦")[:170]
            ctx = msgs.get((b or {}).get("conv_id"), "")
            nums = sorted({x.group(0).replace(" ", "") for x in NUM.finditer((b or {}).get("answer") or "")})
            norm = lambda z: z.replace(" ", "").replace("~", "-").replace("\u2013", "-")  # 「2~4주」 ↔ 자료 「2-4주」
            bad = [x for x in nums if norm(x) not in norm(ctx)]
            rs.append([f"{nm} T{n}", t["q"][:16], ca, cb, emp, len(nums), ",".join(bad) or "0", first2])
    print(table(["턴", "말", "모름 문장 전", "후", "앱 판정 empty", "답 숫자", "자료에 없는 숫자", "답 앞 2 줄(후)"], rs))


if __name__ == "__main__":
    main(*sys.argv[1:4])
