"""「핵심 수치 카드」(key_facts) 설계 측정 — 읽기만 · 결정론 · LLM 없음.

입력: 골드 export(567677ed) · runs.jsonl(rerun-v6a b202611011935-f9a211 case3) · quality.jsonl(같은 배치 판정) · recheck2.py(Gold.gold_match · norm 빌림)
출력: keycard-measure.json (시간 칸 없음 · 두 번 같음)
1. v6a case3 정확성 실패 분류 — 걷기가 받음(답이 안 씀) · 골드에 있는데 못 받음 · 골드 fact 없음
2. 카드 고르기(아래 SLOTS · 결정론) — 시술 노드(단위 · 제품 · 계열) 전부의 카드 · 크기 분포
3. 「골드에 있는데 못 받음」 행 중 카드로 닿는 행 — 카드 노드 = 그 판 walk.required.nodes(rank 상위 3) ∪ 시작 노드(시술이면)
"""
import collections
import json
import re
import sys
from pathlib import Path

W = Path(__file__).resolve().parent
E = W.parents[2] / "reference" / "2026-10-30-hub-evals"
GOLD = Path("/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend/build-out/gold-export.json")
V6A = "b202611011935-f9a211"
sys.path.insert(0, str(E / "fail-triage-scripts"))
from recheck2 import Gold, norm  # noqa: E402

LINE = 80  # 카드 한 줄 글자 상한(넘으면 앞 79 + 「…」 · cut)

# 칸 → (같은 노드에서 찾는 fact 꼴 — 위에서부터 먼저) · 정규식은 fact id 의 마지막 칸 경로 또는 원문
SLOTS = [
    ("onset", [("id", r"onset_duration\.onset\]?$")]),
    ("duration", [("id", r"onset_duration\.duration\]?$"), ("id", r"\.duration_simple$")]),
    ("downtime", [("id", r"\.downtime$")]),
    ("interval", [("id", r"onset_duration\.(maintenance)\]?$"), ("text_in", ("aftercare", "recovery", "overview"), r"(간격|주기)")]),
    ("sessions", [("text_in", ("recovery", "overview", "aftercare", "timeline"), r"\d+\s*(?:[-~]\s*\d+\s*)?회")]),
    ("price_range", [("id", r"#market#market\[")]),
    ("anesthesia", [("id", r"#ops#ops\.anesthesia_ko$"), ("id", r"#ops#ops\.needsAnesthesia$")]),
    ("pain", [("id", r"\.pain_level$")]),
]


def main():
    g = json.loads(GOLD.read_text(encoding="utf-8"))
    nodes = {n["id"]: n for n in g["nodes"]}
    by_owner = collections.defaultdict(list)
    for f in g["facts"]:
        by_owner[f["owner_id"]].append(f)
    for v in by_owner.values():
        v.sort(key=lambda f: (0 if "#step9[" in f["id"] else 1, f["id"]))  # 9단계(resolved 만 실림) 먼저 · id 순

    def family_of(nid):
        n = nodes.get(nid) or {}
        a = n.get("attrs") or {}
        fam = (a.get("gold") or {}).get("family") or ((a.get("silver") or {}).get("key") or {}).get("family")
        if isinstance(fam, list):
            fam = fam[0] if fam else None
        if fam and not str(fam).startswith("family:"):
            fam = f"family:{fam}"
        if not fam and n.get("kind") == "product":
            fs = (a.get("gold") or {}).get("families") or []
            fam = fs[0] if fs else None
        return fam

    def pick(nid, rules):
        for kind, *rest in rules:
            for f in by_owner.get(nid, []):
                if kind == "id" and re.search(rest[0], f["id"]):
                    return f
                if kind == "text_in" and f["section"] in rest[0] and re.search(rest[1], f["text"]):
                    return f
        return None

    def card(nid):
        out = {}
        chain = [nid] + ([family_of(nid)] if nodes.get(nid, {}).get("kind") in ("unit_procedure", "product") and family_of(nid) else [])
        for slot, rules in SLOTS:
            hit, src = None, None
            for i, x in enumerate(chain):
                hit = pick(x, rules)
                if hit:
                    src = "자기" if i == 0 else "계열"
                    break
            if hit:
                t = " ".join(hit["text"].split())
                out[slot] = {"id": hit["id"], "line": t if len(t) <= LINE else t[:LINE - 1] + "…", **({"cut": True} if len(t) > LINE else {}), "from": src}
            else:
                out[slot] = None
        return out

    def size(c):
        body = {"node": "x" * 30, "key_facts": {k: ({kk: vv for kk, vv in v.items() if kk != "from"} if v else None) for k, v in c.items()}}
        return len(json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode())

    proc = sorted(n for n, x in nodes.items() if x["kind"] in ("unit_procedure", "product", "family"))
    cards = {n: card(n) for n in proc}
    sizes = sorted(size(c) for c in cards.values())
    fill = collections.Counter()
    for n, c in cards.items():
        for k, v in c.items():
            fill[(nodes[n]["kind"], k, "빔" if v is None else v["from"])] += 1

    # 1. v6a 실패 분류
    gold = Gold(GOLD)
    runs = {}
    for line in (E / "runs" / "runs.jsonl").open(encoding="utf-8"):
        r = json.loads(line)
        if r.get("batch_id") == V6A:
            runs[r["run_id"]] = r
    rows = []
    for line in (E / "runs" / "quality.jsonl").open(encoding="utf-8"):
        q = json.loads(line)
        if q.get("run_id") not in runs or q.get("case") != "case3":
            continue
        w = runs[q["run_id"]]["cases"]["case3"]["trace"].get("walk") or {}
        got = set(w.get("fact_ids") or []) | set((w.get("required") or {}).get("fact_ids") or []) | set((w.get("full") or {}).get("fact_ids") or []) \
            | set((w.get("fixed") or {}).get("fact_ids") or []) if isinstance(w.get("fixed"), dict) else set(w.get("fact_ids") or []) | set((w.get("required") or {}).get("fact_ids") or []) | set((w.get("full") or {}).get("fact_ids") or [])
        for f in q["judge"].get("failures") or []:
            if f["item"] != "accuracy":
                continue
            qt = norm((f.get("evidence") or {}).get("quote") or "")
            tier, hits = gold.gold_match(qt) if len(qt) >= 2 else (None, [])
            fids = sorted({h[2]["fact_id"] for h in hits if h[1] == "fact"})
            if fids and set(fids) & got:
                cls = "걷기가 받음(답이 안 씀)"
            elif fids:
                cls = "골드에 있는데 못 받음"
            else:
                cls = "골드 fact 없음"
            start = w.get("start_node")
            req = list((w.get("required") or {}).get("nodes") or [])
            cnodes = sorted(set(req) | ({start} if start in cards else set()))
            cfacts = {v["id"]: (n, k) for n in cnodes for k, v in cards.get(n, {}).items() if v}
            reach = sorted({cfacts[x][1] for x in fids if x in cfacts})
            # 넓힌 셈(참고): 카드 노드 = 그 판에서 받은 노드 전부(걸음 · 필수 · 시작)
            seen = set(cnodes) | {s.get("node") for s in w.get("steps") or [] if s.get("node") in cards}
            wide = {v["id"] for n in seen for v in cards.get(n, {}).values() if v}
            rows.append({"no": q["question_no"], "path": (f.get("evidence") or {}).get("path"), "class": cls, "fact_ids": fids[:6],
                         "card_nodes": cnodes, "card_reach": bool(reach), "card_slots": reach, "card_reach_wide": bool(set(fids) & wide),
                         "fact_kinds": sorted({re.sub(r"\[[^\]]*\]", "[]", x.split("#")[-1])[:40] for x in fids})[:4]})
    miss = [r for r in rows if r["class"] == "골드에 있는데 못 받음"]
    out = {
        "meta": {"gold_build": g["build"]["build_hash"], "v6a": V6A, "slots": [s for s, _ in SLOTS], "line_chars": LINE},
        "classes": dict(sorted(collections.Counter(r["class"] for r in rows).items())), "rows": len(rows),
        "miss_card_reach": sum(r["card_reach"] for r in miss), "miss_card_reach_wide": sum(r["card_reach_wide"] for r in miss),
        "miss_card_slots": dict(sorted(collections.Counter(s for r in miss for s in r["card_slots"]).items())),
        "card_size": {"n": len(sizes), "median": sizes[len(sizes) // 2], "p95": sizes[int(len(sizes) * 0.95) - 1], "max": sizes[-1]},
        "card_fill": {f"{a} {b} {c}": v for (a, b, c), v in sorted(fill.items())},
        "detail": rows,
    }
    (W / "keycard-measure.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in out.items() if k not in ("detail", "card_fill")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
