"""실버 9단계(설명 사실) 조사 — 읽기 전용 · 결정론. 원장 · 실버 · 골드 export 를 읽고 step9-research.json 을 쓴다(원장 인용은 work/ 안에만).

실행: python3 step9-research.py   (표준 라이브러리만 · recheck2.py 의 Gold.gold_match 를 빌려 씀 — 판정 식 같음)
"""
from __future__ import annotations

import ast
import collections
import glob
import json
import os
import re
import sys
from pathlib import Path

W = Path(__file__).resolve().parent
RAW = Path("/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26")
GOLD = Path("/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend/build-out/gold-export.json")
E = W.parents[2] / "reference" / "2026-10-30-hub-evals"
V5A = "b202611011627-a76c8e"
sys.path.insert(0, str(E / "fail-triage-scripts"))
from recheck2 import Gold, norm  # noqa: E402  — 판정 식(정규화 · 포함 · 8자) 그대로

CODE = re.compile(r"^([A-Z]{1,2}\d+(-\d+)*|auto-.*)$")
GAP = "정보 없음(gap)"


def leaves(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from leaves(v, f"{p}.{k}" if p else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from leaves(v, f"{p}[{i}]")
    elif isinstance(o, (str, int, float)) and not isinstance(o, bool):
        yield p, str(o)


def pat(p: str) -> str:
    return ".".join("{code}" if CODE.match(x) else x for x in re.sub(r"\[\d+\]", "[]", p).split("."))


raw = {os.path.basename(f)[:-5]: json.load(open(f, encoding="utf-8")) for f in sorted(glob.glob(str(RAW / "*.json")))}
g = json.loads(GOLD.read_text(encoding="utf-8"))
gnodes = {n["id"]: n for n in g["nodes"]}
gold = Gold(GOLD)
s5 = json.loads((W / "step5-units.json").read_text(encoding="utf-8"))
s7 = json.loads((W / "step7-concerns.json").read_text(encoding="utf-8"))
s8 = json.loads((W / "step8-relations.json").read_text(encoding="utf-8"))

# ── 골드 fact 문자열 색인(덮임 셈 — fact 만 · 인용 가능한 자리) ────────────────
FN = [norm(f["text"]) for f in g["facts"]]
FSET = set(FN)
INV: dict[str, set[int]] = collections.defaultdict(set)
for i, s in enumerate(FN):
    if len(s) >= 8:
        for j in range(len(s) - 2):
            INV[s[j:j + 3]].add(i)


def in_gold_fact(q: str) -> bool:
    if q in FSET:
        return True
    if len(q) < 8:
        return False
    cand = None
    for gr in sorted({q[j:j + 3] for j in range(len(q) - 2)}, key=lambda x: len(INV.get(x, ())))[:3]:
        c = INV.get(gr, set())
        cand = c if cand is None else cand & c
        if not cand:
            return False
    return any(q in FN[i] or FN[i] in q for i in cand or ())


SIL: set[str] = set()
for fn in ["step1-products.json", "step2-families.json", "step3-sites.json", "step4-techniques.json", "step5-units.json", "step6-packages.json",
           "step7-concerns.json", "step8-relations.json"]:
    for _, s in leaves(json.loads((W / fn).read_text(encoding="utf-8"))):
        SIL.add(norm(s))
SIL_L = [x for x in SIL if len(x) >= 12]


def in_silver(q: str) -> bool:
    return q in SIL or (len(q) >= 12 and any(q in x for x in SIL_L))


# ── 대상 정의(설명 사실 종류 · grep 식) ────────────────────────────────────
DESC_KEYS = r"(mechanism|overview|onset_duration\.(onset|duration|peak|peak_effect|maintenance|diffusion)|indications\.(primary|secondary|extended)(\[\])?)"
KINDS = [
    ("K1", "효과 시작 · 지속", r"onset_duration\."),
    ("K2", "작용 원리", r"(extracted\.mechanism|\{code\}\.mechanism|moa_summary)$"),
    ("K3", "개요 · 설명", r"(extracted\.overview|\{code\}\.overview|items\[\]\.detail|subcategories\[\]\.description)$"),
    ("K4", "적응증", r"(?<!contra)indications\."),
    ("K5", "합병증 설명", r"^complications\.categories\[\]\.complications\[\]\.(management|prevention|duration|onset|incidence|mechanism|risk_factors\[\])$"),
    ("K6", "반응 · 중증도 단계(값 사전)", r"^(post-procedure-timeline\.reaction_levels|complications\.severity_levels)\."),
    ("K7", "제품 메모", r"products\[\]\.(note|ingredient|material|legal_warning|type)$"),
    ("K8", "대안", r"alternatives\[\]$"),
    ("K9", "관련 기법", r"related_techniques\[\]$"),
    ("K10", "최적화 중증도 단계", r"^treatment-optimization\.by_concern\[\]\.severity_levels\[\]\.(rationale|sequence|expected_sessions|total_duration|evidence_level|caveats\[\]|contraindicated_combos\[\])$"),
    ("K11", "고민 상세", r"(cc_detail|problem\[\]\.subcategories\[\]\.items\[\]\.detail)$"),
]


def kind_of(pt: str) -> tuple[str, str] | None:
    for k, name, rx in KINDS:
        if re.search(rx, pt):
            return k, name
    return None


# ── 붙는 자리(attach) ─────────────────────────────────────────────────────
EX = {x["id"]: x for x in s5["extracted"]}
TP = {x["id"]: x for x in s5["taxonomy_products"]}
ITEM = {x["id"]: x for x in s7["concerns"]["items"]}


def item_nodes(iid: str) -> tuple[list[str], str]:
    """7단계 고민 항목 → 골드 노드: 고민 노드 그 자체 · 항목의 concern · 아니면 resolve 단위 시술(시술 이름 항목)."""
    if f"concern:{iid}" in gnodes:
        return [f"concern:{iid}"], "고민 노드"
    it = ITEM.get(iid) or {}
    c = it.get("concern")
    cs = c if isinstance(c, list) else [c] if c else []
    out = [f"concern:{x}" for x in cs if f"concern:{x}" in gnodes]
    if out:
        return out, "항목의 고민"
    us = [f"unit_procedure:{u}" for u in ((it.get("resolve") or {}).get("units") or []) if f"unit_procedure:{u}" in gnodes]
    if us:
        return us, "시술 이름 항목 → 단위 시술"
    return [], "붙을 노드 없음(" + str(it.get("kind")) + ")"


CC2NODES: dict[str, tuple[list[str], str]] = {}
for c in s7["correspondence"]:
    if c.get("field") == "complaints[].cc" and c.get("target"):
        ns, why = [], []
        for t in c["target"]:
            n_, w_ = item_nodes(t)
            ns += [x for x in n_ if x not in ns]
            why.append(w_)
        CC2NODES[c["text"]] = (ns, " · ".join(sorted(set(why))))
TAXPROD_BY_NAME = {}
for m in raw["taxonomy"]["modality"]:
    for p in m.get("products") or []:
        TAXPROD_BY_NAME[(m["id"], p.get("name"))] = p["id"]
CX_BY_NAME = {}
for x in (s8["safety"]["complications"] + s8["safety"]["side_effects"]):
    CX_BY_NAME[(x["family"], x["name"])] = x["id"]


def tp_attach(x: dict | None) -> dict:
    """taxonomy products 행(5단계 taxonomy_products) — 제품이면 제품 · 「단위 시술」(예 스킨보톡스 M4-P-3)이면 그 단위."""
    if not x:
        return {"rule": "R9-2", "status": "5단계 기록 없음", "nodes": []}
    if x.get("product"):
        return {"rule": "R9-2", "status": "제품(taxonomy products)", "nodes": [f"product:{x['product']}"]}
    if x.get("units"):
        return {"rule": "R9-2", "status": "단위 시술(taxonomy products · 5단계 S8)", "nodes": [f"unit_procedure:{u}" for u in x["units"]]}
    return {"rule": "R9-2", "status": x.get("attach") or "붙지 않음", "nodes": []}


def node_ok(n: str) -> bool:
    return n in gnodes


def attach(p: str, pt: str) -> dict:
    """원장 경로 → 붙는 실버 노드(들) · 규칙 번호 · 상태."""
    m = re.match(r"taxonomy\.modality\[(\d+)\]\.subcategories\[(\d+)\]\.items\[(\d+)\]", p)
    if m:
        it = raw["taxonomy"]["modality"][int(m[1])]["subcategories"][int(m[2])]["items"][int(m[3])]
        x = EX.get(it.get("id"))
        if not x:
            return {"rule": "R9-1", "status": "5단계 기록 없음", "nodes": []}
        a = x["attach"]
        if a.startswith("제품"):
            return {"rule": "R9-1", "status": a, "nodes": [f"product:{x['product']}"], "family": x.get("family")}
        if a == "단위 시술":
            return {"rule": "R9-1", "status": a, "nodes": [f"unit_procedure:{u}" for u in x["units"]]}
        if a == "단위 시술 후보":
            return {"rule": "R9-1", "status": a, "nodes": [f"unit_procedure:{u}" for u in x["units"]], "flag": "candidates"}
        return {"rule": "R9-1", "status": a, "nodes": []}  # 원문 보관 — 붙이지 않음(5단계 결정)
    m = re.match(r"taxonomy\.modality\[(\d+)\]\.products\[(\d+)\]", p)
    if m:
        pid = raw["taxonomy"]["modality"][int(m[1])]["products"][int(m[2])]["id"]
        return tp_attach(TP.get(pid))
    m = re.match(r"products\.(\w+)\.products\[(\d+)\]", p)
    if m:
        pr = raw["products"][m[1]]["products"][int(m[2])]
        hit = sorted(v for (mid, nm), v in TAXPROD_BY_NAME.items() if nm == pr.get("name"))
        a = tp_attach(TP.get(hit[0]) if hit else None)
        a["status"] = "products.json → " + (a["status"] if hit else "이름이 taxonomy products 에 없음")
        return a
    m = re.match(r"taxonomy\.modality\[(\d+)\]\.extracted", p)
    if m:
        return {"rule": "R9-3", "status": "계열(taxonomy 정본)", "nodes": [f"family:{raw['taxonomy']['modality'][int(m[1])]['id']}"]}
    m = re.match(r"extracted\.([A-Z]+\d+)\.", p)
    if m:
        return {"rule": "R9-3", "status": "계열(extracted.json 대조본)", "nodes": [f"family:{m[1]}"]}
    m = re.match(r"procedure-profiles\.profiles\[(\d+)\]", p)
    if m:
        return {"rule": "R9-4", "status": "계열(프로파일)", "nodes": [f"family:{raw['procedure-profiles']['profiles'][int(m[1])]['id']}"]}
    m = re.match(r"problem-packages\.problems\[(\d+)\]\.complaints\[(\d+)\]", p)
    if m:
        cc = raw["problem-packages"]["problems"][int(m[1])]["complaints"][int(m[2])]
        ns, why = CC2NODES.get(f"{cc['cc']} [{cc.get('cc_detail')}]") or CC2NODES.get(cc["cc"]) or ([], "대응표 없음")
        return {"rule": "R9-5", "status": "고민 CC → " + why, "nodes": ns}
    m = re.match(r"taxonomy\.problem\[(\d+)\]\.subcategories\[(\d+)\]\.items\[(\d+)\]", p)
    if m:
        it = raw["taxonomy"]["problem"][int(m[1])]["subcategories"][int(m[2])]["items"][int(m[3])]
        ns, why = item_nodes(it["id"])
        return {"rule": "R9-5", "status": "고민 항목 → " + why, "nodes": ns}
    m = re.match(r"complications\.categories\[(\d+)\]\.complications\[(\d+)\]", p)
    if m:
        cat = raw["complications"]["categories"][int(m[1])]
        cx = cat["complications"][int(m[2])]
        nid = CX_BY_NAME.get((cat["id"], cx["name"]))
        if nid and nid.startswith("SE-"):  # 경미 = 부작용 문장(계열 safety.side_effects) — 노드 아님
            return {"rule": "R9-6", "status": "부작용(8단계 실버 side_effects · 계열에 붙음)", "nodes": [f"family:{cat['id']}"] if f"family:{cat['id']}" in gnodes else [], "silver_id": nid}
        return {"rule": "R9-6", "status": "합병증(8단계 실버 complications · 노드)", "nodes": [f"complication:{nid}"] if nid and f"complication:{nid}" in gnodes else [], "silver_id": nid}
    if pt.startswith(("post-procedure-timeline.reaction_levels", "complications.severity_levels")):
        return {"rule": "R9-7", "status": "값 사전(시맨틱 · B02)", "nodes": ["scope:all"]}
    if pt.startswith("treatment-optimization.by_concern[].severity_levels[]"):
        return {"rule": "—", "status": "7단계 조합에 이미 있음", "nodes": []}
    return {"rule": "—", "status": "규칙 밖", "nodes": []}


# ── 1. 대상 필드 전수 ─────────────────────────────────────────────────────
fields: dict[str, dict] = {}
leaf_rows: list[dict] = []
for fname, obj in raw.items():
    for p, v in leaves(obj, fname):
        pt = pat(p)
        k = kind_of(pt)
        if not k:
            continue
        q = norm(v)
        if len(q) < 2:
            continue
        a = attach(p, pt)
        gf = in_gold_fact(q)
        sv = (not gf) and in_silver(q)
        f = fields.setdefault(pt, {"field": pt, "file": fname, "kind": k[0], "kind_name": k[1], "rule": a["rule"], "rows": 0, "gold_fact": 0,
                                   "silver_only": 0, "neither": 0, "attached_rows": 0, "attach_status": collections.Counter(), "example_path": p,
                                   "example_text": v[:120]})
        f["rows"] += 1
        f["gold_fact"] += gf
        f["silver_only"] += sv
        f["neither"] += (not gf and not sv)
        nodes = [n for n in a["nodes"] if n == "scope:all" or node_ok(n)]
        f["attached_rows"] += bool(nodes)
        f["attach_status"][a["status"]] += 1
        leaf_rows.append({"path": p, "field": pt, "kind": k[0], "rule": a["rule"], "status": a["status"], "nodes": nodes, "flag": a.get("flag"),
                          "gold_fact": gf, "silver_only": sv, "norm": q, "text": v})
for f in fields.values():
    f["attach_status"] = dict(sorted(f["attach_status"].items()))

# ── 중복 · 충돌(같은 노드 · 같은 칸 · 다른 값) ─────────────────────────────
def slot_key(r: dict) -> str:
    """같은 노드 안의 칸 이름 — extracted 아래는 그 뒤 경로(예 indications.primary · onset_duration.onset) · 그 밖은 마지막 키 · 배열 번호는 뗌."""
    p = re.sub(r"^extracted\.[A-Z]+\d+\.", "extracted.", r["path"])
    leaf = p.split("extracted.", 1)[-1] if "extracted." in p else p.rsplit(".", 1)[-1]
    return re.sub(r"\[\d+\]", "", leaf)


SCALAR = re.compile(r"(mechanism|overview|onset_duration\.\w+|moa_summary|note|ingredient|material|type|legal_warning|management|prevention|duration|onset|incidence|cc_detail|detail|indications\.\w+|related_techniques|alternatives)$")
slots: dict[tuple[str, str], list[dict]] = collections.defaultdict(list)
for r in leaf_rows:
    if r["rule"] in ("R9-1", "R9-2", "R9-3", "R9-4", "R9-5") and SCALAR.search(slot_key(r)):
        for n in r["nodes"]:
            slots[(n, slot_key(r))].append(r)
dup, conf, conf_by = 0, [], collections.Counter()
for (n, k), rs in sorted(slots.items()):
    by_src: dict[str, set] = collections.defaultdict(set)  # 원천 레코드(배열 번호 뗀 경로)마다 값 집합 — 배열 칸은 한 레코드 안 여러 값이 정상
    for r in rs:
        by_src[re.sub(r"\[\d+\]$", "", r["path"])].add(r["norm"])
    if len(by_src) < 2:
        continue
    sets = {frozenset(v) for v in by_src.values()}
    if len(sets) == 1:
        dup += 1
        continue
    srcs = sorted({r["rule"] + ":" + r["status"] for r in rs})
    kind = ("계열 taxonomy ↔ extracted.json" if n.startswith("family:") and any("extracted.json" in x for x in srcs) else
            "제품 원장 항목 ↔ taxonomy products" if n.startswith("product:") and len({r["rule"] for r in rs}) > 1 else
            "제품 원장 항목 여럿" if n.startswith("product:") else
            "단위 시술 원장 항목 여럿" if n.startswith("unit_procedure:") else
            "고민 · CC 여럿" if n.startswith("concern:") else "기타")
    conf_by[kind] += 1
    conf.append({"node": n, "slot": k, "kind": kind, "n_sources": len(by_src), "sources": sorted(by_src)[:6],
                 "texts": [r["text"][:80] for r in rs][:4]})

# ── 2차 A 54 · v5a A ──────────────────────────────────────────────────────
tri = json.loads((E / "build-out" / "fail-triage2.json").read_text(encoding="utf-8"))
A2 = []
for r in tri["rows"]:
    if r["cls"] != "A":
        continue
    ev = r["evidence"] if isinstance(r["evidence"], dict) else ast.literal_eval(r["evidence"])
    A2.append({"no": r["question_no"], "case": r["case"], "item": r["item"], "path": ev.get("path"), "quote": ev.get("quote")})
runs = {}
for line in (E / "runs" / "runs.jsonl").open(encoding="utf-8"):
    x = json.loads(line)
    if x.get("batch_id") == V5A:
        runs[x["run_id"]] = x
v5_fail, v5_tiers, A5 = 0, collections.Counter(), []
for line in (E / "runs" / "quality.jsonl").open(encoding="utf-8"):
    q = json.loads(line)
    if q.get("run_id") not in runs:
        continue
    for f in q["judge"].get("failures") or []:
        ev = f.get("evidence") or {}
        qt = norm(ev.get("quote") or "")
        tier = gold.gold_match(qt)[0] if len(qt) >= 2 else "short"
        v5_fail += 1
        v5_tiers[str(tier)] += 1
        if tier is None:
            A5.append({"no": q["question_no"], "case": "case3", "item": f["item"], "path": ev.get("path"), "quote": ev.get("quote"), "status": f.get("status")})

BY_PATH = collections.defaultdict(list)
for r in leaf_rows:
    BY_PATH[r["path"]].append(r)


def resolve_row(a: dict) -> dict:
    p = a["path"] or ""
    qn = norm(a["quote"] or "")
    cands = [r for r in leaf_rows if r["path"] == p or r["path"].startswith(p + ".") or r["path"].startswith(p + "[")]
    hit = [r for r in cands if qn and (qn in r["norm"] or (len(r["norm"]) >= 8 and r["norm"] in qn))] or ([] if qn else cands)  # 인용이 대상 잎과 안 맞으면 닫지 않음
    if not hit:
        fam = "라벨 · 메타 칸(설명 사실 아님)" if re.search(r"(period|label|description|\])$", p) or "profiles[" in p else "대상 밖"
        return {"closes": "아니오", "how": fam, "rule": None, "nodes": []}
    r = hit[0]
    nodes = sorted({n for h in hit for n in h["nodes"]})
    if r["rule"] == "R9-6":
        return {"closes": "골드 빌드로(실버 변경 없음)", "how": "8단계 실버에 이미 있음 — 골드 section 추가(R9-6 · V-4)", "rule": "R9-6", "nodes": nodes, "field": r["field"]}
    if r["rule"] in ("R9-1", "R9-2", "R9-3", "R9-4", "R9-5", "R9-7") and nodes:
        how = r["status"] + (" · 후보 전부(candidates)" if r.get("flag") else "")
        if r["rule"] == "R9-3" and "extracted.json" in r["status"]:
            tx = [x for x in slots.get((nodes[0], slot_key(r)), []) if "taxonomy" in x["status"]]
            same = any(x["norm"] == r["norm"] for x in tx)
            quote_in_tx = any(qn and qn in x["norm"] for x in tx)
            how += " · taxonomy 정본과 " + ("같음" if same or not tx else "다름 · 인용은 정본 안에도 있음" if quote_in_tx else "다름 → 대조본 원문도 싣는 규칙(R9-3b)일 때만")
        return {"closes": "예", "how": how, "rule": r["rule"], "nodes": nodes, "field": r["field"]}
    return {"closes": "아니오", "how": r["status"], "rule": r["rule"], "nodes": nodes, "field": r["field"]}


for lst in (A2, A5):
    for a in lst:
        a.update(resolve_row(a))


def tally(lst):
    c = collections.Counter(a["closes"] for a in lst)
    return dict(sorted(c.items()))


SECTION = {"K1": "recovery", "K2": "method", "K3": "overview", "K4": "overview", "K5": "safety.management(새 · V-4) · 관리 외 칸은 safety.complications",
           "K6": "global(값 사전)", "K7": "products(제품 노드 overview)", "K8": "overview(고민 노드)", "K9": "method", "K10": "evidence(이미)", "K11": "overview(고민 노드)"}

out = {
    "meta": {"generated_by": "step9-research.py", "raw_dir": str(RAW), "gold_build": g["build"]["build_hash"], "v5a_batch": V5A,
             "rule": "읽기 전용 · 원장 인용은 work/ 안에만 · 결정론"},
    "summary": {
        "fields": len(fields), "rows": sum(f["rows"] for f in fields.values()),
        "rows_gold_fact": sum(f["gold_fact"] for f in fields.values()), "rows_silver_only": sum(f["silver_only"] for f in fields.values()),
        "rows_neither": sum(f["neither"] for f in fields.values()),
        "by_kind": {k: {"name": nm, "fields": sum(1 for f in fields.values() if f["kind"] == k), "rows": sum(f["rows"] for f in fields.values() if f["kind"] == k),
                        "gold_fact": sum(f["gold_fact"] for f in fields.values() if f["kind"] == k),
                        "silver_only": sum(f["silver_only"] for f in fields.values() if f["kind"] == k),
                        "neither": sum(f["neither"] for f in fields.values() if f["kind"] == k),
                        "attached_rows": sum(f["attached_rows"] for f in fields.values() if f["kind"] == k), "section": SECTION[k]} for k, nm, _ in KINDS},
        "by_rule": dict(sorted(collections.Counter(r["rule"] for r in leaf_rows).items())),
        "attach_status_rows": dict(sorted(collections.Counter(r["status"] for r in leaf_rows).items())),
        "slots": len(slots), "duplicate_slots": dup, "conflict_slots": len(conf), "conflict_by_kind": dict(conf_by),
        "A2": {"rows": len(A2), "questions": len({a["no"] for a in A2}), "closes": tally(A2)},
        "A5": {"failures": v5_fail, "tiers": dict(v5_tiers), "rows": len(A5), "valid": sum(1 for a in A5 if a["status"] == "valid"), "closes": tally(A5)},
    },
    "fields": sorted(fields.values(), key=lambda f: (f["kind"], -f["rows"], f["field"])),
    "conflicts": conf,
    "A2_rows": A2, "A5_rows": A5,
}
(W / "step9-research.json").write_text(json.dumps(out, ensure_ascii=False, indent=1, default=dict) + "\n", encoding="utf-8")
print(json.dumps(out["summary"], ensure_ascii=False, indent=1))
