"""SPEC-005 v3.3 근거 측정 — expand 를 걷기용 꼴로(fact 한 줄 목록) 바꿀 때의 크기 · 걸음 재생(결정론 · Jev · LLM 없음).

읽기만: 허브 코드(b031371c 와 같은 입력 · 같은 코드로 메모리 빌드 — 발행 · 18005 손대지 않음) · runs.jsonl(rerun-v4 · rerun-v3) ·
recheck2 의 rerun-responses.inprocess.json(676) · rerun-v4-vs-v3.json · gold-export.json(b031371c). 쓰기: 이 파일 옆 spec005-v33-measure.json(시간 칸 e_other.precompute_bytes_seconds 빼면 두 번 같음).

실행(backend venv):
  cd /Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend
  DATABASE_URL=sqlite+aiosqlite:///:memory: .venv/bin/python <이 파일>
"""
from __future__ import annotations

import collections
import json
import os
import re
import statistics as st
import sys
from pathlib import Path
from typing import Any

os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
BACKEND = Path("/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend")
W = Path(__file__).resolve().parent
E = W.parents[2] / "reference" / "2026-10-30-hub-evals"
sys.path.insert(0, str(BACKEND))
sys.path.insert(0, str(E / "fail-triage-scripts"))

from app.modules.gold import tools as T  # noqa: E402
from app.modules.gold.build import build_gold  # noqa: E402
from app.modules.gold.facts import SECTIONS  # noqa: E402
from app.modules.gold.inputs import read_dir  # noqa: E402
from app.modules.gold.memory import GoldGraph  # noqa: E402

V4 = "b202611011148-c6ed3a"
REAL_BUILD = {"id": "edcd64fc-1cc8-4697-8530-2d0c773a0daa", "build_hash": "b031371c4c69cea1", "published_at": "2026-11-01T02:24:44.436010+00:00"}
BUDGET = 20000
MAX_STEPS = 4
NO_DATA = re.compile(r"자료에 없|정보 없음|없다고|찾지 못")  # 「자료에 없다」 류 판정 문장(case3 68 · case2 51)
GAP = "정보 없음(gap)"


def B(x: Any) -> int:
    return len(json.dumps(x, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


def BA(x: Any) -> int:
    """앱(clinic_chat case3 `_hub`)이 예산에 세는 바이트 — json.dumps 기본 구분자(공백 있음) · 허브 REST 본문(B)보다 ≈ 4% 큼."""
    return len(json.dumps(x, ensure_ascii=False).encode("utf-8"))


def stat(xs: list[int]) -> dict[str, Any]:
    if not xs:
        return {"n": 0}
    s = sorted(xs)
    return {"n": len(s), "median": st.median(s), "p95": s[max(0, int(len(s) * 0.95 + 0.5) - 1)], "max": s[-1]}


# ── 그래프 ────────────────────────────────────────────────────────────────
b = build_gold(read_dir(W))
assert b.build_hash == REAL_BUILD["build_hash"], b.build_hash
g = GoldGraph.from_content(b.content, build=dict(REAL_BUILD))
T.warm_sections(g)


def owner_of(f: dict[str, Any]) -> str:
    o = f["owner_id"]
    if o in g.nodes or o in g.edges or o.startswith("scope:"):
        return o
    at = f.get("attached_to") or []
    return at[0] if at else o


def line_of(text: str, n: int) -> tuple[str, bool]:
    t = " ".join(str(text).split())
    return (t, False) if len(t) <= n else (t[: n - 1] + "…", True)


# ── 새 꼴(후보) ───────────────────────────────────────────────────────────
class Form:
    def __init__(self, n: int = 40, k: int = 12, owner_mode: str = "omit_self", contract: str = "rule") -> None:
        self.n, self.k, self.owner_mode, self.contract = n, k, owner_mode, contract

    def row(self, fid: str, req: str, full: bool) -> dict[str, Any]:
        f = g.facts[fid]
        r: dict[str, Any] = {"id": fid}
        if full:
            r["text"] = f["text"]
        else:
            ln, cut = line_of(f["text"], self.n)
            r["line"] = ln
            if cut:
                r["cut"] = True
        r["section"] = f["section"]
        o = owner_of(f)
        if self.owner_mode == "always" or o != req:
            r["owner"] = o
        if f["flags"]:
            r["flags"] = f["flags"]
        if f["state"] == GAP:
            r["gap"] = True
        if full:
            r["source"] = {"file": f["source"].get("file"), "path": f["source"].get("path")}
        return r

    def expand(self, nid: str, sections: list[str] | None = None, neighbors: list[str] | None = None, neighbor_kinds: list[str] | None = None,
               fact_ids: list[str] | None = None, full: bool = False, page: int = 1, intent: str | None = None) -> dict[str, Any]:
        req = {k: v for k, v in {"id": nid, "sections": sections, "neighbors": neighbors, "neighbor_kinds": neighbor_kinds,
                                 "fact_ids": fact_ids, "full": full or None, "page": page if page != 1 else None, "intent": intent}.items() if v}
        rows: list[dict[str, Any]] = []
        more: dict[str, int] = {}
        for s in sections or []:
            ids = g.section_ids.get((nid, s), [])
            lo, hi = (page - 1) * self.k, page * self.k
            rows += [self.row(f, nid, full) for f in ids[lo:hi]]
            if len(ids) > hi:
                more[s] = len(ids) - hi
        for f in fact_ids or []:
            rows.append(self.row(f, nid, True))
        out: dict[str, Any] = {"build": {"build_hash": g.build["build_hash"]}, "request": req, "intent_used": None,
                               "node": T._node_head(g, nid, full=False), "facts": rows}
        if more:
            out["more"] = more
        if neighbors or neighbor_kinds:
            nb = T.expand(g, nid, neighbors=neighbors, neighbor_kinds=neighbor_kinds)
            for k in ("neighbors", "neighbors_truncated", "neighbors_more_ids"):
                if k in nb:
                    out[k] = nb[k]
        flags = sorted({x for r in rows for x in r.get("flags", []) if x in T.MUST_SHOW} | ({"gap"} if any(r.get("gap") for r in rows) else set()))
        if self.contract == "ids":
            out["claude_contract"] = {"allowed_fact_ids": [r["id"] for r in rows if not r.get("cut")], "must_show_flags": flags}
        else:  # rule — 허용 = facts[] 중 cut 없는 줄 · full/fact_ids 원문(규칙 문장은 peek 에 한 번)
            out["claude_contract"] = {"allowed": "facts_uncut", "must_show_flags": flags}
        return out


FORM = Form()  # 정본 후보(아래 grid 로 고름)


def new_peek(nid: str, form: Form) -> dict[str, Any]:
    p = T.peek(g, nid)
    for kind, v in p["neighbors_by_kind"].items():
        for it in v["items"]:
            it["n_facts"] = sum(len(g.section_ids.get((it["id"], s), [])) for s in SECTIONS)
    for s in p["sections"]:
        s["bytes"] = B(form.expand(nid, sections=[s["name"]]))
    return p


def old_expand(nid: str, **kw: Any) -> dict[str, Any]:
    return T.expand(g, nid, **kw)


# ── (a) 전 (노드, section) ───────────────────────────────────────────────
pairs = sorted(g.section_ids)
old_pair = {p: B(old_expand(p[0], sections=[p[1]])) for p in pairs}
grid = {}
for n in (40, 60, 80):
    for k in (8, 12):
        for om in ("omit_self", "always"):
            for ct in ("rule", "ids"):
                f = Form(n, k, om, ct)
                grid[f"N{n}-K{k}-{om}-{ct}"] = stat([B(f.expand(p[0], sections=[p[1]])) for p in pairs])
new_pair = {p: B(FORM.expand(p[0], sections=[p[1]])) for p in pairs}
cut_share = sum(1 for f in g.facts.values() if line_of(f["text"], FORM.n)[1]) / len(g.facts)

# 구성(옛 꼴) — 칸별 바이트 합
comp: collections.Counter = collections.Counter()
for p in pairs:
    r = old_expand(p[0], sections=[p[1]])
    for k2, v in r.items():
        comp[k2] += B(v)
comp_new: collections.Counter = collections.Counter()
for p in pairs:
    r = FORM.expand(p[0], sections=[p[1]])
    for k2, v in r.items():
        comp_new[k2] += B(v)

# ── (b) rerun-v4 걸음 기록 ───────────────────────────────────────────────
runs = [json.loads(x) for x in (E / "runs" / "runs.jsonl").open(encoding="utf-8")]
v4 = [r for r in runs if r.get("batch_id") == V4]
assert len(v4) == 182
calls_old, calls_rec, calls_new, calls_new_app, calls_new_sec, mism = [], [], [], [], [], []
line_tot = [0, 0]  # rerun-v4 걸음 호출 476 의 새 꼴 줄 수 · 그중 cut
peek_old, peek_new = [], []
for r in v4:
    w = r["cases"]["case3"]["trace"].get("walk") or {}
    for s in w.get("steps", []):
        peek_old.append(B(T.peek(g, s["node"])))
        peek_new.append(B(new_peek(s["node"], FORM)))
        for c in (s.get("expand") or {}).get("calls", []):
            kw = {"sections": c.get("sections") or None, "neighbors": c.get("neighbors") or None, "intent": w.get("intent")}
            o = BA(old_expand(s["node"], **kw))
            calls_old.append(o)
            calls_rec.append(c["bytes"])
            calls_new.append(B(FORM.expand(s["node"], **kw)))
            calls_new_app.append(BA(FORM.expand(s["node"], **kw)))
            _rows = FORM.expand(s["node"], **kw)["facts"]
            line_tot[0] += len(_rows)
            line_tot[1] += sum(1 for x in _rows if x.get("cut"))
            if not c.get("neighbors"):
                calls_new_sec.append(B(FORM.expand(s["node"], **kw)))
            if o != c["bytes"]:
                mism.append((r["question_no"], s["node"], c.get("sections"), o, c["bytes"]))

# ── (c) 676(rerun-v3 재실행 호출)이 닿은 (노드, section) ──────────────────
resp = json.loads((E / "build-out" / "recheck2" / "rerun-responses.inprocess.json").read_text(encoding="utf-8"))
touched: set[tuple[str, str]] = set()
for c in resp:
    inp = c["input"] if isinstance(c["input"], dict) else None
    if inp is None:
        try:
            inp = eval(c["input"], {}, {})  # noqa: S307 — recheck2 가 repr 로 저장한 dict
        except Exception:  # noqa: BLE001
            continue
    if not isinstance(inp, dict):
        continue
    nodes = set()
    for v in inp.values():
        for x in (v if isinstance(v, list) else [v]):
            if isinstance(x, str) and x in g.nodes:
                nodes.add(x)
    secs = [x for x in inp.get("sections") or [] if x in SECTIONS]
    for nid in nodes:
        for s in secs or SECTIONS:
            if (nid, s) in g.section_ids:
                touched.add((nid, s))
touched_l = sorted(touched)


# ── (d) 걸음 재생(같은 선택 · 새 꼴 · 결정론) ─────────────────────────────
def gold_hits() -> dict[tuple[str, str], list[dict[str, Any]]]:
    from recheck2 import Gold, norm  # noqa: PLC0415
    gold = Gold(BACKEND / "build-out" / "gold-export.json")
    assert gold.hash == REAL_BUILD["build_hash"], gold.hash
    d = json.loads((E / "build-out" / "rerun-v4-vs-v3.json").read_text(encoding="utf-8"))
    out: dict[tuple[str, str], list[dict[str, Any]]] = collections.defaultdict(list)
    for i, row in enumerate(d["remaining_failures"]):
        if row["item"] != "accuracy" or row["case"] not in ("case3", "case2") or not NO_DATA.search(row["claim"]):
            continue
        q = norm((row.get("evidence") or {}).get("quote") or "")
        tier, hits = gold.gold_match(q) if len(q) >= 2 else (None, [])
        fids = sorted({h[2]["fact_id"] for h in hits if h[1] == "fact"})
        nodes = sorted({n for h in hits for n in gold.owners_of(h[1], h[2])})
        out[(row["no"], row["case"])].append({"i": i, "tier": tier, "fact_ids": fids, "nodes": nodes, "path": (row.get("evidence") or {}).get("path")})
    return out


def picked_items(step: dict[str, Any]) -> tuple[list[str], list[str]]:
    secs, nbs = [], []
    for x in step["jev"].get("picked") or []:
        if x.startswith("section:"):
            secs.append(x[8:])
        else:
            nbs.append(x)
    return secs, nbs


def replay(w: dict[str, Any], form: Form | None) -> dict[str, Any]:
    """form None = 옛 꼴(기록 재현 확인용). 기록된 걸음의 선택(picked 전부 — 옛 판에서 예산으로 빠진 것 포함)을 같은 순서로:
    호출 = section 하나씩(이웃은 첫 호출에 같이 · 앱 0be5ca6 과 같음) · 예산 넘는 호출은 통째로 빼고 그 걸음 끝에서 멈춤(budget).
    기록이 끝났는데 옛 판이 budget 으로 멈췄으면 이어감: 다음 노드 = 펼친 이웃 큐(BFS · 방문 안 한 것) · 고르는 것 = 이 걸음에서 Jev 가 고른 section 이름 ∩ 그 노드 section(peek 순) ·
    이웃은 안 고름. 옛 판 stop 이 enough · steps · empty 면 같은 자리에서 멈춤(Jev 판단 그대로)."""
    steps = w.get("steps") or []
    used, listed, full_ids, visited, queue = 0, [], [], [], []
    cut_by_node: dict[str, list[str]] = collections.defaultdict(list)
    stop, n_steps, cont = None, 0, 0
    expanded: set[tuple[str, str]] = set()
    jev_secs: list[str] = []
    for s in steps:
        jev_secs += [x for x in picked_items(s)[0] if x not in jev_secs]
    plan = [(s["node"], *picked_items(s)) for s in steps]
    i = 0
    while n_steps < MAX_STEPS:
        if i < len(plan):
            node, secs, nbs = plan[i]
        elif w.get("stop") == "budget" and form is not None:
            node = next((q for q in queue if q not in visited), None)
            if node is None:
                stop = "frontier_empty"
                break
            secs = [x["name"] for x in T.peek(g, node)["sections"] if x["name"] in jev_secs]
            nbs = []
            cont += 1
        else:
            stop = w.get("stop")
            break
        i += 1
        n_steps += 1
        visited.append(node)
        calls = [(sx, nbs if j == 0 else []) for j, sx in enumerate(secs)] or ([(None, nbs)] if nbs else [])
        hit = False
        for sx, nb in calls:
            kw = {"sections": [sx] if sx else None, "neighbors": nb or None, "intent": w.get("intent")}
            resp_ = (form.expand(node, **kw) if form else old_expand(node, **kw))
            by = BA(resp_)
            if used + by > BUDGET:  # 앱과 같음 — 처음 넘는 호출은 통째로 빼고 그 걸음에서 멈춤
                hit = True
                break
            used += by
            if sx:
                expanded.add((node, sx))
            for f in resp_.get("facts") or []:
                listed.append(f["id"])
                if form is None or not f.get("cut"):
                    full_ids.append(f["id"])
                elif f["id"] not in cut_by_node[node]:
                    cut_by_node[node].append(f["id"])
            if form is None:
                for sec in (resp_.get("sections") or {}).values():
                    listed += [x for x in sec.get("facts", []) if isinstance(x, str)] + list(sec.get("more_ids") or [])
            for x in nb:
                if x not in queue:
                    queue.append(x)
        if hit:
            stop = "budget"
            break
    else:
        stop = "steps"
    fetch = sum(BA(form.expand(n_, fact_ids=ids[:64], intent=w.get("intent"))) for n_, ids in cut_by_node.items()) if form else 0
    return {"steps": n_steps, "bytes": used, "cut_fetch_bytes": fetch, "cut_n": sum(len(v) for v in cut_by_node.values()), "stop": stop, "listed": sorted(set(listed)), "full": sorted(set(full_ids)),
            "neighbor_reached": len(visited) >= 2, "continued": cont, "visited": visited, "expanded": sorted(expanded)}


def all_sections_walk(visited: list[str], intent: str | None) -> set[str]:
    """정책 B(상한 참고) — 새 재생과 같은 방문 노드 순서 · 노드마다 section 전부(peek 순 · 1쪽) · 같은 예산 · 같은 멈춤 규칙."""
    used, listed = 0, set()
    for node in visited[:MAX_STEPS]:
        for sx in [x["name"] for x in T.peek(g, node)["sections"]]:
            r_ = FORM.expand(node, sections=[sx], intent=intent)
            by = BA(r_)
            if used + by > BUDGET:
                return listed
            used += by
            listed |= {f["id"] for f in r_["facts"]}
    return listed


ADJ: dict[str, set[str]] = collections.defaultdict(set)
for e in g.edges.values():
    for a_ in [e["from_id"]] + ((e["to_id"] or "")[11:].split("|") if (e["to_id"] or "").startswith("candidates:") else [e["to_id"]]):
        pass
    a, z = e["from_id"], e["to_id"]
    zs = (z or "")[11:].split("|") if (z or "").startswith("candidates:") else [z]
    for z_ in zs:
        if a in g.nodes and z_ in g.nodes:
            ADJ[a].add(z_)
            ADJ[z_].add(a)


def hops(src: list[str], dst: set[str], cap: int = 6) -> int | None:
    if not dst:
        return None
    seen, fr = set(src), list(src)
    for d in range(cap + 1):
        if seen & dst:
            return d
        nxt = []
        for x in fr:
            for y in ADJ.get(x, ()):
                if y not in seen:
                    seen.add(y)
                    nxt.append(y)
        fr = nxt
    return None


def fact_nodes(fids: set[str]) -> set[str]:
    out = set()
    for f in fids:
        x = g.facts[f]
        for o in [x["owner_id"]] + list(x.get("attached_to") or []):
            if o in g.nodes:
                out.add(o)
            elif o in g.edges:
                out |= {g.edges[o]["from_id"], g.edges[o]["to_id"]} & set(g.nodes)
    return out


hits = gold_hits()
walk_rows = []
for r in v4:
    w = r["cases"]["case3"]["trace"].get("walk") or {}
    if not w.get("steps") or w.get("fallback"):
        continue
    old = replay(w, None)
    new = replay(w, FORM)
    walk_rows.append({"no": r["question_no"], "rec_stop": w.get("stop"), "rec_steps": w.get("steps_n"), "rec_bytes": w.get("bytes_total"),
                      "rec_fact_ids": w.get("fact_ids") or [], "old": old, "new": new})

by_no = {x["no"]: x for x in walk_rows}
v4_by_no = {r["question_no"]: r for r in v4}


def reach_table(case: str) -> dict[str, Any]:
    rows = [(k, v) for k, v in hits.items() if k[1] == case]
    n_rows = sum(len(v) for _, v in rows)
    res = collections.Counter()
    why_c, pol_b, dist = collections.Counter(), collections.Counter(), collections.Counter()
    detail = []
    for (no, _), items in sorted(rows):
        w = by_no.get(no)
        rec = v4_by_no[no]["cases"]["case3"]["trace"].get("walk") or {}
        for it in items:
            fids = set(it["fact_ids"])
            if not fids:
                tag = "골드 fact 없음(인용이 fact 와 안 맞음)"
            elif w is None:
                tag = "걸음 없음(되돌아감 · fallback)" if rec.get("fallback") else "걸음 없음"
            else:
                rec_hit = bool(fids & set(w["rec_fact_ids"]))
                new_list = bool(fids & set(w["new"]["listed"]))
                new_full = bool(fids & set(w["new"]["full"]))
                tag = ("옛 판도 받음" if rec_hit else "새 꼴 줄로 닿음" + (" · 원문" if new_full else " · cut") if new_list else "새 꼴로도 안 닿음")
                fn = fact_nodes(fids)
                vis = w["new"]["visited"]
                exp_ = {tuple(x) for x in w["new"]["expanded"]}
                secs_f = {(n_, g.facts[f]["section"]) for f in fids for n_ in fn}
                if tag == "새 꼴로도 안 닿음":
                    if fn & set(vis):
                        why = "방문 노드 · 그 section 펼침 · 1쪽 밖(more)" if secs_f & exp_ else "방문 노드 · 그 section 안 고름"
                    else:
                        h = hops(vis, fn)
                        why = f"방문 노드에서 {h}홉" if h is not None else "6홉 안 연결 없음"
                    why_c[why] += 1
                else:
                    why = None
                b_hit = bool(fids & all_sections_walk(vis, rec.get("intent")))
                d0 = hops([rec.get("start_node")], fn) if rec.get("start_node") else None
                pol_b["정책 B 닿음" if b_hit else "정책 B 안 닿음"] += 1
                dist[str(d0)] += 1
            res[tag] += 1
            detail.append({"no": no, "i": it["i"], "tier": it["tier"], "fact_ids": it["fact_ids"][:6], "path": it["path"], "tag": tag,
                           "why": why if fids and w else None})
    return {"rows": n_rows, "by_tag": dict(sorted(res.items())), "unreached_why": dict(sorted(why_c.items())),
            "policy_b_all_sections_same_nodes": dict(pol_b), "hops_from_start_to_fact_node": dict(sorted(dist.items())), "detail": detail}


def walk_stats(key: str) -> dict[str, Any]:
    xs = [x[key] for x in walk_rows]
    stops = collections.Counter(x["stop"] for x in xs)
    return {"walks": len(xs), "steps_mean": round(sum(x["steps"] for x in xs) / len(xs), 2), "steps_median": st.median(x["steps"] for x in xs),
            "steps_dist": dict(sorted(collections.Counter(x["steps"] for x in xs).items())),
            "neighbor_reached": sum(1 for x in xs if x["neighbor_reached"]), "neighbor_reached_ratio": round(sum(1 for x in xs if x["neighbor_reached"]) / len(xs), 3),
            "bytes": stat([x["bytes"] for x in xs]), "stop": dict(sorted(stops.items(), key=lambda t: str(t[0]))),
            "listed_facts": stat([len(x["listed"]) for x in xs]), "full_facts": stat([len(x["full"]) for x in xs]),
            "continued_walks": sum(1 for x in xs if x.get("continued")),
            "cut_fetch_bytes": stat([x["cut_fetch_bytes"] for x in xs]), "cut_n": stat([x["cut_n"] for x in xs]),
            "bytes_plus_cut_fetch": stat([x["bytes"] + x["cut_fetch_bytes"] for x in xs]),
            "cut_line_ratio": round(sum(x["cut_n"] for x in xs) / max(1, sum(len(x["listed"]) for x in xs)), 4)}


import time  # noqa: E402
t0 = time.perf_counter()
_pre = {p: B(FORM.expand(p[0], sections=[p[1]])) for p in pairs}
precompute_s = round(time.perf_counter() - t0, 2)
full_pair = stat([B(FORM.expand(p[0], sections=[p[1]], full=True)) for p in pairs])
peek_all_old = [B(T.peek(g, n_)) for n_ in sorted(g.nodes)]
peek_all_new = [B(new_peek(n_, FORM)) for n_ in sorted(g.nodes)]
pages = stat([-(-len(v) // FORM.k) for v in g.section_ids.values()])
over_k = sum(1 for v in g.section_ids.values() if len(v) > FORM.k)
over_8 = sum(1 for v in g.section_ids.values() if len(v) > 8)
_tl = [len(" ".join(str(f["text"]).split())) for f in g.facts.values()]
fact_chars = {**stat(_tl), "le40": round(sum(1 for x in _tl if x <= 40) / len(_tl), 4), "le60": round(sum(1 for x in _tl if x <= 60) / len(_tl), 4),
              "le80": round(sum(1 for x in _tl if x <= 80) / len(_tl), 4)}
facts_per_section = stat([len(v) for v in g.section_ids.values()])
_pl = [r for p_ in pairs for r in FORM.expand(p_[0], sections=[p_[1]])["facts"]]
pairs_cut_line_ratio = round(sum(1 for r in _pl if r.get("cut")) / len(_pl), 4)

rep = {
    "meta": {"build_hash": g.build["build_hash"], "facts": len(g.facts), "pairs": len(pairs), "form": vars(FORM), "budget": BUDGET, "max_steps": MAX_STEPS,
             "v4_batch": V4, "no_data_pattern": NO_DATA.pattern, "cut_share": round(cut_share, 4)},
    "a_all_pairs": {"old": stat(list(old_pair.values())), "new": stat(list(new_pair.values())),
                    "peek_bytes_old_sum_text": stat([g.sections_bytes[p] for p in pairs]),
                    "ratio_old_over_peekbytes": stat([round(old_pair[p] / max(1, g.sections_bytes[p])) for p in pairs]),
                    "grid": grid, "composition_old": dict(comp.most_common()), "composition_new": dict(comp_new.most_common())},
    "b_v4_calls": {"recorded": stat(calls_rec), "old_recomputed": stat(calls_old), "new": stat(calls_new), "new_app_bytes": stat(calls_new_app), "new_section_only": stat(calls_new_sec), "lines": line_tot[0], "cut_lines": line_tot[1],
                   "cut_line_ratio": round(line_tot[1] / max(1, line_tot[0]), 4), "mismatch_n": len(mism), "mismatch_head": mism[:5],
                   "peek_old": stat(peek_old), "peek_new": stat(peek_new)},
    "e_other": {"full_true_per_section": full_pair, "peek_all_old": stat(peek_all_old), "peek_all_new": stat(peek_all_new),
                "pages_per_section": pages, "sections_over_k": over_k, "sections_over_8": over_8, "fact_chars": fact_chars,
                "facts_per_section": facts_per_section, "pairs_page1_cut_line_ratio": pairs_cut_line_ratio, "precompute_bytes_seconds": precompute_s},
    "c_676_touched": {"pairs": len(touched_l), "old": stat([old_pair[p] for p in touched_l]), "new": stat([new_pair[p] for p in touched_l])},
    "d_walk": {"recorded": {"walks": len(walk_rows), "steps_mean": round(sum(x["rec_steps"] for x in walk_rows) / len(walk_rows), 2),
                            "stop": dict(collections.Counter(x["rec_stop"] for x in walk_rows))},
               "old_replay": walk_stats("old"), "new_replay": walk_stats("new"),
               "reach_case3": reach_table("case3"), "reach_case2_note": reach_table("case2")["by_tag"]},
}
(W / "spec005-v33-measure.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
print(json.dumps({k: v for k, v in rep.items() if k != "d_walk"}, ensure_ascii=False, indent=1, default=str)[:6000])
print(json.dumps({k: v for k, v in rep["d_walk"].items() if k != "reach_case3"}, ensure_ascii=False, indent=1, default=str))
print(json.dumps({k: v for k, v in rep["d_walk"]["reach_case3"].items() if k != "detail"}, ensure_ascii=False, indent=1))
