#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ERD v2.2 — 튜플 분해 실측기. v2.1(erd-v2.1-tuples.py) 위에 독립 검토(erd-v2.1-review.md) 반영 시술 규칙 3건만 바꾼다. 독립 실행.

v2.1 → v2.2 (발주서 erd-v2.2-brief.md 수정 1·2·3):
  1. 미상은 식별자 값이 아니다. 접힘 조건 = 「세 칸 전부 사전 값일 때만」(what ∈ product|modality_subcategory|modality · site ≠ none · technique ≠ none).
     미상 칸이 하나라도 있거나 what 이 항목 자신(CAT-)이면 식별자에 anchor 를 섞는다:
       PRC-sha256(what_id|site_id|technique_id|anchor)[:10] — anchor = 분류 항목 CAT- id(①) · 참조 REF- id(②③, REF-sha256(norm(label)|hint)) · 조합 멤버는 anchor#m<i>.
     세 칸 전부 사전 값이면 v2 그대로 PRC-sha256(what_id|site_id|technique_id)[:10] — 그때만 다른 항목·참조와 접힌다.
     참조(또는 조합 멤버)가 분류 항목 이름과 정규화 완전 일치(①)하면 그 참조는 그 항목 자체라 그 항목의 anchor 를 쓴다(같은 튜플 — 접힘 아님). 규격·수식·계열명 조각이 붙은 참조는 자기 anchor.
  2. 조각을 버리고 접지 않는다. primary(what 후보) 조각이 둘 이상(조합 아님) · site 조각이 둘 이상 · technique 조각이 둘 이상 ·
     what 으로 쓸 수 없는 primary 조각이 있으면 사전 값으로 조립하지 않는다 — 분류 항목은 항목 자신 튜플(status ambiguous), 참조는 미해결(⑨).
     조합(combo_ref)은 멤버 밖에 primary·site 조각이 없을 때만. 같은 계열의 계열명 조각(what 의 계열과 같은 modality 조각)은 what 의 상위(R1·R4)로 이미 담기므로 버린 조각이 아니다(family_fragments 로 기록).
     v2.1 규칙 8(primary 여럿 → 우선순위 하나만 what, 나머지 extra_primaries) 삭제. 산출물의 primaries[]/sites[]/techniques[]/extra_primaries[]/extra_sites[] 는 항상 실제 값(null 아님).
  3. 기법 상속을 끈다. technique = 이름 조각이 기법 사전에 닿을 때만(fragment), 아니면 none. R5 계열 → 기법은 결정 kind canonical_mapping 후보로만 목록(inheritance_candidates).
부작용 튜플·adverse_expression 은 v2 그대로(코드 재사용).

입력(같은 폴더): erd-v2.2-dictionaries.json(없으면 v2.1) · erd-v2.2.json(tuple_rules/resolve_rules — 없으면 erd_spec_v22) · erd-v2.1-tuples.py · erd-v2-tuples.py ·
      erd-v1.1-resolve.py · 원장 21 · erd-v2.1-tuples.json(§9.5 나란히 비교용)
출력: 표준 출력에 §9.5/§9.6 표 + erd-v2.2-tuples.json
실행: python3 erd-v2.2-tuples.py
"""
import importlib.util
import json
import os
import sys
from collections import Counter, OrderedDict, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


V21 = load_module("erd_v21_tuples", os.path.join(HERE, "erd-v2.1-tuples.py"))
V2 = V21.V2
norm, mkid, md_table, with_alias, LEDGER = V2.norm, V2.mkid, V2.md_table, V2.with_alias, V2.LEDGER
PRIMARY_KINDS = V2.PRIMARY_KINDS
DICT_WHAT_KINDS = V21.DICT_WHAT_KINDS


def ref_anchor(label, hint):
    """참조 anchor = 정규화 라벨 + 계열 힌트. 같은 라벨·같은 힌트는 정규화 완전 일치(①)라 자리가 달라도 같은 참조다."""
    return mkid("REF", f"{label}|{hint}")


def tuple_id(what_id, site_id, tech_id, what_kind, anchor):
    """수정 1: 세 칸 전부 사전 값일 때만 anchor 없이(접힘 가능). 아니면 anchor 를 섞어 항목·참조마다 고유."""
    all_dict = what_kind in DICT_WHAT_KINDS and site_id != "none" and tech_id != "none"
    key = f"{what_id}|{site_id}|{tech_id}" + ("" if all_dict else f"|{anchor}")
    return mkid("PRC", key), all_dict


class ProcedureTuples22(V21.ProcedureTuples21):
    """v2.1 위에 수정 1(anchor)·2(조각 버림 금지)·3(상속 끔)."""

    # --- 튜플 등록 (식별자 = 수정 1)
    def register22(self, what_kind, what, site, tech, origin, src, unregistered, anchor, status_extra=None, matched=None):
        site_id = site["id"] if site else "none"
        tech_id = self.ids.tech[norm(tech)]["id"] if tech else "none"
        tid, all_dict = tuple_id(what["id"], site_id, tech_id, what_kind, anchor)
        t = self.tuples.get(tid)
        if t is None:
            t = {"id": tid, "what_kind": what_kind, "what_id": what["id"], "what_label": what["label"], "family": what.get("family"),
                 "site": site["label"] if site else None, "site_id": site_id, "technique": tech, "technique_id": tech_id, "technique_origin": "fragment" if tech else "none",
                 "all_dict_values": all_dict, "anchor": None if all_dict else anchor, "origins": [], "status": "complete", "unregistered_fragments": [], "sources": []}
            self.tuples[tid] = t
        if origin not in t["origins"]:
            t["origins"].append(origin)
        t["sources"].append(dict(src, anchor=anchor, matched_text=matched if matched is not None else src.get("label")))
        for u in unregistered:
            if u not in t["unregistered_fragments"]:
                t["unregistered_fragments"].append(u)
        if unregistered:
            t["status"] = "partial"
        elif status_extra == "ambiguous" and t["status"] == "complete":
            t["status"] = "ambiguous"
        return tid

    # --- primary 조각 → what (None = what 으로 쓸 수 없음)
    def what_of(self, s, family, for_item):
        k = s["kind"]
        if k == "procedure":
            fam = s.get("code")
            cands = [x for x in self.item_index.get(norm(s["canonical"]), []) if ("|" not in str(fam) and x[0] == fam) or "|" in str(fam)]
            if not cands:
                cands = self.item_index.get(norm(s["canonical"]), [])
            if not cands:
                return None
            fam2, sub2, name2 = cands[0]
            rec = self.catalog_tuple(fam2, sub2, name2)
            if rec is None or not rec.get("procedure_id") or rec["result"] != "tuple":
                return None
            t = self.tuples[rec["procedure_id"]]
            if for_item and t["what_kind"] not in DICT_WHAT_KINDS:
                return None  # 항목 자신이 what 인 항목에 닿은 조각 — 이 항목의 what 으로 쓸 수 없다(v2.1 그대로)
            return {"kind": t["what_kind"], "what": {"id": t["what_id"], "label": t["what_label"], "family": t["family"]},
                    "basis": f"catalog_item:{name2}[{fam2}]→{t['what_kind']}:{t['what_label']}",
                    "via_item": {"family": fam2, "name": name2, "cat_id": mkid("CAT", f"{fam2}|{name2}"), "procedure_id": rec["procedure_id"],
                                 "anchor": t["anchor"], "site": (t["site"], t["site_id"]) if t["site_id"] != "none" else None,
                                 "technique": t["technique"] if t["technique_id"] != "none" else None}}
        w = self.what_from_span(s, family, for_item)  # v2.1 (product · subcategory · modality)
        if not w:
            return None
        return {"kind": w[0], "what": w[1], "basis": w[2], "via_item": None}

    @staticmethod
    def _frag(s):
        return f"{s['kind']}:{s['canonical']}"

    def assemble22(self, groups, family, for_item, anchor, label_text=None):
        """묶음·멤버 → (조합 | 튜플 | 모호). 버린 조각 0 이 조건."""
        all_spans = [s for g in groups for m in g["members"] for s in m["spans"]]
        untouched = [u["text"] for g in groups for m in g["members"] for u in m["untouched"]]
        qualifiers = [(s["kind"], s["canonical"]) for s in all_spans if s["kind"] in ("spec", "product_tier")]
        frag = {"primaries": [self._frag(s) for s in all_spans if s["kind"] in PRIMARY_KINDS],
                "sites": list(dict.fromkeys(s["canonical"] for s in all_spans if s["kind"] == "site")),
                "techniques": list(dict.fromkeys(s["canonical"] for s in all_spans if s["kind"] == "technique"))}
        base = {"untouched": untouched, "qualifiers": qualifiers, "fragments": frag}
        if for_item and untouched:
            return dict(base, kind="self", reason="unregistered", status="partial")
        # 조합
        combo_members = None
        for g in groups:
            pm = [m for m in g["members"] if any(s["kind"] in PRIMARY_KINDS for s in m["spans"])]
            if len(pm) >= 2:
                combo_members = pm
                break
        if combo_members is not None:
            cm = {id(m) for m in combo_members}
            subs = [dict(self.assemble22([{"where": "member", "members": [m]}], family, for_item, f"{anchor}#m{i}", m["text"]), text=m["text"]) for i, m in enumerate(combo_members)]
            member_fams = {str(x["what"].get("family")) for x in subs if x["kind"] == "tuple"}
            outside = [s for g in groups for m in g["members"] if id(m) not in cm for s in m["spans"]]
            bad = [self._frag(s) for s in outside if s["kind"] == "site" or s["kind"] == "technique" or (s["kind"] in PRIMARY_KINDS and not (s["kind"] == "modality" and str(s.get("code")) in member_fams))]
            if bad:
                return dict(base, kind="ambiguous", reason="combo_outside_fragment", status="ambiguous", detail=bad)
            badm = [x for x in subs if x["kind"] != "tuple"]
            if badm:
                return dict(base, kind="ambiguous", reason="combo_member_" + badm[0].get("reason", badm[0]["kind"]), status="ambiguous", detail=[x.get("fragments") for x in badm])
            fam_frags = [self._frag(s) for s in outside if s["kind"] == "modality"]
            return dict(base, kind="combo_ref", members=subs, family_fragments=fam_frags)
        # what 후보
        prim, fam_frags, unusable = [], [], []
        for s in all_spans:
            if s["kind"] not in PRIMARY_KINDS:
                continue
            s2 = s
            if s["kind"] == "modality":
                ph = self.R.lex.hits("product", s["text"])
                if ph:  # 계열명 = 제품명 (v2 규칙 9 그대로 — 1-E 는 결정 레코드 몫)
                    hh = {x for x in ph if self.R._in_family(x[0], family)} or ph
                    x = sorted(hh, key=lambda z: str(z))[0]
                    s2 = {"kind": "product", "text": s["text"], "code": x[0], "canonical": x[1], "cross_family": not self.R._in_family(x[0], family)}
                elif for_item:
                    if str(s.get("code")) == str(family):
                        fam_frags.append(s)  # 항목 자신의 계열명 — R2 상위로 이미 담김
                        continue
                    unusable.append(self._frag(s))  # 다른 계열명 — 분류 항목의 what 으로 쓸 수 없고 버릴 수도 없다
                    continue
            w = self.what_of(s2, family, for_item)
            if w is None:
                unusable.append(self._frag(s))
                continue
            prim.append((s2, w))
        # 참조: what 의 계열과 같은 계열명 조각은 상위(버린 것 아님)
        non_mod_fams = {str(w["what"].get("family")) for s2, w in prim if w["kind"] != "modality"}
        keep = []
        for s2, w in prim:
            if w["kind"] == "modality" and str(w["what"].get("family")) in non_mod_fams:
                fam_frags.append(s2)
                continue
            keep.append((s2, w))
        # 같은 what 을 두 번 가리키면 하나
        seen, uniq = set(), []
        for s2, w in keep:
            if w["what"]["id"] in seen:
                continue
            seen.add(w["what"]["id"])
            uniq.append((s2, w))
        base["family_fragments"] = [self._frag(s) for s in fam_frags]
        if unusable:
            return dict(base, kind="ambiguous", reason="unusable_primary", status="ambiguous", detail=unusable)
        if len(uniq) >= 2:
            return dict(base, kind="ambiguous", reason="multi_primary", status="ambiguous", detail=[w["basis"] for _, w in uniq])
        via = uniq[0][1]["via_item"] if uniq else None
        sites = list(frag["sites"])
        if via and via["site"] and via["site"][0] not in sites:
            sites.append(via["site"][0])
        techs = list(frag["techniques"])
        if via and via["technique"] and via["technique"] not in techs:
            techs.append(via["technique"])
        if len(sites) >= 2:
            return dict(base, kind="ambiguous", reason="multi_site", status="ambiguous", detail=sites)
        if len(techs) >= 2:
            return dict(base, kind="ambiguous", reason="multi_technique", status="ambiguous", detail=techs)
        if uniq:
            s2, w = uniq[0]
            what_kind, what, basis = w["kind"], w["what"], w["basis"]
        elif for_item:
            return dict(base, kind="self", reason="no_primary", status="complete")
        else:
            return dict(base, kind="hint_only")  # 참조: primary 없음 → 자리 힌트 계열(호출부)
        site = self.ids.site[norm(sites[0])] if sites else None
        tech = techs[0] if techs else None
        # 참조(멤버)가 분류 항목 이름과 정규화 완전 일치(①)면 그 항목 자체 → 그 항목의 anchor. 규격·수식·계열명 조각이 붙으면 자기 anchor
        own_anchor = anchor
        exact = (via is not None and len(all_spans) == 1 and all_spans[0]["kind"] == "procedure" and not untouched and label_text is not None and norm(all_spans[0]["text"]) == norm(label_text))
        if exact:
            own_anchor = via["anchor"] or anchor
        return dict(base, kind="tuple", what_kind=what_kind, what=what, what_basis=basis, site=site, technique=tech, anchor=own_anchor,
                    extra_primaries=[], extra_sites=[], via_item=via["name"] if via else None)

    def _self(self, family, name, a):
        """분류 항목 자신 튜플 — 사전 값 조립 없음. 닿은 site·technique 가 하나씩일 때만 그 칸에, 둘 이상이면 none + extra 에 실값."""
        what = self.cat_what(family, name)
        f = a["fragments"]
        site = self.ids.site[norm(f["sites"][0])] if len(f["sites"]) == 1 else None
        tech = f["techniques"][0] if len(f["techniques"]) == 1 else None
        return {"what_kind": "catalog_item", "what": what, "site": site, "technique": tech,
                "extra_primaries": list(f["primaries"]), "extra_sites": list(f["sites"]) if len(f["sites"]) != 1 else [],
                "extra_techniques": list(f["techniques"]) if len(f["techniques"]) != 1 else []}

    # --- ① 분류 항목
    def catalog_tuple(self, family, sub, name):
        key = (family, name)
        if key in self.catalog:
            return self.catalog[key]
        if key in self._busy:
            return None
        self._busy.add(key)
        cat_id = self.cat_what(family, name)["id"]
        groups, whole = self.decompose_whole_first(name, family, exclude=norm(name))
        a = self.assemble22(groups, family, True, cat_id, name)
        rec = {"family": family, "subcategory": sub, "name": name, "catalog_item_id": cat_id, "whole_match": whole, "anchor": cat_id,
               "groups": [{"where": g["where"], "members": [{"text": m["text"], "spans": [(s["kind"], s["canonical"]) for s in m["spans"]], "untouched": [u["text"] for u in m["untouched"]]} for m in g["members"]]} for g in groups],
               "fragments": a["fragments"], "family_fragments": a.get("family_fragments", [])}
        src = {"origin": "catalog_item", "label": name, "family": family, "catalog_item_id": cat_id}
        if a["kind"] == "combo_ref":
            ids = [self.register22(m["what_kind"], m["what"], m["site"], m["technique"], "catalog_item", src, [], m["anchor"], matched=m["text"]) for m in a["members"]]
            rec.update({"result": "combo_ref", "procedure_id": ids[0] if ids else None, "member_ids": ids, "unregistered": [], "qualifiers": a["qualifiers"], "what_basis": "combo", "status": "complete",
                        "extra_primaries": [], "extra_sites": []})
        elif a["kind"] == "tuple":
            tid = self.register22(a["what_kind"], a["what"], a["site"], a["technique"], "catalog_item", src, [], cat_id)
            rec.update({"result": "tuple", "procedure_id": tid, "what_kind": a["what_kind"], "what_basis": a["what_basis"], "site": a["site"]["label"] if a["site"] else None,
                        "technique": a["technique"], "technique_origin": "fragment" if a["technique"] else "none", "unregistered": [], "qualifiers": a["qualifiers"], "status": "complete",
                        "extra_primaries": [], "extra_sites": [], "candidate_name": []})
        else:  # self (unregistered | no_primary) · ambiguous → 항목 자신
            sf = self._self(family, name, a)
            st = a.get("status", "complete")
            tid = self.register22("catalog_item", sf["what"], sf["site"], sf["technique"], "catalog_item", src, a["untouched"], cat_id, status_extra=st)
            self.tuples[tid]["candidate_name"] = list(a["untouched"])
            reason = a.get("reason")
            rec.update({"result": "tuple", "procedure_id": tid, "what_kind": "catalog_item", "what_basis": f"self:{reason}", "self_reason": reason, "self_detail": a.get("detail", []),
                        "site": sf["site"]["label"] if sf["site"] else None, "technique": sf["technique"], "technique_origin": "fragment" if sf["technique"] else "none",
                        "unregistered": a["untouched"], "qualifiers": a["qualifiers"], "status": st, "candidate_name": list(a["untouched"]),
                        "extra_primaries": sf["extra_primaries"], "extra_sites": sf["extra_sites"], "extra_techniques": sf["extra_techniques"]})
        self.catalog[key] = rec
        self._busy.discard(key)
        return rec

    # --- ② ③ 참조
    def run_reference(self, label, hint, origin, slot):
        anc = ref_anchor(label, hint)
        if isinstance(label, str) and label.startswith("__MODALITY__"):
            code = label[12:]
            tid = self.register22("modality", self.ids.mod[code], None, None, origin, {"origin": origin, "slot": slot, "label": code, "family": code}, [], anc)
            return {"label": code, "hint": code, "ref_id": anc, "result": "tuple", "procedure_id": tid, "what_kind": "modality", "what_basis": "modality_code", "status": "complete", "unregistered": [], "qualifiers": [],
                    "fragments": {"primaries": [f"modality:{code}"], "sites": [], "techniques": []}, "extra_primaries": [], "extra_sites": [], "technique_origin": "none"}
        if isinstance(label, str) and label.startswith("__SUBID__"):
            sid = label[9:]
            e = self.ids.sub[sid]
            tid = self.register22("modality_subcategory", e, None, None, origin, {"origin": origin, "slot": slot, "label": sid, "family": hint}, [], anc)
            return {"label": sid, "hint": hint, "ref_id": anc, "result": "tuple", "procedure_id": tid, "what_kind": "modality_subcategory", "what_basis": "subcategory_id", "status": "complete", "unregistered": [], "qualifiers": [],
                    "fragments": {"primaries": [f"modality_subcategory:{e['label']}"], "sites": [], "techniques": []}, "extra_primaries": [], "extra_sites": [], "technique_origin": "none"}
        groups, whole = self.decompose_whole_first(label, hint)
        a = self.assemble22(groups, hint, False, anc, str(label))
        base = {"label": label, "hint": hint, "ref_id": anc, "whole_match": whole, "fragments": a["fragments"], "family_fragments": a.get("family_fragments", []),
                "groups": [{"where": g["where"], "members": [{"text": m["text"], "spans": [(s["kind"], s["canonical"]) for s in m["spans"]], "untouched": [u["text"] for u in m["untouched"]]} for m in g["members"]]} for g in groups]}
        src = {"origin": origin, "slot": slot, "label": label, "family": hint, "ref_id": anc}
        if a["untouched"]:
            base.update({"result": "unresolved", "unresolved_reason": "unregistered", "unregistered": a["untouched"], "qualifiers": a["qualifiers"], "reason": "미등록 조각 있음 → ⑨ 미해결",
                         "extra_primaries": list(a["fragments"]["primaries"]), "extra_sites": list(a["fragments"]["sites"])})
            return base
        if a["kind"] == "ambiguous":
            base.update({"result": "unresolved", "unresolved_reason": a["reason"], "unregistered": [], "qualifiers": a["qualifiers"], "detail": a.get("detail"),
                         "reason": {"multi_primary": "primary 조각 둘 이상(조합 아님) → ⑨ 미해결 (버리고 접지 않음)", "multi_site": "site 조각 둘 이상 → ⑨ 미해결", "multi_technique": "technique 조각 둘 이상 → ⑨ 미해결",
                                    "unusable_primary": "what 으로 쓸 수 없는 primary 조각 → ⑨ 미해결", "combo_outside_fragment": "조합 멤버 밖 primary/site 조각 → ⑨ 미해결"}.get(a["reason"], a["reason"] + " → ⑨ 미해결"),
                         "extra_primaries": list(a["fragments"]["primaries"]), "extra_sites": list(a["fragments"]["sites"])})
            return base
        if a["kind"] == "combo_ref":
            ids = [self.register22(m["what_kind"], m["what"], m["site"], m["technique"], origin, dict(src, member=True), [], m["anchor"], matched=m["text"]) for m in a["members"]]
            base.update({"result": "combo_ref", "member_ids": list(dict.fromkeys(ids)), "member_count": len(a["members"]), "unregistered": [], "qualifiers": a["qualifiers"], "status": "complete", "extra_primaries": [], "extra_sites": []})
            return base
        if a["kind"] == "tuple":
            tid = self.register22(a["what_kind"], a["what"], a["site"], a["technique"], origin, src, [], a["anchor"])
            base.update({"result": "tuple", "procedure_id": tid, "what_kind": a["what_kind"], "what_basis": a["what_basis"], "site": a["site"]["label"] if a["site"] else None, "technique": a["technique"],
                         "technique_origin": "fragment" if a["technique"] else "none", "unregistered": [], "qualifiers": a["qualifiers"], "status": "complete", "anchor": a["anchor"], "via_item": a.get("via_item"),
                         "extra_primaries": [], "extra_sites": []})
            return base
        # hint_only: primary 없음 → 자리 힌트 계열 (v2.1 그대로). 부위·기법 조각은 칸에
        if hint and hint in self.ids.mod:
            f = a["fragments"]
            site = self.ids.site[norm(f["sites"][0])] if f["sites"] else None
            tech = f["techniques"][0] if f["techniques"] else None
            tid = self.register22("modality", self.ids.mod[hint], site, tech, origin, src, [], anc)
            base.update({"result": "tuple", "procedure_id": tid, "what_kind": "modality", "what_basis": f"hint_family:{hint}", "site": site["label"] if site else None, "technique": tech,
                         "technique_origin": "fragment" if tech else "none", "unregistered": [], "qualifiers": a["qualifiers"], "status": "complete", "anchor": anc, "extra_primaries": [], "extra_sites": []})
            return base
        base.update({"result": "none", "unregistered": [], "qualifiers": a["qualifiers"], "reason": "primary 조각도 계열 힌트도 없음", "extra_primaries": [], "extra_sites": list(a["fragments"]["sites"])})
        return base


# ---------------------------------------------------------------------------
# 전체 실행 · 집계
# ---------------------------------------------------------------------------
def run_all(dic_json, rules, L, resolve_rules=None):
    if resolve_rules is None:
        sys.path.insert(0, HERE)
        import erd_spec_v22
        resolve_rules = erd_spec_v22.RESOLVE_RULES
    ids = V2.Ids(dic_json, L)
    lex = V2.V11.Lexicon(with_alias(dic_json))
    PT = ProcedureTuples22(lex, resolve_rules, ids, L)
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
                "unresolved_by_reason": dict(Counter(r.get("unresolved_reason") for r in rows if r["result"] == "unresolved")),
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
    # 접힘(전 원천): 서로 다른 anchor 가 둘 이상 들어간 튜플
    multi_anchor = []
    for t in T.values():
        anchors = list(dict.fromkeys(s["anchor"] for s in t["sources"]))
        if len(anchors) >= 2:
            multi_anchor.append({"procedure_id": t["id"], "what_kind": t["what_kind"], "what": t["what_label"], "site": t["site"], "technique": t["technique"], "all_dict_values": t["all_dict_values"],
                                 "n_anchors": len(anchors), "labels": list(dict.fromkeys(f"{s['label']}" + (f"@{s.get('slot', '')[:20]}" if s.get("slot") else "") for s in t["sources"]))})
    # 기법 상속 후보 (canonical_mapping 후보 — 적용 안 함)
    inh = []
    for fam, techs in sorted(ids.family_tech.items()):
        if len(techs) != 1:
            continue
        ts = [t for t in T.values() if t["technique_id"] == "none" and str(t.get("family")) == fam]
        cat_items = [r for r in cat_recs if r["family"] == fam and r.get("technique_origin") == "none"]
        inh.append({"kind": "canonical_mapping", "from_ref": f"R5:{fam}", "to_technique": techs[0], "to_id": ids.tech[norm(techs[0])]["id"], "scope": f"technique=none 인 {fam} 튜플",
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
        ("inheritance_candidates", [{k: v for k, v in c.items() if k != "items"} for c in inh]),
        ("unregistered_distinct", len(unreg_all)),
        ("unregistered_total", sum(unreg_all.values())),
        ("unregistered_top30", unreg_all.most_common(30)),
        ("unregistered_top30_by_origin", {k: v.most_common(30) for k, v in unreg_by_origin.items()}),
    ])
    adv = V2.run_all(dic_json, rules, L, resolve_rules)["adverse"]
    af2 = [f for f in adv["folded"] if f["n_names"] >= 2]
    adv["summary"]["folded_with_2plus_names"] = len(af2)
    adv["summary"]["folded_with_partial_name"] = sum(1 for f in af2 if f["status"] == "partial")
    adv["summary"]["folded_partial_detail"] = [{"event": f["event"], "site": f["site"], "course": f["course"], "names": f["names"], "unregistered": f["unregistered"]} for f in af2 if f["status"] == "partial"]
    out = OrderedDict([
        ("erd_version", "v2.2"), ("rules", rules["name"]), ("fallback_to_parent", False), ("fold_condition", "세 칸 전부 사전 값일 때만"), ("technique_inheritance", False),
        ("procedure", OrderedDict([("summary", proc_summary), ("tuples", list(T.values())), ("catalog", cat_recs), ("folded", folded), ("multi_anchor", multi_anchor),
                                   ("inheritance_candidates", inh), ("references", ref_rows), ("market_pricing", mk_rows)])),
        ("adverse", adv),
    ])
    return out


def v21_split(R, v21=None):
    """수정 1 실측: v2.1 에서 미상 칸(site/technique none)이 있는데 서로 다른 라벨(항목·참조)이 한 튜플로 접혔던 것 전부 → v2.2 에서 어디로 갔는지.
    갈라짐 = v2.2 에서 서로 다른 정규화 라벨이 같은 튜플에 남지 않음(같은 라벨 = ① 정규화 완전 일치는 같은 튜플이 맞다)."""
    if v21 is None:
        try:
            v21 = json.load(open(os.path.join(HERE, "erd-v2.1-tuples.json"), encoding="utf-8"))
        except FileNotFoundError:
            return []
    P = R["procedure"]
    TT = {t["id"]: t for t in P["tuples"]}
    cat = {(r["family"], r["name"]): r for r in P["catalog"]}
    refs = {}
    for rows in list(P["references"].values()) + [P["market_pricing"]]:
        for r in rows:
            refs.setdefault((r["label"], r.get("hint")), r)
    out = []
    for t in v21["procedure"]["tuples"]:
        labs = list(dict.fromkeys((s["origin"], s["label"], s.get("family")) for s in t["sources"]))
        subj = {((x[2] if x[0] == "catalog_item" else None), norm(x[1])) for x in labs}  # 분류 항목은 (계열, 이름) — 볼뉴머[M4]·[M9] 는 다른 항목
        if t["what_kind"] not in DICT_WHAT_KINDS or (t["site_id"] != "none" and t["technique_id"] != "none") or len({k[1] for k in subj}) + len({k for k in subj if k[0]}) - len({k[1] for k in subj if k[0]}) < 2:
            continue
        dest = []
        for origin, label, fam in labs:
            r = cat.get((fam, label)) if origin == "catalog_item" else refs.get((label, fam))
            if not r:
                continue
            if r["result"] == "tuple":
                x = TT[r["procedure_id"]]
                dest.append({"label": label, "origin": origin, "result": "tuple", "procedure_ids": [x["id"]], "tuple": f"{x['what_kind']}:{x['what_label']}×{x['site'] or 'none'}×{x['technique'] or 'none'}", "anchor": x["anchor"]})
            elif r["result"] == "combo_ref":
                dest.append({"label": label, "origin": origin, "result": "combo_ref", "procedure_ids": list(r["member_ids"]), "tuple": "combo_ref[" + " + ".join(f"{TT[m]['what_label']}×{TT[m]['site'] or 'none'}×{TT[m]['technique'] or 'none'}" for m in r["member_ids"]) + "]", "anchor": None})
            else:
                dest.append({"label": label, "origin": origin, "result": r["result"], "procedure_ids": [], "tuple": "미해결:" + str(r.get("unresolved_reason") or r["result"]), "anchor": None})
        ids_ = {i for d in dest for i in d["procedure_ids"]}
        texts = {i: {norm(s["matched_text"]) for s in TT[i]["sources"]} for i in ids_}
        out.append({"v21_id": t["id"], "v21_tuple": f"{t['what_kind']}:{t['what_label']}×{t['site'] or 'none'}×{t['technique'] or 'none'}", "n_labels": len({k[1] for k in subj}) + len({k for k in subj if k[0]}) - len({k[1] for k in subj if k[0]}),
                    "v22_distinct_tuples": len(ids_), "v22_unresolved": sum(1 for d in dest if d["result"] == "unresolved"), "split": all(len(v) == 1 for v in texts.values()), "dest": dest})
    return out


def load_v21_summary():
    try:
        return json.load(open(os.path.join(HERE, "erd-v2.1-tuples.json"), encoding="utf-8"))["procedure"]["summary"]
    except (FileNotFoundError, KeyError):
        return None


def _kv(d):
    return ", ".join(f"{k}={v}" for k, v in (d or {}).items())


def procedure_md(R, v21s=None):
    s = R["procedure"]["summary"]
    v21s = v21s or load_v21_summary() or {}
    g = lambda k, d="—": v21s.get(k, d)  # noqa
    o = []
    A = o.append
    A("#### 9.5.1 분류 항목 521 → 튜플 (v2.1 → v2.2 나란히)")
    A("")
    A(md_table(["항목", "v2.1", "v2.2"], [
        ("분류 항목", g("catalog_items"), s["catalog_items"]),
        ("분해 결과", _kv(g("catalog_result", {})), _kv(s["catalog_result"])),
        ("튜플 수(distinct)", f"**{g('catalog_distinct_tuples')}** (비율 {g('catalog_fold_ratio')})", f"**{s['catalog_distinct_tuples']}** (521 → N · 비율 {s['catalog_fold_ratio']})"),
        ("둘 이상 항목이 접힌 튜플", f"{g('catalog_tuples_with_2plus_items')} 개 튜플에 항목 {g('catalog_items_in_folded_tuples')} 개", f"{s['catalog_tuples_with_2plus_items']} 개 튜플에 항목 {s['catalog_items_in_folded_tuples']} 개"),
        ("접힌 튜플 중 세 칸 전부 사전 값(site·technique 미상 없음)", f"{g('catalog_folded_all_dict_values')} (v2.1 은 미상 none 을 사전 값으로 셌다)", f"{s['catalog_folded_all_dict_values']} / {s['catalog_tuples_with_2plus_items']}"),
        ("what 축", _kv(g("catalog_by_what_kind", {})) + " · 근거: " + _kv(g("catalog_by_what_basis", {})), _kv(s["catalog_by_what_kind"]) + " · 근거: " + _kv(s["catalog_by_what_basis"])),
        ("항목 자신(catalog_item)이 what 인 항목", g("catalog_self_items"), f"{s['catalog_self_items']} (사유: {_kv(s['catalog_self_by_reason'])} · 그중 부위 칸 있음 {s['catalog_self_with_site']})"),
        ("site 축", f"none {g('catalog_site_none')} / 항목 기준 {g('catalog_site_none_ratio')}", f"none {s['catalog_site_none']} / 항목 기준 none 비율 {s['catalog_site_none_ratio']} · 튜플 기준 {s['catalog_tuple_site_none_ratio']}"),
        ("technique 축", _kv(g("catalog_technique", {})) + f" · 항목 기준 none {g('catalog_technique_none_ratio')}", _kv(s["catalog_technique"]) + f" · 항목 기준 none 비율 {s['catalog_technique_none_ratio']} · 튜플 기준 {s['catalog_tuple_technique_none_ratio']} (상속 삭제)"),
        ("항목 상태", _kv(g("catalog_status", {})), _kv(s["catalog_status"]) + " (ambiguous = 조각은 전부 사전에 닿았지만 primary·site·technique 가 둘 이상이거나 what 으로 못 쓰는 primary — 사전 값으로 조립하지 않음)"),
    ]))
    A("")
    A("#### 9.5.2 접힌 결과 — 둘 이상의 분류 항목이 같은 튜플로 간 것 전부 (세 칸 전부 사전 값만 남는다)")
    A("")
    rows = [(i + 1, f["what_kind"], f["what"], f["site"] or "none", f"{f['technique'] or 'none'}({f['technique_origin']})", f["n_items"], " · ".join(f["items"]))
            for i, f in enumerate(x for x in R["procedure"]["folded"] if x["n_items"] >= 2)]
    A(md_table(["#", "what 종류", "what", "site", "technique", "항목 수", "접힌 분류 항목(전부)"], rows) if rows else "(없음 — 접힌 분류 항목 0. 세 칸 전부 사전 값인 분류 항목 튜플이 서로 같은 경우가 없다)")
    A("")
    A("v2.1 §9.5.2 의 접힌 3건(볼뉴머[M4]·[M9] · 클라리티2·클라리티2 (혈관) · 피코슈어·피코슈어 프락셀) — v2.2 에서 어디로 갔는지:")
    A("")
    cat = {(r["family"], r["name"]): r for r in R["procedure"]["catalog"]}
    TT = {t["id"]: t for t in R["procedure"]["tuples"]}
    rows = []
    for fam, name in [("M4", "볼뉴머"), ("M9", "볼뉴머"), ("M8", "클라리티2"), ("M8", "클라리티2 (혈관)"), ("M8", "피코슈어"), ("M8", "피코슈어 프락셀")]:
        r = cat.get((fam, name))
        if not r:
            continue
        t = TT[r["procedure_id"]]
        rows.append((f"{name}[{fam}]", r["procedure_id"], f"{t['what_kind']}:{t['what_label']} × {t['site'] or 'none'} × {t['technique'] or 'none'}", r["status"], r.get("what_basis"), ", ".join(r.get("extra_primaries") or []) or "—", t["anchor"] or "(없음 · 세 칸 사전 값)"))
    A(md_table(["분류 항목", "튜플 id", "튜플", "상태", "what 근거", "extra_primaries(실값)", "식별자 anchor"], rows))
    A("")
    sp = R["procedure"].get("v21_none_fold_split") or []
    A(f"v2.1 에서 **미상 칸이 있는데 서로 다른 라벨이 한 튜플로 접혔던 것 전부 {len(sp)}**(분류 항목 3 + 참조 — 검토 1-A·②) → v2.2 행선지. 「갈라짐」= v2.2 에서 서로 다른 정규화 라벨이 같은 튜플에 남지 않음(같은 라벨은 ① 정규화 완전 일치라 같은 튜플이 맞다 · 참조가 분류 항목 이름과 같으면 그 항목 튜플). [ ] 는 v2.2 튜플 id 끝 4자리:")
    A("")
    A(md_table(["#", "v2.1 튜플", "라벨 수", "v2.2 distinct 튜플", "v2.2 미해결", "갈라짐", "라벨 → v2.2"], [(i + 1, x["v21_tuple"], x["n_labels"], x["v22_distinct_tuples"], x["v22_unresolved"], "○" if x["split"] else "✗",
                                                                                                    " · ".join(f"`{d['label']}`({d['origin'][:3]})→{d['tuple']}" + (f"[{','.join(i[-4:] for i in d['procedure_ids'])}]" if d['procedure_ids'] else "") for d in x["dest"])) for i, x in enumerate(sp)]))
    A("")
    A("#### 9.5.3 항목 하나짜리 튜플 (접히지 않은 것 전부)")
    A("")
    rows = []
    for i, f in enumerate(x for x in R["procedure"]["folded"] if x["n_items"] == 1):
        r = cat.get(tuple(f["keys"][0]))
        ex = ""
        if r:
            ex = "; ".join(x for x in [("P:" + ",".join(r.get("extra_primaries") or [])) if r.get("extra_primaries") else "", ("S:" + ",".join(r.get("extra_sites") or [])) if r.get("extra_sites") else ""] if x)
        rows.append((i + 1, f["what_kind"], f["what"], f["site"] or "none", f"{f['technique'] or 'none'}", f["status"], f["items"][0], ", ".join(f["unregistered"]) or "—", ex or "—"))
    A(md_table(["#", "what 종류", "what", "site", "technique", "상태", "분류 항목", "미등록 조각(candidate_name)", "extra(실값 · P=primary S=site)"], rows))
    A("")
    A("#### 9.5.4 참조 자리 전부(②) + market-pricing(③) → 튜플 (v2.2: 미등록 조각 · primary/site/technique 둘 이상 · 못 쓰는 primary → 미해결 ⑨)")
    A("")
    rows = []
    v21slots = g("reference_slots", {})

    def srow(name, v, w):
        return (name, v["n"], v["tuple"], v["combo_ref"], v["unresolved"], _kv(v["unresolved_by_reason"]) or "—", v["none"], v["distinct_tuples"], v["new_tuples_not_from_catalog"],
                (f"{w['tuple']}/{w['combo_ref']}/{w['unresolved']}/{w['distinct_tuples']}" if w else "—"))
    for k, v in s["reference_slots"].items():
        rows.append(srow(k, v, v21slots.get(k)))
    rows.append(srow("**② 합계**", s["reference_total"], g("reference_total", None)))
    rows.append(srow("**③ market-pricing.items[].name (122)**", s["market_pricing"], g("market_pricing", None)))
    A(md_table(["참조 자리", "건", "튜플", "combo_ref", "미해결(⑨)", "미해결 사유", "튜플 불가", "distinct 튜플", "①에 없는 새 튜플", "v2.1 튜플/combo/미해결/distinct"], rows))
    A("")
    A(f"②·③ 튜플의 what 종류: ② {_kv(s['reference_total']['by_what_kind'])} · ③ {_kv(s['market_pricing']['by_what_kind'])}.")
    A("")
    A("참조 행 전부 (라벨 → 결과):")
    A("")
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
                if r["unresolved_reason"] == "unregistered":
                    parts.append(lab + f" → 미해결 미등록[{','.join(r['unregistered'])}]")
                else:
                    parts.append(lab + f" → 미해결 {r['unresolved_reason']}[{','.join(str(x) for x in (r.get('detail') or []))}]")
            else:
                parts.append(lab + " → 튜플 불가")
        A(f"- **{k}**: " + " · ".join(parts))
    A("")
    A("#### 9.5.5 튜플 전체 집계 (① ② ③ 합집합 · v2.1 → v2.2)")
    A("")
    A(md_table(["항목", "v2.1", "v2.2"], [
        ("튜플 수", f"**{g('tuples_total')}**", f"**{s['tuples_total']}**"),
        ("원천별", _kv(g("tuples_by_origin", {})), _kv(s["tuples_by_origin"])),
        ("what 종류", _kv(g("tuples_by_what_kind", {})), _kv(s["tuples_by_what_kind"])),
        ("상태", _kv(g("tuples_status", {})), _kv(s["tuples_status"])),
        ("site none 비율", g("tuples_site_none_ratio"), f"{s['tuples_site_none_ratio']} (what 이 사전 값인 튜플만: {s['tuples_dict_what_site_none_ratio']})"),
        ("technique none 비율", f"{g('tuples_technique_none_ratio')} · 출처 " + _kv(g("tuples_technique_origin", {})), f"{s['tuples_technique_none_ratio']} · 출처 " + _kv(s["tuples_technique_origin"])),
        ("미상 칸(site 또는 technique none) 있는 튜플 비율", "—", s["tuples_any_none_ratio"]),
        ("세 칸 전부 사전 값 튜플 / anchor 튜플", "—", f"{s['tuples_all_dict_values']} / {s['tuples_anchored']}"),
        ("서로 다른 anchor(항목·참조)가 둘 이상 들어간 튜플", "—", f"{s['tuples_with_2plus_anchors']} (그중 미상 칸 있는 것 {s['tuples_with_2plus_anchors_not_all_dict']})"),
        ("미등록 조각", f"distinct {g('unregistered_distinct')} · 총 {g('unregistered_total')}", f"distinct {s['unregistered_distinct']} · 총 {s['unregistered_total']}"),
    ]))
    A("")
    ma = R["procedure"]["multi_anchor"]
    if ma:
        A("세 칸 전부 사전 값이라 둘 이상의 항목·참조가 접힌 튜플 전부:")
        A("")
        A(md_table(["#", "what", "site", "technique", "anchor 수", "라벨"], [(i + 1, f"{m['what_kind']}:{m['what']}", m["site"] or "none", m["technique"] or "none", m["n_anchors"], " · ".join(m["labels"])) for i, m in enumerate(ma)]))
        A("")
    A("#### 9.5.6 기법 상속 후보 — 결정 kind `canonical_mapping` 후보 (적용하지 않음 · v2.1 에서 자동 상속하던 것)")
    A("")
    A("R5 계열 → 기법이 하나인 계열(procedure-profiles mechanism[]). v2.2 는 붙이지 않는다. 사람이 승인하면 decision(kind=canonical_mapping, target={from_ref: \"R5:<계열>\", scope}, new_value={to_id: <기법 id>}, status=approved) 을 빌드가 읽어 scope 안의 technique=none 튜플에 붙인다. 아래 항목 목록이 그 scope 다(전부).")
    A("")
    A(md_table(["#", "from_ref", "to (기법)", "to_id", "technique none 튜플", "분류 항목 수", "분류 항목(전부)"], [(i + 1, c["from_ref"], c["to_technique"], c["to_id"], c["tuples"], c["catalog_items"], " · ".join(c["items"])) for i, c in enumerate(R["procedure"]["inheritance_candidates"])]))
    A("")
    A(f"상속 불가 계열(R5 기법 둘 이상 또는 없음): {', '.join(s['families_without_single_technique'])}.")
    A("")
    A(f"#### 9.5.7 미등록 조각 상위 30 (v2.1 distinct {g('unregistered_distinct')}/총 {g('unregistered_total')} → v2.2 distinct {s['unregistered_distinct']}/총 {s['unregistered_total']})")
    A("")
    A("- 전체: " + " · ".join(f"`{f}`×{n}" for f, n in s["unregistered_top30"]))
    for k, v in s["unregistered_top30_by_origin"].items():
        A(f"- {k}: " + (" · ".join(f"`{f}`×{n}" for f, n in v) or "—"))
    return "\n".join(o)


def adverse_md(R):
    return V21.adverse_md(R).replace("#### 9.6.6 검산 항목(v2.1 발주서): 미등록 조각 있는 이름이 접혔는가 — 부작용 튜플은 손대지 않았다",
                                      "#### 9.6.6 미등록 조각 있는 이름이 접혔는가 — 부작용 튜플은 v2.2 범위 밖(손대지 않음 · 검토 2-C·2-D 는 결정 몫)")


def load_all():
    for name in ("erd-v2.2-dictionaries.json", "erd-v2.1-dictionaries.json"):
        if os.path.exists(os.path.join(HERE, name)):
            dic = json.load(open(os.path.join(HERE, name), encoding="utf-8"))
            break
    try:
        erd = json.load(open(os.path.join(HERE, "erd-v2.2.json"), encoding="utf-8"))
        rules, rrules = erd["tuple_rules"], erd["resolve_rules"]
    except (FileNotFoundError, KeyError):
        sys.path.insert(0, HERE)
        import erd_spec_v22
        rules, rrules = erd_spec_v22.TUPLE_RULES, erd_spec_v22.RESOLVE_RULES
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
    json.dump(R, open(os.path.join(HERE, "erd-v2.2-tuples.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    print("\n→ erd-v2.2-tuples.json")


if __name__ == "__main__":
    main()
