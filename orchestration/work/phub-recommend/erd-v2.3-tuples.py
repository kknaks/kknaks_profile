#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ERD v2.3 — 튜플 분해 실측기. v2.2(erd-v2.2-tuples.py) 위에 2차 독립 검토(erd-v2.2-review.md) 반영 수정 1·2·3 만 바꾼다. 독립 실행.

v2.2 → v2.3 (발주서 erd-v2.3-brief.md):
  1. 시술 축 엣지의 끝 = 시술 튜플. 참조가 튜플(또는 combo_ref 멤버)로 해결됐으면 procedure 튜플 id 가 끝(target_depth=procedure).
     M 코드만(M1)·실존 하위분류 id(M1-2·M16-DCA)인 참조는 분해하지 않고 그 노드가 끝(modality/subcategory · 튜플 없음) — v2.2 는 이것도 튜플(what=modality|subcategory × none × none)로 만들었다.
     제품 전용 자리(products[])·제품 레코드는 product 끝. 분류 항목 id·항목 레코드는 그 항목의 튜플. 실측 §9.5.8 「엣지 자리별 끝 분포」(procedure / modality / subcategory / product / unresolved).
  2. 경과(course)는 사건에 바로 붙은 수식어(같은 멤버)만. 멤버 밖(묶음·outer·이름 전체)에서 가져오지 않는다. site 는 v2 그대로.
  3. 부작용도 미등록 조각이 있으면 접지 않는다. complications 이름에 미등록 조각이 있으면 이름마다 고유한 raw_name 튜플(anchor=원장 locator · candidate_name) —
     접힘은 세 칸 전부 사전 값(미등록 0)일 때만. 표현(AEX)은 raw_name 을 만들지 않고 닿은 사전 튜플에 연결하되 match_status=partial.
시술 분해 규칙(①②③ 조각·what·site·technique)은 v2.2 그대로(코드 재사용).

입력(같은 폴더): erd-v2.3-dictionaries.json(없으면 v2.2) · erd-v2.3.json(tuple_rules/resolve_rules — 없으면 erd_spec_v23) · erd-v2.2-tuples.py(→ v2.1 → v2) · erd-v1.1-resolve.py · 원장 21 · erd-v2.2-tuples.json(§9.5·§9.6 나란히 비교용)
출력: 표준 출력에 §9.5/§9.6 표 + erd-v2.3-tuples.json
실행: python3 erd-v2.3-tuples.py
"""
import importlib.util
import json
import os
import re
import sys
from collections import Counter, OrderedDict, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


V22 = load_module("erd_v22_tuples", os.path.join(HERE, "erd-v2.2-tuples.py"))
V21 = V22.V21
V2 = V22.V2
norm, mkid, md_table, with_alias, LEDGER = V2.norm, V2.mkid, V2.md_table, V2.with_alias, V2.LEDGER
DICT_WHAT_KINDS = V22.DICT_WHAT_KINDS
CODE_KEY_RE = V2.CODE_KEY_RE
END_KINDS = ["procedure", "modality", "subcategory", "product", "unresolved"]


def locator(file, path, record):
    return f"{file}:{path}@{record}"


# ---------------------------------------------------------------------------
# ① ② ③ 시술 — v2.2 그대로 + 수정 1(코드 참조는 노드 끝 · 튜플 없음)
# ---------------------------------------------------------------------------
class ProcedureTuples23(V22.ProcedureTuples22):
    def run_reference(self, label, hint, origin, slot):
        anc = V22.ref_anchor(label, hint)
        if isinstance(label, str) and label.startswith("__MODALITY__"):
            code = label[12:]
            return {"label": code, "hint": code, "ref_id": anc, "result": "node", "end_kind": "modality", "end_id": self.ids.mod[code]["id"], "what_basis": "modality_code", "status": "complete", "unregistered": [], "qualifiers": [],
                    "fragments": {"primaries": [f"modality:{code}"], "sites": [], "techniques": []}, "extra_primaries": [], "extra_sites": [], "reason": "M 코드만 적힌 참조 — 계열 노드가 끝(튜플 없음 · v2.3 수정 1)"}
        if isinstance(label, str) and label.startswith("__SUBID__"):
            sid = label[9:]
            e = self.ids.sub[sid]
            return {"label": sid, "hint": hint, "ref_id": anc, "result": "node", "end_kind": "subcategory", "end_id": e["id"], "what_basis": "subcategory_id", "status": "complete", "unregistered": [], "qualifiers": [],
                    "fragments": {"primaries": [f"modality_subcategory:{e['label']}"], "sites": [], "techniques": []}, "extra_primaries": [], "extra_sites": [], "reason": "실존 하위분류 id 만 적힌 참조 — 하위분류 노드가 끝(튜플 없음 · v2.3 수정 1)"}
        return super().run_reference(label, hint, origin, slot)


# 참조 자리 → 관계 (엣지 자리별 끝 분포 · 전수: R9·R12·R15·R16·R17·R18 의 시술 축 출처 키 전부)
SLOT_RELATION = OrderedDict([
    ("synergy.links[].from/to (노드 52)", ("R18", "kind=synergy_*")),
    ("problem-packages.procedures[].name (시술 종류 29)", ("R9", "target_label")),
    ("problem-packages.combos[].combo[] (멤버 29)", ("R12", "cc_combo 멤버")),
    ("problem-packages.procedures[].products[] (제품 34)", ("R9", "products 속성 — 제품 사전 전용 자리 · 끝은 product(제품 층까지만 적힌 참조)")),
    ("procedure-comparison.procedures[].name (39)", ("R12", "comparison 멤버")),
    ("treatment-optimization.optimal_combo[] (57)", ("R12", "optimization_plan 멤버")),
    ("treatment-optimization.by_age_group recommended_base/avoid/upgrade (22)", ("R17", "age_group → proc_axis")),
    ("treatment-optimization.annual_plans.schedule[].procedures[] (29)", ("R12", "annual_plan 멤버")),
    ("treatment-sequence.sequence_order[].categories[] (19)", ("R18", "kind=pair_rule(순서)")),
    ("treatment-sequence.incompatible_same_day[].pair[] (14 distinct)", ("R18", "kind=incompatible_same_day")),
    ("treatment-sequence.minimum_intervals from/to (14 distinct)", ("R18", "kind=minimum_interval")),
    ("treatment-sequence.common_combos[].sequence[] (22 distinct)", ("R12", "session_combo 멤버")),
    ("post-procedure-timeline.timelines[].name (10)", ("R15", "from(timeline name)")),
])
MARKET_SLOT_NOTE = ("—", "③ market-pricing items[].name — 엣지가 아니라 modality.price_items.label 의 튜플 연결(참고 행)")


def edge_ends(PT, ref_rows, mk_rows, cat_recs, L, ids):
    """엣지 자리별 끝 분포 — 텍스트 참조 자리(②③) + 코드·레코드 자리(원장에서 직접) 전부."""
    T = PT.tuples
    cat = {(r["family"], r["name"]): r for r in cat_recs}
    item_by_id = {}
    for m in L["taxonomy.json"]["modality"]:
        for sc in m["subcategories"]:
            for it in sc["items"]:
                item_by_id[it["id"]] = (m["id"], it["name"])
    sub_ids = set(ids.sub)
    mod_ids = set(ids.mod)

    def classify_code(v):
        v = str(v)
        if v in mod_ids:
            return ("modality", ids.mod[v]["id"], None)
        if v in sub_ids:
            return ("subcategory", ids.sub[v]["id"], None)
        if v in item_by_id:
            fam, name = item_by_id[v]
            rec = cat[(fam, name)]
            return ("procedure", rec.get("procedure_id"), rec["catalog_item_id"])
        return ("unresolved", None, None)

    rows = []

    def text_row(slot, rel, note, rrows, product_slot=False):
        ends = []
        for r in rrows:
            if r["result"] == "tuple":
                t = T[r["procedure_id"]]
                kind = "product" if product_slot else "procedure"
                ends.append({"label": r["label"], "hint": r.get("hint"), "end_kind": kind, "target_depth": kind, "end_id": t["what_id"] if product_slot else r["procedure_id"],
                             "procedure_id": r["procedure_id"], "via_catalog_item": (mkid("CAT", f"{t['family']}|{r['via_item']}") if (r.get("via_item") and not product_slot) else None), "anchored": t["anchor"] is not None})
            elif r["result"] == "combo_ref":
                ends.append({"label": r["label"], "hint": r.get("hint"), "end_kind": "procedure", "target_depth": "procedure", "end_id": list(r["member_ids"]), "procedure_id": list(r["member_ids"]), "via_catalog_item": None, "combo_members": len(r["member_ids"]), "anchored": any(T[m]["anchor"] is not None for m in r["member_ids"])})
            elif r["result"] == "node":
                ends.append({"label": r["label"], "hint": r.get("hint"), "end_kind": r["end_kind"], "target_depth": r["end_kind"], "end_id": r["end_id"], "procedure_id": None, "via_catalog_item": None})
            else:
                ends.append({"label": r["label"], "hint": r.get("hint"), "end_kind": "unresolved", "target_depth": None, "end_id": None, "procedure_id": None, "via_catalog_item": None, "reason": r.get("unresolved_reason") or r["result"]})
        c = Counter(e["end_kind"] for e in ends)
        rows.append(OrderedDict([("slot", slot), ("relation", rel), ("note", note), ("kind", "text"), ("n", len(ends))] + [(k, c.get(k, 0)) for k in END_KINDS]
                                + [("procedure_anchored", sum(1 for e in ends if e["end_kind"] == "procedure" and e.get("anchored"))), ("via_catalog_item", sum(1 for e in ends if e.get("via_catalog_item"))), ("ends", ends)]))

    for slot, rrows in ref_rows.items():
        rel, note = SLOT_RELATION[slot]
        text_row(slot, rel, note, rrows, product_slot=slot.startswith("problem-packages.procedures[].products[]"))
    text_row("market-pricing.items[].name (122)", MARKET_SLOT_NOTE[0], MARKET_SLOT_NOTE[1], mk_rows)

    def code_row(slot, rel, note, values):
        ends = []
        for v in values:
            if isinstance(v, tuple) and v[0] == "item":
                rec = cat[(v[1], v[2])]
                ends.append({"label": v[2], "hint": v[1], "end_kind": "procedure", "target_depth": "procedure", "end_id": rec.get("procedure_id"), "via_catalog_item": rec["catalog_item_id"]})
            elif isinstance(v, tuple) and v[0] == "product":
                p = ids.prod.get(norm(v[2]))
                ends.append({"label": v[2], "hint": v[1], "end_kind": "product" if p else "unresolved", "target_depth": "product" if p else None, "end_id": p["id"] if p else None, "reason": None if p else "제품 색인에 없는 taxonomy products[] 이름"})
            else:
                k, eid, via = classify_code(v)
                ends.append({"label": str(v), "hint": None, "end_kind": k, "target_depth": k if k != "unresolved" else None, "end_id": eid, "via_catalog_item": via})
        c = Counter(e["end_kind"] for e in ends)
        rows.append(OrderedDict([("slot", slot), ("relation", rel), ("note", note), ("kind", "code"), ("n", len(ends))] + [(k, c.get(k, 0)) for k in END_KINDS]
                                + [("procedure_anchored", None), ("via_catalog_item", sum(1 for e in ends if e.get("via_catalog_item"))), ("ends", ends)]))

    # R3 — 분류 항목 이름 = 같은 계열 제품명
    r3 = [r for r in cat_recs if r["result"] == "tuple" and r.get("what_kind") == "product" and r.get("whole_match") and str(r.get("what_basis", "")).startswith("product:") and "(타 계열)" not in str(r.get("what_basis", ""))]
    rows.append(OrderedDict([("slot", "taxonomy.json:modality[].subcategories[].items[].name = 같은 계열 제품명 (①)"), ("relation", "R3"), ("note", "uses_product — 항목 이름이 같은 계열 제품명과 정규화 완전 일치. from 끝 = 그 항목의 튜플(what=product)"), ("kind", "code"), ("n", len(r3))]
                            + [(k, (len(r3) if k == "procedure" else 0)) for k in END_KINDS]
                            + [("procedure_anchored", sum(1 for r in r3 if T[r["procedure_id"]]["anchor"] is not None)), ("via_catalog_item", len(r3)),
                               ("ends", [{"label": r["name"], "hint": r["family"], "end_kind": "procedure", "target_depth": "procedure", "end_id": r["procedure_id"], "via_catalog_item": r["catalog_item_id"]} for r in r3])]))
    # R15 코드·레코드 자리
    comp = L["complications.json"]
    code_row("complications.json:categories[].id (10)", "R15", "from — 계열 코드 자리(이름 65 의 원인 시술)", [c["id"] for c in comp["categories"]])
    pih = L["pih-risk.json"]
    code_row("pih-risk.json:procedures[].procedure_ref (26)", "R15", "from — 가장 구체 수준 그대로(질문 5): 항목 id → 그 항목의 튜플 · 하위분류 id → subcategory · M 코드 → modality", [p["procedure_ref"] for p in pih["procedures"]])
    tl = L["post-procedure-timeline.json"]
    code_row("post-procedure-timeline.json:timelines[].category (10)", "R15", "from — M 코드 → modality · M16-DCA → subcategory(질문 7)", [t["category"] for t in tl["timelines"]])
    code_row("post-procedure-timeline.json:timelines[].phases[].normal/abnormal/caution/emergency[] 문구 (R29 → R15)", "R15", "from = 그 타임라인의 category", [t["category"] for t in tl["timelines"] for ph in t["phases"] for k in ("normal", "abnormal", "caution", "emergency") for _ in (ph.get(k) or [])])
    code_row("consent-checklist.json:categories[].emergency_signs[] 문구 (R29 → R15)", "R15", "from = categories[].id", [c["id"] for c in L["consent-checklist.json"]["categories"] for _ in (c.get("emergency_signs") or [])])
    ex = L["extracted.json"]
    code_row("extracted.json:{code}.safety.common/uncommon/serious/emergency[] 문구 (R29 → R15)", "R15", "from = 코드 키(계열)", [code for code, v in ex.items() if CODE_KEY_RE.match(code) for k in ("common", "uncommon", "serious", "emergency") for _ in ((v.get("safety") or {}).get(k) or [])])
    tx = L["taxonomy.json"]
    code_row("taxonomy.json:modality[].extracted.safety.common/uncommon/serious[] 문구 (R29 → R15)", "R15", "from = 계열 레코드", [m["id"] for m in tx["modality"] for k in ("common", "uncommon", "serious") for _ in (((m.get("extracted") or {}).get("safety") or {}).get(k) or [])])
    code_row("taxonomy.json:modality[].subcategories[].items[].extracted.safety.* 문구 (R29 → R15)", "R15", "from = 항목 레코드 → 그 항목의 튜플(procedure)",
             [("item", m["id"], it["name"]) for m in tx["modality"] for sc in m["subcategories"] for it in sc["items"] for k in ("common", "serious", "common_adverse_effects", "serious_adverse_effects", "long_term") for _ in (((it.get("extracted") or {}).get("safety") or {}).get(k) or [])])
    code_row("taxonomy.json:modality[].products[].extracted.safety.* 문구 (R29 → R15)", "R15", "from = 제품 레코드 → product(제품 층까지만 적힘)",
             [("product", m["id"], pr["name"]) for m in tx["modality"] for pr in m["products"] for k in ("common", "serious", "common_side_effects") for _ in (((pr.get("extracted") or {}).get("safety") or {}).get(k) or [])])
    lit = L["literature-evidence.json"]
    code_row("literature-evidence.json:categories.{code}.adverse_effects[] (R29 → R15)", "R15", "from = 코드 키(계열)", [code for code, c in lit["categories"].items() for _ in (c.get("adverse_effects") or [])])
    # R16
    code_row("consent-checklist.json:categories[].id (17)", "R16", "from — 계열 코드 자리", [c["id"] for c in L["consent-checklist.json"]["categories"]])
    code_row("pre-procedure-checklist.json:category_specific[].id (17)", "R16", "from — 계열 코드 자리", [c["id"] for c in L["pre-procedure-checklist.json"]["category_specific"]])
    # R18 contraindications
    code_row("contraindications.json:rules[].from/to (27×2)", "R18", "kind=pair_rule — M 코드 자리", [x for r in L["contraindications.json"]["rules"] for x in (r["from"], r["to"])])
    # R12 코드 멤버
    code_row("combo-recipes.json:recipes[].procedures[] (M 코드)", "R12", "recipe 멤버 — M 코드 자리", [x for r in L["combo-recipes.json"]["recipes"] for x in r["procedures"]])
    code_row("problem-combos.json:combos[].packages[].procedures[] (M 코드)", "R12", "consult_package 멤버 — M 코드 자리", [x for c in L["problem-combos.json"]["combos"] for p in c["packages"] for x in p["procedures"]])
    tot = Counter()
    for r in rows:
        if r["relation"] == "—":
            continue
        for k in END_KINDS:
            tot[k] += r[k]
    by_rel = OrderedDict()
    for r in rows:
        if r["relation"] == "—":
            continue
        d = by_rel.setdefault(r["relation"], Counter())
        for k in END_KINDS:
            d[k] += r[k]
        d["n"] += r["n"]
    return {"rows": rows, "total": dict(tot), "total_n": sum(r["n"] for r in rows if r["relation"] != "—"), "by_relation": {k: dict(v) for k, v in by_rel.items()},
            "text_slots": sum(1 for r in rows if r["kind"] == "text" and r["relation"] != "—"), "code_slots": sum(1 for r in rows if r["kind"] == "code"),
            "relations_covered": sorted({r["relation"] for r in rows if r["relation"] != "—"}, key=lambda x: int(x[1:]))}


# ---------------------------------------------------------------------------
# 부작용 — 수정 2(course 멤버만) · 수정 3(raw_name · 접힘 조건)
# ---------------------------------------------------------------------------
class AdverseTuples23(V2.AdverseTuples):
    def assemble(self, groups):
        """멤버 안의 사건 하나 = 튜플 하나. course 는 같은 멤버 안의 수식어만(v2.3). site 는 v2 그대로 멤버 → 묶음 → outer → 이름 전체 유일값."""
        def pick(spans, kind):
            x = [s for s in spans if s["kind"] == kind]
            return x[0]["canonical"] if x else None

        def pick_site(spans):
            for s in spans:
                if s["kind"] in ("relative", "site"):
                    return (s["kind"], s["canonical"])
            return None

        outer_spans = [s for m in groups[0]["members"] for s in m["spans"]]
        all_spans = [s for g in groups for m in g["members"] for s in m["spans"]]
        name_sites = list(dict.fromkeys((s["kind"], s["canonical"]) for s in all_spans if s["kind"] in ("relative", "site")))
        name_site = name_sites[0] if len(name_sites) == 1 else None
        out = []
        for g in groups:
            g_spans = [s for m in g["members"] for s in m["spans"]]
            for m in g["members"]:
                events = [s["canonical"] for s in m["spans"] if s["kind"] == "event"]
                if not events:
                    continue
                site = pick_site(m["spans"]) or pick_site(g_spans) or pick_site(outer_spans) or name_site
                course = pick(m["spans"], "course") or "미상"
                for ev in dict.fromkeys(events):
                    out.append({"event": ev, "site": site, "course": course, "member": m["text"], "course_basis": "member" if pick(m["spans"], "course") else None})
        untouched = [u for g in groups for m in g["members"] for u in m["untouched"]]
        seen, uniq = set(), []
        for t in out:
            k = (t["event"], t["site"], t["course"])
            if k not in seen:
                seen.add(k)
                uniq.append(t)
        return uniq, untouched

    def register(self, t, src, untouched):
        """사전 튜플(event_kind=dict · 세 칸 전부 사전 값). 미등록 조각이 있는 문구(표현)가 닿아도 접힘이 아니라 R29 partial 이다 — 튜플 status 는 v2 그대로 보고용."""
        tid = super().register(t, src, untouched)
        rec = self.tuples[tid]
        rec.setdefault("event_kind", "dict")
        rec.setdefault("event_id", self.ids.event[norm(t["event"])]["id"])
        rec.setdefault("anchor", None)
        rec.setdefault("all_dict_values", True)
        rec.setdefault("candidate_name", [])
        rec.setdefault("event_fragments", [rec["event"]])
        rec.setdefault("extra_sites", [])
        rec.setdefault("extra_courses", [])
        return tid

    def register_raw(self, text, groups, untouched, src, anchor):
        """수정 3: 미등록 조각이 있는 complications 이름 → 이름마다 고유한 raw_name 튜플."""
        all_spans = [s for g in groups for m in g["members"] for s in m["spans"]]
        events = list(dict.fromkeys(s["canonical"] for s in all_spans if s["kind"] == "event"))
        sites = list(dict.fromkeys((s["kind"], s["canonical"]) for s in all_spans if s["kind"] in ("relative", "site")))
        courses = list(dict.fromkeys(s["canonical"] for s in all_spans if s["kind"] == "course"))
        site = sites[0] if len(sites) == 1 else None
        course = courses[0] if len(courses) == 1 else "미상"
        if site is None:
            site_id, site_label, site_kind = "none", None, "none"
        elif site[0] == "relative":
            site_id, site_label, site_kind = self.ids.rsite[norm(site[1])]["id"], site[1], "relative"
        else:
            site_id, site_label, site_kind = self.ids.site[norm(site[1])]["id"], site[1], "site"
        cid = self.ids.course[norm(course)]["id"]
        event_id = f"RAW:{anchor}"
        tid = mkid("ADV", f"{event_id}|{site_id}|{cid}|{anchor}")
        rec = self.tuples.get(tid)
        if rec is None:
            cat = self.ids.event[norm(events[0])]["category"] if events else None
            rec = {"id": tid, "event_kind": "raw_name", "event": text, "event_id": event_id, "event_category": cat, "site_kind": site_kind, "site": site_label, "site_id": site_id, "course": course, "course_id": cid,
                   "status": "partial", "unregistered_fragments": list(untouched), "origins": [], "sources": [], "anchor": anchor, "all_dict_values": False, "candidate_name": list(untouched),
                   "event_fragments": events, "extra_sites": [s[1] for s in sites] if len(sites) != 1 else [], "extra_courses": list(courses) if len(courses) != 1 else []}
            self.tuples[tid] = rec
        rec["sources"].append(src)
        if src["origin"] not in rec["origins"]:
            rec["origins"].append(src["origin"])
        return tid

    def run_text(self, text, src, identity=False):
        groups = self.split(text)
        tuples, untouched = self.assemble(groups)
        spans = [(s["kind"], s["canonical"], s["text"]) for g in groups for m in g["members"] for s in m["spans"]]
        if identity and untouched:
            tid = self.register_raw(text, groups, untouched, src, src["locator"])
            r = self.tuples[tid]
            return {"text": text, "event_kind": "raw_name", "tuples": [(r["event"], r["site"], r["course"])], "dict_tuples": [(t["event"], t["site"][1] if t["site"] else None, t["course"]) for t in tuples], "tuple_ids": [tid],
                    "unregistered": untouched, "candidate_name": untouched, "event_fragments": r["event_fragments"], "spans": spans, "locator": src["locator"], "anchor": src["locator"]}
        ids = [self.register(t, src, untouched) for t in tuples]
        return {"text": text, "event_kind": "dict" if ids else None, "tuples": [(t["event"], t["site"][1] if t["site"] else None, t["course"], t["course_basis"]) for t in tuples], "tuple_ids": ids, "unregistered": untouched,
                "match_status": ("linked" if ids and not untouched else "partial" if ids else "unlinked"), "spans": spans, "locator": src.get("locator")}


def adverse_phrases23(L):
    """v2 표현 레코드 전부 + 원장 locator(file:path@modality/순번)."""
    seq = Counter()
    out = []
    for kind, text, src in V2.adverse_phrases(L):
        key = (src["file"], src["path"], src.get("modality"))
        rec = src.get("record")
        if rec is None:
            rec = seq[key]
            seq[key] += 1
        src = dict(src, locator=locator(src["file"], src["path"], f"{src.get('modality')}/{rec}"))
        out.append((kind, text, src))
    return out


def run_adverse(ids, rules, L):
    AT = AdverseTuples23(ids)
    comp_rows = []
    for cat in L["complications.json"]["categories"]:
        for i, c in enumerate(cat["complications"]):
            loc = locator("complications.json", "categories[].complications[].name", f"{cat['id']}/{i}")
            r = AT.run_text(c["name"], {"origin": "complications", "file": "complications.json", "path": "categories[].complications[].name", "modality": cat["id"], "record": i, "locator": loc}, identity=True)
            r.update({"modality": cat["id"], "severity": c.get("severity"), "record": i})
            comp_rows.append(r)
    comp_tuple_ids = list(dict.fromkeys(x for r in comp_rows for x in r["tuple_ids"]))
    expr_rows = []
    for kind, text, src in adverse_phrases23(L):
        r = AT.run_text(text, dict(src, kind=kind))
        r.update({"kind": kind, "modality": src.get("modality"), "origin": src["origin"], "path": src["path"], "context": src.get("context")})
        if kind == "evidence_statement" and src.get("patient_ko"):
            r2 = AT.run_text(src["patient_ko"], dict(src, kind="patient_text", lang="ko", path="categories.{code}.adverse_effects[].patient_ko", origin="literature.patient_ko", locator=src["locator"].replace(".statement@", ".patient_ko@")))
            r["patient_ko"] = {"text": src["patient_ko"], "tuples": r2["tuples"], "tuple_ids": r2["tuple_ids"], "unregistered": r2["unregistered"], "match_status": r2["match_status"]}
            r["tuple_ids_union"] = list(dict.fromkeys(r["tuple_ids"] + r2["tuple_ids"]))
            r["basis"] = "both" if r["tuple_ids"] and r2["tuple_ids"] else "statement" if r["tuple_ids"] else "patient_ko" if r2["tuple_ids"] else "none"
            unreg_any = bool(r["unregistered"] or r2["unregistered"])
            r["match_status"] = "linked" if r["tuple_ids_union"] and not unreg_any else "partial" if r["tuple_ids_union"] else "unlinked"
        else:
            r["tuple_ids_union"] = r["tuple_ids"]
        r["linked"] = bool(r["tuple_ids_union"])
        expr_rows.append(r)
    A = AT.tuples
    adv_folded = []
    for tid in comp_tuple_ids:
        rows_ = [r for r in comp_rows if tid in r["tuple_ids"]]
        names = [f"{r['text']} [{r['modality']}]" for r in rows_]
        own_unreg = list(dict.fromkeys(u for r in rows_ for u in r["unregistered"]))
        t = A[tid]
        adv_folded.append({"adverse_id": tid, "event_kind": t["event_kind"], "event": t["event"], "category": t["event_category"], "site_kind": t["site_kind"], "site": t["site"], "course": t["course"], "status": "partial" if own_unreg else "complete",
                           "all_dict_values": t["all_dict_values"], "anchor": t["anchor"], "n_names": len(names), "names": names, "unregistered": own_unreg, "event_fragments": t["event_fragments"], "extra_sites": t["extra_sites"], "extra_courses": t["extra_courses"]})
    adv_folded.sort(key=lambda x: (-x["n_names"], x["event_kind"], x["category"] or "", x["event"]))
    adv_unreg = Counter()
    adv_unreg_by_origin = defaultdict(Counter)
    for r in comp_rows:
        for u in r["unregistered"]:
            adv_unreg[u] += 1
            adv_unreg_by_origin["complications"][u] += 1
    for r in expr_rows:
        for u in r["unregistered"]:
            adv_unreg[u] += 1
            adv_unreg_by_origin[r["kind"]][u] += 1
        if r.get("patient_ko"):
            for u in r["patient_ko"]["unregistered"]:
                adv_unreg[u] += 1
                adv_unreg_by_origin["patient_text(ko)"][u] += 1

    def kind_summary(kind):
        rows = [r for r in expr_rows if r["kind"] == kind]
        return {"n": len(rows), "linked": sum(1 for r in rows if r["linked"]), "unlinked": sum(1 for r in rows if not r["linked"]),
                "match_status": dict(Counter(r["match_status"] for r in rows)),
                "distinct_tuples": len({x for r in rows for x in r["tuple_ids_union"]}),
                "new_tuples_not_from_complications": len({x for r in rows for x in r["tuple_ids_union"] if "complications" not in A[x]["origins"]})}

    raw = [t for t in A.values() if t["event_kind"] == "raw_name"]
    dict_t = [t for t in A.values() if t["event_kind"] == "dict"]
    af2 = [f for f in adv_folded if f["n_names"] >= 2]
    # 수정 2 실측: LOP · 이름 안에 사건 둘 이상 + 수식어
    lop = [r for r in comp_rows if "LOP" in r["text"]]
    course_split = [{"name": f"{r['text']} [{r['modality']}]", "event_kind": r["event_kind"], "tuples": r.get("dict_tuples") if r["event_kind"] == "raw_name" else [t[:3] for t in r["tuples"]]} for r in comp_rows
                    if len({t[0] for t in (r.get("dict_tuples") or [t[:3] for t in r["tuples"]])}) >= 1 and any(c in r["text"] for c in ("일시적", "지연성", "가역적", "Transient", "Delayed", "영구", "Late-Onset"))]
    summary = OrderedDict([
        ("complications_names", len(comp_rows)),
        ("complications_names_with_tuple", sum(1 for r in comp_rows if r["tuple_ids"])),
        ("complications_names_without_tuple", [f"{r['text']} [{r['modality']}]" for r in comp_rows if not r["tuple_ids"]]),
        ("complications_names_multi_tuple", sum(1 for r in comp_rows if len(r["tuple_ids"]) >= 2)),
        ("complications_names_raw", sum(1 for r in comp_rows if r["event_kind"] == "raw_name")),
        ("complications_names_dict", sum(1 for r in comp_rows if r["event_kind"] == "dict")),
        ("complications_distinct_tuples", len(comp_tuple_ids)),
        ("complications_distinct_tuples_dict", sum(1 for t in comp_tuple_ids if A[t]["event_kind"] == "dict")),
        ("complications_distinct_tuples_raw", sum(1 for t in comp_tuple_ids if A[t]["event_kind"] == "raw_name")),
        ("complications_fold_ratio", round(len(comp_tuple_ids) / len(comp_rows), 3)),
        ("complications_tuples_with_2plus_names", len(af2)),
        ("complications_folded_all_dict_values", sum(1 for f in af2 if f["all_dict_values"] and not f["unregistered"])),
        ("complications_folded_with_unregistered", sum(1 for f in af2 if f["unregistered"])),
        ("complications_by_course", dict(Counter(A[t]["course"] for t in comp_tuple_ids))),
        ("complications_by_course_dict_only", dict(Counter(A[t]["course"] for t in comp_tuple_ids if A[t]["event_kind"] == "dict"))),
        ("complications_by_site_kind", dict(Counter(A[t]["site_kind"] for t in comp_tuple_ids))),
        ("complications_by_category", dict(Counter(A[t]["event_category"] for t in comp_tuple_ids))),
        ("event_dictionary_values", len(ids.event)),
        ("event_dictionary_used_by_complications", len({A[t]["event"] for t in comp_tuple_ids if A[t]["event_kind"] == "dict"})),
        ("event_dictionary_unused", sorted(set(e["label"] for e in ids.event.values()) - {A[t]["event"] for t in comp_tuple_ids if A[t]["event_kind"] == "dict"})),
        ("course_dictionary_values", len(ids.course)),
        ("relative_site_values", len(ids.rsite)),
        ("course_member_only", True),
        ("course_split_examples", course_split),
        ("lop", [{"name": r["text"], "event_kind": r["event_kind"], "tuples": [t[:3] for t in r["tuples"]], "dict_tuples": r.get("dict_tuples")} for r in lop]),
        ("expressions", OrderedDict((k, kind_summary(k)) for k in ["safety_phrase", "emergency_sign", "symptom_phrase", "evidence_statement"])),
        ("expressions_by_origin", OrderedDict((o, {"n": sum(1 for r in expr_rows if r["origin"] == o), "linked": sum(1 for r in expr_rows if r["origin"] == o and r["linked"]), "partial": sum(1 for r in expr_rows if r["origin"] == o and r["match_status"] == "partial")}) for o in dict.fromkeys(r["origin"] for r in expr_rows))),
        ("expressions_total", {"n": len(expr_rows), "linked": sum(1 for r in expr_rows if r["linked"]), "unlinked": sum(1 for r in expr_rows if not r["linked"]), "match_status": dict(Counter(r["match_status"] for r in expr_rows)), "patient_text_records": 4 * sum(1 for r in expr_rows if r["kind"] == "evidence_statement")}),
        ("expressions_raw_name_tuples", sum(1 for t in A.values() if t["event_kind"] == "raw_name" and "complications" not in t["origins"])),
        ("literature_basis", dict(Counter(r.get("basis") for r in expr_rows if r["kind"] == "evidence_statement"))),
        ("tuples_total", len(A)),
        ("tuples_dict", len(dict_t)),
        ("tuples_raw_name", len(raw)),
        ("tuples_by_origin", OrderedDict((o, sum(1 for t in A.values() if o in t["origins"])) for o in dict.fromkeys(o for t in A.values() for o in t["origins"]))),
        ("tuples_status", dict(Counter(t["status"] for t in A.values()))),
        ("tuples_by_course", dict(Counter(t["course"] for t in A.values()))),
        ("tuples_by_site_kind", dict(Counter(t["site_kind"] for t in A.values()))),
        ("tuples_by_category", dict(Counter(t["event_category"] for t in A.values()))),
        ("tuples_all_dict_values", sum(1 for t in A.values() if t["all_dict_values"])),
        ("tuples_with_2plus_names_raw", sum(1 for f in af2 if f["event_kind"] == "raw_name")),
        ("folded_with_2plus_names", len(af2)),
        ("folded_with_partial_name", sum(1 for f in af2 if f["status"] == "partial")),
        ("folded_partial_detail", [{"event": f["event"], "site": f["site"], "course": f["course"], "names": f["names"], "unregistered": f["unregistered"]} for f in af2 if f["status"] == "partial"]),
        ("unregistered_distinct", len(adv_unreg)),
        ("unregistered_total", sum(adv_unreg.values())),
        ("unregistered_all", adv_unreg.most_common()),
        ("unregistered_by_origin", {k: v.most_common() for k, v in adv_unreg_by_origin.items()}),
    ])
    return OrderedDict([("summary", summary), ("tuples", list(A.values())), ("complications", comp_rows), ("folded", adv_folded), ("expressions", expr_rows)])


# ---------------------------------------------------------------------------
# 전체 실행 · 집계
# ---------------------------------------------------------------------------
def run_all(dic_json, rules, L, resolve_rules=None):
    if resolve_rules is None:
        sys.path.insert(0, HERE)
        import erd_spec_v23
        resolve_rules = erd_spec_v23.RESOLVE_RULES
    ids = V2.Ids(dic_json, L)
    lex = V2.V11.Lexicon(with_alias(dic_json))
    PT = ProcedureTuples23(lex, resolve_rules, ids, L)
    PT.run_catalog()
    cat_recs = list(PT.catalog.values())
    n_cat = len(cat_recs)
    cat_tuple_ids = [r["procedure_id"] for r in cat_recs if r.get("procedure_id")]
    cat_distinct = list(dict.fromkeys(cat_tuple_ids))
    refs, market = V2.procedure_slots(L, lex)
    ref_rows = OrderedDict()
    for slot, items in refs.items():
        rows, seen = [], set()
        for label, hint, types in items:
            if (label, hint) in seen:
                continue
            seen.add((label, hint))
            rows.append(PT.run_reference(label, hint, "reference", slot))
        ref_rows[slot] = rows
    mk_rows, seen = [], set()
    for label, hint, types in market[1]:
        if (label, hint) in seen:
            continue
        seen.add((label, hint))
        mk_rows.append(PT.run_reference(label, hint, "market_pricing", market[0]))
    T = PT.tuples

    def tids_of(r):
        return [r.get("procedure_id")] if r["result"] == "tuple" else r.get("member_ids", []) if r["result"] == "combo_ref" else []

    def slot_summary(rows):
        c = Counter(r["result"] for r in rows)
        st = Counter(r.get("status") for r in rows if r["result"] in ("tuple", "combo_ref"))
        return {"n": len(rows), "tuple": c.get("tuple", 0), "combo_ref": c.get("combo_ref", 0), "node": c.get("node", 0), "unresolved": c.get("unresolved", 0), "none": c.get("none", 0), "complete": st.get("complete", 0), "partial": st.get("partial", 0),
                "unresolved_by_reason": dict(Counter(r.get("unresolved_reason") for r in rows if r["result"] == "unresolved")),
                "node_by_kind": dict(Counter(r.get("end_kind") for r in rows if r["result"] == "node")),
                "distinct_tuples": len({x for r in rows for x in tids_of(r) if x}),
                "new_tuples_not_from_catalog": len({x for r in rows for x in tids_of(r) if x and "catalog_item" not in T[x]["origins"]}),
                "whole_match": sum(1 for r in rows if r.get("whole_match")),
                "by_what_kind": dict(Counter(T[x]["what_kind"] for r in rows for x in tids_of(r) if x))}

    folded = []
    for tid in cat_distinct:
        names = [r for r in cat_recs if r.get("procedure_id") == tid or tid in r.get("member_ids", [])]
        t = T[tid]
        own_unreg = list(dict.fromkeys(u for r in names for u in r.get("unregistered", [])))
        folded.append({"procedure_id": tid, "what_kind": t["what_kind"], "what": t["what_label"], "site": t["site"], "technique": t["technique"], "technique_origin": t["technique_origin"], "status": t["status"],
                       "n_items": len(names), "items": [f"{r['name']}[{r['family']}]" for r in names], "item_status": [r.get("status") for r in names], "unregistered": own_unreg,
                       "all_dict_values": t["all_dict_values"], "self_reason": [r.get("self_reason") for r in names], "keys": [[r["family"], r["name"]] for r in names]})
    folded.sort(key=lambda x: (-x["n_items"], x["what_kind"], x["what"]))
    multi_anchor = []
    for t in T.values():
        anchors = list(dict.fromkeys(s["anchor"] for s in t["sources"]))
        if len(anchors) >= 2:
            multi_anchor.append({"procedure_id": t["id"], "what_kind": t["what_kind"], "what": t["what_label"], "site": t["site"], "technique": t["technique"], "all_dict_values": t["all_dict_values"],
                                 "n_anchors": len(anchors), "labels": list(dict.fromkeys(f"{s['label']}" + (f"@{s.get('slot', '')[:20]}" if s.get("slot") else "") for s in t["sources"]))})
    inh = []
    for fam, techs in sorted(ids.family_tech.items()):
        if len(techs) != 1:
            continue
        ts = [t for t in T.values() if t["technique_id"] == "none" and str(t.get("family")) == fam]
        cat_items = [r for r in cat_recs if r["family"] == fam and r.get("technique_origin") == "none"]
        inh.append({"kind": "canonical_mapping", "from_ref": f"R5:{fam}", "to_technique": techs[0], "to_id": ids.tech[norm(techs[0])]["id"], "scope": [r["catalog_item_id"] for r in cat_items], "scope_note": f"technique=none 인 {fam} 분류 항목의 CAT- id 전부(참조 튜플은 REF- 로 따로)",
                    "tuples": len(ts), "catalog_items": len(cat_items), "items": [r["name"] for r in cat_items]})
    unreg_all = Counter()
    unreg_by_origin = {"catalog_item": Counter(), "reference": Counter(), "market_pricing": Counter()}
    for r in cat_recs:
        for u in r.get("unregistered", []):
            unreg_all[u] += 1
            unreg_by_origin["catalog_item"][u] += 1
    for rows in ref_rows.values():
        for r in rows:
            for u in r.get("unregistered", []):
                unreg_all[u] += 1
                unreg_by_origin["reference"][u] += 1
    for r in mk_rows:
        for u in r.get("unregistered", []):
            unreg_all[u] += 1
            unreg_by_origin["market_pricing"][u] += 1
    cat_tuples = [T[i] for i in cat_distinct]
    tup_rows = [r for r in cat_recs if r["result"] == "tuple"]
    fold2 = [f for f in folded if f["n_items"] >= 2]
    none_t = [t for t in T.values() if not t["all_dict_values"]]
    EE = edge_ends(PT, ref_rows, mk_rows, cat_recs, L, ids)
    proc_summary = OrderedDict([
        ("catalog_items", n_cat),
        ("catalog_result", dict(Counter(r["result"] for r in cat_recs))),
        ("catalog_distinct_tuples", len(cat_distinct)),
        ("catalog_fold_ratio", round(len(cat_distinct) / n_cat, 3) if n_cat else None),
        ("catalog_tuples_with_2plus_items", len(fold2)),
        ("catalog_items_in_folded_tuples", sum(f["n_items"] for f in fold2)),
        ("catalog_folded_all_dict_values", sum(1 for f in fold2 if f["all_dict_values"])),
        ("catalog_folded_with_partial_item", sum(1 for f in fold2 if any(s == "partial" for s in f["item_status"]))),
        ("catalog_folded_with_2plus_partial_items", sum(1 for f in fold2 if sum(1 for s in f["item_status"] if s == "partial") >= 2)),
        ("catalog_fallback_to_parent", sum(1 for r in cat_recs if str(r.get("what_basis", "")).startswith("parent_subcategory"))),
        ("catalog_by_what_kind", dict(Counter(r.get("what_kind") for r in tup_rows))),
        ("catalog_by_what_basis", dict(Counter(str(r.get("what_basis", "")).split(":")[0] if not str(r.get("what_basis", "")).startswith("self:") else str(r.get("what_basis", "")) for r in tup_rows))),
        ("catalog_status", dict(Counter(r.get("status") for r in tup_rows))),
        ("catalog_whole_match", sum(1 for r in cat_recs if r.get("whole_match"))),
        ("catalog_self_items", sum(1 for r in tup_rows if r.get("what_kind") == "catalog_item")),
        ("catalog_self_by_reason", dict(Counter(r.get("self_reason") for r in tup_rows if r.get("what_kind") == "catalog_item"))),
        ("catalog_self_with_site", sum(1 for r in tup_rows if r.get("what_kind") == "catalog_item" and r.get("site"))),
        ("catalog_site_none", sum(1 for r in tup_rows if not r.get("site"))),
        ("catalog_site_none_ratio", round(sum(1 for r in tup_rows if not r.get("site")) / max(1, len(tup_rows)), 3)),
        ("catalog_technique", dict(Counter(r.get("technique_origin") for r in tup_rows))),
        ("catalog_technique_none_ratio", round(sum(1 for r in tup_rows if r.get("technique_origin") == "none") / max(1, len(tup_rows)), 3)),
        ("catalog_tuple_site_none_ratio", round(sum(1 for t in cat_tuples if t["site_id"] == "none") / max(1, len(cat_tuples)), 3)),
        ("catalog_tuple_technique_none_ratio", round(sum(1 for t in cat_tuples if t["technique_id"] == "none") / max(1, len(cat_tuples)), 3)),
        ("reference_slots", OrderedDict((k, slot_summary(v)) for k, v in ref_rows.items())),
        ("reference_total", slot_summary([r for v in ref_rows.values() for r in v])),
        ("market_pricing", slot_summary(mk_rows)),
        ("tuples_total", len(T)),
        ("tuples_by_origin", {k: sum(1 for t in T.values() if k in t["origins"]) for k in ["catalog_item", "reference", "market_pricing"]}),
        ("tuples_by_what_kind", dict(Counter(t["what_kind"] for t in T.values()))),
        ("tuples_status", dict(Counter(t["status"] for t in T.values()))),
        ("tuples_site_none_ratio", round(sum(1 for t in T.values() if t["site_id"] == "none") / max(1, len(T)), 3)),
        ("tuples_technique_none_ratio", round(sum(1 for t in T.values() if t["technique_id"] == "none") / max(1, len(T)), 3)),
        ("tuples_any_none_ratio", round(sum(1 for t in T.values() if t["site_id"] == "none" or t["technique_id"] == "none") / max(1, len(T)), 3)),
        ("tuples_technique_origin", dict(Counter(t["technique_origin"] for t in T.values()))),
        ("tuples_dict_what_site_none_ratio", round(sum(1 for t in T.values() if t["what_kind"] in DICT_WHAT_KINDS and t["site_id"] == "none") / max(1, sum(1 for t in T.values() if t["what_kind"] in DICT_WHAT_KINDS)), 3)),
        ("tuples_all_dict_values", sum(1 for t in T.values() if t["all_dict_values"])),
        ("tuples_anchored", len(none_t)),
        ("tuples_with_2plus_anchors", len(multi_anchor)),
        ("tuples_with_2plus_anchors_not_all_dict", sum(1 for m in multi_anchor if not m["all_dict_values"])),
        ("technique_inherited", sum(1 for t in T.values() if t["technique_origin"] == "inherited")),
        ("families_without_single_technique", sorted(f for f, v in ids.family_tech.items() if len(v) != 1)),
        ("inheritance_candidates", [{k: v for k, v in c.items() if k not in ("items", "scope")} for c in inh]),
        ("code_references_node", sum(1 for rows in ref_rows.values() for r in rows if r["result"] == "node")),
        ("edge_ends_total", EE["total"]),
        ("edge_ends_total_n", EE["total_n"]),
        ("edge_ends_by_relation", EE["by_relation"]),
        ("edge_ends_slots", {"text": EE["text_slots"], "code": EE["code_slots"], "relations": EE["relations_covered"]}),
        ("unregistered_distinct", len(unreg_all)),
        ("unregistered_total", sum(unreg_all.values())),
        ("unregistered_top30", unreg_all.most_common(30)),
        ("unregistered_top30_by_origin", {k: v.most_common(30) for k, v in unreg_by_origin.items()}),
    ])
    adv = run_adverse(ids, rules, L)
    out = OrderedDict([
        ("erd_version", "v2.3"), ("rules", rules["name"]), ("fallback_to_parent", False), ("fold_condition", "세 칸 전부 사전 값일 때만"), ("technique_inheritance", False), ("edge_end", "procedure"), ("course_member_only", True), ("adverse_fold_unregistered", False),
        ("procedure", OrderedDict([("summary", proc_summary), ("tuples", list(T.values())), ("catalog", cat_recs), ("folded", folded), ("multi_anchor", multi_anchor),
                                   ("inheritance_candidates", inh), ("references", ref_rows), ("market_pricing", mk_rows), ("edge_ends", EE["rows"])])),
        ("adverse", adv),
    ])
    return out


def v21_split(R, v21=None):
    sp = V22.v21_split(R, v21)
    for x in sp:
        for d in x["dest"]:
            if d["result"] == "node":
                d["tuple"] = "node(끝=" + ("계열" if "modality" in d["tuple"] else "노드") + " · 튜플 없음)"
    return sp


def load_v22_summary():
    try:
        j = json.load(open(os.path.join(HERE, "erd-v2.2-tuples.json"), encoding="utf-8"))
        return j["procedure"]["summary"], j["adverse"]["summary"]
    except (FileNotFoundError, KeyError):
        return None, None


def _kv(d):
    return ", ".join(f"{k}={v}" for k, v in (d or {}).items())


# ---------------------------------------------------------------------------
# 표 (md) — §9.5 (v2.2 수치 나란히 + 9.5.8 엣지 끝 분포) · §9.6 (v2.2 나란히)
# ---------------------------------------------------------------------------
def procedure_md(R, v22s=None):
    s = R["procedure"]["summary"]
    v22s = v22s or load_v22_summary()[0] or {}
    g = lambda k, d="—": v22s.get(k, d)  # noqa
    o = []
    A = o.append
    A("#### 9.5.1 분류 항목 521 → 튜플 (v2.2 → v2.3 나란히 · ① 규칙은 v2.2 그대로)")
    A("")
    A(md_table(["항목", "v2.2", "v2.3"], [
        ("분류 항목", g("catalog_items"), s["catalog_items"]),
        ("분해 결과", _kv(g("catalog_result", {})), _kv(s["catalog_result"])),
        ("튜플 수(distinct)", f"**{g('catalog_distinct_tuples')}** (비율 {g('catalog_fold_ratio')})", f"**{s['catalog_distinct_tuples']}** (521 → N · 비율 {s['catalog_fold_ratio']})"),
        ("둘 이상 항목이 접힌 튜플", f"{g('catalog_tuples_with_2plus_items')} 개 튜플에 항목 {g('catalog_items_in_folded_tuples')} 개", f"{s['catalog_tuples_with_2plus_items']} 개 튜플에 항목 {s['catalog_items_in_folded_tuples']} 개"),
        ("접힌 튜플 중 세 칸 전부 사전 값", f"{g('catalog_folded_all_dict_values')} / {g('catalog_tuples_with_2plus_items')}", f"{s['catalog_folded_all_dict_values']} / {s['catalog_tuples_with_2plus_items']}"),
        ("what 축", _kv(g("catalog_by_what_kind", {})) + " · 근거: " + _kv(g("catalog_by_what_basis", {})), _kv(s["catalog_by_what_kind"]) + " · 근거: " + _kv(s["catalog_by_what_basis"])),
        ("항목 자신(catalog_item)이 what 인 항목", g("catalog_self_items"), f"{s['catalog_self_items']} (사유: {_kv(s['catalog_self_by_reason'])} · 그중 부위 칸 있음 {s['catalog_self_with_site']})"),
        ("site 축", f"none {g('catalog_site_none')} / 항목 기준 {g('catalog_site_none_ratio')} · 튜플 기준 {g('catalog_tuple_site_none_ratio')}", f"none {s['catalog_site_none']} / 항목 기준 none 비율 {s['catalog_site_none_ratio']} · 튜플 기준 {s['catalog_tuple_site_none_ratio']}"),
        ("technique 축", _kv(g("catalog_technique", {})) + f" · 항목 기준 none {g('catalog_technique_none_ratio')}", _kv(s["catalog_technique"]) + f" · 항목 기준 none 비율 {s['catalog_technique_none_ratio']} · 튜플 기준 {s['catalog_tuple_technique_none_ratio']}"),
        ("항목 상태", _kv(g("catalog_status", {})), _kv(s["catalog_status"])),
    ]))
    A("")
    A("#### 9.5.2 접힌 결과 — 둘 이상의 분류 항목이 같은 튜플로 간 것 전부 (세 칸 전부 사전 값만 남는다 · v2.2 와 같은 규칙)")
    A("")
    rows = [(i + 1, f["what_kind"], f["what"], f["site"] or "none", f"{f['technique'] or 'none'}({f['technique_origin']})", f["n_items"], " · ".join(f["items"]))
            for i, f in enumerate(x for x in R["procedure"]["folded"] if x["n_items"] >= 2)]
    A(md_table(["#", "what 종류", "what", "site", "technique", "항목 수", "접힌 분류 항목(전부)"], rows) if rows else "(없음 — 접힌 분류 항목 0. 세 칸 전부 사전 값인 분류 항목 튜플이 서로 같은 경우가 없다 · v2.2 와 같다)")
    A("")
    sp = R["procedure"].get("v21_none_fold_split") or []
    A(f"v2.1 에서 미상 칸이 있는데 서로 다른 라벨이 한 튜플로 접혔던 것 {len(sp)} → v2.3 에서도 전부 갈라져 있다 {sum(1 for x in sp if x['split'])}/{len(sp)} (v2.2 §9.5.2 표와 같음 · M 코드 참조는 v2.3 에서 튜플이 아니라 노드 끝 `node`). 표는 `erd-v2.3-tuples.json → procedure.v21_none_fold_split`.")
    A("")
    A("#### 9.5.3 항목 하나짜리 튜플 (접히지 않은 것 전부 · v2.2 와 동일 규칙)")
    A("")
    cat = {(r["family"], r["name"]): r for r in R["procedure"]["catalog"]}
    rows = []
    for i, f in enumerate(x for x in R["procedure"]["folded"] if x["n_items"] == 1):
        r = cat.get(tuple(f["keys"][0]))
        ex = ""
        if r:
            ex = "; ".join(x for x in [("P:" + ",".join(r.get("extra_primaries") or [])) if r.get("extra_primaries") else "", ("S:" + ",".join(r.get("extra_sites") or [])) if r.get("extra_sites") else ""] if x)
        rows.append((i + 1, f["what_kind"], f["what"], f["site"] or "none", f"{f['technique'] or 'none'}", f["status"], f["items"][0], ", ".join(f["unregistered"]) or "—", ex or "—"))
    A(md_table(["#", "what 종류", "what", "site", "technique", "상태", "분류 항목", "미등록 조각(candidate_name)", "extra(실값 · P=primary S=site)"], rows))
    A("")
    A("#### 9.5.4 참조 자리 전부(②) + market-pricing(③) → 튜플 (v2.3: M 코드·하위분류 id 만 적힌 참조는 `node`(노드 끝 · 튜플 없음) · 그 밖은 v2.2 그대로)")
    A("")
    rows = []
    v22slots = g("reference_slots", {})

    def srow(name, v, w):
        return (name, v["n"], v["tuple"], v["combo_ref"], f"{v['node']}" + (f"({_kv(v['node_by_kind'])})" if v["node"] else ""), v["unresolved"], _kv(v["unresolved_by_reason"]) or "—", v["none"], v["distinct_tuples"], v["new_tuples_not_from_catalog"],
                (f"{w['tuple']}/{w['combo_ref']}/{w['unresolved']}/{w['distinct_tuples']}" if w else "—"))
    for k, v in s["reference_slots"].items():
        rows.append(srow(k, v, v22slots.get(k)))
    rows.append(srow("**② 합계**", s["reference_total"], g("reference_total", None)))
    rows.append(srow("**③ market-pricing.items[].name (122)**", s["market_pricing"], g("market_pricing", None)))
    A(md_table(["참조 자리", "건", "튜플", "combo_ref", "node(v2.3)", "미해결(⑨)", "미해결 사유", "튜플 불가", "distinct 튜플", "①에 없는 새 튜플", "v2.2 튜플/combo/미해결/distinct"], rows))
    A("")
    A(f"②·③ 튜플의 what 종류: ② {_kv(s['reference_total']['by_what_kind'])} · ③ {_kv(s['market_pricing']['by_what_kind'])}. v2.2 에서 튜플이던 코드 참조 {s['code_references_node']} 건(sequence_order 의 M 코드·하위분류 id)은 v2.3 에서 노드 끝이다(엣지 끝 규칙 · §9.5.8).")
    A("")
    A("참조 행 전부 (라벨 → 결과):")
    A("")
    TT = {t["id"]: t for t in R["procedure"]["tuples"]}
    for k, rows_ in list(R["procedure"]["references"].items()) + [("market-pricing.items[].name (122)", R["procedure"]["market_pricing"])]:
        parts = []
        for r in rows_:
            lab = f"`{r['label']}`" + (f"@{r['hint']}" if r.get("hint") else "")
            if r["result"] == "tuple":
                t = TT[r["procedure_id"]]
                parts.append(lab + f" → ({t['what_kind']}:{t['what_label']} × {t['site'] or 'none'} × {t['technique'] or 'none'})")
            elif r["result"] == "combo_ref":
                ms = [f"{TT[m]['what_kind']}:{TT[m]['what_label']}×{TT[m]['site'] or 'none'}×{TT[m]['technique'] or 'none'}" for m in r["member_ids"]]
                parts.append(lab + " → combo_ref[" + " + ".join(ms) + "]")
            elif r["result"] == "node":
                parts.append(lab + f" → node:{r['end_kind']}")
            elif r["result"] == "unresolved":
                if r["unresolved_reason"] == "unregistered":
                    parts.append(lab + f" → 미해결 미등록[{','.join(r['unregistered'])}]")
                else:
                    parts.append(lab + f" → 미해결 {r['unresolved_reason']}[{','.join(str(x) for x in (r.get('detail') or []))}]")
            else:
                parts.append(lab + " → 튜플 불가")
        A(f"- **{k}**: " + " · ".join(parts))
    A("")
    A("#### 9.5.5 튜플 전체 집계 (① ② ③ 합집합 · v2.2 → v2.3)")
    A("")
    A(md_table(["항목", "v2.2", "v2.3"], [
        ("튜플 수", f"**{g('tuples_total')}**", f"**{s['tuples_total']}** (코드 참조 {s['code_references_node']} 건이 튜플에서 빠짐 — 노드 끝)"),
        ("원천별", _kv(g("tuples_by_origin", {})), _kv(s["tuples_by_origin"])),
        ("what 종류", _kv(g("tuples_by_what_kind", {})), _kv(s["tuples_by_what_kind"])),
        ("상태", _kv(g("tuples_status", {})), _kv(s["tuples_status"])),
        ("site none 비율", g("tuples_site_none_ratio"), f"{s['tuples_site_none_ratio']} (what 이 사전 값인 튜플만: {s['tuples_dict_what_site_none_ratio']})"),
        ("technique none 비율", f"{g('tuples_technique_none_ratio')} · 출처 " + _kv(g("tuples_technique_origin", {})), f"{s['tuples_technique_none_ratio']} · 출처 " + _kv(s["tuples_technique_origin"])),
        ("세 칸 전부 사전 값 튜플 / anchor 튜플", f"{g('tuples_all_dict_values')} / {g('tuples_anchored')}", f"{s['tuples_all_dict_values']} / {s['tuples_anchored']}"),
        ("서로 다른 anchor(항목·참조)가 둘 이상 들어간 튜플", g("tuples_with_2plus_anchors"), f"{s['tuples_with_2plus_anchors']} (그중 미상 칸 있는 것 {s['tuples_with_2plus_anchors_not_all_dict']})"),
        ("미등록 조각", f"distinct {g('unregistered_distinct')} · 총 {g('unregistered_total')}", f"distinct {s['unregistered_distinct']} · 총 {s['unregistered_total']}"),
    ]))
    A("")
    A("#### 9.5.6 R5 계열 기법 → 결정 kind `canonical_mapping` 후보 (적용하지 않음 · v2.3: scope = 분류 항목 CAT- id 목록)")
    A("")
    A("R5 계열 → 기법이 하나인 계열(procedure-profiles mechanism[]). 튜플에 붙이지 않는다. 사람이 승인하면 decision(kind=canonical_mapping, target={from_ref: \"R5:<계열>\", scope: [CAT- …]}, new_value={to_id: <기법 id>}, status=approved) 을 빌드가 적용 순서 ② 에서 읽어 scope 의 technique=none 튜플에 붙인다. scope 는 아래 항목의 CAT- id 목록(`erd-v2.3-tuples.json → procedure.inheritance_candidates[].scope`)이다.")
    A("")
    A(md_table(["#", "from_ref", "to (기법)", "to_id", "technique none 튜플", "scope(분류 항목 수)", "분류 항목(전부)"], [(i + 1, c["from_ref"], c["to_technique"], c["to_id"], c["tuples"], c["catalog_items"], " · ".join(c["items"])) for i, c in enumerate(R["procedure"]["inheritance_candidates"])]))
    A("")
    A(f"후보 불가 계열(R5 기법 둘 이상 또는 없음): {', '.join(s['families_without_single_technique'])}.")
    A("")
    A(f"#### 9.5.7 미등록 조각 상위 30 (v2.2 distinct {g('unregistered_distinct')}/총 {g('unregistered_total')} → v2.3 distinct {s['unregistered_distinct']}/총 {s['unregistered_total']})")
    A("")
    A("- 전체: " + " · ".join(f"`{f}`×{n}" for f, n in s["unregistered_top30"]))
    for k, v in s["unregistered_top30_by_origin"].items():
        A(f"- {k}: " + (" · ".join(f"`{f}`×{n}" for f, n in v) or "—"))
    A("")
    A("#### 9.5.8 엣지 자리별 끝 분포 (v2.3 수정 1 · `erd-v2.3-tuples.py` 실측 · 시술 축 엣지 R3·R9·R12·R15·R16·R17·R18 의 출처 자리 전부)")
    A("")
    A("끝 = procedure(참조가 튜플·combo_ref 멤버로 해결됨 · 분류 항목 id·레코드 자리) / modality(M 코드만 적힘) / subcategory(실존 하위분류 id 만) / product(제품 전용 자리·제품 레코드) / unresolved(⑨ · 끝 없음). "
      "「텍스트 자리」는 §9.2 참조 자리(②)를 §1.4 로 분해한 결과, 「코드·레코드 자리」는 원장 코드 키·레코드 소속을 그대로 센 것(건 = 그 자리의 참조·문구 수). anchor 튜플 = 미상 칸이 있는 procedure 끝(접히지 않지만 끝은 튜플). via = 참조가 분류 항목 이름과 일치해 그 항목의 튜플을 끝으로 쓴 수.")
    A("")
    rows = []
    for r in R["procedure"]["edge_ends"]:
        rows.append((r["relation"], r["kind"], r["slot"], r["n"], r["procedure"], r["modality"], r["subcategory"], r["product"], r["unresolved"], r["procedure_anchored"] if r["procedure_anchored"] is not None else "—", r["via_catalog_item"], r["note"]))
    tot = s["edge_ends_total"]
    rows.append(("**합계(③ 제외)**", "", "", s["edge_ends_total_n"], tot.get("procedure", 0), tot.get("modality", 0), tot.get("subcategory", 0), tot.get("product", 0), tot.get("unresolved", 0), "", "", ""))
    A(md_table(["관계", "자리 종류", "자리", "건", "procedure", "modality", "subcategory", "product", "unresolved", "anchor 튜플", "via 항목", "비고"], rows))
    A("")
    A("관계별 합계: " + " · ".join(f"**{k}** {_kv({kk: vv for kk, vv in v.items() if kk != 'n'})} (건 {v['n']})" for k, v in s["edge_ends_by_relation"].items()))
    A("")
    A("procedure 끝 전부(텍스트 자리 · 라벨 → 튜플 id 끝 4자리, via 는 CAT-):")
    A("")
    for r in R["procedure"]["edge_ends"]:
        if r["kind"] != "text":
            continue
        parts = []
        for e in r["ends"]:
            if e["end_kind"] == "procedure":
                pid = e["procedure_id"]
                tag = ",".join(x[-4:] for x in pid) if isinstance(pid, list) else pid[-4:]
                parts.append(f"`{e['label']}`" + (f"@{e['hint']}" if e.get("hint") else "") + f"→[{tag}]" + ("(via)" if e.get("via_catalog_item") else ""))
            elif e["end_kind"] in ("modality", "subcategory", "product"):
                parts.append(f"`{e['label']}`→{e['end_kind']}")
        A(f"- **{r['relation']} {r['slot']}**: " + (" · ".join(parts) or "—"))
    return "\n".join(o)


def adverse_md(R, v22a=None):
    s = R["adverse"]["summary"]
    v22a = v22a or load_v22_summary()[1] or {}
    g = lambda k, d="—": v22a.get(k, d)  # noqa
    o = []
    A = o.append
    A("#### 9.6.1 complications 65 → 튜플 (v2.2 → v2.3 나란히)")
    A("")
    A(md_table(["항목", "v2.2", "v2.3"], [
        ("이름", g("complications_names"), s["complications_names"]), ("튜플이 생긴 이름", g("complications_names_with_tuple"), s["complications_names_with_tuple"]),
        ("튜플이 안 생긴 이름(사건 조각 없음)", "; ".join(g("complications_names_without_tuple", [])) or "0", "; ".join(s["complications_names_without_tuple"]) or "0"),
        ("미등록 조각이 있는 이름 → raw_name 튜플(이름마다 고유)", "—(접혔다)", f"**{s['complications_names_raw']}** (사전 튜플 이름 {s['complications_names_dict']})"),
        ("사건이 둘 이상인 이름(튜플 둘 이상)", g("complications_names_multi_tuple"), s["complications_names_multi_tuple"]),
        ("튜플 수(distinct)", f"**{g('complications_distinct_tuples')}** (비율 {g('complications_fold_ratio')})", f"**{s['complications_distinct_tuples']}** (65 → N · 사전 튜플 {s['complications_distinct_tuples_dict']} + raw_name {s['complications_distinct_tuples_raw']} · 비율 {s['complications_fold_ratio']})"),
        ("둘 이상 이름이 접힌 튜플", g("complications_tuples_with_2plus_names"), f"{s['complications_tuples_with_2plus_names']} (전부 세 칸 사전 값·미등록 0: {s['complications_folded_all_dict_values']} · 미등록 조각 섞임 **{s['complications_folded_with_unregistered']}**)"),
        ("경과", _kv(g("complications_by_course", {})), _kv(s["complications_by_course"]) + f" (사전 튜플만 {_kv(s['complications_by_course_dict_only'])})"),
        ("부위", _kv(g("complications_by_site_kind", {})), _kv(s["complications_by_site_kind"])),
        ("분류", _kv(g("complications_by_category", {})), _kv(s["complications_by_category"])),
        ("사건 사전 최종 값", f"**{g('event_dictionary_values')}**", f"**{s['event_dictionary_values']}** (사전 튜플 이름이 쓴 값 {s['event_dictionary_used_by_complications']} · 안 쓰인 값: {', '.join(s['event_dictionary_unused']) or '없음'})"),
        ("경과 사전 값 · 상대 부위 사전 값", f"{g('course_dictionary_values')} · {g('relative_site_values')}", f"{s['course_dictionary_values']} · {s['relative_site_values']}"),
    ]))
    A("")
    A("#### 9.6.2 65 가 접힌 결과 — 튜플마다 어떤 이름들이 갔는지 전부 (v2.3 재실측 · raw_name 튜플은 이름 하나씩)")
    A("")
    rows = [(i + 1, f["event_kind"], f["category"] or "—", f["event"] if f["event_kind"] == "dict" else f"(raw) {f['event']}", f"{f['site'] or 'none'}({f['site_kind']})", f["course"], f["n_names"], " · ".join(f["names"]),
             ", ".join(f["unregistered"]) or "—", (", ".join(f["event_fragments"]) if f["event_kind"] == "raw_name" else "—") + (f" / S:{','.join(f['extra_sites'])}" if f["extra_sites"] else "") + (f" / C:{','.join(f['extra_courses'])}" if f["extra_courses"] else ""))
            for i, f in enumerate(R["adverse"]["folded"])]
    A(md_table(["#", "event_kind", "분류", "event", "site", "course", "이름 수", "접힌 complications 이름(전부)", "미등록 조각(candidate_name)", "raw_name 의 닿은 사건 조각(실값) / extra"], rows))
    A("")
    A("#### 9.6.2a 경과 규칙 실측 (수정 2 · 사건에 바로 붙은 수식어만) — 수식어가 있는 이름 전부")
    A("")
    A(md_table(["#", "이름", "event_kind", "튜플 (event, site, course)"], [(i + 1, x["name"], x["event_kind"], " + ".join(f"({t[0]}, {t[1] or 'none'}, {t[2]})" for t in x["tuples"])) for i, x in enumerate(s["course_split_examples"])]))
    A("")
    for x in s["lop"]:
        dt = " + ".join("(%s, %s, %s)" % (t[0], t[1] or "none", t[2]) for t in (x["dict_tuples"] or x["tuples"]))
        A(f"- LOP: 「{x['name']}」 → event_kind={x['event_kind']} · 사전 분해 {dt}" + (" — 이름에 미등록 조각(Procedural · &)이 있어 raw_name 튜플 하나로 남고, 사전 분해 결과는 event_fragments·dict_tuples 에 보존(adverse_tuple_assign 의 재료)" if x["event_kind"] == "raw_name" else ""))
    A("")
    A("#### 9.6.3 표현(adverse_expression) → 튜플 (v2.3: match_status linked / partial / unlinked)")
    A("")
    rows = [(k, v["n"], v["linked"], v["match_status"].get("partial", 0), v["unlinked"], v["distinct_tuples"], v["new_tuples_not_from_complications"]) for k, v in s["expressions"].items()]
    t = s["expressions_total"]
    rows.append(("**합계**", t["n"], t["linked"], t["match_status"].get("partial", 0), t["unlinked"], "", ""))
    A(md_table(["kind", "표현 수", "linked(R29)", "그중 partial(미등록 조각 있음)", "unlinked(null)", "distinct 튜플", "65 에 없던 새 튜플"], rows))
    A("")
    A("- 출처별(linked/전체 · partial): " + " · ".join(f"{k} {v['linked']}/{v['n']} · partial {v['partial']}" for k, v in s["expressions_by_origin"].items()))
    A(f"- v2.2: linked {g('expressions_total', {}).get('linked')}/{g('expressions_total', {}).get('n')} → v2.3 linked {t['linked']}/{t['n']} (경과 규칙이 바뀌어 닿는 튜플이 달라질 뿐 연결 수는 사건 조각이 정한다) · 표현이 만든 raw_name 튜플 {s['expressions_raw_name_tuples']} (표현은 정체성을 만들지 않는다)")
    A(f"- 문헌 32: statement/patient_ko 어느 쪽에서 닿았나 — " + ", ".join(f"{k}={v}" for k, v in s["literature_basis"].items()) + f" · patient_text 표현 레코드 {t['patient_text_records']}(4개 언어 × 32, 같은 레코드의 튜플을 따라감)")
    A("")
    A("#### 9.6.4 튜플 전체 집계 (65 + 표현 전부 · v2.2 → v2.3)")
    A("")
    A(md_table(["항목", "v2.2", "v2.3"], [
        ("튜플 수", f"**{g('tuples_total')}**", f"**{s['tuples_total']}** (사전 {s['tuples_dict']} + raw_name {s['tuples_raw_name']})"), ("원천별", _kv(g("tuples_by_origin", {})), _kv(s["tuples_by_origin"])),
        ("상태", _kv(g("tuples_status", {})), _kv(s["tuples_status"])), ("경과", _kv(g("tuples_by_course", {})), _kv(s["tuples_by_course"])),
        ("부위", _kv(g("tuples_by_site_kind", {})), _kv(s["tuples_by_site_kind"])), ("분류", _kv(g("tuples_by_category", {})), _kv(s["tuples_by_category"])),
        ("세 칸 전부 사전 값(접힘 가능) 튜플", "—", s["tuples_all_dict_values"]),
        ("미등록 조각", f"distinct {g('unregistered_distinct')} · 총 {g('unregistered_total')}", f"distinct {s['unregistered_distinct']} · 총 {s['unregistered_total']}"),
    ]))
    A("")
    A("표현에서 새로 생긴 튜플 전부(65 에 없던 것):")
    A("")
    new = [t for t in R["adverse"]["tuples"] if "complications" not in t["origins"]]
    A(md_table(["#", "분류", "event", "site", "course", "상태", "원천", "표현 수"], [(i + 1, t["event_category"], t["event"], f"{t['site'] or 'none'}({t['site_kind']})", t["course"], t["status"], ", ".join(t["origins"]), len(t["sources"])) for i, t in enumerate(new)]))
    A("")
    A("#### 9.6.5 미등록 조각 전부 (출처별 · 횟수) — 사전 추가는 실버 빌드의 결정 묶음(dictionary_add · adverse_tuple_assign)")
    A("")
    for k, v in s["unregistered_by_origin"].items():
        A(f"- **{k}** ({len(v)}): " + " · ".join(f"`{f}`×{n}" for f, n in v))
    A("")
    A("#### 9.6.6 미등록 조각 있는 이름이 접혔는가 — v2.3 재실측 (수정 3)")
    A("")
    A(f"- 둘 이상 이름이 접힌 부작용 튜플 {s['folded_with_2plus_names']} 중 미등록 조각 있는 이름이 섞인 튜플 **{s['folded_with_partial_name']}** (v2.2: {g('folded_with_partial_name')}). raw_name 튜플 {s['complications_distinct_tuples_raw']} 은 전부 이름 하나씩(접힘 0).")
    if s["folded_with_partial_name"]:
        A("")
        A(md_table(["#", "event", "site", "course", "접힌 이름(전부)", "미등록 조각"], [(i + 1, d["event"], d["site"] or "none", d["course"], " · ".join(d["names"]), ", ".join(d["unregistered"])) for i, d in enumerate(s["folded_partial_detail"])]))
    A("")
    A("v2.2 §9.6.6 의 12 튜플(미등록 조각이 있는 이름이 접혔던 것)이 v2.3 에서 어디로 갔는지 — 미등록 조각이 있는 이름은 raw_name 튜플(위 9.6.2 표의 `(raw)` 행), 미등록 0 인 이름끼리만 사전 튜플로 남는다. 「주사 통증 / 불편감」[M2] 은 더 이상 M7·M9·M16 의 통증과 접히지 않고, 「공기색전·카테터 관련 감염」[M16] 은 감염·색전 튜플에서 빠지며, 「구형구축 (…섬유성 결절)」[M7] 은 결절 튜플에서 빠진다(각각 raw_name · adverse_tuple_assign 의 대상).")
    return "\n".join(o)


def load_all():
    for name in ("erd-v2.3-dictionaries.json", "erd-v2.2-dictionaries.json"):
        if os.path.exists(os.path.join(HERE, name)):
            dic = json.load(open(os.path.join(HERE, name), encoding="utf-8"))
            break
    try:
        erd = json.load(open(os.path.join(HERE, "erd-v2.3.json"), encoding="utf-8"))
        rules, rrules = erd["tuple_rules"], erd["resolve_rules"]
    except (FileNotFoundError, KeyError):
        sys.path.insert(0, HERE)
        import erd_spec_v23
        rules, rrules = erd_spec_v23.TUPLE_RULES, erd_spec_v23.RESOLVE_RULES
    files = [f for f in os.listdir(LEDGER) if f.endswith(".json")]
    L = {f: json.load(open(os.path.join(LEDGER, f), encoding="utf-8")) for f in files}
    return dic, rules, rrules, L


def main():
    dic, rules, rrules, L = load_all()
    R = run_all(dic, rules, L, rrules)
    R["procedure"]["v21_none_fold_split"] = v21_split(R)
    print(procedure_md(R))
    print()
    print(adverse_md(R))
    json.dump(R, open(os.path.join(HERE, "erd-v2.3-tuples.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    print("\n→ erd-v2.3-tuples.json")


if __name__ == "__main__":
    main()
