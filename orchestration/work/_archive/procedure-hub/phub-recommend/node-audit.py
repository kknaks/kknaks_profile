"""빈 노드 · 고립 노드 · 입구 · 효과 추정 — 읽기 전용 · 결정론(허브 18005 는 GET resolve 만).

입력: 원장 21(RAW) · gold-export 567677ed · semantic.json 사전 · fullrun-v2 배치 b202611020020-edc407(runs.jsonl)
· node-audit-coverage.py 의 판정 계층(①②③④ — 판사 인용 대조에 씀).
출력: stdout JSON(node-audit.json 의 §1~§4 재료). §0 커버리지는 node-audit-coverage.py.
"""
from __future__ import annotations

import collections
import importlib.util
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = Path("/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26")
GOLD = Path("/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend/build-out/gold-export.json")
RUNS = HERE.parents[2] / "reference/2026-10-30-hub-evals/runs/runs.jsonl"
BATCH = "b202611020020-edc407"
HUB = "http://127.0.0.1:18005/procedure-hub/gold/resolve"
KINDS = ["concern", "site", "technique", "purpose", "check_condition", "package", "combo"]
UNKNOWN = re.compile(r"정보 ?없음|정보가 없|자료에 없|확인되지 않|확인할 수 없|모르|알 수 없|안내하기 어렵|찾지 못", re.I)  # rerun_report 와 같은 식
CLAIM_NOINFO = re.compile(r"정보 ?없음|정보가 없|자료에 없|없다고|없습니다라고|확인되지 않|모른다")  # report.py CAUSES 1번과 같은 식
DEF_Q = re.compile(r"뭔가요|무엇인가요|뭐예요|뭐에요|이란|란 무엇|어떤 거|무슨 뜻|뭐죠")
JOSA = ["이랑", "에서", "으로", "만으로", "부터", "까지", "하고", "처럼", "보다", "에게", "이나", "은", "는", "이", "가", "을", "를", "와", "과",
        "랑", "에", "로", "만", "도", "의", "나"]
JOSA = sorted(set(JOSA), key=lambda x: (-len(x), x))

spec = importlib.util.spec_from_file_location("cov", HERE / "node-audit-coverage.py")
cov = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cov)
norm = cov.norm

# 재료 종류 — 잎 키(마지막 키) 기준
MAT = [
    ("별칭", re.compile(r"alias|synonym|other_name|aka|also_known|patient_name|name_ko$|nickname", re.I)),
    ("영문명", re.compile(r"(_en$|^en$|english|name_en)", re.I)),
    ("위치", re.compile(r"location|zone|area|region|anatom|layer|vessel|nerve|course|depth|muscle|tissue", re.I)),
    ("위험 등급", re.compile(r"risk|grade|severity|danger|level|caution|warning", re.I)),
    ("정의 · 설명", re.compile(r"description|overview|definition|explanation|simple_|analogy|summary|what$|subtitle|significance", re.I)),
    ("기법 설명", re.compile(r"technique|method|mechanism|modality$|approach|how", re.I)),
    ("가격", re.compile(r"price|cost|krw|won|^low$|^mid$|^high$|spec$", re.I)),
    ("대표 시술", re.compile(r"procedure|treatment|recommend|product|combo|package|option|first_line|items|name$|role|modality_ref|category$", re.I)),
    ("세부 · 메모", re.compile(r"detail|note|reason|evidence|caveat|tip|pearl|why|effect|goal|target|alternative", re.I)),
]
NAMEKEYS = {"name", "name_ko", "label", "problem", "concern", "cc", "title", "category", "patient_name", "zone", "condition", "label_ko"}
SKIPKEY = re.compile(r"source|citation|author|journal|doi|pmid|pmc|consensus|scored_by|rubric", re.I)
IDKEY = re.compile(r"(^|_)(id|ids|ref|refs|code|version|updated|added_at|extracted_at|source_type)$", re.I)


def mat_of(path: str) -> str:
    leaf = re.sub(r"\[\]", "", path.split(".")[-1])
    for name, rx in MAT:
        if rx.search(leaf):
            return name
    return "기타"


def walk(o, p, out, chain):
    """원장 잎(구체 경로) + 감싸는 레코드 사슬."""
    if isinstance(o, dict):
        rec = (p, o)
        for k, v in o.items():
            walk(v, f"{p}.{k}" if p else k, out, chain + [rec])
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, f"{p}[{i}]", out, chain)
    elif o is not None and not isinstance(o, bool):
        out.append((p, o, chain))


def rec_name(o: dict) -> str | None:
    for k in ("name", "name_ko", "label", "problem", "concern", "cc", "title", "category", "zone", "condition"):
        v = o.get(k)
        if isinstance(v, str) and v.strip():
            return v
    return None


def terms_of(n: dict, dict_by_target: dict) -> list[str]:
    s = (n.get("attrs") or {}).get("silver") or {}
    t = {n["name"]}
    for k in ("name", "source_name", "en", "medical_name"):
        if isinstance(s.get(k), str):
            t.add(s[k])
    for k in ("synonyms", "aliases"):
        for x in s.get(k) or []:
            t.add(x if isinstance(x, str) else (x.get("text") or ""))
    if isinstance(s.get("match_pattern"), str):
        t.update(s["match_pattern"].split("|"))
    an = s.get("anatomical_name")
    if isinstance(an, dict):
        t.update(v for v in (an.get("en"), an.get("ko")) if isinstance(v, str))
    t.update(dict_by_target.get(n["id"], []))
    base = re.sub(r"\s*\(.*?\)\s*", "", n["name"]).strip()
    if base:
        t.add(base)
    return sorted({x for x in t if len(norm(x)) >= 1})


def hub_resolve(text: str, cache: dict) -> dict:
    if text in cache:
        return cache[text]
    url = HUB + "?" + urllib.parse.urlencode({"text": text})
    with urllib.request.urlopen(url, timeout=20) as r:
        d = json.loads(r.read().decode("utf-8"))
    res = {"stage": d.get("stage"), "matches": sorted({c.get("id") or c.get("node_id") or json.dumps(c, ensure_ascii=False)
                                                       for m in d.get("matches") or [] for c in (m.get("candidates") or [m])}),
           "unmatched": d.get("unmatched") or []}
    cache[text] = res
    return res


def strip_josa(w: str) -> str:
    w = re.sub(r"[?!.,~]+$", "", w)
    for j in JOSA:
        if w.endswith(j) and len(w) - len(j) >= 2:
            return w[: -len(j)]
    return w


def main() -> None:
    g = json.loads(GOLD.read_text(encoding="utf-8"))
    nodes = {n["id"]: n for n in g["nodes"]}
    deg = collections.Counter()
    nb = collections.defaultdict(list)
    for e in g["edges"]:
        deg[e["from_id"]] += 1
        deg[e["to_id"]] += 1
    fc = collections.Counter()
    for f in g["facts"]:
        for i in {f["owner_id"], *(f.get("attached_to") or [])}:
            fc[i] += 1
    sem = json.loads((HERE / "semantic.json").read_text(encoding="utf-8"))["dictionary"]["expressions"]
    dict_by_target = collections.defaultdict(set)
    dict_norm = collections.defaultdict(set)
    for e in sem:
        for t in e["targets"]:
            if t.get("qualifier") is None:
                dict_by_target[t["id"]].add(e["expr"])
            dict_norm[e["norm"]].add(t["id"])
    # 원장 잎
    leaves = []
    for fn in sorted(os.listdir(RAW)):
        out = []
        walk(json.loads((RAW / fn).read_text(encoding="utf-8")), "", out, [])
        leaves += [(fn.replace(".json", ""), p, v, ch) for p, v, ch in out]
    str_leaves = [(f, p, str(v), norm(v), ch) for f, p, v, ch in leaves]
    # 괄호 별칭 후보
    paren = collections.defaultdict(set)
    for f, p, v, nv, ch in str_leaves:
        if SKIPKEY.search(p):
            continue
        for m in re.finditer(r"([가-힣A-Za-z0-9]{1,20})\s?\(([^()]{1,30})\)", v):
            a, b = m.group(1).strip(), m.group(2).strip()
            for x in re.split(r"[,/·]", b):
                x = x.strip()
                if 1 <= len(norm(x)) <= 20 and not re.search(r"\d{3,}|Ed\.|et al|등$", x):
                    paren[norm(a)].add((x, f"{f}.{p}"))
                    paren[norm(x)].add((a, f"{f}.{p}"))
    tiers = cov.build_tiers()[1]
    tier_cache: dict[str, str] = {}

    def tier_of(text: str) -> str:
        q = norm(text)
        if q not in tier_cache:
            r = "④"
            for t in tiers:
                if t.match(q)[0]:
                    r = "②" if t.name == "②m" else t.name
                    break
            tier_cache[q] = r
        return tier_cache[q]

    empty_ids = sorted(i for i, n in nodes.items() if n["kind"] in KINDS and fc[i] == 0)
    iso_ids = sorted(i for i in nodes if deg[i] == 0)
    audit_nodes = {}
    mat_norms: dict[str, list[str]] = {}
    all7 = {i for i, n in nodes.items() if n["kind"] in KINDS}
    for nid in sorted(all7 | {i for i in iso_ids if nodes[i]["kind"] != "evidence_source"}):
        n = nodes[nid]
        terms = terms_of(n, dict_by_target)
        tn = {norm(t) for t in terms}
        selfrec, mats, mentions = {}, collections.defaultdict(list), collections.defaultdict(list)
        for f, p, v, nv, ch in str_leaves:
            leafkey = re.sub(r"\[\d+\]", "", p.split(".")[-1])
            base = norm(re.sub(r"\s*\(.*?\)\s*", "", v))
            if leafkey in NAMEKEYS and (nv in tn or base in tn) and ch:
                rp, ro = ch[-1]
                selfrec.setdefault(f"{f}.{rp}", (ro, ch))
            elif SKIPKEY.search(p):
                continue
            elif any(len(t) >= 3 and t in nv for t in tn) or any(len(t) == 2 and (nv == t or nv.startswith(t) and len(nv) <= 6) for t in tn):
                mentions[mat_of(p)].append(f"{f}.{p}")
        for rp, (ro, ch) in sorted(selfrec.items()):
            sub = []
            walk(ro, "", sub, [])
            for p2, v2, _ in sub:
                if IDKEY.search(re.sub(r"\[\d+\]", "", p2.split(".")[-1])):
                    continue
                mk = mat_of(p2)
                depth = re.sub(r"\[\d+\]", "", re.sub(r"^extracted\.", "", p2)).count(".")
                if depth >= 1 and mk in ("정의 · 설명", "대표 시술", "기타", "기법 설명", "세부 · 메모"):
                    mk = "하위 항목"
                mats[mk].append({"path": f"{rp}.{p2}", "text": str(v2)[:200], "gold": tier_of(str(v2))})
            parents = [rec_name(o) for _, o in ch[:-1] if rec_name(o)]
            if parents:
                mats["상위 분류"].append({"path": rp, "text": " > ".join(parents), "gold": "–"})
        alias = sorted({(a, src) for t in tn for a, src in paren.get(t, ()) if norm(a) not in tn})
        # 같은 레코드가 여러 경로로 잡히면 재료 중복 — 경로+글로 한 번
        for k in list(mats):
            seen, uniq = set(), []
            for m in mats[k]:
                key = (m["path"], m["text"])
                if key not in seen:
                    seen.add(key)
                    uniq.append(m)
            mats[k] = uniq
        counts = {k: len(v) for k, v in sorted(mats.items())}
        mat_norms[nid] = sorted({norm(m["text"]) for v in mats.values() for m in v if len(norm(m["text"])) >= 6})
        has_def = bool(mats.get("정의 · 설명"))
        audit_nodes[nid] = {
            "id": nid, "kind": n["kind"], "name": n["name"], "facts": fc[nid], "edges": deg[nid],
            "terms": terms, "self_records": sorted(selfrec)[:12], "self_records_n": len(selfrec),
            "materials_count": counts, "materials": {k: v[:8] for k, v in sorted(mats.items())},
            "materials_not_fact": sum(1 for v in mats.values() for m in v if m["gold"] in ("②", "③", "④")),
            "alias_candidates": [{"alias": a, "src": s} for a, s in alias[:10]], "alias_candidates_n": len(alias),
            "mentions_count": {k: len(v) for k, v in sorted(mentions.items())},
            "mentions_top": {k: sorted(v)[:3] for k, v in sorted(mentions.items())},
            "empty": fc[nid] == 0, "isolated": deg[nid] == 0,
            "has_material": bool(selfrec and any(k != "상위 분류" for k in mats)),
            "has_definition": has_def,
            "silver_basis": ((n.get("attrs") or {}).get("silver") or {}).get("basis"),
        }
    # 고립 사유 · 후보
    iso = []
    for nid in iso_ids:
        n = nodes[nid]
        s = (n.get("attrs") or {}).get("silver") or {}
        why = {k: s.get(k) for k in ("anchor", "status", "notes", "note_8", "node", "same_as_concern", "from", "kind", "source",
                                     "4_license", "verdict", "open_reason", "cited_by", "used_by") if s.get(k) not in (None, [], "")}
        comps = [{"text": c.get("text"), "units": c.get("units"), "status": c.get("status"), "basis": c.get("basis")}
                 for c in (s.get("components") if isinstance(s.get("components"), list) else [])]
        iso.append({"id": nid, "kind": n["kind"], "name": n["name"], "facts": fc[nid], "silver_why": json.dumps(why, ensure_ascii=False)[:900],
                    "components": comps, "source_refs": n.get("source_refs")})
    # fullrun-v2
    rows = {}
    for line in RUNS.read_text(encoding="utf-8").splitlines():
        if BATCH not in line:
            continue
        r = json.loads(line)
        if r.get("batch_id") != BATCH:
            continue
        q = r["question_no"]
        if q not in rows or r["asked_at"] > rows[q]["asked_at"]:
            rows[q] = r
    hub_cache: dict = {}
    unmatched = collections.Counter()
    unmatched_q = collections.defaultdict(set)
    fb_rows, fail_rows = [], []
    empty_set, iso_set = set(empty_ids), set(iso_ids)
    for q in sorted(rows):
        r = rows[q]
        c3 = r["cases"]["case3"]
        w = (c3.get("trace") or {}).get("walk") or {}
        res = w.get("resolve") or {}
        for u in res.get("unmatched") or []:
            unmatched[u] += 1
            unmatched_q[u].add(q)
        items = (c3.get("judge") or {}).get("items") or {}
        fails = [f for f in (c3.get("judge") or {}).get("failures") or [] if f.get("status") == "valid"]
        touched = set(res.get("candidates") or [])
        if w.get("start_node"):
            touched.add(w["start_node"])
        for st in w.get("steps") or []:
            touched.add(st.get("node"))
            touched.update(((st.get("jev") or {}).get("picked_neighbors")) or [])
        touched.discard(None)
        ans = c3.get("answer") or ""
        row = {"q": q, "src": r.get("src_id"), "question": r["question"], "topic": r.get("topic"), "items": items,
               "fallback": w.get("fallback_reason"), "start": w.get("start_node"), "intent": ((w.get("jev0") or {}).get("intent") or {}).get("choice"),
               "resolve": {"candidates": res.get("candidates"), "menu": res.get("menu_candidates"), "unmatched": res.get("unmatched")},
               "touched_empty": sorted(touched & empty_set), "touched_iso": sorted(touched & iso_set),
               "answer_unknown": bool(UNKNOWN.search(ans)),
               "fail_claims": [{"item": f["item"], "noinfo_claim": bool(CLAIM_NOINFO.search(f.get("claim") or "")),
                                "evidence": f.get("evidence"), "quote_gold": tier_of((f.get("evidence") or {}).get("quote") or "") if (f.get("evidence") or {}).get("quote") else None,
                                "claim": (f.get("claim") or "")[:220]} for f in fails]}
        for fcl in row["fail_claims"]:
            qn = norm((fcl.get("evidence") or {}).get("quote") or "")
            hit = []
            if len(qn) >= 6:
                for tnid in sorted(touched):
                    if any(qn in m or (len(m) >= 8 and m in qn) for m in mat_norms.get(tnid, [])):
                        hit.append(tnid)
            fcl["quote_in_node_material"] = hit
            fcl["quote_in_isolated_material"] = [i for i in iso_ids if i in mat_norms and len(qn) >= 6
                                                 and any(qn in m or (len(m) >= 8 and m in qn) for m in mat_norms[i])]
        if w.get("fallback_reason"):
            words = []
            for u in res.get("unmatched") or []:
                sj = strip_josa(u)
                hr = hub_resolve(sj, hub_cache) if sj != u or True else None
                raw_hits = sorted({f"{f}.{re.sub(r'\[\d+\]', '[]', p)}" for f, p, v, nv, ch in str_leaves if len(norm(sj)) >= 2 and norm(sj) in nv})
                words.append({"word": u, "stripped": sj, "hub_resolve_stripped": hr, "dict_exact": sorted(dict_norm.get(norm(sj), [])),
                              "raw_paths_n": len(raw_hits), "raw_paths_top": raw_hits[:4]})
            row["words"] = words
            row["whole_resolve"] = hub_resolve(r["question"], hub_cache)
            fb_rows.append(row)
        if any(v == "실패" for v in items.values()):
            fail_rows.append(row)
    top_unmatched = []
    for u, k in sorted(unmatched.items(), key=lambda x: (-x[1], x[0])):
        sj = strip_josa(u)
        hr = hub_resolve(sj, hub_cache)
        raw_n = sum(1 for f, p, v, nv, ch in str_leaves if len(norm(sj)) >= 2 and norm(sj) in nv)
        top_unmatched.append({"word": u, "n": k, "questions": sorted(unmatched_q[u])[:6], "stripped": sj,
                              "hub_resolve_stripped": hr, "dict_exact": sorted(dict_norm.get(norm(sj), [])), "raw_leaves_containing": raw_n})
    out = {"gold_build": g["build"]["build_hash"], "batch": BATCH, "rows": len(rows),
           "empty_ids": empty_ids, "iso_ids": iso_ids, "nodes": audit_nodes, "isolated": iso,
           "fallback_rows": fb_rows, "fail_rows": fail_rows, "unmatched_top": top_unmatched,
           "unmatched_distinct": len(unmatched), "unmatched_total": sum(unmatched.values())}
    json.dump(out, sys.stdout, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
