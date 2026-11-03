"""SPEC-006 v2.4 근거 셈 — 「받는 자리」 정의 하나로 순서 표(461 행)와 34 행 덮는 셈을 다시(결정론 · Jev · LLM 없음).

받는 자리(v2.4 · 재검수 F-1 · F-2): fact f 를 걸음이 받는 곳 = (노드 n, section s, 쪽 p) 중 f 가 `g.section_ids[(n, s)]`(= expand(n, sections=[s])
가 실제로 줄로 내는 목록 · 노드 자신의 줄 · 계열 · 제품의 펼친 단위 fact 는 들어가지 않음)의 i 번째이면 p = i // 12 + 1(1쪽 12줄 ·
SPEC-005 `GOLD_EXPAND_SECTION_MAX`). 걸음은 1쪽만 받는다(SPEC-006 §3-4-2).

행 자리(우선순위 순 — 걸음이 받을 수 있는 쪽을 먼저):
  0홉·1쪽 · 1홉·1쪽(edge kind 들) · 0홉·2쪽+ · 1홉·2쪽+ · 2홉+(어딘가 줄에 있음) · 받을 곳 없음(어느 노드 줄에도 없음) · 이름·속성만(fact hit 없음)

읽기만: 허브 코드(b031371c 와 같은 입력 · 메모리 빌드) · runs.jsonl(rerun-v4) · fail-triage2.json · rerun-v4-vs-v3.json ·
gold-export.json(b031371c) · spec005-v33-measure.json(34 행 목록) · spec006-v22-count.json(v2.2 · v2.3 표 — 비교용).
쓰기: 이 파일 옆 spec006-v24-recount.json · .md(두 번 같음).

실행(backend venv):
  cd /Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend
  DATABASE_URL=sqlite+aiosqlite:///:memory: .venv/bin/python <이 파일>
"""
from __future__ import annotations

import collections
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
BACKEND = Path("/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend")
W = Path(__file__).resolve().parent
E = W.parents[2] / "reference" / "2026-10-30-hub-evals"
sys.path.insert(0, str(BACKEND))
sys.path.insert(0, str(E / "build-out" / "fail-triage2-scripts"))

from app.modules.gold import tools as T  # noqa: E402
from app.modules.gold.build import build_gold  # noqa: E402
from app.modules.gold.inputs import read_dir  # noqa: E402
from app.modules.gold.memory import GoldGraph  # noqa: E402
from triage2 import Gold, norm  # noqa: E402 — spec006-v22-count.py 와 같은 판정 식

V4 = "b202611011148-c6ed3a"
REAL_BUILD = {"id": "edcd64fc-1cc8-4697-8530-2d0c773a0daa", "build_hash": "b031371c4c69cea1", "published_at": "2026-11-01T02:24:44.436010+00:00"}
PAGE = 12
COVER, KIND_MIN, ORDER_MIN_N = 0.9, 3, 10
UNIT_LINK = {"family": "key_family", "product": "product_unit"}  # S 가 계열 · 제품이면 단위 이웃 종류(F-1 규칙)
OUT = W / "spec006-v24-recount"
PLACES = ("0홉·1쪽", "1홉·1쪽", "0홉·2쪽+", "1홉·2쪽+", "2홉+", "받을 곳 없음", "이름·속성만")

b = build_gold(read_dir(W))
assert b.build_hash == REAL_BUILD["build_hash"], b.build_hash
g = GoldGraph.from_content(b.content, build=dict(REAL_BUILD))
T.warm_sections(g)
gold = Gold(BACKEND / "build-out" / "gold-export.json")
assert gold.hash == REAL_BUILD["build_hash"], gold.hash

SEAT: dict[str, list[tuple[str, str, int]]] = collections.defaultdict(list)  # fact → [(노드, section, 쪽)]
for (n_, s_), ids in sorted(g.section_ids.items()):
    for i, f in enumerate(ids):
        SEAT[f].append((n_, s_, i // PAGE + 1))
NB: dict[str, dict[str, list[str]]] = {}


def nbrs(s: str) -> dict[str, list[str]]:
    if s not in NB:
        NB[s] = {k: sorted({o for _e, o, _d in lst if o in g.nodes}) for k, lst in T._neighbor_edges(g, s, False).items()}
    return NB[s]


def place(s: str, fids: set[str]) -> dict:
    if not fids:
        return {"place": "이름·속성만"}
    seats = [x for f in sorted(fids) for x in SEAT.get(f, [])]
    if not seats:
        return {"place": "받을 곳 없음", "owners": sorted({gold.facts[f]["owner_id"].split(":")[0] for f in fids if f in gold.facts})}
    own = [x for x in seats if x[0] == s]
    nb = nbrs(s)
    k1 = collections.defaultdict(set)  # 쪽 → edge kind
    for k, xs in nb.items():
        xs_ = set(xs)
        for n_, _s, p in seats:
            if n_ in xs_:
                k1[1 if p == 1 else 2].add(k)
    if any(p == 1 for *_, p in own):
        return {"place": "0홉·1쪽", "sections": sorted({sx for _n, sx, p in own if p == 1})}
    if k1[1]:
        return {"place": "1홉·1쪽", "kinds": sorted(k1[1])}
    if own:
        return {"place": "0홉·2쪽+", "sections": sorted({sx for _n, sx, _p in own})}
    if k1[2]:
        return {"place": "1홉·2쪽+", "kinds": sorted(k1[2])}
    return {"place": "2홉+"}


def fact_hits(quote: str) -> tuple[set[str], bool]:
    q = norm(quote)
    if len(q) < 2:
        return set(), False
    _tier, hits = gold.gold_match(q)
    return {h[2]["fact_id"] for h in hits if h[1] == "fact"}, bool(hits)


# ── 461 행(spec006-v22-count.py 와 같은 행) ─────────────────────────────────
runs = {}
with (E / "runs" / "runs.jsonl").open(encoding="utf-8") as f:
    for line in f:
        r = json.loads(line)
        if r.get("batch_id") == V4:
            runs[r["question_no"]] = r
tri = json.loads((E / "build-out" / "fail-triage2.json").read_text(encoding="utf-8"))
src = []
for q, r in runs.items():
    for case in ("case2", "case3"):
        for f in r["cases"][case].get("judge", {}).get("failures") or []:
            if f.get("status") == "valid" and (f.get("evidence") or {}).get("quote"):
                src.append(("v4", q, case, f["evidence"]["quote"]))
for row in tri["rows"]:
    if (row.get("evidence") or {}).get("quote"):
        src.append(("v3", row["question_no"], row["case"], row["evidence"]["quote"]))
rows = []
for sname, q, case, quote in src:
    w = runs.get(q, {}).get("cases", {}).get("case3", {}).get("trace", {}).get("walk") or {}
    s, intent = w.get("start_node"), w.get("intent")
    fids, anyhit = fact_hits(quote)
    if not anyhit or not s:
        continue
    rows.append({"src": sname, "q": q, "case": case, "start": s, "skind": g.nodes[s]["kind"] if s in g.nodes else None, "intent": intent, **place(s, fids)})
assert len(rows) == 461, len(rows)

dist_all = collections.Counter(x["place"] for x in rows)
cnt = json.loads((W / "spec006-v22-count.json").read_text(encoding="utf-8"))


def pick(rs: list[dict], c: collections.Counter, allc: collections.Counter) -> tuple[list[str], int]:
    out, cov = [], set()
    for e in sorted(c, key=lambda e: (-c[e], -allc[e], e)):
        if len(out) >= KIND_MIN and len(cov) >= COVER * len(rs):
            break
        out.append(e)
        cov |= {i for i, x in enumerate(rs) if e in x["kinds"]}
    return out, len(cov)


one = [x for x in rows if x["place"] == "1홉·1쪽"]
allc = collections.Counter(k for x in one for k in x["kinds"])
o_all, cov_all = pick(one, allc, allc)
by = collections.defaultdict(list)
for x in one:
    by[x["intent"] or "-"].append(x)
table = {"_all": {"n1": len(one), "kinds": o_all, "covered": cov_all, "counts": dict(sorted(allc.items(), key=lambda t: (-t[1], t[0])))}}
for it, rs in sorted(by.items()):
    if len(rs) >= ORDER_MIN_N:
        c = collections.Counter(k for x in rs for k in x["kinds"])
        ks, cv = pick(rs, c, allc)
        table[it] = {"n1": len(rs), "source": "intent", "kinds": ks, "covered": cv, "counts": dict(sorted(c.items(), key=lambda t: (-t[1], t[0])))}
    else:
        table[it] = {"n1": len(rs), "source": "_all", "kinds": o_all, "covered": sum(1 for x in rs if set(x["kinds"]) & set(o_all))}
by_int_place = collections.defaultdict(collections.Counter)
for x in rows:
    by_int_place[x["intent"] or "-"][x["place"]] += 1
sec2 = sorted(it for it, c in by_int_place.items() if it != "-" and c and max(c, key=lambda p: (c[p], p)) == "0홉·1쪽")
# 단위 이웃 규칙이 461 의 1홉·1쪽 행에 더하는 덮음
unit_add = sum(1 for x in one if x["skind"] in UNIT_LINK and UNIT_LINK[x["skind"]] in x["kinds"]
               and not set(x["kinds"]) & set((table.get(x["intent"]) or table["_all"])["kinds"]))
order_v24 = {"rule": f"받는 자리 = 노드 자신의 section 줄 1쪽 · 1홉·1쪽 행(S 줄 1쪽에 없고 edge kind k 이웃 X 의 줄 1쪽에 있음)의 edge kind 셈 · "
                     f"n ≥ {ORDER_MIN_N} 이면 그 의도 · 아니면 전체 · 내림차순(동점 = 전체 셈 → 이름) · 의도 1홉·1쪽 행 {COVER:.0%} 덮을 때까지(최소 {KIND_MIN}) · "
                     f"S 가 계열 · 제품이면 단위 이웃 종류 {UNIT_LINK} 를 늘 더함",
             "table": table, "first_section_max_2": sec2, "unit_link": UNIT_LINK, "unit_link_adds_461": unit_add,
             "place_461": {p: dist_all.get(p, 0) for p in PLACES},
             "place_by_intent": {it: {p: c.get(p, 0) for p in PLACES} for it, c in sorted(by_int_place.items())}}

# ── 34 행(005 reach_case3 · 새 꼴로도 안 닿음) — hit 전부(앞 6 자르지 않음 · W-7) ───────────
m = json.loads((W / "spec005-v33-measure.json").read_text(encoding="utf-8"))
rem = json.loads((E / "build-out" / "rerun-v4-vs-v3.json").read_text(encoding="utf-8"))["remaining_failures"]
det = [x for x in m["d_walk"]["reach_case3"]["detail"] if x["tag"] == "새 꼴로도 안 닿음"]
assert len(det) == 34
V22 = cnt["order"]
V23 = cnt["order_v23"]
c34 = []
for x in det:
    quote = (rem[x["i"]].get("evidence") or {}).get("quote") or ""
    fids, _ = fact_hits(quote)
    assert sorted(fids)[:6] == x["fact_ids"] or set(x["fact_ids"]) <= fids, x["no"]
    w = runs[x["no"]]["cases"]["case3"]["trace"]["walk"]
    s, intent = w["start_node"], w["intent"]
    pl = place(s, fids)
    pk = T.peek(g, s)["neighbors_by_kind"]
    e22 = {e for grp in (V22["table"].get(intent) or V22["table"]["_all"])["order"] for e in V22["group_edges"][grp]}
    e23 = set((V23["table"].get(intent) or V23["table"]["_all"])["kinds"])
    e24 = set((table.get(intent) or table["_all"])["kinds"])
    sk = g.nodes[s]["kind"]
    e24u = e24 | ({UNIT_LINK[sk]} if sk in UNIT_LINK else set())
    shown = {"v22": False, "v23": False, "v24_no_unit": False, "v24": False}
    if pl["place"] == "0홉·1쪽":
        shown = dict.fromkeys(shown, True)
    elif pl["place"] == "1홉·1쪽":
        ks = set(pl["kinds"])
        p1 = {n_ for f in fids for n_, _s, p in SEAT.get(f, []) if p == 1}  # 목표를 1쪽에 가진 노드
        front4 = {k for k in ks if p1 & {it["id"] for it in (pk.get(k) or {}).get("items") or []}}
        shown = {"v22": bool(front4 & e22), "v23": bool(ks & e23), "v24_no_unit": bool(ks & e24), "v24": bool(ks & e24u)}
    c34.append({"no": x["no"], "i": x["i"], "intent": intent, "start": s, "skind": sk, "n_fact_hits": len(fids), **pl, **shown})
s34 = collections.Counter(x["place"] for x in c34)
summary34 = {"rows": len(c34), "place": {p: s34.get(p, 0) for p in PLACES},
             "shown": {k: sum(x[k] for x in c34) for k in ("v22", "v23", "v24_no_unit", "v24")},
             "shown_1hop": {k: sum(x[k] for x in c34 if x["place"] == "1홉·1쪽") for k in ("v22", "v23", "v24_no_unit", "v24")},
             "zero_hop_p1": s34.get("0홉·1쪽", 0),
             "zero_hop_p1_in_section2_intents": sum(1 for x in c34 if x["place"] == "0홉·1쪽" and x["intent"] in sec2),
             "missed_1hop_p1": [{"no": x["no"], "intent": x["intent"], "kinds": x["kinds"]} for x in c34 if x["place"] == "1홉·1쪽" and not x["v24"]],
             "note": "34 행 문항은 461 행(표 근거)과 겹친다 — 표본 안 · 상한 참고"}
d = {"build": REAL_BUILD["build_hash"], "order_v24": order_v24, "cover34": {"summary": summary34, "rows": c34},
     "rows461": [{k: x[k] for k in ("src", "q", "case", "intent", "start", "place") } | ({"kinds": x["kinds"]} if "kinds" in x else {}) for x in rows]}
OUT.with_suffix(".json").write_text(json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
L = ["# SPEC-006 v2.4 근거 셈 — 받는 자리 정의 하나로(spec006-v24-recount.py · 결정론)", "", f"빌드 `{REAL_BUILD['build_hash']}`", "",
     "## 461 행 자리", "", " · ".join(f"{p} {dist_all.get(p, 0)}" for p in PLACES), "", "| 의도 | " + " | ".join(PLACES) + " |", "|---" * (len(PLACES) + 1) + "|"]
for it, c in sorted(by_int_place.items()):
    L.append(f"| {it} | " + " | ".join(str(c.get(p, 0)) for p in PLACES) + " |")
L += ["", "## 순서 표 v2.4", "", order_v24["rule"], "", f"걸음 1 섹션 2 의도(0홉·1쪽 1위): {sec2} · 단위 이웃 규칙이 461 의 1홉·1쪽에 더하는 덮음 {unit_add}", "",
      "| 의도 | 1홉·1쪽 행 | 근거 | edge kind(순서) | 덮음 | 셈 |", "|---|---|---|---|---|---|"]
for it, x in table.items():
    L.append(f"| {it} | {x['n1']} | {x.get('source', '-')} | {' → '.join(x['kinds'])} | {x['covered']} | {x.get('counts', '')} |")
L += ["", "## 34 행", "", "```json", json.dumps(summary34, ensure_ascii=False, indent=1), "```", "",
      "| 문항 | 의도 | S 종류 | hit | 자리 | 종류 · 섹션 | v2.2 | v2.3 | v2.4(단위 규칙 없이) | v2.4 |", "|---|---|---|---|---|---|---|---|---|---|"]
for x in c34:
    L.append(f"| {x['no']} | {x['intent']} | {x['skind']} | {x['n_fact_hits']} | {x['place']} | {' · '.join(x.get('kinds') or x.get('sections') or x.get('owners') or [])} | "
             f"{x['v22']} | {x['v23']} | {x['v24_no_unit']} | {x['v24']} |")
OUT.with_suffix(".md").write_text("\n".join(L) + "\n", encoding="utf-8")
print(json.dumps({"place_461": order_v24["place_461"], "sec2": sec2, "unit_add": unit_add, "all_kinds": o_all, **summary34}, ensure_ascii=False, indent=1))
