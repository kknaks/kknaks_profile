#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ERD v2 — 튜플 분해 실측기 (구조 변경 ①②). 독립 실행.

입력(같은 폴더): erd-v2-dictionaries.json(사전 46: 부위·기법·제품명·하위분류 라벨·분류 항목 이름 색인·사건·경과·상대 부위) ·
      erd-v2.json(tuple_rules — 없으면 erd_spec_v2.TUPLE_RULES) · erd-v1.1-resolve.py(v1.1 분해기: Lexicon·Resolver·slot_items 재사용) ·
      원장 21(/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26)
출력: 표준 출력에 §9.5/§9.6 표 + erd-v2-tuples.json(튜플 전부 · 접힌 결과 전부 · 미등록 조각 전부)

규칙은 전부 데이터(erd-v2.json → tuple_rules)다. 유사도·추측 없음. 사전 값·동의어 추가 없음(미등록은 기록만).
  시술: ① 분류 항목 521 ② 자유 텍스트 참조 자리 전부(v1.1 §9.2) ③ market-pricing 122 → 튜플 (what, site, technique)
  부작용: complications 65 + extracted/taxonomy safety 전 문구 + consent 응급 징후 + 문헌 adverse_effects 32(+patient_ko) + 타임라인 normal/abnormal/caution/emergency → 튜플 (event, site, course)
실행: python3 erd-v2-tuples.py
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
LEDGER = "/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26"
CODE_KEY_RE = re.compile(r"^(?:[A-Z]{1,2}\d+(?:-\d+)*|M\d+_to_M\d+|auto-\d+-\d+)$")


def norm(s):
    if s is None:
        return None
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", str(s)).casefold())


def mkid(prefix, key):
    return f"{prefix}-{hashlib.sha256(norm(key).encode()).hexdigest()[:10]}"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


V11 = load_module("erd_v11_resolve", os.path.join(HERE, "erd-v1.1-resolve.py"))


def with_alias(dic_json):
    """v1.1 Lexicon 은 'procedure_name' 색인을 읽는다 — v2 의 catalog_item_name 을 그 이름으로 비춰 준다(값·순서 동일)."""
    d = dict(dic_json)
    ds = list(d["dictionaries"])
    cat = next(x for x in ds if x["name"] == "catalog_item_name")
    if not any(x["name"] == "procedure_name" for x in ds):
        ds.append(dict(cat, name="procedure_name"))
    d["dictionaries"] = ds
    return d


# ---------------------------------------------------------------------------
# 개체 id (v1.1 식별자 규칙 그대로)
# ---------------------------------------------------------------------------
class Ids:
    def __init__(self, dic_json, L):
        D = {d["name"]: d for d in dic_json["dictionaries"]}
        tx = L["taxonomy.json"]
        self.mod = {m["id"]: {"id": mkid("MOD", m["id"]), "label": m["category"], "family": m["id"]} for m in tx["modality"]}
        self.sub = {}
        self.sub_by_label = defaultdict(list)
        for m in tx["modality"]:
            for sc in m["subcategories"]:
                e = {"id": mkid("SUB", f"{m['id']}|{sc['label']}"), "label": f"{sc['id']} {sc['label']}", "family": m["id"], "code": sc["id"], "raw_label": sc["label"]}
                self.sub[sc["id"]] = e
                self.sub_by_label[(m["id"], norm(sc["label"]))].append(e)
        self.prod = {}
        for e in D["product_name"]["entries"]:
            self.prod[norm(e["canonical"])] = {"id": mkid("PRD", f"{e['code']}|{e['canonical']}"), "label": e["canonical"], "family": e["code"], "code": e["code"]}
        self.site = {}
        for e in D["site"]["entries"]:
            key = e.get("zone_id") if e.get("site_kind") == "backbone" else e["canonical"]
            self.site[norm(e["canonical"])] = {"id": mkid("SIT", key), "label": e["canonical"]}
        self.tech = {norm(e["canonical"]): {"id": e["id"], "label": e["canonical"]} for e in D["technique"]["entries"]}
        self.tech_surface = {}
        for e in D["technique"]["entries"]:
            self.tech_surface[norm(e["canonical"])] = e["canonical"]
            for s in e.get("synonyms", []):
                self.tech_surface[norm(s["value"])] = e["canonical"]
        # R5 계열 → 기법 (procedure-profiles mechanism[])
        self.family_tech = {}
        for pr in L["procedure-profiles.json"]["profiles"]:
            self.family_tech[pr["id"]] = list(dict.fromkeys(pr["mechanism"]))
        self.event = {}
        self.event_surface = {}
        for e in D["adverse_event_type"]["entries"]:
            self.event[norm(e["canonical"])] = {"id": e["id"], "label": e["canonical"], "category": e.get("category")}
            self.event_surface[norm(e["canonical"])] = e["canonical"]
            for s in e.get("synonyms", []):
                self.event_surface[norm(s["value"])] = e["canonical"]
        self.course = {}
        self.course_surface = {}
        for e in D["course"]["entries"]:
            self.course[norm(e["canonical"])] = {"id": e["id"], "label": e["canonical"]}
            self.course_surface[norm(e["canonical"])] = e["canonical"]
            for s in e.get("synonyms", []):
                self.course_surface[norm(s["value"])] = e["canonical"]
        self.rsite = {}
        self.rsite_surface = {}
        for e in D["relative_site"]["entries"]:
            self.rsite[norm(e["canonical"])] = {"id": e["id"], "label": e["canonical"]}
            self.rsite_surface[norm(e["canonical"])] = e["canonical"]
            for s in e.get("synonyms", []):
                self.rsite_surface[norm(s["value"])] = e["canonical"]
        self.site_surface = {}
        for e in D["site"]["entries"]:
            self.site_surface[norm(e["canonical"])] = e["canonical"]
            for s in e.get("synonyms", []):
                self.site_surface[norm(s["value"])] = e["canonical"]

    def inherit_tech(self, family):
        """R5 계열 기법이 하나면 상속, 둘 이상·없음이면 none."""
        if not family or "|" in str(family):
            return None, "none"
        t = self.family_tech.get(family, [])
        if len(t) == 1:
            return t[0], "inherited"
        return None, "none"


# ---------------------------------------------------------------------------
# ① ② ③ 시술 튜플
# ---------------------------------------------------------------------------
class V2Resolver(V11.Resolver):
    """v1.1 Resolver 위에 (a) 자기 이름 제외 (b) 기법 사전 조각 (c) 묶음·멤버 단위 분해."""

    def __init__(self, lex, rules, ids):
        super().__init__(lex, rules)
        self.ids = ids
        self.exclude = None

    def primary(self, text, family, types=None):
        p = super().primary(text, family, types)
        if p and self.exclude and p["kind"] == "procedure" and norm(p["canonical"]) == self.exclude:
            # 자기 이름 — 다른 사전만 다시 본다
            t = text.strip()
            for k in ("product", "modality_subcategory"):
                h = {x for x in self.lex.hits(k, t)}
                if h:
                    hh = {x for x in h if self._in_family(x[0], family)} or h
                    x = sorted(hh, key=lambda z: str(z))[0]
                    return {"kind": k, "text": t, "code": family if (family and family in str(x[0]).split("|")) else x[0], "canonical": x[1], "overlap": None, "cross_family": not self._in_family(x[0], family)}
            return None
        return p

    def classify2(self, frag, family):
        c = self.classify(frag, family)
        if c is None:
            t = norm(frag)
            if t in self.ids.tech_surface:
                return {"kind": "technique", "text": frag.strip(), "canonical": self.ids.tech_surface[t]}
        return c

    def decompose(self, label, family, exclude=None):
        """묶음(outer/inner) → 멤버(조합 기호) → 조각(사전 순서 · 공백 토큰 최장 구간)."""
        self.exclude = exclude
        parens = self.paren_re.findall(label)
        outer = self.paren_re.sub(" ", label)
        groups = []
        for gi, (where, g) in enumerate([("outer", outer)] + [("inner", p) for p in parens]):
            members = []
            for part in self.combo_re.split(g):
                part = part.strip(" ·")
                if not part:
                    continue
                spans, untouched = [], []
                c = self.classify2(part, family)
                if c and c["kind"] != "ambiguous":
                    spans.append(c)
                else:
                    toks = part.split()
                    i = 0
                    while i < len(toks):
                        found = None
                        for j in range(len(toks), i, -1):
                            h = self.classify2(" ".join(toks[i:j]), family)
                            if h and h["kind"] != "ambiguous":
                                found = (h, j)
                                break
                        if found:
                            spans.append(found[0])
                            i = found[1]
                        else:
                            amb = self.classify(toks[i], family)
                            untouched.append({"text": toks[i], "reason": "모호(계열 " + ",".join(amb["codes"]) + ")" if amb and amb["kind"] == "ambiguous" else "사전 없음"})
                            i += 1
                members.append({"text": part, "spans": spans, "untouched": untouched})
            groups.append({"where": where, "members": members})
        self.exclude = None
        return groups


PRIMARY_KINDS = ("modality", "modality_subcategory", "procedure", "product")
WHAT_PREC = {"product": 0, "modality_subcategory": 1, "modality": 2}


class ProcedureTuples:
    def __init__(self, lex, rules, ids, L):
        self.R = V2Resolver(lex, rules, ids)
        self.ids = ids
        self.L = L
        self.tuples = OrderedDict()   # id -> tuple record
        self.catalog = OrderedDict()  # (family, name) -> decomposition record
        self.items = []               # (family, parent_sub_id, name)
        tx = L["taxonomy.json"]
        for m in tx["modality"]:
            for sc in m["subcategories"]:
                for it in sc["items"]:
                    self.items.append((m["id"], sc["id"], it["name"]))
        self.item_index = defaultdict(list)
        for fam, sub, name in self.items:
            self.item_index[norm(name)].append((fam, sub, name))
        self._busy = set()

    # --- 튜플 등록
    def register(self, what_kind, what, site, tech, tech_origin, origin, src, unregistered):
        site_id = site["id"] if site else "none"
        tech_id = self.ids.tech[norm(tech)]["id"] if tech else "none"
        tid = mkid("PRC", f"{what['id']}|{site_id}|{tech_id}")
        t = self.tuples.get(tid)
        if t is None:
            t = {"id": tid, "what_kind": what_kind, "what_id": what["id"], "what_label": what["label"], "family": what.get("family"),
                 "site": site["label"] if site else None, "site_id": site_id, "technique": tech, "technique_id": tech_id, "technique_origin": tech_origin,
                 "origins": [], "status": "complete", "unregistered_fragments": [], "sources": []}
            self.tuples[tid] = t
        if origin not in t["origins"]:
            t["origins"].append(origin)
        if tech_origin == "fragment" and t["technique_origin"] != "fragment":
            t["technique_origin"] = tech_origin
        t["sources"].append(src)
        for u in unregistered:
            if u not in t["unregistered_fragments"]:
                t["unregistered_fragments"].append(u)
        if unregistered:
            t["status"] = "partial"
        return tid

    # --- what 후보 → (what_kind, what record, basis, inherited site/tech from catalog)
    def what_from_span(self, s, family, for_item):
        k = s["kind"]
        if k == "product":
            e = self.ids.prod.get(norm(s["canonical"]))
            return ("product", e, f"product:{s['canonical']}" + ("(타 계열)" if s.get("cross_family") else ""), None, None)
        if k == "modality_subcategory":
            fam = s.get("code")
            cands = self.ids.sub_by_label.get((fam, norm(s["canonical"]))) if fam and "|" not in str(fam) else None
            if not cands:
                # 라벨이 여러 계열(기타·추가)인데 힌트 계열이 없으면 what 으로 못 쓴다
                return None
            if for_item and fam != family:
                return None
            return ("modality_subcategory", cands[0], f"subcategory:{cands[0]['label']}", None, None)
        if k == "procedure":
            fam = s.get("code")
            cands = [x for x in self.item_index.get(norm(s["canonical"]), []) if ("|" not in str(fam) and x[0] == fam) or "|" in str(fam)]
            if not cands:
                cands = self.item_index.get(norm(s["canonical"]), [])
            if not cands:
                return None
            fam2, sub2, name2 = cands[0]
            rec = self.catalog_tuple(fam2, sub2, name2)
            if rec is None:
                return None
            t = self.tuples[rec["procedure_id"]]
            what = {"id": t["what_id"], "label": t["what_label"], "family": t["family"]}
            return (t["what_kind"], what, f"catalog_item:{name2}[{fam2}]→{t['what_kind']}:{t['what_label']}", (t["site"], t["site_id"]), (t["technique"], t["technique_origin"]))
        if k == "modality":
            e = self.ids.mod.get(s.get("code"))
            return ("modality", e, f"modality:{s['canonical']}", None, None) if e else None
        return None

    def assemble(self, groups, family, for_item=False, parent_sub=None, hint_family=None):
        """묶음·멤버 → 조합 판정 → what/site/technique."""
        # 조합: 같은 묶음 안에서 primary 를 가진 멤버가 둘 이상
        combo_members = None
        for g in groups:
            pm = [m for m in g["members"] if any(s["kind"] in PRIMARY_KINDS for s in m["spans"])]
            if len(pm) >= 2:
                combo_members = pm
                break
        all_spans = [s for g in groups for m in g["members"] for s in m["spans"]]
        untouched = [u["text"] for g in groups for m in g["members"] for u in m["untouched"]]
        qualifiers = [(s["kind"], s["canonical"]) for s in all_spans if s["kind"] in ("spec", "product_tier")]
        if combo_members is not None:
            members = []
            for m in combo_members:
                sub = self.assemble([{"where": "member", "members": [m]}], family, for_item, parent_sub, hint_family)
                members.append(sub)
            return {"kind": "combo_ref", "members": members, "untouched": untouched, "qualifiers": qualifiers}
        # what
        cands = []
        for s in all_spans:
            if s["kind"] in PRIMARY_KINDS:
                s2 = s
                if s["kind"] == "modality":
                    ph = self.R.lex.hits("product", s["text"])
                    if ph:  # 계열명 = 제품명(보톡스·필러) → what 은 product
                        hh = {x for x in ph if self.R._in_family(x[0], family)} or ph
                        x = sorted(hh, key=lambda z: str(z))[0]
                        s2 = {"kind": "product", "text": s["text"], "code": x[0], "canonical": x[1], "cross_family": not self.R._in_family(x[0], family)}
                    elif for_item:
                        continue  # ① 분류 항목: 계열 조각은 what 으로 쓰지 않는다(부모 하위분류가 더 구체적)
                w = self.what_from_span(s2, family, for_item)
                if w:
                    cands.append((WHAT_PREC[w[0]], len(cands), w, s2))
        cands.sort(key=lambda x: (x[0], x[1]))
        site_spans = [s for s in all_spans if s["kind"] == "site"]
        tech_spans = [s for s in all_spans if s["kind"] == "technique"]
        inh_site, inh_tech = None, None
        if cands:
            what_kind, what, basis, inh_site, inh_tech = cands[0][2]
            extra = [c[2][2] for c in cands[1:]]
        elif for_item:
            e = self.ids.sub[parent_sub]
            what_kind, what, basis, extra = "modality_subcategory", e, f"parent_subcategory:{e['label']}", []
        elif hint_family and hint_family in self.ids.mod:
            what_kind, what, basis, extra = "modality", self.ids.mod[hint_family], f"hint_family:{hint_family}", []
        else:
            return {"kind": "none", "untouched": untouched, "qualifiers": qualifiers, "reason": "primary 조각도 계열 힌트도 없음"}
        # site
        site = None
        site_basis = None
        if site_spans:
            site = self.ids.site[norm(site_spans[0]["canonical"])]
            site_basis = site_spans[0]["text"]
        elif inh_site and inh_site[1] != "none":
            site = {"id": inh_site[1], "label": inh_site[0]}
            site_basis = f"(분류 항목 상속) {inh_site[0]}"
        extra_sites = [s["canonical"] for s in site_spans[1:]]
        # technique
        if tech_spans:
            tech, tech_origin = tech_spans[0]["canonical"], "fragment"
        elif inh_tech and inh_tech[0]:
            tech, tech_origin = inh_tech
        else:
            tech, tech_origin = self.ids.inherit_tech(what.get("family"))
        return {"kind": "tuple", "what_kind": what_kind, "what": what, "what_basis": basis, "extra_primaries": extra, "site": site, "site_basis": site_basis,
                "extra_sites": extra_sites, "technique": tech, "technique_origin": tech_origin, "untouched": untouched, "qualifiers": qualifiers}

    # --- ① 분류 항목
    def catalog_tuple(self, family, sub, name):
        key = (family, name)
        if key in self.catalog:
            return self.catalog[key]
        if key in self._busy:
            return None
        self._busy.add(key)
        groups = self.R.decompose(name, family, exclude=norm(name))
        a = self.assemble(groups, family, for_item=True, parent_sub=sub)
        rec = {"family": family, "subcategory": sub, "name": name, "groups": [{"where": g["where"], "members": [{"text": m["text"], "spans": [(s["kind"], s["canonical"]) for s in m["spans"]], "untouched": [u["text"] for u in m["untouched"]]} for m in g["members"]]} for g in groups]}
        if a["kind"] == "combo_ref":
            # 분류 항목 자체가 조합이면 멤버 튜플을 만들고 항목은 첫 멤버 튜플로 매단다(패키지 combo_ref 는 참조 쪽 개념) — 항목 수준에서는 표시만
            ids = []
            for m in a["members"]:
                if m["kind"] == "tuple":
                    ids.append(self.register(m["what_kind"], m["what"], m["site"], m["technique"], m["technique_origin"], "catalog_item", {"origin": "catalog_item", "label": name, "family": family}, m["untouched"]))
            rec.update({"result": "combo_ref", "procedure_id": ids[0] if ids else None, "member_ids": ids, "unregistered": a["untouched"], "qualifiers": a["qualifiers"], "what_basis": "combo"})
        elif a["kind"] == "tuple":
            tid = self.register(a["what_kind"], a["what"], a["site"], a["technique"], a["technique_origin"], "catalog_item", {"origin": "catalog_item", "label": name, "family": family}, a["untouched"])
            rec.update({"result": "tuple", "procedure_id": tid, "what_kind": a["what_kind"], "what_basis": a["what_basis"], "extra_primaries": a["extra_primaries"], "site": a["site"]["label"] if a["site"] else None, "site_basis": a["site_basis"],
                        "technique": a["technique"], "technique_origin": a["technique_origin"], "unregistered": a["untouched"], "qualifiers": a["qualifiers"], "status": "partial" if a["untouched"] else "complete"})
        else:
            rec.update({"result": "none", "procedure_id": None, "unregistered": a["untouched"]})
        self.catalog[key] = rec
        self._busy.discard(key)
        return rec

    def run_catalog(self):
        for fam, sub, name in self.items:
            self.catalog_tuple(fam, sub, name)

    # --- ② ③ 참조
    def run_reference(self, label, hint, origin, slot):
        if isinstance(label, str) and label.startswith("__MODALITY__"):
            code = label[12:]
            tech, to = self.ids.inherit_tech(code)
            tid = self.register("modality", self.ids.mod[code], None, tech, to, origin, {"origin": origin, "slot": slot, "label": code, "family": code}, [])
            return {"label": code, "hint": code, "result": "tuple", "procedure_id": tid, "what_basis": "modality_code", "status": "complete", "unregistered": [], "qualifiers": []}
        if isinstance(label, str) and label.startswith("__SUBID__"):
            sid = label[9:]
            e = self.ids.sub[sid]
            tech, to = self.ids.inherit_tech(hint)
            tid = self.register("modality_subcategory", e, None, tech, to, origin, {"origin": origin, "slot": slot, "label": sid, "family": hint}, [])
            return {"label": sid, "hint": hint, "result": "tuple", "procedure_id": tid, "what_basis": "subcategory_id", "status": "complete", "unregistered": [], "qualifiers": []}
        groups = self.R.decompose(str(label), hint)
        a = self.assemble(groups, hint, hint_family=hint)
        base = {"label": label, "hint": hint, "groups": [{"where": g["where"], "members": [{"text": m["text"], "spans": [(s["kind"], s["canonical"]) for s in m["spans"]], "untouched": [u["text"] for u in m["untouched"]]} for m in g["members"]]} for g in groups]}
        if a["kind"] == "combo_ref":
            ids = []
            for m in a["members"]:
                if m["kind"] == "tuple":
                    ids.append(self.register(m["what_kind"], m["what"], m["site"], m["technique"], m["technique_origin"], origin, {"origin": origin, "slot": slot, "label": label, "family": hint, "member": True}, m["untouched"]))
            base.update({"result": "combo_ref", "member_ids": list(dict.fromkeys(ids)), "member_count": len(a["members"]), "unregistered": a["untouched"], "qualifiers": a["qualifiers"], "status": "partial" if a["untouched"] else "complete"})
        elif a["kind"] == "tuple":
            tid = self.register(a["what_kind"], a["what"], a["site"], a["technique"], a["technique_origin"], origin, {"origin": origin, "slot": slot, "label": label, "family": hint}, a["untouched"])
            base.update({"result": "tuple", "procedure_id": tid, "what_kind": a["what_kind"], "what_basis": a["what_basis"], "extra_primaries": a["extra_primaries"], "site": a["site"]["label"] if a["site"] else None, "technique": a["technique"], "technique_origin": a["technique_origin"],
                         "unregistered": a["untouched"], "qualifiers": a["qualifiers"], "status": "partial" if a["untouched"] else "complete"})
        else:
            base.update({"result": "none", "unregistered": a["untouched"], "qualifiers": a["qualifiers"], "reason": a["reason"]})
        return base


def procedure_slots(L, lex):
    """v1.1 §9.2 의 자유 텍스트 자리 전부(slot_items) — market-pricing 은 ③ 으로 따로 센다."""
    S = V11.slot_items(L, lex)
    refs, market = OrderedDict(), None
    for k, (note, items) in S.items():
        if k.startswith("market-pricing"):
            market = (k, items)
        else:
            refs[k] = items
    return refs, market


# ---------------------------------------------------------------------------
# 부작용 튜플
# ---------------------------------------------------------------------------
ADV_PAREN = re.compile(r"\(([^()]*)\)")
ADV_MEMBER_SPLIT = re.compile(r"[·/,+]|\s및\s|\s또는\s|--|—|:|;")
ADV_STRIP = "*'\"“”‘’.…`~!?"


class AdverseTuples:
    def __init__(self, ids):
        self.ids = ids
        self.tuples = OrderedDict()
        self.lookup = {}
        for surf, canon in ids.rsite_surface.items():
            self.lookup.setdefault(surf, ("relative", canon))
        for surf, canon in ids.site_surface.items():
            self.lookup.setdefault(surf, ("site", canon))
        for surf, canon in ids.course_surface.items():
            self.lookup.setdefault(surf, ("course", canon))
        for surf, canon in ids.event_surface.items():
            self.lookup.setdefault(surf, ("event", canon))
        self.maxlen = 6

    def split(self, text):
        parens = ADV_PAREN.findall(text)
        outer = ADV_PAREN.sub(" ", text)
        groups = []
        for where, g in [("outer", outer)] + [("inner", p) for p in parens]:
            members = []
            for part in ADV_MEMBER_SPLIT.split(g):
                part = part.strip()
                if not part:
                    continue
                toks = [t.strip(ADV_STRIP) for t in part.split()]
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
                    else:
                        untouched.append(toks[i])
                        i += 1
                members.append({"text": part, "spans": spans, "untouched": untouched})
            groups.append({"where": where, "members": members})
        return groups

    def assemble(self, groups):
        """멤버 안의 사건 하나 = 튜플 하나. site·course 는 멤버 → 같은 묶음 → outer 묶음 순으로 상속."""
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
        name_courses = list(dict.fromkeys(s["canonical"] for s in all_spans if s["kind"] == "course"))
        name_sites = list(dict.fromkeys((s["kind"], s["canonical"]) for s in all_spans if s["kind"] in ("relative", "site")))
        name_course = name_courses[0] if len(name_courses) == 1 else None
        name_site = name_sites[0] if len(name_sites) == 1 else None
        out = []
        for g in groups:
            g_spans = [s for m in g["members"] for s in m["spans"]]
            for m in g["members"]:
                events = [s["canonical"] for s in m["spans"] if s["kind"] == "event"]
                if not events:
                    continue
                site = pick_site(m["spans"]) or pick_site(g_spans) or pick_site(outer_spans) or name_site
                course = pick(m["spans"], "course") or pick(g_spans, "course") or pick(outer_spans, "course") or name_course or "미상"
                for ev in dict.fromkeys(events):
                    out.append({"event": ev, "site": site, "course": course, "member": m["text"]})
        untouched = [u for g in groups for m in g["members"] for u in m["untouched"]]
        # 같은 튜플 중복 제거(괄호 안 영문 반복)
        seen, uniq = set(), []
        for t in out:
            k = (t["event"], t["site"], t["course"])
            if k not in seen:
                seen.add(k)
                uniq.append(t)
        return uniq, untouched

    def register(self, t, src, untouched):
        ev = self.ids.event[norm(t["event"])]
        if t["site"] is None:
            site_id, site_label, site_kind = "none", None, "none"
        elif t["site"][0] == "relative":
            site_id, site_label, site_kind = self.ids.rsite[norm(t["site"][1])]["id"], t["site"][1], "relative"
        else:
            site_id, site_label, site_kind = self.ids.site[norm(t["site"][1])]["id"], t["site"][1], "site"
        cid = self.ids.course[norm(t["course"])]["id"]
        tid = mkid("ADV", f"{ev['id']}|{site_id}|{cid}")
        rec = self.tuples.get(tid)
        if rec is None:
            rec = {"id": tid, "event": ev["label"], "event_category": ev["category"], "site_kind": site_kind, "site": site_label, "site_id": site_id, "course": t["course"], "course_id": cid,
                   "status": "complete", "unregistered_fragments": [], "origins": [], "sources": []}
            self.tuples[tid] = rec
        rec["sources"].append(src)
        if src["origin"] not in rec["origins"]:
            rec["origins"].append(src["origin"])
        for u in untouched:
            if u not in rec["unregistered_fragments"]:
                rec["unregistered_fragments"].append(u)
        if untouched:
            rec["status"] = "partial"
        return tid

    def run_text(self, text, src):
        groups = self.split(text)
        tuples, untouched = self.assemble(groups)
        ids = [self.register(t, src, untouched) for t in tuples]
        return {"text": text, "tuples": [(t["event"], t["site"][1] if t["site"] else None, t["course"]) for t in tuples], "tuple_ids": ids, "unregistered": untouched,
                "spans": [(s["kind"], s["canonical"], s["text"]) for g in groups for m in g["members"] for s in m["spans"]]}


def adverse_phrases(L):
    """표현(adverse_expression) 레코드 전부: (kind, text, src dict)"""
    out = []
    for cat in L["consent-checklist.json"]["categories"]:
        for i, x in enumerate(cat.get("emergency_signs", []) or []):
            out.append(("emergency_sign", x, {"origin": "consent", "file": "consent-checklist.json", "path": "categories[].emergency_signs[]", "modality": cat["id"], "context": {"frequency_class": "emergency"}}))
    for tl in L["post-procedure-timeline.json"]["timelines"]:
        code = tl["category"].split("-")[0]
        for ph in tl["phases"]:
            for k in ["normal", "abnormal", "caution", "emergency"]:
                for x in ph.get(k, []) or []:
                    out.append(("symptom_phrase", x, {"origin": f"timeline.{k}", "file": "post-procedure-timeline.json", "path": f"timelines[].phases[].{k}[]", "modality": code, "context": {"reaction_level": k, "period": ph["period"], "phase_label": ph["label"], "timeline": tl["name"]}}))
    ex = L["extracted.json"]
    for code, v in ex.items():
        if not CODE_KEY_RE.match(code):
            continue
        s = v.get("safety") or {}
        for k in ["common", "uncommon", "serious", "emergency"]:
            for x in s.get(k) or []:
                out.append(("safety_phrase", x, {"origin": "extracted.safety", "file": "extracted.json", "path": f"{{code}}.safety.{k}[]", "modality": code, "context": {"frequency_class": k}}))
    tx = L["taxonomy.json"]
    syn = {"common_adverse_effects": "common", "serious_adverse_effects": "serious", "common_side_effects": "common"}
    for m in tx["modality"]:
        s = (m.get("extracted") or {}).get("safety") or {}
        for k in ["common", "uncommon", "serious"]:
            for x in s.get(k) or []:
                out.append(("safety_phrase", x, {"origin": "taxonomy.modality.safety", "file": "taxonomy.json", "path": f"modality[].extracted.safety.{k}[]", "modality": m["id"], "context": {"frequency_class": k}}))
        for sc in m["subcategories"]:
            for it in sc["items"]:
                s = (it.get("extracted") or {}).get("safety") or {}
                for k in ["common", "serious", "common_adverse_effects", "serious_adverse_effects", "long_term"]:
                    for x in s.get(k) or []:
                        out.append(("safety_phrase", x, {"origin": "taxonomy.item.safety", "file": "taxonomy.json", "path": f"modality[].subcategories[].items[].extracted.safety.{k}[]", "modality": m["id"], "context": {"frequency_class": syn.get(k, k), "item_name": it["name"]}}))
        for pr in m["products"]:
            s = (pr.get("extracted") or {}).get("safety") or {}
            for k in ["common", "serious", "common_side_effects"]:
                for x in s.get(k) or []:
                    out.append(("safety_phrase", x, {"origin": "taxonomy.product.safety", "file": "taxonomy.json", "path": f"modality[].products[].extracted.safety.{k}[]", "modality": m["id"], "context": {"frequency_class": syn.get(k, k), "product_name": pr["name"]}}))
    lit = L["literature-evidence.json"]
    for code, cat in lit["categories"].items():
        for i, ae in enumerate(cat.get("adverse_effects", []) or []):
            out.append(("evidence_statement", ae["statement"], {"origin": "literature", "file": "literature-evidence.json", "path": "categories.{code}.adverse_effects[].statement", "modality": code, "record": i, "patient_ko": ae.get("patient_ko"), "context": {}}))
    return out


# ---------------------------------------------------------------------------
# 전체 실행 · 집계
# ---------------------------------------------------------------------------
def run_all(dic_json, rules, L, resolve_rules=None):
    """rules = tuple_rules(§1.4/§1.5 데이터) · resolve_rules = v1.1 §1.3 분해 규칙 데이터(조각 내기에 그대로 쓴다)"""
    if resolve_rules is None:
        sys.path.insert(0, HERE)
        import erd_spec_v2
        resolve_rules = erd_spec_v2.RESOLVE_RULES
    ids = Ids(dic_json, L)
    lex = V11.Lexicon(with_alias(dic_json))
    PT = ProcedureTuples(lex, resolve_rules, ids, L)
    # ① 분류 항목 521
    PT.run_catalog()
    cat_recs = list(PT.catalog.values())
    n_cat = len(cat_recs)
    cat_tuple_ids = [r["procedure_id"] for r in cat_recs if r.get("procedure_id")]
    cat_distinct = list(dict.fromkeys(cat_tuple_ids))
    # ② 참조 자리 · ③ market-pricing
    refs, market = procedure_slots(L, lex)
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
    # 집계 — 시술
    T = PT.tuples

    def slot_summary(rows):
        c = Counter(r["result"] for r in rows)
        st = Counter(r.get("status") for r in rows if r["result"] in ("tuple", "combo_ref"))
        return {"n": len(rows), "tuple": c.get("tuple", 0), "combo_ref": c.get("combo_ref", 0), "none": c.get("none", 0), "complete": st.get("complete", 0), "partial": st.get("partial", 0),
                "distinct_tuples": len({x for r in rows for x in ([r.get("procedure_id")] if r["result"] == "tuple" else r.get("member_ids", [])) if x}),
                "new_tuples_not_from_catalog": len({x for r in rows for x in ([r.get("procedure_id")] if r["result"] == "tuple" else r.get("member_ids", [])) if x and "catalog_item" not in T[x]["origins"]})}

    folded = []
    for tid in cat_distinct:
        names = [r for r in cat_recs if r.get("procedure_id") == tid or tid in r.get("member_ids", [])]
        t = T[tid]
        own_unreg = list(dict.fromkeys(u for r in names for u in r.get("unregistered", [])))
        folded.append({"procedure_id": tid, "what_kind": t["what_kind"], "what": t["what_label"], "site": t["site"], "technique": t["technique"], "technique_origin": t["technique_origin"], "status": "partial" if own_unreg else "complete",
                       "n_items": len(names), "items": [f"{r['name']}[{r['family']}]" for r in names], "unregistered": own_unreg})
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
    proc_summary = OrderedDict([
        ("catalog_items", n_cat),
        ("catalog_result", dict(Counter(r["result"] for r in cat_recs))),
        ("catalog_distinct_tuples", len(cat_distinct)),
        ("catalog_fold_ratio", round(len(cat_distinct) / n_cat, 3) if n_cat else None),
        ("catalog_tuples_with_2plus_items", sum(1 for f in folded if f["n_items"] >= 2)),
        ("catalog_items_in_folded_tuples", sum(f["n_items"] for f in folded if f["n_items"] >= 2)),
        ("catalog_by_what_kind", dict(Counter(r.get("what_kind") for r in cat_recs if r["result"] == "tuple"))),
        ("catalog_by_what_basis", dict(Counter(str(r.get("what_basis", "")).split(":")[0] for r in cat_recs if r["result"] == "tuple"))),
        ("catalog_status", dict(Counter(r.get("status") for r in cat_recs if r["result"] == "tuple"))),
        ("catalog_site_none", sum(1 for r in cat_recs if r["result"] == "tuple" and not r.get("site"))),
        ("catalog_site_none_ratio", round(sum(1 for r in cat_recs if r["result"] == "tuple" and not r.get("site")) / max(1, sum(1 for r in cat_recs if r["result"] == "tuple")), 3)),
        ("catalog_technique", dict(Counter(r.get("technique_origin") for r in cat_recs if r["result"] == "tuple"))),
        ("catalog_technique_none_ratio", round(sum(1 for r in cat_recs if r["result"] == "tuple" and r.get("technique_origin") == "none") / max(1, sum(1 for r in cat_recs if r["result"] == "tuple")), 3)),
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
        ("families_without_single_technique", sorted(f for f, v in ids.family_tech.items() if len(v) != 1)),
        ("unregistered_distinct", len(unreg_all)),
        ("unregistered_total", sum(unreg_all.values())),
        ("unregistered_top30", unreg_all.most_common(30)),
        ("unregistered_top30_by_origin", {k: v.most_common(30) for k, v in unreg_by_origin.items()}),
    ])
    # ---- 부작용
    AT = AdverseTuples(ids)
    comp_rows = []
    for cat in L["complications.json"]["categories"]:
        for i, c in enumerate(cat["complications"]):
            r = AT.run_text(c["name"], {"origin": "complications", "file": "complications.json", "path": "categories[].complications[].name", "modality": cat["id"], "record": i})
            r.update({"modality": cat["id"], "severity": c.get("severity")})
            comp_rows.append(r)
    comp_tuple_ids = list(dict.fromkeys(x for r in comp_rows for x in r["tuple_ids"]))
    expr_rows = []
    for kind, text, src in adverse_phrases(L):
        r = AT.run_text(text, dict(src, kind=kind))
        r.update({"kind": kind, "modality": src.get("modality"), "origin": src["origin"], "path": src["path"], "context": src.get("context")})
        if kind == "evidence_statement" and src.get("patient_ko"):
            r2 = AT.run_text(src["patient_ko"], dict(src, kind="patient_text", lang="ko", path="categories.{code}.adverse_effects[].patient_ko", origin="literature.patient_ko"))
            r["patient_ko"] = {"text": src["patient_ko"], "tuples": r2["tuples"], "tuple_ids": r2["tuple_ids"], "unregistered": r2["unregistered"]}
            r["tuple_ids_union"] = list(dict.fromkeys(r["tuple_ids"] + r2["tuple_ids"]))
            r["basis"] = "both" if r["tuple_ids"] and r2["tuple_ids"] else "statement" if r["tuple_ids"] else "patient_ko" if r2["tuple_ids"] else "none"
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
        adv_folded.append({"adverse_id": tid, "event": t["event"], "category": t["event_category"], "site_kind": t["site_kind"], "site": t["site"], "course": t["course"], "status": "partial" if own_unreg else "complete", "n_names": len(names), "names": names, "unregistered": own_unreg})
    adv_folded.sort(key=lambda x: (-x["n_names"], x["category"], x["event"]))
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
                "distinct_tuples": len({x for r in rows for x in r["tuple_ids_union"]}),
                "new_tuples_not_from_complications": len({x for r in rows for x in r["tuple_ids_union"] if "complications" not in A[x]["origins"]})}

    adv_summary = OrderedDict([
        ("complications_names", len(comp_rows)),
        ("complications_names_with_tuple", sum(1 for r in comp_rows if r["tuple_ids"])),
        ("complications_names_without_tuple", [f"{r['text']} [{r['modality']}]" for r in comp_rows if not r["tuple_ids"]]),
        ("complications_names_multi_tuple", sum(1 for r in comp_rows if len(r["tuple_ids"]) >= 2)),
        ("complications_distinct_tuples", len(comp_tuple_ids)),
        ("complications_fold_ratio", round(len(comp_tuple_ids) / len(comp_rows), 3)),
        ("complications_tuples_with_2plus_names", sum(1 for f in adv_folded if f["n_names"] >= 2)),
        ("complications_by_course", dict(Counter(A[t]["course"] for t in comp_tuple_ids))),
        ("complications_by_site_kind", dict(Counter(A[t]["site_kind"] for t in comp_tuple_ids))),
        ("complications_by_category", dict(Counter(A[t]["event_category"] for t in comp_tuple_ids))),
        ("event_dictionary_values", len(ids.event)),
        ("event_dictionary_used_by_complications", len({A[t]["event"] for t in comp_tuple_ids})),
        ("event_dictionary_unused", sorted(set(e["label"] for e in ids.event.values()) - {A[t]["event"] for t in comp_tuple_ids})),
        ("course_dictionary_values", len(ids.course)),
        ("relative_site_values", len(ids.rsite)),
        ("expressions", OrderedDict((k, kind_summary(k)) for k in ["safety_phrase", "emergency_sign", "symptom_phrase", "evidence_statement"])),
        ("expressions_by_origin", OrderedDict((o, {"n": sum(1 for r in expr_rows if r["origin"] == o), "linked": sum(1 for r in expr_rows if r["origin"] == o and r["linked"])}) for o in dict.fromkeys(r["origin"] for r in expr_rows))),
        ("expressions_total", {"n": len(expr_rows), "linked": sum(1 for r in expr_rows if r["linked"]), "unlinked": sum(1 for r in expr_rows if not r["linked"]), "patient_text_records": 4 * sum(1 for r in expr_rows if r["kind"] == "evidence_statement")}),
        ("literature_basis", dict(Counter(r.get("basis") for r in expr_rows if r["kind"] == "evidence_statement"))),
        ("tuples_total", len(A)),
        ("tuples_by_origin", OrderedDict((o, sum(1 for t in A.values() if o in t["origins"])) for o in dict.fromkeys(o for t in A.values() for o in t["origins"]))),
        ("tuples_status", dict(Counter(t["status"] for t in A.values()))),
        ("tuples_by_course", dict(Counter(t["course"] for t in A.values()))),
        ("tuples_by_site_kind", dict(Counter(t["site_kind"] for t in A.values()))),
        ("tuples_by_category", dict(Counter(t["event_category"] for t in A.values()))),
        ("unregistered_distinct", len(adv_unreg)),
        ("unregistered_total", sum(adv_unreg.values())),
        ("unregistered_all", adv_unreg.most_common()),
        ("unregistered_by_origin", {k: v.most_common() for k, v in adv_unreg_by_origin.items()}),
    ])
    out = OrderedDict([
        ("erd_version", "v2"), ("rules", rules["name"]),
        ("procedure", OrderedDict([("summary", proc_summary), ("tuples", list(T.values())), ("catalog", cat_recs), ("folded", folded), ("references", ref_rows), ("market_pricing", mk_rows)])),
        ("adverse", OrderedDict([("summary", adv_summary), ("tuples", list(A.values())), ("complications", comp_rows), ("folded", adv_folded), ("expressions", expr_rows)])),
    ])
    return out


# ---------------------------------------------------------------------------
# 표 (md) — erd-v2.md §9.5 / §9.6 에 그대로 붙는다
# ---------------------------------------------------------------------------
def md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    for r in rows:
        out.append("| " + " | ".join(str(x).replace("|", "\\|").replace("\n", " ") for x in r) + " |")
    return "\n".join(out)


def procedure_md(R):
    s = R["procedure"]["summary"]
    o = []
    A = o.append
    A("#### 9.5.1 분류 항목 521 → 튜플")
    A("")
    A(md_table(["항목", "값"], [
        ("분류 항목", s["catalog_items"]), ("분해 결과", ", ".join(f"{k}={v}" for k, v in s["catalog_result"].items())),
        ("튜플 수(distinct)", f"**{s['catalog_distinct_tuples']}** (521 → N · 비율 {s['catalog_fold_ratio']})"),
        ("둘 이상 항목이 접힌 튜플", f"{s['catalog_tuples_with_2plus_items']} 개 튜플에 항목 {s['catalog_items_in_folded_tuples']} 개 (나머지 {s['catalog_distinct_tuples'] - s['catalog_tuples_with_2plus_items']} 튜플은 항목 1개씩)"),
        ("what 축", ", ".join(f"{k}={v}" for k, v in s["catalog_by_what_kind"].items()) + " · 근거: " + ", ".join(f"{k}={v}" for k, v in s["catalog_by_what_basis"].items())),
        ("site 축", f"none {s['catalog_site_none']} / 항목 기준 none 비율 {s['catalog_site_none_ratio']} · 튜플 기준 none 비율 {s['catalog_tuple_site_none_ratio']}"),
        ("technique 축", ", ".join(f"{k}={v}" for k, v in s["catalog_technique"].items()) + f" · 항목 기준 none 비율 {s['catalog_technique_none_ratio']} · 튜플 기준 none 비율 {s['catalog_tuple_technique_none_ratio']}"),
        ("상속 불가 계열(R5 기법 둘 이상 또는 없음)", ", ".join(s["families_without_single_technique"])),
        ("항목 상태", ", ".join(f"{k}={v}" for k, v in s["catalog_status"].items())),
    ]))
    A("")
    A("#### 9.5.2 접힌 결과 — 둘 이상의 분류 항목이 같은 튜플로 간 것 전부 (사용자가 「같은 게 맞다」고 볼 것)")
    A("")
    rows = [(i + 1, f["what_kind"], f["what"], f["site"] or "none", f"{f['technique'] or 'none'}({f['technique_origin']})", f["status"], f["n_items"], " · ".join(f["items"]), ", ".join(f["unregistered"]) or "—")
            for i, f in enumerate(x for x in R["procedure"]["folded"] if x["n_items"] >= 2)]
    A(md_table(["#", "what 종류", "what", "site", "technique", "상태", "항목 수", "접힌 분류 항목(전부)", "미등록 조각"], rows))
    A("")
    A("#### 9.5.3 항목 하나짜리 튜플 (접히지 않은 것 전부)")
    A("")
    rows = [(i + 1, f["what_kind"], f["what"], f["site"] or "none", f"{f['technique'] or 'none'}({f['technique_origin']})", f["status"], f["items"][0], ", ".join(f["unregistered"]) or "—")
            for i, f in enumerate(x for x in R["procedure"]["folded"] if x["n_items"] == 1)]
    A(md_table(["#", "what 종류", "what", "site", "technique", "상태", "분류 항목", "미등록 조각"], rows))
    A("")
    A("#### 9.5.4 참조 자리 전부(②) + market-pricing(③) → 튜플")
    A("")
    rows = []
    for k, v in s["reference_slots"].items():
        rows.append((k, v["n"], v["tuple"], v["combo_ref"], v["none"], v["complete"], v["partial"], v["distinct_tuples"], v["new_tuples_not_from_catalog"]))
    v = s["reference_total"]
    rows.append(("**② 합계**", v["n"], v["tuple"], v["combo_ref"], v["none"], v["complete"], v["partial"], v["distinct_tuples"], v["new_tuples_not_from_catalog"]))
    v = s["market_pricing"]
    rows.append(("**③ market-pricing.items[].name (122)**", v["n"], v["tuple"], v["combo_ref"], v["none"], v["complete"], v["partial"], v["distinct_tuples"], v["new_tuples_not_from_catalog"]))
    A(md_table(["참조 자리", "건", "튜플", "combo_ref", "튜플 불가", "complete", "partial", "distinct 튜플", "①에 없는 새 튜플"], rows))
    A("")
    A("참조 행 전부 (라벨 → 결과):")
    A("")
    for k, rows_ in list(R["procedure"]["references"].items()) + [(R["procedure"]["summary"] and "market-pricing.items[].name (122)", R["procedure"]["market_pricing"])]:
        parts = []
        for r in rows_:
            if r["result"] == "tuple":
                t = next(t for t in R["procedure"]["tuples"] if t["id"] == r["procedure_id"])
                parts.append(f"`{r['label']}`" + (f"@{r['hint']}" if r.get("hint") else "") + f" → ({t['what_kind']}:{t['what_label']} × {t['site'] or 'none'} × {t['technique'] or 'none'})" + (f" 미등록[{','.join(r['unregistered'])}]" if r.get("unregistered") else ""))
            elif r["result"] == "combo_ref":
                ms = []
                for mid in r["member_ids"]:
                    t = next(t for t in R["procedure"]["tuples"] if t["id"] == mid)
                    ms.append(f"{t['what_kind']}:{t['what_label']}×{t['site'] or 'none'}×{t['technique'] or 'none'}")
                parts.append(f"`{r['label']}`" + (f"@{r['hint']}" if r.get("hint") else "") + " → combo_ref[" + " + ".join(ms) + "]" + (f" 미등록[{','.join(r['unregistered'])}]" if r.get("unregistered") else ""))
            else:
                parts.append(f"`{r['label']}`" + (f"@{r['hint']}" if r.get("hint") else "") + " → 튜플 불가" + (f" 미등록[{','.join(r['unregistered'])}]" if r.get("unregistered") else ""))
        A(f"- **{k}**: " + " · ".join(parts))
    A("")
    A("#### 9.5.5 튜플 전체 집계 (① ② ③ 합집합)")
    A("")
    A(md_table(["항목", "값"], [
        ("튜플 수", f"**{s['tuples_total']}**"), ("원천별", ", ".join(f"{k}={v}" for k, v in s["tuples_by_origin"].items())),
        ("what 종류", ", ".join(f"{k}={v}" for k, v in s["tuples_by_what_kind"].items())), ("상태", ", ".join(f"{k}={v}" for k, v in s["tuples_status"].items())),
        ("site none 비율", s["tuples_site_none_ratio"]), ("technique none 비율", f"{s['tuples_technique_none_ratio']} · 출처 " + ", ".join(f"{k}={v}" for k, v in s["tuples_technique_origin"].items())),
        ("미등록 조각", f"distinct {s['unregistered_distinct']} · 총 {s['unregistered_total']}"),
    ]))
    A("")
    A("#### 9.5.6 미등록 조각 상위 30 (어느 축인지는 판정하지 않는다 — 사전 추가는 실버 빌드의 결정 묶음)")
    A("")
    A("- 전체: " + " · ".join(f"`{f}`×{n}" for f, n in s["unregistered_top30"]))
    for k, v in s["unregistered_top30_by_origin"].items():
        A(f"- {k}: " + (" · ".join(f"`{f}`×{n}" for f, n in v) or "—"))
    return "\n".join(o)


def adverse_md(R):
    s = R["adverse"]["summary"]
    o = []
    A = o.append
    A("#### 9.6.1 complications 65 → 튜플")
    A("")
    A(md_table(["항목", "값"], [
        ("이름", s["complications_names"]), ("튜플이 생긴 이름", s["complications_names_with_tuple"]), ("튜플이 안 생긴 이름(사건 조각 없음)", "; ".join(s["complications_names_without_tuple"]) or "0"),
        ("사건이 둘 이상인 이름", s["complications_names_multi_tuple"]), ("튜플 수(distinct)", f"**{s['complications_distinct_tuples']}** (65 → N · 비율 {s['complications_fold_ratio']})"),
        ("둘 이상 이름이 접힌 튜플", s["complications_tuples_with_2plus_names"]),
        ("경과", ", ".join(f"{k}={v}" for k, v in s["complications_by_course"].items())), ("부위", ", ".join(f"{k}={v}" for k, v in s["complications_by_site_kind"].items())),
        ("분류", ", ".join(f"{k}={v}" for k, v in s["complications_by_category"].items())),
        ("사건 사전 최종 값", f"**{s['event_dictionary_values']}** (65 이름이 쓴 값 {s['event_dictionary_used_by_complications']} · 안 쓰인 값: {', '.join(s['event_dictionary_unused']) or '없음'})"),
        ("경과 사전 값", s["course_dictionary_values"]), ("상대 부위 사전 값", s["relative_site_values"]),
    ]))
    A("")
    A("#### 9.6.2 65 가 접힌 결과 — 튜플마다 어떤 이름들이 갔는지 전부")
    A("")
    rows = [(i + 1, f["category"], f["event"], f"{f['site'] or 'none'}({f['site_kind']})", f["course"], f["status"], f["n_names"], " · ".join(f["names"]), ", ".join(f["unregistered"]) or "—") for i, f in enumerate(R["adverse"]["folded"])]
    A(md_table(["#", "분류", "event", "site", "course", "상태", "이름 수", "접힌 complications 이름(전부)", "미등록 조각"], rows))
    A("")
    A("#### 9.6.3 표현(adverse_expression) → 튜플")
    A("")
    rows = [(k, v["n"], v["linked"], v["unlinked"], v["distinct_tuples"], v["new_tuples_not_from_complications"]) for k, v in s["expressions"].items()]
    t = s["expressions_total"]
    rows.append(("**합계**", t["n"], t["linked"], t["unlinked"], "", ""))
    A(md_table(["kind", "표현 수", "linked(R29)", "unlinked(null)", "distinct 튜플", "65 에 없던 새 튜플"], rows))
    A("")
    A("- 출처별: " + " · ".join(f"{k} {v['linked']}/{v['n']}" for k, v in s["expressions_by_origin"].items()))
    A(f"- 문헌 32: statement/patient_ko 어느 쪽에서 닿았나 — " + ", ".join(f"{k}={v}" for k, v in s["literature_basis"].items()) + f" · patient_text 표현 레코드 {t['patient_text_records']}(4개 언어 × 32, 같은 레코드의 튜플을 따라감)")
    A("")
    A("#### 9.6.4 튜플 전체 집계 (65 + 표현 전부)")
    A("")
    A(md_table(["항목", "값"], [
        ("튜플 수", f"**{s['tuples_total']}**"), ("원천별", ", ".join(f"{k}={v}" for k, v in s["tuples_by_origin"].items())),
        ("상태", ", ".join(f"{k}={v}" for k, v in s["tuples_status"].items())), ("경과", ", ".join(f"{k}={v}" for k, v in s["tuples_by_course"].items())),
        ("부위", ", ".join(f"{k}={v}" for k, v in s["tuples_by_site_kind"].items())), ("분류", ", ".join(f"{k}={v}" for k, v in s["tuples_by_category"].items())),
        ("미등록 조각", f"distinct {s['unregistered_distinct']} · 총 {s['unregistered_total']}"),
    ]))
    A("")
    A("표현에서 새로 생긴 튜플 전부(65 에 없던 것):")
    A("")
    new = [t for t in R["adverse"]["tuples"] if "complications" not in t["origins"]]
    A(md_table(["#", "분류", "event", "site", "course", "상태", "원천", "표현 수"], [(i + 1, t["event_category"], t["event"], f"{t['site'] or 'none'}({t['site_kind']})", t["course"], t["status"], ", ".join(t["origins"]), len(t["sources"])) for i, t in enumerate(new)]))
    A("")
    A("#### 9.6.5 미등록 조각 전부 (출처별 · 횟수) — 사전 추가는 실버 빌드의 결정 묶음")
    A("")
    for k, v in s["unregistered_by_origin"].items():
        A(f"- **{k}** ({len(v)}): " + " · ".join(f"`{f}`×{n}" for f, n in v))
    return "\n".join(o)


def load_all():
    dic = json.load(open(os.path.join(HERE, "erd-v2-dictionaries.json"), encoding="utf-8"))
    try:
        erd = json.load(open(os.path.join(HERE, "erd-v2.json"), encoding="utf-8"))
        rules, rrules = erd["tuple_rules"], erd["resolve_rules"]
    except (FileNotFoundError, KeyError):
        sys.path.insert(0, HERE)
        import erd_spec_v2
        rules, rrules = erd_spec_v2.TUPLE_RULES, erd_spec_v2.RESOLVE_RULES
    files = [f for f in os.listdir(LEDGER) if f.endswith(".json")]
    L = {f: json.load(open(os.path.join(LEDGER, f), encoding="utf-8")) for f in files}
    return dic, rules, rrules, L


def main():
    dic, rules, rrules, L = load_all()
    R = run_all(dic, rules, L, rrules)
    print(procedure_md(R))
    print()
    print(adverse_md(R))
    json.dump(R, open(os.path.join(HERE, "erd-v2-tuples.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    print("\n→ erd-v2-tuples.json")


if __name__ == "__main__":
    main()
