# -*- coding: utf-8 -*-
"""관계 31종(ERD v3.1 — R29 없음 · R32 rule_applies_to) — 엣지마다 원장 locator provenance.
v3.1: R12 session_count(V3.1-5) · R15 경과 = 엣지 속성 course(원칙 C) · 문구 유래 R15 는 문구 사전 항목(auto · approved)에서 source_phrases 부록과 함께 ·
R16/R17/R18 의 person_condition 끝 = 조건 단위(source_phrases = 문장 locator) · R19/R20 끝에 문구 없음 · R31 끝은 site 만 · R32 basis=ledger(필수 고지 → 계열).

시술 축 끝(R3·R9·R12·R15·R16·R17·R18)은 §3 엣지 끝 규칙: 참조가 튜플로 풀리면 anchor → 최종 튜플 id(finalize 에서),
M 코드만 → modality · 실존 하위분류 id → modality_subcategory · 제품 전용 자리 → product · 미해결은 엣지 없이 ⑨.
"""
import json
import re
from collections import OrderedDict, defaultdict

from .decompose import MARKET_SLOT, split_code
from .provenance import P, loc, records, leaves, rec_str
from .units31 import PARSED_REFS
from .util import mkid, norm, dedupe

MCODE = re.compile(r"^M\d+$")


class Ends:
    """참조 자리 행 → 끝."""

    def __init__(self, S):
        self.S = S
        D = S.ctx["proc"]
        self.rows = {}
        for slot, rr in list(D["ref_rows"].items()) + [(MARKET_SLOT, D["mk_rows"])]:
            for r in rr:
                self.rows[(slot, tuple(r["_in"]))] = r
        self.PT = D["PT"]
        self.ids = S.ctx["ids"]

    @staticmethod
    def _v3(r, extra=None):
        """v3 엣지 속성(R9/R12/R17/R18 · V3-3 · V3-4): qualifier_text · session_index · alternatives · member_mode — 값이 있을 때만."""
        out = {}
        if r.get("qualifier_text"):
            out["qualifier_text"] = list(r["qualifier_text"])
        if r.get("session_index") is not None:
            out["session_index"] = r["session_index"]
        if r.get("session_count") is not None:
            out["session_count"] = r["session_count"]
        if r.get("alternatives"):
            out["alternatives"] = [a["what_id"] or a["text"] for a in r["alternatives"]]
            out["alternatives_text"] = [a["text"] for a in r["alternatives"]]
        if r.get("member_mode"):
            out["member_mode"] = r["member_mode"]
        out.update(extra or {})
        return out

    def of(self, slot, label, hint, product_slot=False):
        """→ [(type, id|anchor, attrs)] 또는 None(미해결)."""
        r = self.rows[(slot, (label, hint))]
        AM = self.S.ctx.get("AM_live")
        if AM is not None and not product_slot and r.get("ref_id") in AM.established and r["result"] not in ("tuple", "combo_ref", "multi_tuple", "node"):
            # V3-9 — 결정이 세운 미해결 참조의 튜플(바탕 anchor → resolve 가 단일·여럿을 푼다)
            sp = AM.spec.get(r["ref_id"]) or {}
            mode = sp.get("member_mode")
            return [("procedure", {"anchor": r["ref_id"]}, self._v3(r, {"target_depth": "procedure", "via_catalog_item": None, "decision_id": AM.established[r["ref_id"]], **({"member_mode": mode} if mode else {})}))]
        if r["result"] in ("combo_ref", "multi_tuple") and AM is not None and r.get("ref_id") in AM.spec and r["ref_id"] not in AM.multi and not AM.spec[r["ref_id"]].get("virtual"):
            # 결정이 조합·부위 여럿 참조를 한 튜플로 다시 정했다 — 바탕 anchor 하나
            return [("procedure", {"anchor": r["ref_id"]}, self._v3(dict(r, member_mode=None), {"target_depth": "procedure", "via_catalog_item": None}))]
        if r["result"] == "tuple":
            t = self.PT.tuples[r["procedure_id"]]
            if product_slot:
                return [("product", t["what_id"], self._v3(r, {"target_depth": "product"}))]
            via = r["anchor"] if r.get("via_item_id") else mkid("CAT", f"{t['family']}|{r['via_item']}") if r.get("via_item") else None
            return [("procedure", {"anchor": r["anchor"]}, self._v3(r, {"target_depth": "procedure", "via_catalog_item": via}))]
        if r["result"] == "combo_ref":
            pk = self.S.ctx["combo_pkg"].get((slot, tuple(r["_in"])))
            return [("procedure", {"anchor": a}, self._v3(r, {"target_depth": "procedure", "via_catalog_item": None, "combo_ref": pk})) for a in r["member_anchors"]]
        if r["result"] == "multi_tuple":
            # V3-4 「무엇을 하나 × 부위 여럿」 — 부위별 튜플마다 엣지(member_mode and)
            return [("procedure", {"anchor": a}, self._v3(r, {"target_depth": "procedure", "via_catalog_item": None, "site_index": i})) for i, a in enumerate(r["member_anchors"])]
        if r["result"] == "node":
            return [("modality" if r["end_kind"] == "modality" else "modality_subcategory", r["end_id"], {"target_depth": r["end_kind"]})]
        return None

    def code(self, v):
        """원장 코드 자리(M 코드 · 하위분류 id · 분류 항목 id) → 끝."""
        v = str(v)
        if v in self.ids.mod:
            return [("modality", self.ids.mod[v]["id"], {"target_depth": "modality"})]
        if v in self.ids.sub:
            return [("modality_subcategory", self.ids.sub[v]["id"], {"target_depth": "subcategory"})]
        it = self.S.ctx["item_by_id"].get(v)
        if it:
            return [("procedure", {"anchor": it["cat"]["catalog_item_id"]}, {"target_depth": "procedure", "via_catalog_item": it["cat"]["catalog_item_id"]})]
        return None


def cell(file, path, r, v):
    return {"value": v, "prov": [P(file, path, r)]}


def leaf(L, file, obj, key, path, r):
    if key in obj:
        return cell(file, path, r, obj[key])
    return None


def put(attrs, k, c):
    if c is not None:
        attrs[k] = c


def edge_to(S, rel, ftype, fid, end, prov, attrs, derived=None):
    typ, ident, eattrs = end
    a = dict(attrs)
    for k, v in eattrs.items():
        if v is not None:
            a[k] = {"value": v, "derived_from": [loc(p) for p in prov]}
    if typ == "procedure":
        return S.edge(rel, ftype, fid, "procedure", None, prov, a, derived, to_anchor=ident["anchor"])
    return S.edge(rel, ftype, fid, typ, ident, prov, a, derived)


def edge_from(S, rel, start, ttype, tid, prov, attrs):
    typ, ident, eattrs = start
    a = dict(attrs)
    for k, v in eattrs.items():
        if v is not None:
            a["from_" + k] = {"value": v, "derived_from": [loc(p) for p in prov]}
    if typ == "procedure":
        return S.edge(rel, "procedure", None, ttype, tid, prov, a, from_anchor=ident["anchor"])
    return S.edge(rel, typ, ident, ttype, tid, prov, a)


def edge_pair(S, rel, a_end, b_end, prov, attrs):
    ta, ia, ea = a_end
    tb, ib, eb = b_end
    at = dict(attrs)
    for k, v in ea.items():
        if v is not None:
            at["from_" + k] = {"value": v, "derived_from": [loc(p) for p in prov]}
    for k, v in eb.items():
        if v is not None:
            at["to_" + k] = {"value": v, "derived_from": [loc(p) for p in prov]}
    extra = {}
    fid = ia
    tid = ib
    if ta == "procedure":
        extra["from_anchor"] = ia["anchor"]
        fid = None
    if tb == "procedure":
        extra["to_anchor"] = ib["anchor"]
        tid = None
    return S.edge(rel, ta, fid, tb, tid, prov, at, **extra)


# ---------------------------------------------------------------------------
def build_relations(S, AU):
    L, ids = S.ctx["L"], S.ctx["ids"]
    E = Ends(S)
    S.ctx["ends"] = E
    occ = S.ctx["occ"]
    mods = {m: ids.mod[m]["id"] for m in ids.mod}

    # R1 · R2 (+ ⓪ reclassification)
    for r, sc in records(L["taxonomy.json"], "modality[].subcategories[]"):
        fam = L["taxonomy.json"]["modality"][r[0]]["id"]
        S.edge("R1", "modality", mods[fam], "modality_subcategory", ids.sub[sc["id"]]["id"], [P("taxonomy.json", "modality[].subcategories[].id", r)])
    recl = S.ctx.get("reclass", {})
    for (fam, name), it in S.ctx["items"].items():
        sub = ids.sub[it["sub"]]["id"]
        attrs = {}
        if it["cat"]["catalog_item_id"] in recl:
            d = recl[it["cat"]["catalog_item_id"]]
            attrs["reclassified_modality_id"] = {"value": d["modality_id"], "derived_from": [d["id"]]}
            attrs["decision_id"] = {"value": d["id"], "derived_from": [d["id"]]}
        S.edge("R2", "modality_subcategory", sub, "catalog_item", it["cat"]["catalog_item_id"], [P("taxonomy.json", "modality[].subcategories[].items[].id", it["r"])], attrs)

    # R3 — 항목 이름 = 같은 계열 제품명(정규화 완전 일치)
    for c in S.ctx["proc"]["cat_recs"]:
        if c["result"] == "tuple" and c.get("what_kind") == "product" and c.get("whole_match") and str(c.get("what_basis", "")).startswith("product:") and "(타 계열)" not in str(c.get("what_basis", "")):
            it = S.ctx["items"][(c["family"], c["name"])]
            t = S.ctx["proc"]["PT"].tuples[c["procedure_id"]]
            S.edge("R3", "procedure", None, "product", t["what_id"], [P("taxonomy.json", "modality[].subcategories[].items[].name", it["r"])],
                   {"target_depth": {"value": "procedure", "derived_from": [it["name_loc"]]}, "via_catalog_item": {"value": c["catalog_item_id"], "derived_from": [it["name_loc"]]}}, from_anchor=c["catalog_item_id"])

    # R4 — modality → product
    pbn = S.ctx["prod_by_norm"]
    for k, v in L["products.json"].items():
        if not isinstance(v, dict):
            continue
        cats = v["category_id"] if isinstance(v["category_id"], list) else [v["category_id"]]
        for i, pr in enumerate(v.get("products", [])):
            pid = pbn.get(norm(pr["name"]))
            if not pid:
                continue
            if len(cats) == 1:
                S.edge("R4", "modality", mods[cats[0]], "product", pid, [P("products.json", f"{k}.category_id", ()), P("products.json", f"{k}.products[].name", (i,))],
                       {"section_key": {"value": k, "derived_from": [loc(P("products.json", f"{k}.category_id", ()))]}})
            else:
                # 집합 category_id — 개별 제품 계열은 taxonomy 소속으로 확정, 집합은 검증 제약(R4 규칙)
                fams = [L["taxonomy.json"]["modality"][r[0]]["id"] for r, x in records(L["taxonomy.json"], "modality[].products[]") if pbn.get(norm(x["name"])) == pid]
                for fam in dedupe(fams):
                    if fam in cats:
                        S.edge("R4", "modality", mods[fam], "product", pid, [P("products.json", f"{k}.category_id[]", (cats.index(fam),)), P("products.json", f"{k}.products[].name", (i,))],
                               {"section_key": {"value": k, "derived_from": [loc(P("products.json", f"{k}.category_id[]", (cats.index(fam),)))]}, "set_constraint": {"value": cats, "derived_from": [loc(P("products.json", f"{k}.category_id[]", (j,))) for j in range(len(cats))]}})
                    else:
                        S.note(f"products.json:{k}.products[].name@{i}", f"taxonomy 소속 계열 {fam} 이 category_id 집합 {cats} 밖 — R4 를 만들지 않음")
    for r, pr in records(L["taxonomy.json"], "modality[].products[]"):
        pid = pbn.get(norm(pr["name"]))
        if pid:
            fam = L["taxonomy.json"]["modality"][r[0]]["id"]
            S.edge("R4", "modality", mods[fam], "product", pid, [P("taxonomy.json", "modality[].products[].id", r)])
    for r, it in records(L["step1-products.json"], "items[]"):
        code = it["family"]["code"]
        if MCODE.match(str(code)) and code in mods:
            S.edge("R4", "modality", mods[code], "product", S.ctx["step1_product"][r[0]], [P("step1-products.json", "items[].family.code", r)], {"basis": {"value": "survey_family_code", "derived_from": [loc(P("step1-products.json", "items[].family.code", r))]}})
    # v3.1(V3.1-1) product_reclassify — 옛 계열 → 새 계열로 옮긴다(section_key 보존 · 원장 category_id 와 다른 것은 결정 출처 derived_from)
    for e in S.R.get("R4", []):
        rc = S.ctx.get("prd_reclass", {}).get(e["to"]["id"])
        if rc and e["from"]["id"] == mods.get(rc["from_code"]):
            e["from"] = dict(e["from"], id=mods[rc["to_code"]])
            e["attrs"]["reclassified_from_modality"] = {"value": rc["from_code"], "derived_from": [rc["decision_id"]]}
            e["attrs"]["decision_id"] = {"value": rc["decision_id"], "derived_from": [rc["decision_id"]]}
            if rc["decision_id"] not in e["derived_from"]:
                e["derived_from"].append(rc["decision_id"])

    # R5 — modality → technique
    for r, pr in records(L["procedure-profiles.json"], "profiles[]"):
        for j, m in enumerate(pr.get("mechanism") or []):
            if pr["id"] in mods:
                pv = P("procedure-profiles.json", "profiles[].mechanism[]", r + (j,))
                S.edge("R5", "modality", mods[pr["id"]], "technique", mkid("TEC", m), [pv], {"basis": {"value": "ledger", "derived_from": [loc(pv)]}})
    # V3-8 — 하위분류 단위 기본 기법(canonical_mapping R5:<하위분류 id> · approved · 적용된 것만)
    for x in S.ctx.get("r5_sub_decisions", []):
        S.edge("R5", "modality_subcategory", ids.sub[x["subcategory"]]["id"], "technique", mkid("TEC", x["technique"]), [],
               {"basis": {"value": "canonical_mapping", "derived_from": [x["id"]]}, "decision_id": {"value": x["id"], "derived_from": [x["id"]]}}, derived_from=[x["id"]])

    # R6 · R7 · R11 · R8 (taxonomy problem 트리)
    site_by_norm = {norm(e["canonical"]): ids.site[norm(e["canonical"])]["id"] for e in S.ctx["dicts"]["site"]["entries"]}
    for e in S.ctx["dicts"]["site"]["entries"]:
        for s in e.get("synonyms", []):
            site_by_norm.setdefault(norm(s["value"]), ids.site[norm(e["canonical"])]["id"])
    for (pid, nl), (srec, sr, sc, _) in S.ctx["psubs"].items():
        S.edge("R6", "problem", mkid("PRB", pid), "problem_subcategory", srec["id"], [P("taxonomy.json", "problem[].subcategories[].id", sr)])
        if nl in site_by_norm:
            S.edge("R11", "problem_subcategory", srec["id"], "site", site_by_norm[nl], [P("taxonomy.json", "problem[].subcategories[].label", sr)])
    for (pid, nn), hs in S.ctx["tx_complaints"].items():
        for crec, ir, it, srec in hs:
            S.edge("R7", "problem_subcategory", srec["id"], "complaint", crec["id"], [P("taxonomy.json", "problem[].subcategories[].items[].id", ir)])
            for j, mr in enumerate(it.get("modality_ref") or []):
                pv = P("taxonomy.json", "problem[].subcategories[].items[].modality_ref[]", ir + (j,))
                if mr in mods:
                    S.edge("R8", "complaint", crec["id"], "modality", mods[mr], [pv])
                else:
                    S.unresolved_ref("R8", "taxonomy.json:problem[].subcategories[].items[].modality_ref[]", mr, None, [pv], "modality_ref 가 M 코드가 아니다", [])
    # problem-packages: R7(cc_group) · R10 · R9 · R14
    psl = {}
    for e in S.ctx["dicts"]["problem_subcategory_label"]["entries"]:
        for v in [e["canonical"]] + [s["value"] for s in e.get("synonyms", [])]:
            psl.setdefault(norm(v), e["canonical"])
    for r, p in records(L["problem-packages.json"], "problems[]"):
        for ci, c in enumerate(p["complaints"]):
            cr = r + (ci,)
            crec = S.ctx["pp_complaints"][cr]
            g = c.get("cc_group")
            gp = P("problem-packages.json", "problems[].complaints[].cc_group", cr)
            if g:
                lab = psl.get(norm(g))
                hit = S.ctx["psubs"].get((p["problem_id"], norm(lab))) if lab else None
                if hit:
                    S.edge("R7", "problem_subcategory", hit[0]["id"], "complaint", crec["id"], [gp, P("problem-packages.json", "problems[].problem_id", r)], {"cc_group_raw": cell("problem-packages.json", gp["path"], cr, g)})
                else:
                    S.unresolved_ref("R7", "problem-packages.json:problems[].complaints[].cc_group", g, p["problem_id"], [gp], "(problem_id, cc_group) 이 고민 하위분류 라벨 사전에 없다", [])
                if norm(g) in site_by_norm:
                    S.edge("R10", "complaint", crec["id"], "site", site_by_norm[norm(g)], [gp], {"label_raw": cell("problem-packages.json", gp["path"], cr, g)})
            for bi, b in enumerate(c.get("combos") or []):
                br = cr + (bi,)
                pk = S.ctx["pkgs"][("problem-packages.json", br)]
                a = {}
                put(a, "reason", leaf(L, "problem-packages.json", b, "reason", "problems[].complaints[].combos[].reason", br))
                put(a, "evidence", leaf(L, "problem-packages.json", b, "evidence", "problems[].complaints[].combos[].evidence", br))
                S.edge("R14", "complaint", crec["id"], "package", pk["id"], [P("problem-packages.json", "problems[].complaints[].combos[].name", br)], a)

    # R9 — complaint → proc_axis (시술 종류 이름 · 제품 전용 자리)
    slot = "problem-packages.procedures[].name (시술 종류 29)"
    pslot = "problem-packages.procedures[].products[] (제품 34)"
    prod_occ = defaultdict(list)
    for lab, hint, pv, ctx in occ[pslot]:
        prod_occ[ctx["r"]].append((lab, hint, pv))
    for lab, hint, pv, ctx in occ[slot]:
        r = ctx["r"]
        pr = L["problem-packages.json"]["problems"][r[0]]["complaints"][r[1]]["procedures"][r[2]]
        crec = S.ctx["pp_complaints"][r[:2]]
        a = {"target_label": cell(pv["file"], pv["path"], r, lab)}
        put(a, "modality_code", leaf(L, "problem-packages.json", pr, "category", "problems[].complaints[].procedures[].category", r))
        put(a, "role", leaf(L, "problem-packages.json", pr, "role", "problems[].complaints[].procedures[].role", r))
        plist, pprov = [], []
        for plab, phint, ppv in prod_occ.get(r, []):
            pe = E.of(pslot, plab, phint, product_slot=True)
            if pe:
                plist.append(pe[0][1])
                pprov.append(ppv)
                edge_to(S, "R9", "complaint", crec["id"], pe[0], [ppv], {"target_label": cell(ppv["file"], ppv["path"], tuple(int(x) for x in ppv["rec"].split("/")), plab), "parent_label": cell(pv["file"], pv["path"], r, lab)})
        if pr.get("products"):
            a["products"] = {"value": plist, "prov": pprov} if pprov else {"value": [], "derived_from": [loc(P("problem-packages.json", "problems[].complaints[].procedures[].products[]", r + (0,)))]}
        else:
            a["products"] = {"value": None, "prov": [P("problem-packages.json", "problems[].complaints[].procedures[].products", r)]}
        ends = E.of(slot, lab, hint)
        for end in ends or []:
            edge_to(S, "R9", "complaint", crec["id"], end, [pv], a)

    # R12 — package → proc_axis
    def member(pkg, end_list, pv, a):
        for end in end_list or []:
            edge_to(S, "R12", "package", pkg["id"], end, [pv], a)

    for r, x in records(L["combo-recipes.json"], "recipes[]"):
        for j, c in enumerate(x.get("procedures") or []):
            pv = P("combo-recipes.json", "recipes[].procedures[]", r + (j,))
            ends = E.code(c)
            if ends is None:
                S.unresolved_ref("R12", "combo-recipes.json:recipes[].procedures[]", c, None, [pv], "M 코드 아님", [])
            member(S.ctx["pkgs"][("combo-recipes.json", r)], ends, pv, {"target_label": cell(pv["file"], pv["path"], r + (j,), c), "order": {"value": j, "derived_from": [loc(pv)]}})
    for r, x in records(L["problem-combos.json"], "combos[].packages[]"):
        for j, c in enumerate(x.get("procedures") or []):
            pv = P("problem-combos.json", "combos[].packages[].procedures[]", r + (j,))
            ends = E.code(c)
            if ends is None:
                S.unresolved_ref("R12", "problem-combos.json:combos[].packages[].procedures[]", c, None, [pv], "M 코드 아님", [])
            member(S.ctx["pkgs"][("problem-combos.json", r)], ends, pv, {"target_label": cell(pv["file"], pv["path"], r + (j,), c)})
    for lab, hint, pv, ctx in occ["problem-packages.combos[].combo[] (멤버 29)"]:
        member(S.ctx["pkgs"][("problem-packages.json", ctx["r"])], E.of("problem-packages.combos[].combo[] (멤버 29)", lab, hint), pv,
               {"target_label": cell(pv["file"], pv["path"], ctx["r"] + (ctx["j"],), lab), "order": {"value": ctx["j"], "derived_from": [loc(pv)]}})
    for lab, hint, pv, ctx in occ["treatment-optimization.optimal_combo[] (57)"]:
        member(S.ctx["pkgs"][("treatment-optimization.json/by_concern", ctx["r"])], E.of("treatment-optimization.optimal_combo[] (57)", lab, hint), pv,
               {"target_label": cell(pv["file"], pv["path"], ctx["r"] + (ctx["j"],), lab), "order": {"value": ctx["j"], "derived_from": [loc(pv)]}})
    for lab, hint, pv, ctx in occ["treatment-optimization.annual_plans.schedule[].procedures[] (29)"]:
        r = ctx["r"]
        sch = L["treatment-optimization.json"]["annual_plans"][r[0]]["schedule"][r[1]]
        a = {"target_label": cell(pv["file"], pv["path"], r + (ctx["j"],), lab)}
        put(a, "month", leaf(L, "treatment-optimization.json", sch, "month", "annual_plans[].schedule[].month", r))
        member(S.ctx["pkgs"][("treatment-optimization.json/annual", r[:1])], E.of("treatment-optimization.annual_plans.schedule[].procedures[] (29)", lab, hint), pv, a)
    for lab, hint, pv, ctx in occ["treatment-sequence.common_combos[].sequence[] (22 distinct)"]:
        member(S.ctx["pkgs"][("treatment-sequence.json", ctx["r"])], E.of("treatment-sequence.common_combos[].sequence[] (22 distinct)", lab, hint), pv,
               {"target_label": cell(pv["file"], pv["path"], ctx["r"] + (ctx["j"],), lab), "order": {"value": ctx["j"], "derived_from": [loc(pv)]}})
    for lab, hint, pv, ctx in occ["procedure-comparison.procedures[].name (39)"]:
        r = ctx["r"]
        pr = L["procedure-comparison.json"]["comparisons"][r[0]]["procedures"][r[1]]
        a = {"target_label": cell(pv["file"], pv["path"], r, lab)}
        for k, an in (("category", "modality_code"), ("mechanism_simple", "mechanism_simple"), ("pain", "pain"), ("downtime", "downtime"), ("onset", "onset"), ("duration", "duration"),
                      ("cost_range", "cost_range"), ("best_for", "best_for"), ("limitations", "limitations"), ("pih_risk", "pih_risk"), ("asian_skin_note", "asian_skin_note")):
            put(a, an, leaf(L, "procedure-comparison.json", pr, k, f"comparisons[].procedures[].{k}", r))
        member(S.ctx["pkgs"][("procedure-comparison.json", r[:1])], E.of("procedure-comparison.procedures[].name (39)", lab, hint), pv, a)
    # combo_ref 패키지 → 멤버
    for (slot_, key), pkid in S.ctx["combo_pkg"].items():
        r = E.rows[(slot_, key)]
        ov = [o for o in occ[slot_] if (o[0], o[1]) == key]
        for a_ in r["member_anchors"]:
            S.edge("R12", "package", pkid, "procedure", None, [o[2] for o in ov], {"target_depth": {"value": "procedure", "derived_from": [loc(o[2]) for o in ov]},
                                                                                   "member_mode": {"value": r.get("member_mode") or "and", "derived_from": [loc(o[2]) for o in ov]}}, to_anchor=a_)

    # R13 — package → problem
    pidx = {}
    for e in S.ctx["dicts"]["problem"]["entries"]:
        pidx[norm(e["canonical"])] = e
        for s in e.get("synonyms", []):
            pidx[norm(s["value"])] = e
    for r, c in records(L["problem-combos.json"], "combos[]"):
        for pi, _ in enumerate(c["packages"]):
            if c["problem_id"] in S.ctx["problems"]:
                S.edge("R13", "package", S.ctx["pkgs"][("problem-combos.json", r + (pi,))]["id"], "problem", mkid("PRB", c["problem_id"]), [P("problem-combos.json", "combos[].problem_id", r)])
    sev = S.ctx["dicts"]["concern_severity"]
    for r, c in records(L["treatment-optimization.json"], "by_concern[]"):
        cp = P("treatment-optimization.json", "by_concern[].concern", r)
        e = pidx.get(norm(c["concern"]))
        if not e:
            S.unresolved_ref("R13", "treatment-optimization.json:by_concern[].concern", c["concern"], None, [cp], "고민 사전 일치 없음(질문 12)", [])
        for si, sv in enumerate(c["severity_levels"]):
            pk = S.ctx["pkgs"][("treatment-optimization.json/by_concern", r + (si,))]
            if not e:
                continue
            lp = P("treatment-optimization.json", "by_concern[].severity_levels[].level", r + (si,))
            m = re.match(r"^(.*?)\s*\((.*)\)\s*$", sv["level"])
            a = {"problem_label": cell(cp["file"], cp["path"], r, c["concern"]), "severity": {"value": (m.group(1) if m else sv["level"]), "derived_from": [loc(lp)]}}
            if m:
                a["severity_detail"] = {"value": m.group(2), "derived_from": [loc(lp)]}
            S.edge("R13", "package", pk["id"], "problem", mkid("PRB", e["code"]), [cp, lp], a)
    for r, c in records(L["procedure-comparison.json"], "comparisons[]"):
        ip = P("procedure-comparison.json", "comparisons[].id", r)
        e = pidx.get(norm(c["id"])) or pidx.get(norm(c["title"]))
        if e:
            S.edge("R13", "package", S.ctx["pkgs"][("procedure-comparison.json", r)]["id"], "problem", mkid("PRB", e["code"]), [ip], {"problem_label": cell(ip["file"], ip["path"], r, c["id"])})
        else:
            S.unresolved_ref("R13", "procedure-comparison.json:comparisons[].id", c["id"], None, [ip], "고민 사전 일치 없음(질문 12)", [])

    if S.ctx.get("is32"):
        # v3.2 — R15(이름 · 문구 · 타임라인 · 응급 징후 · 상속 · layer) · R33 · R34 · R35 · R20(adverse_effects) · R4(장비 제품)
        from .relations32 import build_v32
        build_v32(S, AU, E)
    else:
        # R15 — complications(계열 → 단위 · 경과 = 그 이름에서 그 단위의 사건 멤버에 붙은 경과)
        for ci, cat in enumerate(L["complications.json"]["categories"]):
            start = E.code(cat["id"])
            for i, cm in enumerate(cat["complications"]):
                r = (ci, i)
                locator = f"complications.json:categories[].complications[].name@{cat['id']}/{i}"
                a = {}
                for k in ("severity", "incidence", "onset", "mechanism", "management", "prevention", "duration"):
                    put(a, k, leaf(L, "complications.json", cm, k, f"categories[].complications[].{k}", r))
                if "risk_factors" in cm:
                    rf = cm["risk_factors"] or []
                    a["risk_factors"] = {"value": rf or None, "prov": [P("complications.json", "categories[].complications[].risk_factors[]", r + (j,)) for j in range(len(rf))] or [P("complications.json", "categories[].complications[].risk_factors", r)]}
                if cm.get("evidence"):
                    a["evidence_ref"] = {"value": [mkid("CIT", f"url:{u.strip()}") for u in cm["evidence"].split(";") if u.strip()], "derived_from": [loc(P("complications.json", "categories[].complications[].evidence", r))]}
                prov = [P("complications.json", "categories[].id", (ci,)), P("complications.json", "categories[].complications[].name", r)]
                for uid in AU.name_units.get(locator, []):
                    if start:
                        aa = dict(a)
                        co = AU.name_courses.get((locator, uid)) or []
                        aa["course"] = {"value": co or None, "derived_from": [loc(prov[1])]}
                        aa["source_phrases"] = {"value": [], "derived_from": [loc(prov[1])]}
                        edge_from(S, "R15", start[0], "adverse_effect", uid, prov, aa)
    # R15 — pih-risk(가장 구체 수준 → PIH 단위)
    pih_units = AU.find_units("PIH")
    for r, p in records(L["pih-risk.json"], "procedures[]"):
        rp = P("pih-risk.json", "procedures[].procedure_ref", r)
        start = E.code(p["procedure_ref"])
        if start is None:
            S.unresolved_ref("R15", "pih-risk.json:procedures[].procedure_ref", p["procedure_ref"], None, [rp], "id 깊이 판정 실패", [])
            continue
        if not pih_units:
            S.unresolved_ref("R15", "pih-risk.json:procedures[] → adverse_effect PIH", "PIH", None, [rp], "PIH 단위(색소침착)가 없다 — complications 이름·auto 문구 어디에도 (색소침착, none, none) 이 서지 않았다(단위는 세 칸 전부 사전 값일 때만)", [])
            continue
        a = {}
        for k, an in (("name", "source_label"), ("category", "modality_code"), ("subcategory", "subcategory_label"), ("pih_risk", "pih_risk"), ("pih_rate", "pih_rate"), ("fitzpatrick_note", "fitzpatrick_note"), ("prevention", "prevention")):
            put(a, an, leaf(L, "pih-risk.json", p, k, f"procedures[].{k}", r))
        if "risk_factors" in p:
            rf = p["risk_factors"] or []
            a["risk_factors"] = {"value": rf or None, "prov": [P("pih-risk.json", "procedures[].risk_factors[]", r + (j,)) for j in range(len(rf))] or [P("pih-risk.json", "procedures[].risk_factors", r)]}
        sub = ids.sub_by_label.get((p.get("category"), norm(p.get("subcategory"))))
        if sub:
            a["subcategory_id"] = {"value": sub[0]["id"], "derived_from": [loc(P("pih-risk.json", "procedures[].subcategory", r))]}
        for uid in pih_units:
            edge_from(S, "R15", start[0], "adverse_effect", uid, [rp, P("pih-risk.json", "procedures[].name", r)], a)
    if not S.ctx.get("is32"):
        # R15 — 문구 사전 항목(auto · approved) → 단위 · 문구 자리(계열 · 항목 · 제품)에서 · (출발, 단위) 마다 엣지 하나(source_phrases 부록)
        agg = OrderedDict()
        for pid, e in AU.phrases.items():
            if e["status"] not in ("auto", "approved") or not e["units"]:
                continue
            for c in e["contexts"]:
                row = {"file": c["file"], "rec": tuple_rec(c["rec"]), "modality": c.get("modality"), "item": c.get("item"), "product": c.get("product")}
                st = expr_start(S, E, row)
                if not st:
                    continue
                pv = P(c["file"], c["path"], c["rec"])
                for s0 in st:
                    skey = (s0[0], json.dumps(s0[1], sort_keys=True, ensure_ascii=False))
                    for uid in e["units"]:
                        g = agg.setdefault((skey, uid), {"start": s0, "uid": uid, "prov": [], "phrases": [], "courses": [], "kinds": [], "disclosure": False, "ctx": OrderedDict(), "refs": {k: [] for _, k in PARSED_REFS}})
                        for q in [pv] + start_prov(dict(row, path=c["path"])):
                            if q not in g["prov"]:
                                g["prov"].append(q)
                        if pid not in g["phrases"]:
                            g["phrases"].append(pid)
                        g["courses"] = dedupe(g["courses"] + AU.phrase_courses(pid, uid))
                        if c["kind"] not in g["kinds"]:
                            g["kinds"].append(c["kind"])
                        if c["kind"] == "disclosure":
                            g["disclosure"] = True
                        for k_, v_ in (c.get("context") or {}).items():
                            if k_ in ("frequency_class", "reaction_level", "period", "phase_label"):
                                g["ctx"].setdefault(k_, [])
                                if v_ not in g["ctx"][k_]:
                                    g["ctx"][k_].append(v_)
                        for pk, ak in PARSED_REFS:
                            if e["parsed"].get(pk) and pid not in g["refs"][ak]:
                                g["refs"][ak].append(pid)
        for (skey, uid), g in agg.items():
            df = [loc(q) for q in g["prov"]]
            a = {"source_phrases": {"value": g["phrases"], "derived_from": df}, "course": {"value": g["courses"] or None, "derived_from": df},
                 "created_by_phrase": {"value": bool(AU.units.get(uid, {}).get("created_by_phrase")), "derived_from": df}, "disclosure": {"value": g["disclosure"], "derived_from": df},
                 "phrase_kinds": {"value": g["kinds"], "derived_from": df}}
            for ak, v in g["refs"].items():
                a[ak] = {"value": v or None, "derived_from": df}
            for k_, v_ in g["ctx"].items():
                a[k_] = {"value": v_[0] if len(v_) == 1 else v_, "derived_from": df}
            edge_from(S, "R15", g["start"], "adverse_effect", uid, g["prov"], a)
    lit = L["literature-evidence.json"]
    for code, cat in lit["categories"].items():
        if code not in mods:
            continue
        for sec in ("moa", "effects"):
            for i, x in enumerate(cat.get(sec) or []):
                eid = mkid("EVS", f"{code}|{'moa' if sec == 'moa' else 'effect'}|{x['statement']}")
                S.edge("R20", "modality", mods[code], "evidence_statement", eid, [P("literature-evidence.json", f"categories.{{code}}.{sec}[].statement", (code, i))])

    # R32 — 필수 고지 clinical_rule(disclosure) → 계열(basis=ledger · V3.1-7)
    for rid, code, pv, r in S.ctx.get("disclosure_edges", []):
        st = E.code(code)
        if not st:
            continue
        cp = P("consent-checklist.json", "categories[].id", r)
        a = {"scope": {"value": "modality", "derived_from": [loc(pv)]}, "severity": {"value": "info", "derived_from": [loc(pv)]}, "source_locator": {"value": loc(pv), "derived_from": [loc(pv)]},
             "basis": {"value": "ledger", "derived_from": [loc(pv), loc(cp)]}, "target_depth": {"value": "modality", "derived_from": [loc(cp)]}}
        edge_to(S, "R32", "clinical_rule", rid, st[0], [pv, cp], a)

    # R16 — proc_axis → person_condition
    CU = S.ctx["CU"]

    def r16(start_list, cond_text, pv, level, level_prov=None, from_prov=None):
        if not start_list or not isinstance(cond_text, str) or not cond_text.strip():
            return
        a = {"level": ({"value": level, "prov": [level_prov]} if level_prov else {"value": level, "derived_from": [loc(pv)]}), "source_phrases": {"value": [loc(pv)], "derived_from": [loc(pv)]}}
        for st in start_list:
            for cid in CU.of(pv):   # v3.1(V3.1-4) — 끝은 그 문장이 만든 조건 단위(사전 단위 · raw_name)
                edge_from(S, "R16", st, "person_condition", cid, [pv] + ([from_prov] if from_prov else []), a)

    for r, c in records(L["consent-checklist.json"], "categories[]"):
        for j, x in enumerate(c.get("contraindications") or []):
            r16(E.code(c["id"]), x, P("consent-checklist.json", "categories[].contraindications[]", r + (j,)), "consent", from_prov=P("consent-checklist.json", "categories[].id", r))
    for code, v in L["extracted.json"].items():
        for lv in ("absolute", "relative"):
            for j, x in enumerate(((v.get("contraindications") or {}).get(lv)) or []):
                r16(E.code(code), x, P("extracted.json", f"{{code}}.contraindications.{lv}[]", (code, j)), lv)
    for r, m in records(L["taxonomy.json"], "modality[]"):
        for lv in ("absolute", "relative"):
            for j, x in enumerate((((m.get("extracted") or {}).get("contraindications") or {}).get(lv)) or []):
                r16(E.code(m["id"]), x, P("taxonomy.json", f"modality[].extracted.contraindications.{lv}[]", r + (j,)), lv)
    for (fam, name), it in S.ctx["items"].items():
        for j, x in enumerate((((it["item"].get("extracted") or {}).get("safety") or {}).get("contraindications")) or []):
            r16([("procedure", {"anchor": it["cat"]["catalog_item_id"]}, {"target_depth": "procedure", "via_catalog_item": it["cat"]["catalog_item_id"]})], x,
                P("taxonomy.json", "modality[].subcategories[].items[].extracted.safety.contraindications[]", it["r"] + (j,)), "unspecified")
    for r, c in records(L["pre-procedure-checklist.json"], "category_specific[]"):
        for j, ck in enumerate(c.get("checks") or []):
            r16(E.code(c["id"]), ck.get("label"), P("pre-procedure-checklist.json", "category_specific[].checks[].label", r + (j,)), ck.get("type"),
                P("pre-procedure-checklist.json", "category_specific[].checks[].type", r + (j,)) if "type" in ck else None, from_prov=P("pre-procedure-checklist.json", "category_specific[].id", r))

    # R17 — age_group → proc_axis | problem
    for r, g in records(L["treatment-optimization.json"], "by_age_group[]"):
        ap = P("treatment-optimization.json", "by_age_group[].age", r)
        for j, x in enumerate(g.get("primary_concerns") or []):
            pv = P("treatment-optimization.json", "by_age_group[].primary_concerns[]", r + (j,))
            e = pidx.get(norm(x))
            if e:
                for cid in CU.of(ap):
                    S.edge("R17", "person_condition", cid, "problem", mkid("PRB", e["code"]), [pv, ap], {"relation_kind": {"value": "primary_concern", "derived_from": [loc(pv)]}, "target_label": cell(pv["file"], pv["path"], r + (j,), x),
                                                                                                    "source_phrases": {"value": [loc(ap)], "derived_from": [loc(ap)]}})
            else:
                S.unresolved_ref("R17", "treatment-optimization.json:by_age_group[].primary_concerns[]", x, g["age"], [pv], "고민 사전 일치 없음(질문 12)", [])
    for lab, hint, pv, ctx in occ["treatment-optimization.by_age_group recommended_base/avoid/upgrade (22)"]:
        r = ctx["r"]
        ap = P("treatment-optimization.json", "by_age_group[].age", r[:1])
        for cid in CU.of(ap):
            for end in E.of("treatment-optimization.by_age_group recommended_base/avoid/upgrade (22)", lab, hint) or []:
                edge_to(S, "R17", "person_condition", cid, end, [pv, ap], {"relation_kind": {"value": ctx["relation_kind"], "derived_from": [loc(pv)]}, "target_label": cell(pv["file"], pv["path"], r + (ctx["j"],), lab),
                                                                           "source_phrases": {"value": [loc(ap)], "derived_from": [loc(ap)]}})

    # R18 — interaction
    syn = {"함께": "synergy_together", "다음에": "synergy_after", "대신": "synergy_instead"}
    sslot = "synergy.links[].from/to (노드 52)"
    for r, l in records(L["synergy.json"], "links[]"):
        fc, fl = split_code(l["from"])
        tc, tl = split_code(l["to"])
        fe, te = E.of(sslot, fl, fc), E.of(sslot, tl, tc)
        if not fe or not te:
            continue
        prov = [P("synergy.json", "links[].from", r), P("synergy.json", "links[].to", r)]
        a = {"kind": {"value": syn.get(l.get("type"), l.get("type")), "derived_from": [loc(P("synergy.json", "links[].type", r))]}, "type_raw": cell("synergy.json", "links[].type", r, l.get("type")), "from_label": cell("synergy.json", "links[].from", r, l["from"]), "to_label": cell("synergy.json", "links[].to", r, l["to"])}
        for k, an in (("from_category", "from_modality"), ("to_category", "to_modality"), ("reason", "reason"), ("timing", "timing"), ("target", "target")):
            put(a, an, leaf(L, "synergy.json", l, k, f"links[].{k}", r))
        for x in fe:
            for y in te:
                edge_pair(S, "R18", x, y, prov, a)
    for r, x in records(L["contraindications.json"], "rules[]"):
        fe, te = E.code(x["from"]), E.code(x["to"])
        prov = [P("contraindications.json", "rules[].from", r), P("contraindications.json", "rules[].to", r)]
        if not fe or not te:
            S.unresolved_ref("R18", "contraindications.json:rules[].from/to", f"{x['from']}→{x['to']}", None, prov, "M 코드 아님", [])
            continue
        a = {"kind": {"value": "pair_rule", "derived_from": [loc(p) for p in prov]}}
        for k, an in (("level", "level"), ("interval", "interval_text"), ("note", "note"), ("from_name", "from_label"), ("to_name", "to_label")):
            put(a, an, leaf(L, "contraindications.json", x, k, f"rules[].{k}", r))
        edge_pair(S, "R18", fe[0], te[0], prov, a)
    islot = "treatment-sequence.incompatible_same_day[].pair[] (14 distinct)"
    for r, x in records(L["treatment-sequence.json"], "incompatible_same_day[]"):
        pr = x.get("pair") or []
        if len(pr) != 2:
            continue
        fe, te = E.of(islot, pr[0], None), E.of(islot, pr[1], None)
        if not fe or not te:
            continue
        prov = [P("treatment-sequence.json", "incompatible_same_day[].pair[]", r + (0,)), P("treatment-sequence.json", "incompatible_same_day[].pair[]", r + (1,))]
        a = {"kind": {"value": "incompatible_same_day", "derived_from": [loc(p) for p in prov]}, "from_label": cell("treatment-sequence.json", "incompatible_same_day[].pair[]", r + (0,), pr[0]),
             "to_label": cell("treatment-sequence.json", "incompatible_same_day[].pair[]", r + (1,), pr[1])}
        put(a, "reason", leaf(L, "treatment-sequence.json", x, "reason", "incompatible_same_day[].reason", r))
        for p_ in fe:
            for q in te:
                edge_pair(S, "R18", p_, q, prov, a)
    mslot = "treatment-sequence.minimum_intervals from/to (14 distinct)"
    for r, x in records(L["treatment-sequence.json"], "minimum_intervals[]"):
        fe, te = E.of(mslot, x["from"], None), E.of(mslot, x["to"], None)
        if not fe or not te:
            continue
        prov = [P("treatment-sequence.json", "minimum_intervals[].from", r), P("treatment-sequence.json", "minimum_intervals[].to", r)]
        a = {"kind": {"value": "minimum_interval", "derived_from": [loc(p) for p in prov]}, "from_label": cell("treatment-sequence.json", "minimum_intervals[].from", r, x["from"]), "to_label": cell("treatment-sequence.json", "minimum_intervals[].to", r, x["to"])}
        for k, unit in (("min_days", "day"), ("min_months", "month")):
            if k in x:
                a["min_interval_value"] = cell("treatment-sequence.json", f"minimum_intervals[].{k}", r, x[k])
                a["min_interval_unit"] = {"value": unit, "derived_from": [loc(P("treatment-sequence.json", f"minimum_intervals[].{k}", r))]}
        put(a, "reason", leaf(L, "treatment-sequence.json", x, "reason", "minimum_intervals[].reason", r))
        if x.get("source"):
            a["source_ref"] = {"value": mkid("CIT", f"text:{norm(x['source'])}"), "derived_from": [loc(P("treatment-sequence.json", "minimum_intervals[].source", r))]}
        for p_ in fe:
            for q in te:
                edge_pair(S, "R18", p_, q, prov, a)
    # same_session_order — 끝 레코드의 속성(컬럼 표: modality.same_session_order)
    qslot = "treatment-sequence.sequence_order[].categories[] (19)"
    for lab, hint, pv, ctx in occ[qslot]:
        r = ctx["r"]
        so = L["treatment-sequence.json"]["sequence_order"][r[0]]
        val = {k: so.get(k) for k in ("order", "phase", "reason")}
        ends = E.of(qslot, lab, hint)
        for end in ends or []:
            typ, ident, _ = end
            df = [loc(pv)] + [loc(P("treatment-sequence.json", f"sequence_order[].{k}", r)) for k in ("order", "phase", "reason") if k in so]
            if typ in ("modality", "modality_subcategory"):
                rec = S.E[typ].get(ident)
                if rec is not None:
                    S.dattr(rec, "same_session_order", dict(val, category=ctx["raw"]), df, replace=False)
            else:
                S.ctx.setdefault("tuple_session_order", []).append((ident["anchor"], dict(val, category=ctx["raw"]), df))

    # R19 cites
    for eid, (rec, r, x, sec) in S.ctx["evs"].items():
        for k, c in enumerate(x.get("citations") or []):
            from .entities import cit_key
            S.edge("R19", "evidence_statement", eid, "citation", cit_key(c), [P("literature-evidence.json", f"categories.{{code}}.{sec}[].citations[].pmid", r + (k,))])
    # v3.1(V3.1-10): 문헌 adverse_effects 문구의 인용은 문구 사전 항목 citations[] 에(개체 아님 · R19 끝 아님)
    for rid, (rec, r, x) in S.ctx["rules_combo"].items():
        if x.get("evidence"):
            S.edge("R19", "clinical_rule", rid, "citation", mkid("CIT", f"text:{norm(x['evidence'])}"), [P("treatment-optimization.json", "combination_rules[].evidence", r)])
    for code, v in L["extracted.json"].items():
        if code in mods and v.get("source"):
            S.edge("R19", "modality", mods[code], "citation", mkid("CIT", f"text:{norm(v['source'])}"), [P("extracted.json", "{code}.source", (code,))], {"basis": {"value": "extracted_meta.source", "derived_from": [loc(P("extracted.json", "{code}.source", (code,)))]}})
    for p, r, v in leaves(L["step1-products.json"]):
        if p in ("items[].evidence[].urls[]", "items[].4_license.distribution_sources[].url") and isinstance(v, str) and v:
            S.edge("R19", "product", S.ctx["step1_product"][r[0]], "citation", mkid("CIT", f"url:{v}"), [P("step1-products.json", p, r)])

    # R21 · R22 — site → 구조 · 계열
    zid = {e.get("zone_id"): ids.site[norm(e["canonical"])]["id"] for e in S.ctx["dicts"]["site"]["entries"] if e.get("zone_id")}
    for r, z in records(L["anatomy-danger-zones.json"], "zones[]"):
        sid = zid.get(z["id"])
        if not sid:
            continue
        for kind in ("vessels", "nerves"):
            for j, x in enumerate(z.get(kind) or []):
                rr = r + (j,)
                a = {}
                for k in ("depth_mm", "diameter_mm", "course", "danger", "note", "significance"):
                    put(a, k, leaf(L, "anatomy-danger-zones.json", x, k, f"zones[].{kind}[].{k}", rr))
                if "depth_range_mm" in x:
                    a["depth_range_mm"] = {"value": x["depth_range_mm"], "prov": [P("anatomy-danger-zones.json", f"zones[].{kind}[].depth_range_mm[]", rr + (i,)) for i in range(len(x["depth_range_mm"]))] or [P("anatomy-danger-zones.json", f"zones[].{kind}[].depth_range_mm", rr)]}
                S.edge("R21", "site", sid, "anatomical_structure", mkid("ANA", x["name"]), [P("anatomy-danger-zones.json", f"zones[].{kind}[].name", rr)], a)
        for key, mcode, keys in (("botox_specific", "M1", [("target_muscle", "target_muscle"), ("risk", "risk_text"), ("safe_zone", "safe_zone"), ("diffusion_range_cm", "diffusion_range_cm"), ("key_warning", "key_warning"), ("dose_range", "dose_range")]),
                                 ("filler_specific", "M2", [("risk_level", "risk_level"), ("primary_risk", "primary_risk"), ("safe_technique", "safe_technique"), ("max_per_point_ml", "max_per_point_ml"), ("preferred_product", "preferred_product"), ("emergency_protocol", "emergency_protocol")])):
            obj = z.get(key)
            if not obj:
                continue
            a = {}
            for k, an in keys:
                put(a, an, leaf(L, "anatomy-danger-zones.json", obj, k, f"zones[].{key}.{k}", r))
            S.edge("R22", "site", sid, "modality", mods[mcode], [P("anatomy-danger-zones.json", f"zones[].{key}.{keys[0][0]}", r)] + [c["prov"][0] for c in a.values() if "prov" in c], a,
                   derived_from=[f"DEC-2026-11-04-13"])

    # R26 · R27 · R28 · R31 — finalize 뒤(튜플 확정 후)


def tuple_rec(rec):
    """문구 자리의 원장 rec(튜플) — 숫자 키는 int 로."""
    if isinstance(rec, tuple):
        return rec
    return tuple(int(x) if str(x).isdigit() else x for x in str(rec).split("/"))


def expr_start(S, E, row):
    """표현이 놓인 자리의 시술 축 끝(R15 from)."""
    f = row["file"]
    if f == "consent-checklist.json":
        return E.code(row["modality"])
    if f == "post-procedure-timeline.json":
        tl = S.ctx["L"]["post-procedure-timeline.json"]["timelines"][row["rec"][0]]
        return E.code(tl["category"])
    if f == "extracted.json" or f == "literature-evidence.json":
        return E.code(row["modality"])
    if f == "taxonomy.json":
        if row.get("item"):
            it = S.ctx["items"][tuple(row["item"])]
            return [("procedure", {"anchor": it["cat"]["catalog_item_id"]}, {"target_depth": "procedure", "via_catalog_item": it["cat"]["catalog_item_id"]})]
        if row.get("product"):
            pid = S.ctx["prod_by_norm"].get(norm(row["product"][1]))
            return [("product", pid, {"target_depth": "product"})] if pid else None
        return E.code(row["modality"])
    return None


def start_prov(row):
    f = row["file"]
    r = row["rec"]
    if f == "consent-checklist.json":
        return [P(f, "categories[].id", r[:1])]
    if f == "post-procedure-timeline.json":
        return [P(f, "timelines[].category", r[:1])]
    if f == "taxonomy.json" and row.get("item"):
        return [P(f, "modality[].subcategories[].items[].name", r[:3])]
    if f == "taxonomy.json" and row.get("product"):
        return [P(f, "modality[].products[].name", r[:2])]
    if f == "taxonomy.json":
        return [P(f, "modality[].id", r[:1])]
    return []


def finalize(S, AM, AU):
    """anchor 끝 → 최종 튜플 id. 제외·미해결 anchor 의 엣지는 버리고 기록."""
    ids = S.ctx["ids"]
    for rel, es in list(S.R.items()):
        out = []
        for e in es:
            fa, ta = e.pop("from_anchor", None), e.pop("to_anchor", None)
            fids = AM.resolve(fa) if fa else [e["from"]["id"]]
            tids = AM.resolve(ta) if ta else [e["to"]["id"]]
            if not fids or not tids:
                S.excluded.append({"relation": rel, "from_anchor": fa, "to_anchor": ta, "reason": "anchor 제외(결정 ⑦) 또는 튜플 없음", "provenance": e["provenance"]})
                continue
            for f in fids:
                for t in tids:
                    e2 = dict(e, **{"from": dict(e["from"], id=f), "to": dict(e["to"], id=t), "attrs": dict(e["attrs"])})
                    if fa:
                        e2["attrs"]["from_anchor"] = {"value": fa, "derived_from": [loc(p) for p in e["provenance"]] or e["derived_from"]}
                    if ta:
                        e2["attrs"]["to_anchor"] = {"value": ta, "derived_from": [loc(p) for p in e["provenance"]] or e["derived_from"]}
                    out.append(e2)
        S.R[rel] = out
    # R26 · R27 · R28
    D = S.ctx["proc"]
    for c in D["cat_recs"]:
        it = S.ctx["items"][(c["family"], c["name"])]
        dec = {"what_basis": c.get("what_basis"), "fragments": c.get("fragments"), "family_fragments": c.get("family_fragments"), "extra_primaries": c.get("extra_primaries", []),
               "extra_sites": c.get("extra_sites", []), "qualifiers": c.get("qualifiers", []), "unregistered_fragments": c.get("unregistered", []), "self_reason": c.get("self_reason")}
        for tid in AM.resolve(c["catalog_item_id"]):
            S.edge("R26", "procedure", tid, "catalog_item", c["catalog_item_id"], [P("taxonomy.json", "modality[].subcategories[].items[].name", it["r"])],
                   {"decomposition": {"value": dec, "derived_from": [it["name_loc"]]}})
    for tid, rec in S.E["procedure"].items():
        a = {x: rec["attrs"][x][0]["value"] for x in ("what_kind", "what_id", "site_id")}
        df = rec["derived_from"]
        tt = {"modality": "modality", "modality_subcategory": "modality_subcategory", "product": "product", "catalog_item": "catalog_item", "component": "product"}.get(a["what_kind"])   # v3.3(V3.3-A): component 끝 = product(kind=component) · 값 0
        if tt is None:
            # v3.2(V3.2-6) what_kind=ingredient — 성분은 사전 값(DIC-)이지 개체가 아니라 R27 끝(modality|modality_subcategory|product|catalog_item)이 없다 · 튜플 what_id 에 사전 id 보존
            S.ctx.setdefault("r27_skipped", []).append((tid, a["what_kind"], a["what_id"]))
        else:
            S.edge("R27", "procedure", tid, tt, a["what_id"], [], {"what_kind": {"value": a["what_kind"], "derived_from": df}}, derived_from=df)
        if a["site_id"] != "none":
            S.edge("R28", "procedure", tid, "site", a["site_id"], [], {}, derived_from=df)
    # tuple 끝 same_session_order
    for anc, val, df in S.ctx.get("tuple_session_order", []):
        for tid in AM.resolve(anc):
            rec = S.E["procedure"].get(tid)
            if rec is not None:
                S.dattr(rec, "same_session_order", val, df, replace=False)
    # R31
    for uid, rec in S.E["adverse_effect"].items():
        sk = rec["attrs"]["site_ref_kind"][0]["value"]
        sid = rec["attrs"]["site_ref_id"][0]["value"]
        if sk == "site":   # v3.1(V3.1-9): 끝은 anatomical·layer·region 만 — 상대 부위는 none(relative_site_text)
            S.edge("R31", "adverse_effect", uid, "site", sid, [], {}, derived_from=rec["derived_from"])
