"""SPEC-006 v2.3 근거 셈 E — 「자료에 없다」 case3 68 중 새 꼴로도 안 닿은 34 행을 걸음 규칙이 선택지에 올리는가(결정론 · Jev · LLM 없음).

읽기만: 허브 코드(b031371c 와 같은 입력 · 같은 코드로 메모리 빌드 — 발행 · 18005 손대지 않음) · runs.jsonl(rerun-v4) ·
spec005-v33-measure.json(reach_case3.detail 34 행) · spec006-v22-count.json(order · order_v23).
쓰기: 이 파일 옆 spec006-v23-cover.json · .md(두 번 같음).

실행(backend venv):
  cd /Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend
  DATABASE_URL=sqlite+aiosqlite:///:memory: .venv/bin/python <이 파일>

「선택지에 뜸」 정의(걸음 1 · S = rerun-v4 시작 노드 · 목표 = 그 행 골드 fact):
  0홉  — 목표 fact 가 S 의 section fact(_node_fact_ids(S)) → 걸음 1 섹션 선택지에 그 section 이 뜸
  1홉  — 목표 fact 가 S 의 1홉 이웃 X 의 section fact → X 가 걸음 1 이웃 선택지에 뜨면 「뜸」
         v2.2: X 의 edge kind ∈ 순서 표 위 3 묶음의 edge 이고 peek 앞 4(items) 안
         v2.3: X 의 edge kind ∈ v2.3 edge kind 표 · 그 종류 전부(expand(neighbor_kinds) 목록 · 앞 4 제한 없음)
  2홉+ — 그 밖(대기열로만)
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

from app.modules.gold import tools as T  # noqa: E402
from app.modules.gold.build import build_gold  # noqa: E402
from app.modules.gold.inputs import read_dir  # noqa: E402
from app.modules.gold.memory import GoldGraph  # noqa: E402

V4 = "b202611011148-c6ed3a"
REAL_BUILD = {"id": "edcd64fc-1cc8-4697-8530-2d0c773a0daa", "build_hash": "b031371c4c69cea1", "published_at": "2026-11-01T02:24:44.436010+00:00"}
OUT = W / "spec006-v23-cover"

b = build_gold(read_dir(W))
assert b.build_hash == REAL_BUILD["build_hash"], b.build_hash
g = GoldGraph.from_content(b.content, build=dict(REAL_BUILD))
T.warm_sections(g)

m = json.loads((W / "spec005-v33-measure.json").read_text(encoding="utf-8"))
cnt = json.loads((W / "spec006-v22-count.json").read_text(encoding="utf-8"))
rows34 = [x for x in m["d_walk"]["reach_case3"]["detail"] if x["tag"] == "새 꼴로도 안 닿음"]
assert len(rows34) == 34, len(rows34)
walks = {}
with (E / "runs" / "runs.jsonl").open(encoding="utf-8") as f:
    for line in f:
        r = json.loads(line)
        if r.get("batch_id") == V4:
            walks[r["question_no"]] = r["cases"]["case3"]["trace"]["walk"]

HOLDERS: dict[str, list[str]] = collections.defaultdict(list)  # fact → 그 fact 를 section fact 로 가진 노드(expand(sections) 로 받을 수 있는 자리)
for _n in sorted(g.nodes):
    for _f in T._node_fact_ids(g, _n):
        HOLDERS[_f].append(_n)


def node_hops(src: str, dst: set[str], cap: int = 4) -> int | None:
    seen, fr = {src}, [src]
    for d_ in range(cap + 1):
        if seen & dst:
            return d_
        nxt = []
        for x in fr:
            for lst in T._neighbor_edges(g, x, False).values():
                for _e, y, _d in lst:
                    if y in g.nodes and y not in seen:
                        seen.add(y)
                        nxt.append(y)
        fr = nxt
    return None


V22 = cnt["order"]
V23 = cnt["order_v23"]


def v22_edges(intent: str) -> set[str]:
    t = V22["table"].get(intent) or V22["table"]["_all"]
    return {e for grp in t["order"] for e in V22["group_edges"][grp]}


def v23_edges(intent: str) -> list[str]:
    return (V23["table"].get(intent) or V23["table"]["_all"])["kinds"]


def classify(row: dict) -> dict:
    w = walks[row["no"]]
    s, intent = w["start_node"], w["intent"]
    fids = set(row["fact_ids"])  # detail 은 앞 6 id 만 — 그 안에서 셈(보수적)
    out = {"no": row["no"], "i": row["i"], "start": s, "intent": intent, "why_005": row["why"]}
    if fids & T._node_fact_ids(g, s):
        secs = sorted({g.facts[x]["section"] for x in fids & T._node_fact_ids(g, s)})
        out.update(place="0홉 · S 섹션", sections=secs, v22=True, v23=True, first_section_max_2=intent in V23["first_section_max_2"])
        return out
    pk = T.peek(g, s)["neighbors_by_kind"]
    hits = []  # (edge kind, 이웃 id, 앞 4 안)
    for kind, lst in T._neighbor_edges(g, s, False).items():
        shown = {it["id"] for it in (pk.get(kind) or {}).get("items") or []}
        for _e, other, _d in lst:
            if other in g.nodes and fids & T._node_fact_ids(g, other):
                hits.append((kind, other, other in shown, len(lst)))
    if not hits:
        hold = {n for x in fids for n in HOLDERS.get(x, [])}
        if not hold:
            owners = sorted({g.facts[x]["owner_id"].split(":")[0] for x in fids})
            out.update(place="어느 노드 섹션에도 없음", owners=owners, v22=False, v23=False)
        else:
            out.update(place="2홉+ · 대기열로만", hops=node_hops(s, hold), v22=False, v23=False)
        return out
    e22, e23 = v22_edges(intent), set(v23_edges(intent))
    v22 = any(k in e22 and sh for k, _, sh, _ in hits)
    v23 = any(k in e23 for k, *_ in hits)
    if any(k in e22 and sh for k, _, sh, _ in hits):
        place = "1홉 · 순서 표 · 앞 4 안"
    elif any(k in e22 for k, *_ in hits):
        place = "1홉 · 순서 표 · 앞 4 밖"
    else:
        place = "1홉 · 순서 표 밖 종류"
    out.update(place=place, kinds=sorted({k for k, *_ in hits}), kind_n=max(n for *_, n in hits), v22=v22, v23=v23)
    return out


res = [classify(x) for x in rows34]
by = collections.Counter(x["place"] for x in res)
summary = {
    "rows": len(res), "by_place": dict(sorted(by.items())),
    "v22_shown": sum(x["v22"] for x in res), "v23_shown": sum(x["v23"] for x in res),
    "v22_shown_1hop": sum(x["v22"] for x in res if x["place"].startswith("1홉")),
    "v23_shown_1hop": sum(x["v23"] for x in res if x["place"].startswith("1홉")),
    "zero_hop": by.get("0홉 · S 섹션", 0),
    "zero_hop_in_section2_intents": sum(1 for x in res if x["place"].startswith("0홉") and x.get("first_section_max_2")),
    "two_hop_plus": by.get("2홉+ · 대기열로만", 0),
    "no_holder": by.get("어느 노드 섹션에도 없음", 0),
    "no_holder_owner_kinds": dict(collections.Counter(o for x in res if x["place"] == "어느 노드 섹션에도 없음" for o in x["owners"])),
    "v23_missed_1hop_kinds": dict(collections.Counter(k for x in res if x["place"].startswith("1홉") and not x["v23"] for k in x["kinds"])),
    "note": "34 행은 461 행(순서 표 근거)의 부분집합과 겹친다 — 표본 안 셈 · 상한 참고 · 끝 조건은 「선택지에 뜸」 수까지만",
}
d = {"build": REAL_BUILD["build_hash"], "summary": summary, "rows": res}
OUT.with_suffix(".json").write_text(json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
L = ["# SPEC-006 v2.3 근거 셈 E — 안 닿은 34 행 × 걸음 1 선택지(spec006-v23-cover.py · 결정론)", "",
     "```json", json.dumps(summary, ensure_ascii=False, indent=1), "```", "",
     "| 문항 | 의도 | 자리 | 종류 | v2.2 뜸 | v2.3 뜸 |", "|---|---|---|---|---|---|"]
for x in res:
    L.append(f"| {x['no']} | {x['intent']} | {x['place']} | {' · '.join(x.get('kinds') or x.get('sections') or x.get('owners') or ([f"{x['hops']}홉"] if x.get('hops') is not None else []))} | {x['v22']} | {x['v23']} |")
OUT.with_suffix(".md").write_text("\n".join(L) + "\n", encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False, indent=1))
