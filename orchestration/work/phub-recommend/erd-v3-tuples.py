#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ERD v3 — 튜플 분해 실측기. v2.4(erd-v2.4-tuples.py · 동결) 위에 발주서 erd-v3-brief.md 의 변경 10건 중 분해·실측에 닿는 것(V3-1 · V3-2 · V3-3 · V3-4 · V3-5 · V3-8 후보 표)을 바꾼다. 독립 실행.
원장 21 = 브론즈 2판 `bronze/phub-ledger/`(HASHES.txt 검증) — 1판과의 차이는 부위 나열 `/` → `+` 6곳.

v2.4 → v3:
  V3-1 부작용 튜플 (event, site, course, qualifier?) — 수식 조각(사전 adverse_qualifier)은 같은 멤버 안에서만(C) · 둘 이상이면 수식마다(B) · 붙지 않으면 extra_qualifiers(raw/unlinked) · 없음 = none(값) · 식별자 포함 · 「공기색전」은 접두 수식 + 사건으로 가른다.
  V3-2 괄호 안 조각 하나가 회사 사전(manufacturer)·제품 사전에 닿으면 바깥 what 의 그 회사 제품/그 제품.
  V3-3 stopwords(규칙 데이터 · locator 실측)는 조각이 아니라 qualifier_text · `\\d+차` → session_index.
  V3-4 `+` 함께 · `/` 부위 둘 → 함께 · 대안 둘 → 또는 · 괄호 안 대안은 바깥 하나(alternatives) · 「무엇을 하나 × 부위 여럿」 → 같은 what 의 튜플 여럿(anchor REF-…#s<i>) · R12 member_mode.
  V3-5 site 사전에 kind(anatomical|relative|layer|region) · 조직층 5 — 시술 site 칸에는 layer 를 넣지 않는다(layer_fragments).
  실측 신설: `+`/`/` 라벨 전수(2판 `+` 4곳 · 1판 이름 대조) · stopwords 전후 미등록 조각 · 회사 괄호 후보 전수 · qualifier 가 생기는 이름 전부 · v2.4 접힘·exact 대조.

입력(같은 폴더): erd-v3-dictionaries.json(없으면 v2.4) · erd-v3.json(tuple_rules/resolve_rules — 없으면 erd_spec_v3) · erd-v2.4-tuples.py(→ v2.3 → … → v2) · erd-v1.1-resolve.py · bronze/phub-ledger/ · erd-v2.4-tuples.json(나란히 비교)
출력: 표준 출력에 §9.5/§9.6 표 + erd-v3-tuples.json
실행: python3 erd-v3-tuples.py
"""
import hashlib
import importlib.util
import json
import os
import re
import sys
import unicodedata
from collections import Counter, OrderedDict, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(HERE, "bronze", "phub-ledger")


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


V24 = load_module("erd_v24_tuples", os.path.join(HERE, "erd-v2.4-tuples.py"))
V23 = V24.V23
V22 = V24.V22
V21 = V22.V21
V2 = V24.V2
V11 = V2.V11
norm, mkid, md_table, with_alias = V2.norm, V2.mkid, V2.md_table, V2.with_alias
locator = V23.locator
PRIMARY_KINDS = V2.PRIMARY_KINDS
DICT_WHAT_KINDS = V22.DICT_WHAT_KINDS
END_KINDS = V23.END_KINDS
PRINCIPLES = V24.PRINCIPLES
SEP_RE = re.compile(r"([+/&,])")
AND_SEPS = {"+", "&", ","}
SESSION_RE = re.compile(r"^(\d+)\s*차$")
COUNT_RE = re.compile(r"^(\d+)\s*회")


def _dedupe(xs):
    return list(dict.fromkeys(xs))


def bronze_check(ledger_dir):
    """HASHES.txt(16자리 접두)로 원장 21 을 검증한다 — 2판."""
    hp = os.path.join(ledger_dir, "HASHES.txt")
    out = {"dir": ledger_dir, "hashes_file": os.path.exists(hp), "files": 0, "mismatch": []}
    if not out["hashes_file"]:
        return out
    for line in open(hp, encoding="utf-8"):
        h, f = line.split()
        full = hashlib.sha256(open(os.path.join(ledger_dir, f), "rb").read()).hexdigest()
        out["files"] += 1
        if not full.startswith(h):
            out["mismatch"].append(f)
    return out


# ---------------------------------------------------------------------------
# 개체 id + v3 색인(수식 사전 · 회사 · 부위 kind)
# ---------------------------------------------------------------------------
class Ids3(V2.Ids):
    def __init__(self, dic_json, L, resolve_rules):
        super().__init__(dic_json, L)
        D = {d["name"]: d for d in dic_json["dictionaries"]}
        # 부위 kind(V3-5)
        self.site_kind = {}
        for e in D["site"]["entries"]:
            self.site_kind[norm(e["canonical"])] = e.get("kind") or ("region" if e["canonical"] == "얼굴" else "anatomical")
        # 수식 사전(V3-1)
        self.qualifier, self.qualifier_surface = {}, {}
        for e in D.get("adverse_qualifier", {"entries": []})["entries"]:
            self.qualifier[norm(e["canonical"])] = {"id": e["id"], "label": e["canonical"], "kind": e.get("kind")}
            self.qualifier_surface[norm(e["canonical"])] = e["canonical"]
            for s in e.get("synonyms", []):
                self.qualifier_surface[norm(s["value"])] = e["canonical"]
        # 회사 사전(V3-2) — 정준값 · 동의어 · `/` 로 이어진 회사명 각각
        self.manufacturer_surface = {}
        for e in D["manufacturer"]["entries"]:
            self.manufacturer_surface[norm(e["canonical"])] = e["canonical"]
            for part in e["canonical"].split("/"):
                self.manufacturer_surface.setdefault(norm(part), e["canonical"])
            for s in e.get("synonyms", []):
                self.manufacturer_surface[norm(s["value"])] = e["canonical"]
        # 제품 → 제조사(원장 products.json · taxonomy products[].manufacturer)
        self.product_company = defaultdict(set)
        for sec, body in L["products.json"].items():
            if isinstance(body, dict):
                for pr in body["products"]:
                    if pr.get("manufacturer") and pr["manufacturer"] != "-":
                        self.product_company[norm(pr["name"])].add(pr["manufacturer"])
        for m in L["taxonomy.json"]["modality"]:
            for pr in m["products"]:
                if pr.get("manufacturer") and pr["manufacturer"] != "-":
                    self.product_company[norm(pr["name"])].add(pr["manufacturer"])
        # stopwords(V3-3)
        sw = resolve_rules["step2_decompose"].get("stopwords", {})
        self.stopwords = {norm(w["word"]): w["word"] for w in sw.get("words", [])}
        self.stopwords_enabled = True

    def products_of_company(self, family, company_canonical):
        """바깥 what 의 계열 안 제품 중 제조사가 그 회사인 제품(정준값 기준 · `/` 분리 각각)."""
        out = []
        for k, p in self.prod.items():
            if family and family not in str(p["family"]).split("|"):
                continue
            comps = self.product_company.get(k, set())
            for c in comps:
                if self.manufacturer_surface.get(norm(c)) == company_canonical:
                    out.append(p)
                    break
        return out


# ---------------------------------------------------------------------------
# §1.3 분해기 v3 — stopwords · manufacturer(inner) · layer_site · 분리 기호 기록
# ---------------------------------------------------------------------------
class V3Resolver(V2.V2Resolver):
    def classify3(self, frag, family, where):
        c = self.classify2(frag, family)
        if c and c["kind"] == "site" and self.ids.site_kind.get(norm(c["canonical"])) == "layer":
            return {"kind": "layer_site", "text": frag.strip(), "canonical": c["canonical"]}
        if c is None and where == "inner":
            t = norm(frag)
            if t in self.ids.manufacturer_surface:
                return {"kind": "manufacturer", "text": frag.strip(), "canonical": self.ids.manufacturer_surface[t]}
        return c

    def is_stop(self, tok):
        return self.ids.stopwords_enabled and norm(tok) in self.ids.stopwords

    def decompose(self, label, family, exclude=None):
        self.exclude = exclude
        parens = self.paren_re.findall(label)
        outer = self.paren_re.sub(" ", label)
        groups = []
        for where, g in [("outer", outer)] + [("inner", p) for p in parens]:
            members, sep = [], None
            for piece in SEP_RE.split(g):
                if piece in ("+", "/", "&", ","):
                    sep = piece
                    continue
                part = piece.strip(" ·")
                if not part:
                    continue
                spans, untouched, stops = [], [], []
                c = self.classify3(part, family, where)
                if c and c["kind"] != "ambiguous":
                    spans.append(c)
                else:
                    toks = part.split()
                    i = 0
                    while i < len(toks):
                        found = None
                        for j in range(len(toks), i, -1):
                            h = self.classify3(" ".join(toks[i:j]), family, where)
                            if h and h["kind"] != "ambiguous":
                                found = (h, j)
                                break
                        if found:
                            spans.append(found[0])
                            i = found[1]
                        else:
                            if self.is_stop(toks[i]):
                                stops.append(toks[i])
                            else:
                                amb = self.classify(toks[i], family)
                                untouched.append({"text": toks[i], "reason": "모호(계열 " + ",".join(amb["codes"]) + ")" if amb and amb["kind"] == "ambiguous" else "사전 없음"})
                            i += 1
                members.append({"text": part, "spans": spans, "untouched": untouched, "stopwords": stops, "sep": sep})
                sep = None
            groups.append({"where": where, "members": members})
        self.exclude = None
        return groups


def _frag(s):
    return f"{s['kind']}:{s['canonical']}"


def _is_primary_member(m):
    return any(s["kind"] in PRIMARY_KINDS for s in m["spans"])


def _site_only_member(m):
    return bool(m["spans"]) and all(s["kind"] == "site" for s in m["spans"]) and not m["untouched"]


def _primary_only_member(m):
    return bool(m["spans"]) and all(s["kind"] in PRIMARY_KINDS for s in m["spans"]) and not m["untouched"]


class ProcedureTuples3(V23.ProcedureTuples23):
    """v2.3 위에 V3-2(회사 괄호) · V3-3(stopwords) · V3-4(조합 기호 · 부위 여럿 · member_mode) · V3-5(layer 는 시술 site 아님)."""

    def __init__(self, lex, rules, ids, L):
        super().__init__(lex, rules, ids, L)
        self.R = V3Resolver(lex, rules, ids)
        self.company_applied = []     # (라벨, 회사, 제품)
        self.company_candidates = []  # inner 조각 하나짜리 괄호 전부
        self.multi_tuples = []        # 「무엇을 하나 × 부위 여럿」 결과
        self.alternatives = []        # 괄호 안 대안

    # --- 보조: 멤버 묶음만으로 v2.2 조립 (what/site/technique)
    def _assemble_members(self, members, family, for_item, anchor, label_text):
        return V22.ProcedureTuples22.assemble22(self, [{"where": "outer", "members": members}], family, for_item, anchor, label_text)

    def _annotate(self, groups, base):
        mems = [m for g in groups for m in g["members"]]
        base["qualifier_text"] = [t for m in mems for t in m.get("stopwords", [])]
        sess = [int(SESSION_RE.match(unicodedata.normalize("NFKC", s["canonical"]).replace(" ", "")).group(1)) for m in mems for s in m["spans"] if s["kind"] == "spec" and SESSION_RE.match(unicodedata.normalize("NFKC", s["canonical"]).replace(" ", ""))]
        base["session_index"] = sess[0] if sess else None
        base["layer_fragments"] = [s["canonical"] for m in mems for s in m["spans"] if s["kind"] == "layer_site"]
        base["manufacturer_fragments"] = [s["canonical"] for m in mems for s in m["spans"] if s["kind"] == "manufacturer"]
        base.setdefault("member_mode", None)
        base.setdefault("alternatives", None)
        return base

    @staticmethod
    def _mode_of(members):
        seps = {m["sep"] for m in members[1:]}
        if seps and seps <= AND_SEPS:
            return "and"
        if seps == {"/"}:
            return "or"
        if not seps:
            return None
        return "mixed"

    def assemble22(self, groups, family, for_item, anchor, label_text=None):
        base = super().assemble22(groups, family, for_item, anchor, label_text)
        base = self._annotate(groups, base)
        if base["untouched"]:
            return base  # ⑨ unregistered — 규칙은 사전 값을 만들지 않는다
        outer = groups[0]
        inners = groups[1:]
        outer_prims = [m for m in outer["members"] if _is_primary_member(m)]
        # ---- V3-2 괄호 안 회사·제품 (inner 묶음 하나 · 멤버 하나 · 조각 하나)
        if len(inners) == 1 and len(inners[0]["members"]) == 1 and len(outer_prims) == 1:
            im = inners[0]["members"][0]
            sp0 = im["spans"][0] if len(im["spans"]) == 1 else None
            # 제품 사전에 닿은 조각 — overlap 규칙(항목 > 제품)으로 kind=procedure 가 됐어도 제품 사전에 닿으면 V3-2 의 「제품」이다
            if sp0 is not None and sp0["kind"] == "procedure" and norm(sp0["canonical"]) in self.ids.prod:
                sp0 = dict(sp0, kind="product", overlap_kind="procedure")
            if sp0 is not None and not im["untouched"] and sp0["kind"] in ("manufacturer", "product"):
                sp = sp0
                sub = self._assemble_members(outer["members"], family, for_item, anchor, label_text)
                sub = self._annotate(groups, sub)
                if sub["kind"] == "tuple" and sub["what_kind"] in ("modality", "modality_subcategory", "product"):
                    fam = str(sub["what"].get("family"))
                    if sp["kind"] == "manufacturer":
                        cands = self.ids.products_of_company(fam if fam != "None" else None, sp["canonical"])
                        if len(cands) == 1:
                            sub.update(what_kind="product", what=cands[0], what_basis=f"company_paren:{sp['canonical']}→product:{cands[0]['label']}", company=sp["canonical"])
                            self.company_applied.append({"label": label_text, "company": sp["canonical"], "product": cands[0]["label"], "family": fam})
                            return sub
                        return dict(base, kind="ambiguous", reason="company_product", status="ambiguous", detail=[p["label"] for p in cands], company=sp["canonical"])
                    e = self.ids.prod.get(norm(sp["canonical"]))
                    if e is not None:
                        sub.update(what_kind="product", what=e, what_basis=f"company_paren:product:{e['label']}" + ("(타 계열)" if fam not in str(e["family"]).split("|") else ""), cross_family=fam not in str(e["family"]).split("|"))
                        self.company_applied.append({"label": label_text, "company": None, "product": e["label"], "family": fam})
                        return sub
        # ---- V3-4 괄호 안 대안: inner 묶음 하나가 `/` 로 나뉜 primary 멤버 둘 이상 · 바깥 primary 하나
        alt_groups = [ig for ig in inners if len(ig["members"]) >= 2 and all(_primary_only_member(m) for m in ig["members"]) and self._mode_of(ig["members"]) == "or"]
        other_inner_prims = [m for ig in inners for m in ig["members"] if ig not in alt_groups and _is_primary_member(m)]
        if alt_groups and len(alt_groups) == 1 and len(outer_prims) == 1 and not other_inner_prims:
            sub = self._assemble_members(outer["members"] + [m for ig in inners if ig not in alt_groups for m in ig["members"]], family, for_item, anchor, label_text)
            sub = self._annotate(groups, sub)
            if sub["kind"] == "tuple":
                alts = []
                for m in alt_groups[0]["members"]:
                    w = None
                    for s in m["spans"]:
                        if s["kind"] in PRIMARY_KINDS:
                            w = self.what_of(s, family, False) if s["kind"] != "modality" else {"kind": "modality", "what": self.ids.mod.get(s.get("code")), "basis": f"modality:{s['canonical']}"}
                            break
                    alts.append({"text": m["text"], "fragments": [_frag(s) for s in m["spans"]], "what_kind": w["kind"] if w and w.get("what") else None, "what_id": w["what"]["id"] if w and w.get("what") else None})
                sub.update(member_mode="or", alternatives=alts)
                self.alternatives.append({"label": label_text, "what": f"{sub['what_kind']}:{sub['what']['label']}", "alternatives": [a["text"] for a in alts]})
                return sub
        # ---- V3-4 「무엇을 하나 × 부위 여럿」: primary 멤버 하나 + 부위만 멤버(`+`/`/` 또는 괄호 안) · 그 밖 멤버 없음
        mems = [(g["where"], i, m) for g in groups for i, m in enumerate(g["members"])]
        prim = [(w, i, m) for w, i, m in mems if _is_primary_member(m)]
        siteonly = [(w, i, m) for w, i, m in mems if _site_only_member(m)]
        others = [(w, i, m) for w, i, m in mems if not _is_primary_member(m) and not _site_only_member(m) and (m["spans"] or m["untouched"])]
        if len(prim) == 1 and siteonly and not others:
            pw, pi, pm = prim[0]
            ok_sep = all((w == "inner" and i == 0) or m["sep"] in ("+", "/") or (w == "outer" and i == 0 and pi == 1 and pm["sep"] in ("+", "/")) for w, i, m in siteonly)
            pm_sites = [s for s in pm["spans"] if s["kind"] == "site"]
            if ok_sep and len(pm_sites) <= 1 and len([s for s in pm["spans"] if s["kind"] == "technique"]) <= 1:
                sub = self._assemble_members([pm], family, for_item, anchor, label_text)
                sub = self._annotate(groups, sub)
                if sub["kind"] == "tuple":
                    sites = _dedupe([s["canonical"] for s in pm_sites] + [s["canonical"] for w, i, m in siteonly for s in m["spans"]])
                    site_objs = [self.ids.site[norm(x)] for x in sites]
                    out = dict(base, kind="multi_tuple", what_kind=sub["what_kind"], what=sub["what"], what_basis=sub["what_basis"], technique=sub["technique"], sites=site_objs,
                               member_mode="and", via_item=sub.get("via_item"), extra_primaries=[], extra_sites=[], symbols=sorted({m["sep"] for w, i, m in siteonly if m["sep"]} | {"()"} if any(w == "inner" for w, i, m in siteonly) else {m["sep"] for w, i, m in siteonly if m["sep"]}))
                    self.multi_tuples.append({"label": label_text, "what": f"{sub['what_kind']}:{sub['what']['label']}", "sites": sites, "symbols": out["symbols"]})
                    return out
        # ---- combo_ref 의 member_mode(V3-4)
        if base["kind"] == "combo_ref":
            cm = None
            for g in groups:
                pm_ = [m for m in g["members"] if _is_primary_member(m)]
                if len(pm_) >= 2:
                    cm = pm_
                    break
            mode = self._mode_of(cm) if cm else None
            if mode == "mixed":
                return dict(base, kind="ambiguous", reason="combo_mixed", status="ambiguous", detail=[m["text"] for m in cm])
            base["member_mode"] = mode or "and"
        return base

    # --- ① 분류 항목 — multi_tuple 지원
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
        if a["kind"] != "multi_tuple":
            self._busy.discard(key)
            self.catalog.pop(key, None)
            rec = super().catalog_tuple(family, sub, name)
            for k_ in ("qualifier_text", "session_index", "layer_fragments", "manufacturer_fragments", "member_mode", "alternatives"):
                rec[k_] = a.get(k_)
            rec["company"] = a.get("company")
            return rec
        rec = {"family": family, "subcategory": sub, "name": name, "catalog_item_id": cat_id, "whole_match": whole, "anchor": cat_id,
               "groups": [{"where": g["where"], "members": [{"text": m["text"], "spans": [(s["kind"], s["canonical"]) for s in m["spans"]], "untouched": [u["text"] for u in m["untouched"]], "stopwords": m.get("stopwords", []), "sep": m.get("sep")} for m in g["members"]]} for g in groups],
               "fragments": a["fragments"], "family_fragments": a.get("family_fragments", [])}
        src = {"origin": "catalog_item", "label": name, "family": family, "catalog_item_id": cat_id}
        ids = [self.register22(a["what_kind"], a["what"], st, a["technique"], "catalog_item", dict(src, site_index=i), [], f"{cat_id}#s{i}", matched=name) for i, st in enumerate(a["sites"])]
        rec.update({"result": "multi_tuple", "procedure_id": ids[0], "member_ids": ids, "member_mode": "and", "unregistered": [], "qualifiers": a["qualifiers"], "what_basis": a["what_basis"], "status": "complete",
                    "extra_primaries": [], "extra_sites": [], "sites": [s["label"] for s in a["sites"]], "qualifier_text": a["qualifier_text"], "session_index": a["session_index"], "layer_fragments": a["layer_fragments"], "manufacturer_fragments": a["manufacturer_fragments"], "alternatives": None})
        self.catalog[key] = rec
        self._busy.discard(key)
        return rec

    # --- ② ③ 참조 — multi_tuple · member_mode · alternatives · qualifier_text
    def run_reference(self, label, hint, origin, slot):
        if isinstance(label, str) and (label.startswith("__MODALITY__") or label.startswith("__SUBID__")):
            r = super().run_reference(label, hint, origin, slot)
            r.update({"qualifier_text": [], "session_index": None, "layer_fragments": [], "member_mode": None, "alternatives": None})
            return r
        anc = V22.ref_anchor(label, hint)
        groups, whole = self.decompose_whole_first(label, hint)
        a = self.assemble22(groups, hint, False, anc, str(label))
        base = {"label": label, "hint": hint, "ref_id": anc, "whole_match": whole, "fragments": a["fragments"], "family_fragments": a.get("family_fragments", []),
                "groups": [{"where": g["where"], "members": [{"text": m["text"], "spans": [(s["kind"], s["canonical"]) for s in m["spans"]], "untouched": [u["text"] for u in m["untouched"]], "stopwords": m.get("stopwords", []), "sep": m.get("sep")} for m in g["members"]]} for g in groups],
                "qualifier_text": a.get("qualifier_text", []), "session_index": a.get("session_index"), "layer_fragments": a.get("layer_fragments", []), "manufacturer_fragments": a.get("manufacturer_fragments", []),
                "member_mode": a.get("member_mode"), "alternatives": a.get("alternatives"), "company": a.get("company")}
        src = {"origin": origin, "slot": slot, "label": label, "family": hint, "ref_id": anc}
        if a["untouched"]:
            base.update({"result": "unresolved", "unresolved_reason": "unregistered", "unregistered": a["untouched"], "qualifiers": a["qualifiers"], "reason": "미등록 조각 있음 → ⑨ 미해결",
                         "extra_primaries": list(a["fragments"]["primaries"]), "extra_sites": list(a["fragments"]["sites"])})
            return base
        if a["kind"] == "ambiguous":
            base.update({"result": "unresolved", "unresolved_reason": a["reason"], "unregistered": [], "qualifiers": a["qualifiers"], "detail": a.get("detail"),
                         "reason": {"multi_primary": "primary 조각 둘 이상(조합 아님) → ⑨ 미해결 (버리고 접지 않음)", "multi_site": "한 멤버 안의 site 조각 둘 이상(분리 기호 없음) → ⑨ 미해결", "multi_technique": "technique 조각 둘 이상 → ⑨ 미해결",
                                    "unusable_primary": "what 으로 쓸 수 없는 primary 조각 → ⑨ 미해결", "combo_outside_fragment": "조합 멤버 밖 primary/site 조각 → ⑨ 미해결", "company_product": "괄호 안 회사의 제품이 바깥 계열에 하나가 아님 → ⑨ 미해결", "combo_mixed": "한 라벨에 `+` 와 `/` 가 섞임 → ⑨ 미해결"}.get(a["reason"], a["reason"] + " → ⑨ 미해결"),
                         "extra_primaries": list(a["fragments"]["primaries"]), "extra_sites": list(a["fragments"]["sites"])})
            return base
        if a["kind"] == "multi_tuple":
            ids = [self.register22(a["what_kind"], a["what"], st, a["technique"], origin, dict(src, site_index=i, member=True), [], f"{anc}#s{i}", matched=str(label)) for i, st in enumerate(a["sites"])]
            base.update({"result": "multi_tuple", "member_ids": ids, "member_count": len(ids), "member_mode": "and", "what_kind": a["what_kind"], "what_basis": a["what_basis"], "sites": [s["label"] for s in a["sites"]], "technique": a["technique"],
                         "symbols": a["symbols"], "unregistered": [], "qualifiers": a["qualifiers"], "status": "complete", "extra_primaries": [], "extra_sites": []})
            return base
        if a["kind"] == "combo_ref":
            ids = [self.register22(m["what_kind"], m["what"], m["site"], m["technique"], origin, dict(src, member=True), [], m["anchor"], matched=m["text"]) for m in a["members"]]
            base.update({"result": "combo_ref", "member_ids": list(dict.fromkeys(ids)), "member_count": len(a["members"]), "member_mode": a.get("member_mode") or "and", "unregistered": [], "qualifiers": a["qualifiers"], "status": "complete", "extra_primaries": [], "extra_sites": []})
            return base
        if a["kind"] == "tuple":
            tid = self.register22(a["what_kind"], a["what"], a["site"], a["technique"], origin, src, [], a["anchor"])
            base.update({"result": "tuple", "procedure_id": tid, "what_kind": a["what_kind"], "what_basis": a["what_basis"], "site": a["site"]["label"] if a["site"] else None, "technique": a["technique"],
                         "technique_origin": "fragment" if a["technique"] else "none", "unregistered": [], "qualifiers": a["qualifiers"], "status": "complete", "anchor": a["anchor"], "via_item": a.get("via_item"),
                         "extra_primaries": [], "extra_sites": []})
            return base
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


def tids_of(r):
    return [r.get("procedure_id")] if r["result"] == "tuple" else r.get("member_ids", []) if r["result"] in ("combo_ref", "multi_tuple") else []


# ---------------------------------------------------------------------------
# 엣지 자리별 끝 분포 (v2.3 그대로 + multi_tuple · member_mode)
# ---------------------------------------------------------------------------
def edge_ends(PT, ref_rows, mk_rows, cat_recs, L, ids):
    T = PT.tuples
    cat = {(r["family"], r["name"]): r for r in cat_recs}
    item_by_id = {}
    for m in L["taxonomy.json"]["modality"]:
        for sc in m["subcategories"]:
            for it in sc["items"]:
                item_by_id[it["id"]] = (m["id"], it["name"])
    sub_ids, mod_ids = set(ids.sub), set(ids.mod)

    def classify_code(v):
        v = str(v)
        if v in mod_ids:
            return ("modality", ids.mod[v]["id"], None)
        if v in sub_ids:
            return ("subcategory", ids.sub[v]["id"], None)
        if v in item_by_id:
            fam, name = item_by_id[v]
            rec = cat[(fam, name)]
            return ("procedure", rec.get("procedure_id") if rec["result"] != "multi_tuple" else list(rec["member_ids"]), rec["catalog_item_id"])
        return ("unresolved", None, None)

    rows = []

    def text_row(slot, rel, note, rrows, product_slot=False):
        ends = []
        for r in rrows:
            if r["result"] == "tuple":
                t = T[r["procedure_id"]]
                kind = "product" if product_slot else "procedure"
                ends.append({"label": r["label"], "hint": r.get("hint"), "end_kind": kind, "target_depth": kind, "end_id": t["what_id"] if product_slot else r["procedure_id"],
                             "procedure_id": r["procedure_id"], "via_catalog_item": (mkid("CAT", f"{t['family']}|{r['via_item']}") if (r.get("via_item") and not product_slot) else None), "anchored": t["anchor"] is not None,
                             "member_mode": r.get("member_mode"), "alternatives": [a["text"] for a in r["alternatives"]] if r.get("alternatives") else None, "qualifier_text": r.get("qualifier_text") or [], "session_index": r.get("session_index")})
            elif r["result"] in ("combo_ref", "multi_tuple"):
                ends.append({"label": r["label"], "hint": r.get("hint"), "end_kind": "procedure", "target_depth": "procedure", "end_id": list(r["member_ids"]), "procedure_id": list(r["member_ids"]), "via_catalog_item": None,
                             "combo_members": len(r["member_ids"]), "anchored": any(T[m]["anchor"] is not None for m in r["member_ids"]), "member_mode": r.get("member_mode"), "multi_tuple": r["result"] == "multi_tuple", "qualifier_text": r.get("qualifier_text") or [], "session_index": r.get("session_index")})
            elif r["result"] == "node":
                ends.append({"label": r["label"], "hint": r.get("hint"), "end_kind": r["end_kind"], "target_depth": r["end_kind"], "end_id": r["end_id"], "procedure_id": None, "via_catalog_item": None})
            else:
                ends.append({"label": r["label"], "hint": r.get("hint"), "end_kind": "unresolved", "target_depth": None, "end_id": None, "procedure_id": None, "via_catalog_item": None, "reason": r.get("unresolved_reason") or r["result"], "qualifier_text": r.get("qualifier_text") or []})
        c = Counter(e["end_kind"] for e in ends)
        rows.append(OrderedDict([("slot", slot), ("relation", rel), ("note", note), ("kind", "text"), ("n", len(ends))] + [(k, c.get(k, 0)) for k in END_KINDS]
                                + [("procedure_anchored", sum(1 for e in ends if e["end_kind"] == "procedure" and e.get("anchored"))), ("via_catalog_item", sum(1 for e in ends if e.get("via_catalog_item"))),
                                   ("member_mode_and", sum(1 for e in ends if e.get("member_mode") == "and")), ("member_mode_or", sum(1 for e in ends if e.get("member_mode") == "or")), ("multi_tuple", sum(1 for e in ends if e.get("multi_tuple"))), ("ends", ends)]))

    for slot, rrows in ref_rows.items():
        rel, note = V23.SLOT_RELATION[slot]
        text_row(slot, rel, note, rrows, product_slot=slot.startswith("problem-packages.procedures[].products[]"))
    text_row("market-pricing.items[].name (122)", V23.MARKET_SLOT_NOTE[0], V23.MARKET_SLOT_NOTE[1], mk_rows)

    def code_row(slot, rel, note, values):
        ends = []
        for v in values:
            if isinstance(v, tuple) and v[0] == "item":
                rec = cat[(v[1], v[2])]
                ends.append({"label": v[2], "hint": v[1], "end_kind": "procedure", "target_depth": "procedure", "end_id": rec.get("procedure_id") if rec["result"] != "multi_tuple" else list(rec["member_ids"]), "via_catalog_item": rec["catalog_item_id"]})
            elif isinstance(v, tuple) and v[0] == "product":
                p = ids.prod.get(norm(v[2]))
                ends.append({"label": v[2], "hint": v[1], "end_kind": "product" if p else "unresolved", "target_depth": "product" if p else None, "end_id": p["id"] if p else None, "reason": None if p else "제품 색인에 없는 taxonomy products[] 이름"})
            else:
                k, eid, via = classify_code(v)
                ends.append({"label": str(v), "hint": None, "end_kind": k, "target_depth": k if k != "unresolved" else None, "end_id": eid, "via_catalog_item": via})
        c = Counter(e["end_kind"] for e in ends)
        rows.append(OrderedDict([("slot", slot), ("relation", rel), ("note", note), ("kind", "code"), ("n", len(ends))] + [(k, c.get(k, 0)) for k in END_KINDS]
                                + [("procedure_anchored", None), ("via_catalog_item", sum(1 for e in ends if e.get("via_catalog_item"))), ("member_mode_and", 0), ("member_mode_or", 0), ("multi_tuple", 0), ("ends", ends)]))

    r3 = [r for r in cat_recs if r["result"] == "tuple" and r.get("what_kind") == "product" and r.get("whole_match") and str(r.get("what_basis", "")).startswith("product:") and "(타 계열)" not in str(r.get("what_basis", ""))]
    rows.append(OrderedDict([("slot", "taxonomy.json:modality[].subcategories[].items[].name = 같은 계열 제품명 (①)"), ("relation", "R3"), ("note", "uses_product — 항목 이름이 같은 계열 제품명과 정규화 완전 일치. from 끝 = 그 항목의 튜플(what=product)"), ("kind", "code"), ("n", len(r3))]
                            + [(k, (len(r3) if k == "procedure" else 0)) for k in END_KINDS]
                            + [("procedure_anchored", sum(1 for r in r3 if T[r["procedure_id"]]["anchor"] is not None)), ("via_catalog_item", len(r3)), ("member_mode_and", 0), ("member_mode_or", 0), ("multi_tuple", 0),
                               ("ends", [{"label": r["name"], "hint": r["family"], "end_kind": "procedure", "target_depth": "procedure", "end_id": r["procedure_id"], "via_catalog_item": r["catalog_item_id"]} for r in r3])]))
    comp = L["complications.json"]
    code_row("complications.json:categories[].id (10)", "R15", "from — 계열 코드 자리(이름 65 의 원인 시술)", [c["id"] for c in comp["categories"]])
    pih = L["pih-risk.json"]
    code_row("pih-risk.json:procedures[].procedure_ref (26)", "R15", "from — 가장 구체 수준 그대로(질문 5): 항목 id → 그 항목의 튜플 · 하위분류 id → subcategory · M 코드 → modality", [p["procedure_ref"] for p in pih["procedures"]])
    tl = L["post-procedure-timeline.json"]
    code_row("post-procedure-timeline.json:timelines[].category (10)", "R15", "from — M 코드 → modality · M16-DCA → subcategory(질문 7)", [t["category"] for t in tl["timelines"]])
    code_row("post-procedure-timeline.json:timelines[].phases[].normal/abnormal/caution/emergency[] 문구 (R29 → R15)", "R15", "from = 그 타임라인의 category", [t["category"] for t in tl["timelines"] for ph in t["phases"] for k in ("normal", "abnormal", "caution", "emergency") for _ in (ph.get(k) or [])])
    code_row("consent-checklist.json:categories[].emergency_signs[] 문구 (R29 → R15)", "R15", "from = categories[].id", [c["id"] for c in L["consent-checklist.json"]["categories"] for _ in (c.get("emergency_signs") or [])])
    ex = L["extracted.json"]
    code_row("extracted.json:{code}.safety.common/uncommon/serious/emergency[] 문구 (R29 → R15)", "R15", "from = 코드 키(계열)", [code for code, v in ex.items() if V2.CODE_KEY_RE.match(code) for k in ("common", "uncommon", "serious", "emergency") for _ in ((v.get("safety") or {}).get(k) or [])])
    tx = L["taxonomy.json"]
    code_row("taxonomy.json:modality[].extracted.safety.common/uncommon/serious[] 문구 (R29 → R15)", "R15", "from = 계열 레코드", [m["id"] for m in tx["modality"] for k in ("common", "uncommon", "serious") for _ in (((m.get("extracted") or {}).get("safety") or {}).get(k) or [])])
    code_row("taxonomy.json:modality[].subcategories[].items[].extracted.safety.* 문구 (R29 → R15)", "R15", "from = 항목 레코드 → 그 항목의 튜플(procedure)",
             [("item", m["id"], it["name"]) for m in tx["modality"] for sc in m["subcategories"] for it in sc["items"] for k in ("common", "serious", "common_adverse_effects", "serious_adverse_effects", "long_term") for _ in (((it.get("extracted") or {}).get("safety") or {}).get(k) or [])])
    code_row("taxonomy.json:modality[].products[].extracted.safety.* 문구 (R29 → R15)", "R15", "from = 제품 레코드 → product(제품 층까지만 적힘)",
             [("product", m["id"], pr["name"]) for m in tx["modality"] for pr in m["products"] for k in ("common", "serious", "common_side_effects") for _ in (((pr.get("extracted") or {}).get("safety") or {}).get(k) or [])])
    lit = L["literature-evidence.json"]
    code_row("literature-evidence.json:categories.{code}.adverse_effects[] (R29 → R15)", "R15", "from = 코드 키(계열)", [code for code, c in lit["categories"].items() for _ in (c.get("adverse_effects") or [])])
    code_row("consent-checklist.json:categories[].id (17)", "R16", "from — 계열 코드 자리", [c["id"] for c in L["consent-checklist.json"]["categories"]])
    code_row("pre-procedure-checklist.json:category_specific[].id (17)", "R16", "from — 계열 코드 자리", [c["id"] for c in L["pre-procedure-checklist.json"]["category_specific"]])
    code_row("contraindications.json:rules[].from/to (27×2)", "R18", "kind=pair_rule — M 코드 자리", [x for r in L["contraindications.json"]["rules"] for x in (r["from"], r["to"])])
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
            "relations_covered": sorted({r["relation"] for r in rows if r["relation"] != "—"}, key=lambda x: int(x[1:])),
            "member_mode": {"and": sum(r["member_mode_and"] for r in rows if r["relation"] != "—"), "or": sum(r["member_mode_or"] for r in rows if r["relation"] != "—")}, "multi_tuple_ends": sum(r["multi_tuple"] for r in rows if r["relation"] != "—")}


# ---------------------------------------------------------------------------
# 부작용 — V3-1 qualifier · V3-5 layer
# ---------------------------------------------------------------------------
class AdverseTuples3(V24.AdverseTuples24):
    def __init__(self, ids):
        super().__init__(ids)
        # 사전 순서 relative_site → site → course → adverse_qualifier → event (setdefault = 앞 순서 우선)
        self.lookup = {}
        for surf, canon in ids.rsite_surface.items():
            self.lookup.setdefault(surf, ("relative", canon))
        for surf, canon in ids.site_surface.items():
            self.lookup.setdefault(surf, ("site", canon))
        for surf, canon in ids.course_surface.items():
            self.lookup.setdefault(surf, ("course", canon))
        for surf, canon in ids.qualifier_surface.items():
            self.lookup.setdefault(surf, ("qualifier", canon))
        for surf, canon in ids.event_surface.items():
            self.lookup.setdefault(surf, ("event", canon))
        self.prefix_splits = []

    def split(self, text):
        parens = V2.ADV_PAREN.findall(text)
        outer = V2.ADV_PAREN.sub(" ", text)
        groups = []
        for where, g in [("outer", outer)] + [("inner", p) for p in parens]:
            members = []
            for part in V2.ADV_MEMBER_SPLIT.split(g):
                part = part.strip()
                if not part:
                    continue
                toks = [t.strip(V2.ADV_STRIP) for t in part.split()]
                toks = [t for t in toks if t]
                spans, untouched = [], []
                i = 0
                while i < len(toks):
                    found = None
                    for j in range(min(len(toks), i + self.maxlen), i, -1):
                        key = norm("".join(toks[i:j]))
                        if key in self.lookup:
                            found = (self.lookup[key], " ".join(toks[i:j]), j)
                            break
                    if found:
                        spans.append({"kind": found[0][0], "canonical": found[0][1], "text": found[1]})
                        i = found[2]
                        continue
                    # V3-1: 접두 수식 + 사건 (완전 일치만 · 「공기색전」)
                    tok = toks[i]
                    nt = norm(tok)
                    hit = None
                    for k in range(1, len(nt)):
                        if nt[:k] in self.ids.qualifier_surface and nt[k:] in self.ids.event_surface:
                            hit = (nt[:k], nt[k:])
                            break
                    if hit:
                        spans.append({"kind": "qualifier", "canonical": self.ids.qualifier_surface[hit[0]], "text": tok, "basis": "prefix_split"})
                        spans.append({"kind": "event", "canonical": self.ids.event_surface[hit[1]], "text": tok})
                        self.prefix_splits.append((tok, self.ids.qualifier_surface[hit[0]], self.ids.event_surface[hit[1]]))
                    else:
                        untouched.append(tok)
                    i += 1
                members.append({"text": part, "spans": spans, "untouched": untouched})
            groups.append({"where": where, "members": members})
        return groups

    def assemble(self, groups):
        """v2.4 조립 + 수식(qualifier): 사건이 놓인 멤버 안의 수식만(C) · 둘 이상이면 수식마다(B) · 붙지 않으면 extra_qualifiers."""
        out, merges = [], []
        extra_sites, extra_courses, extra_quals = [], [], []
        for g in groups:
            ms = g["members"]
            pending, pending_text = [], []
            for idx, m in enumerate(ms):
                spans = m["spans"]
                events = _dedupe(s["canonical"] for s in spans if s["kind"] == "event")
                sites = _dedupe((s["kind"], s["canonical"]) for s in spans if s["kind"] in ("relative", "site"))
                courses = _dedupe(s["canonical"] for s in spans if s["kind"] == "course")
                quals = _dedupe(s["canonical"] for s in spans if s["kind"] == "qualifier")
                qbasis = {s["canonical"]: s.get("basis", "member") for s in spans if s["kind"] == "qualifier"}
                if not events:
                    nxt = ms[idx + 1] if idx + 1 < len(ms) else None
                    if sites and not courses and not quals and not m["untouched"] and nxt is not None and any(s["kind"] == "event" for s in nxt["spans"]):
                        pending += sites
                        pending_text.append(m["text"])
                        continue
                    extra_sites += [s[1] for s in sites] + [s[1] for s in pending]
                    extra_courses += courses
                    extra_quals += quals
                    pending, pending_text = [], []
                    continue
                site_list = bool(pending)
                all_sites = _dedupe(pending + sites)
                if site_list:
                    merges.append({"where": g["where"], "site_members": list(pending_text), "event_member": m["text"], "sites": [s[1] for s in all_sites], "events": events})
                pending, pending_text = [], []
                site_opts = all_sites or [None]
                course_opts = courses or ["미상"]
                qual_opts = quals or [None]
                for ev in events:
                    for st in site_opts:
                        for co in course_opts:
                            for q in qual_opts:
                                out.append({"event": ev, "site": st, "course": co, "qualifier": q, "member": (" / ".join(pending_text) + " / " if site_list and pending_text else "") + m["text"],
                                            "site_basis": ("site_list" if site_list and st in pending else "member") if st else None, "course_basis": "member" if courses else None, "qualifier_basis": qbasis.get(q) if q else None,
                                            "n_site_candidates": len(all_sites), "n_course_candidates": len(courses), "n_qualifier_candidates": len(quals)})
            extra_sites += [s[1] for s in pending]
        untouched = [u for g in groups for m in g["members"] for u in m["untouched"]]
        seen, uniq = set(), []
        for t in out:
            k = (t["event"], t["site"], t["course"], t["qualifier"])
            if k not in seen:
                seen.add(k)
                uniq.append(t)
        return uniq, untouched, {"extra_sites": _dedupe(extra_sites), "extra_courses": _dedupe(extra_courses), "extra_qualifiers": _dedupe(extra_quals), "site_list_merges": merges}

    def qual_key(self, q):
        return self.ids.qualifier[norm(q)]["id"] if q else "none"

    def register(self, t, src, untouched, extras=None):
        assert not untouched
        ev = self.ids.event[norm(t["event"])]
        if t["site"] is None:
            site_id, site_label, site_kind = "none", None, "none"
        elif t["site"][0] == "relative":
            site_id, site_label, site_kind = self.ids.rsite[norm(t["site"][1])]["id"], t["site"][1], "relative"
        else:
            site_id, site_label, site_kind = self.ids.site[norm(t["site"][1])]["id"], t["site"][1], "site"
        cid = self.ids.course[norm(t["course"])]["id"]
        qid = self.qual_key(t["qualifier"])
        tid = mkid("ADV", f"{ev['id']}|{site_id}|{cid}|{qid}")
        rec = self.tuples.get(tid)
        if rec is None:
            rec = {"id": tid, "event_kind": "dict", "event": ev["label"], "event_id": ev["id"], "event_category": ev["category"], "site_kind": site_kind, "site": site_label, "site_id": site_id,
                   "site_dict_kind": (self.ids.site_kind.get(norm(t["site"][1])) if t["site"] and t["site"][0] == "site" else ("relative" if t["site"] else None)),
                   "course": t["course"], "course_id": cid, "qualifier": t["qualifier"], "qualifier_id": qid, "qualifier_basis": t.get("qualifier_basis"),
                   "status": "complete", "unregistered_fragments": [], "origins": [], "sources": [], "anchor": None, "all_dict_values": True, "candidate_name": [], "event_fragments": [ev["label"]],
                   "extra_sites": [], "extra_courses": [], "extra_qualifiers": [], "site_basis": t.get("site_basis"), "course_basis": t.get("course_basis")}
            self.tuples[tid] = rec
        rec["sources"].append(src)
        if src["origin"] not in rec["origins"]:
            rec["origins"].append(src["origin"])
        self.units[(rec["event_id"], rec["site_id"], rec["course_id"], rec["qualifier_id"])] = tid
        return tid

    def register_raw(self, text, tuples, untouched, extras, src, anchor):
        all_events = _dedupe(t["event"] for t in tuples)
        sites = _dedupe([t["site"][1] for t in tuples if t["site"]] + list(extras["extra_sites"]))
        courses = _dedupe([t["course"] for t in tuples if t["course"] != "미상"] + list(extras["extra_courses"]))
        quals = _dedupe([t["qualifier"] for t in tuples if t["qualifier"]] + list(extras["extra_qualifiers"]))
        cid = self.ids.course[norm("미상")]["id"]
        event_id = f"RAW:{anchor}"
        tid = mkid("ADV", f"{event_id}|none|{cid}|none|{anchor}")
        rec = self.tuples.get(tid)
        unatt = bool(extras["extra_sites"] or extras["extra_courses"] or extras["extra_qualifiers"])
        if rec is None:
            cat = self.ids.event[norm(all_events[0])]["category"] if all_events else None
            rec = {"id": tid, "event_kind": "raw_name", "event": text, "event_id": event_id, "event_category": cat, "site_kind": "none", "site": None, "site_id": "none", "site_dict_kind": None, "course": "미상", "course_id": cid,
                   "qualifier": None, "qualifier_id": "none", "qualifier_basis": None,
                   "status": "partial" if untouched else "unresolved", "unregistered_fragments": list(untouched), "origins": [], "sources": [], "anchor": anchor, "all_dict_values": False, "candidate_name": list(untouched),
                   "event_fragments": all_events, "extra_sites": sites, "extra_courses": courses, "extra_qualifiers": quals, "site_basis": None, "course_basis": None,
                   "dict_tuples": [(t["event"], t["site"][1] if t["site"] else None, t["course"], t["qualifier"]) for t in tuples], "raw_reason": ("unregistered" if untouched else "") + ("+" if untouched and unatt else "") + ("unattached_fragments" if unatt else "")}
            self.tuples[tid] = rec
        rec["sources"].append(src)
        if src["origin"] not in rec["origins"]:
            rec["origins"].append(src["origin"])
        return tid

    def candidates_of(self, tuples):
        out = []
        for t in tuples:
            ev = self.ids.event[norm(t["event"])]
            sid = self.site_key(t["site"])
            cid = self.ids.course[norm(t["course"])]["id"]
            qid = self.qual_key(t["qualifier"])
            key = (ev["id"], sid, cid, qid)
            out.append({"event": t["event"], "event_id": ev["id"], "site": t["site"][1] if t["site"] else None, "site_kind": t["site"][0] if t["site"] else "none", "site_id": sid, "course": t["course"], "course_id": cid,
                        "qualifier": t["qualifier"], "qualifier_id": qid, "qualifier_basis": t.get("qualifier_basis"),
                        "would_be_id": mkid("ADV", f"{ev['id']}|{sid}|{cid}|{qid}"), "exists": key in self.units, "unit_id": self.units.get(key), "site_basis": t["site_basis"], "course_basis": t["course_basis"], "member": t["member"]})
        return out

    def _row(self, text, src, groups, tuples, untouched, extras):
        spans = [(s["kind"], s["canonical"], s["text"]) for g in groups for m in g["members"] for s in m["spans"]]
        return {"text": text, "spans": spans, "locator": src.get("locator"), "unregistered": untouched, "extra_sites": extras["extra_sites"], "extra_courses": extras["extra_courses"], "extra_qualifiers": extras["extra_qualifiers"], "site_list_merges": extras["site_list_merges"],
                "b_splits": [(t["event"], t["site"][1] if t["site"] else None, t["course"], t["n_site_candidates"], t["n_course_candidates"], t["qualifier"], t["n_qualifier_candidates"]) for t in tuples if t["n_site_candidates"] >= 2 or t["n_course_candidates"] >= 2 or t["n_qualifier_candidates"] >= 2],
                "dict_tuples": [(t["event"], t["site"][1] if t["site"] else None, t["course"], t["qualifier"]) for t in tuples], "event_fragments": _dedupe(t["event"] for t in tuples),
                "qualifiers": _dedupe(t["qualifier"] for t in tuples if t["qualifier"])}

    def run_name(self, text, src):
        groups = self.split(text)
        tuples, untouched, extras = self.assemble(groups)
        base = self._row(text, src, groups, tuples, untouched, extras)
        unattached = bool(extras["extra_sites"] or extras["extra_courses"] or extras["extra_qualifiers"])
        if untouched or unattached:
            tid = self.register_raw(text, tuples, untouched, extras, src, src["locator"])
            r = self.tuples[tid]
            base.update({"event_kind": "raw_name", "tuples": [(r["event"], None, "미상", None, None, None)], "tuple_ids": [tid], "candidate_name": untouched, "anchor": src["locator"], "raw_reason": r["raw_reason"]})
            return base
        ids = [self.register(t, src, untouched) for t in tuples]
        base.update({"event_kind": "dict" if ids else None, "tuples": [(t["event"], t["site"][1] if t["site"] else None, t["course"], t["course_basis"], t["site_basis"], t["qualifier"]) for t in tuples], "tuple_ids": ids, "candidate_name": [], "anchor": None})
        return base

    def run_expression(self, text, src):
        groups = self.split(text)
        tuples, untouched, extras = self.assemble(groups)
        cands = self.candidates_of(tuples)
        reasons = []
        if not cands:
            reasons.append("no_event")
        if untouched:
            reasons.append("unregistered")
        if extras["extra_sites"] or extras["extra_courses"] or extras["extra_qualifiers"]:
            reasons.append("unattached_fragments")
        if cands and any(not c["exists"] for c in cands):
            reasons.append("no_unit")
        exact = not reasons
        ids = []
        if exact:
            for c in cands:
                tid = c["unit_id"]
                rec = self.tuples[tid]
                rec["sources"].append(src)
                if src["origin"] not in rec["origins"]:
                    rec["origins"].append(src["origin"])
                ids.append(tid)
        base = self._row(text, src, groups, tuples, untouched, extras)
        base.update({"candidates": cands, "tuples": [(t["event"], t["site"][1] if t["site"] else None, t["course"], t["course_basis"], t["site_basis"], t["qualifier"]) for t in tuples],
                     "tuple_ids": _dedupe(ids), "match_status": "exact" if exact else "unlinked", "unlinked_reasons": reasons})
        return base


def run_adverse(ids, rules, L, v24tup=None):
    AT = AdverseTuples3(ids)
    comp_rows = []
    for cat in L["complications.json"]["categories"]:
        for i, c in enumerate(cat["complications"]):
            loc = locator("complications.json", "categories[].complications[].name", f"{cat['id']}/{i}")
            r = AT.run_name(c["name"], {"origin": "complications", "file": "complications.json", "path": "categories[].complications[].name", "modality": cat["id"], "record": i, "locator": loc})
            r.update({"modality": cat["id"], "severity": c.get("severity"), "record": i})
            comp_rows.append(r)
    comp_tuple_ids = _dedupe(x for r in comp_rows for x in r["tuple_ids"])
    n_units_before_expr = len(AT.tuples)
    expr_rows = []
    for kind, text, src in V23.adverse_phrases23(L):
        r = AT.run_expression(text, dict(src, kind=kind))
        r.update({"kind": kind, "modality": src.get("modality"), "origin": src["origin"], "path": src["path"], "context": src.get("context")})
        if kind == "evidence_statement" and src.get("patient_ko"):
            r2 = AT.run_expression(src["patient_ko"], dict(src, kind="patient_text", lang="ko", path="categories.{code}.adverse_effects[].patient_ko", origin="literature.patient_ko", locator=src["locator"].replace(".statement@", ".patient_ko@")))
            r["patient_ko"] = {k_: r2[k_] for k_ in ("text", "tuples", "b_splits", "site_list_merges", "candidates", "tuple_ids", "unregistered", "extra_sites", "extra_courses", "extra_qualifiers", "match_status", "unlinked_reasons", "qualifiers")}
            union = r["candidates"] + [c for c in r2["candidates"] if c["would_be_id"] not in {x["would_be_id"] for x in r["candidates"]}]
            reasons = _dedupe(r["unlinked_reasons"] + r2["unlinked_reasons"])
            exact = r["match_status"] == "exact" and r2["match_status"] == "exact"
            if not exact and (r["tuple_ids"] or r2["tuple_ids"]):
                for tid in r["tuple_ids"] + r2["tuple_ids"]:
                    rec = AT.tuples[tid]
                    rec["sources"] = [s_ for s_ in rec["sources"] if s_.get("locator") not in (r["locator"], r2["locator"])]
                    for o in ("literature", "literature.patient_ko"):
                        if o in rec["origins"] and not any(s_["origin"] == o for s_ in rec["sources"]):
                            rec["origins"].remove(o)
                r["tuple_ids"], r2["tuple_ids"], r["patient_ko"]["tuple_ids"] = [], [], []
            r["candidates_union"] = union
            r["unlinked_reasons"] = reasons
            r["match_status"] = "exact" if exact else "unlinked"
            r["tuple_ids_union"] = _dedupe(r["tuple_ids"] + r2["tuple_ids"]) if exact else []
            r["basis"] = "both" if exact else "none"
        else:
            r["tuple_ids_union"] = r["tuple_ids"]
            r["candidates_union"] = r["candidates"]
        r["linked"] = r["match_status"] == "exact"
        expr_rows.append(r)
    A = AT.tuples
    assert len(A) == n_units_before_expr, "표현이 튜플을 만들었다"
    adv_folded = []
    for tid in comp_tuple_ids:
        rows_ = [r for r in comp_rows if tid in r["tuple_ids"]]
        names = [f"{r['text']} [{r['modality']}]" for r in rows_]
        own_unreg = _dedupe(u for r in rows_ for u in r["unregistered"])
        t = A[tid]
        adv_folded.append({"adverse_id": tid, "event_kind": t["event_kind"], "event": t["event"], "category": t["event_category"], "site_kind": t["site_kind"], "site": t["site"], "site_dict_kind": t.get("site_dict_kind"), "course": t["course"], "qualifier": t["qualifier"], "status": t["status"] if t["event_kind"] == "raw_name" else ("partial" if own_unreg else "complete"),
                           "all_dict_values": t["all_dict_values"], "anchor": t["anchor"], "n_names": len(names), "names": names, "unregistered": own_unreg, "event_fragments": t["event_fragments"], "extra_sites": t["extra_sites"], "extra_courses": t["extra_courses"], "extra_qualifiers": t["extra_qualifiers"],
                           "dict_tuples": t.get("dict_tuples"), "raw_reason": t.get("raw_reason"), "site_basis": t.get("site_basis"), "course_basis": t.get("course_basis"), "qualifier_basis": t.get("qualifier_basis")})
    adv_folded.sort(key=lambda x: (-x["n_names"], x["event_kind"], x["category"] or "", x["event"], x["qualifier"] or ""))
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

    def all_cands(r):
        return r.get("candidates_union") or r["candidates"]

    def kind_summary(kind):
        rows = [r for r in expr_rows if r["kind"] == kind]
        return {"n": len(rows), "linked": sum(1 for r in rows if r["linked"]), "unlinked": sum(1 for r in rows if not r["linked"]),
                "match_status": dict(Counter(r["match_status"] for r in rows)),
                "unlinked_reasons": dict(Counter(x for r in rows if not r["linked"] for x in r["unlinked_reasons"])),
                "distinct_tuples": len({x for r in rows for x in r["tuple_ids_union"]}),
                "new_tuples_not_from_complications": len({x for r in rows for x in r["tuple_ids_union"] if "complications" not in A[x]["origins"]}),
                "candidate_units_not_existing": len({c["would_be_id"] for r in rows for c in all_cands(r) if not c["exists"]})}

    raw = [t for t in A.values() if t["event_kind"] == "raw_name"]
    dict_t = [t for t in A.values() if t["event_kind"] == "dict"]
    af2 = [f for f in adv_folded if f["n_names"] >= 2]
    lop = [r for r in comp_rows if "LOP" in r["text"]]
    course_split = [{"name": f"{r['text']} [{r['modality']}]", "event_kind": r["event_kind"], "tuples": [t[:3] for t in r["dict_tuples"]]} for r in comp_rows
                    if r["dict_tuples"] and any(c in r["text"] for c in ("일시적", "지연성", "가역적", "Transient", "Delayed", "영구", "Late-Onset"))]
    all_rows = comp_rows + expr_rows + [dict(r["patient_ko"], kind="patient_text", text=r["patient_ko"]["text"]) for r in expr_rows if r.get("patient_ko")]
    site_outside_member = [(r["text"][:40], t[:3]) for r in all_rows for t in r["tuples"] if t[1] and t[4] not in ("member", "site_list")]
    site_list_merges = [{"text": r["text"], "kind": r.get("kind", "complications"), "merges": r["site_list_merges"]} for r in all_rows if r.get("site_list_merges")]
    multi_cand = [{"text": r["text"], "kind": r.get("kind", "complications"), "tuples": [t[:3] + (t[5],) for t in r["b_splits"]], "site_candidates": max(t[3] for t in r["b_splits"]), "course_candidates": max(t[4] for t in r["b_splits"]), "qualifier_candidates": max(t[6] for t in r["b_splits"])} for r in all_rows if r.get("b_splits")]
    headache_injection = [(r["text"][:40], t[:3]) for r in all_rows for t in r["tuples"] if t[0] == "두통" and t[1] == "주사 부위"]
    headache_injection_tuples = [t["id"] for t in A.values() if t["event"] == "두통" and t["site"] == "주사 부위"]
    unattached = [{"text": r["text"], "kind": r.get("kind", "complications"), "extra_sites": r["extra_sites"], "extra_courses": r["extra_courses"], "extra_qualifiers": r["extra_qualifiers"]} for r in all_rows if r["extra_sites"] or r["extra_courses"] or r["extra_qualifiers"]]
    raw_cells = {"n": len(raw), "site_none": sum(1 for t in raw if t["site_id"] == "none"), "course_unknown": sum(1 for t in raw if t["course"] == "미상"), "qualifier_none": sum(1 for t in raw if t["qualifier_id"] == "none"), "with_dict_tuples": sum(1 for t in raw if t.get("dict_tuples")),
                 "by_reason": dict(Counter(t["raw_reason"] for t in raw)), "with_extra_sites": sum(1 for t in raw if t["extra_sites"]), "with_extra_courses": sum(1 for t in raw if t["extra_courses"]), "with_extra_qualifiers": sum(1 for t in raw if t["extra_qualifiers"])}
    new_from_expr = [t["id"] for t in A.values() if "complications" not in t["origins"]]
    partial_linked = [r["text"][:40] for r in expr_rows if r["tuple_ids_union"] and (r["unregistered"] or (r.get("patient_ko") or {}).get("unregistered") or r["extra_sites"] or r["extra_courses"] or r["extra_qualifiers"] or (r.get("patient_ko") or {}).get("extra_sites") or (r.get("patient_ko") or {}).get("extra_courses") or (r.get("patient_ko") or {}).get("extra_qualifiers"))]
    cand_units = Counter()
    cand_units_detail = {}
    for r in expr_rows:
        for c in all_cands(r):
            if not c["exists"]:
                cand_units[c["would_be_id"]] += 1
                cand_units_detail.setdefault(c["would_be_id"], {"event": c["event"], "site": c["site"], "site_kind": c["site_kind"], "course": c["course"], "qualifier": c["qualifier"], "expressions": 0, "kinds": Counter()})
                cand_units_detail[c["would_be_id"]]["expressions"] += 1
                cand_units_detail[c["would_be_id"]]["kinds"][r["kind"]] += 1
    cand_units_list = [dict(v, id=k, kinds=dict(v["kinds"])) for k, v in sorted(cand_units_detail.items(), key=lambda x: -x[1]["expressions"])]
    # ---- V3-1 실측: qualifier 가 생기는 이름·표현 전부
    q_names = [{"text": r["text"], "modality": r["modality"], "event_kind": r["event_kind"], "dict_tuples": r["dict_tuples"], "qualifiers": r["qualifiers"], "extra_qualifiers": r["extra_qualifiers"], "spans": [s for s in r["spans"] if s[0] == "qualifier"]} for r in comp_rows if r["qualifiers"] or r["extra_qualifiers"] or any(s[0] == "qualifier" for s in r["spans"])]
    q_exprs = [{"text": r["text"], "kind": r.get("kind"), "origin": r.get("origin"), "locator": r.get("locator"), "match_status": r.get("match_status"), "candidates": [(c["event"], c["site"], c["course"], c["qualifier"], c["exists"]) for c in r.get("candidates", []) if c["qualifier"]], "extra_qualifiers": r["extra_qualifiers"], "qualifier_spans": [s for s in r["spans"] if s[0] == "qualifier"]}
               for r in expr_rows + [dict(r["patient_ko"], kind="patient_text", origin="literature.patient_ko", locator=(r.get("locator") or "").replace(".statement@", ".patient_ko@"), spans=[]) for r in expr_rows if r.get("patient_ko")] if r.get("qualifiers") or r.get("extra_qualifiers") or any(s[0] == "qualifier" for s in r.get("spans", []))]
    q_tuples = [t for t in A.values() if t["qualifier_id"] != "none"]
    # ---- V3-5 실측: layer 부위가 붙은 튜플·후보·조각
    layer_tuples = [t for t in A.values() if t.get("site_dict_kind") == "layer"]
    layer_cands = [(r["text"][:40], c["event"], c["site"], c["exists"]) for r in expr_rows for c in all_cands(r) if c["site"] and ids.site_kind.get(norm(c["site"])) == "layer"]
    layer_extra = [(r["text"][:40], [s for s in r["extra_sites"] if ids.site_kind.get(norm(s)) == "layer"]) for r in all_rows if any(ids.site_kind.get(norm(s)) == "layer" for s in r["extra_sites"])]
    # ---- v2.4 대조(접힘 그룹 · exact) — 수식 칸이 기존 접힘·표현 연결을 깨지 않는지
    cmp = {}
    if v24tup:
        v24f = v24tup["adverse"]["folded"]
        g24 = sorted(sorted(f["names"]) for f in v24f if f["event_kind"] == "dict")
        g3 = sorted(sorted(f["names"]) for f in adv_folded if f["event_kind"] == "dict")
        raw24 = sorted(f["names"][0] for f in v24f if f["event_kind"] == "raw_name")
        raw3 = sorted(f["names"][0] for f in adv_folded if f["event_kind"] == "raw_name")
        ex24 = {r["locator"]: r["match_status"] for r in v24tup["adverse"]["expressions"]}
        ex3 = {r["locator"]: r["match_status"] for r in expr_rows}
        diff_ex = [(k, ex24.get(k), ex3.get(k)) for k in set(ex24) | set(ex3) if ex24.get(k) != ex3.get(k)]
        T24 = {t["id"]: t for t in v24tup["adverse"]["tuples"]}
        tid24 = {r["locator"]: sorted({(T24[x]["event"], T24[x]["site"] or "", T24[x]["course"]) for x in r["tuple_ids_union"]}) for r in v24tup["adverse"]["expressions"]}
        tid3 = {r["locator"]: sorted({(A[x]["event"], A[x]["site"] or "", A[x]["course"]) for x in r["tuple_ids_union"]}) for r in expr_rows}
        diff_units = [k for k in tid24 if tid24[k] != tid3.get(k)]
        cmp = {"dict_fold_groups_v24": len(g24), "dict_fold_groups_v3": len(g3), "dict_fold_groups_same": g24 == g3, "fold_group_diff": [g for g in g24 if g not in g3] + [g for g in g3 if g not in g24],
               "raw_names_v24": len(raw24), "raw_names_v3": len(raw3), "raw_names_same": raw24 == raw3,
               "exact_v24": v24tup["adverse"]["summary"]["expressions_total"]["linked"], "exact_v3": sum(1 for r in expr_rows if r["linked"]), "match_status_diff": diff_ex, "linked_units_diff": diff_units,
               "tuples_v24": v24tup["adverse"]["summary"]["tuples_total"], "tuples_v3": len(A), "tuple_ids_changed": "식별자에 qualifier_id 가 들어가 ADV- 값은 전부 바뀐다(네 칸 키) — 접힘 그룹·exact 연결은 위 대조"}
    summary = OrderedDict([
        ("principles", PRINCIPLES),
        ("complications_names", len(comp_rows)),
        ("complications_names_with_tuple", sum(1 for r in comp_rows if r["tuple_ids"])),
        ("complications_names_without_tuple", [f"{r['text']} [{r['modality']}]" for r in comp_rows if not r["tuple_ids"]]),
        ("complications_names_multi_tuple", sum(1 for r in comp_rows if len(r["tuple_ids"]) >= 2)),
        ("complications_names_raw", sum(1 for r in comp_rows if r["event_kind"] == "raw_name")),
        ("complications_names_raw_by_reason", dict(Counter(r["raw_reason"] for r in comp_rows if r["event_kind"] == "raw_name"))),
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
        ("complications_by_qualifier", dict(Counter(A[t]["qualifier"] or "none" for t in comp_tuple_ids))),
        ("complications_by_category", dict(Counter(A[t]["event_category"] for t in comp_tuple_ids))),
        ("event_dictionary_values", len(ids.event)),
        ("event_dictionary_used_by_complications", len({A[t]["event"] for t in comp_tuple_ids if A[t]["event_kind"] == "dict"})),
        ("event_dictionary_unused", sorted(set(e["label"] for e in ids.event.values()) - {A[t]["event"] for t in comp_tuple_ids if A[t]["event_kind"] == "dict"})),
        ("course_dictionary_values", len(ids.course)),
        ("relative_site_values", len(ids.rsite)),
        ("qualifier_dictionary_values", len(ids.qualifier)),
        ("site_dictionary_values", len(ids.site)),
        ("site_dictionary_by_kind", dict(Counter(ids.site_kind.values()))),
        ("course_member_only", True), ("site_member_only", True), ("qualifier_member_only", True), ("expressions_create_units", False), ("qualifier_none_is_value", True),
        ("course_split_examples", course_split),
        ("lop", [{"name": r["text"], "event_kind": r["event_kind"], "tuples": [t[:3] for t in r["tuples"]], "dict_tuples": r["dict_tuples"]} for r in lop]),
        ("site_outside_member", len(site_outside_member)), ("site_outside_member_examples", site_outside_member[:10]),
        ("site_list_merges", len(site_list_merges)), ("site_list_merges_all", site_list_merges),
        ("multi_candidate_splits", len(multi_cand)), ("multi_candidate_splits_all", multi_cand),
        ("headache_x_injection_site", len(headache_injection)), ("headache_x_injection_site_tuples", headache_injection_tuples),
        ("unattached_fragments_texts", len(unattached)), ("unattached_fragments_all", unattached),
        ("raw_cells", raw_cells),
        ("expressions", OrderedDict((k, kind_summary(k)) for k in ["safety_phrase", "emergency_sign", "symptom_phrase", "evidence_statement"])),
        ("expressions_by_origin", OrderedDict((o, {"n": sum(1 for r in expr_rows if r["origin"] == o), "linked": sum(1 for r in expr_rows if r["origin"] == o and r["linked"]), "unlinked": sum(1 for r in expr_rows if r["origin"] == o and not r["linked"])}) for o in dict.fromkeys(r["origin"] for r in expr_rows))),
        ("expressions_total", {"n": len(expr_rows), "linked": sum(1 for r in expr_rows if r["linked"]), "unlinked": sum(1 for r in expr_rows if not r["linked"]), "match_status": dict(Counter(r["match_status"] for r in expr_rows)),
                               "unlinked_reasons": dict(Counter(x for r in expr_rows if not r["linked"] for x in r["unlinked_reasons"])), "patient_text_records": 4 * sum(1 for r in expr_rows if r["kind"] == "evidence_statement")}),
        ("expressions_raw_name_tuples", sum(1 for t in A.values() if t["event_kind"] == "raw_name" and "complications" not in t["origins"])),
        ("expressions_new_tuples", len(new_from_expr)),
        ("expressions_partial_linked", len(partial_linked)), ("expressions_partial_linked_examples", partial_linked[:10]),
        ("candidate_units_not_existing", len(cand_units)), ("candidate_units_not_existing_expressions", sum(cand_units.values())), ("candidate_units_not_existing_all", cand_units_list),
        ("literature_basis", dict(Counter(r.get("basis") for r in expr_rows if r["kind"] == "evidence_statement"))),
        ("tuples_total", len(A)), ("tuples_dict", len(dict_t)), ("tuples_raw_name", len(raw)),
        ("tuples_by_origin", OrderedDict((o, sum(1 for t in A.values() if o in t["origins"])) for o in dict.fromkeys(o for t in A.values() for o in t["origins"]))),
        ("tuples_status", dict(Counter(t["status"] for t in A.values()))),
        ("tuples_by_course", dict(Counter(t["course"] for t in A.values()))),
        ("tuples_by_site_kind", dict(Counter(t["site_kind"] for t in A.values()))),
        ("tuples_by_qualifier", dict(Counter(t["qualifier"] or "none" for t in A.values()))),
        ("tuples_by_category", dict(Counter(t["event_category"] for t in A.values()))),
        ("tuples_all_dict_values", sum(1 for t in A.values() if t["all_dict_values"])),
        ("tuples_with_expression_sources", sum(1 for t in A.values() if any(s_["origin"] != "complications" for s_ in t["sources"]))),
        ("tuples_with_2plus_names_raw", sum(1 for f in af2 if f["event_kind"] == "raw_name")),
        ("folded_with_2plus_names", len(af2)),
        ("folded_with_partial_name", sum(1 for f in af2 if f["status"] == "partial")),
        ("folded_partial_detail", [{"event": f["event"], "site": f["site"], "course": f["course"], "names": f["names"], "unregistered": f["unregistered"]} for f in af2 if f["status"] == "partial"]),
        ("unregistered_distinct", len(adv_unreg)), ("unregistered_total", sum(adv_unreg.values())),
        ("unregistered_all", adv_unreg.most_common()), ("unregistered_by_origin", {k: v.most_common() for k, v in adv_unreg_by_origin.items()}),
        # V3-1
        ("qualifier_names", len(q_names)), ("qualifier_names_all", q_names),
        ("qualifier_expressions", len(q_exprs)), ("qualifier_expressions_all", q_exprs),
        ("qualifier_tuples", len(q_tuples)), ("qualifier_tuples_all", [{"id": t["id"], "event": t["event"], "site": t["site"], "course": t["course"], "qualifier": t["qualifier"], "event_kind": t["event_kind"], "basis": t.get("qualifier_basis"), "sources": len(t["sources"])} for t in q_tuples]),
        ("prefix_splits", _dedupe(AT.prefix_splits)),
        ("qualifier_in_raw_dict_tuples", [{"text": t["event"], "dict_tuples": t["dict_tuples"], "extra_qualifiers": t["extra_qualifiers"]} for t in raw if any(x[3] for x in (t.get("dict_tuples") or [])) or t["extra_qualifiers"]]),
        # V3-5
        ("layer_site_tuples", len(layer_tuples)), ("layer_site_tuples_all", [{"id": t["id"], "event": t["event"], "site": t["site"], "course": t["course"]} for t in layer_tuples]),
        ("layer_site_candidates", len(layer_cands)), ("layer_site_candidates_all", layer_cands[:60]),
        ("layer_site_extra", len(layer_extra)), ("layer_site_extra_all", layer_extra[:60]),
        ("v24_comparison", cmp),
    ])
    return OrderedDict([("summary", summary), ("tuples", list(A.values())), ("complications", comp_rows), ("folded", adv_folded), ("expressions", expr_rows)])


# ---------------------------------------------------------------------------
# 전체 실행 · 집계 (시술 = v3 분해기 · 실측 신설)
# ---------------------------------------------------------------------------
def run_procedure(ids, lex, rules, L, resolve_rules, stop_enabled=True):
    ids.stopwords_enabled = stop_enabled
    PT = ProcedureTuples3(lex, resolve_rules, ids, L)
    PT.run_catalog()
    cat_recs = list(PT.catalog.values())
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
    return PT, cat_recs, ref_rows, mk_rows


def run_all(dic_json, rules, L, resolve_rules=None, v24tup=None):
    if resolve_rules is None:
        sys.path.insert(0, HERE)
        import erd_spec_v3
        resolve_rules = erd_spec_v3.RESOLVE_RULES
    ids = Ids3(dic_json, L, resolve_rules)
    lex = V11.Lexicon(with_alias(dic_json))
    # ---- stopwords 전(비교용 · 결과는 수치만)
    PT0, cat0, ref0, mk0 = run_procedure(ids, lex, rules, L, resolve_rules, stop_enabled=False)
    ids = Ids3(dic_json, L, resolve_rules)
    PT, cat_recs, ref_rows, mk_rows = run_procedure(ids, lex, rules, L, resolve_rules, stop_enabled=True)
    T = PT.tuples
    n_cat = len(cat_recs)
    cat_tuple_ids = [x for r in cat_recs for x in tids_of(r)]
    cat_distinct = list(dict.fromkeys(cat_tuple_ids))

    def slot_summary(rows):
        c = Counter(r["result"] for r in rows)
        st = Counter(r.get("status") for r in rows if r["result"] in ("tuple", "combo_ref", "multi_tuple"))
        return {"n": len(rows), "tuple": c.get("tuple", 0), "multi_tuple": c.get("multi_tuple", 0), "combo_ref": c.get("combo_ref", 0), "node": c.get("node", 0), "unresolved": c.get("unresolved", 0), "none": c.get("none", 0), "complete": st.get("complete", 0), "partial": st.get("partial", 0),
                "unresolved_by_reason": dict(Counter(r.get("unresolved_reason") for r in rows if r["result"] == "unresolved")),
                "node_by_kind": dict(Counter(r.get("end_kind") for r in rows if r["result"] == "node")),
                "member_mode": dict(Counter(r.get("member_mode") for r in rows if r.get("member_mode"))),
                "with_alternatives": sum(1 for r in rows if r.get("alternatives")), "with_qualifier_text": sum(1 for r in rows if r.get("qualifier_text")), "with_session_index": sum(1 for r in rows if r.get("session_index") is not None),
                "distinct_tuples": len({x for r in rows for x in tids_of(r) if x}),
                "new_tuples_not_from_catalog": len({x for r in rows for x in tids_of(r) if x and "catalog_item" not in T[x]["origins"]}),
                "whole_match": sum(1 for r in rows if r.get("whole_match")),
                "by_what_kind": dict(Counter(T[x]["what_kind"] for r in rows for x in tids_of(r) if x))}

    folded = []
    for tid in cat_distinct:
        names = [r for r in cat_recs if tid in tids_of(r)]
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
    # V3-8: 기법 상속 후보 — 계열 + 하위분류별 scope
    inh = []
    for fam, techs in sorted(ids.family_tech.items()):
        if len(techs) != 1:
            continue
        ts = [t for t in T.values() if t["technique_id"] == "none" and str(t.get("family")) == fam]
        cat_items = [r for r in cat_recs if r["family"] == fam and r.get("technique_origin") == "none"]
        by_sub = OrderedDict()
        for r in cat_items:
            by_sub.setdefault(r["subcategory"], []).append(r)
        inh.append({"kind": "canonical_mapping", "from_ref": f"R5:{fam}", "to_technique": techs[0], "to_id": ids.tech[norm(techs[0])]["id"], "scope": [r["catalog_item_id"] for r in cat_items], "scope_note": f"technique=none 인 {fam} 분류 항목의 CAT- id 전부(참조 튜플은 REF- 로 따로) · v3: 하위분류 단위 from_ref=R5:<하위분류 id> 로 scope 를 가를 수 있다",
                    "tuples": len(ts), "catalog_items": len(cat_items), "items": [r["name"] for r in cat_items],
                    "by_subcategory": [{"from_ref": f"R5:{sub}", "subcategory": sub, "label": ids.sub[sub]["label"] if sub in ids.sub else sub, "catalog_items": len(rs), "scope": [r["catalog_item_id"] for r in rs], "items": [r["name"] for r in rs]} for sub, rs in by_sub.items()]})
    mixed = sorted(f for f, v in ids.family_tech.items() if len(v) != 1)
    mixed_detail = [{"family": fam, "techniques": ids.family_tech[fam], "subcategories": [{"subcategory": sc["id"], "label": sc["label"], "catalog_items": len(sc["items"])} for sc in next(m for m in L["taxonomy.json"]["modality"] if m["id"] == fam)["subcategories"]]} for fam in mixed]
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
    # ---- V3-3 실측: stopwords 전후
    unreg0 = Counter()
    for r in cat0 + [r for v in ref0.values() for r in v] + mk0:
        for u in r.get("unregistered", []):
            unreg0[u] += 1
    all_ref = [r for v in ref_rows.values() for r in v] + mk_rows
    all_ref0 = [r for v in ref0.values() for r in v] + mk0
    stop_hits = Counter()
    stop_locs = defaultdict(list)
    for r in cat_recs:
        for w in r.get("qualifier_text") or []:
            stop_hits[norm(w)] += 1
            stop_locs[norm(w)].append(f"taxonomy.json:modality[].subcategories[].items[].name@{r['family']}/{r['name']}")
    for r in all_ref:
        for w in r.get("qualifier_text") or []:
            stop_hits[norm(w)] += 1
            stop_locs[norm(w)].append(f"{r.get('ref_id')}:{r['label']}")
    # 회·차 — 독립 토큰이 아니라 규격 토큰(`\d+회` · `\d+차`) 안에 있다: 그 라벨이 locator
    for r in cat_recs + all_ref:
        for g in r.get("groups", []):
            for m in g["members"]:
                for k_, c_ in m["spans"]:
                    if k_ != "spec":
                        continue
                    cc = unicodedata.normalize("NFKC", str(c_)).replace(" ", "")
                    for w_, rx in (("회", COUNT_RE), ("차", SESSION_RE)):
                        if rx.match(cc):
                            stop_hits[norm(w_)] += 1
                            stop_locs[norm(w_)].append((f"taxonomy.json:modality[].subcategories[].items[].name@{r['family']}/{r['name']}" if "name" in r else f"{r.get('ref_id')}:{r['label']}") + f" (규격 {c_})")
    stop_table = []
    for w in resolve_rules["step2_decompose"]["stopwords"]["words"]:
        nw = norm(w["word"])
        stop_table.append({"word": w["word"], "origin": w["origin"], "hits": stop_hits.get(nw, 0), "locators": _dedupe(stop_locs.get(nw, []))[:12], "unregistered_before": unreg0.get(w["word"], 0), "unregistered_after": unreg_all.get(w["word"], 0),
                           "in_dictionary": bool(lex.hits("product", w["word"]) or lex.hits("modality", w["word"]) or lex.hits("modality_subcategory", w["word"]) or lex.hits("procedure", w["word"]) or lex.hits("site", w["word"]))})
    ref_changed_by_stop = []
    r0map = {(r["label"], r.get("hint")): r for r in all_ref0}
    for r in all_ref:
        r0 = r0map.get((r["label"], r.get("hint")))
        if r0 and (r0["result"] != r["result"] or r0.get("unresolved_reason") != r.get("unresolved_reason") or sorted(r0.get("unregistered", [])) != sorted(r.get("unregistered", []))):
            ref_changed_by_stop.append({"label": r["label"], "hint": r.get("hint"), "slot": next((k for k, v in ref_rows.items() if r in v), "market-pricing.items[].name (122)"), "before": f"{r0['result']}:{r0.get('unresolved_reason') or ''}[{','.join(r0.get('unregistered', []))}]", "after": f"{r['result']}:{r.get('unresolved_reason') or ''}[{','.join(r.get('unregistered', []))}]", "qualifier_text": r.get("qualifier_text")})
    stop_summary = {"unregistered_distinct_before": len(unreg0), "unregistered_total_before": sum(unreg0.values()), "unregistered_distinct_after": len(unreg_all), "unregistered_total_after": sum(unreg_all.values()),
                    "words": stop_table, "words_with_locator": sum(1 for w in stop_table if w["locators"]), "words_total": len(stop_table), "references_changed": ref_changed_by_stop, "references_resolved_newly": sum(1 for x in ref_changed_by_stop if x["after"].startswith(("tuple", "combo_ref", "multi_tuple")) and not x["before"].startswith(("tuple", "combo_ref", "multi_tuple")))}
    # ---- V3-4 실측: `+`/`/` 라벨 전수(참조 자리 + market + 분류 항목) · 1판 이름 대조
    v1_names = {"보톡스(턱선+광대)": "보톡스(턱선/광대)", "보톡스 이마+미간": "보톡스 이마/미간", "필러 볼+턱": "필러 볼/턱", "필러 팔자+볼": "필러 팔자/볼"}
    combo_rows = []
    for slot, rows in list(ref_rows.items()) + [("market-pricing.items[].name (122)", mk_rows)]:
        for r in rows:
            lab = str(r["label"])
            if "+" in lab or "/" in lab:
                combo_rows.append({"slot": slot, "label": lab, "hint": r.get("hint"), "v1_name": v1_names.get(lab), "symbols": sorted(set(ch for ch in lab if ch in "+/")), "result": r["result"], "reason": r.get("unresolved_reason"), "unregistered": r.get("unregistered", []),
                                   "member_mode": r.get("member_mode"), "alternatives": [a["text"] for a in r["alternatives"]] if r.get("alternatives") else None, "sites": r.get("sites"),
                                   "tuples": [f"{T[x]['what_kind']}:{T[x]['what_label']}×{T[x]['site'] or 'none'}×{T[x]['technique'] or 'none'}" for x in tids_of(r)], "qualifier_text": r.get("qualifier_text"), "detail": r.get("detail")})
    for r in cat_recs:
        if "+" in r["name"] or "/" in r["name"]:
            combo_rows.append({"slot": "① taxonomy 항목", "label": r["name"], "hint": r["family"], "v1_name": None, "symbols": sorted(set(ch for ch in r["name"] if ch in "+/")), "result": r["result"], "reason": r.get("self_reason"), "unregistered": r.get("unregistered", []), "member_mode": r.get("member_mode"), "alternatives": [a["text"] for a in r["alternatives"]] if r.get("alternatives") else None, "sites": r.get("sites"),
                               "tuples": [f"{T[x]['what_kind']}:{T[x]['what_label']}×{T[x]['site'] or 'none'}×{T[x]['technique'] or 'none'}" for x in tids_of(r)], "qualifier_text": r.get("qualifier_text"), "detail": r.get("self_detail")})
    plus_v2 = [c for c in combo_rows if c["v1_name"]]
    v24_cmp_rows = []
    if v24tup:
        r24 = {}
        for slot, rows in list(v24tup["procedure"]["references"].items()) + [("market-pricing.items[].name (122)", v24tup["procedure"]["market_pricing"])]:
            for r in rows:
                r24[(slot, str(r["label"]), r.get("hint"))] = r
        T24 = {t["id"]: t for t in v24tup["procedure"]["tuples"]}
        for slot, rows in list(ref_rows.items()) + [("market-pricing.items[].name (122)", mk_rows)]:
            for r in rows:
                key = (slot, str(r["label"]), r.get("hint"))
                old = r24.get(key)
                if old is None:
                    old_lab = v1_names.get(str(r["label"]))
                    old = r24.get((slot, old_lab, r.get("hint"))) if old_lab else None
                o_desc = (f"{old['result']}:{old.get('unresolved_reason') or ''}" + (f"[{','.join(f'{T24[x]['what_kind']}:{T24[x]['what_label']}×{T24[x]['site'] or 'none'}' for x in ([old.get('procedure_id')] if old['result']=='tuple' else old.get('member_ids', [])) if x)}]" if old["result"] in ("tuple", "combo_ref") else "")) if old else "(없음 · 2판 새 이름)"
                n_desc = f"{r['result']}:{r.get('unresolved_reason') or ''}" + (f"[{','.join(f'{T[x]['what_kind']}:{T[x]['what_label']}×{T[x]['site'] or 'none'}' for x in tids_of(r))}]" if r["result"] in ("tuple", "combo_ref", "multi_tuple") else "")
                if o_desc != n_desc:
                    v24_cmp_rows.append({"slot": slot, "label": r["label"], "hint": r.get("hint"), "v24": o_desc, "v3": n_desc, "why": ("V3-4 부위 여럿" if r["result"] == "multi_tuple" else "V3-4 괄호 안 대안" if r.get("alternatives") else "V3-3 stopwords" if r.get("qualifier_text") else "V3-2 회사·제품 괄호" if r.get("company") or str(r.get("what_basis", "")).startswith("company_paren") else "2판 이름" if r["label"] in v1_names else "")})
    # ---- V3-2 실측: 괄호 안 조각 하나짜리 전수(참조 자리 + 분류 항목 + 속성 문장) · 사전 닿음 여부
    PAREN = re.compile(r"\(([^()]*)\)")
    comp_cands = []

    def paren_probe(where, text, hint):
        for inner in PAREN.findall(text):
            if any(ch in inner for ch in "+/&,"):
                continue
            frag = inner.strip()
            if not frag:
                continue
            nf = norm(frag)
            comp_cands.append({"where": where, "text": text, "inner": frag, "manufacturer": ids.manufacturer_surface.get(nf), "product": ids.prod[nf]["label"] if nf in ids.prod else None,
                               "touches": "manufacturer" if nf in ids.manufacturer_surface else "product" if nf in ids.prod else "-"})
    for slot, rows in list(ref_rows.items()) + [("market-pricing.items[].name (122)", mk_rows)]:
        for r in rows:
            paren_probe(slot, str(r["label"]), r.get("hint"))
    for r in cat_recs:
        paren_probe("① taxonomy 항목", r["name"], r["family"])
    for c in L["problem-combos.json"]["combos"]:
        for p in c["packages"]:
            for x in p.get("products", []) or []:
                paren_probe("problem-combos.json:combos[].packages[].products[] (속성 문장)", x, None)
    for code, v in L["extracted.json"].items():
        if V2.CODE_KEY_RE.match(code):
            for x in v.get("related_techniques", []) or []:
                paren_probe("extracted.json:{code}.related_techniques[] (설명 문장)", x, code)
    for m in L["taxonomy.json"]["modality"]:
        for x in ((m.get("extracted") or {}).get("related_techniques") or []):
            paren_probe("taxonomy.json:modality[].extracted.related_techniques[] (설명 문장)", x, m["id"])
    company_summary = {"candidates": len(comp_cands), "touch_manufacturer": sum(1 for c in comp_cands if c["touches"] == "manufacturer"), "touch_product": sum(1 for c in comp_cands if c["touches"] == "product"), "no_touch": sum(1 for c in comp_cands if c["touches"] == "-"),
                       "applied": PT.company_applied, "applied_n": len(PT.company_applied), "ambiguous_company_product": sum(1 for r in all_ref if r.get("unresolved_reason") == "company_product"),
                       "botox_allergan_sites": [c for c in comp_cands if "엘러간" in c["inner"] or "더모톡신" in c["inner"]], "unregistered_inner_top": Counter(c["inner"] for c in comp_cands if c["touches"] == "-").most_common(30), "candidates_all": comp_cands}
    cat_tuples = [T[i] for i in cat_distinct]
    tup_rows = [r for r in cat_recs if r["result"] == "tuple"]
    fold2 = [f for f in folded if f["n_items"] >= 2]
    none_t = [t for t in T.values() if not t["all_dict_values"]]
    EE = edge_ends(PT, ref_rows, mk_rows, cat_recs, L, ids)
    proc_summary = OrderedDict([
        ("bronze_version", 2),
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
        ("catalog_multi_tuple", sum(1 for r in cat_recs if r["result"] == "multi_tuple")),
        ("catalog_with_qualifier_text", sum(1 for r in cat_recs if r.get("qualifier_text"))),
        ("catalog_with_layer_fragments", sum(1 for r in cat_recs if r.get("layer_fragments"))),
        ("catalog_company_applied", sum(1 for r in cat_recs if str(r.get("what_basis", "")).startswith("company_paren"))),
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
        ("tuples_site_by_kind", dict(Counter(ids.site_kind.get(norm(t["site"]), "none") if t["site"] else "none" for t in T.values()))),
        ("tuples_layer_site", sum(1 for t in T.values() if t["site"] and ids.site_kind.get(norm(t["site"])) == "layer")),
        ("technique_inherited", sum(1 for t in T.values() if t["technique_origin"] == "inherited")),
        ("families_without_single_technique", mixed),
        ("families_mixed_detail", mixed_detail),
        ("inheritance_candidates", [{k: v for k, v in c.items() if k not in ("items", "scope")} | {"by_subcategory": [{kk: vv for kk, vv in s.items() if kk not in ("scope", "items")} for s in c["by_subcategory"]]} for c in inh]),
        ("code_references_node", sum(1 for rows in ref_rows.values() for r in rows if r["result"] == "node")),
        ("edge_ends_total", EE["total"]),
        ("edge_ends_total_n", EE["total_n"]),
        ("edge_ends_by_relation", EE["by_relation"]),
        ("edge_ends_slots", {"text": EE["text_slots"], "code": EE["code_slots"], "relations": EE["relations_covered"]}),
        ("edge_ends_member_mode", EE["member_mode"]),
        ("edge_ends_multi_tuple", EE["multi_tuple_ends"]),
        ("unregistered_distinct", len(unreg_all)),
        ("unregistered_total", sum(unreg_all.values())),
        ("unregistered_top30", unreg_all.most_common(30)),
        ("unregistered_top30_by_origin", {k: v.most_common(30) for k, v in unreg_by_origin.items()}),
        # V3-3
        ("stopwords", stop_summary),
        # V3-4
        ("combo_labels", len(combo_rows)), ("combo_labels_all", combo_rows), ("combo_plus_v2", plus_v2),
        ("combo_by_result", dict(Counter(c["result"] + (":" + c["reason"] if c["reason"] else "") for c in combo_rows))),
        ("combo_member_mode", dict(Counter(c["member_mode"] for c in combo_rows if c["member_mode"]))),
        ("multi_tuples", PT.multi_tuples), ("alternatives", PT.alternatives),
        ("v24_reference_changes", v24_cmp_rows),
        # V3-2
        ("company_paren", company_summary),
    ])
    adv = run_adverse(ids, rules, L, v24tup)
    out = OrderedDict([
        ("erd_version", "v3"), ("rules", rules["name"]), ("bronze_version", 2), ("bronze_check", bronze_check(LEDGER if os.path.isdir(LEDGER) else "")), ("fallback_to_parent", False), ("fold_condition", "세 칸 전부 사전 값일 때만"), ("technique_inheritance", False), ("edge_end", "procedure"),
        ("course_member_only", True), ("adverse_fold_unregistered", False), ("site_member_only", True), ("expressions_create_units", False), ("raw_name_cells", "none/미상"), ("qualifier_none_is_value", True), ("principles", PRINCIPLES),
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


def load_v24_summary():
    try:
        j = json.load(open(os.path.join(HERE, "erd-v2.4-tuples.json"), encoding="utf-8"))
        return j["procedure"]["summary"], j["adverse"]["summary"]
    except (FileNotFoundError, KeyError):
        return None, None


def _kv(d):
    return ", ".join(f"{k}={v}" for k, v in (d or {}).items())


def _fmt_tuple(TT, x):
    t = TT[x]
    return f"{t['what_kind']}:{t['what_label']}×{t['site'] or 'none'}×{t['technique'] or 'none'}"


def procedure_md(R, v24s=None):
    s = R["procedure"]["summary"]
    v24s = v24s or load_v24_summary()[0] or {}
    g = lambda k, d="—": v24s.get(k, d)  # noqa
    o = []
    A = o.append
    TT = {t["id"]: t for t in R["procedure"]["tuples"]}
    cat = {(r["family"], r["name"]): r for r in R["procedure"]["catalog"]}
    A("#### 9.5.1 분류 항목 521 → 튜플 (v2.4 → v3 나란히 · 원장 2판)")
    A("")
    A(md_table(["항목", "v2.4", "v3"], [
        ("분류 항목", g("catalog_items"), s["catalog_items"]),
        ("분해 결과", _kv(g("catalog_result", {})), _kv(s["catalog_result"])),
        ("튜플 수(distinct)", f"**{g('catalog_distinct_tuples')}** (비율 {g('catalog_fold_ratio')})", f"**{s['catalog_distinct_tuples']}** (521 → N · 비율 {s['catalog_fold_ratio']})"),
        ("둘 이상 항목이 접힌 튜플", f"{g('catalog_tuples_with_2plus_items')} 개 튜플에 항목 {g('catalog_items_in_folded_tuples')} 개", f"{s['catalog_tuples_with_2plus_items']} 개 튜플에 항목 {s['catalog_items_in_folded_tuples']} 개"),
        ("what 축", _kv(g("catalog_by_what_kind", {})) + " · 근거: " + _kv(g("catalog_by_what_basis", {})), _kv(s["catalog_by_what_kind"]) + " · 근거: " + _kv(s["catalog_by_what_basis"])),
        ("항목 자신(catalog_item)이 what 인 항목", g("catalog_self_items"), f"{s['catalog_self_items']} (사유: {_kv(s['catalog_self_by_reason'])} · 그중 부위 칸 있음 {s['catalog_self_with_site']})"),
        ("site 축", f"none {g('catalog_site_none')} / 항목 기준 {g('catalog_site_none_ratio')} · 튜플 기준 {g('catalog_tuple_site_none_ratio')}", f"none {s['catalog_site_none']} / 항목 기준 none 비율 {s['catalog_site_none_ratio']} · 튜플 기준 {s['catalog_tuple_site_none_ratio']}"),
        ("technique 축", _kv(g("catalog_technique", {})) + f" · 항목 기준 none {g('catalog_technique_none_ratio')}", _kv(s["catalog_technique"]) + f" · 항목 기준 none 비율 {s['catalog_technique_none_ratio']} · 튜플 기준 {s['catalog_tuple_technique_none_ratio']}"),
        ("항목 상태", _kv(g("catalog_status", {})), _kv(s["catalog_status"])),
        ("v3 신설 — 부위 여럿(multi_tuple) 항목 · stopwords 가 뗀 항목 · layer 조각 항목 · 회사 괄호 적용 항목", "—", f"{s['catalog_multi_tuple']} · {s['catalog_with_qualifier_text']} · {s['catalog_with_layer_fragments']} · {s['catalog_company_applied']}"),
    ]))
    A("")
    A("#### 9.5.2 접힌 결과 — 둘 이상의 분류 항목이 같은 튜플로 간 것 전부 (세 칸 전부 사전 값만 남는다 · v2.4 와 같은 규칙)")
    A("")
    rows = [(i + 1, f["what_kind"], f["what"], f["site"] or "none", f"{f['technique'] or 'none'}({f['technique_origin']})", f["n_items"], " · ".join(f["items"]))
            for i, f in enumerate(x for x in R["procedure"]["folded"] if x["n_items"] >= 2)]
    A(md_table(["#", "what 종류", "what", "site", "technique", "항목 수", "접힌 분류 항목(전부)"], rows) if rows else f"(없음 — 접힌 분류 항목 0. v2.4 {g('catalog_tuples_with_2plus_items')} 과 같다)")
    A("")
    A("#### 9.5.3 항목 하나짜리 튜플 (접히지 않은 것 전부 · v2.4 와 동일 규칙 + v3 stopwords/layer/회사 괄호)")
    A("")
    rows = []
    for i, f in enumerate(x for x in R["procedure"]["folded"] if x["n_items"] == 1):
        r = cat.get(tuple(f["keys"][0]))
        ex = ""
        if r:
            ex = "; ".join(x for x in [("P:" + ",".join(r.get("extra_primaries") or [])) if r.get("extra_primaries") else "", ("S:" + ",".join(r.get("extra_sites") or [])) if r.get("extra_sites") else "", ("Q:" + ",".join(r.get("qualifier_text") or [])) if r.get("qualifier_text") else "", ("L:" + ",".join(r.get("layer_fragments") or [])) if r.get("layer_fragments") else ""] if x)
        rows.append((i + 1, f["what_kind"], f["what"], f["site"] or "none", f"{f['technique'] or 'none'}", f["status"], f["items"][0], ", ".join(f["unregistered"]) or "—", ex or "—"))
    A(md_table(["#", "what 종류", "what", "site", "technique", "상태", "분류 항목", "미등록 조각(candidate_name)", "extra(실값 · P=primary S=site Q=stopword L=layer)"], rows))
    A("")
    A("#### 9.5.4 참조 자리 전부(②) + market-pricing(③) → 튜플 (v3: multi_tuple(부위 여럿) · member_mode · alternatives · qualifier_text · 원장 2판)")
    A("")
    rows = []
    v24slots = g("reference_slots", {})

    def srow(name, v, w):
        return (name, v["n"], v["tuple"], v["multi_tuple"], v["combo_ref"], f"{v['node']}" + (f"({_kv(v['node_by_kind'])})" if v["node"] else ""), v["unresolved"], _kv(v["unresolved_by_reason"]) or "—", v["none"], v["distinct_tuples"], v["new_tuples_not_from_catalog"],
                _kv(v["member_mode"]) or "—", v["with_alternatives"], v["with_qualifier_text"], v["with_session_index"], (f"{w['tuple']}/{w['combo_ref']}/{w['unresolved']}/{w['distinct_tuples']}" if w else "—"))
    for k, v in s["reference_slots"].items():
        rows.append(srow(k, v, v24slots.get(k)))
    rows.append(srow("**② 합계**", s["reference_total"], g("reference_total", None)))
    rows.append(srow("**③ market-pricing.items[].name (122)**", s["market_pricing"], g("market_pricing", None)))
    A(md_table(["참조 자리", "건", "튜플", "multi_tuple(v3)", "combo_ref", "node", "미해결(⑨)", "미해결 사유", "튜플 불가", "distinct 튜플", "①에 없는 새 튜플", "member_mode", "alternatives", "qualifier_text", "session_index", "v2.4 튜플/combo/미해결/distinct"], rows))
    A("")
    A(f"②·③ 튜플의 what 종류: ② {_kv(s['reference_total']['by_what_kind'])} · ③ {_kv(s['market_pricing']['by_what_kind'])}. 코드 참조 {s['code_references_node']} 건은 노드 끝(v2.3).")
    A("")
    A("참조 행 전부 (라벨 → 결과 · [and]/[or] = member_mode · {…} = alternatives · «…» = qualifier_text):")
    A("")
    for k, rows_ in list(R["procedure"]["references"].items()) + [("market-pricing.items[].name (122)", R["procedure"]["market_pricing"])]:
        parts = []
        for r in rows_:
            lab = f"`{r['label']}`" + (f"@{r['hint']}" if r.get("hint") else "")
            tail = (f" {{{', '.join(a['text'] for a in r['alternatives'])}}}" if r.get("alternatives") else "") + (f" «{', '.join(r['qualifier_text'])}»" if r.get("qualifier_text") else "") + (f" 회차{r['session_index']}" if r.get("session_index") is not None else "")
            if r["result"] == "tuple":
                parts.append(lab + f" → ({_fmt_tuple(TT, r['procedure_id'])})" + (f"[{r['member_mode']}]" if r.get("member_mode") else "") + tail)
            elif r["result"] == "multi_tuple":
                parts.append(lab + " → 튜플 여럿[and](" + " + ".join(_fmt_tuple(TT, m) for m in r["member_ids"]) + ")" + tail)
            elif r["result"] == "combo_ref":
                parts.append(lab + f" → combo_ref[{r.get('member_mode')}](" + " + ".join(_fmt_tuple(TT, m) for m in r["member_ids"]) + ")" + tail)
            elif r["result"] == "node":
                parts.append(lab + f" → node:{r['end_kind']}")
            elif r["result"] == "unresolved":
                if r["unresolved_reason"] == "unregistered":
                    parts.append(lab + f" → 미해결 미등록[{','.join(r['unregistered'])}]" + tail)
                else:
                    parts.append(lab + f" → 미해결 {r['unresolved_reason']}[{','.join(str(x) for x in (r.get('detail') or []))}]" + tail)
            else:
                parts.append(lab + " → 튜플 불가" + tail)
        A(f"- **{k}**: " + " · ".join(parts))
    A("")
    A("#### 9.5.5 튜플 전체 집계 (① ② ③ 합집합 · v2.4 → v3)")
    A("")
    A(md_table(["항목", "v2.4", "v3"], [
        ("튜플 수", f"**{g('tuples_total')}**", f"**{s['tuples_total']}**"),
        ("원천별", _kv(g("tuples_by_origin", {})), _kv(s["tuples_by_origin"])),
        ("what 종류", _kv(g("tuples_by_what_kind", {})), _kv(s["tuples_by_what_kind"])),
        ("상태", _kv(g("tuples_status", {})), _kv(s["tuples_status"])),
        ("site none 비율", g("tuples_site_none_ratio"), f"{s['tuples_site_none_ratio']} (what 이 사전 값인 튜플만: {s['tuples_dict_what_site_none_ratio']})"),
        ("site kind 분포(v3)", "—", _kv(s["tuples_site_by_kind"]) + f" · layer 가 시술 site 칸에 들어간 튜플 {s['tuples_layer_site']}"),
        ("technique none 비율", f"{g('tuples_technique_none_ratio')} · 출처 " + _kv(g("tuples_technique_origin", {})), f"{s['tuples_technique_none_ratio']} · 출처 " + _kv(s["tuples_technique_origin"])),
        ("세 칸 전부 사전 값 튜플 / anchor 튜플", f"{g('tuples_all_dict_values')} / {g('tuples_anchored')}", f"{s['tuples_all_dict_values']} / {s['tuples_anchored']}"),
        ("서로 다른 anchor(항목·참조)가 둘 이상 들어간 튜플", g("tuples_with_2plus_anchors"), f"{s['tuples_with_2plus_anchors']} (그중 미상 칸 있는 것 {s['tuples_with_2plus_anchors_not_all_dict']})"),
        ("미등록 조각", f"distinct {g('unregistered_distinct')} · 총 {g('unregistered_total')}", f"distinct {s['unregistered_distinct']} · 총 {s['unregistered_total']} (stopwords 적용 후 · 전후는 §9.5.10)"),
    ]))
    A("")
    A("#### 9.5.6 R5 계열 기법 → 결정 kind `canonical_mapping` 후보 (적용하지 않음 · v3(V3-8): 하위분류 단위 scope)")
    A("")
    A("R5 계열 → 기법이 하나인 계열(procedure-profiles mechanism[]). 튜플에 붙이지 않는다. v3: from_ref 는 R5:<계열> 또는 R5:<하위분류 id>, scope 는 그 아래 CAT- 목록(`erd-v3-tuples.json → procedure.inheritance_candidates[].by_subcategory[].scope`). 섞인 계열은 하위분류별·항목별 지정.")
    A("")
    rows = []
    for i, c in enumerate(R["procedure"]["inheritance_candidates"]):
        rows.append((i + 1, c["from_ref"], c["to_technique"], c["to_id"], c["tuples"], c["catalog_items"], " · ".join(f"{b['from_ref']}({b['label']} · {b['catalog_items']})" for b in c["by_subcategory"])))
    A(md_table(["#", "from_ref(계열)", "to (기법)", "to_id", "technique none 튜플", "scope(분류 항목 수)", "하위분류별 from_ref(scope 수)"], rows))
    A("")
    A(f"후보 불가 계열(R5 기법 둘 이상 또는 없음 — 하위분류별·항목별 지정 대상): {', '.join(s['families_without_single_technique'])}.")
    A("")
    A(md_table(["계열", "R5 기법(procedure-profiles)", "하위분류(항목 수)"], [(m["family"], ", ".join(m["techniques"]) or "(없음)", " · ".join(f"{x['subcategory']} {x['label']}({x['catalog_items']})" for x in m["subcategories"])) for m in s["families_mixed_detail"]]))
    A("")
    A(f"#### 9.5.7 미등록 조각 상위 30 (v2.4 distinct {g('unregistered_distinct')}/총 {g('unregistered_total')} → v3 distinct {s['unregistered_distinct']}/총 {s['unregistered_total']} — stopwords(V3-3)가 뗀 만큼 줄었다 · 사전은 조직층 5 값 외 바뀌지 않았다)")
    A("")
    A("- 전체: " + " · ".join(f"`{f}`×{n}" for f, n in s["unregistered_top30"]))
    for k, v in s["unregistered_top30_by_origin"].items():
        A(f"- {k}: " + (" · ".join(f"`{f}`×{n}" for f, n in v) or "—"))
    A("")
    A("#### 9.5.8 엣지 자리별 끝 분포 (v2.3 규칙 그대로 · v3: multi_tuple 끝 · member_mode)")
    A("")
    rows = []
    for r in R["procedure"]["edge_ends"]:
        rows.append((r["relation"], r["kind"], r["slot"], r["n"], r["procedure"], r["modality"], r["subcategory"], r["product"], r["unresolved"], r["procedure_anchored"] if r["procedure_anchored"] is not None else "—", r["via_catalog_item"], r["member_mode_and"], r["member_mode_or"], r["multi_tuple"], r["note"]))
    tot = s["edge_ends_total"]
    rows.append(("**합계(③ 제외)**", "", "", s["edge_ends_total_n"], tot.get("procedure", 0), tot.get("modality", 0), tot.get("subcategory", 0), tot.get("product", 0), tot.get("unresolved", 0), "", "", s["edge_ends_member_mode"]["and"], s["edge_ends_member_mode"]["or"], s["edge_ends_multi_tuple"], ""))
    A(md_table(["관계", "자리 종류", "자리", "건", "procedure", "modality", "subcategory", "product", "unresolved", "anchor 튜플", "via 항목", "and", "or", "multi_tuple", "비고"], rows))
    A("")
    A("관계별 합계: " + " · ".join(f"**{k}** {_kv({kk: vv for kk, vv in v.items() if kk != 'n'})} (건 {v['n']})" for k, v in s["edge_ends_by_relation"].items()))
    A("")
    # ---- V3-2
    cp = s["company_paren"]
    A("#### 9.5.9 괄호 안 회사·제품 규칙 실측 (V3-2) — 괄호 안 조각 하나짜리 전수(참조 자리 ②③ + 분류 항목 ① + 속성 문장)")
    A("")
    A(f"- 후보 {cp['candidates']} · 회사 사전에 닿음 **{cp['touch_manufacturer']}** · 제품 사전에 닿음 **{cp['touch_product']}** · 어느 쪽에도 안 닿음 {cp['no_touch']} · 규칙 적용(what 이 바뀜) **{cp['applied_n']}** · company_product 모호 {cp['ambiguous_company_product']}.")
    A(f"- 「보톡스(엘러간)」·「더모톡신」 자리 {len(cp['botox_allergan_sites'])}: " + " · ".join(f"[{c['where'][:40]}] 「{c['text'][:40]}」 inner=`{c['inner']}` → {c['touches']}" for c in cp["botox_allergan_sites"]))
    A("- 「엘러간」은 회사 사전 정준값 「앨러간/애브비」와 정규화 일치하지 않는다(앨≠엘) — 회사 동의어 dictionary_add 뒤에 규칙이 적용된다(규칙은 데이터로 있고 사전 값은 결정 · §12).")
    if cp["applied"]:
        A("- 적용된 것 전부: " + " · ".join(f"「{a['label']}」→ {a['company'] or '제품'} → {a['product']}[{a['family']}]" for a in cp["applied"]))
    A("- 안 닿은 inner 조각 상위: " + " · ".join(f"`{f}`×{n}" for f, n in cp["unregistered_inner_top"]))
    A("")
    A(md_table(["#", "자리", "라벨", "괄호 안", "닿음", "회사", "제품"], [(i + 1, c["where"][:45], c["text"][:60], c["inner"], c["touches"], c["manufacturer"] or "—", c["product"] or "—") for i, c in enumerate(c_ for c_ in cp["candidates_all"] if c_["touches"] != "-")]) if any(c["touches"] != "-" for c in cp["candidates_all"]) else "(회사·제품 사전에 닿은 괄호 안 조각 0)")
    A("")
    # ---- V3-3
    st = s["stopwords"]
    A("#### 9.5.10 stopwords 실측 (V3-3) — 단어마다 locator · 적용 전후 미등록 조각")
    A("")
    A(f"- 미등록 조각 **전** distinct {st['unregistered_distinct_before']} · 총 {st['unregistered_total_before']} → **후** distinct {st['unregistered_distinct_after']} · 총 {st['unregistered_total_after']}. 단어 {st['words_total']} 중 원장 locator 가 있는 단어 **{st['words_with_locator']}**. stopwords 만으로 결과(튜플/미해결)가 바뀐 참조 {len(st['references_changed'])}(새로 튜플이 된 참조 {st['references_resolved_newly']} — 수식어를 떼도 남는 조각이 있으면 여전히 ⑨).")
    A("")
    A(md_table(["단어", "출처", "토큰 적중", "미등록(전→후)", "사전 값과 겹침", "locator(실측 · 최대 12)"], [(w["word"], w["origin"], w["hits"], f"{w['unregistered_before']}→{w['unregistered_after']}", "○" if w["in_dictionary"] else "", " · ".join(f"`{x}`" for x in w["locators"]) or "—") for w in st["words"]]))
    A("")
    if st["references_changed"]:
        A("결과가 바뀐 참조 전부:")
        A("")
        A(md_table(["라벨", "힌트", "전", "후", "qualifier_text"], [(x["label"], x["hint"] or "—", x["before"], x["after"], ", ".join(x["qualifier_text"] or [])) for x in st["references_changed"]]))
        A("")
    # ---- V3-4
    A("#### 9.5.11 `+`/`/` 규칙 실측 (V3-4) — 조합 기호가 든 라벨 전수(참조 자리 ②③ + 분류 항목 ①) · 2판 `+` 4곳은 1판 이름을 함께")
    A("")
    A(f"- 라벨 {s['combo_labels']} · 결과 분포: {_kv(s['combo_by_result'])} · member_mode {_kv(s['combo_member_mode'])} · 「무엇을 하나 × 부위 여럿」 {len(s['multi_tuples'])} · 괄호 안 대안 {len(s['alternatives'])}.")
    A("- 2B 12건의 목록 파일은 읽기 범위 밖(silver-v3/decisions)이라 그 12 를 따로 고르지 않고 treatment-optimization·treatment-sequence 를 포함한 **전수**를 아래 표로 보인다(12 는 이 안에 있다). 2판 `+` 4곳은 v1_name 열에 1판 이름.")
    A("")
    A(md_table(["#", "자리", "라벨(2판)", "1판 이름", "기호", "결과", "사유/미등록", "member_mode", "부위", "alternatives", "튜플", "qualifier_text"],
               [(i + 1, c["slot"][:40], c["label"], c["v1_name"] or "—", "".join(c["symbols"]), c["result"], (c["reason"] or "") + (("[" + ",".join(c["unregistered"]) + "]") if c["unregistered"] else "") + (("[" + ",".join(str(x) for x in c["detail"]) + "]") if c.get("detail") and not c["unregistered"] else ""),
                 c["member_mode"] or "—", ", ".join(c["sites"] or []) or "—", ", ".join(c["alternatives"] or []) or "—", " + ".join(c["tuples"]) or "—", ", ".join(c["qualifier_text"] or []) or "—") for i, c in enumerate(s["combo_labels_all"])]))
    A("")
    A("2판 `+` 4곳(1판 `/` → `+`)의 규칙만으로의 결과:")
    A("")
    A(md_table(["라벨(2판)", "1판", "v3 결과", "튜플", "비고"], [(c["label"], c["v1_name"], c["result"] + (":" + (c["reason"] or "") if c["reason"] else ""), " + ".join(c["tuples"]) or "—", ("같은 what 의 튜플 " + str(len(c["tuples"])) + " · R12 member_mode and") if c["result"] == "multi_tuple" else "조각 미등록(" + ",".join(c["unregistered"]) + ") → 규칙이 사전 값을 만들지 않는다 · dictionary_add 뒤") for c in s["combo_plus_v2"]]))
    A("")
    if s["v24_reference_changes"]:
        A("v2.4 와 결과가 다른 참조 전부(원인 열 = 어느 변경이 바꿨나):")
        A("")
        A(md_table(["자리", "라벨", "힌트", "v2.4", "v3", "원인"], [(x["slot"][:40], x["label"], x["hint"] or "—", x["v24"], x["v3"], x["why"]) for x in s["v24_reference_changes"]]))
    return "\n".join(o)


def adverse_md(R, v24a=None):
    s = R["adverse"]["summary"]
    v24a = v24a or load_v24_summary()[1] or {}
    g = lambda k, d="—": v24a.get(k, d)  # noqa
    o = []
    A = o.append
    A("#### 9.6.1 complications 65 → 튜플 (v2.4 → v3 나란히 · 수식 칸 포함)")
    A("")
    A(md_table(["항목", "v2.4", "v3"], [
        ("이름", g("complications_names"), s["complications_names"]), ("튜플이 생긴 이름", g("complications_names_with_tuple"), s["complications_names_with_tuple"]),
        ("튜플이 안 생긴 이름(사건 조각 없음)", "; ".join(g("complications_names_without_tuple", [])) or "0", "; ".join(s["complications_names_without_tuple"]) or "0"),
        ("raw_name 튜플이 된 이름(이름마다 고유)", f"**{g('complications_names_raw')}**", f"**{s['complications_names_raw']}** (사유 {_kv(s['complications_names_raw_by_reason'])} · 사전 튜플 이름 {s['complications_names_dict']})"),
        ("사건이 둘 이상인 이름(튜플 둘 이상)", g("complications_names_multi_tuple"), s["complications_names_multi_tuple"]),
        ("튜플 수(distinct)", f"**{g('complications_distinct_tuples')}** (사전 {g('complications_distinct_tuples_dict')} + raw_name {g('complications_distinct_tuples_raw')})", f"**{s['complications_distinct_tuples']}** (사전 {s['complications_distinct_tuples_dict']} + raw_name {s['complications_distinct_tuples_raw']} · 비율 {s['complications_fold_ratio']})"),
        ("둘 이상 이름이 접힌 튜플", f"{g('complications_tuples_with_2plus_names')}", f"{s['complications_tuples_with_2plus_names']} (전부 사전 값·미등록 0: {s['complications_folded_all_dict_values']} · 미등록 섞임 **{s['complications_folded_with_unregistered']}**)"),
        ("경과", _kv(g("complications_by_course", {})), _kv(s["complications_by_course"])),
        ("부위", _kv(g("complications_by_site_kind", {})), _kv(s["complications_by_site_kind"])),
        ("수식 칸(v3)", "—", _kv(s["complications_by_qualifier"])),
        ("분류", _kv(g("complications_by_category", {})), _kv(s["complications_by_category"])),
        ("사건 사전 최종 값", f"**{g('event_dictionary_values')}**", f"**{s['event_dictionary_values']}** (안 쓰인 값: {', '.join(s['event_dictionary_unused']) or '없음'})"),
        ("경과 · 상대 부위 · 수식(v3) · 부위 사전 값", f"{g('course_dictionary_values')} · {g('relative_site_values')} · — · 21", f"{s['course_dictionary_values']} · {s['relative_site_values']} · {s['qualifier_dictionary_values']} · {s['site_dictionary_values']}({_kv(s['site_dictionary_by_kind'])})"),
    ]))
    A("")
    A("#### 9.6.2 65 가 접힌 결과 — 튜플마다 어떤 이름들이 갔는지 전부 (v3 재실측 · 수식 칸 열)")
    A("")
    rows = [(i + 1, f["event_kind"], f["category"] or "—", f["event"] if f["event_kind"] == "dict" else f"(raw) {f['event']}", f"{f['site'] or 'none'}({f['site_kind']}{(':' + f['site_dict_kind']) if f.get('site_dict_kind') else ''})", f["course"], f["qualifier"] or "none", f["n_names"], " · ".join(f["names"]),
             ", ".join(f["unregistered"]) or "—",
             ((" + ".join(f"({t[0]}, {t[1] or 'none'}, {t[2]}, {t[3] or 'none'})" for t in (f["dict_tuples"] or [])) or "(사건 조각 없음)") if f["event_kind"] == "raw_name" else "—") + (f" / S:{','.join(f['extra_sites'])}" if f["extra_sites"] else "") + (f" / C:{','.join(f['extra_courses'])}" if f["extra_courses"] else "") + (f" / Q:{','.join(f['extra_qualifiers'])}" if f["extra_qualifiers"] else ""))
            for i, f in enumerate(R["adverse"]["folded"])]
    A(md_table(["#", "event_kind", "분류", "event", "site", "course", "qualifier", "이름 수", "접힌 complications 이름(전부)", "미등록 조각", "raw_name 의 사전 분해(dict_tuples · 보존만) / extra"], rows))
    A("")
    A("#### 9.6.2a 경과 규칙 실측 (사건에 바로 붙은 수식어만 · v2.3 그대로)")
    A("")
    A(md_table(["#", "이름", "event_kind", "사전 분해 (event, site, course)"], [(i + 1, x["name"], x["event_kind"], " + ".join(f"({t[0]}, {t[1] or 'none'}, {t[2]})" for t in x["tuples"])) for i, x in enumerate(s["course_split_examples"])]))
    A("")
    for x in s["lop"]:
        A(f"- LOP: 「{x['name']}」 → event_kind={x['event_kind']} · 튜플 칸 {[t for t in x['tuples']]} · 사전 분해 {' + '.join('(%s, %s, %s, %s)' % (t[0], t[1] or 'none', t[2], t[3] or 'none') for t in x['dict_tuples'])}")
    A("")
    A("#### 9.6.2b 부위 규칙 실측 (v2.4 수정 1 그대로 · 원칙 B·C)")
    A("")
    A(f"- 사건 멤버 밖(같은 묶음 · outer · 이름 전체)에서 온 site 가 들어간 튜플·후보 **{s['site_outside_member']}** · 「두통 × 주사 부위」류 틀린 조합: 튜플·후보 **{s['headache_x_injection_site']}** · 부위 나열 합치기 {s['site_list_merges']} · 후보 둘 이상 분할 {s['multi_candidate_splits']} · 붙지 않은 조각 보존 {s['unattached_fragments_texts']} 문자열(부위·경과·수식). v3: 조직층 값(피부·혈관 …)이 site 사전에 들어와 「시술 부위 피부 발적」처럼 부위 후보가 둘이 되는 표현이 생긴다(원칙 B · 후보마다).")
    for m in s["multi_candidate_splits_all"]:
        A(f"  - [{m['kind']}] 「{m['text']}」 → " + " + ".join(f"({t[0]}, {t[1] or 'none'}, {t[2]}, {t[3] or 'none'})" for t in m["tuples"]) + f" (부위 후보 {m['site_candidates']} · 경과 후보 {m['course_candidates']} · 수식 후보 {m['qualifier_candidates']})")
    A("")
    A("#### 9.6.2c raw_name 칸 실측 (v2.4 수정 2 그대로 + 수식 칸)")
    A("")
    rc = s["raw_cells"]
    A(f"- raw_name 튜플 {rc['n']}: site none **{rc['site_none']}/{rc['n']}** · course 미상 **{rc['course_unknown']}/{rc['n']}** · qualifier none **{rc['qualifier_none']}/{rc['n']}** · 사유 {_kv(rc['by_reason'])} · dict_tuples 보존 {rc['with_dict_tuples']} · extra_sites {rc['with_extra_sites']} · extra_courses {rc['with_extra_courses']} · extra_qualifiers {rc['with_extra_qualifiers']}")
    A("")
    A("#### 9.6.3 표현(adverse_expression) → 단위 (exact / unlinked · v2.4 와 나란히)")
    A("")
    rows = [(k, v["n"], v["linked"], v["unlinked"], _kv(v["unlinked_reasons"]), v["distinct_tuples"], v["new_tuples_not_from_complications"], v["candidate_units_not_existing"]) for k, v in s["expressions"].items()]
    t = s["expressions_total"]
    rows.append(("**합계**", t["n"], t["linked"], t["unlinked"], _kv(t["unlinked_reasons"]), "", s["expressions_new_tuples"], s["candidate_units_not_existing"]))
    A(md_table(["kind", "표현 수", "exact(R29)", "unlinked", "unlinked 사유(중복 셈)", "distinct 튜플(기존 단위)", "65 에 없던 새 튜플", "기존 단위에 없는 후보 단위(distinct)"], rows))
    A("")
    ge = g("expressions_total", {})
    A(f"- v2.4: exact {ge.get('linked')}/{ge.get('n')} → v3 exact {t['linked']}/{t['n']} · unlinked {t['unlinked']} · partial 인데 연결된 표현 **{s['expressions_partial_linked']}** · 표현이 만든 튜플 {s['expressions_new_tuples']}.")
    A(f"- 문헌 32: " + ", ".join(f"{k}={v}" for k, v in s["literature_basis"].items()))
    A("")
    A("#### 9.6.4 튜플 전체 집계 (65 유래뿐 · v2.4 → v3)")
    A("")
    A(md_table(["항목", "v2.4", "v3"], [
        ("튜플 수", f"**{g('tuples_total')}**", f"**{s['tuples_total']}** (사전 {s['tuples_dict']} + raw_name {s['tuples_raw_name']})"),
        ("원천별", _kv(g("tuples_by_origin", {})), _kv(s["tuples_by_origin"])),
        ("상태", _kv(g("tuples_status", {})), _kv(s["tuples_status"])), ("경과", _kv(g("tuples_by_course", {})), _kv(s["tuples_by_course"])),
        ("부위", _kv(g("tuples_by_site_kind", {})), _kv(s["tuples_by_site_kind"])), ("수식 칸(v3)", "—", _kv(s["tuples_by_qualifier"])), ("분류", _kv(g("tuples_by_category", {})), _kv(s["tuples_by_category"])),
        ("미등록 조각", f"distinct {g('unregistered_distinct')} · 총 {g('unregistered_total')}", f"distinct {s['unregistered_distinct']} · 총 {s['unregistered_total']}"),
    ]))
    A("")
    A(f"표현에서 새로 생긴 튜플: **{s['expressions_new_tuples']}**. 기존 단위에 없는 후보 단위 {s['candidate_units_not_existing']} 중 상위 40:")
    A("")
    A(md_table(["#", "event", "site", "course", "qualifier", "표현 수", "kind"], [(i + 1, c["event"], f"{c['site'] or 'none'}({c['site_kind']})", c["course"], c["qualifier"] or "none", c["expressions"], _kv(c["kinds"])) for i, c in enumerate(s["candidate_units_not_existing_all"][:40])]))
    A("")
    A("#### 9.6.5 미등록 조각 전부 (출처별 · 횟수)")
    A("")
    for k, v in s["unregistered_by_origin"].items():
        A(f"- **{k}** ({len(v)}): " + " · ".join(f"`{f}`×{n}" for f, n in v))
    A("")
    A("#### 9.6.6 미등록 조각 있는 이름이 접혔는가 — v3 재실측")
    A("")
    A(f"- 둘 이상 이름이 접힌 부작용 튜플 {s['folded_with_2plus_names']} 중 미등록 조각 있는 이름이 섞인 튜플 **{s['folded_with_partial_name']}**. raw_name 튜플 {s['complications_distinct_tuples_raw']} 은 전부 이름 하나씩 · 칸은 none/미상/none.")
    A("")
    # ---- V3-1
    A("#### 9.6.7 수식 칸(qualifier) 실측 (V3-1) — 수식 조각이 생기는 이름·표현 전부 · v2.4 접힘·exact 대조")
    A("")
    A(f"- 수식 사전 값 {s['qualifier_dictionary_values']}(공기 · 필러 · 지방 · 혈전 — 물질 / 역행성 — 기전). 수식 조각이 든 complications 이름 **{s['qualifier_names']}** · 표현(+patient_ko) **{s['qualifier_expressions']}** · 수식 칸이 none 이 아닌 튜플 **{s['qualifier_tuples']}** · 접두 가름(prefix_split) {len(s['prefix_splits'])}: " + " · ".join(f"「{a}」→ {b} + {c}" for a, b, c in s["prefix_splits"]))
    A("")
    A("수식 조각이 든 complications 이름 전부:")
    A("")
    A(md_table(["#", "이름", "계열", "event_kind", "사전 분해 (event, site, course, qualifier)", "붙지 않은 수식"], [(i + 1, q["text"], q["modality"], q["event_kind"], " + ".join(f"({t[0]}, {t[1] or 'none'}, {t[2]}, {t[3] or 'none'})" for t in q["dict_tuples"]), ", ".join(q["extra_qualifiers"]) or "—") for i, q in enumerate(s["qualifier_names_all"])]))
    A("")
    A("수식 조각이 든 표현 전부(원문 · 후보 네 칸 · exists):")
    A("")
    A(md_table(["#", "kind", "출처", "원문", "후보(수식 있는 것)", "붙지 않은 수식", "match"], [(i + 1, q["kind"], (q["origin"] or "")[:28], q["text"][:70], " + ".join(f"({a}, {b or 'none'}, {c}, {d}{'·있음' if e else '·없음'})" for a, b, c, d, e in q["candidates"]) or "—", ", ".join(q["extra_qualifiers"]) or "—", q["match_status"] or "—") for i, q in enumerate(s["qualifier_expressions_all"])]))
    A("")
    A("수식 칸이 none 이 아닌 튜플 전부:")
    A("")
    A(md_table(["#", "id", "event", "site", "course", "qualifier", "event_kind", "basis", "출처 수"], [(i + 1, q["id"], q["event"], q["site"] or "none", q["course"], q["qualifier"], q["event_kind"], q["basis"] or "—", q["sources"]) for i, q in enumerate(s["qualifier_tuples_all"])]) if s["qualifier_tuples_all"] else "(없음 — 65 이름 중 수식 조각이 사건과 같은 멤버에 있으면서 미등록 0 인 이름이 없다 · 「공기색전·카테터 관련 감염」은 raw_name 이며 dict_tuples 에 (색전, none, 미상, 공기) 보존)")
    A("")
    c = s.get("v24_comparison") or {}
    if c:
        A(f"- **v2.4 대조**: 사전 튜플 접힘 그룹(이름 집합) v2.4 {c['dict_fold_groups_v24']} = v3 {c['dict_fold_groups_v3']} · 같음 **{c['dict_fold_groups_same']}**(다른 그룹 {len(c['fold_group_diff'])}) · raw_name 이름 {c['raw_names_v24']} = {c['raw_names_v3']} 같음 {c['raw_names_same']} · exact {c['exact_v24']} → {c['exact_v3']} · match_status 가 바뀐 표현 **{len(c['match_status_diff'])}** · 연결 단위(세 칸)가 바뀐 exact 표현 **{len(c['linked_units_diff'])}** · 튜플 수 {c['tuples_v24']} → {c['tuples_v3']}. {c['tuple_ids_changed']}.")
        if c["fold_group_diff"]:
            A("  - 다른 접힘 그룹: " + " · ".join(str(x) for x in c["fold_group_diff"]))
        if c["match_status_diff"]:
            A("  - match_status 가 바뀐 표현: " + " · ".join(f"{k}: {a}→{b}" for k, a, b in c["match_status_diff"][:20]))
    A("")
    # ---- V3-5
    A("#### 9.6.8 조직층 부위 실측 (V3-5) — layer 값이 붙은 튜플·후보·조각")
    A("")
    A(f"- 부위 사전 {s['site_dictionary_values']}({_kv(s['site_dictionary_by_kind'])}) · layer site 가 든 튜플 **{s['layer_site_tuples']}** · 후보 {s['layer_site_candidates']} · 붙지 않은 layer 조각(extra_sites) {s['layer_site_extra']}. 「피부 괴사」「지방괴사」는 사건 사전 동의어(통째 일치)라 자동으로 (괴사, 피부)·(괴사, 피하 지방층)이 되지 않는다 — adverse_tuple_assign(§12).")
    if s["layer_site_tuples_all"]:
        A("  - 튜플: " + " · ".join(f"({t['event']}, {t['site']}, {t['course']})" for t in s["layer_site_tuples_all"]))
    if s["layer_site_candidates_all"]:
        A("  - 후보(원문 · event · site · exists): " + " · ".join(f"「{a}」({b}, {c}, {'있음' if d else '없음'})" for a, b, c, d in s["layer_site_candidates_all"]))
    if s["layer_site_extra_all"]:
        A("  - 붙지 않은 layer 조각: " + " · ".join(f"「{a}」{b}" for a, b in s["layer_site_extra_all"]))
    return "\n".join(o)


def load_all():
    for name in ("erd-v3-dictionaries.json", "erd-v2.4-dictionaries.json"):
        if os.path.exists(os.path.join(HERE, name)):
            dic = json.load(open(os.path.join(HERE, name), encoding="utf-8"))
            break
    try:
        erd = json.load(open(os.path.join(HERE, "erd-v3.json"), encoding="utf-8"))
        rules, rrules = erd["tuple_rules"], erd["resolve_rules"]
    except (FileNotFoundError, KeyError):
        sys.path.insert(0, HERE)
        import erd_spec_v3
        rules, rrules = erd_spec_v3.TUPLE_RULES, erd_spec_v3.RESOLVE_RULES
    files = [f for f in os.listdir(LEDGER) if f.endswith(".json")]
    L = {f: json.load(open(os.path.join(LEDGER, f), encoding="utf-8")) for f in files}
    v24 = None
    if os.path.exists(os.path.join(HERE, "erd-v2.4-tuples.json")):
        v24 = json.load(open(os.path.join(HERE, "erd-v2.4-tuples.json"), encoding="utf-8"))
    return dic, rules, rrules, L, v24


def main():
    dic, rules, rrules, L, v24 = load_all()
    bc = bronze_check(LEDGER)
    assert bc["hashes_file"] and not bc["mismatch"], f"브론즈 2판 해시 불일치 {bc}"
    R = run_all(dic, rules, L, rrules, v24)
    R["procedure"]["v21_none_fold_split"] = v21_split(R)
    print(procedure_md(R))
    print()
    print(adverse_md(R))
    json.dump(R, open(os.path.join(HERE, "erd-v3-tuples.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    print("\n→ erd-v3-tuples.json")


if __name__ == "__main__":
    main()
