#!/usr/bin/env python3
"""walk3 — SPEC-005 v3.3 §6-7 (a)~(f) 를 **실물 코드**로 잰다(WORK-008 · 결정론 · Jev 다시 안 부름 · LLM 없음).

셈 · 재생 규칙 · 「자료에 없다」 식 · 사유 분류는 `spec005-v33-measure.py` 와 같은 식을 **여기에 다시 적는다**(import 안 함).
다른 점은 하나 — 새 꼴을 흉내 내지 않고 허브 REST(in-process TestClient 또는 --base-url)를 실제로 불러 그 본문 바이트를 센다.
그래서 옛 코드(cc637a2)에서 돌리면 기준선(옛 꼴), 새 코드에서 돌리면 새 꼴을 잰다(꼴은 첫 expand 응답의 `facts[].line` 유무로 판정).

입력(읽기만): gold-export(--export · 기본 backend/build-out/gold-export.json · 발행본과 해시가 같아야 함) · runs/runs.jsonl(b202611011148-c6ed3a · rerun-v4)
            · build-out/rerun-v4-vs-v3.json · build-out/recheck2/rerun-responses.inprocess.json(676 · WORK-007).
출력: build-out/walk3/walk3-report[.<label>].{md,json} · sizes[.<label>].json — 시간 칸은 따로 walk3-timing[.<label>].json(결정론 비교 밖).

실행(backend venv · in-process 는 DB 발행본 적재 — DATABASE_URL 은 backend/envs/.env.gold):
  cd backend && set -a && . envs/.env.gold && set +a && .venv/bin/python <E>/fail-triage-scripts/walk3.py --inprocess [--label baseline]
  .venv/bin/python <E>/fail-triage-scripts/walk3.py --base-url http://127.0.0.1:18005 --label base-url     (읽기 호출만)
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import statistics as st
import sys
import time
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import recheck2 as R  # noqa: E402 — 판정 식(Gold · norm · gold_match · rest_call) 은 recheck2 와 같은 것

E = R.E
OUT = E / "build-out" / "walk3"
V4 = "b202611011148-c6ed3a"
BUDGET = 20000
MAX_STEPS = 4
FACT_IDS_MAX = 64
NO_DATA = re.compile(r"자료에 없|정보 없음|없다고|찾지 못")  # 「자료에 없다」 류 판정 문장(SPEC §6-7 (f))
SECTIONS = ("overview", "method", "ops", "dose", "recovery", "aftercare", "timeline", "emergency", "safety.side_effects", "safety.complications",
            "safety.pih", "site_caution", "checks", "evidence", "disclosure", "products", "market")  # §4-3 · 17(이름만 · 순서는 peek 가 정함)


def B(x: Any) -> int:
    """허브 REST 본문 바이트(FastAPI JSONResponse 와 같은 직렬화)."""
    return len(json.dumps(x, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


def BA(x: Any) -> int:
    """rerun-v4 앱(clinic_chat case3 `_hub`)이 예산에 센 바이트 — json.dumps 기본 구분자(공백 있음)."""
    return len(json.dumps(x, ensure_ascii=False).encode("utf-8"))


def stat(xs: list[int]) -> dict[str, Any]:
    if not xs:
        return {"n": 0}
    s = sorted(xs)
    return {"n": len(s), "median": st.median(s), "p95": s[max(0, int(len(s) * 0.95 + 0.5) - 1)], "max": s[-1]}


# ── 허브 호출(REST 본문 그대로 · 캐시 · 결정론) ─────────────────────────────────────
class Hub:
    def __init__(self, base: str, client: Any) -> None:
        self.base, self.client = base, client
        self.cache: dict[str, tuple[int, str]] = {}
        self.calls = 0

    def raw(self, tool: str, args: dict[str, Any]) -> tuple[int, str]:
        k = R.call_key(tool, args)
        if k not in self.cache:
            self.calls += 1
            self.cache[k] = R.rest_call(self.base, tool, args, self.client)
        return self.cache[k]

    def json(self, tool: str, args: dict[str, Any]) -> tuple[dict[str, Any], int]:
        """(응답 dict, REST 본문 바이트) — 200 아니면 예외."""
        code, txt = self.raw(tool, args)
        if code != 200:
            raise RuntimeError(f"{tool} {args} → {code} {txt[:200]}")
        return json.loads(txt), len(txt.encode("utf-8"))

    def peek(self, nid: str) -> tuple[dict[str, Any], int]:
        return self.json("peek", {"id": nid})

    def expand(self, nid: str, *, sections: list[str] | None = None, neighbors: list[str] | None = None, fact_ids: list[str] | None = None,
               full: bool = False, intent: str | None = None) -> tuple[dict[str, Any], int]:
        a: dict[str, Any] = {"id": nid}
        for k, v in (("sections", sections), ("neighbors", neighbors), ("fact_ids", fact_ids), ("intent", intent)):
            if v:
                a[k] = v
        if full:
            a["full"] = True
        return self.json("expand", a)


def make_hub(args: argparse.Namespace) -> Hub:
    if args.inprocess:
        return Hub("http://127.0.0.1:18005", R.inprocess_client())
    return Hub(args.base_url.rstrip("/"), None)


def is_line_form(resp: dict[str, Any]) -> bool:
    """v3.3 꼴 = facts[] 에 line(또는 full 의 text 와 함께 claude_contract.allowed) · 옛 꼴 = sections{s: {facts, more_ids}}."""
    return (resp.get("claude_contract") or {}).get("allowed") == "facts_uncut"


# ── 걸음 재생(SPEC §6-7 규칙 1~5) ────────────────────────────────────────────────
def picked_items(step: dict[str, Any]) -> tuple[list[str], list[str]]:
    secs, nbs = [], []
    for x in step["jev"].get("picked") or []:
        if x.startswith("section:"):
            secs.append(x[8:])
        else:
            nbs.append(x)
    return secs, nbs


ExpandFn = Callable[..., dict[str, Any]]
PeekSecsFn = Callable[[str], list[str]]


def replay(w: dict[str, Any], expand_fn: ExpandFn, peek_secs: PeekSecsFn, line_form: bool) -> dict[str, Any]:
    """기록된 걸음의 선택(picked 전부 — 옛 판에서 예산으로 빠진 것 포함)을 같은 순서로 · section 하나씩(이웃은 첫 호출에 같이) · 앱이 넘긴 intent 그대로.
    예산 = expand 응답 BA 합 · 처음 넘는 호출은 통째로 빼고 그 걸음에서 멈춤(budget). 기록이 끝났는데 기록 stop == budget 이고 새 꼴이면 이어감:
    다음 노드 = 펼친 이웃 큐(넣은 순서 · 방문 안 한 것 · 없으면 frontier_empty) · 고르는 것 = 그 판 Jev section ∩ 그 노드 peek section(peek 순) · 이웃 안 고름.
    기록 stop 이 enough · steps · empty 면 같은 자리에서 멈춤. 옛 꼴(line_form False)은 이어 가지 않는다(기록 재현 확인용)."""
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
        elif w.get("stop") == "budget" and line_form:
            node = next((q for q in queue if q not in visited), None)
            if node is None:
                stop = "frontier_empty"
                break
            secs = [x for x in peek_secs(node) if x in jev_secs]
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
            resp = expand_fn(node, sections=[sx] if sx else None, neighbors=nb or None, intent=w.get("intent"))
            by = BA(resp)
            if used + by > BUDGET:
                hit = True
                break
            used += by
            if sx:
                expanded.add((node, sx))
            for f in resp.get("facts") or []:
                listed.append(f["id"])
                if not f.get("cut"):
                    full_ids.append(f["id"])
                elif f["id"] not in cut_by_node[node]:
                    cut_by_node[node].append(f["id"])
            for sec in (resp.get("sections") or {}).values() if not line_form else ():
                listed += [x for x in sec.get("facts", []) if isinstance(x, str)] + list(sec.get("more_ids") or [])
            for x in nb:
                if x not in queue:
                    queue.append(x)
        if hit:
            stop = "budget"
            break
    else:
        stop = "steps"
    fetch = sum(BA(expand_fn(n_, fact_ids=ids[:FACT_IDS_MAX], intent=w.get("intent"))) for n_, ids in cut_by_node.items()) if line_form else 0
    return {"steps": n_steps, "bytes": used, "cut_fetch_bytes": fetch, "cut_n": sum(len(v) for v in cut_by_node.values()), "stop": stop,
            "listed": sorted(set(listed)), "full": sorted(set(full_ids)), "neighbor_reached": len(visited) >= 2, "continued": cont,
            "visited": visited, "expanded": sorted(expanded)}


def walk_stats(xs: list[dict[str, Any]]) -> dict[str, Any]:
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


# ── 그래프 구조(gold-export · 홉 · fact 노드) ───────────────────────────────────────
class Graph:
    def __init__(self, gold: R.Gold) -> None:
        self.gold = gold
        self.adj: dict[str, set[str]] = collections.defaultdict(set)
        for e in gold.edges_by_id.values():
            a, z = e["from_id"], e["to_id"]
            zs = (z or "")[11:].split("|") if (z or "").startswith("candidates:") else [z]
            for z_ in zs:
                if a in gold.nodes and z_ in gold.nodes:
                    self.adj[a].add(z_)
                    self.adj[z_].add(a)

    def hops(self, src: list[str], dst: set[str], cap: int = 6) -> int | None:
        if not dst:
            return None
        seen, fr = set(src), list(src)
        for d in range(cap + 1):
            if seen & dst:
                return d
            nxt = []
            for x in fr:
                for y in self.adj.get(x, ()):
                    if y not in seen:
                        seen.add(y)
                        nxt.append(y)
            fr = nxt
        return None

    def fact_nodes(self, fids: set[str]) -> set[str]:
        out: set[str] = set()
        for f in fids:
            x = self.gold.facts[f]
            for o in [x["owner_id"]] + list(x.get("attached_to") or []):
                if o in self.gold.nodes:
                    out.add(o)
                elif o in self.gold.edges_by_id:
                    e = self.gold.edges_by_id[o]
                    out |= {e["from_id"], e["to_id"]} & set(self.gold.nodes)
        return out


def no_data_rows(d: dict[str, Any]) -> list[tuple[int, dict[str, Any]]]:
    """rerun-v4 remaining_failures 중 정확성 · case3/case2 · 판정 문장이 「자료에 없다」 류인 행(SPEC §6-7 (f))."""
    return [(i, row) for i, row in enumerate(d["remaining_failures"])
            if row["item"] == "accuracy" and row["case"] in ("case3", "case2") and NO_DATA.search(row["claim"])]


def gold_hits(gold: R.Gold, d: dict[str, Any]) -> dict[tuple[str, str], list[dict[str, Any]]]:
    out: dict[tuple[str, str], list[dict[str, Any]]] = collections.defaultdict(list)
    for i, row in no_data_rows(d):
        q = R.norm((row.get("evidence") or {}).get("quote") or "")
        tier, hits = gold.gold_match(q) if len(q) >= 2 else (None, [])
        fids = sorted({h[2]["fact_id"] for h in hits if h[1] == "fact"})
        nodes = sorted({n for h in hits for n in gold.owners_of(h[1], h[2])})
        out[(row["no"], row["case"])].append({"i": i, "tier": tier, "fact_ids": fids, "nodes": nodes, "path": (row.get("evidence") or {}).get("path")})
    return out


# ── 본체 ─────────────────────────────────────────────────────────────────────
def measure(hub: Hub, gold: R.Gold, runs: list[dict[str, Any]], v4vs3: dict[str, Any], resp676: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any], dict[str, float]]:
    tm: dict[str, float] = {}
    t0 = time.perf_counter()
    G = Graph(gold)
    nodes = sorted(gold.nodes)
    peeks = {n: hub.peek(n) for n in nodes}
    tm["peek_1071_s"] = round(time.perf_counter() - t0, 2)
    pairs = [(n, s["name"]) for n in nodes for s in peeks[n][0]["sections"]]
    pair_set = set(pairs)
    peek_secs = {n: [s["name"] for s in peeks[n][0]["sections"]] for n in nodes}

    def ex(nid: str, **kw: Any) -> dict[str, Any]:
        return hub.expand(nid, **kw)[0]

    probe = hub.expand(pairs[0][0], sections=[pairs[0][1]])[0]
    line_form = is_line_form(probe)

    # (a) · (b) · (c) 전 (노드, section)
    t0 = time.perf_counter()
    a_bytes, b_bytes, c_diff, rows_sizes = {}, {}, [], []
    lines_total = cut_total = 0
    for n, s in pairs:
        r, by = hub.expand(n, sections=[s])
        a_bytes[(n, s)] = by
        rf, byf = hub.expand(n, sections=[s], full=True)
        b_bytes[(n, s)] = byf
        pb = next(x["bytes"] for x in peeks[n][0]["sections"] if x["name"] == s)
        if pb != by:
            c_diff.append({"node": n, "section": s, "peek_bytes": pb, "expand_bytes": by})
        if line_form:
            lines_total += len(r["facts"])
            cut_total += sum(1 for x in r["facts"] if x.get("cut"))
        rows_sizes.append({"node": n, "section": s, "expand": by, "full": byf, "peek_bytes": pb, "n_facts": next(x["n_facts"] for x in peeks[n][0]["sections"] if x["name"] == s)})
    tm["pairs_6140_s"] = round(time.perf_counter() - t0, 2)

    # rerun-v4 걸음 호출 476 · 걸음이 연 peek 311
    v4 = [r for r in runs if r.get("batch_id") == V4]
    calls_rec, calls_ba, calls_b, calls_b_sec, peek_walk, mism = [], [], [], [], [], []
    walk_lines = [0, 0]
    for r in v4:
        w = r["cases"]["case3"]["trace"].get("walk") or {}
        for s in w.get("steps", []):
            peek_walk.append(peeks[s["node"]][1] if s["node"] in peeks else hub.peek(s["node"])[1])
            for c in (s.get("expand") or {}).get("calls", []):
                resp, by = hub.expand(s["node"], sections=c.get("sections") or None, neighbors=c.get("neighbors") or None, intent=w.get("intent"))
                ba = BA(resp)
                calls_rec.append(c["bytes"])
                calls_ba.append(ba)
                calls_b.append(by)
                if not c.get("neighbors"):
                    calls_b_sec.append(by)
                if line_form:
                    walk_lines[0] += len(resp["facts"])
                    walk_lines[1] += sum(1 for x in resp["facts"] if x.get("cut"))
                if ba != c["bytes"]:
                    mism.append({"no": r["question_no"], "node": s["node"], "sections": c.get("sections"), "app_bytes_now": ba, "recorded": c["bytes"]})

    # 676 재실행이 닿은 (노드, section)
    touched: set[tuple[str, str]] = set()
    for c in resp676:
        inp = c["input"] if isinstance(c["input"], dict) else None
        if inp is None:
            try:
                inp = eval(c["input"], {}, {})  # noqa: S307 — recheck2 가 repr 로 저장한 dict(measure 와 같은 읽기)
            except Exception:  # noqa: BLE001
                continue
        if not isinstance(inp, dict):
            continue
        ns = set()
        for v in inp.values():
            for x in (v if isinstance(v, list) else [v]):
                if isinstance(x, str) and x in gold.nodes:
                    ns.add(x)
        secs = [x for x in inp.get("sections") or [] if x in SECTIONS]
        for nid in ns:
            for s in secs or SECTIONS:
                if (nid, s) in pair_set:
                    touched.add((nid, s))
    touched_l = sorted(touched)

    # (e) 걸음 재생
    t0 = time.perf_counter()
    walk_rows = []
    for r in v4:
        w = r["cases"]["case3"]["trace"].get("walk") or {}
        if not w.get("steps") or w.get("fallback"):
            continue
        new = replay(w, ex, lambda n: peek_secs[n] if n in peek_secs else [x["name"] for x in hub.peek(n)[0]["sections"]], line_form)
        walk_rows.append({"no": r["question_no"], "rec_stop": w.get("stop"), "rec_steps": w.get("steps_n"), "rec_fact_ids": w.get("fact_ids") or [], "new": new})
    tm["replay_s"] = round(time.perf_counter() - t0, 2)
    by_no = {x["no"]: x for x in walk_rows}
    v4_by_no = {r["question_no"]: r for r in v4}

    def all_sections_walk(visited: list[str], intent: str | None) -> set[str]:
        """정책 B(상한 참고) — 같은 방문 노드 순서 · 노드마다 section 전부(peek 순 · 1쪽) · 같은 예산."""
        used, listed = 0, set()
        for node in visited[:MAX_STEPS]:
            for sx in peek_secs.get(node, []):
                r_ = ex(node, sections=[sx], intent=intent)
                by = BA(r_)
                if used + by > BUDGET:
                    return listed
                used += by
                listed |= {f["id"] for f in r_.get("facts") or []}
        return listed

    hits = gold_hits(gold, v4vs3)

    def reach_table(case: str) -> dict[str, Any]:
        rows = [(k, v) for k, v in hits.items() if k[1] == case]
        res, why_c, pol_b, dist = collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter()
        detail = []
        for (no, _), items in sorted(rows):
            w = by_no.get(no)
            rec = v4_by_no[no]["cases"]["case3"]["trace"].get("walk") or {}
            for it in items:
                fids = set(it["fact_ids"])
                why = None
                if not fids:
                    tag = "골드 fact 없음(인용이 fact 와 안 맞음)"
                elif w is None:
                    tag = "걸음 없음(되돌아감 · fallback)" if rec.get("fallback") else "걸음 없음"
                else:
                    rec_hit = bool(fids & set(w["rec_fact_ids"]))
                    new_list = bool(fids & set(w["new"]["listed"]))
                    new_full = bool(fids & set(w["new"]["full"]))
                    if rec_hit:
                        tag = "옛 판도 받음"
                    elif new_list:
                        tag = "새 꼴 줄로 닿음" + (" · 원문" if new_full else " · cut")
                    else:
                        tag = "새 꼴로도 안 닿음"
                    fn = G.fact_nodes(fids)
                    vis = w["new"]["visited"]
                    exp_ = {tuple(x) for x in w["new"]["expanded"]}
                    secs_f = {(n_, gold.facts[f]["section"]) for f in fids for n_ in fn}
                    if tag == "새 꼴로도 안 닿음":
                        if fn & set(vis):
                            why = "방문 노드 · 그 section 펼침 · 1쪽 밖(more)" if secs_f & exp_ else "방문 노드 · 그 section 안 고름"
                        else:
                            h = G.hops(vis, fn)
                            why = f"방문 노드에서 {h}홉" if h is not None else "6홉 안 연결 없음"
                        why_c[why] += 1
                    b_hit = bool(fids & all_sections_walk(vis, rec.get("intent")))
                    d0 = G.hops([rec.get("start_node")], fn) if rec.get("start_node") else None
                    pol_b["정책 B 닿음" if b_hit else "정책 B 안 닿음"] += 1
                    dist[str(d0)] += 1
                res[tag] += 1
                detail.append({"no": no, "i": it["i"], "tier": it["tier"], "fact_ids": it["fact_ids"][:6], "path": it["path"], "tag": tag, "why": why})
        return {"rows": sum(len(v) for _, v in rows), "by_tag": dict(sorted(res.items())), "unreached_why": dict(sorted(why_c.items())),
                "policy_b_all_sections_same_nodes": dict(sorted(pol_b.items())), "hops_from_start_to_fact_node": dict(sorted(dist.items())), "detail": detail}

    t0 = time.perf_counter()
    reach3 = reach_table("case3")
    reach2 = reach_table("case2")["by_tag"]
    tm["reach_s"] = round(time.perf_counter() - t0, 2)

    peek_all = [peeks[n][1] for n in nodes]
    n_facts_items = [it.get("n_facts") for n in nodes for v in peeks[n][0]["neighbors_by_kind"].values() for it in v["items"]]
    items_per_kind = max((len(v["items"]) for n in nodes for v in peeks[n][0]["neighbors_by_kind"].values()), default=0)
    sec_only = [x for x in walk_rows]
    rep = {
        "meta": {"build_hash": probe["build"]["build_hash"], "export_hash": gold.hash, "nodes": len(nodes), "pairs": len(pairs), "form": "v3.3 line" if line_form else "v3.2 sections",
                 "budget": BUDGET, "max_steps": MAX_STEPS, "v4_batch": V4, "no_data_pattern": NO_DATA.pattern, "hub_calls_unique": len(hub.cache)},
        "a_pairs": {"default": stat(list(a_bytes.values())), "lines": lines_total, "cut_lines": cut_total,
                    "cut_line_ratio": round(cut_total / lines_total, 4) if lines_total else None},
        "a_walk_calls": {"recorded_app_bytes": stat(calls_rec), "now_app_bytes": stat(calls_ba), "now_rest_bytes": stat(calls_b), "now_rest_bytes_no_neighbors": stat(calls_b_sec),
                         "same_as_recorded": len(calls_rec) - len(mism), "mismatch_n": len(mism), "mismatch_head": mism[:5],
                         "lines": walk_lines[0], "cut_lines": walk_lines[1], "cut_line_ratio": round(walk_lines[1] / walk_lines[0], 4) if walk_lines[0] else None},
        "a_676_touched": {"pairs": len(touched_l), "default": stat([a_bytes[p] for p in touched_l])},
        "b_full": stat(list(b_bytes.values())),
        "c_peek_bytes": {"pairs": len(pairs), "equal": len(pairs) - len(c_diff), "diff_n": len(c_diff), "diff_head": c_diff[:5]},
        "d_peek": {"all": stat(peek_all), "walk_opened": stat(peek_walk), "items_per_kind_max": items_per_kind,
                   "items_with_n_facts": sum(1 for x in n_facts_items if x is not None), "items": len(n_facts_items)},
        "e_walk": {"recorded": {"walks": len(walk_rows), "steps_mean": round(sum(x["rec_steps"] for x in walk_rows) / len(walk_rows), 2),
                                "stop": dict(sorted(collections.Counter(x["rec_stop"] for x in sec_only).items()))},
                   "replay": walk_stats([x["new"] for x in walk_rows])},
        "f_reach_case3": reach3,
        "f_reach_case2_note": reach2,
    }
    sizes = {"build_hash": rep["meta"]["build_hash"], "form": rep["meta"]["form"], "pairs": rows_sizes,
             "walk_calls": [{"recorded": a, "now_app": b, "now_rest": c} for a, b, c in zip(calls_rec, calls_ba, calls_b, strict=True)]}
    return rep, sizes, tm


# ── 끝 조건 판정 · md ──────────────────────────────────────────────────────────
def verdict(rep: dict[str, Any]) -> dict[str, Any]:
    a, aw, b, c, d, e, f = rep["a_pairs"]["default"], rep["a_walk_calls"]["now_rest_bytes_no_neighbors"], rep["b_full"], rep["c_peek_bytes"], rep["d_peek"]["all"], rep["e_walk"]["replay"], rep["f_reach_case3"]["by_tag"]
    new_reach = sum(v for k, v in f.items() if k.startswith("새 꼴 줄로 닿음"))
    return {
        "(a) 6,140 중앙 ≤ 2,000 · p95 ≤ 5,000": a["median"] <= 2000 and a["p95"] <= 5000,
        "(a) 이웃 없는 걸음 호출 중앙 ≤ 2,000 · p95 ≤ 5,000": aw["median"] <= 2000 and aw["p95"] <= 5000,
        "(b) full 중앙 ≤ 4,000 · p95 ≤ 8,000": b["median"] <= 4000 and b["p95"] <= 8000,
        "(c) peek bytes 차 0": c["diff_n"] == 0,
        "(d) peek 1,071 중앙 ≤ 2,500 · p95 ≤ 8,000 · n_facts": d["median"] <= 2500 and d["p95"] <= 8000 and rep["d_peek"]["items_with_n_facts"] == rep["d_peek"]["items"],
        "(e) 평균 걸음 ≥ 3.0 · 이웃 도달 ≥ 85% · 걸음 바이트 ≤ 20,000": e["steps_mean"] >= 3.0 and e["neighbor_reached_ratio"] >= 0.85 and e["bytes"]["max"] <= BUDGET,
        "(f) 「자료에 없다」 case3 새로 닿음 ≥ 5": new_reach >= 5,
    }


def render(rep: dict[str, Any], label: str) -> str:
    m, v = rep["meta"], verdict(rep)
    L = [f"# walk3 — SPEC-005 v3.3 §6-7 (a)~(f){' · ' + label if label else ''}", "",
         f"빌드 `{m['build_hash']}` · export `{m['export_hash']}` · 꼴 **{m['form']}** · 노드 {m['nodes']} · (노드, section) {m['pairs']} · 예산 {m['budget']} · 걸음 {m['max_steps']} · 고유 호출 {m['hub_calls_unique']}", "",
         "| 끝 조건 | 통과 |", "|---|---|"]
    L += [f"| {k} | {'○' if ok else '✗'} |" for k, ok in v.items()]

    def s(x: dict[str, Any]) -> str:
        return f"n {x['n']} · 중앙 {x['median']} · p95 {x['p95']} · 최대 {x['max']}" if x.get("n") else "n 0"
    aw = rep["a_walk_calls"]
    L += ["", "## (a) expand 기본 꼴 · section 1", "",
          f"- 전 (노드, section): {s(rep['a_pairs']['default'])} · 줄 {rep['a_pairs']['lines']} · cut {rep['a_pairs']['cut_lines']}({rep['a_pairs']['cut_line_ratio']})",
          f"- rerun-v4 걸음 호출(REST 본문 · 이웃 포함): {s(aw['now_rest_bytes'])}",
          f"- 그중 이웃 없는 호출: {s(aw['now_rest_bytes_no_neighbors'])}",
          f"- 앱 셈(json.dumps 기본) 지금 꼴: {s(aw['now_app_bytes'])} · 기록: {s(aw['recorded_app_bytes'])} · 기록과 같음 {aw['same_as_recorded']}/{aw['recorded_app_bytes']['n']}(차 {aw['mismatch_n']})",
          f"- 걸음 호출 줄 {aw['lines']} · cut {aw['cut_lines']}({aw['cut_line_ratio']})",
          f"- 676 재실행이 닿은 쌍: {rep['a_676_touched']['pairs']} · {s(rep['a_676_touched']['default'])}",
          "", "## (b) full=true", "", f"- {s(rep['b_full'])}",
          "", "## (c) peek bytes = 실제 expand 본문", "", f"- 같음 {rep['c_peek_bytes']['equal']}/{rep['c_peek_bytes']['pairs']} · 차 {rep['c_peek_bytes']['diff_n']}",
          "", "## (d) peek", "", f"- 1,071: {s(rep['d_peek']['all'])}", f"- 걸음이 연 peek: {s(rep['d_peek']['walk_opened'])}",
          f"- 종류별 items 최대 {rep['d_peek']['items_per_kind_max']} · n_facts 있는 items {rep['d_peek']['items_with_n_facts']}/{rep['d_peek']['items']}"]
    e = rep["e_walk"]["replay"]
    L += ["", "## (e) 걸음 재생", "",
          f"- 기록: 판 {rep['e_walk']['recorded']['walks']} · 평균 걸음 {rep['e_walk']['recorded']['steps_mean']} · 멈춤 {rep['e_walk']['recorded']['stop']}",
          f"- 재생: 평균 걸음 **{e['steps_mean']}** · 중앙 {e['steps_median']} · 분포 {e['steps_dist']} · 이웃 도달 **{e['neighbor_reached']}/{e['walks']} = {e['neighbor_reached_ratio']}**",
          f"- 멈춤 {e['stop']} · 이어 간 판 {e['continued_walks']}",
          f"- 걸음 바이트 {s(e['bytes'])} · 줄로 받은 fact {s(e['listed_facts'])} · 원문(cut 없음) {s(e['full_facts'])}",
          f"- cut 줄 {s(e['cut_n'])} · cut 원문 받기 바이트(재생에 안 넣음 · V-15) {s(e['cut_fetch_bytes'])} · 합 {s(e['bytes_plus_cut_fetch'])} · cut 비율 {e['cut_line_ratio']}"]
    f = rep["f_reach_case3"]
    L += ["", "## (f) 「자료에 없다」 case3", "", f"- 행 {f['rows']} · 분류 {f['by_tag']}", f"- 안 닿은 자리 {f['unreached_why']}",
          f"- 정책 B {f['policy_b_all_sections_same_nodes']} · 시작 노드 → fact 노드 홉 {f['hops_from_start_to_fact_node']}",
          f"- (참고) case2 같은 식 {rep['f_reach_case2_note']}", "", "| 문항 | 행 | tier | 분류 | 자리 | fact id(앞 6) |", "|---|---|---|---|---|---|"]
    L += [f"| {x['no']} | {x['i']} | {x['tier']} | {x['tag']} | {x['why'] or ''} | {' '.join(x['fact_ids'])} |" for x in f["detail"]]
    return "\n".join(L) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--inprocess", action="store_true")
    g.add_argument("--base-url")
    ap.add_argument("--export", default=str(R.BACKEND / "build-out" / "gold-export.json"))
    ap.add_argument("--label", default="")
    ap.add_argument("--out-dir", default=str(OUT))
    a = ap.parse_args()
    t0 = time.perf_counter()
    hub = make_hub(a)
    gold = R.Gold(Path(a.export))
    runs = [json.loads(x) for x in (E / "runs" / "runs.jsonl").open(encoding="utf-8") if x.strip()]
    v4vs3 = json.loads((E / "build-out" / "rerun-v4-vs-v3.json").read_text(encoding="utf-8"))
    resp676 = json.loads((E / "build-out" / "recheck2" / "rerun-responses.inprocess.json").read_text(encoding="utf-8"))
    rep, sizes, tm = measure(hub, gold, runs, v4vs3, resp676)
    if rep["meta"]["build_hash"] != gold.hash:
        print(f"경고: 허브 빌드 {rep['meta']['build_hash']} ≠ export {gold.hash}", file=sys.stderr)
    tm["total_s"] = round(time.perf_counter() - t0, 2)
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    suf = f".{a.label}" if a.label else ""
    (out / f"walk3-report{suf}.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1, sort_keys=False) + "\n", encoding="utf-8")
    (out / f"walk3-report{suf}.md").write_text(render(rep, a.label), encoding="utf-8")
    (out / f"sizes{suf}.json").write_text(json.dumps(sizes, ensure_ascii=False, indent=0) + "\n", encoding="utf-8")
    (out / f"walk3-timing{suf}.json").write_text(json.dumps({**tm, "ran_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"verdict": verdict(rep), "meta": rep["meta"], "timing": tm}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
