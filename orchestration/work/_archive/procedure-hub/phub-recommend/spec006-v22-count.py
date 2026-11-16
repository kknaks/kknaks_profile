"""SPEC-006 v2.2 근거 셈(읽기 전용 · 결정론 · LLM · 허브 · CLI 호출 없음).

입력: rerun-v4 배치 b202611011148-c6ed3a(runs.jsonl) · rerun-v3 배치 b202610311552-d39a4d · fail-triage2.json ·
      허브 gold-export.json(b031371c — rerun-v4 와 같은 빌드) · CLI 바이너리 문자열(stray 오류 문구 확인)
출력: spec006-v22-count.json · .md (이 폴더) — 두 번 돌려 바이트 같음.

셈 4:
  A. 걸음 해부 — case3 걸음 판 148: 걸음 수 · 멈춤 · 이웃 peek 도달 · budget 멈춤 때 대기 이웃(frontier) · expand 호출 바이트(섹션별)
  B. 답이 산 노드 종류 — case2 · case3 채점 실패 행(valid 근거)의 인용 → 골드 hit → 가장 가까운 owner 의 종류(시작 노드 기준) · 의도별
  C. 새 꼴 재생 — 기록된 expand 호출의 fact 를 짧은 꼴 {id, line(앞 N자), section, owner} 로 다시 셈 · 걸음 1 뒤 남은 예산
  D. stray 15 — 문항 · 차례 · 직전 도구 · 다음 도구 · 입력 꼴 · 오류 바이트 = 64 + len(이름) 대조
"""
from __future__ import annotations

import collections
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUNS = ROOT / "reference/2026-10-30-hub-evals/runs/runs.jsonl"
TRIAGE2 = ROOT / "reference/2026-10-30-hub-evals/build-out/fail-triage2.json"
EXPORT = Path("/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend/build-out/gold-export.json")
V4, V3 = "b202611011148-c6ed3a", "b202610311552-d39a4d"
OUT = Path(__file__).with_name("spec006-v22-count")
LINE_NS = (60, 80, 120)
BUDGETS = (12000, 16000, 20000)

sys.path.insert(0, str(ROOT / "reference/2026-10-30-hub-evals/build-out/fail-triage2-scripts"))
from triage2 import Gold, norm  # noqa: E402 — 같은 판정 식(복사 안 함)


def med(xs):
    return statistics.median(xs) if xs else None


def pct(xs, p):
    if not xs:
        return None
    s = sorted(xs)
    return s[min(len(s) - 1, int(round(p * (len(s) - 1))))]


def jb(o) -> int:
    return len(json.dumps(o, ensure_ascii=False).encode("utf-8"))


# 이웃 종류(발주서 다섯 + 나머지) — edge kind · 노드 kind → 묶음 이름
EDGE_GROUP = {
    "site_caution": "부위 위험", "site_caution_unit": "부위 위험",
    "requires_check": "금기 조건", "requires_check_unit": "금기 조건", "requires_check_product": "금기 조건", "requires_check_package": "금기 조건",
    "procedure_relation": "쌍 관계", "procedure_pair": "쌍 관계",
    "combo_component": "조합", "anchors_combo": "조합",
    "key_family": "계열", "product_family": "계열", "family_technique": "계열", "child_of": "계열",
    "has_complication": "합병증", "has_complication_unit": "합병증",
    "treats": "고민 관계", "treats_unit": "고민 관계", "concern_avoid": "고민 관계", "concern_avoid_unit": "고민 관계",
    "concern_site": "부위", "key_site": "부위",
    "product_unit": "제품", "uses_product": "제품",
    "has_statement": "근거", "has_statement_unit": "근거", "cites": "근거",
}
NODE_GROUP = {"check_condition": "금기 조건", "combo": "조합", "family": "계열", "complication": "합병증", "concern": "고민 관계",
              "purpose": "고민 관계", "site": "부위", "product": "제품", "evidence_statement": "근거", "evidence_source": "근거",
              "unit_procedure": "다른 시술", "technique": "계열", "package": "조합"}


class Graph:
    def __init__(self, gold: Gold) -> None:
        self.g = gold
        self.inc: dict[str, list[tuple[str, str, str]]] = collections.defaultdict(list)  # node → (edge kind, other, edge id)
        for e in gold.edges_by_id.values():
            self.inc[e["from_id"]].append((e["kind"], e["to_id"], e["id"]))
            self.inc[e["to_id"]].append((e["kind"], e["from_id"], e["id"]))

    def group_of(self, start: str, k: str, ref: dict) -> tuple[str, int]:
        """hit 하나 → (묶음, 홉). 홉 0 = 시작 노드 자신(섹션)."""
        g = self.g
        if k == "fact":
            oid = ref["owner_id"]
            if oid == start:
                return "섹션(시작 노드)", 0
            e = g.edges_by_id.get(oid)
            if e is not None:  # 엣지가 owner(site_caution · procedure_relation · treats · product_family …)
                grp = EDGE_GROUP.get(e["kind"], "기타 엣지")
                if start in (e["from_id"], e["to_id"]):
                    return grp, 1
                d = self.hops(start, {e["from_id"], e["to_id"]})
                return grp, (d + 1 if d is not None else 99)
            if oid in g.nodes:
                return self.node_group(start, oid)
            if oid.startswith("scope:"):
                tg = [t for t in ((g.facts[ref["fact_id"]]["source"].get("meta") or {}).get("target_keys") or []) if t in g.nodes]
                if start in tg:
                    return "섹션(시작 노드)", 0
                d = self.hops(start, set(tg)) if tg else None
                return "전역 · scope", (d + 1 if d is not None else 1)
            return "노드 밖(조합 메모 · CC)", 99
        if k in ("node_attr", "node_name"):
            return self.node_group(start, ref["node_id"])
        if k == "edge_attr":
            grp = EDGE_GROUP.get(ref["kind"], "기타 엣지")
            if start in (ref["from"], ref["to"]):
                return grp, 1
            d = self.hops(start, {ref["from"], ref["to"]})
            return grp, (d + 1 if d is not None else 99)
        return "전역 · scope", 1

    def node_group(self, start: str, nid: str) -> tuple[str, int]:
        if nid == start:
            return "섹션(시작 노드)", 0
        for ek, other, _ in self.inc.get(start, ()):
            if other == nid:
                return EDGE_GROUP.get(ek, NODE_GROUP.get(self.g.nodes[nid]["kind"], "기타")), 1
        d = self.hops(start, {nid})
        return NODE_GROUP.get(self.g.nodes[nid]["kind"], "기타"), (d if d is not None else 99)

    def edges1(self, start: str, k: str, ref: dict) -> set[str]:
        """hit 하나가 S 의 1홉이면 S 와 잇는 edge kind 들(v2.3 순서 표 · edge kind 단위)."""
        g = self.g
        if k == "fact":
            oid = ref["owner_id"]
            e = g.edges_by_id.get(oid)
            if e is not None:
                return {e["kind"]} if start in (e["from_id"], e["to_id"]) else set()
            tgt = {oid} if oid in g.nodes else set()
        elif k in ("node_attr", "node_name"):
            tgt = {ref["node_id"]}
        elif k == "edge_attr":
            return {ref["kind"]} if start in (ref["from"], ref["to"]) else set()
        else:
            return set()
        return {ek for ek, other, _ in self.inc.get(start, ()) if other in tgt}

    def hops(self, start: str, targets: set[str], limit: int = 3) -> int | None:
        if start in targets:
            return 0
        seen, front = {start}, [start]
        for d in range(1, limit + 1):
            nxt = []
            for n in front:
                for x in self.g.adj.get(n, ()):
                    if x in targets:
                        return d
                    if x not in seen:
                        seen.add(x)
                        nxt.append(x)
            front = nxt
        return None


def load(batch: str) -> dict[str, dict]:
    out = {}
    with RUNS.open(encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            if r.get("batch_id") == batch:
                out[r["question_no"]] = r
    return out


def walk_anatomy(v4: dict[str, dict]) -> dict:
    runs = [r["cases"]["case3"]["trace"]["walk"] for r in v4.values()]
    walked = [w for w in runs if not w.get("fallback")]
    reach_nb = sum(1 for w in walked if any(s.get("node") != w["start_node"] for s in w["steps"] if s.get("peek_bytes")))
    reach_nb_fact = sum(1 for w in walked if any(s.get("node") != w["start_node"] and (s.get("expand") or {}).get("fact_ids") for s in w["steps"]))
    step1 = [w["steps"][0] for w in walked if w["steps"]]
    picked_sec = [sum(1 for x in (s.get("jev") or {}).get("picked", []) if x.startswith("section:")) for s in step1]
    picked_nb = [sum(1 for x in (s.get("jev") or {}).get("picked", []) if not x.startswith("section:")) for s in step1]
    # budget 멈춤 때 대기 이웃(첫 expand 호출이 담겼으면 이웃이 frontier 에 들어갔는데 peek 를 못 함)
    budget = [w for w in walked if w["stop"] == "budget"]
    queued = []
    for w in budget:
        visited = {s["node"] for s in w["steps"]}
        q = set()
        for s in w["steps"]:
            ex = s.get("expand") or {}
            calls = ex.get("calls") or []
            if calls and not calls[0].get("excluded"):
                q |= set(calls[0].get("neighbors") or [])
        queued.append(len(q - visited))
    budget_step1 = sum(1 for w in budget if len(w["steps"]) == 1)
    excl_first = sum(1 for w in budget if (w["steps"][-1].get("expand") or {}).get("calls", [{}])[0].get("excluded"))
    sec_bytes: dict[str, list[int]] = collections.defaultdict(list)
    for w in runs:
        for s in w["steps"]:
            for c in (s.get("expand") or {}).get("calls") or []:
                if len(c.get("sections") or []) == 1 and not c.get("neighbors"):
                    sec_bytes[c["sections"][0]].append(c["bytes"])
    return {
        "runs": len(runs), "walked": len(walked), "fallback": len(runs) - len(walked),
        "stop": dict(collections.Counter(w["stop"] for w in runs)),
        "steps_n": dict(sorted(collections.Counter(w["steps_n"] for w in runs).items())),
        "neighbor_peek_reached": reach_nb, "neighbor_fact_reached": reach_nb_fact,
        "steps_n_median_all": med([w["steps_n"] for w in runs]),
        "step1_picked_sections_median": med(picked_sec), "step1_picked_neighbors_median": med(picked_nb),
        "step1_picked_neighbors_ge1": sum(1 for x in picked_nb if x >= 1),
        "budget_stops": len(budget), "budget_stop_at_step1": budget_step1,
        "budget_stop_with_queued_neighbors": sum(1 for x in queued if x > 0), "queued_neighbors_median": med([x for x in queued if x > 0]),
        "budget_stop_first_call_excluded": excl_first,
        "section_call_bytes": {k: {"n": len(v), "median": med(v), "p95": pct(v, 0.95), "max": max(v)}
                               for k, v in sorted(sec_bytes.items(), key=lambda kv: -len(kv[1]))},
    }


def answer_kinds(gold: Gold, graph: Graph, v4: dict[str, dict], tri: dict) -> dict:
    """채점 실패 행 → 답이 산 곳(시작 노드 기준 가장 가까운 hit) · 의도별."""
    def rows_v4():
        for q, r in v4.items():
            for case in ("case2", "case3"):
                for f in r["cases"][case].get("judge", {}).get("failures") or []:
                    if f.get("status") == "valid" and (f.get("evidence") or {}).get("quote"):
                        yield "v4", q, case, f["item"], f["evidence"]["quote"], ("자료에 없" in (f.get("claim") or ""))

    def rows_v3():
        for row in tri["rows"]:
            ev = row.get("evidence") or {}
            if ev.get("quote"):
                yield "v3", row["question_no"], row["case"], row["item"], ev["quote"], bool(row.get("answer_says_unknown"))

    out_rows = []
    for src, q, case, item, quote, unknown in list(rows_v4()) + list(rows_v3()):
        w = v4.get(q, {}).get("cases", {}).get("case3", {}).get("trace", {}).get("walk") or {}
        start, intent = w.get("start_node"), w.get("intent")
        tier, hits = gold.gold_match(norm(quote))
        best = ("골드에 없음", 99)
        e1: list[str] = []
        if start and hits:
            cands = [graph.group_of(start, k, ref) for _, k, ref in hits]
            best = min(cands, key=lambda t: (t[1], t[0]))
            e1 = sorted(set().union(*(graph.edges1(start, k, ref) for _, k, ref in hits))) if best[1] == 1 else []
        elif hits:
            best = ("시작 노드 없음", 99)
        out_rows.append({"src": src, "q": q, "case": case, "item": item, "intent": intent, "start": start, "tier": tier,
                         "group": best[0], "hop": best[1], "edges1": e1, "unknown": unknown})

    def table(rows):
        by_int: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
        for x in rows:
            by_int[x["intent"] or "-"][x["group"]] += 1
        allc = collections.Counter(x["group"] for x in rows)
        hop = collections.Counter(min(x["hop"], 9) for x in rows)
        return {"n": len(rows), "all": dict(allc.most_common()), "hop": dict(sorted(hop.items())),
                "by_intent": {k: dict(v.most_common()) for k, v in sorted(by_int.items())}}

    with_hit = [x for x in out_rows if x["group"] not in ("골드에 없음", "시작 노드 없음")]
    return {"rows_total": len(out_rows), "rows_with_gold_hit": len(with_hit),
            "v4": table([x for x in with_hit if x["src"] == "v4"]), "v3": table([x for x in with_hit if x["src"] == "v3"]),
            "both": table(with_hit),
            "v4_case3_unknown": table([x for x in with_hit if x["src"] == "v4" and x["case"] == "case3" and x["unknown"]]),
            "rows": out_rows}


NEIGHBOR_GROUPS = ("부위 위험", "금기 조건", "쌍 관계", "조합", "계열", "합병증", "고민 관계", "제품", "부위", "근거")  # 발주서 다섯 먼저 = 동점 깨기 순
GROUP_EDGES = {g: sorted(k for k, v in EDGE_GROUP.items() if v == g) for g in NEIGHBOR_GROUPS}
ORDER_MIN_N = 10  # 의도 행이 이보다 적으면 전체 분포를 씀
ORDER_TOP = 3


def order_table(ak: dict) -> dict:
    """의도별 첫 걸음 이웃 종류 순서 — 결정론 규칙: 셈 내림차순 · 동점은 전체 셈 · 그다음 NEIGHBOR_GROUPS 순 · 위 3."""
    allc = ak["both"]["all"]

    def rank(c: dict) -> list[str]:
        gs = [g for g in NEIGHBOR_GROUPS if c.get(g, 0) > 0]
        return sorted(gs, key=lambda g: (-c.get(g, 0), -allc.get(g, 0), NEIGHBOR_GROUPS.index(g)))[:ORDER_TOP]

    out = {"_all": {"n": ak["both"]["n"], "order": rank(allc), "section_rows": allc.get("섹션(시작 노드)", 0)}}
    for it, c in ak["both"]["by_intent"].items():
        n = sum(c.values())
        src = c if n >= ORDER_MIN_N else allc
        out[it] = {"n": n, "source": "intent" if n >= ORDER_MIN_N else "_all", "order": rank(src),
                   "section_rows": c.get("섹션(시작 노드)", 0), "section_rank1": max(c, key=lambda g: (c[g], g)) == "섹션(시작 노드)"}
    return {"rule": f"n ≥ {ORDER_MIN_N} 이면 그 의도 · 아니면 전체 · 셈 내림차순 · 동점 = 전체 셈 → {NEIGHBOR_GROUPS} 순 · 위 {ORDER_TOP}",
            "group_edges": GROUP_EDGES, "table": out}


COVER = 0.9   # v2.3 — 의도별 1홉 행의 이 비율을 덮을 때까지 edge kind 를 넣음
KIND_MIN = 3


def order_table_v23(ak: dict) -> dict:
    """v2.3 첫 걸음 이웃 edge kind 표 — 1홉 행(461 중 hop 1)의 edge kind 셈 · 의도 행 ≥ ORDER_MIN_N 이면 그 의도 · 아니면 전체 ·
    셈 내림차순(동점 = 전체 셈 → 이름) 으로 넣어 가며 그 의도 1홉 행의 COVER 를 덮으면 멈춤(최소 KIND_MIN)."""
    rows = [x for x in ak["rows"] if x["group"] not in ("골드에 없음", "시작 노드 없음") and x["hop"] == 1 and x["edges1"]]
    allc = collections.Counter(e for x in rows for e in x["edges1"])

    def pick(rs, c):
        out, cov = [], set()
        for e in sorted(c, key=lambda e: (-c[e], -allc[e], e)):
            if len(out) >= KIND_MIN and len(cov) >= COVER * len(rs):
                break
            out.append(e)
            cov |= {i for i, x in enumerate(rs) if e in x["edges1"]}
        return out, len(cov)

    by = collections.defaultdict(list)
    for x in rows:
        by[x["intent"] or "-"].append(x)
    o_all, cov_all = pick(rows, allc)
    table = {"_all": {"n1": len(rows), "kinds": o_all, "covered": cov_all, "counts": dict(allc.most_common())}}
    for it, rs in sorted(by.items()):
        if len(rs) >= ORDER_MIN_N:
            c = collections.Counter(e for x in rs for e in x["edges1"])
            ks, cv = pick(rs, c)
            table[it] = {"n1": len(rs), "source": "intent", "kinds": ks, "covered": cv, "counts": dict(c.most_common())}
        else:
            cv = sum(1 for x in rs if set(x["edges1"]) & set(o_all))
            table[it] = {"n1": len(rs), "source": "_all", "kinds": o_all, "covered": cv}
    sec_first = {it: (ak["both"]["by_intent"].get(it, {}) and max(ak["both"]["by_intent"][it], key=lambda g: (ak["both"]["by_intent"][it][g], g)) == "섹션(시작 노드)")
                 for it in table if it != "_all"}
    return {"rule": f"1홉 행 edge kind 셈 · n ≥ {ORDER_MIN_N} 이면 그 의도 · 아니면 전체 · 내림차순(동점 = 전체 셈 → 이름) · 1홉 행 {COVER:.0%} 덮을 때까지(최소 {KIND_MIN})",
            "table": table, "first_section_max_2": sorted(k for k, v in sec_first.items() if v)}


def short_replay(gold: Gold, v4: dict[str, dict]) -> dict:
    """기록된 expand 호출을 짧은 꼴로 다시 셈(같은 fact · 원문 앞 N자) — v3.3 꼴 전제의 추정."""
    def short_bytes(fids, n):
        facts = []
        for fid in fids:
            f = gold.facts.get(fid)
            text = f["text"] if f else ""
            facts.append({"id": fid, "line": text[:n], "section": (f or {}).get("section"), "owner": (f or {}).get("owner_id")})
        return jb({"facts": facts, "more": 0})

    res = {}
    for n in LINE_NS:
        per_call, ratio, step1_left, = [], [], {b: [] for b in BUDGETS}
        for r in v4.values():
            w = r["cases"]["case3"]["trace"]["walk"]
            if w.get("fallback") or not w["steps"]:
                continue
            s1 = 0
            for i, s in enumerate(w["steps"]):
                for c in (s.get("expand") or {}).get("calls") or []:
                    sb = short_bytes(c.get("fact_ids") or [], n)
                    per_call.append(sb)
                    if c.get("bytes"):
                        ratio.append(sb / c["bytes"])
                    if i == 0:
                        s1 += sb
            for b in BUDGETS:
                step1_left[b].append(b - s1)
        res[str(n)] = {"calls": len(per_call), "short_median": med(per_call), "short_p95": pct(per_call, 0.95),
                       "short_max": max(per_call), "ratio_median": round(med(ratio), 3),
                       "step1_all_calls_left": {str(b): {"median": med(v), "lt0": sum(1 for x in v if x < 0)} for b, v in step1_left.items()}}
    return res


NB_SLIM_B = 300  # 이웃 slim 카드 1장 가정 바이트(v3.3 실측 전 · WORK-009 T-2 가 실측으로 바꿈)


def step_budget(gold: Gold, v4: dict[str, dict], n: int = 80) -> dict:
    """새 걸음 규칙(첫 걸음 = 이웃 ≤3 slim + 섹션 ≤1 · 뒤 걸음 = 섹션 ≤ cap)의 예산 추정 · 「충분」 Noul 분포 · 되돌아감 사유."""
    def sb(ids):
        return jb({"facts": [{"id": i, "line": (gold.facts.get(i) or {}).get("text", "")[:n], "section": (gold.facts.get(i) or {}).get("section"),
                              "owner": (gold.facts.get(i) or {}).get("owner_id")} for i in ids], "more": 0})
    sec_calls, enough, fb, fullb, nfacts = [], collections.defaultdict(list), collections.Counter(), [], []
    for r in v4.values():
        w = r["cases"]["case3"]["trace"]["walk"]
        for s in w["steps"]:
            j = s.get("jev") or {}
            if "enough" in j:
                enough[s["k"]].append(j["enough"])
            for c in (s.get("expand") or {}).get("calls") or []:
                if c.get("sections"):
                    sec_calls.append(sb(c.get("fact_ids") or []))
        if w.get("fallback"):
            st0 = w["steps"][0] if w["steps"] else {}
            fb[f"{w['fallback_reason']}/{w['stop']}/steps{len(w['steps'])}" + ("/step1_first_call_excluded" if (
                (st0.get("expand") or {}).get("calls") or [{}])[0].get("excluded") else "")] += 1
            continue
        nfacts.append(len(w["fact_ids"]))
        fullb.append(sum(jb({"id": i, "text": (gold.facts.get(i) or {}).get("text", "")}) for i in w["fact_ids"]))
    m, p95 = med(sec_calls), pct(sec_calls, 0.95)
    est = {}
    for cap in (1, 2, 3):
        first_m, first_p = 3 * NB_SLIM_B + m, 3 * NB_SLIM_B + p95
        est[str(cap)] = {"first_step_median": first_m, "later_step_median": cap * m, "walk4_median": first_m + 3 * cap * m,
                         "walk4_p95": first_p + 3 * cap * p95}
    return {"line_n": n, "nb_slim_assumed_b": NB_SLIM_B, "section_call_short": {"n": len(sec_calls), "median": m, "p95": p95},
            "walk4_by_sections_per_step": est,
            "enough_noul_by_step": {str(k): {"n": len(v), "median": med(v), "ge_0.5": sum(x >= 0.5 for x in v), "ge_0.3": sum(x >= 0.3 for x in v)}
                                    for k, v in sorted(enough.items())},
            "fallback_reasons": dict(sorted(fb.items())),
            "collected_facts_per_walk": {"median": med(nfacts), "p95": pct(nfacts, 0.95)},
            "collected_full_text_bytes_per_walk": {"median": med(fullb), "p95": pct(fullb, 0.95), "max": max(fullb)}}


def stray(v4: dict[str, dict]) -> dict:
    rows = []
    for q, r in sorted(v4.items()):
        tc = r["cases"]["case2"]["trace"]["tool_calls"]
        for i, c in enumerate(tc):
            if not c.get("stray"):
                continue
            nx = tc[i + 1] if i + 1 < len(tc) else {}
            inp = c.get("input") or {}
            rows.append({"q": q, "idx": i, "n_calls": len(tc), "name": c["tool"], "err_bytes": c["output_bytes"],
                         "bytes_eq_64_plus_name": c["output_bytes"] == 64 + len(c["tool"]),
                         "prev": tc[i - 1]["tool"] if i else None, "next": nx.get("tool"), "next_ok": nx.get("is_error") is False,
                         "input_shape": "empty" if not inp else ("stringified_array" if any(isinstance(v, str) and v.startswith("[") for v in inp.values()) else "normal"),
                         "cli_version": r["versions"].get("cli_version"), "prompt_case2": r["versions"]["prompts"]["case2"]})
    calls = sum(len(r["cases"]["case2"]["trace"]["tool_calls"]) for r in v4.values())
    return {"n": len(rows), "case2_calls": calls, "questions": len({x["q"] for x in rows}),
            "bytes_rule_all": all(x["bytes_eq_64_plus_name"] for x in rows),
            "next_same_name": sum(1 for x in rows if x["next"] == x["name"] or x["name"].startswith(x["next"] or "\0")),
            "input_shape": dict(collections.Counter(x["input_shape"] for x in rows)),
            "prev": dict(collections.Counter(x["prev"] for x in rows)), "rows": rows}


def md(d: dict) -> str:
    L = ["# SPEC-006 v2.2 · v2.3 근거 셈(spec006-v22-count.py · 결정론)", "",
         f"배치 rerun-v4 `{V4}` · rerun-v3 `{V3}` · gold-export `{d['export_hash']}`", ""]
    a = d["walk"]
    L += ["## A. 걸음 해부(case3)", "", "```json", json.dumps({k: v for k, v in a.items() if k != "section_call_bytes"}, ensure_ascii=False, indent=1), "```", "",
          "| 섹션(단독 expand 호출) | n | 중앙 B | p95 | 최대 |", "|---|---|---|---|---|"]
    for k, v in a["section_call_bytes"].items():
        L.append(f"| {k} | {v['n']} | {v['median']} | {v['p95']} | {v['max']} |")
    b = d["answer_kinds"]
    L += ["", "## B. 답이 산 곳(실패 행 인용 → 골드 hit · 시작 노드 기준 가장 가까운 것)", "",
          f"행 {b['rows_total']} · 골드 hit {b['rows_with_gold_hit']}", ""]
    for key in ("both", "v4", "v3", "v4_case3_unknown"):
        t = b[key]
        L += [f"### {key} (n={t['n']})", "", "전체: " + " · ".join(f"{k} {v}" for k, v in t["all"].items()), "",
              "홉: " + " · ".join(f"{k}:{v}" for k, v in t["hop"].items()), "", "| 의도 | 분포 |", "|---|---|"]
        for it, c in t["by_intent"].items():
            L.append(f"| {it} | " + " · ".join(f"{k} {v}" for k, v in c.items()) + " |")
        L.append("")
    o = d["order"]
    L += ["### 의도별 첫 걸음 이웃 종류 순서(결정론 규칙)", "", o["rule"], "", "| 의도 | 행 | 근거 | 순서 | 섹션 행 | 섹션 1위 |", "|---|---|---|---|---|---|"]
    for it, x in o["table"].items():
        L.append(f"| {it} | {x['n']} | {x.get('source', '-')} | {' → '.join(x['order'])} | {x['section_rows']} | {x.get('section_rank1', '-')} |")
    L += [""]
    o3 = d["order_v23"]
    L += ["### v2.3 첫 걸음 이웃 edge kind 표", "", o3["rule"], "", f"섹션 상한 2 의도(시작 노드 섹션이 1위): {o3['first_section_max_2']}", "",
          "| 의도 | 1홉 행 | 근거 | edge kind(순서) | 덮음 |", "|---|---|---|---|---|"]
    for it, x in o3["table"].items():
        L.append(f"| {it} | {x['n1']} | {x.get('source', '-')} | {' → '.join(x['kinds'])} | {x['covered']} |")
    L += [""]
    L += ["## C. 짧은 꼴 재생(기록된 expand 호출 · 같은 fact)", "", "```json", json.dumps(d["short"], ensure_ascii=False, indent=1), "```", "",
          "### 새 걸음 규칙 예산 추정 · 「충분」 · 되돌아감", "", "```json", json.dumps(d["budget"], ensure_ascii=False, indent=1), "```", "",
          "## D. stray", "", "```json", json.dumps({k: v for k, v in d["stray"].items() if k != "rows"}, ensure_ascii=False, indent=1), "```", "",
          "| 문항 | 차례 | 이름 | 오류 B | =64+len | 직전 | 다음 | 다음 성공 | 입력 꼴 |", "|---|---|---|---|---|---|---|---|---|"]
    for x in d["stray"]["rows"]:
        L.append(f"| {x['q']} | {x['idx'] + 1}/{x['n_calls']} | {x['name']} | {x['err_bytes']} | {x['bytes_eq_64_plus_name']} | {x['prev']} | {x['next']} | {x['next_ok']} | {x['input_shape']} |")
    return "\n".join(L) + "\n"


def main() -> None:
    v4 = load(V4)
    tri = json.loads(TRIAGE2.read_text(encoding="utf-8"))
    gold = Gold(EXPORT)
    graph = Graph(gold)
    ak = answer_kinds(gold, graph, v4, tri)
    d = {"export_hash": gold.hash, "walk": walk_anatomy(v4), "answer_kinds": ak, "order": order_table(ak), "order_v23": order_table_v23(ak),
         "short": short_replay(gold, v4), "budget": step_budget(gold, v4), "stray": stray(v4)}
    OUT.with_suffix(".json").write_text(json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    OUT.with_suffix(".md").write_text(md(d), encoding="utf-8")


if __name__ == "__main__":
    main()
