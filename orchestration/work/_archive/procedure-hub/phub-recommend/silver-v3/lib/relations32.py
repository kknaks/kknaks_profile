# -*- coding: utf-8 -*-
"""ERD v3.2 관계 — R15 may_cause(v3.2) · R33 has_timeline · R34 timeline_refers · R35 sign_refers · R20(문헌 adverse_effects) · R4(장비 제품).

R15(v3.2): (출발, 단위) 마다 엣지 하나 — 참조 구현 erd-v3.2-tuples.py run_adverse32 의 all_edges 와 같은 묶음.
  - 이름(complications 표 행): 계열 → 단위 · severity·incidence·onset·mechanism·management·prevention·duration·risk_factors·evidence_ref(그 이름의 잎 · 이름 둘 이상이 같은 (계열, 단위)면 값 목록)
  - 문구(부작용 문구 사전 exact · new · approved): 계열·항목·제품 → 단위 · source_phrases · frequency_class · 경과(원칙 C) · degree/timing/incidence/condition_text(항목 참조)
  - 타임라인 줄(R34 참조): 계열 → 단위 timeline_refs(참조) · 응급 징후(R35 참조): 계열 → 단위 emergency_sign_refs(참조)
  - layer: family(계열 출발) | item(분류 항목·제품 출발) · inheritance(V3.2-8): 속성마다 basis item|family|unit|none · ref · ref_locator — 값 복사 없음
시술 축 끝은 relations.Ends(참조 · 코드) → finalize 가 anchor 를 최종 튜플 id 로.
"""
import json
from collections import OrderedDict

from .provenance import P, loc
from .relations import edge_from, expr_start, start_prov, tuple_rec
from .units31 import PARSED_REFS
from .units32 import ACTIVE
from .util import dedupe, mkid

INHERIT_ATTRS = ["severity", "incidence", "onset", "duration", "mechanism", "management", "prevention", "risk_factors"]
NAME_ATTRS = ("severity", "incidence", "onset", "mechanism", "management", "prevention", "duration")
TL_SLOT = "post-procedure-timeline.timelines[].name (10)"


def build_v32(S, AU, E):
    L = S.ctx["L"]
    agg = OrderedDict()

    def g_of(start, uid, layer, fam):
        k = ((start[0], json.dumps(start[1], sort_keys=True, ensure_ascii=False)), uid)
        g = agg.get(k)
        if g is None:
            g = agg[k] = {"start": start, "uid": uid, "layer": layer, "family": fam, "prov": [], "names": [], "attrs": OrderedDict(), "courses": [], "phrases": [], "freq": [], "kinds": [],
                          "refs": {ak: [] for _, ak in PARSED_REFS}, "timeline_refs": [], "sign_refs": [], "decision_ids": [], "evidence_ref": []}
        elif layer == "family":
            g["layer"] = "family"
        return g

    def addp(g, ps):
        for p in ps:
            if p not in g["prov"]:
                g["prov"].append(p)

    # ---- ① complications 이름(계열 → 단위)
    for ci, cat in enumerate(L["complications.json"]["categories"]):
        start = E.code(cat["id"])
        if not start:
            continue
        for i, cm in enumerate(cat["complications"]):
            r = (ci, i)
            lc = f"complications.json:categories[].complications[].name@{cat['id']}/{i}"
            for uid in AU.name_units.get(lc, []):
                g = g_of(start[0], uid, "family", cat["id"])
                npv = P("complications.json", "categories[].complications[].name", r)
                addp(g, [P("complications.json", "categories[].id", (ci,)), npv])
                g["names"].append(loc(npv))
                for k in NAME_ATTRS:
                    if cm.get(k) not in (None, "", [], {}):
                        g["attrs"].setdefault(k, []).append((cm[k], [P("complications.json", f"categories[].complications[].{k}", r)]))
                if "risk_factors" in cm:
                    rf = cm["risk_factors"] or []
                    g["attrs"].setdefault("risk_factors", []).append((rf or None, [P("complications.json", "categories[].complications[].risk_factors[]", r + (j,)) for j in range(len(rf))] or [P("complications.json", "categories[].complications[].risk_factors", r)]))
                if cm.get("evidence"):
                    g["evidence_ref"] = dedupe(g["evidence_ref"] + [mkid("CIT", f"url:{u.strip()}") for u in cm["evidence"].split(";") if u.strip()])
                    addp(g, [P("complications.json", "categories[].complications[].evidence", r)])
                g["courses"] = dedupe(g["courses"] + list(AU.name_courses.get((lc, uid)) or []))
    # ---- ② 부작용 문구 사전(exact · new · approved) → 단위
    for pid, e in AU.phrases.items():
        if e["status"] not in ACTIVE or not e["units"]:
            continue
        for c in e["contexts"]:
            if c.get("rec") is None:
                continue
            row = {"file": c["file"], "rec": tuple_rec(c["rec"]), "modality": c.get("modality"), "item": c.get("item"), "product": c.get("product")}
            st = expr_start(S, E, row)
            if not st:
                continue
            layer = "item" if (c.get("item") or c.get("product")) else "family"
            pv = P(c["file"], c["path"], c["rec"])
            for s0 in st:
                for uid in e["units"]:
                    g = g_of(s0, uid, layer, c.get("modality"))
                    addp(g, [pv] + start_prov(dict(row, path=c["path"])))
                    if pid not in g["phrases"]:
                        g["phrases"].append(pid)
                    g["courses"] = dedupe(g["courses"] + AU.phrase_courses(pid, uid))
                    fc = (c.get("context") or {}).get("frequency_class") or c.get("frequency_class")
                    if fc and fc not in g["freq"]:
                        g["freq"].append(fc)
                    if c.get("kind") and c["kind"] not in g["kinds"]:
                        g["kinds"].append(c["kind"])
                    for pk, ak in PARSED_REFS:
                        if e["parsed"].get(pk) and pid not in g["refs"][ak]:
                            g["refs"][ak].append(pid)
                    for d in e.get("decision_ids") or []:
                        if d not in g["decision_ids"]:
                            g["decision_ids"].append(d)
    # ---- ③ 타임라인 줄(R34 참조) → 계열 R15 timeline_refs
    for ti, T in enumerate(AU.timelines):
        start = E.code(T["modality"])
        if not start:
            continue
        for ph in T["phases"]:
            for ln in ph["lines"]:
                for uid in ln["adverse_ref"]:
                    g = g_of(start[0], uid, "family", T["modality"])
                    addp(g, [P("post-procedure-timeline.json", "timelines[].category", (ti,)), P("post-procedure-timeline.json", ln["path"], ln["rec"])])
                    if ln["locator"] not in g["timeline_refs"]:
                        g["timeline_refs"].append(ln["locator"])
                    g["courses"] = dedupe(g["courses"] + list(ln.get("mapped_courses") or []))
                    for d in ln.get("decision_ids") or []:
                        if d not in g["decision_ids"]:
                            g["decision_ids"].append(d)
    # ---- ④ 응급 징후(R35 참조) → 계열 R15 emergency_sign_refs
    for sg in AU.signs:
        for code, r in zip(sg["modality_codes"], sg["recs"]):
            start = E.code(code)
            if not start:
                continue
            for uid in sg["adverse_ref"]:
                g = g_of(start[0], uid, "family", code)
                addp(g, [P("consent-checklist.json", "categories[].id", (r[0],)), P("consent-checklist.json", "categories[].emergency_signs[]", r)])
                if sg["id"] not in g["sign_refs"]:
                    g["sign_refs"].append(sg["id"])
    # ---- V3.2-8 상속(참조만)
    fam_edges = {(g["family"], g["uid"]): g for g in agg.values() if g["start"][0] == "modality"}
    rows = []
    for g in agg.values():
        uid = g["uid"]
        inh = []
        for a in INHERIT_ATTRS:
            if g["attrs"].get(a):
                inh.append(OrderedDict([("attr", a), ("basis", "item" if g["layer"] == "item" else "family"), ("ref", loc(g["attrs"][a][0][1][0]))]))
                continue
            fe = fam_edges.get((g["family"], uid)) if g["start"][0] != "modality" else None
            if fe is not None and fe["attrs"].get(a):
                inh.append(OrderedDict([("attr", a), ("basis", "family"), ("ref", f"R15:{g['family']}→{uid}"), ("ref_locator", loc(fe["attrs"][a][0][1][0]))]))
                continue
            gen = (AU.units.get(uid) or {}).get("general_management") or [] if a == "management" else []
            if gen:
                inh.append(OrderedDict([("attr", a), ("basis", "unit"), ("ref", f"{uid}.general_management"), ("ref_locator", gen[0]["locator"])]))
                continue
            inh.append(OrderedDict([("attr", a), ("basis", "none"), ("ref", None)]))
        df = [loc(p) for p in g["prov"]]
        attrs = OrderedDict()
        for k, vals in g["attrs"].items():
            if len(vals) == 1:
                attrs[k] = {"value": vals[0][0], "prov": list(vals[0][1])}
            else:   # 같은 (계열, 단위)로 접힌 이름 둘 이상 — 이름마다의 값(버리지 않는다 · 이름 순서 = names)
                attrs[k] = {"value": [v for v, _ in vals], "prov": [p for _, ps in vals for p in ps], "per_name": True}
        if g["evidence_ref"]:
            attrs["evidence_ref"] = {"value": g["evidence_ref"], "derived_from": df}
        attrs["course"] = {"value": g["courses"] or None, "derived_from": df}
        attrs["source_phrases"] = {"value": g["phrases"], "derived_from": df}
        if g["freq"]:
            attrs["frequency_class"] = {"value": g["freq"][0] if len(g["freq"]) == 1 else g["freq"], "derived_from": df}
        for ak, v in g["refs"].items():
            attrs[ak] = {"value": v or None, "derived_from": df}
        attrs["created_by_phrase"] = {"value": bool((AU.units.get(uid) or {}).get("created_by_phrase")), "derived_from": df}
        attrs["timeline_refs"] = {"value": g["timeline_refs"], "derived_from": df}
        attrs["emergency_sign_refs"] = {"value": g["sign_refs"], "derived_from": df}
        attrs["inheritance"] = {"value": inh, "derived_from": df}
        attrs["layer"] = {"value": g["layer"], "derived_from": df}
        if g["names"]:
            attrs["names"] = {"value": g["names"], "derived_from": g["names"]}
        if g["kinds"]:
            attrs["phrase_kinds"] = {"value": g["kinds"], "derived_from": df}
        if g["decision_ids"]:
            attrs["decision_ids"] = {"value": g["decision_ids"], "derived_from": g["decision_ids"]}
        edge_from(S, "R15", g["start"], "adverse_effect", uid, g["prov"], attrs)
        rows.append((g["start"][0], g["layer"], uid, inh))
    S.ctx["r15_v32"] = rows

    # ---- R33 has_timeline — 이름이 튜플로 풀리면 그 튜플 · 아니면 계열(V3.2-9)
    occ = S.ctx["occ"].get(TL_SLOT, [])
    tls = L["post-procedure-timeline.json"]["timelines"]
    by_rec = {tuple(o[3]["r"]) if isinstance(o[3], dict) and "r" in o[3] else None: o for o in occ}
    for ti, T in enumerate(AU.timelines):
        prov = [P("post-procedure-timeline.json", "timelines[].name", (ti,)), P("post-procedure-timeline.json", "timelines[].category", (ti,))]
        o = by_rec.get((ti,))
        ends = None
        if o is not None:
            try:
                ends = E.of(TL_SLOT, o[0], o[1])
            except KeyError:
                ends = None
        if ends and all(x[0] == "procedure" for x in ends):
            for typ, ident, ea in ends:
                a = {"target_depth": {"value": "procedure", "derived_from": [loc(p) for p in prov]}}
                if ea.get("via_catalog_item"):
                    a["via_catalog_item"] = {"value": ea["via_catalog_item"], "derived_from": [loc(prov[0])]}
                S.edge("R33", "procedure", None, "post_procedure_timeline", T["id"], prov, a, from_anchor=ident["anchor"])
        else:
            st = E.code(T["modality"])
            if st:
                S.edge("R33", "modality", st[0][1], "post_procedure_timeline", T["id"], prov, {"target_depth": {"value": "modality", "derived_from": [loc(prov[1])]},
                                                                                              "name_result": {"value": (ends[0][0] if ends else "unresolved"), "derived_from": [loc(prov[0])]}})
        # ---- R34 timeline_refers — 줄 → 이미 있는 단위(참조)
        for ph in T["phases"]:
            for ln in ph["lines"]:
                lp = P("post-procedure-timeline.json", ln["path"], ln["rec"])
                for uid in ln["adverse_ref"]:
                    a = {"line_locator": {"value": ln["locator"], "derived_from": [loc(lp)]}, "reaction_level": {"value": ln["reaction_level"], "derived_from": [loc(lp)]},
                         "period": {"value": ph["period"], "prov": [P("post-procedure-timeline.json", "timelines[].phases[].period", (ti, ph["order"]))]},
                         "phase_label": {"value": ph["label"], "prov": [P("post-procedure-timeline.json", "timelines[].phases[].label", (ti, ph["order"]))]}}
                    if ln.get("decision_ids"):
                        a["decision_ids"] = {"value": list(ln["decision_ids"]), "derived_from": list(ln["decision_ids"])}
                    S.edge("R34", "post_procedure_timeline", T["id"], "adverse_effect", uid, [lp], a)
    # ---- R35 sign_refers
    for sg in AU.signs:
        provs = [P("consent-checklist.json", "categories[].emergency_signs[]", r) for r in sg["recs"]]
        for uid in sg["adverse_ref"]:
            S.edge("R35", "emergency_sign", sg["id"], "adverse_effect", uid, provs)
    # ---- R20 — 계열 → 문헌 adverse_effects 근거 문장(V3.2-0)
    ids = S.ctx["ids"]
    for code, cat in L["literature-evidence.json"]["categories"].items():
        if code not in ids.mod:
            continue
        for i, x in enumerate(cat.get("adverse_effects") or []):
            S.edge("R20", "modality", ids.mod[code]["id"], "evidence_statement", mkid("EVS", f"{code}|adverse_effects|{x['statement']}"),
                   [P("literature-evidence.json", "categories.{code}.adverse_effects[].statement", (code, i))])
    # ---- R4 — 계열 → 장비 제품(V3.2-5 · 그 계열의 taxonomy 항목 이름이 출처)
    tx = L["taxonomy.json"]
    for pid, provs, codes in S.ctx.get("equipment_products", []):
        for code in codes:
            ps = [p for p in provs if tx["modality"][int(p["rec"].split("/")[0])]["id"] == code]
            if code in ids.mod and ps:
                S.edge("R4", "modality", ids.mod[code]["id"], "product", pid, ps, {"basis": {"value": "equipment_auto", "derived_from": [loc(p) for p in ps]}})
