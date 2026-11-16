"""실버 9단계(설명 사실) 반영 — 결정론(3~8단계와 같은 구조).

입력: step9-decisions.json(결정 — 종류 식 · 규칙 R9-1~R9-8 · section 표 · D9-3 충돌 처리 · 대조본 규칙 · 값 사전)
      원천(결정 source.path) taxonomy · extracted · products · procedure-profiles · problem-packages · complications · post-procedure-timeline
      실버 정본 step1-products · step2-families · step5-units(extracted · taxonomy_products attach) · step7-concerns(고민 항목 · CC 대응표) ·
      step8-relations(complications · side_effects) — 전부 읽기만
출력: step9-explanations.json · step9-explanations.md

조사(step9-research.py)의 붙는 자리 계산을 옮기고, 결정 D9-1~D9-9(사용자 11-01 「추천으로 데이터 결정하자」)를 반영한다.
사람 확인 게이트는 없다 — 붙는 자리는 5 · 7 · 8단계가 정한 대응으로, 충돌은 D9-3 ①②③ 규칙으로 푼다.
숫자는 이 파일에 적지 않는다(고정 assert 없음). 시각 · 무작위 없음 · 모든 목록 정렬 — 두 번 실행해 cmp 같음.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
from pathlib import Path

W = Path(__file__).resolve().parent
C_ = collections.Counter
CODE = re.compile(r"^([A-Z]{1,2}\d+(-\d+)*|auto-.*)$")


def norm(s) -> str:
    return re.sub(r"[\s\W_]+", "", str(s).lower())


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


def slot_key(path: str) -> str:
    """같은 노드 안의 칸 이름 — extracted 아래는 그 뒤 경로 · 그 밖은 마지막 키 · 배열 번호는 뗌."""
    p = re.sub(r"^extracted\.[A-Z]+\d+\.", "extracted.", path)
    leaf = p.split("extracted.", 1)[-1] if "extracted." in p else p.rsplit(".", 1)[-1]
    return re.sub(r"\[\d+\]", "", leaf)


def src_key(path: str) -> str:
    return re.sub(r"\[\d+\]$", "", path)


# ───────── 입력 ─────────
def load(args):
    dec = json.loads(Path(args.decisions).read_text(encoding="utf-8"))
    src = Path(args.source or dec["source"]["path"])
    raw = {f: json.loads((src / f"{f}.json").read_text(encoding="utf-8")) for f in dec["source"]["files"]}
    canon = {f: json.loads((Path(args.canon or W) / f).read_text(encoding="utf-8")) for f in dec["canon"]}
    return dec, raw, canon


def build(dec, raw, canon):
    S1, S2, S5, S7, S8 = (canon[f] for f in dec["canon"])
    OPEN: list[dict] = []

    def op(t, **kw):
        OPEN.append(dict(type=t, **kw))

    # 실버 노드(골드 export 를 읽지 않는다 — 실버에 있는 id 만)
    PRODUCTS = {x["ledger_id"] for x in S1["items"]}
    UNITS = {u["id"] for u in S5["units"]}
    FAMILIES = {f["id"] for f in S2["families"]}
    CON = S7["concerns"]
    CONCERNS = {x["id"] for k in ("categories", "subcategories") for x in CON[k] if x.get("node")}
    CONCERNS |= {x["id"] for x in CON["items"] if x.get("kind") == "고민"}  # 시맨틱 정본과 같음 — items[kind=고민] 이 고민 노드
    CONCERNS |= {x["id"].split("-")[0] for x in CON["extra_items"]}
    CX = {x["id"]: x for x in S8["safety"]["complications"]}
    SE = {x["id"]: x for x in S8["safety"]["side_effects"]}

    def node_ok(n: str) -> bool:
        kind, _, i = n.partition(":")
        return {"product": PRODUCTS, "unit_procedure": UNITS, "family": FAMILIES, "concern": CONCERNS}.get(kind, set()).__contains__(i) or n == "scope:all"

    KINDS = [(k["id"], k["name"], re.compile(k["regex"])) for k in dec["kinds"]]

    def kind_of(pt):
        for k, nm, rx in KINDS:
            if rx.search(pt):
                return k, nm
        return None

    EX = {x["id"]: x for x in S5["extracted"]}
    TP = {x["id"]: x for x in S5["taxonomy_products"]}
    EX_BY_NAME = collections.defaultdict(list)
    for x in S5["extracted"]:
        EX_BY_NAME[x["name"]].append(x)
    ITEM = {x["id"]: x for x in CON["items"]}
    TAX = raw["taxonomy"]
    TAXPROD = {}  # 이름 → taxonomy products 행
    for m in TAX["modality"]:
        for pr in m.get("products") or []:
            TAXPROD.setdefault(pr.get("name"), pr)
    UNATTACHED = set(dec["attach_status_unattached"])

    def ex_attach(x, rule):
        if not x:
            return dict(rule=rule, status="5단계 기록 없음", nodes=[], rank=9)
        a = x["attach"]
        if a.startswith("제품") and x.get("product"):
            return dict(rule=rule, status=a, nodes=[f"product:{x['product']}"], rank=0 if rule == "R9-1" else 1)
        if x.get("units") and a in ("단위 시술", "단위 시술 후보") or (rule == "R9-2" and x.get("units")):
            cand = a == "단위 시술 후보"
            return dict(rule=rule, status=a, nodes=[f"unit_procedure:{u}" for u in x["units"]], rank=2 if cand else (0 if rule == "R9-1" else 1),
                        flags=["candidates"] if cand else [])
        return dict(rule=rule, status=a, nodes=[], rank=9)

    def item_nodes(iid):
        if iid in CONCERNS:
            return [f"concern:{iid}"], "고민 노드"
        it = ITEM.get(iid) or {}
        c = it.get("concern")
        cs = [x for x in (c if isinstance(c, list) else [c] if c else []) if x in CONCERNS]
        if cs:
            return [f"concern:{x}" for x in cs], "항목의 고민"
        us = [f"unit_procedure:{u}" for u in ((it.get("resolve") or {}).get("units") or []) if u in UNITS]
        if us:
            return us, "시술 이름 항목 → 단위 시술"
        fs = [f"family:{f}" for f in ((it.get("resolve") or {}).get("families") or []) if f in FAMILIES]
        if fs:  # 7단계 R21 「이 부위 단위 시술 없음 · 계열만」 — 계열에 붙이고 표시
            return fs, "시술 이름 항목 → 계열(7단계 resolve · 단위 시술 없음)"
        return [], f"붙을 노드 없음({it.get('kind')})"

    CC2 = {}
    for c in S7["correspondence"]:
        if c.get("field") == "complaints[].cc" and c.get("target"):
            ns, why = [], []
            for t in c["target"]:
                n_, w_ = item_nodes(t)
                ns += [x for x in n_ if x not in ns]
                why.append(w_)
            CC2[c["text"]] = (ns, " · ".join(sorted(set(why))))

    def attach(p, pt):
        m = re.match(r"taxonomy\.modality\[(\d+)\]\.subcategories\[(\d+)\]\.items\[(\d+)\]", p)
        if m:
            it = TAX["modality"][int(m[1])]["subcategories"][int(m[2])]["items"][int(m[3])]
            return dict(ex_attach(EX.get(it.get("id")), "R9-1"), record=it.get("id"))
        m = re.match(r"taxonomy\.modality\[(\d+)\]\.subcategories\[(\d+)\]\.description$", p)
        if m:
            mod = TAX["modality"][int(m[1])]
            sub = mod["subcategories"][int(m[2])]
            return dict(rule="R9-8", status="계열 하위 분류 설명(D9-9)", nodes=[f"family:{mod['id']}"], rank=3, flags=[f"sub_family:{sub.get('label') or sub.get('id')}"])
        m = re.match(r"taxonomy\.modality\[(\d+)\]\.products\[(\d+)\]", p)
        if m:
            pid = TAX["modality"][int(m[1])]["products"][int(m[2])]["id"]
            return dict(ex_attach(TP.get(pid), "R9-2"), record=pid)
        m = re.match(r"products\.(\w+)\.products\[(\d+)\]", p)
        if m:
            pr = raw["products"][m[1]]["products"][int(m[2])]
            tp = TAXPROD.get(pr.get("name"))
            if tp:
                return dict(ex_attach(TP.get(tp["id"]), "R9-2"), record=tp["id"], twin=tp)
            exs = EX_BY_NAME.get(pr.get("name")) or []
            prods = sorted({x.get("product") for x in exs if x.get("product")})
            if len(prods) == 1:  # 같은 이름 원장 항목이 전부 같은 제품을 가리킴
                x0 = sorted((x for x in exs if x.get("product") == prods[0]), key=lambda x: x["id"])[0]
                return dict(ex_attach(x0, "R9-2"), rule="R9-2b", record=x0["id"])
            return dict(rule="R9-2b", status="이름 대응 없음", nodes=[], rank=9)
        m = re.match(r"taxonomy\.modality\[(\d+)\]\.extracted", p)
        if m:
            return dict(rule="R9-3", status="계열(taxonomy 정본)", nodes=[f"family:{TAX['modality'][int(m[1])]['id']}"], rank=3)
        m = re.match(r"extracted\.([A-Z]+\d+)\.", p)
        if m:
            return dict(rule="R9-3", status="계열(extracted.json 대조본)", nodes=[f"family:{m[1]}"], rank=3, twin_family=m[1])
        m = re.match(r"procedure-profiles\.profiles\[(\d+)\]", p)
        if m:
            return dict(rule="R9-4", status="계열(프로파일)", nodes=[f"family:{raw['procedure-profiles']['profiles'][int(m[1])]['id']}"], rank=3)
        m = re.match(r"problem-packages\.problems\[(\d+)\]\.complaints\[(\d+)\]", p)
        if m:
            cc = raw["problem-packages"]["problems"][int(m[1])]["complaints"][int(m[2])]
            key = f"{cc['cc']} [{cc.get('cc_detail')}]"
            ns, why = CC2.get(key) or CC2.get(cc["cc"]) or ([], "대응표 없음")
            fl = [f"cc:{key}"] if any(n.startswith("unit_procedure:") for n in ns) else []
            return dict(rule="R9-5", status="고민 CC → " + why, nodes=ns, rank=4, flags=fl)
        m = re.match(r"taxonomy\.problem\[(\d+)\]\.subcategories\[(\d+)\]\.items\[(\d+)\]", p)
        if m:
            it = TAX["problem"][int(m[1])]["subcategories"][int(m[2])]["items"][int(m[3])]
            ns, why = item_nodes(it["id"])
            return dict(rule="R9-5", status="고민 항목 → " + why, nodes=ns, rank=4)
        m = re.match(r"complications\.categories\[(\d+)\]\.complications\[(\d+)\]", p)
        if m:
            return dict(rule="R9-6", status="8단계 실버", nodes=[], rank=9)
        if pt.startswith(("post-procedure-timeline.reaction_levels", "complications.severity_levels")):
            return dict(rule="R9-7", status="값 사전(D9-7)", nodes=["scope:all"], rank=9)
        return dict(rule="—", status="규칙 밖", nodes=[], rank=9)

    SECTION = dec["section_map"]

    def section_of(slot, where=None):
        base = slot.split(".")[0] if slot.startswith(("onset_duration", "indications")) else slot.split(".")[-1]
        if where and f"{base}@{where}" in SECTION:
            return SECTION[f"{base}@{where}"]
        return SECTION.get(base)

    # ───────── 1. 대상 잎 전수 → 레코드 · 대조 · 값 사전 · 8단계 section 표 ─────────
    records, twins, source_conflicts, value_dict, section_map = [], [], [], [], []
    for fname in dec["source"]["files"]:
        for p, v in leaves(raw[fname], fname):
            pt = pat(p)
            k = kind_of(pt)
            if not k or len(norm(v)) < 2:
                continue
            a = attach(p, pt)
            slot = slot_key(p)
            if a["rule"] == "—":
                op("원천 칸 규칙 없음", path=p, field=pt)
                continue
            if a["rule"] == "R9-6":  # 실버 변경 없음 — 8단계 레코드에 같은 값이 있는지 대조 · section 만 정함
                m = re.match(r"complications\.categories\[(\d+)\]\.complications\[(\d+)\]\.(\w+)", p)
                cat = raw["complications"]["categories"][int(m[1])]
                cx = cat["complications"][int(m[2])]
                hit = next((x for x in list(CX.values()) + list(SE.values()) if x["family"] == cat["id"] and x["name"] == cx["name"]), None)
                field = m[3]
                if not hit:
                    op("8단계 실버에 합병증 · 부작용 레코드 없음", path=p)
                    continue
                sv = hit.get(field)
                ok = norm(v) in norm(json.dumps(sv, ensure_ascii=False)) if sv is not None else False
                if not ok:
                    op("8단계 실버 값과 원천 다름", path=p, silver_id=hit["id"], field=field)
                where = "complication" if hit["id"] in CX else "side_effect"
                sec = section_of(field, where)
                if not sec:
                    op("section 없는 칸", path=p, slot=field)
                section_map.append({"path": p, "silver_id": hit["id"], "silver_where": where, "field": field, "section": sec,
                                    "node": f"complication:{hit['id']}" if where == "complication" else f"family:{cat['id']}"})
                continue
            if a["rule"] == "R9-7":
                d_ = "reaction_levels" if "reaction_levels" in p else "severity_levels"
                value_dict.append({"dictionary": d_, "key": p.rsplit(".", 1)[-1], "text": v, "source": {"file": fname, "path": p}, "decision": "D9-7"})
                continue
            rec = {"id": f"S9:{p}", "rule": a["rule"], "kind": k[0], "slot": slot, "text": v, "source": {"file": fname, "path": p, "record": a.get("record")},
                   "attach": {"nodes": sorted(n for n in a["nodes"] if node_ok(n)), "status": a["status"], "flags": sorted(a.get("flags") or []), "rank": a["rank"]},
                   "section": section_of(slot)}
            missing = sorted(n for n in a["nodes"] if not node_ok(n))
            if missing:
                rec["attach"]["missing_nodes"] = missing
            if rec["section"] is None:
                op("section 없는 칸", path=p, slot=slot)
            # 대조본(D9-4 · R9-2a)
            if a.get("twin_family"):
                twins.append(rec)
                continue
            if a.get("twin"):
                tv = a["twin"].get(p.rsplit(".", 1)[-1])
                if tv is not None:
                    if norm(tv) == norm(v):
                        rec["status"] = "대조본 같음(same_as taxonomy products)"
                    else:
                        source_conflicts.append({"rule": "R9-2a", "path": p, "slot": slot, "text": v, "canon_text": str(tv), "canon": a["record"]})
                        rec["status"] = "source_conflict(싣지 않음)"
                    rec["attach"]["nodes"] = []
                    records.append(rec)
                    continue
            if not rec["attach"]["nodes"]:
                st = a["status"]
                unat = st in UNATTACHED or any(st.endswith(f"붙을 노드 없음({x})") for x in dec["concern_item_unattached_kinds"])
                rec["status"] = "붙이지 않음(" + st + ")" if unat else "open"
                if not unat:
                    op("붙는 노드 없음", path=p, status=st, missing=missing)
            else:
                rec["status"] = "붙음"
            records.append(rec)

    # extracted.json 대조(D9-4) — 같은 계열 · 같은 칸의 taxonomy 정본 값과
    tax_fam = collections.defaultdict(set)
    for r in records:
        if r["rule"] == "R9-3":
            tax_fam[(r["attach"]["nodes"][0], r["slot"])].add(norm(r["text"]))
    for r in twins:
        key = (f"family:{re.match(r'extracted\.([A-Z]+\d+)', r['source']['path'])[1]}", r["slot"])
        vals = tax_fam.get(key, set())
        if norm(r["text"]) in vals:
            r["status"] = "대조본 같음(same_as taxonomy 정본)"
        else:
            r["status"] = "source_conflict(싣지 않음)"
            source_conflicts.append({"rule": "D9-4", "path": r["source"]["path"], "slot": r["slot"], "text": r["text"], "canon": key[0]})
        r["attach"]["nodes"] = []
        records.append(r)

    # ───────── 2. D9-3 — 같은 노드 · 같은 칸 ─────────
    CR = dec["conflict_resolution"]
    UNITS_D = CR["time_units_days"]
    RANGE = re.compile(CR["range_regex"])
    NUM = re.compile(CR["numeric_regex"])
    ZERO = CR["zero_words"]
    LIST_SLOTS = set(CR["list_slots"])
    BYSLOT = [(re.compile(b["slot_regex"]), b["pick"]) for b in CR["by_slot"]]

    def numset(t):
        s = {re.sub(r"\.0+$", "", x) for x in NUM.findall(t)}
        if any(z in t for z in ZERO):
            s.add("0")
        return frozenset(s)

    def days(t):
        out = []
        for m in RANGE.finditer(t):
            a, u1, b, u2 = m.group(1), m.group(2), m.group(3), m.group(4)
            lo = float(a) * UNITS_D[u1 or u2]
            hi = float(b) * UNITS_D[u2] if b else lo
            out.append((lo, hi))
        if any(z in t for z in ZERO):
            out.append((0.0, 0.0))
        if not out:
            return None
        return (min(x[0] for x in out), max(x[1] for x in out))

    by_node = collections.defaultdict(list)
    for r in records:
        if r["status"] == "붙음":
            for n in r["attach"]["nodes"]:
                by_node[(n, r["slot"])].append(r)

    def cluster(rs):
        """같은 값 · 포함 관계를 긴 쪽으로 접는다 — (대표, [접힌 레코드 id]) 목록."""
        rs = sorted(rs, key=lambda r: (-len(norm(r["text"])), r["attach"]["rank"], r["source"]["path"]))
        reps = []
        for r in rs:
            q = norm(r["text"])
            host = next((h for h in reps if q in norm(h[0]["text"])), None)
            if host:
                host[1].append(r["id"])
            else:
                reps.append([r, []])
        return reps

    node_slots, cls_count, cls_by_slot = [], C_(), C_()
    for (n, slot), rs in sorted(by_node.items()):
        srcs = {src_key(r["source"]["path"]) for r in rs}
        reps = cluster(rs)
        is_list = slot in LIST_SLOTS
        entry = {"node": n, "slot": slot, "section": rs[0]["section"], "sources": len(srcs), "records": sorted(r["id"] for r in rs)}
        if len(srcs) < 2:
            cls = "한 원천"
        elif len({norm(r["text"]) for r in rs}) == 1 or (not is_list and len(reps) == 1 and all(norm(r["text"]) == norm(reps[0][0]["text"]) for r in rs)):
            cls = "같음"
        elif is_list:
            by_src = collections.defaultdict(set)
            for r in rs:
                by_src[src_key(r["source"]["path"])].add(norm(r["text"]))
            if len({frozenset(v) for v in by_src.values()}) == 1:
                cls = "같음"
            else:
                rep_src = collections.defaultdict(set)
                for h in reps:
                    rep_src[src_key(h[0]["source"]["path"])].add(h[0]["id"])
                cls = "①" if len(rep_src) == 1 else "③"
        elif len(reps) == 1:
            cls = "①"
        else:
            ns = [numset(h[0]["text"]) for h in reps]
            numeric = [i for i, s in enumerate(ns) if s]
            if numeric and len({ns[i] for i in numeric}) == 1 and len(numeric) == len(reps):
                cls = "①"  # 숫자 · 단위 집합이 같고 문장만 다름 — 긴 쪽(reps[0])
                reps = [[reps[0][0], reps[0][1] + [x for h in reps[1:] for x in [h[0]["id"]] + h[1]]]]
            elif len({ns[i] for i in numeric}) >= 2:
                cls = "②"
            else:
                cls = "③"
        entry["class"] = cls
        if cls == "②":
            numeric_reps = [h for h in reps if numset(h[0]["text"])]
            plain = [h for h in reps if not numset(h[0]["text"])]
            pick, how = None, None
            for rx, rule in BYSLOT:
                if rx.search(slot):
                    ds = [(days(h[0]["text"]), h) for h in numeric_reps]
                    if all(d for d, _ in ds):
                        if rule == "짧은 쪽":  # 지속 · 유지 — 위 끝(상한)이 짧은 쪽 · 같으면 아래 끝
                            pick = min(ds, key=lambda t: (t[0][1], t[0][0], t[1][0]["attach"]["rank"], t[1][0]["source"]["path"]))[1]
                        elif rule == "늦은 쪽":
                            pick = max(ds, key=lambda t: (t[0][0], t[0][1], -t[1][0]["attach"]["rank"], t[1][0]["source"]["path"]))[1]
                        else:
                            pick = max(ds, key=lambda t: (t[0][1], t[0][0], -t[1][0]["attach"]["rank"], t[1][0]["source"]["path"]))[1]
                        how = rule
                    break
            if pick is None:
                pick = min(numeric_reps, key=lambda h: (h[0]["attach"]["rank"], h[0]["source"]["path"]))
                how = "원천 우선순위"
            entry["resolved"] = pick[0]["id"]
            entry["resolved_by"] = how
            entry["alternatives"] = sorted(h[0]["id"] for h in numeric_reps if h is not pick)
            entry["emit"] = sorted([pick[0]["id"]] + [h[0]["id"] for h in plain])
            entry["same_as"] = {pick[0]["id"]: sorted(pick[1])} if pick[1] else {}
            for h in plain:
                if h[1]:
                    entry["same_as"][h[0]["id"]] = sorted(h[1])
            if plain:
                entry["multi_source"] = True
            if not entry["resolved"]:
                op("② 인데 resolved 없음", node=n, slot=slot)
        else:
            entry["emit"] = sorted(h[0]["id"] for h in reps)
            entry["same_as"] = {h[0]["id"]: sorted(h[1]) for h in reps if h[1]}
            if cls == "③" or (is_list and len(entry["emit"]) > 1 and len(srcs) > 1):
                entry["multi_source"] = True
        entry["fact_ids"] = [f"{n}#{entry['section']}#step9[{rid[3:]}]" for rid in entry["emit"]]
        cls_count[cls] += 1
        if cls in ("①", "②", "③"):
            cls_by_slot[(cls, slot)] += 1
        node_slots.append(entry)

    for r in records:
        if r["status"] == "open":
            pass
    rec_by = C_(r["status"] for r in records)
    summary = {
        "records": len(records), "records_by_status": dict(sorted(rec_by.items())),
        "records_by_rule": dict(sorted(C_(r["rule"] for r in records).items())),
        "records_by_kind": dict(sorted(C_(r["kind"] for r in records).items())),
        "attached_records": rec_by.get("붙음", 0),
        "node_slots": len(node_slots), "facts_out": sum(len(e["emit"]) for e in node_slots),
        "d93": {k: cls_count.get(k, 0) for k in ("한 원천", "같음", "①", "②", "③")},
        "d93_by_slot": {f"{c} {s}": v for (c, s), v in sorted(cls_by_slot.items())},
        "d93_resolved_by": dict(sorted(C_(e["resolved_by"] for e in node_slots if e.get("resolved_by")).items())),
        "alternatives": sum(len(e.get("alternatives") or []) for e in node_slots),
        "source_conflicts": len(source_conflicts), "source_conflicts_by_rule": dict(sorted(C_(c["rule"] for c in source_conflicts).items())),
        "value_dictionary": len(value_dict), "section_map": len(section_map),
        "section_map_by_section": dict(sorted(C_(str(x["section"]) for x in section_map).items())),
        "facts_by_section": dict(sorted(C_(str(e["section"]) for e in node_slots for _ in e["emit"]).items())),
        "nodes_by_kind": dict(sorted(C_(e["node"].split(":")[0] for e in node_slots).items())),
        "human_check": 0, "open": len(OPEN),
    }
    out = {"version": "step9-v1", "generated_by": "step9-apply.py", "decision_ref": dec["decision_ref"],
           "inputs": {"decisions": "step9-decisions.json", "source": dec["source"], "canon": dec["canon"]},
           "summary": summary, "records": sorted(records, key=lambda r: r["id"]), "node_slots": node_slots,
           "source_conflicts": sorted(source_conflicts, key=lambda c: c["path"]),
           "value_dictionary": sorted(value_dict, key=lambda x: (x["dictionary"], x["key"])),
           "section_map": sorted(section_map, key=lambda x: x["path"]),
           "new_sections": dec["new_sections"], "open": OPEN}
    return out


def write_md(o, OUT):
    s = o["summary"]
    L = ["# 실버 9단계 — 설명 사실 원장(step9-explanations)", "",
         "> 생성 `step9-apply.py`(결정론 · 두 번 cmp 같음) · 결정 `step9-decisions.json`(사용자 11-01 「추천으로 데이터 결정하자」) · 조사 `step9-research.md`. **원장 인용은 work/ 안에만**(공개 레포 커밋 안 함). 골드 반영(section `safety.management` 등)은 다음 허브 발주.", "",
         "## 셈", "", "| 칸 | 값 |", "|---|---|"]
    for k in ("records", "attached_records", "node_slots", "facts_out", "alternatives", "source_conflicts", "value_dictionary", "section_map", "human_check", "open"):
        L.append(f"| {k} | {s[k]:,} |")
    L += ["", "레코드 상태:", "", "| 상태 | 레코드 |", "|---|---|"] + [f"| {k} | {v:,} |" for k, v in s["records_by_status"].items()]
    L += ["", "규칙별:", "", "| 규칙 | 레코드 |", "|---|---|"] + [f"| {k} | {v:,} |" for k, v in s["records_by_rule"].items()]
    L += ["", "## D9-3 같은 노드 · 같은 칸(node_slots)", "", "| 분류 | 칸 수 | 뜻 |", "|---|---|---|",
          f"| 한 원천 | {s['d93']['한 원천']:,} | 원천 레코드 하나 — 충돌 아님 |",
          f"| 같음 | {s['d93']['같음']:,} | 원천 여럿 · 값 같음(same_as) |",
          f"| ① 포함 관계 | {s['d93']['①']:,} | 한쪽이 다른 쪽을 정규화 포함 · 또는 숫자 · 단위 집합 같음 → 긴 쪽 하나 |",
          f"| ② 숫자 다름 | {s['d93']['②']:,} | resolved 하나 · 나머지 alternatives({s['alternatives']:,}) — " + " · ".join(f"{k} {v}" for k, v in s["d93_resolved_by"].items()) + " |",
          f"| ③ 숫자 없는 다른 문장 | {s['d93']['③']:,} | 둘 다 실음 · multi_source |", "",
          "| 분류 · 칸 | 수 |", "|---|---|"] + [f"| {k} | {v} |" for k, v in s["d93_by_slot"].items()]
    L += ["", "## 골드로 나갈 fact(section 별 · 다음 허브 발주)", "", "| section | fact |", "|---|---|"] + [f"| {k} | {v:,} |" for k, v in s["facts_by_section"].items()]
    L += ["", "8단계 실버 그대로 · section 만 정함(R9-6 · D9-1):", "", "| section | 칸 |", "|---|---|"] + [f"| {k} | {v} |" for k, v in s["section_map_by_section"].items()]
    L += ["", "## 대조본 source_conflict(싣지 않음 · D9-4 · R9-2a)", "", "| 규칙 | 원천 경로 | 칸 | 대조 정본 |", "|---|---|---|---|"]
    L += [f"| {c['rule']} | `{c['path']}` | {c['slot']} | {c.get('canon')} |" for c in o["source_conflicts"]]
    L += ["", "## 값 사전(D9-7 · 시맨틱 value_dictionary)", "", "| 사전 | 키 | 원문 |", "|---|---|---|"]
    L += [f"| {x['dictionary']} | {x['key']} | {x['text']} |" for x in o["value_dictionary"]]
    L += ["", "## ② 처분 예(처음 10)", "", "| 노드 | 칸 | 고른 방법 | resolved | alternatives |", "|---|---|---|---|---|"]
    rec = {r["id"]: r for r in o["records"]}
    for e in [e for e in o["node_slots"] if e["class"] == "②"][:10]:
        L.append(f"| {e['node']} | {e['slot']} | {e['resolved_by']} | 「{rec[e['resolved']]['text'][:50]}」 | " + " / ".join("「" + rec[a]["text"][:40] + "」" for a in e["alternatives"]) + " |")
    L += ["", f"## open — {len(o['open'])}", ""] + [f"- {json.dumps(x, ensure_ascii=False)}" for x in o["open"]]
    (OUT / "step9-explanations.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def main(argv=None):
    AP = argparse.ArgumentParser()
    AP.add_argument("--decisions", default=str(W / "step9-decisions.json"))
    AP.add_argument("--source", help="원천 경로 덮어쓰기(고정 시험용)")
    AP.add_argument("--canon", help="실버 정본 폴더 덮어쓰기(고정 시험용)")
    AP.add_argument("--out", default=str(W))
    args = AP.parse_args(argv)
    dec, raw, canon = load(args)
    o = build(dec, raw, canon)
    OUT = Path(args.out)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "step9-explanations.json").write_text(json.dumps(o, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    write_md(o, OUT)
    print(json.dumps(o["summary"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
