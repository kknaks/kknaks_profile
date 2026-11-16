#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ERD v2.1 — 튜플 분해 실측기. v2(erd-v2-tuples.py)의 시술 튜플 **what 결정 규칙 하나**만 바꾼다. 독립 실행.

v2 → v2.1 (발주서 erd-v2.1-brief.md):
  1. 이름 조각이 **전부** 사전에 닿았을 때만 what/site/technique 를 사전 값으로 조립하고, 그때만 다른 항목과 접힐 수 있다.
  2. 조각 중 하나라도 미등록이면 **접지 않는다** — what = 그 분류 항목 자신(what_kind=catalog_item · 미등록 조각은 candidate_name),
     site/technique 는 닿은 조각만(technique 는 §1.4 그대로 R5 상속 허용), 상태 partial. 식별자는 CAT- id 기반이라 항목마다 고유.
  3. 부모 하위분류 fallback 삭제(fallback_to_parent=false). 조각이 전부 닿았는데 primary 가 없으면(부위만·계열명만) 역시 항목 자신.
     다른 분류 항목(catalog_item_name 색인)에 닿은 조각은 그 항목의 what 이 사전 값(product|subcategory|modality)일 때만 what 으로 쓴다.
  4. 참조(②)·market-pricing(③): 미등록 조각이 있으면 그 참조는 미해결(v1.1 ⑨) — 튜플을 만들지 않는다(부모 층으로 접지 않는다).
     v1.1 ⑨ 와 같은 판정이 되도록 3단계 (a) 통째 일치를 먼저 본다(라벨 전체가 사전 값이면 쪼개지 않음 · 분류 항목에도 같은 순서, 자기 이름 제외).
부작용 튜플·adverse_expression 은 v2 그대로(코드 재사용). 입력·출력 파일만 v2.1 이름.

입력(같은 폴더): erd-v2.1-dictionaries.json(없으면 erd-v2-dictionaries.json · 값 동일) · erd-v2.1.json(tuple_rules/resolve_rules — 없으면 erd_spec_v21) ·
      erd-v2-tuples.py(v2 분해기 · 부작용 분해기 재사용) · erd-v1.1-resolve.py · 원장 21 · erd-v2-tuples.json(§9.5 나란히 비교용, 있으면)
출력: 표준 출력에 §9.5/§9.6 표 + erd-v2.1-tuples.json
실행: python3 erd-v2.1-tuples.py
"""
import importlib.util
import json
import os
import sys
from collections import Counter, OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


V2 = load_module("erd_v2_tuples", os.path.join(HERE, "erd-v2-tuples.py"))
norm, mkid, md_table, with_alias, LEDGER = V2.norm, V2.mkid, V2.md_table, V2.with_alias, V2.LEDGER
PRIMARY_KINDS = V2.PRIMARY_KINDS
WHAT_PREC = dict(V2.WHAT_PREC, catalog_item=3)  # 참조(②③)에서 분류 항목 자신이 what 인 항목에 닿은 경우 — 사전 값 what 보다 뒤
DICT_WHAT_KINDS = ("product", "modality_subcategory", "modality")  # 사전 값인 what 종류 — 접힘 허용


class ProcedureTuples21(V2.ProcedureTuples):
    """v2 ProcedureTuples 위에 what 결정 규칙만 교체."""

    def cat_what(self, family, name):
        return {"id": mkid("CAT", f"{family}|{name}"), "label": name, "family": family}

    def decompose_whole_first(self, label, family, exclude=None):
        """v1.1 3단계 (a) 통째 일치를 먼저 본다: 라벨 전체가 하나의 사전 값(계열·제품·하위분류·분류 항목 이름)이면 조각 하나(괄호·조합 기호가 값 안에 있어도 쪼개지 않는다).
        v2 는 바로 분해해서 「PRP/자가혈」「마이크로니들링(MTS)」「리쥬란 HB+」 같은 사전 값을 조각으로 쪼개 미등록을 만들었다. 아니면 v2 분해 그대로."""
        self.R.exclude = exclude
        try:
            w = self.R.whole(str(label), family)
        finally:
            self.R.exclude = None
        if w:
            return [{"where": "outer", "members": [{"text": str(label).strip(), "spans": [w], "untouched": []}]}], True
        return self.R.decompose(str(label), family, exclude=exclude), False

    def what_from_span(self, s, family, for_item):
        w = super().what_from_span(s, family, for_item)
        if w and for_item and s["kind"] == "procedure" and w[0] not in DICT_WHAT_KINDS:
            # 다른 분류 항목에 닿았지만 그 항목의 what 이 사전 값이 아니다(항목 자신) → 이 항목의 what 으로 쓰지 않는다
            return None
        return w

    def assemble(self, groups, family, for_item=False, parent_sub=None, hint_family=None, self_item=None):
        combo_members = None
        for g in groups:
            pm = [m for m in g["members"] if any(s["kind"] in PRIMARY_KINDS for s in m["spans"])]
            if len(pm) >= 2:
                combo_members = pm
                break
        all_spans = [s for g in groups for m in g["members"] for s in m["spans"]]
        untouched = [u["text"] for g in groups for m in g["members"] for u in m["untouched"]]
        qualifiers = [(s["kind"], s["canonical"]) for s in all_spans if s["kind"] in ("spec", "product_tier")]
        site_spans = [s for s in all_spans if s["kind"] == "site"]
        tech_spans = [s for s in all_spans if s["kind"] == "technique"]
        # 규칙 2: 분류 항목에 미등록 조각 → 접지 않는다 (조합이어도 항목 자신)
        if for_item and untouched:
            found = [f"{s['kind']}:{s['canonical']}" for s in all_spans if s["kind"] in PRIMARY_KINDS]
            return self._self_tuple(self_item, "self:unregistered", found, site_spans, tech_spans, untouched, qualifiers)
        if combo_members is not None:
            members = [self.assemble([{"where": "member", "members": [m]}], family, for_item, parent_sub, hint_family, self_item) for m in combo_members]
            return {"kind": "combo_ref", "members": members, "untouched": untouched, "qualifiers": qualifiers}
        cands = []
        for s in all_spans:
            if s["kind"] in PRIMARY_KINDS:
                s2 = s
                if s["kind"] == "modality":
                    ph = self.R.lex.hits("product", s["text"])
                    if ph:
                        hh = {x for x in ph if self.R._in_family(x[0], family)} or ph
                        x = sorted(hh, key=lambda z: str(z))[0]
                        s2 = {"kind": "product", "text": s["text"], "code": x[0], "canonical": x[1], "cross_family": not self.R._in_family(x[0], family)}
                    elif for_item:
                        continue  # 계열 조각은 what 이 아니다(v2 그대로). v2.1: 부모 하위분류 대신 항목 자신
                w = self.what_from_span(s2, family, for_item)
                if w:
                    cands.append((WHAT_PREC[w[0]], len(cands), w, s2))
        cands.sort(key=lambda x: (x[0], x[1]))
        inh_site, inh_tech = None, None
        if cands:
            what_kind, what, basis, inh_site, inh_tech = cands[0][2]
            extra = [c[2][2] for c in cands[1:]]
        elif for_item:
            # 규칙 3: 부모 하위분류 fallback 삭제 → 항목 자신 (전부 닿았지만 primary 없음)
            found = [f"{s['kind']}:{s['canonical']}" for s in all_spans if s["kind"] in PRIMARY_KINDS]
            return self._self_tuple(self_item, "self:no_primary", found, site_spans, tech_spans, [], qualifiers)
        elif hint_family and hint_family in self.ids.mod:
            what_kind, what, basis, extra = "modality", self.ids.mod[hint_family], f"hint_family:{hint_family}", []
        else:
            return {"kind": "none", "untouched": untouched, "qualifiers": qualifiers, "reason": "primary 조각도 계열 힌트도 없음"}
        site, site_basis = None, None
        if site_spans:
            site = self.ids.site[norm(site_spans[0]["canonical"])]
            site_basis = site_spans[0]["text"]
        elif inh_site and inh_site[1] != "none":
            site = {"id": inh_site[1], "label": inh_site[0]}
            site_basis = f"(분류 항목 상속) {inh_site[0]}"
        extra_sites = [s["canonical"] for s in site_spans[1:]]
        if tech_spans:
            tech, tech_origin = tech_spans[0]["canonical"], "fragment"
        elif inh_tech and inh_tech[0]:
            tech, tech_origin = inh_tech
        else:
            tech, tech_origin = self.ids.inherit_tech(what.get("family"))
        return {"kind": "tuple", "what_kind": what_kind, "what": what, "what_basis": basis, "extra_primaries": extra, "site": site, "site_basis": site_basis,
                "extra_sites": extra_sites, "technique": tech, "technique_origin": tech_origin, "untouched": untouched, "qualifiers": qualifiers}

    def _self_tuple(self, self_item, basis, found, site_spans, tech_spans, untouched, qualifiers):
        family, name = self_item
        what = self.cat_what(family, name)
        site, site_basis = None, None
        if site_spans:
            site = self.ids.site[norm(site_spans[0]["canonical"])]
            site_basis = site_spans[0]["text"]
        if tech_spans:
            tech, tech_origin = tech_spans[0]["canonical"], "fragment"
        else:
            tech, tech_origin = self.ids.inherit_tech(family)
        return {"kind": "tuple", "what_kind": "catalog_item", "what": what, "what_basis": basis, "extra_primaries": found, "site": site, "site_basis": site_basis,
                "extra_sites": [s["canonical"] for s in site_spans[1:]], "technique": tech, "technique_origin": tech_origin, "untouched": untouched, "qualifiers": qualifiers,
                "candidate_name": list(untouched)}

    # --- ① 분류 항목
    def catalog_tuple(self, family, sub, name):
        key = (family, name)
        if key in self.catalog:
            return self.catalog[key]
        if key in self._busy:
            return None
        self._busy.add(key)
        groups, whole = self.decompose_whole_first(name, family, exclude=norm(name))
        a = self.assemble(groups, family, for_item=True, parent_sub=sub, self_item=(family, name))
        rec = {"family": family, "subcategory": sub, "name": name, "catalog_item_id": self.cat_what(family, name)["id"], "whole_match": whole,
               "groups": [{"where": g["where"], "members": [{"text": m["text"], "spans": [(s["kind"], s["canonical"]) for s in m["spans"]], "untouched": [u["text"] for u in m["untouched"]]} for m in g["members"]]} for g in groups]}
        if a["kind"] == "combo_ref":
            ids = []
            for m in a["members"]:
                if m["kind"] == "tuple":
                    ids.append(self.register(m["what_kind"], m["what"], m["site"], m["technique"], m["technique_origin"], "catalog_item", {"origin": "catalog_item", "label": name, "family": family}, m["untouched"]))
            rec.update({"result": "combo_ref", "procedure_id": ids[0] if ids else None, "member_ids": ids, "unregistered": a["untouched"], "qualifiers": a["qualifiers"], "what_basis": "combo", "status": "partial" if a["untouched"] else "complete"})
        elif a["kind"] == "tuple":
            tid = self.register(a["what_kind"], a["what"], a["site"], a["technique"], a["technique_origin"], "catalog_item", {"origin": "catalog_item", "label": name, "family": family}, a["untouched"])
            if a["what_kind"] == "catalog_item":
                self.tuples[tid]["candidate_name"] = list(a.get("candidate_name", []))
            rec.update({"result": "tuple", "procedure_id": tid, "what_kind": a["what_kind"], "what_basis": a["what_basis"], "extra_primaries": a["extra_primaries"], "site": a["site"]["label"] if a["site"] else None, "site_basis": a["site_basis"],
                        "technique": a["technique"], "technique_origin": a["technique_origin"], "unregistered": a["untouched"], "qualifiers": a["qualifiers"], "status": "partial" if a["untouched"] else "complete",
                        "candidate_name": list(a.get("candidate_name", []))})
        else:
            rec.update({"result": "none", "procedure_id": None, "unregistered": a["untouched"]})
        self.catalog[key] = rec
        self._busy.discard(key)
        return rec

    # --- ② ③ 참조 — 규칙 4: 미등록 조각 있으면 미해결(튜플 없음)
    def run_reference(self, label, hint, origin, slot):
        if isinstance(label, str) and (label.startswith("__MODALITY__") or label.startswith("__SUBID__")):
            return super().run_reference(label, hint, origin, slot)
        groups, whole = self.decompose_whole_first(label, hint)
        a = self.assemble(groups, hint, hint_family=hint)
        base = {"label": label, "hint": hint, "whole_match": whole, "groups": [{"where": g["where"], "members": [{"text": m["text"], "spans": [(s["kind"], s["canonical"]) for s in m["spans"]], "untouched": [u["text"] for u in m["untouched"]]} for m in g["members"]]} for g in groups]}
        if a["untouched"]:
            base.update({"result": "unresolved", "unregistered": a["untouched"], "qualifiers": a["qualifiers"], "reason": "미등록 조각 있음 → v1.1 ⑨ 미해결 (부모 층 튜플로 접지 않음)",
                         "partial_spans": [(s["kind"], s["canonical"]) for g in groups for m in g["members"] for s in m["spans"]]})
            return base
        if a["kind"] == "combo_ref":
            ids = []
            for m in a["members"]:
                if m["kind"] == "tuple":
                    ids.append(self.register(m["what_kind"], m["what"], m["site"], m["technique"], m["technique_origin"], origin, {"origin": origin, "slot": slot, "label": label, "family": hint, "member": True}, m["untouched"]))
            base.update({"result": "combo_ref", "member_ids": list(dict.fromkeys(ids)), "member_count": len(a["members"]), "unregistered": [], "qualifiers": a["qualifiers"], "status": "complete"})
        elif a["kind"] == "tuple":
            tid = self.register(a["what_kind"], a["what"], a["site"], a["technique"], a["technique_origin"], origin, {"origin": origin, "slot": slot, "label": label, "family": hint}, a["untouched"])
            base.update({"result": "tuple", "procedure_id": tid, "what_kind": a["what_kind"], "what_basis": a["what_basis"], "extra_primaries": a["extra_primaries"], "site": a["site"]["label"] if a["site"] else None, "technique": a["technique"], "technique_origin": a["technique_origin"],
                         "unregistered": [], "qualifiers": a["qualifiers"], "status": "complete"})
        else:
            base.update({"result": "none", "unregistered": [], "qualifiers": a["qualifiers"], "reason": a["reason"]})
        return base


# ---------------------------------------------------------------------------
# 전체 실행 · 집계 (시술 = v2.1 · 부작용 = v2 코드 그대로)
# ---------------------------------------------------------------------------
def run_all(dic_json, rules, L, resolve_rules=None):
    if resolve_rules is None:
        sys.path.insert(0, HERE)
        import erd_spec_v21
        resolve_rules = erd_spec_v21.RESOLVE_RULES
    ids = V2.Ids(dic_json, L)
    lex = V2.V11.Lexicon(with_alias(dic_json))
    PT = ProcedureTuples21(lex, resolve_rules, ids, L)
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
        return {"n": len(rows), "tuple": c.get("tuple", 0), "combo_ref": c.get("combo_ref", 0), "unresolved": c.get("unresolved", 0), "none": c.get("none", 0), "complete": st.get("complete", 0), "partial": st.get("partial", 0),
                "distinct_tuples": len({x for r in rows for x in tids_of(r) if x}),
                "new_tuples_not_from_catalog": len({x for r in rows for x in tids_of(r) if x and "catalog_item" not in T[x]["origins"]}),
                "whole_match": sum(1 for r in rows if r.get("whole_match")),
                "by_what_kind": dict(Counter(T[x]["what_kind"] for r in rows for x in tids_of(r) if x))}

    folded = []
    for tid in cat_distinct:
        names = [r for r in cat_recs if r.get("procedure_id") == tid or tid in r.get("member_ids", [])]
        t = T[tid]
        own_unreg = list(dict.fromkeys(u for r in names for u in r.get("unregistered", [])))
        folded.append({"procedure_id": tid, "what_kind": t["what_kind"], "what": t["what_label"], "site": t["site"], "technique": t["technique"], "technique_origin": t["technique_origin"], "status": "partial" if own_unreg else "complete",
                       "n_items": len(names), "items": [f"{r['name']}[{r['family']}]" for r in names], "item_status": [r.get("status") for r in names], "unregistered": own_unreg,
                       "all_dict_values": t["what_kind"] in DICT_WHAT_KINDS and not own_unreg})
    folded.sort(key=lambda x: (-x["n_items"], x["what_kind"], x["what"]))
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
        ("tuples_technique_origin", dict(Counter(t["technique_origin"] for t in T.values()))),
        ("tuples_dict_what_site_none_ratio", round(sum(1 for t in T.values() if t["what_kind"] in DICT_WHAT_KINDS and t["site_id"] == "none") / max(1, sum(1 for t in T.values() if t["what_kind"] in DICT_WHAT_KINDS)), 3)),
        ("families_without_single_technique", sorted(f for f, v in ids.family_tech.items() if len(v) != 1)),
        ("unregistered_distinct", len(unreg_all)),
        ("unregistered_total", sum(unreg_all.values())),
        ("unregistered_top30", unreg_all.most_common(30)),
        ("unregistered_top30_by_origin", {k: v.most_common(30) for k, v in unreg_by_origin.items()}),
    ])
    # ---- 부작용: v2 그대로 (코드 재사용 — run_all 의 부작용 절을 그대로 실행)
    adv = V2.run_all(dic_json, rules, L, resolve_rules)["adverse"]
    af2 = [f for f in adv["folded"] if f["n_names"] >= 2]
    adv["summary"]["folded_with_2plus_names"] = len(af2)
    adv["summary"]["folded_with_partial_name"] = sum(1 for f in af2 if f["status"] == "partial")
    adv["summary"]["folded_partial_detail"] = [{"event": f["event"], "site": f["site"], "course": f["course"], "names": f["names"], "unregistered": f["unregistered"]} for f in af2 if f["status"] == "partial"]
    out = OrderedDict([
        ("erd_version", "v2.1"), ("rules", rules["name"]), ("fallback_to_parent", False),
        ("procedure", OrderedDict([("summary", proc_summary), ("tuples", list(T.values())), ("catalog", cat_recs), ("folded", folded), ("references", ref_rows), ("market_pricing", mk_rows)])),
        ("adverse", adv),
    ])
    return out


# ---------------------------------------------------------------------------
# 표 (md) — §9.5 (v2 수치 나란히) · §9.6 (v2 그대로 + 검산 항목)
# ---------------------------------------------------------------------------
def load_v2_summary():
    try:
        return json.load(open(os.path.join(HERE, "erd-v2-tuples.json"), encoding="utf-8"))["procedure"]["summary"]
    except (FileNotFoundError, KeyError):
        return None


def _kv(d):
    return ", ".join(f"{k}={v}" for k, v in d.items())


def procedure_md(R, v2s=None):
    s = R["procedure"]["summary"]
    v2s = v2s or load_v2_summary() or {}
    g = lambda k, d="—": v2s.get(k, d)  # noqa
    o = []
    A = o.append
    A("#### 9.5.1 분류 항목 521 → 튜플 (v2 → v2.1 나란히)")
    A("")
    A(md_table(["항목", "v2", "v2.1"], [
        ("분류 항목", g("catalog_items"), s["catalog_items"]),
        ("분해 결과", _kv(g("catalog_result", {})), _kv(s["catalog_result"])),
        ("튜플 수(distinct)", f"**{g('catalog_distinct_tuples')}** (비율 {g('catalog_fold_ratio')})", f"**{s['catalog_distinct_tuples']}** (521 → N · 비율 {s['catalog_fold_ratio']})"),
        ("둘 이상 항목이 접힌 튜플", f"{g('catalog_tuples_with_2plus_items')} 개 튜플에 항목 {g('catalog_items_in_folded_tuples')} 개", f"{s['catalog_tuples_with_2plus_items']} 개 튜플에 항목 {s['catalog_items_in_folded_tuples']} 개 (나머지 {s['catalog_distinct_tuples'] - s['catalog_tuples_with_2plus_items']} 튜플은 항목 1개씩)"),
        ("접힌 튜플 중 세 칸 전부 사전 값", "—(규칙 없음)", f"{s['catalog_folded_all_dict_values']} / {s['catalog_tuples_with_2plus_items']} · partial 항목이 섞인 접힌 튜플 {s['catalog_folded_with_partial_item']} · partial 항목 둘 이상 {s['catalog_folded_with_2plus_partial_items']}"),
        ("부모 하위분류 fallback", f"{g('catalog_by_what_basis', {}).get('parent_subcategory', '—')} 항목", f"{s['catalog_fallback_to_parent']} (삭제)"),
        ("what 축", _kv(g("catalog_by_what_kind", {})) + " · 근거: " + _kv(g("catalog_by_what_basis", {})), _kv(s["catalog_by_what_kind"]) + " · 근거: " + _kv(s["catalog_by_what_basis"])),
        ("항목 자신(catalog_item)이 what 인 항목", "0", f"{s['catalog_self_items']} (그중 부위 조각 있음 {s['catalog_self_with_site']})"),
        ("site 축", f"none {g('catalog_site_none')} / 항목 기준 {g('catalog_site_none_ratio')} · 튜플 기준 {g('catalog_tuple_site_none_ratio')}", f"none {s['catalog_site_none']} / 항목 기준 none 비율 {s['catalog_site_none_ratio']} · 튜플 기준 none 비율 {s['catalog_tuple_site_none_ratio']}"),
        ("technique 축", _kv(g("catalog_technique", {})) + f" · 항목 기준 none {g('catalog_technique_none_ratio')} · 튜플 기준 {g('catalog_tuple_technique_none_ratio')}", _kv(s["catalog_technique"]) + f" · 항목 기준 none 비율 {s['catalog_technique_none_ratio']} · 튜플 기준 none 비율 {s['catalog_tuple_technique_none_ratio']}"),
        ("상속 불가 계열(R5 기법 둘 이상 또는 없음)", ", ".join(g("families_without_single_technique", [])), ", ".join(s["families_without_single_technique"])),
        ("항목 상태", _kv(g("catalog_status", {})), _kv(s["catalog_status"])),
    ]))
    A("")
    A("#### 9.5.2 접힌 결과 — 둘 이상의 분류 항목이 같은 튜플로 간 것 전부 (세 칸 전부 사전 값 · 사용자가 「같은 게 맞다」고 볼 것)")
    A("")
    rows = [(i + 1, f["what_kind"], f["what"], f["site"] or "none", f"{f['technique'] or 'none'}({f['technique_origin']})", f["status"], f["n_items"], " · ".join(f["items"]), ", ".join(f["unregistered"]) or "—")
            for i, f in enumerate(x for x in R["procedure"]["folded"] if x["n_items"] >= 2)]
    A(md_table(["#", "what 종류", "what", "site", "technique", "상태", "항목 수", "접힌 분류 항목(전부)", "미등록 조각"], rows))
    A("")
    A(f"v2 에서 접혔던 큰 묶음(M15-1 케미컬필링 60 · M7-3 브랜드 21 · M8-1 색소/토닝 16 · M9-1 HIFU 13 · M1-3 용도별 9 …)은 v2.1 에서 전부 항목 하나짜리 튜플(9.5.3, what=항목 자신)로 갈라졌다. 접힌 튜플 {s['catalog_tuples_with_2plus_items']} 개 전부 미등록 조각 0.")
    A("")
    A("#### 9.5.3 항목 하나짜리 튜플 (접히지 않은 것 전부)")
    A("")
    rows = [(i + 1, f["what_kind"], f["what"], f["site"] or "none", f"{f['technique'] or 'none'}({f['technique_origin']})", f["status"], f["items"][0], ", ".join(f["unregistered"]) or "—")
            for i, f in enumerate(x for x in R["procedure"]["folded"] if x["n_items"] == 1)]
    A(md_table(["#", "what 종류", "what", "site", "technique", "상태", "분류 항목", "미등록 조각(candidate_name)"], rows))
    A("")
    A("#### 9.5.4 참조 자리 전부(②) + market-pricing(③) → 튜플 (v2.1: 미등록 조각 있으면 미해결 ⑨ · 튜플 없음)")
    A("")
    rows = []
    v2slots = g("reference_slots", {})

    def srow(name, v, w):
        return (name, v["n"], v["tuple"], v["combo_ref"], v["unresolved"], v["none"], v["complete"], v["partial"], v["distinct_tuples"], v["new_tuples_not_from_catalog"],
                (f"{w['tuple']}/{w['combo_ref']}/{w['none']}/{w['partial']}/{w['distinct_tuples']}" if w else "—"))
    for k, v in s["reference_slots"].items():
        rows.append(srow(k, v, v2slots.get(k)))
    rows.append(srow("**② 합계**", s["reference_total"], g("reference_total", None)))
    rows.append(srow("**③ market-pricing.items[].name (122)**", s["market_pricing"], g("market_pricing", None)))
    A(md_table(["참조 자리", "건", "튜플", "combo_ref", "미해결(⑨)", "튜플 불가", "complete", "partial", "distinct 튜플", "①에 없는 새 튜플", "v2 튜플/combo/불가/partial/distinct"], rows))
    A("")
    A(f"②·③ 튜플의 what 종류: ② {_kv(s['reference_total']['by_what_kind'])} · ③ {_kv(s['market_pricing']['by_what_kind'])} (catalog_item = 참조가 분류 항목 이름에 닿았고 그 항목의 what 이 항목 자신인 경우 — 그 항목의 튜플로 간다, 부모 층 아님).")
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
            elif r["result"] == "unresolved":
                parts.append(lab + f" → 미해결 미등록[{','.join(r['unregistered'])}]")
            else:
                parts.append(lab + " → 튜플 불가")
        A(f"- **{k}**: " + " · ".join(parts))
    A("")
    A("#### 9.5.5 튜플 전체 집계 (① ② ③ 합집합 · v2 → v2.1)")
    A("")
    A(md_table(["항목", "v2", "v2.1"], [
        ("튜플 수", f"**{g('tuples_total')}**", f"**{s['tuples_total']}**"),
        ("원천별", _kv(g("tuples_by_origin", {})), _kv(s["tuples_by_origin"])),
        ("what 종류", _kv(g("tuples_by_what_kind", {})), _kv(s["tuples_by_what_kind"])),
        ("상태", _kv(g("tuples_status", {})), _kv(s["tuples_status"])),
        ("site none 비율", g("tuples_site_none_ratio"), f"{s['tuples_site_none_ratio']} (what 이 사전 값인 튜플만: {s['tuples_dict_what_site_none_ratio']})"),
        ("technique none 비율", f"{g('tuples_technique_none_ratio')} · 출처 " + _kv(g("tuples_technique_origin", {})), f"{s['tuples_technique_none_ratio']} · 출처 " + _kv(s["tuples_technique_origin"])),
        ("미등록 조각", f"distinct {g('unregistered_distinct')} · 총 {g('unregistered_total')}", f"distinct {s['unregistered_distinct']} · 총 {s['unregistered_total']} (분류 항목은 candidate_name 으로 튜플에 보존 · 참조는 미해결 기록)"),
    ]))
    A("")
    A(f"#### 9.5.6 미등록 조각 상위 30 (어느 축인지는 판정하지 않는다 — 사전 추가는 실버 빌드의 결정 묶음 · v2 distinct {g('unregistered_distinct')}/총 {g('unregistered_total')} → v2.1 distinct {s['unregistered_distinct']}/총 {s['unregistered_total']}: 차이는 통째 일치(§1.4 조각 규칙)로 더 이상 쪼개지 않는 「PRP/자가혈」「마이크로니들링(MTS)」「리쥬란 HB+」「바이오스티뮬레이터/콜라겐부스터」 분 · 사전은 안 바뀌었다)")
    A("")
    A("- 전체: " + " · ".join(f"`{f}`×{n}" for f, n in s["unregistered_top30"]))
    for k, v in s["unregistered_top30_by_origin"].items():
        A(f"- {k}: " + (" · ".join(f"`{f}`×{n}" for f, n in v) or "—"))
    return "\n".join(o)


def adverse_md(R):
    s = R["adverse"]["summary"]
    o = [V2.adverse_md(R), "", "#### 9.6.6 검산 항목(v2.1 발주서): 미등록 조각 있는 이름이 접혔는가 — 부작용 튜플은 손대지 않았다", ""]
    o.append(f"- 둘 이상 이름이 접힌 부작용 튜플 {s['folded_with_2plus_names']} 중 미등록 조각 있는 이름이 섞인 튜플 **{s['folded_with_partial_name']}**.")
    if s["folded_with_partial_name"]:
        o.append("- 발주서의 전제(「같은 원칙이 이미 적용돼 있다」)와 **다르다**: 부작용 튜플은 event×site×course 세 축이 사전 값이면 접히고, 이름의 수식 조각(「기저 위험」「반응」「시술 직후」…)이 미등록이어도 접힌다(§1.5 규칙 그대로). 아래 표가 그 전부다. 처분은 사용자 결정(v2.1 범위 밖 · 손대지 않음).")
        o.append("")
        o.append(md_table(["#", "event", "site", "course", "접힌 이름(전부)", "미등록 조각"], [(i + 1, d["event"], d["site"] or "none", d["course"], " · ".join(d["names"]), ", ".join(d["unregistered"])) for i, d in enumerate(s["folded_partial_detail"])]))
    return "\n".join(o)


def load_all():
    for name in ("erd-v2.1-dictionaries.json", "erd-v2-dictionaries.json"):
        if os.path.exists(os.path.join(HERE, name)):
            dic = json.load(open(os.path.join(HERE, name), encoding="utf-8"))
            break
    try:
        erd = json.load(open(os.path.join(HERE, "erd-v2.1.json"), encoding="utf-8"))
        rules, rrules = erd["tuple_rules"], erd["resolve_rules"]
    except (FileNotFoundError, KeyError):
        sys.path.insert(0, HERE)
        import erd_spec_v21
        rules, rrules = erd_spec_v21.TUPLE_RULES, erd_spec_v21.RESOLVE_RULES
    files = [f for f in os.listdir(LEDGER) if f.endswith(".json")]
    L = {f: json.load(open(os.path.join(LEDGER, f), encoding="utf-8")) for f in files}
    return dic, rules, rrules, L


def main():
    dic, rules, rrules, L = load_all()
    R = run_all(dic, rules, L, rrules)
    print(procedure_md(R))
    print()
    print(adverse_md(R))
    json.dump(R, open(os.path.join(HERE, "erd-v2.1-tuples.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    print("\n→ erd-v2.1-tuples.json")


if __name__ == "__main__":
    main()
