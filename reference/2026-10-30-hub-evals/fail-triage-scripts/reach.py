#!/usr/bin/env python3
"""reach — SPEC-005 v3.2 §6-6 걸음 도달 측정(결정론 BFS · LLM 없음 · WORK-007).

B 186(2차 분류 `fail-triage2.json b_rows`)의 fact 에 Jev 재귀 탐색(peek → expand)이 걸음 4 안에 닿을 수 있는지를 골드 export 그래프의 경로 길이로 센다.
- 시작 노드 S = case3 `trace.hub.resolve.candidates ∪ menu_candidates`(메뉴는 그 라벨의 추천 패키지 조합 · dictionary 의 menu 표) ·
  허브 안 부른 문항(X0 · resolve 없음)은 그 문항 질문을 T1 resolve 로(in-process · 결정론) 돌린 candidates
- 걸음 1 = S 의 노드 n 을 peek → expand(sections)로 n 이 owner 또는 attached_to 인 fact 전부(상한 밖은 more_ids → fact_ids 로 같은 걸음)
- 걸음 +1 = 이웃으로 옮김 — 엣지 = 골드 엣지 전부(저장 + 펼친 · candidates: 끝은 후보 전부 · 조건부(default_out ∧ conditional)는 제외) · 방향 무관
- d(f) = min over s ∈ S of (s → owner/attached 노드 최단 홉 + 1) · 엣지 속성 fact(owner 가 엣지)는 양끝 중 가까운 쪽 · scope:all 은 attached_to · 전역(G16 · 붙은 노드 없는 scope:all)은 1
- 행의 fact = 새 export 로 gold_match 한 hit(fact · 엣지 속성 · 노드 속성 · 노드 이름)의 최소 d
산출 `build-out/recheck2/reach-report.{md,json}`(baseline 은 옛 export · `reach-report.baseline.*`). 시간 칸은 meta.ran_at 하나.
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import recheck2 as R  # noqa: E402  (같은 폴더 · 판정 식 · 입력 로더 공유)

E, BACKEND, OUT, BATCH = R.E, R.BACKEND, R.OUT, R.BATCH
MAX_D = 4


class Graph:
    def __init__(self, export: Path) -> None:
        g = json.loads(export.read_text(encoding="utf-8"))
        self.hash = g["build"]["build_hash"]
        self.nodes = {n["id"]: n for n in g["nodes"]}
        self.facts = {f["id"]: f for f in g["facts"]}
        self.edges = {e["id"]: e for e in g["edges"]}
        self.adj: dict[str, set[str]] = collections.defaultdict(set)
        self.excluded_conditional = 0
        for e in g["edges"]:
            if e.get("default_out") and "conditional" in (e.get("flags") or []):
                self.excluded_conditional += 1
                continue
            a, b = ends(e["from_id"]), ends(e["to_id"])
            for x in a:
                for y in b:
                    if x in self.nodes and y in self.nodes:
                        self.adj[x].add(y)
                        self.adj[y].add(x)
        self.menu: dict[str, list[str]] = {}
        for d in g.get("dictionary") or []:
            for m in (d.get("targets") or {}).get("menu") or []:
                self.menu[m["label"]] = m["combos"]
        if not self.menu:  # export 에 dictionary 가 없으면 추천 패키지 anchor.source_label 로
            for n in g["nodes"]:
                if n["kind"] == "combo":
                    lab = ((n["attrs"].get("silver") or {}).get("anchor") or {}).get("source_label")
                    if lab:
                        self.menu.setdefault(lab, []).append(n["id"])
        self._dist: dict[str, dict[str, int]] = {}

    def dist_from(self, s: str) -> dict[str, int]:
        if s not in self._dist:
            d = {s: 0}
            q = collections.deque([s])
            while q:
                x = q.popleft()
                if d[x] >= MAX_D + 2:
                    continue
                for y in self.adj.get(x, ()):
                    if y not in d:
                        d[y] = d[x] + 1
                        q.append(y)
            self._dist[s] = d
        return self._dist[s]

    def fact_nodes(self, fid: str) -> tuple[list[str], str]:
        """fact 가 닿는 노드 — owner 노드 · attached_to · 엣지 owner 는 양끝 · 전역은 ()."""
        f = self.facts[fid]
        oid = f["owner_id"]
        att = [a for a in (f.get("attached_to") or []) if a in self.nodes]
        if oid in self.nodes:
            return sorted({oid, *att}), "node"
        if oid in self.edges:
            e = self.edges[oid]
            return sorted({*(x for x in ends(e["from_id"]) + ends(e["to_id"]) if x in self.nodes), *att}), "edge"
        if oid.startswith("scope:"):
            if att:
                return att, "scope(attached)"
            keys = [t for t in ((f["source"].get("meta") or {}).get("target_keys") or []) if t in self.nodes]
            return (keys, "scope(target_keys)") if keys else ([], "global")
        if oid.startswith("procedure_relation:") or oid.startswith("site_caution:") or oid.startswith("combo:"):
            m = re.match(r"(procedure_relation:[^#]+)", oid)
            if m and m.group(1) in self.edges:
                e = self.edges[m.group(1)]
                return sorted({*(x for x in ends(e["from_id"]) + ends(e["to_id"]) if x in self.nodes), *att}), "edge"
        return (att, "attached") if att else ([], "no-node")


def ends(x: str | None) -> list[str]:
    if not x:
        return []
    return x[11:].split("|") if x.startswith("candidates:") else [x]


def resolve_inprocess(client: Any, text: str) -> list[str]:
    st, txt = R.rest_call("http://127.0.0.1:18005", "resolve", {"text": text}, client)
    if st != 200:
        return []
    o = json.loads(txt)
    out: list[str] = []
    for m in o.get("matches") or []:
        out += [c["id"] for c in m.get("candidates") or []]
        out += [x["id"] for x in m.get("menu_candidates") or []]
    return list(dict.fromkeys(out))


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--export", type=Path, default=BACKEND / "build-out" / "gold-export.json")
    p.add_argument("--baseline", action="store_true", help="옛 export(d3a1abd5) · reach-report.baseline")
    p.add_argument("--fail-triage2", type=Path, default=E / "build-out" / "fail-triage2.json")
    p.add_argument("--runs", type=Path, default=E / "runs" / "runs.jsonl")
    p.add_argument("--clauses", type=Path, default=OUT / "b186-clauses.json")
    p.add_argument("--inprocess", action="store_true", help="X0 문항의 T1 resolve 를 같은 앱(TestClient)으로(없으면 --base-url)")
    p.add_argument("--base-url", default="http://127.0.0.1:18005")
    p.add_argument("--out-prefix", type=Path, default=None)
    a = p.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    export = (OUT / "gold-export.d3a1abd52f70afe9.json") if a.baseline else a.export
    prefix = a.out_prefix or (OUT / ("reach-report.baseline" if a.baseline else "reach-report"))
    G = Graph(export)
    gold = R.Gold(export)
    runs = R.load_runs(a.runs)
    qrid = {d["question_no"]: rid for rid, d in runs.items()}
    ft = json.loads(a.fail_triage2.read_text(encoding="utf-8"))
    clauses = {(r["question_no"], r["case"], r["item"]): r for r in json.loads(a.clauses.read_text(encoding="utf-8"))["rows"]}
    client = R.inprocess_client() if a.inprocess else None
    meta = {"ran_at": datetime.now(UTC).isoformat(), "export": {"path": str(export), "build_hash": G.hash}, "batch": BATCH, "max_d": MAX_D,
            "edges_excluded_conditional": G.excluded_conditional, "start": "case3 hub.resolve.candidates ∪ menu_candidates(라벨 → 추천 패키지 조합) · X0 는 T1 resolve(" + ("inprocess" if a.inprocess else a.base_url) + ")",
            "rule": "d(f) = min_s(최단 홉(s → owner/attached) + 1) · 엣지 owner 는 양끝 중 가까운 쪽 · scope:all 은 attached_to · 전역(붙은 노드 없음)은 1 · 행 = hit 중 최소 d"}
    start_cache: dict[str, dict[str, Any]] = {}
    rows = []
    for r in ft["b_rows"]:
        rid = qrid[r["question_no"]]
        d = runs[rid]
        if rid not in start_cache:
            hub = (d["cases"]["case3"].get("trace") or {}).get("hub") or {}
            rs = hub.get("resolve") or {}
            cands = list(rs.get("candidates") or [])
            menus = list(rs.get("menu_candidates") or [])
            how = "case3 hub.resolve"
            if not cands and not menus:
                how = "T1 resolve(질문 · X0)"
                for x in resolve_inprocess(client, d["question"]) if (client is not None or not a.inprocess) else []:
                    (menus if x.startswith("menu:") else cands).append(x)
            S = [c for c in cands if c in G.nodes]
            for m in menus:
                S += [c for c in G.menu.get(m.split(":", 1)[1], []) if c in G.nodes]
            start_cache[rid] = {"S": list(dict.fromkeys(S)), "how": how, "candidates": cands, "menus": menus}
        st = start_cache[rid]
        q = R.norm(r["evidence"]["quote"])
        tier, hits = gold.gold_match(q)
        cl = clauses[(r["question_no"], r["case"], r["item"])]
        best: tuple[int | None, str, str] = (None, "", "")
        why = []
        targets: list[tuple[str, list[str], str]] = []
        for ns, k, ref in hits:
            if k == "fact":
                ns_, kind = G.fact_nodes(ref["fact_id"])
                if kind == "global":
                    targets.append((ref["fact_id"], [], "global"))
                else:
                    targets.append((ref["fact_id"], ns_, kind))
            elif k == "edge_attr":
                e = G.edges.get(ref["edge_id"])
                targets.append((ref["edge_id"], [x for x in ends(e["from_id"]) + ends(e["to_id"]) if x in G.nodes] if e else [], "edge_attr"))
            elif k in ("node_attr", "node_name"):
                targets.append((ref["node_id"], [ref["node_id"]], k))
        for tid, ns_, kind in targets:
            if kind == "global":
                if best[0] is None or 1 < best[0]:
                    best = (1, tid, "global")
                continue
            if not ns_:
                why.append(f"{tid}: 붙은 노드 없음({kind})")
                continue
            for s in st["S"]:
                dist = G.dist_from(s)
                for n in ns_:
                    if n in dist:
                        dd = dist[n] + 1
                        if best[0] is None or dd < best[0]:
                            best = (dd, tid, f"{s} → {n} ({dist[n]}홉 · {kind})")
        if best[0] is None:
            reason = "S 가 빔(resolve 후보 없음)" if not st["S"] else ("fact 가 어느 노드에도 안 붙음" if targets and all(not ns_ for _, ns_, k in targets if k != "global") else
                                                             ("골드에 hit 없음" if not targets else f"S 에서 {MAX_D + 2}홉 안 도달 불가"))
            why.append(reason)
        rows.append({"question_no": r["question_no"], "case": r["case"], "item": r["item"], "clause": cl["clause"], "not_closable": cl["not_closable"],
                     "group": R.coarse(r["sub"]), "start_n": len(st["S"]), "start_how": st["how"], "d": best[0], "via": best[2], "target": best[1],
                     "reachable4": best[0] is not None and best[0] <= MAX_D, "why": why[:3]})
    reach = [x for x in rows if not x["not_closable"]]
    ok = sum(1 for x in reach if x["reachable4"])

    def dist_table(rs: list[dict[str, Any]]) -> dict[str, int]:
        c = collections.Counter(("도달 불가" if x["d"] is None else (f"d={x['d']}" if x["d"] <= MAX_D else f"d>{MAX_D}")) for x in rs)
        return {k: c.get(k, 0) for k in ["d=1", "d=2", "d=3", "d=4", f"d>{MAX_D}", "도달 불가"]}

    def by(key: str, rs: list[dict[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = collections.OrderedDict()
        for x in sorted(rs, key=lambda x: str(x[key])):
            g_ = out.setdefault(str(x[key]), {"n": 0, "reach4": 0})
            g_["n"] += 1
            g_["reach4"] += int(x["reachable4"])
        return out
    rate = {"reach161": {"n": len(reach), "reach4": ok, "rate": round(ok / len(reach), 4) if reach else None, "target": 0.9, "pass": bool(reach) and ok / len(reach) >= 0.9},
            "b186": {"n": len(rows), "reach4": sum(1 for x in rows if x["reachable4"]), "rate": round(sum(1 for x in rows if x["reachable4"]) / len(rows), 4)}}
    rep = {"meta": meta, "rate": rate, "dist161": dist_table(reach), "dist186": dist_table(rows), "by_group": by("group", rows), "by_case": by("case", rows),
           "by_clause": by("clause", rows), "unreachable": [x for x in rows if not x["reachable4"]], "rows": rows}
    Path(str(prefix) + ".json").write_text(json.dumps(rep, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    Path(str(prefix) + ".md").write_text(render(rep), encoding="utf-8")
    print(f"reach — export {G.hash} · 161 중 d≤4 {ok}/{len(reach)} ({rate['reach161']['rate']}) · 186 {rate['b186']['reach4']}/186 · 분포 {rep['dist161']} → {prefix}.md")
    return 0


def render(rep: dict[str, Any]) -> str:
    m, r = rep["meta"], rep["rate"]
    L = [f"# reach — 걸음 도달 측정(SPEC-005 v3.2 §6-6)", "",
         f"export `{m['export']['build_hash']}` · 배치 `{m['batch']}` · 시작 노드 = {m['start']} · 조건부 엣지 제외 {m['edges_excluded_conditional']}", f"규칙: {m['rule']}", "",
         "| 기준 | 분모 | d ≤ 4 | 비율 | 목표 | 판정 |", "|---|---|---|---|---|---|",
         f"| 조항 닿는 행 161 | {r['reach161']['n']} | {r['reach161']['reach4']} | {r['reach161']['rate']} | ≥ 0.9 | {'PASS' if r['reach161']['pass'] else 'FAIL'} |",
         f"| B 186 | {r['b186']['n']} | {r['b186']['reach4']} | {r['b186']['rate']} | 보고 | — |", "",
         "## 분포", "", "| 기준 | " + " | ".join(rep["dist161"]) + " |", "|---|" + "---|" * len(rep["dist161"]),
         "| 161 | " + " | ".join(str(v) for v in rep["dist161"].values()) + " |", "| 186 | " + " | ".join(str(v) for v in rep["dist186"].values()) + " |", ""]
    for title, key in (("묶음별", "by_group"), ("케이스별", "by_case"), ("조항별", "by_clause")):
        L += [f"### {title}", "", "| 키 | 행 | d ≤ 4 |", "|---|---|---|"] + [f"| {k} | {v['n']} | {v['reach4']} |" for k, v in rep[key].items()] + [""]
    L += ["## 도달 불가 · 4 밖(사유)", "", "| 문항 | 케이스 | 조항 | 시작 노드 수 | 시작 출처 | d | 사유 · 경로 |", "|---|---|---|---|---|---|---|"]
    for x in rep["unreachable"]:
        L.append(f"| {x['question_no']} | {x['case']} | {x['clause']} | {x['start_n']} | {x['start_how']} | {x['d']} | {'; '.join(x['why']) or x['via']} |")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
