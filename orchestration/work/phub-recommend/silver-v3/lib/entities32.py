# -*- coding: utf-8 -*-
"""ERD v3.2 개체 — 개체 22(v3.1 20 + post_procedure_timeline · emergency_sign) 중 v3.2 에서 바뀐 것.

- product: origin=taxonomy(V3.2-5 장비 자동 등록 · license_status=미확인 · 출처 = taxonomy 항목 이름 locator)
- evidence_statement: kind=adverse_effects(V3.2-0 · 문헌 adverse_effects 는 문구 사전이 아니라 근거 문장 · adverse_ref · ref_status)
- clinical_rule(disclosure): parsed · adverse_ref · ref_status(V3.2-0 · phrase_ids 대체)
- post_procedure_timeline(V3.2-9) · emergency_sign(V3.2-0) — 자기 테이블(참조만)
값은 참조만(단위를 세우지 않는다) · 출처는 원장 locator.
"""
from collections import OrderedDict

from .core import dref
from .entities import collect
from .provenance import P, loc, records
from .util import dedupe, mkid, norm


def products_v32(S):
    """장비 제품(product_name origin=taxonomy) — origin · license_status(미확인) · name(taxonomy 항목 이름 출처)."""
    L = S.ctx["L"]
    tx = L["taxonomy.json"]
    pos = {}
    for mi, m in enumerate(tx["modality"]):
        for si, sc in enumerate(m["subcategories"]):
            for ii, it in enumerate(sc["items"]):
                pos[f"{m['id']}/{si}/{ii}"] = (mi, si, ii)
    out = []
    for e in S.ctx["dicts"]["product_name"]["entries"]:
        if e.get("origin") != "taxonomy":
            continue
        pid = mkid("PRD", f"{e['code']}|{e['canonical']}")
        rec = S.E["product"].get(pid)
        if rec is None:
            continue
        provs = []
        for s_ in e.get("sources", []):
            lc = s_.get("locator")
            if lc and lc.split("@", 1)[1] in pos:
                provs.append(P("taxonomy.json", "modality[].subcategories[].items[].name", pos[lc.split("@", 1)[1]]))
        df = [loc(p) for p in provs] or dref("product_name", e)
        S.dattr(rec, "origin", "taxonomy", df)
        S.dattr(rec, "equipment_auto", {"rule": "V3.2-5", "status": e.get("status"), "kind_note": e.get("kind_note"), "codes": str(e.get("code")).split("|")}, df)
        if "license_status" not in rec["attrs"]:
            S.dattr(rec, "license_status", e.get("license_status") or "미확인", df)
        if "name" not in rec["attrs"]:
            for p in provs:
                S.attr(rec, "name", e["canonical"], p)
        out.append((pid, [p for p in provs], str(e.get("code")).split("|")))
    S.ctx["equipment_products"] = out
    return out


def evidence_adverse(S):
    """문헌 adverse_effects(V3.2-0) → evidence_statement(kind=adverse_effects) — statement · patient_text · accuracy · R19 · R20(관계에서)."""
    L = S.ctx["L"]
    root = "categories.{code}.adverse_effects[]"
    out = S.ctx.setdefault("evs", {})
    for r, x in records(L["literature-evidence.json"], root):
        sloc = P("literature-evidence.json", f"{root}.statement", r)
        rec = S.ent("evidence_statement", mkid("EVS", f"{r[0]}|adverse_effects|{x['statement']}"), [loc(sloc)])
        S.dattr(rec, "kind", "adverse_effects", [loc(sloc)])
        S.dattr(rec, "modality_code", r[0], [loc(sloc)])
        collect(S, "evidence_statement", rec, "literature-evidence.json", root, r, x)
        out[rec["id"]] = (rec, r, x, "adverse_effects")
    return out


def after_units(S, AU):
    """결정 · 단위 마감(AU.finish) 뒤 — 참조(adverse_ref)는 마감된 단위만 가리킨다."""
    L = S.ctx["L"]
    E = S.E
    # evidence_statement(adverse_effects).adverse_ref
    for lit in AU.literature:
        rec = E["evidence_statement"].get(lit["id"])
        if rec is None:
            continue
        df = [loc(P("literature-evidence.json", "categories.{code}.adverse_effects[].statement", lit["rec"]))]
        S.dattr(rec, "adverse_ref", list(lit["adverse_ref"]), df)
        S.dattr(rec, "ref_status", lit["ref_status"], df)
        S.dattr(rec, "parsed", {"statement": lit.get("parsed"), "patient_ko": lit.get("patient_ko_parsed")}, df)
    # clinical_rule(disclosure).parsed · adverse_ref · ref_status — 같은 정규화 문장이 여러 계열이면 참조 합집합
    by = OrderedDict()
    for d in AU.disclosures:
        rid = mkid("RUL", f"disclosure|{norm(d['text'])}")
        g = by.setdefault(rid, {"refs": [], "status": [], "parsed": None, "df": []})
        g["refs"] = dedupe(g["refs"] + d["adverse_ref"])
        g["status"].append(d["ref_status"])
        g["parsed"] = g["parsed"] or d.get("parsed")
        g["df"].append(loc(P("consent-checklist.json", "categories[].mandatory_disclosures[]", d["rec"])))
    for rid, g in by.items():
        rec = E["clinical_rule"].get(rid)
        if rec is None:
            continue
        st = "ref" if "ref" in g["status"] else ("ref_partial" if g["refs"] else "none")
        S.dattr(rec, "parsed", g["parsed"], g["df"])
        S.dattr(rec, "adverse_ref", g["refs"], g["df"])
        S.dattr(rec, "ref_status", st, g["df"])
        rec["attrs"].pop("phrase_ids", None)   # v3.2: phrase_ids 삭제(adverse_ref 로 대체)
    # post_procedure_timeline(V3.2-9)
    tls = L["post-procedure-timeline.json"]["timelines"]
    for ti, T in enumerate(AU.timelines):
        tl = tls[ti]
        rec = S.ent("post_procedure_timeline", T["id"], [loc(P("post-procedure-timeline.json", "timelines[].id", (ti,)))])
        S.attr(rec, "ledger_id", tl["id"], P("post-procedure-timeline.json", "timelines[].id", (ti,)))
        S.attr(rec, "category", tl["category"], P("post-procedure-timeline.json", "timelines[].category", (ti,)))
        S.attr(rec, "name", tl["name"], P("post-procedure-timeline.json", "timelines[].name", (ti,)))
        phases, lines, dfp = [], [], []
        for ph in T["phases"]:
            pl = loc(P("post-procedure-timeline.json", "timelines[].phases[].period", (ti, ph["order"])))
            dfp.append(pl)
            phases.append(OrderedDict([("order", ph["order"]), ("period", ph["period"]), ("label", ph["label"]), ("locator", pl), ("lines", [ln["locator"] for ln in ph["lines"]])]))
            for ln in ph["lines"]:
                lines.append(OrderedDict([("phase", ph["order"]), ("reaction_level", ln["reaction_level"]), ("text", ln["text"]), ("locator", ln["locator"]), ("parsed", ln.get("parsed")),
                                          ("adverse_ref", list(ln["adverse_ref"])), ("ref_status", ln["ref_status"]), ("decision_ids", list(ln.get("decision_ids") or []))]))
        tl_loc = loc(P("post-procedure-timeline.json", "timelines[].id", (ti,)))
        S.dattr(rec, "phases", phases, dfp or [tl_loc])   # 단계 없는 타임라인(원장 phases [])도 레코드 — 출처는 그 타임라인
        S.dattr(rec, "lines", lines, [x["locator"] for x in lines] or dfp or [tl_loc])
        S.dattr(rec, "modality_code", T["modality"], [loc(P("post-procedure-timeline.json", "timelines[].category", (ti,)))])
    # emergency_sign(V3.2-0)
    for s_ in AU.signs:
        provs = [P("consent-checklist.json", "categories[].emergency_signs[]", r) for r in s_["recs"]]
        rec = S.ent("emergency_sign", s_["id"], [loc(p) for p in provs])
        for p in provs:
            S.attr(rec, "text", s_["text"], p)
        df = [loc(p) for p in provs]
        S.dattr(rec, "modality_codes", list(s_["modality_codes"]), [loc(P("consent-checklist.json", "categories[].id", (r[0],))) for r in s_["recs"]])
        S.dattr(rec, "locators", [loc(p) for p in provs], df)
        S.dattr(rec, "parsed", s_.get("parsed"), df)
        S.dattr(rec, "adverse_ref", list(s_["adverse_ref"]), df)
        S.dattr(rec, "ref_status", s_["ref_status"], df)


def products_v33(S):
    """v3.3(V3.3-A) product.kind · component_of · component_kind — 원장에 구성품 칸이 없어 전부 kind=product · component_of null · component_kind null(값 0 · R36 엣지 0)."""
    n = 0
    by_id = {mkid("PRD", f"{e['code']}|{e['canonical']}"): e for e in S.ctx["dicts"]["product_name"]["entries"]}
    for pid, rec in S.E["product"].items():   # 제품 레코드 전부(사전 색인 제품 + step1 조사 제품) — kind 는 필수 속성
        e = by_id.get(pid)
        df = dref("product_name", e) if e is not None else (list(rec["derived_from"]) or [loc(p) for cells in rec["attrs"].values() for c in cells for p in c.get("prov", [])][:1])
        S.dattr(rec, "kind", "product", df)
        S.dattr(rec, "component_of", None, df)
        S.dattr(rec, "component_kind", None, df)
        n += 1
    S.ctx["products_v33"] = {"products": n, "components": 0}
    return n
