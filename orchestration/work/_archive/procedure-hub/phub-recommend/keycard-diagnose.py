"""keycard 측정 61행 진단 — 읽기만 · 결정론. keycard-measure.json(행 · 분류) + 골드 export(567677ed) + runs(v6a) → keycard-measure.md

행마다(「골드에 있는데 못 받음」) hit fact 중 가장 가까운 것 기준:
- 그 fact 를 내는 노드(serving) = owner ∪ attached_to ∪ (owner 가 계열이면 그 계열 단위 시술 — 단위 expand 가 계열 수준 section 을 같이 냄) ∪ (owner 가 엣지 · 조합이면 양끝 · 구성 노드)
- 방문 = serving 노드가 그 판의 걸음 노드(steps[].node) · 필수 묶음 노드(required.nodes)에 있음
  - 방문 · 그 section 을 받음(expand.sections 또는 필수 묶음 calls) · 그래도 fact 없음 = 1쪽 밖(more)
  - 방문 · 그 section 안 받음 = Jev 가 안 고름(peek 에는 그 section 이 떴음 — serving 노드에 그 section fact 가 있으므로)
- 안 방문 = 시작 노드에서 serving 노드까지 최단 홉(골드 엣지 · 방향 무관 · candidates 끝 풀기 · 6홉까지)
"""
import collections
import json
import re
from pathlib import Path

W = Path(__file__).resolve().parent
E = W.parents[2] / "reference" / "2026-10-30-hub-evals"
GOLD = Path("/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend/build-out/gold-export.json")
V6A = "b202611011935-f9a211"


def main():
    m = json.loads((W / "keycard-measure.json").read_text(encoding="utf-8"))
    g = json.loads(GOLD.read_text(encoding="utf-8"))
    F = {f["id"]: f for f in g["facts"]}
    nodes = {n["id"]: n for n in g["nodes"]}
    edges = {e["id"]: e for e in g["edges"]}
    adj = collections.defaultdict(set)
    for e in g["edges"]:
        a, z = e["from_id"], e["to_id"] or ""
        for z_ in (z[11:].split("|") if z.startswith("candidates:") else [z]):
            if a in nodes and z_ in nodes:
                adj[a].add(z_)
                adj[z_].add(a)
    units_of = collections.defaultdict(set)
    for n, x in nodes.items():
        if x["kind"] == "unit_procedure":
            fam = ((x.get("attrs") or {}).get("silver") or {}).get("key", {}).get("family")
            if fam:
                units_of[f"family:{fam}"].add(n)

    def serving(fid):
        f = F[fid]
        o = f["owner_id"]
        s = {o} | set(f.get("attached_to") or [])
        if o.startswith("family:"):
            s |= units_of.get(o, set())
        if o in edges:
            s |= {edges[o]["from_id"], edges[o]["to_id"]}
        if o.startswith("combo:"):
            s |= adj.get(o, set())
        return {x for x in s if x in nodes}

    def hops(src, dst, cap=6):
        if not src or not dst:
            return None
        seen, fr = set(src), list(src)
        for d in range(cap + 1):
            if seen & dst:
                return d
            nx = []
            for x in fr:
                for y in adj.get(x, ()):
                    if y not in seen:
                        seen.add(y)
                        nx.append(y)
            fr = nx
        return None

    runs = {}
    for line in (E / "runs" / "runs.jsonl").open(encoding="utf-8"):
        r = json.loads(line)
        if r.get("batch_id") == V6A:
            runs[r["question_no"]] = r
    miss = [r for r in m["detail"] if r["class"] == "골드에 있는데 못 받음"]
    out_rows = []
    for r in miss:
        w = runs[r["no"]]["cases"]["case3"]["trace"].get("walk") or {}
        got_sec = collections.defaultdict(set)
        visited = set()
        for s in w.get("steps") or []:
            visited.add(s.get("node"))
            for sec in (s.get("expand") or {}).get("sections") or []:
                got_sec[s.get("node")].add(sec)
        for c in (w.get("required") or {}).get("calls") or []:
            visited.add(c.get("node"))
            for sec in c.get("sections") or []:
                got_sec[c.get("node")].add(sec)
        visited.discard(None)
        best = None
        for fid in r["fact_ids"]:
            if fid not in F:
                continue
            f = F[fid]
            sv = serving(fid)
            vis = sv & visited
            if vis:
                took = [n for n in vis if f["section"] in got_sec.get(n, set())]
                tag = "방문 · section 받음 · 1쪽 밖(more)" if took else "방문 · Jev 가 그 section 안 고름(peek 엔 떴음)"
                rank = 0 if took else 1
                h = 0
            else:
                h = hops([w.get("start_node")] if w.get("start_node") else [], sv)
                tag = f"안 방문 · 시작에서 {h}홉" if h is not None else "안 방문 · 6홉 밖 · 연결 없음"
                rank = 2 + (h if h is not None else 9)
            cand = (rank, fid, tag, f["section"], f["owner_id"].split(":")[0], h)
            if best is None or cand < best:
                best = cand
        if best is None:
            continue
        out_rows.append({"no": r["no"], "path": r["path"], "fact": best[1], "section": best[3], "owner_kind": best[4], "diag": best[2], "hops": best[5],
                         "start": w.get("start_node"), "intent": w.get("intent"), "stop": w.get("stop")})
    C = collections.Counter
    sec = C(x["section"] for x in out_rows)
    own = C(x["owner_kind"] for x in out_rows)
    diag = C(re.sub(r"\d홉", lambda mm: mm.group(0), x["diag"]) for x in out_rows)
    by_sec_diag = C((x["section"], x["diag"].split(" · ")[0] + (" · " + x["diag"].split(" · ")[1] if x["diag"].startswith("방문") else "")) for x in out_rows)
    res = {"rows": len(out_rows), "section": dict(sec.most_common()), "owner_kind": dict(own.most_common()), "diag": dict(diag.most_common()),
           "detail": out_rows}
    (W / "keycard-diagnose.json").write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    L = ["# keycard 측정 — v6a case3 정확성 실패 진단(스펙 작성 안 함 · 코디 11-01)", "",
         f"> `keycard-measure.py` · `keycard-diagnose.py`(읽기만 · 결정론) · 골드 `{m['meta']['gold_build']}` · rerun-v6a `{V6A}` case3 · 판정 = recheck2 `gold_match`(fact hit) ∩ 받은 fact(walk.fact_ids ∪ required ∪ full). 원장 인용 없음(fact id · 경로 · 셈만).", "",
         "## 1. 분류", "", "| 분류 | 행 |", "|---|---|"] + [f"| {k} | {v} |" for k, v in m["classes"].items()] + [f"| 합 | {m['rows']} |", "",
         "- 코디 셈(65 · 받았는데 안 씀 0 · 못 받음 45)은 키워드 기준이었고 이 셈과 식이 다르다(코디 확인 11-01 — 이 셈이 맞음)", "",
         "## 2. 핵심 수치 카드로 닿는가(스펙 멈춤의 근거)", "",
         f"- 카드 = 시술 노드마다 칸 8(onset · duration · downtime · interval · sessions · price_range · anesthesia · pain) · 칸당 fact 1(자기 → 계열 · 9단계 먼저) · 카드 노드 = 그 판의 필수 묶음 노드(rank 상위 3) ∪ 시작 노드",
         f"- 「골드에 있는데 못 받음」 {len(miss)} 중 **카드로 닿음 {m['miss_card_reach']}**(칸: " + " · ".join(f"{k} {v}" for k, v in m["miss_card_slots"].items()) + f") · 상한(칸 후보 fact 전부 · 자기 + 계열) **8** · 핵심 수치 칸에 해당하는 fact 자체가 10행뿐",
         f"- 카드 크기(전 시술 노드 {m['card_size']['n']} · 줄 80자): 중앙 {m['card_size']['median']:,}B · p95 {m['card_size']['p95']:,} · 최대 {m['card_size']['max']:,} — ≤ 1KB 면 줄 40자로 줄여야 함", "",
         f"## 3. 못 받은 {len(out_rows)}행 — 무엇을 못 받았나", "", "### section", "", "| section | 행 |", "|---|---|"] + [f"| {k} | {v} |" for k, v in sec.most_common()] + [
         "", "### fact 를 가진 노드 종류(owner)", "", "| 종류 | 행 |", "|---|---|"] + [f"| {k} | {v} |" for k, v in own.most_common()] + [
         "", "## 4. 왜 못 받았나(걸음 기록 대조)", "", "| 진단 | 행 |", "|---|---|"] + [f"| {k} | {v} |" for k, v in diag.most_common()] + [
         "", "- 「방문」 = fact 를 내는 노드(owner · attached_to · 계열 fact 면 그 계열 단위 시술 · 엣지 · 조합이면 양끝 · 구성)가 걸음 노드 또는 필수 묶음 노드 · 「peek 엔 떴음」 = 그 노드에 그 section fact 가 있으므로 peek `sections[]` 에 나옴 · 「1쪽 밖」 = 그 section 을 받았는데 12줄 밖",
         "", "### section × 진단", "", "| section | 진단 | 행 |", "|---|---|---|"] + [f"| {a} | {b} | {v} |" for (a, b), v in sorted(by_sec_diag.items(), key=lambda kv: (-kv[1], kv[0]))] + [
         "", "## 5. 행 목록", "", "| 문항 | 원장 경로 | fact | section | 노드 | 진단 | 시작 노드 | 의도 | 멈춤 |", "|---|---|---|---|---|---|---|---|---|"] + [
         f"| {x['no']} | `{x['path']}` | `{x['fact'][:70]}` | {x['section']} | {x['owner_kind']} | {x['diag']} | {x['start']} | {x['intent']} | {x['stop']} |" for x in out_rows] + [""]
    (W / "keycard-measure.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in res.items() if k != "detail"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
