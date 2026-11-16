#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ERD v3.1 — 튜플·단위 분해 실측기. v3(erd-v3-tuples.py · 동결) 위에 발주서 erd-v3.1-brief.md 6건 + 코디 추가 3건 중 분해·실측에 닿는 것을 바꾼다. 독립 실행.
원장 21 = 브론즈 2판 `bronze/phub-ledger/`(HASHES.txt 검증).

v3 → v3.1 (실측에 닿는 것):
  V3.1-4 조건 축 신설 — 조건 사전(person_condition · 정준값·동의어·kind·출처)으로 사람 조건 이름 471(distinct 298 · kind 포함 299)을 분해: 완전 일치만 접고(멤버 안 조건 조각마다 단위 · 원칙 B) 미등록 조각이 있으면 raw_name(원칙 A) · 표현(condition_expression)은 단위를 가리키기만(R33).
  V3.1-5 회·차 자리 — `\\d+회` → R12.session_count · `\\d+차` → R12.session_index · R9/R17/R18/market 자리는 qualifier_text 만.
  V3.1-6 stopwords 겹침 — 48 사전 전수에서 stopword 와 같은 값·동의어를 센다(관리 ↔ modality_group).
  V3.1-7 필수 고지 — consent mandatory_disclosures 109 를 표현(kind=disclosure)으로 분해 · 계열 17 × 고지 · 부작용 조각 연결 수.
  V3.1-8 안전 문구 수식어 — 목록·패턴(정도·시간·발생률·조건·연결어·기타)은 미등록 조각이 아니라 속성 · 단어마다 locator.
  V3.1-9 단위 생성 = 시술 튜플과 대칭 — 조각 전부 사전 값이면 어느 출처든 조합 단위를 세운다(없으면 생성 · 있으면 연결 · exact) · 미등록 조각이 섞인 단위 0 · phrase_shape.
  V3.1-1/2 실측 — product_reclassify 대상 예(EXO-02 · id 재계산) · R32 출처 후보(제품 note·legal_warning·regulatory_status 규칙 문장 전수).

입력(같은 폴더): erd-v3.1-dictionaries.json(없으면 v3 사전 + 명세의 조건 사전) · erd-v3.1.json(tuple_rules/resolve_rules — 없으면 erd_spec_v31) · erd-v3-tuples.py(→ v2.4 → …) · bronze/phub-ledger/ · erd-v3-tuples.json(나란히 비교)
출력: 표준 출력에 §9.5/§9.6/§9.7/§9.8 표 + erd-v3.1-tuples.json
실행: python3 erd-v3.1-tuples.py
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


V3 = load_module("erd_v3_tuples", os.path.join(HERE, "erd-v3-tuples.py"))
V24, V23, V22, V2, V11 = V3.V24, V3.V23, V3.V22, V3.V2, V3.V11
norm, mkid, md_table, with_alias = V3.norm, V3.mkid, V3.md_table, V3.with_alias
locator = V3.locator
_dedupe = V3._dedupe
SESSION_RE, COUNT_RE = V3.SESSION_RE, V3.COUNT_RE
CODE_KEY_RE = V2.CODE_KEY_RE
bronze_check = V3.bronze_check
v21_split = V3.v21_split


# ---------------------------------------------------------------------------
# 조건 사전 — 명세 데이터(CONDITION_CORES)에서 출처 횟수를 실측해 사전 항목을 만든다(build 와 tuples 가 같은 함수를 쓴다)
# ---------------------------------------------------------------------------
COND_KEYS = [("consent-checklist.json", "categories[].contraindications[]"), ("extracted.json", "{code}.contraindications.absolute[]"), ("extracted.json", "{code}.contraindications.relative[]"),
             ("taxonomy.json", "modality[].extracted.contraindications.absolute[]"), ("taxonomy.json", "modality[].extracted.contraindications.relative[]"), ("taxonomy.json", "modality[].subcategories[].items[].extracted.safety.contraindications[]"),
             ("pre-procedure-checklist.json", "universal_checks[].label"), ("pre-procedure-checklist.json", "category_specific[].checks[].label"), ("treatment-optimization.json", "by_age_group[].age")]


def condition_occurrences(L):
    """사람 조건 이름 자리 전부 — (file, path, rec, text, modality_code, level_hint)."""
    out = []
    for c in L["consent-checklist.json"]["categories"]:
        for i, x in enumerate(c.get("contraindications") or []):
            out.append(("consent-checklist.json", "categories[].contraindications[]", f"{c['id']}/{i}", x, c["id"], "contraindication"))
    for code, v in L["extracted.json"].items():
        if not CODE_KEY_RE.match(code):
            continue
        for k in ("absolute", "relative"):
            for i, x in enumerate((v.get("contraindications") or {}).get(k) or []):
                out.append(("extracted.json", f"{{code}}.contraindications.{k}[]", f"{code}/{i}", x, code, k))
    for m in L["taxonomy.json"]["modality"]:
        for k in ("absolute", "relative"):
            for i, x in enumerate(((m.get("extracted") or {}).get("contraindications") or {}).get(k) or []):
                out.append(("taxonomy.json", f"modality[].extracted.contraindications.{k}[]", f"{m['id']}/{i}", x, m["id"], k))
        for sc in m["subcategories"]:
            for it in sc["items"]:
                for i, x in enumerate(((it.get("extracted") or {}).get("safety") or {}).get("contraindications") or []):
                    out.append(("taxonomy.json", "modality[].subcategories[].items[].extracted.safety.contraindications[]", f"{m['id']}/{it['name']}/{i}", x, m["id"], "contraindication"))
    for i, u in enumerate(L["pre-procedure-checklist.json"]["universal_checks"]):
        out.append(("pre-procedure-checklist.json", "universal_checks[].label", str(i), u["label"], None, u.get("type")))
    for c in L["pre-procedure-checklist.json"]["category_specific"]:
        for i, ch in enumerate(c["checks"]):
            out.append(("pre-procedure-checklist.json", "category_specific[].checks[].label", f"{c['id']}/{i}", ch["label"], c["id"], ch.get("type")))
    for i, a in enumerate(L["treatment-optimization.json"]["by_age_group"]):
        out.append(("treatment-optimization.json", "by_age_group[].age", str(i), a["age"], None, None))
    return out


def condition_core_sources(L, cores):
    """명세 CONDITION_CORES → 값·동의어마다 [(file, path, n)] (derived · 부분 문자열 · 0 이면 빌드가 실패한다)."""
    occ = condition_occurrences(L)
    byk = defaultdict(list)
    for f, p, rec, x, _, _ in occ:
        byk[(f, p)].append(norm(x))
    out = []
    for canon, syns, note in cores:
        srcs = [(f, p, sum(1 for v in byk[(f, p)] if norm(canon) in v)) for f, p in COND_KEYS]
        srcs = [s for s in srcs if s[2] > 0]
        syn_srcs = []
        for sv in syns:
            ss = [(f, p, sum(1 for v in byk[(f, p)] if norm(sv) in v)) for f, p in COND_KEYS]
            syn_srcs.append((sv, [s for s in ss if s[2] > 0]))
        out.append({"canonical": canon, "sources": srcs, "synonyms": syn_srcs, "note": note})
    return out


def condition_dictionary_json(L, S):
    """build 가 없을 때(독립 실행)의 조건 사전 JSON — build 는 Dict_ 로 같은 값을 만든다."""
    entries = []
    kind_by = S.CONDITION_KIND_BY_SOURCE
    for r in condition_core_sources(L, S.CONDITION_CORES):
        kinds = sorted({kind_by[f"{f}:{p}"] for f, p, n in r["sources"]} | {kind_by[f"{f}:{p}"] for _, ss in r["synonyms"] for f, p, n in ss})
        entries.append({"id": mkid("DIC", f"person_condition|{r['canonical']}"), "canonical": r["canonical"], "sources": [{"file": f, "path": p, "n": n, "kind": "derived"} for f, p, n in r["sources"]],
                        "synonyms": [{"value": sv, "link": "표기 변형(derived)" if any(x in sv for x in ("한냉", "냉", "당뇨")) else "괄호 동치(derived)", "sources": [{"file": f, "path": p, "n": n, "kind": "derived"} for f, p, n in ss]} for sv, ss in r["synonyms"]],
                        "definition": None, "kind": "|".join(kinds) if kinds else None, "kinds": kinds, "note": r["note"]})
    return {"name": "person_condition", "label": "사람 조건 사전(condition_dictionary)", "note": "v3.1(V3.1-4)", "kind": "value", "entries": entries, "candidates": [], "canonical_count": len(entries), "synonym_count": sum(len(e["synonyms"]) for e in entries), "candidate_count": 0}


# ---------------------------------------------------------------------------
# 시술 축 — V3.1-5 회·차 자리
# ---------------------------------------------------------------------------
SLOT_RELATION = dict(V23.SLOT_RELATION)
MARKET_SLOT = "market-pricing.items[].name (122)"


def _session_tokens(groups):
    out = []
    for g in groups:
        for m in g["members"]:
            for s in m["spans"]:
                kind, canon = (s["kind"], s["canonical"]) if isinstance(s, dict) else (s[0], s[1])
                if kind != "spec":
                    continue
                cc = unicodedata.normalize("NFKC", str(canon)).replace(" ", "")
                ms = SESSION_RE.match(cc)
                mc = COUNT_RE.match(cc)
                if ms:
                    out.append({"token": canon, "kind": "차", "value": int(ms.group(1))})
                elif mc:
                    out.append({"token": canon, "kind": "회", "value": int(mc.group(1))})
    return out


class ProcedureTuples31(V3.ProcedureTuples3):
    """v3 위에 V3.1-5: 회·차 규격 → R12 session_index/session_count · R9/R17/R18/③ 는 qualifier_text 만."""

    def _annotate(self, groups, base):
        base = super()._annotate(groups, base)
        toks = _session_tokens(groups)
        base["session_tokens"] = toks
        counts = [t["value"] for t in toks if t["kind"] == "회"]
        base["session_count"] = counts[0] if counts else None
        sess = [t["value"] for t in toks if t["kind"] == "차"]
        base["session_index"] = sess[0] if sess else None
        return base

    def run_reference(self, label, hint, origin, slot):
        r = super().run_reference(label, hint, origin, slot)
        rel = SLOT_RELATION.get(slot, ("—", ""))[0] if slot != MARKET_SLOT else "—"
        toks = _session_tokens(r.get("groups") or [])
        r["session_tokens"] = toks
        r["session_relation"] = rel
        if rel == "R12":
            r["session_target"] = "R12.session_index/session_count" if toks else None
            sess = [x["value"] for x in toks if x["kind"] == "차"]
            cnts = [x["value"] for x in toks if x["kind"] == "회"]
            r["session_index"] = sess[0] if sess else None
            r["session_count"] = cnts[0] if cnts else None
            # 둘 이상이면 첫 값만 속성 · 나머지는 qualifier_text
            extra = [t["token"] for i, t in enumerate(toks) if any(t2["kind"] == t["kind"] for t2 in toks[:i])]
            if extra:
                r["qualifier_text"] = list(r.get("qualifier_text") or []) + extra
        else:
            if toks:
                r["qualifier_text"] = list(r.get("qualifier_text") or []) + [t["token"] for t in toks]
                r["session_target"] = "qualifier_text"
            else:
                r["session_target"] = None
            r["session_index"] = None
            r["session_count"] = None
        return r


# ---------------------------------------------------------------------------
# 부작용 축 — V3.1-9 단위 (사건, 부위, 물질) · 경과는 엣지 · V3.1-8 수식어 · V3.1-10 문구 사전 · V3.1-7 고지
# ---------------------------------------------------------------------------
SHAPES = ["event_only", "event_site", "event_degree_course", "event_incidence_condition", "explanatory", "unresolved"]
MOD_CLASSES = ("degree", "timing", "incidence", "condition", "connector", "misc")


class AdverseUnits31(V3.AdverseTuples3):
    """v3 분해(멤버 · 원칙 B·C · 접두 가름) 위에: 단위 세 칸 · 상대 부위 none · 경과는 엣지 · 수식어 분류 · 정규화형."""

    def __init__(self, ids, rules):
        super().__init__(ids)
        sw = rules["adverse_stopwords"]
        self.stop = {norm(w["word"]): (w["word"], w["class"]) for w in sw["words"]}
        self.patterns = [(p["class"], re.compile(p["regex"]), p["regex"]) for p in sw["patterns"]]
        self.stop_hits, self.pat_hits = Counter(), Counter()
        self.stop_locs, self.pat_locs = defaultdict(list), defaultdict(list)
        self.units = {}          # (event_id, site_id, qualifier_id) → tid
        self.created = OrderedDict()   # tid → PHR- id(처음 세운 문구 항목)
        self.unit_courses = defaultdict(Counter)

    def _classify_token(self, tok):
        nt = norm(tok)
        if nt in self.stop:
            return self.stop[nt][1], "word", self.stop[nt][0]
        for cls, rx, raw in self.patterns:
            if rx.match(unicodedata.normalize("NFKC", tok)):
                return cls, "pattern", raw
        return None, None, None

    def split(self, text, loc=None):
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
                spans, untouched, mods = [], [], []
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
                        i += 1
                        continue
                    cls, how, key_ = self._classify_token(tok)
                    if cls:
                        mods.append({"text": tok, "class": cls, "by": how, "key": key_})
                        tgt_hits, tgt_locs = (self.stop_hits, self.stop_locs) if how == "word" else (self.pat_hits, self.pat_locs)
                        tgt_hits[key_] += 1
                        if loc and len(tgt_locs[key_]) < 12 and loc not in tgt_locs[key_]:
                            tgt_locs[key_].append(loc)
                    else:
                        untouched.append(tok)
                    i += 1
                members.append({"text": part, "spans": spans, "untouched": untouched, "modifiers": mods, "where": where})
            groups.append({"where": where, "members": members})
        return groups

    @staticmethod
    def normalized(groups):
        """정규화형 = 수식어 토큰을 뺀 조각(사전에 닿은 구간 + 미등록 토큰)의 norm_v1 연결."""
        toks = []
        for g in groups:
            for m in g["members"]:
                toks += [s["text"] for s in m["spans"]] + m["untouched"]
        return norm("".join(toks))

    @staticmethod
    def _classes(groups):
        out = []
        for g in groups:
            for m in g["members"]:
                for s in m["spans"]:
                    out.append({"token": s["text"], "class": "relative_site" if s["kind"] == "relative" else s["kind"]})
                for md in m["modifiers"]:
                    out.append({"token": md["text"], "class": md["class"]})
                for u in m["untouched"]:
                    out.append({"token": u, "class": "explanation" if g["where"] == "inner" else "unregistered"})
        return out

    @staticmethod
    def _shape(classes, has_event):
        cs = {c["class"] for c in classes}
        if not has_event or "unregistered" in cs:
            return "unresolved"
        if cs & {"incidence", "condition"}:
            return "event_incidence_condition"
        if cs & {"degree", "timing", "course"}:
            return "event_degree_course"
        if "explanation" in cs:
            return "explanatory"
        if cs & {"site", "relative_site"}:
            return "event_site"
        return "event_only"

    def _parsed(self, groups):
        by = defaultdict(list)
        for g in groups:
            for m in g["members"]:
                for md in m["modifiers"]:
                    by[md["class"]].append(md["text"])
                if g["where"] == "inner":
                    for u in m["untouched"]:
                        by["explanation"].append(u)
        return {k: _dedupe(by[k]) for k in MOD_CLASSES + ("explanation",)}

    # --- 세 칸 단위 후보: v3 assemble(사건·부위·경과·수식 후보) → (사건, 부위 칸, 물질) 로 접고 경과·상대 부위는 따로
    def unit_candidates(self, tuples):
        out = OrderedDict()
        for t in tuples:
            site = t["site"]
            rel = site[1] if site and site[0] == "relative" else None
            cell = site if site and site[0] == "site" else None
            key = (t["event"], cell[1] if cell else None, t["qualifier"])
            c = out.get(key)
            if c is None:
                c = {"event": t["event"], "site": cell, "qualifier": t["qualifier"], "courses": [], "relative_sites": [], "site_basis": t.get("site_basis") if cell else None, "qualifier_basis": t.get("qualifier_basis"), "members": []}
                out[key] = c
            if t["course"] != "미상" and t["course"] not in c["courses"]:
                c["courses"].append(t["course"])
            if rel and rel not in c["relative_sites"]:
                c["relative_sites"].append(rel)
            if t["member"] not in c["members"]:
                c["members"].append(t["member"])
        return list(out.values())

    def unit_key(self, c):
        ev = self.ids.event[norm(c["event"])]
        sid = self.ids.site[norm(c["site"][1])]["id"] if c["site"] else "none"
        qid = self.qual_key(c["qualifier"])
        return (ev["id"], sid, qid)

    def register_unit(self, c, src):
        key = self.unit_key(c)
        tid = mkid("ADV", "|".join(key))
        rec = self.tuples.get(tid)
        if rec is None:
            ev = self.ids.event[norm(c["event"])]
            rec = {"id": tid, "event_kind": "dict", "event": ev["label"], "event_id": key[0], "event_category": ev["category"], "site_kind": "site" if c["site"] else "none", "site": c["site"][1] if c["site"] else None, "site_id": key[1],
                   "site_dict_kind": self.ids.site_kind.get(norm(c["site"][1])) if c["site"] else None, "qualifier": c["qualifier"], "qualifier_id": key[2], "qualifier_basis": c.get("qualifier_basis"),
                   "status": "complete", "unregistered_fragments": [], "origins": [], "sources": [], "anchor": None, "all_dict_values": True, "candidate_name": [], "event_fragments": [ev["label"]],
                   "extra_sites": [], "extra_qualifiers": [], "relative_site_text": [], "site_basis": c.get("site_basis"), "created_by_phrase": None, "explanations": []}
            self.tuples[tid] = rec
        rec["sources"].append(src)
        if src["origin"] not in rec["origins"]:
            rec["origins"].append(src["origin"])
        for r_ in c["relative_sites"]:
            if r_ not in rec["relative_site_text"]:
                rec["relative_site_text"].append(r_)
        for co in c["courses"]:
            self.unit_courses[tid][co] += 1
        self.units[key] = tid
        return tid

    def register_raw(self, text, tuples, untouched, extras, src, anchor):
        all_events = _dedupe(t["event"] for t in tuples)
        sites = _dedupe([t["site"][1] for t in tuples if t["site"]] + list(extras["extra_sites"]))
        courses = _dedupe([t["course"] for t in tuples if t["course"] != "미상"] + list(extras["extra_courses"]))
        quals = _dedupe([t["qualifier"] for t in tuples if t["qualifier"]] + list(extras["extra_qualifiers"]))
        event_id = f"RAW:{anchor}"
        tid = mkid("ADV", f"{event_id}|none|none|{anchor}")
        rec = self.tuples.get(tid)
        unatt = bool(extras["extra_sites"] or extras["extra_courses"] or extras["extra_qualifiers"])
        if rec is None:
            cat = self.ids.event[norm(all_events[0])]["category"] if all_events else None
            rec = {"id": tid, "event_kind": "raw_name", "event": text, "event_id": event_id, "event_category": cat, "site_kind": "none", "site": None, "site_id": "none", "site_dict_kind": None,
                   "qualifier": None, "qualifier_id": "none", "qualifier_basis": None,
                   "status": "partial" if untouched else "unresolved", "unregistered_fragments": list(untouched), "origins": [], "sources": [], "anchor": anchor, "all_dict_values": False, "candidate_name": list(untouched),
                   "event_fragments": all_events, "extra_sites": sites, "extra_courses": courses, "extra_qualifiers": quals, "relative_site_text": [], "site_basis": None, "created_by_phrase": None, "explanations": [],
                   "dict_tuples": [(t["event"], t["site"][1] if t["site"] else None, t["course"], t["qualifier"]) for t in tuples], "raw_reason": ("unregistered" if untouched else "") + ("+" if untouched and unatt else "") + ("unattached_fragments" if unatt else "")}
            self.tuples[tid] = rec
        rec["sources"].append(src)
        if src["origin"] not in rec["origins"]:
            rec["origins"].append(src["origin"])
        return tid

    def candidates_of(self, ucands):
        out = []
        for c in ucands:
            key = self.unit_key(c)
            out.append({"event": c["event"], "event_id": key[0], "site": c["site"][1] if c["site"] else None, "site_kind": "site" if c["site"] else "none", "site_id": key[1], "qualifier": c["qualifier"], "qualifier_id": key[2],
                        "courses": list(c["courses"]), "relative_sites": list(c["relative_sites"]), "would_be_id": mkid("ADV", "|".join(key)), "exists": key in self.units, "unit_id": self.units.get(key), "site_basis": c.get("site_basis"), "qualifier_basis": c.get("qualifier_basis"), "members": c["members"]})
        return out

    def evaluate(self, text, src):
        groups = self.split(text, src.get("locator"))
        tuples, untouched, extras = self.assemble(groups)
        uc = self.unit_candidates(tuples)
        cands = self.candidates_of(uc)
        reasons = []
        if not cands:
            reasons.append("no_event")
        if untouched:
            reasons.append("unregistered")
        if extras["extra_sites"] or extras["extra_courses"] or extras["extra_qualifiers"]:
            reasons.append("unattached_fragments")
        classes = self._classes(groups)
        row = {"text": text, "locator": src.get("locator"), "normalized": self.normalized(groups), "spans": [(s["kind"], s["canonical"], s["text"]) for g in groups for m in g["members"] for s in m["spans"]],
               "unregistered": untouched, "extra_sites": extras["extra_sites"], "extra_courses": extras["extra_courses"], "extra_qualifiers": extras["extra_qualifiers"], "site_list_merges": extras["site_list_merges"],
               "b_splits": [(t["event"], t["site"][1] if t["site"] else None, t["course"], t["n_site_candidates"], t["n_course_candidates"], t["qualifier"], t["n_qualifier_candidates"]) for t in tuples if t["n_site_candidates"] >= 2 or t["n_course_candidates"] >= 2 or t["n_qualifier_candidates"] >= 2],
               "dict_tuples": [(t["event"], t["site"][1] if t["site"] else None, t["course"], t["qualifier"]) for t in tuples], "event_fragments": _dedupe(t["event"] for t in tuples), "qualifiers": _dedupe(t["qualifier"] for t in tuples if t["qualifier"]),
               "tuples": [(t["event"], t["site"][1] if t["site"] else None, t["course"], t["course_basis"], t["site_basis"], t["qualifier"]) for t in tuples],
               "unit_candidates": uc, "candidates": cands, "status": "auto" if not reasons else "unlinked", "reasons": reasons, "fragment_classes": classes, "phrase_shape": self._shape(classes, bool(cands)), "parsed": self._parsed(groups),
               "courses": _dedupe(co for c in uc for co in c["courses"]), "relative_sites": _dedupe(r_ for c in uc for r_ in c["relative_sites"])}
        return row

    def run_name(self, text, src):
        row = self.evaluate(text, src)
        unattached = bool(row["extra_sites"] or row["extra_courses"] or row["extra_qualifiers"])
        if row["unregistered"] or unattached:
            tid = self.register_raw(text, [t for t in self._last_tuples(text, src)], row["unregistered"], {"extra_sites": row["extra_sites"], "extra_courses": row["extra_courses"], "extra_qualifiers": row["extra_qualifiers"]}, src, src["locator"])
            r = self.tuples[tid]
            row.update({"event_kind": "raw_name", "unit_ids": [tid], "candidate_name": row["unregistered"], "anchor": src["locator"], "raw_reason": r["raw_reason"]})
            return row
        ids = [self.register_unit(c, src) for c in row["unit_candidates"]]
        row.update({"event_kind": "dict" if ids else None, "unit_ids": _dedupe(ids), "candidate_name": [], "anchor": None})
        return row

    def _last_tuples(self, text, src):
        groups = self.split(text)
        tuples, _, _ = self.assemble(groups)
        return tuples


def adverse_phrases31(L):
    """v3 표현 자리 전부 + 환자 설명 4개 국어 + V3.1-7 필수 고지(kind=disclosure). (kind, text, src)"""
    out = []
    for kind, text, src in V23.adverse_phrases23(L):
        out.append((kind, text, src))
        if kind == "evidence_statement":
            rec = src["locator"].split("@", 1)[1]
            ae = next(a for code_, cat_ in L["literature-evidence.json"]["categories"].items() if code_ == src["modality"] for i_, a in enumerate(cat_.get("adverse_effects") or []) if f"{code_}/{i_}" == rec)
            for lang in ("ko", "en", "zh", "ja"):
                if ae.get(f"patient_{lang}"):
                    out.append(("patient_text", ae[f"patient_{lang}"], dict(src, kind="patient_text", lang=lang, path=f"categories.{{code}}.adverse_effects[].patient_{lang}", origin=f"literature.patient_{lang}", locator=src["locator"].replace(".statement@", f".patient_{lang}@"), statement_locator=src["locator"], patient_ko=None)))
    for cat in L["consent-checklist.json"]["categories"]:
        for i, x in enumerate(cat.get("mandatory_disclosures") or []):
            out.append(("disclosure", x, {"origin": "consent.disclosure", "file": "consent-checklist.json", "path": "categories[].mandatory_disclosures[]", "modality": cat["id"], "record": i, "context": {"disclosure": True},
                                          "locator": locator("consent-checklist.json", "categories[].mandatory_disclosures[]", f"{cat['id']}/{i}")}))
    return out


def _from_end(src):
    ctx = src.get("context") or {}
    if ctx.get("item_name"):
        return ("procedure(item)", f"{src.get('modality')}/{ctx['item_name']}")
    if ctx.get("product_name"):
        return ("product", f"{src.get('modality')}/{ctx['product_name']}")
    return ("modality", str(src.get("modality")))


def run_adverse31(ids, rules, L, v3tup=None):
    rules = rules["adverse"] if "adverse" in rules else rules
    AT = AdverseUnits31(ids, rules)
    # ---- ① complications 65 이름 → 단위(세 칸) · category → 단위 R15(course)
    comp_rows = []
    name_edges = OrderedDict()
    for cat in L["complications.json"]["categories"]:
        for i, c in enumerate(cat["complications"]):
            loc = locator("complications.json", "categories[].complications[].name", f"{cat['id']}/{i}")
            r = AT.run_name(c["name"], {"origin": "complications", "file": "complications.json", "path": "categories[].complications[].name", "modality": cat["id"], "record": i, "locator": loc})
            r.update({"modality": cat["id"], "severity": c.get("severity"), "record": i})
            comp_rows.append(r)
            for uid in r["unit_ids"]:
                k = (("modality", cat["id"]), uid)
                e = name_edges.setdefault(k, {"from": ("modality", cat["id"]), "unit": uid, "courses": [], "names": []})
                e["courses"] = _dedupe(e["courses"] + [co for c in r["candidates"] if c.get("unit_id") == uid or (r["event_kind"] == "dict" and AT.units.get((c["event_id"], c["site_id"], c["qualifier_id"])) == uid) for co in c["courses"]])
                e["names"].append(loc)
    units_before = len(AT.tuples)
    name_units = set(AT.tuples)
    # ---- ② 문구 → 문구 사전 항목(정규화형) · auto 면 단위(없으면 생성) · R15 source_phrases
    occ = adverse_phrases31(L)
    entries = OrderedDict()
    occ_rows = []
    for kind, text, src in occ:
        src = dict(src, kind=kind)
        if kind == "patient_text" and src.get("lang") != "ko":
            occ_rows.append({"kind": kind, "lang": src["lang"], "text": text, "locator": src["locator"], "statement_locator": src["statement_locator"], "translation": True, "modality": src.get("modality"), "origin": src["origin"]})
            continue
        ev = AT.evaluate(text, src)
        key = ev["normalized"] or norm(text)
        e = entries.get(key)
        if e is None:
            e = OrderedDict([("id", mkid("PHR", key)), ("normalized", key), ("raw_variants", []), ("kinds", []), ("langs", []), ("locators", []), ("modality_codes", []), ("contexts", []), ("status", ev["status"]), ("reasons", ev["reasons"]),
                             ("units", []), ("created_units", []), ("candidates", ev["candidates"]), ("parsed", dict(ev["parsed"], events=ev["event_fragments"], sites=_dedupe(c["site"] for c in ev["candidates"] if c["site"]), relative_sites=ev["relative_sites"], courses=ev["courses"], qualifiers=ev["qualifiers"], phrase_shape=ev["phrase_shape"])),
                             ("unregistered", ev["unregistered"]), ("extra_sites", ev["extra_sites"]), ("extra_courses", ev["extra_courses"]), ("extra_qualifiers", ev["extra_qualifiers"]), ("fragment_classes", ev["fragment_classes"]), ("spans", ev["spans"]), ("dict_tuples", ev["dict_tuples"]), ("b_splits", ev["b_splits"]), ("site_list_merges", ev["site_list_merges"]), ("tuples", ev["tuples"]),
                             ("translations", []), ("citations", []), ("accuracy", []), ("_uc", ev["unit_candidates"]), ("status_mismatch", 0)])
            entries[key] = e
        else:
            if e["status"] != ev["status"]:
                e["status_mismatch"] += 1
        if text not in e["raw_variants"]:
            e["raw_variants"].append(text)
        if kind not in e["kinds"]:
            e["kinds"].append(kind)
        lang = src.get("lang") or ("en" if kind == "evidence_statement" else "ko")
        if lang not in e["langs"]:
            e["langs"].append(lang)
        e["locators"].append(src["locator"])
        if src.get("modality") and src["modality"] not in e["modality_codes"]:
            e["modality_codes"].append(src["modality"])
        e["contexts"].append({"locator": src["locator"], "kind": kind, "origin": src["origin"], "from": _from_end(src), "modality": src.get("modality"), "context": src.get("context") or {}})
        occ_rows.append({"kind": kind, "lang": lang, "text": text, "locator": src["locator"], "phrase_id": e["id"], "status": e["status"], "phrase_shape": e["parsed"]["phrase_shape"], "modality": src.get("modality"), "origin": src["origin"], "from": _from_end(src), "translation": False})
    # 문헌 인용·정확도 → 항목
    for code, cat in L["literature-evidence.json"]["categories"].items():
        for i, ae in enumerate(cat.get("adverse_effects") or []):
            loc = locator("literature-evidence.json", "categories.{code}.adverse_effects[].statement", f"{code}/{i}")
            loc_ko = loc.replace(".statement@", ".patient_ko@")
            for e in entries.values():
                if loc in e["locators"] or loc_ko in e["locators"]:
                    e["citations"] = _dedupe(e["citations"] + [str(c_.get("pmid") or c_.get("url") or c_) for c_ in (ae.get("citations") or [])])
                    if loc in e["locators"]:
                        e["accuracy"].append({"locator": loc, "score": ae.get("accuracy_score"), "note": ae.get("accuracy_note"), "added_at": ae.get("added_at")})
                    for lang in ("en", "zh", "ja"):
                        if ae.get(f"patient_{lang}"):
                            tr = {"lang": lang, "text": ae[f"patient_{lang}"], "locator": loc.replace(".statement@", f".patient_{lang}@"), "record": loc}
                            if tr not in e["translations"]:
                                e["translations"].append(tr)
    # auto → 단위(생성/연결) · 첫 출현 순
    for e in entries.values():
        if e["status"] == "auto":
            src0 = {"origin": e["contexts"][0]["kind"], "locator": e["locators"][0], "phrase_id": e["id"], "kind": e["contexts"][0]["kind"]}
            ids_ = []
            for c in e["_uc"]:
                key = AT.unit_key(c)
                existed = key in AT.units
                tid = AT.register_unit(c, src0)
                ids_.append(tid)
                if not existed:
                    e["created_units"].append(tid)
                    AT.created[tid] = e["id"]
                    AT.tuples[tid]["created_by_phrase"] = e["id"]
            e["units"] = _dedupe(ids_)
            for c in e["candidates"]:
                key = (c["event_id"], c["site_id"], c["qualifier_id"])
                c["exists"] = key in AT.units
                c["unit_id"] = AT.units.get(key)
        e.pop("_uc", None)
    # 단위 explanations · R15 phrase edges
    phrase_edges = OrderedDict()
    for e in entries.values():
        if e["status"] != "auto":
            continue
        for ctx in e["contexts"]:
            for uid in e["units"]:
                k = (ctx["from"], uid)
                pe = phrase_edges.setdefault(k, {"from": ctx["from"], "unit": uid, "source_phrases": [], "courses": [], "kinds": [], "disclosure": False, "created_by_phrase": uid in AT.created})
                if e["id"] not in pe["source_phrases"]:
                    pe["source_phrases"].append(e["id"])
                pe["courses"] = _dedupe(pe["courses"] + [co for c in e["candidates"] if c.get("unit_id") == uid for co in c["courses"]])   # S-1: 그 단위 후보의 경과만(원칙 C)
                if ctx["kind"] not in pe["kinds"]:
                    pe["kinds"].append(ctx["kind"])
                if ctx["kind"] == "disclosure":
                    pe["disclosure"] = True
        for uid in e["units"]:
            for ctx in e["contexts"]:
                AT.tuples[uid]["explanations"].append({"phrase_id": e["id"], "kind": ctx["kind"], "lang": e["langs"][0] if e["langs"] else None, "locator": ctx["locator"]})
            for tr in e["translations"]:
                AT.tuples[uid]["explanations"].append({"phrase_id": e["id"], "kind": "patient_text", "lang": tr["lang"], "locator": tr["locator"]})
    # 번역 자리의 바구니
    stmt_status = {}
    for e in entries.values():
        for loc in e["locators"]:
            stmt_status[loc] = e["status"]
    for r in occ_rows:
        if r.get("translation"):
            loc_ko = r["statement_locator"].replace(".statement@", ".patient_ko@")
            st = "auto" if "auto" in (stmt_status.get(r["statement_locator"], "unlinked"), stmt_status.get(loc_ko, "unlinked")) else "unlinked"
            r["status"] = st
            r["phrase_id"] = next((e["id"] for e in entries.values() if r["statement_locator"] in e["locators"] or loc_ko in e["locators"]), None)
            r["bucket"] = "unit_explanation" if st == "auto" else "gate"
        else:
            r["bucket"] = "edge_attachment" if r["status"] == "auto" else "gate"
    A = AT.tuples
    units_after = len(A)
    created_units = [A[t] for t in AT.created]
    created_bad = [t for t in AT.created if not A[t]["all_dict_values"] or A[t]["unregistered_fragments"] or A[t]["event_kind"] != "dict"]
    all_edges = OrderedDict()
    for k, e in name_edges.items():
        all_edges[k] = dict(e, source_phrases=[], from_names=True, created_by_phrase=False)
    for k, e in phrase_edges.items():
        if k in all_edges:
            all_edges[k]["source_phrases"] = e["source_phrases"]
            all_edges[k]["courses"] = _dedupe(all_edges[k]["courses"] + e["courses"])
        else:
            all_edges[k] = dict(e, from_names=False, names=[])
    # 검산 재료: 엣지 경과·정도 값이 문구 항목을 가리킴
    ent_by_id = {e["id"]: e for e in entries.values()}
    bad_edge_course = []
    for k, e in all_edges.items():
        pool = set(e["courses"])
        ref = set()
        for pid in e["source_phrases"]:
            ref |= {co for c in ent_by_id[pid]["candidates"] if c.get("unit_id") == e["unit"] for co in c["courses"]}
        for loc in e.get("names", []):
            r = next(x for x in comp_rows if x["locator"] == loc)
            ref |= {co for c in r["candidates"] if AT.units.get((c["event_id"], c["site_id"], c["qualifier_id"])) == e["unit"] for co in c["courses"]}
        if pool - ref:
            bad_edge_course.append(k)
    # ---- 집계
    adv_folded = []
    comp_unit_ids = _dedupe(x for r in comp_rows for x in r["unit_ids"])
    for tid in comp_unit_ids:
        rows_ = [r for r in comp_rows if tid in r["unit_ids"]]
        names = [f"{r['text']} [{r['modality']}]" for r in rows_]
        own_unreg = _dedupe(u for r in rows_ for u in r["unregistered"])
        t = A[tid]
        adv_folded.append({"adverse_id": tid, "event_kind": t["event_kind"], "event": t["event"], "category": t["event_category"], "site_kind": t["site_kind"], "site": t["site"], "site_dict_kind": t.get("site_dict_kind"), "qualifier": t["qualifier"], "status": t["status"] if t["event_kind"] == "raw_name" else ("partial" if own_unreg else "complete"),
                           "all_dict_values": t["all_dict_values"], "anchor": t["anchor"], "n_names": len(names), "names": names, "unregistered": own_unreg, "event_fragments": t["event_fragments"], "extra_sites": t["extra_sites"], "extra_courses": t.get("extra_courses", []), "extra_qualifiers": t["extra_qualifiers"],
                           "dict_tuples": t.get("dict_tuples"), "raw_reason": t.get("raw_reason"), "site_basis": t.get("site_basis"), "qualifier_basis": t.get("qualifier_basis"), "relative_site_text": t["relative_site_text"], "edge_courses": _dedupe(co for r in rows_ for co in r["courses"]), "phrase_sources": sum(1 for s_ in t["sources"] if s_["origin"] != "complications")})
    adv_folded.sort(key=lambda x: (-x["n_names"], x["event_kind"], x["category"] or "", x["event"], x["qualifier"] or ""))
    raw = [t for t in A.values() if t["event_kind"] == "raw_name"]
    dict_t = [t for t in A.values() if t["event_kind"] == "dict"]
    af2 = [f for f in adv_folded if f["n_names"] >= 2]
    all_rows = comp_rows + list(entries.values())
    site_outside_member = [(r["text"] if "text" in r else r["normalized"], t[:3]) for r in all_rows for t in r["tuples"] if t[1] and t[4] not in ("member", "site_list")]
    site_list_merges = [{"text": r.get("text") or r["normalized"], "merges": r["site_list_merges"]} for r in all_rows if r.get("site_list_merges")]
    multi_cand = [{"text": r.get("text") or r["normalized"], "tuples": [t[:3] + (t[5],) for t in r["b_splits"]], "site_candidates": max(t[3] for t in r["b_splits"]), "course_candidates": max(t[4] for t in r["b_splits"]), "qualifier_candidates": max(t[6] for t in r["b_splits"])} for r in all_rows if r.get("b_splits")]
    headache_injection = [t["id"] for t in A.values() if t["event"] == "두통" and t["site"] == "주사 부위"]
    unattached = [{"text": r.get("text") or r["normalized"], "extra_sites": r["extra_sites"], "extra_courses": r["extra_courses"], "extra_qualifiers": r["extra_qualifiers"]} for r in all_rows if r["extra_sites"] or r["extra_courses"] or r["extra_qualifiers"]]
    raw_cells = {"n": len(raw), "site_none": sum(1 for t in raw if t["site_id"] == "none"), "qualifier_none": sum(1 for t in raw if t["qualifier_id"] == "none"), "with_dict_tuples": sum(1 for t in raw if t.get("dict_tuples")),
                 "by_reason": dict(Counter(t["raw_reason"] for t in raw)), "with_extra_sites": sum(1 for t in raw if t["extra_sites"]), "with_extra_courses": sum(1 for t in raw if t.get("extra_courses")), "with_extra_qualifiers": sum(1 for t in raw if t["extra_qualifiers"])}
    adv_unreg = Counter()
    adv_unreg_by_origin = defaultdict(Counter)
    for r in comp_rows:
        for u in r["unregistered"]:
            adv_unreg[u] += 1
            adv_unreg_by_origin["complications"][u] += 1
    for e in entries.values():
        for u in e["unregistered"]:
            adv_unreg[u] += len(e["locators"])
            for k_ in e["kinds"]:
                adv_unreg_by_origin[k_][u] += 1
    by_event = OrderedDict()
    for t in sorted(dict_t, key=lambda t: (t["event"], t["site"] or "", t["qualifier"] or "")):
        by_event.setdefault(t["event"], []).append({"id": t["id"], "site": t["site"], "site_dict_kind": t.get("site_dict_kind"), "qualifier": t["qualifier"], "created_by_phrase": t["created_by_phrase"], "origins": t["origins"], "sources": len(t["sources"]), "relative_site_text": t["relative_site_text"], "edge_courses": dict(AT.unit_courses.get(t["id"], {}))})
    event_combo_table = [{"event": ev, "combos": len(us), "from_names": sum(1 for u in us if not u["created_by_phrase"]), "created": sum(1 for u in us if u["created_by_phrase"]), "units": us} for ev, us in sorted(by_event.items(), key=lambda kv: (-len(kv[1]), kv[0]))]
    sw = rules["adverse_stopwords"]
    v3unreg = dict((v3tup or {}).get("adverse", {}).get("summary", {}).get("unregistered_all", [])) if v3tup else {}
    stop_table = [{"word": w["word"], "class": w["class"], "hits": AT.stop_hits.get(w["word"], 0), "locators": AT.stop_locs.get(w["word"], [])[:12], "v3_unregistered": v3unreg.get(w["word"], 0)} for w in sw["words"]]
    pat_table = [{"class": p["class"], "regex": p["regex"], "note": p["note"], "hits": AT.pat_hits.get(p["regex"], 0), "locators": AT.pat_locs.get(p["regex"], [])[:12]} for p in sw["patterns"]]
    class_counter = Counter()
    tokens_total = 0
    unclassified = []
    for r in all_rows:
        for fc in r.get("fragment_classes") or []:
            tokens_total += 1
            class_counter[fc["class"]] += 1
            if fc["class"] not in rules["fragment_classes"]:
                unclassified.append((r.get("text") or r["normalized"], fc))
    E = list(entries.values())
    nontrans = [r for r in occ_rows if not r.get("translation")]
    shape_by_kind = {k: dict(Counter(r["phrase_shape"] for r in nontrans if r["kind"] == k)) for k in dict.fromkeys(r["kind"] for r in nontrans)}
    shape_by_status = {s: dict(Counter(r["phrase_shape"] for r in nontrans if r["status"] == s)) for s in ("auto", "unlinked")}
    inc_cond = [{"normalized": e["normalized"], "variants": e["raw_variants"][:3], "kinds": e["kinds"], "locators": len(e["locators"]), "incidence": e["parsed"]["incidence"], "condition": e["parsed"]["condition"], "status": e["status"]} for e in E if e["parsed"]["phrase_shape"] == "event_incidence_condition"]
    disc = [r for r in nontrans if r["kind"] == "disclosure"]
    disc_entries = [e for e in E if "disclosure" in e["kinds"]]
    disc_by_mod = OrderedDict()
    for r in disc:
        d = disc_by_mod.setdefault(r["modality"], {"n": 0, "auto": 0, "unlinked": 0})
        d["n"] += 1
        d["auto" if r["status"] == "auto" else "unlinked"] += 1
    seen_d = defaultdict(list)
    for r in disc:
        seen_d[norm(r["text"])].append(r["modality"])
    disc_shared = [{"text": next(r["text"] for r in disc if norm(r["text"]) == k), "modalities": v} for k, v in seen_d.items() if len(v) >= 2]
    disc_rows = [{"modality": r["modality"], "locator": r["locator"], "text": r["text"], "status": r["status"], "phrase_shape": r["phrase_shape"], "phrase_id": r["phrase_id"], "candidates": [(c["event"], c["site"], c["qualifier"], c["exists"]) for c in ent_by_id[r["phrase_id"]]["candidates"]], "courses": ent_by_id[r["phrase_id"]]["parsed"]["courses"], "created": ent_by_id[r["phrase_id"]]["created_units"], "unregistered": ent_by_id[r["phrase_id"]]["unregistered"], "reasons": ent_by_id[r["phrase_id"]]["reasons"]} for r in disc]
    occ_nodisc = [r for r in occ_rows if r["kind"] != "disclosure"]
    buckets = Counter(r["bucket"] for r in occ_nodisc)
    cmp = {}
    if v3tup:
        s3 = v3tup["adverse"]["summary"]
        ex3 = {r["locator"]: r["match_status"] for r in v3tup["adverse"]["expressions"]}
        trans = Counter((ex3.get(r["locator"]), r["status"]) for r in occ_nodisc if r["locator"] in ex3)
        cmp = {"units_v3": s3["tuples_total"], "units_v31_names_only": units_before, "units_v31": units_after, "complications_distinct_v3": s3["complications_distinct_tuples"], "complications_distinct_v31": len(comp_unit_ids),
               "exact_v3": s3["expressions_total"]["linked"], "auto_v31_same_sources": sum(1 for r in occ_nodisc if r["locator"] in ex3 and r["status"] == "auto"), "unlinked_v3": s3["expressions_total"]["unlinked"], "unlinked_v31_same_sources": sum(1 for r in occ_nodisc if r["locator"] in ex3 and r["status"] != "auto"),
               "transitions": {f"{a}→{b}": n for (a, b), n in trans.items()}, "unregistered_distinct_v3": s3["unregistered_distinct"], "unregistered_total_v3": s3["unregistered_total"], "expressions_v3": s3["expressions_total"]["n"], "patient_text_records_v3": s3["expressions_total"]["patient_text_records"]}
    summary = OrderedDict([
        ("principles", rules.get("principles")),
        ("complications_names", len(comp_rows)), ("complications_names_with_tuple", sum(1 for r in comp_rows if r["unit_ids"])), ("complications_names_without_tuple", [f"{r['text']} [{r['modality']}]" for r in comp_rows if not r["unit_ids"]]),
        ("complications_names_multi_tuple", sum(1 for r in comp_rows if len(r["unit_ids"]) >= 2)), ("complications_names_raw", sum(1 for r in comp_rows if r["event_kind"] == "raw_name")), ("complications_names_raw_by_reason", dict(Counter(r["raw_reason"] for r in comp_rows if r["event_kind"] == "raw_name"))), ("complications_names_dict", sum(1 for r in comp_rows if r["event_kind"] == "dict")),
        ("complications_distinct_tuples", len(comp_unit_ids)), ("complications_distinct_tuples_dict", sum(1 for t in comp_unit_ids if A[t]["event_kind"] == "dict")), ("complications_distinct_tuples_raw", sum(1 for t in comp_unit_ids if A[t]["event_kind"] == "raw_name")), ("complications_fold_ratio", round(len(comp_unit_ids) / len(comp_rows), 3)),
        ("complications_tuples_with_2plus_names", len(af2)), ("complications_folded_all_dict_values", sum(1 for f in af2 if f["all_dict_values"] and not f["unregistered"])), ("complications_folded_with_unregistered", sum(1 for f in af2 if f["unregistered"])),
        ("complications_by_site_kind", dict(Counter(A[t]["site_kind"] for t in comp_unit_ids))), ("complications_by_qualifier", dict(Counter(A[t]["qualifier"] or "none" for t in comp_unit_ids))), ("complications_by_category", dict(Counter(A[t]["event_category"] for t in comp_unit_ids))),
        ("complications_edge_courses", dict(Counter(co for e in name_edges.values() for co in e["courses"]))), ("complications_edges", len(name_edges)),
        ("event_dictionary_values", len(ids.event)), ("event_dictionary_used_by_complications", len({A[t]["event"] for t in comp_unit_ids if A[t]["event_kind"] == "dict"})), ("event_dictionary_unused", sorted(set(e["label"] for e in ids.event.values()) - {t["event"] for t in dict_t})), ("event_dictionary_used_by_any_unit", len({t["event"] for t in dict_t})),
        ("course_dictionary_values", len(ids.course)), ("relative_site_values", len(ids.rsite)), ("qualifier_dictionary_values", len(ids.qualifier)), ("site_dictionary_values", len(ids.site)), ("site_dictionary_by_kind", dict(Counter(ids.site_kind.values()))),
        ("course_member_only", True), ("site_member_only", True), ("qualifier_member_only", True), ("expressions_create_units", "all_dict_cells_only"), ("expressions_create_raw_units", False), ("qualifier_none_is_value", True), ("course_is_edge_attribute", True), ("relative_site_is_none", True),
        ("lop", [{"name": r["text"], "event_kind": r["event_kind"], "dict_tuples": r["dict_tuples"], "edge_courses": r["courses"]} for r in comp_rows if "LOP" in r["text"]]),
        ("site_outside_member", len(site_outside_member)), ("site_list_merges", len(site_list_merges)), ("site_list_merges_all", site_list_merges), ("multi_candidate_splits", len(multi_cand)), ("multi_candidate_splits_all", multi_cand),
        ("headache_x_injection_site_tuples", headache_injection), ("unattached_fragments_texts", len(unattached)), ("unattached_fragments_all", unattached), ("raw_cells", raw_cells),
        ("tuples_total", len(A)), ("tuples_dict", len(dict_t)), ("tuples_raw_name", len(raw)), ("tuples_by_origin", OrderedDict((o, sum(1 for t in A.values() if o in t["origins"])) for o in dict.fromkeys(o for t in A.values() for o in t["origins"]))),
        ("tuples_status", dict(Counter(t["status"] for t in A.values()))), ("tuples_by_site_kind", dict(Counter(t["site_kind"] for t in A.values()))), ("tuples_by_site_dict_kind", dict(Counter(str(t.get("site_dict_kind")) for t in dict_t))), ("tuples_by_qualifier", dict(Counter(t["qualifier"] or "none" for t in A.values()))), ("tuples_by_category", dict(Counter(t["event_category"] for t in A.values()))),
        ("tuples_all_dict_values", sum(1 for t in A.values() if t["all_dict_values"])), ("tuples_with_relative_site_text", sum(1 for t in A.values() if t["relative_site_text"])),
        ("folded_with_2plus_names", len(af2)), ("folded_with_partial_name", sum(1 for f in af2 if f["status"] == "partial")),
        ("unregistered_distinct", len(adv_unreg)), ("unregistered_total", sum(adv_unreg.values())), ("unregistered_all", adv_unreg.most_common()), ("unregistered_by_origin", {k: v.most_common() for k, v in adv_unreg_by_origin.items()}),
        ("qualifier_tuples", sum(1 for t in A.values() if t["qualifier_id"] != "none")), ("qualifier_tuples_all", [{"id": t["id"], "event": t["event"], "site": t["site"], "qualifier": t["qualifier"], "event_kind": t["event_kind"], "basis": t.get("qualifier_basis"), "created_by_phrase": t["created_by_phrase"]} for t in A.values() if t["qualifier_id"] != "none"]), ("prefix_splits", _dedupe(AT.prefix_splits)),
        ("layer_site_tuples", sum(1 for t in dict_t if t.get("site_dict_kind") == "layer")), ("layer_site_tuples_all", [{"id": t["id"], "event": t["event"], "site": t["site"], "created_by_phrase": t["created_by_phrase"]} for t in dict_t if t.get("site_dict_kind") == "layer"]),
        # V3.1-9 · V3.1-10
        ("units_before_phrases", units_before), ("units_after_phrases", units_after), ("units_created_by_phrases", len(AT.created)), ("units_created_bad", created_bad), ("units_created_all_dict", all(t["all_dict_values"] for t in created_units)), ("units_created_with_unregistered", sum(1 for t in created_units if t["unregistered_fragments"])),
        ("units_created_by_event", dict(Counter(t["event"] for t in created_units))), ("units_created_by_site_kind", dict(Counter(t["site_kind"] for t in created_units))), ("units_created_by_qualifier", dict(Counter(t["qualifier"] or "none" for t in created_units))),
        ("event_combo_table", event_combo_table), ("events_with_2plus_combos", sum(1 for e in event_combo_table if e["combos"] >= 2)), ("events_with_1_combo", sum(1 for e in event_combo_table if e["combos"] == 1)),
        ("phrase_occurrences", len(occ_rows)), ("phrase_occurrences_without_disclosure", len(occ_nodisc)), ("phrase_occurrences_by_kind", dict(Counter(r["kind"] for r in occ_rows))), ("phrase_translations", sum(1 for r in occ_rows if r.get("translation"))),
        ("phrase_entries", len(E)), ("phrase_entries_by_status", dict(Counter(e["status"] for e in E))), ("phrase_entries_by_kind", dict(Counter(k for e in E for k in e["kinds"]))), ("phrase_entries_multi_variant", sum(1 for e in E if len(e["raw_variants"]) >= 2)), ("phrase_entries_multi_kind", sum(1 for e in E if len(e["kinds"]) >= 2)), ("phrase_entries_status_mismatch", sum(e["status_mismatch"] for e in E)),
        ("phrase_occurrences_by_status", dict(Counter(r["status"] for r in occ_nodisc))), ("phrase_buckets", dict(buckets)), ("phrase_buckets_sum_ok", sum(buckets.values()) == len(occ_nodisc)), ("phrase_unlinked_reasons", dict(Counter(x for e in E for x in e["reasons"] for _ in e["locators"]))),
        ("edges_course_member_level", True), ("edges_from_names", len(name_edges)), ("edges_from_phrases", len(phrase_edges)), ("edges_total", len(all_edges)), ("edges_with_source_phrases", sum(1 for e in all_edges.values() if e["source_phrases"])), ("edges_with_course", sum(1 for e in all_edges.values() if e["courses"])), ("edges_by_course", dict(Counter(co for e in all_edges.values() for co in e["courses"]))), ("edges_by_from_kind", dict(Counter(e["from"][0] for e in all_edges.values()))), ("edges_course_not_from_phrase", len(bad_edge_course)), ("edges_disclosure", sum(1 for e in all_edges.values() if e.get("disclosure"))),
        ("adverse_stopwords", {"threshold": sw["threshold"], "words_total": len(stop_table), "words_with_locator": sum(1 for w in stop_table if w["locators"]), "words_without_locator": [w["word"] for w in stop_table if not w["locators"]], "by_class": dict(Counter(w["class"] for w in stop_table)), "words": stop_table, "patterns": pat_table, "patterns_with_locator": sum(1 for p in pat_table if p["locators"]), "hits_total": sum(AT.stop_hits.values()) + sum(AT.pat_hits.values())}),
        ("fragment_classes_total", tokens_total), ("fragment_classes_by_class", dict(class_counter)), ("fragment_classes_unclassified", unclassified[:20]),
        ("phrase_shape", dict(Counter(r["phrase_shape"] for r in nontrans))), ("phrase_shape_entries", dict(Counter(e["parsed"]["phrase_shape"] for e in E))), ("phrase_shape_by_kind", shape_by_kind), ("phrase_shape_by_status", shape_by_status), ("incidence_condition_entries", len(inc_cond)), ("incidence_condition_all", inc_cond),
        ("disclosures", {"n": len(disc), "modalities": len(disc_by_mod), "distinct_sentences": len({norm(r["text"]) for r in disc}), "phrase_entries": len(disc_entries), "shared_sentences": disc_shared, "by_modality": disc_by_mod, "auto": sum(1 for r in disc if r["status"] == "auto"), "unlinked": sum(1 for r in disc if r["status"] != "auto"), "created_units": len({x for e in disc_entries for x in e["created_units"]}), "events_mentioned": sorted({c["event"] for e in disc_entries for c in e["candidates"]}), "rows": disc_rows}),
        ("v3_comparison", cmp),
    ])
    return OrderedDict([("summary", summary), ("tuples", list(A.values())), ("complications", comp_rows), ("folded", adv_folded), ("phrase_dictionary", E), ("phrase_occurrences", occ_rows), ("edges", [dict(e, from_=list(e["from"])) for e in all_edges.values()]), ("created_units", created_units)])


# ---------------------------------------------------------------------------
# 조건 축 — V3.1-4
# ---------------------------------------------------------------------------
COND_PAREN = re.compile(r"\(([^()]*)\)")
COND_SPLIT = re.compile(r"[·/,+]|\s및\s|\s또는\s|--|—|:|;")
COND_STRIP = "*'\"“”‘’.…`~!?"


class ConditionTuples:
    def __init__(self, dic_json, rules):
        D = {d["name"]: d for d in dic_json["dictionaries"]}
        self.entries = {}
        self.surface = {}
        for e in D["person_condition"]["entries"]:
            self.entries[norm(e["canonical"])] = {"id": e["id"], "label": e["canonical"], "kinds": e.get("kinds") or []}
            self.surface[norm(e["canonical"])] = e["canonical"]
            for s in e.get("synonyms", []):
                self.surface[norm(s["value"])] = e["canonical"]
        self.markers = {norm(m): m for m in rules["markers"]}
        self.kind_by = rules["kind_by_source"]
        self.maxlen = 6
        self.units = OrderedDict()
        self.marker_hits = Counter()
        self.marker_locs = defaultdict(list)

    def split(self, text, loc=None):
        parens = COND_PAREN.findall(text)
        outer = COND_PAREN.sub(" ", text)
        groups = []
        for where, g in [("outer", outer)] + [("inner", p) for p in parens]:
            members = []
            for part in COND_SPLIT.split(g):
                toks = [t.strip(COND_STRIP) for t in part.split()]
                toks = [t for t in toks if t]
                if not toks:
                    continue
                spans, untouched, marks = [], [], []
                i = 0
                while i < len(toks):
                    found = None
                    for j in range(min(len(toks), i + self.maxlen), i, -1):
                        key = norm("".join(toks[i:j]))
                        if key in self.surface:
                            found = (self.surface[key], " ".join(toks[i:j]), j)
                            break
                    if found:
                        spans.append({"canonical": found[0], "text": found[1]})
                        i = found[2]
                        continue
                    if norm(toks[i]) in self.markers:
                        marks.append(toks[i])
                        self.marker_hits[self.markers[norm(toks[i])]] += 1
                        if loc and len(self.marker_locs[self.markers[norm(toks[i])]]) < 12:
                            self.marker_locs[self.markers[norm(toks[i])]].append(loc)
                    else:
                        untouched.append(toks[i])
                    i += 1
                members.append({"text": part.strip(), "spans": spans, "untouched": untouched, "markers": marks, "where": where})
            groups.append({"where": where, "members": members})
        return groups

    def run(self, f, p, rec, text, modality_code, level_hint):
        key = f"{f}:{p}"
        kind = self.kind_by[key]
        loc = locator(f, p, rec)
        if norm(text) in self.surface:
            groups = [{"where": "outer", "members": [{"text": text, "spans": [{"canonical": self.surface[norm(text)], "text": text}], "untouched": [], "markers": [], "where": "outer"}]}]
        else:
            groups = self.split(text, loc)
        cores = _dedupe(s["canonical"] for g in groups for m in g["members"] for s in m["spans"])
        untouched = [u for g in groups for m in g["members"] for u in m["untouched"]]
        marks = [x for g in groups for m in g["members"] for x in m["markers"]]
        expl = [m["text"] for g in groups if g["where"] == "inner" for m in g["members"]]
        src = {"locator": loc, "file": f, "path": p, "rec": rec, "kind": kind, "modality_code": modality_code, "level_hint": level_hint, "text": text}
        if untouched or not cores:
            uid = mkid("CND", f"RAW:{kind}|{norm(text)}")
            u = self.units.get(uid)
            if u is None:
                u = {"id": uid, "name_kind": "raw_name", "name": text, "kind": kind, "dictionary_id": None, "candidate_name": untouched, "condition_fragments": cores, "qualifier_text": _dedupe(marks), "anchor": loc, "sources": [], "explanation_text": expl, "status": "partial" if untouched else "unresolved", "phrases": []}
                self.units[uid] = u
            u["sources"].append(loc)
            status = "raw"
            unit_ids = [uid]
        else:
            unit_ids = []
            for c in cores:
                uid = mkid("CND", f"{kind}|{c}")
                u = self.units.get(uid)
                if u is None:
                    u = {"id": uid, "name_kind": "dict", "name": c, "kind": kind, "dictionary_id": self.entries[norm(c)]["id"], "candidate_name": [], "condition_fragments": [c], "qualifier_text": [], "anchor": None, "sources": [], "explanation_text": [], "status": "complete", "phrases": []}
                    self.units[uid] = u
                u["sources"].append(loc)
                u["qualifier_text"] = _dedupe(u["qualifier_text"] + marks)
                unit_ids.append(uid)
            status = "exact"
        ph = {"locator": loc, "text": text, "kind": kind, "modality_code": modality_code, "level_hint": level_hint, "match": status, "condition_fragments": cores, "unregistered_fragments": untouched, "qualifier_text": marks, "explanation_text": expl, "unit_ids": unit_ids,
              "groups": [{"where": g["where"], "members": [{"text": m["text"], "spans": [s["canonical"] for s in m["spans"]], "untouched": m["untouched"], "markers": m["markers"]} for m in g["members"]]} for g in groups]}
        for uid in unit_ids:
            self.units[uid].setdefault("phrases", []).append({k: ph[k] for k in ("locator", "text", "kind", "modality_code", "level_hint", "match", "condition_fragments", "unregistered_fragments", "qualifier_text", "explanation_text")})
        return ph


def run_condition(dic_json, rules, L):
    CT = ConditionTuples(dic_json, rules)
    occ = condition_occurrences(L)
    rows = [CT.run(*o) for o in occ]
    U = CT.units
    names_norm = {(r["kind"], norm(r["text"])) for r in rows}
    names_norm_nokind = {norm(r["text"]) for r in rows}
    dict_units = [u for u in U.values() if u["name_kind"] == "dict"]
    raw_units = [u for u in U.values() if u["name_kind"] == "raw_name"]
    # 접힌 표: 단위 → 이름(distinct 원문)
    folded = []
    for u in U.values():
        texts = _dedupe(r["text"] for r in rows if u["id"] in r["unit_ids"])
        folded.append({"unit_id": u["id"], "name_kind": u["name_kind"], "kind": u["kind"], "name": u["name"], "n_names": len(texts), "n_sources": len(u["sources"]), "names": texts, "candidate_name": u["candidate_name"], "condition_fragments": u["condition_fragments"], "qualifier_text": u["qualifier_text"]})
    folded.sort(key=lambda x: (x["name_kind"] != "dict", -x["n_names"], x["kind"], x["name"]))
    dict_names = {(r["kind"], norm(r["text"])) for r in rows if r["match"] == "exact"}
    raw_names = {(r["kind"], norm(r["text"])) for r in rows if r["match"] == "raw"}
    unreg = Counter(u for r in rows if r["match"] == "raw" for u in _dedupe(r["unregistered_fragments"]))
    cores_used = Counter(c for r in rows for c in r["condition_fragments"])
    D = {d["name"]: d for d in dic_json["dictionaries"]}
    core_entries = D["person_condition"]["entries"]
    cores_unused = [e["canonical"] for e in core_entries if cores_used.get(e["canonical"], 0) == 0]
    syn_used = Counter()
    for r in rows:
        for g in r["groups"]:
            for m in g["members"]:
                pass
    markers = [{"word": m, "hits": CT.marker_hits.get(m, 0), "locators": CT.marker_locs.get(m, [])[:12]} for m in rules["markers"]]
    multi = [r for r in rows if len(r["unit_ids"]) >= 2]
    by_kind_units = Counter(u["kind"] for u in U.values())
    summary = OrderedDict([
        ("occurrences", len(rows)), ("names_distinct", len(names_norm_nokind)), ("names_distinct_with_kind", len(names_norm)),
        ("names_dict", len(dict_names)), ("names_raw", len(raw_names)),
        ("units_total", len(U)), ("units_dict", len(dict_units)), ("units_raw", len(raw_units)),
        ("units_by_kind", dict(by_kind_units)), ("units_dict_by_kind", dict(Counter(u["kind"] for u in dict_units))), ("units_raw_by_kind", dict(Counter(u["kind"] for u in raw_units))),
        ("names_to_units", f"{len(names_norm_nokind)} → {len(U)} (kind 포함 {len(names_norm)} → {len(U)} · 사전 단위 {len(dict_units)} + raw {len(raw_units)})"),
        ("units_with_2plus_names", sum(1 for f in folded if f["n_names"] >= 2)), ("dict_units_with_2plus_names", sum(1 for f in folded if f["n_names"] >= 2 and f["name_kind"] == "dict")),
        ("raw_units_with_2plus_names", sum(1 for f in folded if f["n_names"] >= 2 and f["name_kind"] == "raw_name")),
        ("names_with_2plus_units", len(multi)), ("names_with_2plus_units_all", [{"text": r["text"], "kind": r["kind"], "units": [U[x]["name"] for x in r["unit_ids"]]} for r in multi]),
        ("phrases", len(rows)), ("phrases_by_match", dict(Counter(r["match"] for r in rows))), ("phrases_by_kind", dict(Counter(r["kind"] for r in rows))), ("phrases_attached", sum(len(u["phrases"]) for u in U.values())), ("phrases_attached_distinct", len({p["locator"] for u in U.values() for p in u["phrases"]})),
        ("phrases_create_units", False), ("fold_condition", rules["fold_condition"]),
        ("dictionary_values", len(core_entries)), ("dictionary_synonyms", sum(len(e["synonyms"]) for e in core_entries)), ("dictionary_values_used", len([c for c in cores_used if cores_used[c] > 0])), ("dictionary_values_unused", cores_unused),
        ("dictionary_by_kind", dict(Counter(e.get("kind") for e in core_entries))),
        ("markers", markers), ("markers_without_locator", [m["word"] for m in markers if not m["locators"]]),
        ("unregistered_distinct", len(unreg)), ("unregistered_total", sum(unreg.values())), ("unregistered_top", unreg.most_common(40)),
        ("raw_reasons", dict(Counter(u["status"] for u in raw_units))),
        ("isotretinoin", [{"text": r["text"], "kind": r["kind"], "status": r["match"], "units": [U[x]["name"] for x in r["unit_ids"]]} for r in rows if "이소트레티노인" in r["text"] or "레티노이드" in r["text"]]),
    ])
    return OrderedDict([("summary", summary), ("units", list(U.values())), ("phrases", rows), ("folded", folded)])


# ---------------------------------------------------------------------------
# V3.1-6 겹침 · V3.1-2 R32 후보 · V3.1-1 대상 예
# ---------------------------------------------------------------------------
def stopword_overlap(dic_json, resolve_rules):
    out = []
    for w in resolve_rules["step2_decompose"]["stopwords"]["words"]:
        hits = []
        for d in dic_json["dictionaries"]:
            for e in d["entries"]:
                if norm(e["canonical"]) == norm(w["word"]):
                    hits.append({"name": d["name"], "canonical": e["canonical"], "as": "canonical"})
                for s in e.get("synonyms", []):
                    if norm(s["value"]) == norm(w["word"]):
                        hits.append({"name": d["name"], "canonical": e["canonical"], "as": "synonym"})
        if hits:
            out.append({"word": w["word"], "dictionaries": hits})
    return out


def r32_candidates(L, ids):
    rows = []
    for sec, body in L["products.json"].items():
        if not isinstance(body, dict):
            continue
        for i, p in enumerate(body["products"]):
            for k in ("note", "legal_warning", "regulatory_status"):
                if p.get(k):
                    e = ids.prod.get(norm(p["name"]))
                    rows.append({"locator": locator("products.json", f"{sec}.products[].{k}", str(i)), "product": p["name"], "product_id": e["id"] if e else None, "family": body.get("category_id"), "key": k, "text": p[k]})
    for m in L["taxonomy.json"]["modality"]:
        for i, p in enumerate(m["products"]):
            for k in ("note", "legal_warning", "regulatory_status"):
                if p.get(k):
                    e = ids.prod.get(norm(p["name"]))
                    rows.append({"locator": locator("taxonomy.json", f"modality[].products[].{k}", f"{m['id']}/{i}"), "product": p["name"], "product_id": e["id"] if e else None, "family": m["id"], "key": k, "text": p[k]})
    return rows


def reclassify_examples(L, ids):
    """EXO-02 대상(ASCEplus · EXOSOME SKIN · M5 → M4)의 id 재계산 예 — 값은 결정, 여기는 규칙의 결과만."""
    out = []
    for name, to in (("ASCEplus", "M4"), ("EXOSOME SKIN", "M4")):
        e = ids.prod.get(norm(name))
        if e:
            out.append({"product": name, "family": e["family"], "current_id": e["id"], "to_modality_code": to, "new_id": mkid("PRD", f"{to}|{name}"), "alias_reclassified_from": e["id"], "collision": norm(name) in ids.prod and str(ids.prod[norm(name)]["family"]) == to})
    by_family = Counter(str(p["family"]) for p in ids.prod.values())
    return {"examples": out, "products_by_family": dict(by_family), "products_total": len(ids.prod)}


# ---------------------------------------------------------------------------
# 전체 실행
# ---------------------------------------------------------------------------
def run_all(dic_json, rules, L, resolve_rules=None, v3tup=None):
    if resolve_rules is None:
        sys.path.insert(0, HERE)
        import erd_spec_v31
        resolve_rules = erd_spec_v31.RESOLVE_RULES
    # v3 실행기에 v3.1 클래스를 꽂는다(같은 사전 · 같은 분해 순서)
    V3.ProcedureTuples3 = ProcedureTuples31
    V3.run_adverse = lambda ids, r, L_, v24tup=None: run_adverse31(ids, r, L_, v3tup)
    R = V3.run_all(dic_json, rules, L, resolve_rules, v24tup=None)
    R["erd_version"] = "v3.1"
    R["rules"] = rules["name"]
    R["expressions_create_units"] = "all_dict_cells_only"
    R["principles"] = rules.get("principles")
    ids = V3.Ids3(dic_json, L, resolve_rules)
    # V3.1-5 회·차 자리 실측
    sess = []
    for slot, rows in list(R["procedure"]["references"].items()) + [(MARKET_SLOT, R["procedure"]["market_pricing"])]:
        for r in rows:
            for t in r.get("session_tokens") or []:
                sess.append({"slot": slot, "relation": r.get("session_relation"), "label": r["label"], "hint": r.get("hint"), "token": t["token"], "kind": t["kind"], "value": t["value"], "target": r.get("session_target"), "result": r["result"],
                             "session_index": r.get("session_index"), "session_count": r.get("session_count"), "qualifier_text": r.get("qualifier_text")})
    for r in R["procedure"]["catalog"]:
        for t in _session_tokens(r.get("groups") or []):
            sess.append({"slot": "① taxonomy 항목", "relation": None, "label": r["name"], "hint": r["family"], "token": t["token"], "kind": t["kind"], "value": t["value"], "target": None, "result": r["result"], "session_index": None, "session_count": None, "qualifier_text": r.get("qualifier_text")})
    for r_ in R["procedure"]["edge_ends"]:
        r_["slot"] = r_["slot"].replace("(R29 → R15)", "(문구 사전 → R15 · v3.1)")
    ps = R["procedure"]["summary"]
    ps["session_tokens"] = sess
    ps["session_summary"] = {"total": len(sess), "by_kind": dict(Counter(s["kind"] for s in sess)), "by_relation": dict(Counter(str(s["relation"]) for s in sess)), "by_target": dict(Counter(str(s["target"]) for s in sess)),
                             "r12_session_index": sum(1 for s in sess if s["relation"] == "R12" and s["kind"] == "차"), "r12_session_count": sum(1 for s in sess if s["relation"] == "R12" and s["kind"] == "회"), "to_qualifier_text": sum(1 for s in sess if s["target"] == "qualifier_text")}
    # V3.1-6 겹침
    ov = stopword_overlap(dic_json, resolve_rules)
    ps["stopwords"]["overlap"] = ov
    ps["stopwords"]["overlap_words"] = [o["word"] for o in ov]
    ps["stopwords"]["dictionaries_checked"] = len(dic_json["dictionaries"])
    # V3.1-2 · V3.1-1
    R["r32_candidates"] = r32_candidates(L, ids)
    R["product_reclassify"] = reclassify_examples(L, ids)
    # V3.1-4 조건 축
    R["condition"] = run_condition(dic_json, rules["condition"], L)
    return R


def load_all():
    dic = None
    for name in ("erd-v3.1-dictionaries.json",):
        if os.path.exists(os.path.join(HERE, name)):
            dic = json.load(open(os.path.join(HERE, name), encoding="utf-8"))
    files = [f for f in os.listdir(LEDGER) if f.endswith(".json")]
    L = {f: json.load(open(os.path.join(LEDGER, f), encoding="utf-8")) for f in files}
    sys.path.insert(0, HERE)
    import erd_spec_v31 as S
    if dic is None:
        dic = json.load(open(os.path.join(HERE, "erd-v3-dictionaries.json"), encoding="utf-8"))
        dic = dict(dic, dictionaries=list(dic["dictionaries"]) + [condition_dictionary_json(L, S)])
    try:
        erd = json.load(open(os.path.join(HERE, "erd-v3.1.json"), encoding="utf-8"))
        rules, rrules = erd["tuple_rules"], erd["resolve_rules"]
    except (FileNotFoundError, KeyError):
        rules, rrules = S.TUPLE_RULES, S.RESOLVE_RULES
    v3 = None
    if os.path.exists(os.path.join(HERE, "erd-v3-tuples.json")):
        v3 = json.load(open(os.path.join(HERE, "erd-v3-tuples.json"), encoding="utf-8"))
    return dic, rules, rrules, L, v3


# ---------------------------------------------------------------------------
# 표
# ---------------------------------------------------------------------------
def _kv(d):
    return ", ".join(f"{k}={v}" for k, v in (d or {}).items())


def procedure_md(R, v3s=None):
    s = R["procedure"]["summary"]
    o = [V3.procedure_md(R, v3s)]
    A = o.append
    A("")
    A("#### 9.5.12 「회」·「N차」 자리 실측 (V3.1-5) — 규격 토큰이 든 참조 전부 · 자리의 관계 · 간 곳")
    A("")
    ss = s["session_summary"]
    A(f"- 규격 토큰 {ss['total']}(회 {ss['by_kind'].get('회', 0)} · 차 {ss['by_kind'].get('차', 0)}) · 자리의 관계 {_kv(ss['by_relation'])} · 간 곳 {_kv(ss['by_target'])} — R12.session_index {ss['r12_session_index']} · R12.session_count {ss['r12_session_count']} · qualifier_text(R9/R17/R18/③) {ss['to_qualifier_text']}.")
    A("")
    A(md_table(["#", "자리", "관계", "라벨", "토큰", "종류", "값", "간 곳", "결과", "session_index", "session_count", "qualifier_text"], [(i + 1, x["slot"][:45], x["relation"] or "—", x["label"], x["token"], x["kind"], x["value"], x["target"] or "—", x["result"], x["session_index"] if x["session_index"] is not None else "—", x["session_count"] if x["session_count"] is not None else "—", ", ".join(x["qualifier_text"] or []) or "—") for i, x in enumerate(s["session_tokens"])]))
    A("")
    A("#### 9.5.13 stopwords 와 사전 값 겹침 (V3.1-6) — 48 사전 전수")
    A("")
    st = s["stopwords"]
    A(f"- 사전 {st['dictionaries_checked']} 의 정준값·동의어와 정규화 완전 일치하는 stopword: **{len(st['overlap'])}** — " + (" · ".join(f"`{o['word']}` ↔ " + ", ".join(f"{h['name']}:{h['canonical']}({h['as']})" for h in o["dictionaries"]) for o in st["overlap"]) or "없음") + ". 분해 사전 7 과의 겹침(in_dictionary)은 §9.5.10 표 그대로(0). 규칙: 통째 일치가 먼저, stopword 는 남은 토큰에만.")
    return "\n".join(o)


def adverse_md(R, v3a=None):
    s = R["adverse"]["summary"]
    g = lambda k, d="—": (v3a or {}).get(k, d)  # noqa
    o = []
    A = o.append
    cmp = s.get("v3_comparison") or {}
    A("#### 9.6.1 complications 65 → 단위 (v3 → v3.1 나란히 · 단위 = (사건, 부위, 물질) · 경과는 엣지)")
    A("")
    A(md_table(["항목", "v3", "v3.1"], [
        ("이름", g("complications_names"), s["complications_names"]), ("단위가 생긴 이름", g("complications_names_with_tuple"), s["complications_names_with_tuple"]),
        ("raw_name 단위가 된 이름", f"**{g('complications_names_raw')}**", f"**{s['complications_names_raw']}** (사유 {_kv(s['complications_names_raw_by_reason'])} · 사전 단위 이름 {s['complications_names_dict']})"),
        ("사건이 둘 이상인 이름", g("complications_names_multi_tuple"), s["complications_names_multi_tuple"]),
        ("단위 수(distinct · 이름 유래)", f"**{g('complications_distinct_tuples')}** (사전 {g('complications_distinct_tuples_dict')} + raw {g('complications_distinct_tuples_raw')})", f"**{s['complications_distinct_tuples']}** (사전 {s['complications_distinct_tuples_dict']} + raw {s['complications_distinct_tuples_raw']} · 비율 {s['complications_fold_ratio']})"),
        ("둘 이상 이름이 접힌 단위", g("complications_tuples_with_2plus_names"), f"{s['complications_tuples_with_2plus_names']} (전부 사전 값 {s['complications_folded_all_dict_values']} · 미등록 섞임 **{s['complications_folded_with_unregistered']}**)"),
        ("경과", "단위 칸 " + _kv(g("complications_by_course", {})), "엣지 속성(category → 단위 R15 " + str(s["complications_edges"]) + " · course " + _kv(s["complications_edge_courses"]) + ")"),
        ("부위", _kv(g("complications_by_site_kind", {})), _kv(s["complications_by_site_kind"]) + " (상대 부위는 none · relative_site_text 보존)"),
        ("수식 칸", _kv(g("complications_by_qualifier", {})), _kv(s["complications_by_qualifier"])),
        ("분류", _kv(g("complications_by_category", {})), _kv(s["complications_by_category"])),
        ("사건 사전 값", f"**{g('event_dictionary_values')}**", f"**{s['event_dictionary_values']}** (어느 단위에도 안 쓰인 값: {', '.join(s['event_dictionary_unused']) or '없음'})"),
    ]))
    A("")
    A("#### 9.6.2 65 가 접힌 결과 — 단위마다 어떤 이름들이 갔는지 전부 (세 칸 · 엣지 경과 열)")
    A("")
    rows = [(i + 1, f["event_kind"], f["category"] or "—", f["event"] if f["event_kind"] == "dict" else f"(raw) {f['event']}", f"{f['site'] or 'none'}" + (f"({f['site_dict_kind']})" if f.get("site_dict_kind") else ""), f["qualifier"] or "none", ", ".join(f["edge_courses"]) or "—", ", ".join(f["relative_site_text"]) or "—", f["n_names"], " · ".join(f["names"]), ", ".join(f["unregistered"]) or "—",
             ((" + ".join(f"({t[0]}, {t[1] or 'none'}, {t[2]}, {t[3] or 'none'})" for t in (f["dict_tuples"] or [])) or "(사건 조각 없음)") if f["event_kind"] == "raw_name" else "—") + (f" / S:{','.join(f['extra_sites'])}" if f["extra_sites"] else "") + (f" / C:{','.join(f['extra_courses'])}" if f["extra_courses"] else "") + (f" / Q:{','.join(f['extra_qualifiers'])}" if f["extra_qualifiers"] else ""), f["phrase_sources"])
            for i, f in enumerate(R["adverse"]["folded"])]
    A(md_table(["#", "event_kind", "분류", "event", "site", "qualifier", "엣지 경과", "상대 부위(보존)", "이름 수", "접힌 complications 이름(전부)", "미등록 조각", "raw_name 의 사전 분해(보존만) / extra", "문구 출처 수"], rows))
    A("")
    A("#### 9.6.2b 부위·경과 규칙 실측 (원칙 B·C 그대로 · v3.1 상대 부위 none · 경과 엣지)")
    A("")
    A(f"- 사건 멤버 밖에서 온 site 가 들어간 단위·후보 **{s['site_outside_member']}** · 「두통 × 주사 부위」 단위 **{len(s['headache_x_injection_site_tuples'])}**(상대 부위는 칸이 아니다) · 부위 나열 합치기 {s['site_list_merges']} · 후보 둘 이상 분할 {s['multi_candidate_splits']} · 붙지 않은 조각 보존 {s['unattached_fragments_texts']} 문자열 · 상대 부위 조각을 보존한 단위 {s['tuples_with_relative_site_text']}.")
    for m in s["multi_candidate_splits_all"][:40]:
        A(f"  - 「{m['text'][:60]}」 → " + " + ".join(f"({t[0]}, {t[1] or 'none'}, {t[2]}, {t[3] or 'none'})" for t in m["tuples"]) + f" (부위 후보 {m['site_candidates']} · 경과 후보 {m['course_candidates']} · 수식 후보 {m['qualifier_candidates']})")
    for x in s["lop"]:
        A(f"- LOP: 「{x['name']}」 → event_kind={x['event_kind']} · 사전 분해 {' + '.join('(%s, %s, %s, %s)' % (t[0], t[1] or 'none', t[2], t[3] or 'none') for t in x['dict_tuples'])} · 엣지 경과 {x['edge_courses']}")
    A("")
    A("#### 9.6.2c raw_name 칸 실측")
    A("")
    rc = s["raw_cells"]
    A(f"- raw_name 단위 {rc['n']}: site none **{rc['site_none']}/{rc['n']}** · qualifier none **{rc['qualifier_none']}/{rc['n']}** · 사유 {_kv(rc['by_reason'])} · dict_tuples 보존 {rc['with_dict_tuples']} · extra_sites {rc['with_extra_sites']} · extra_courses {rc['with_extra_courses']} · extra_qualifiers {rc['with_extra_qualifiers']}")
    A("")
    A("#### 9.6.3 문구 → 문구 사전 → 단위 (V3.1-10 · auto / unlinked · v3 exact/unlinked 와 나란히 · 목표 수치 아님)")
    A("")
    A(f"- 문구 자리 **{s['phrase_occurrences']}**(고지 제외 {s['phrase_occurrences_without_disclosure']} = v3 표현 {cmp.get('expressions_v3', '—')} + 환자 설명 번역 {s['phrase_translations']} · kind 별 {_kv(s['phrase_occurrences_by_kind'])}) → 정규화형 항목 **{s['phrase_entries']}**(status {_kv(s['phrase_entries_by_status'])} · 표면형 둘 이상 {s['phrase_entries_multi_variant']} · kind 둘 이상 {s['phrase_entries_multi_kind']} · 같은 정규화형인데 판정이 다른 자리 {s['phrase_entries_status_mismatch']}).")
    A(f"- 자리 기준(고지 제외): {_kv(s['phrase_occurrences_by_status'])} · unlinked 사유(자리 수) {_kv(s['phrase_unlinked_reasons'])}. v3: exact {cmp.get('exact_v3')} · unlinked {cmp.get('unlinked_v3')} → v3.1 같은 자리 auto {cmp.get('auto_v31_same_sources')} · unlinked {cmp.get('unlinked_v31_same_sources')} · 전이 {_kv(cmp.get('transitions'))}.")
    A(f"- **부록 합(V3.1-10)**: 엣지 부록(R15 source_phrases) {s['phrase_buckets'].get('edge_attachment', 0)} + 단위 부록(explanations · 번역) {s['phrase_buckets'].get('unit_explanation', 0)} + 게이트(unlinked_phrases) {s['phrase_buckets'].get('gate', 0)} = {sum(s['phrase_buckets'].values())} = 자리 {s['phrase_occurrences_without_disclosure']} → {s['phrase_buckets_sum_ok']}.")
    A("")
    A("#### 9.6.4 단위 전체 집계 (이름 유래 + 문구가 세운 조합 · v3 → v3.1)")
    A("")
    A(md_table(["항목", "v3", "v3.1"], [
        ("단위 수", f"**{g('tuples_total')}**", f"**{s['tuples_total']}** (사전 {s['tuples_dict']} + raw_name {s['tuples_raw_name']}) — 이름만 {s['units_before_phrases']} → 문구 뒤 {s['units_after_phrases']}(문구가 세운 조합 {s['units_created_by_phrases']})"),
        ("원천별", _kv(g("tuples_by_origin", {})), _kv(s["tuples_by_origin"])), ("상태", _kv(g("tuples_status", {})), _kv(s["tuples_status"])),
        ("부위", _kv(g("tuples_by_site_kind", {})), _kv(s["tuples_by_site_kind"]) + " · site kind " + _kv(s["tuples_by_site_dict_kind"])), ("수식 칸", _kv(g("tuples_by_qualifier", {})), _kv(s["tuples_by_qualifier"])), ("분류", _kv(g("tuples_by_category", {})), _kv(s["tuples_by_category"])),
        ("미등록 조각(자리 수)", f"distinct {g('unregistered_distinct')} · 총 {g('unregistered_total')}", f"distinct {s['unregistered_distinct']} · 총 {s['unregistered_total']} (수식어 목록 적용 후)"),
        ("R15 엣지(ERD 실측 · (from, 단위) 쌍)", "표현 exact 651 자리", f"이름 유래 {s['edges_from_names']} + 문구 유래 {s['edges_from_phrases']} = distinct **{s['edges_total']}** · course 있음 {s['edges_with_course']}({_kv(s['edges_by_course'])}) · from 종류 {_kv(s['edges_by_from_kind'])} · 고지 유래 {s['edges_disclosure']} · 경과가 문구/이름 밖에서 온 엣지 {s['edges_course_not_from_phrase']}"),
    ]))
    A("")
    A("#### 9.6.5 미등록 조각 전부 (출처별 · 횟수 · 수식어 목록 적용 후)")
    A("")
    for k, v in s["unregistered_by_origin"].items():
        A(f"- **{k}** ({len(v)}): " + " · ".join(f"`{f}`×{n}" for f, n in v[:80]) + (" …" if len(v) > 80 else ""))
    A("")
    A("#### 9.6.6 미등록 조각 있는 이름이 접혔는가")
    A("")
    A(f"- 둘 이상 이름이 접힌 단위 {s['folded_with_2plus_names']} 중 미등록 조각 있는 이름이 섞인 단위 **{s['folded_with_partial_name']}**. raw_name 단위 {s['complications_distinct_tuples_raw']} 은 전부 이름 하나씩 · 칸은 none/none.")
    A("")
    A("#### 9.6.7 수식 칸(qualifier) 실측 (V3-1 유지)")
    A("")
    A(f"- 수식 사전 값 {s['qualifier_dictionary_values']} · 수식 칸이 none 이 아닌 단위 **{s['qualifier_tuples']}** · 접두 가름 {len(s['prefix_splits'])}: " + " · ".join(f"「{a}」→ {b} + {c}" for a, b, c in s["prefix_splits"]))
    if s["qualifier_tuples_all"]:
        A(md_table(["#", "id", "event", "site", "qualifier", "event_kind", "basis", "세운 문구"], [(i + 1, q["id"], q["event"], q["site"] or "none", q["qualifier"], q["event_kind"], q["basis"] or "—", q["created_by_phrase"] or "이름") for i, q in enumerate(s["qualifier_tuples_all"])]))
    A("")
    A("#### 9.6.8 조직층 부위 실측 (V3-5 유지)")
    A("")
    A(f"- 부위 사전 {s['site_dictionary_values']}({_kv(s['site_dictionary_by_kind'])}) · layer site 가 든 단위 **{s['layer_site_tuples']}**" + ((": " + " · ".join(f"({t['event']}, {t['site']})" + (f" ← {t['created_by_phrase']}" if t["created_by_phrase"] else "") for t in s["layer_site_tuples_all"])) if s["layer_site_tuples_all"] else ""))
    A("")
    A("#### 9.6.9 안전 문구 수식어 목록 실측 (V3.1-8) — 단어·패턴마다 class · 적중 · locator")
    A("")
    sw = s["adverse_stopwords"]
    A(f"- 목록: 빈도 ≥{sw['threshold']} 미등록 조각(v3)에서 고른 단어 {sw['words_total']}(class 별 {_kv(sw['by_class'])}) · locator 있는 단어 **{sw['words_with_locator']}** · 없는 단어 {sw['words_without_locator'] or 0} · 패턴 {len(sw['patterns'])}(locator 있음 {sw['patterns_with_locator']}) · 적중 합 {sw['hits_total']}. 조각 분류 전수: 토큰 {s['fragment_classes_total']} · class 별 {_kv(s['fragment_classes_by_class'])} · 분류 밖 토큰 {len(s['fragment_classes_unclassified'])}.")
    A("")
    A(md_table(["단어", "class", "v3 미등록 횟수", "적중", "locator(최대 6)"], [(w["word"], w["class"], w["v3_unregistered"], w["hits"], " · ".join(f"`{x}`" for x in w["locators"][:6]) + (" …" if len(w["locators"]) > 6 else "") or "—") for w in sw["words"]]))
    A("")
    A(md_table(["class", "정규식", "뜻", "적중", "locator(최대 6)"], [(p["class"], f"`{p['regex']}`", p["note"], p["hits"], " · ".join(f"`{x}`" for x in p["locators"][:6]) or "—") for p in sw["patterns"]]))
    A("")
    A("#### 9.6.10 사건별 조합(단위) 전부 (V3.1-9) — 이름 유래 / 문구가 세운 것 · 엣지 경과")
    A("")
    A(f"- 사전 단위 {s['tuples_dict']} · 사건 {len(s['event_combo_table'])} 중 조합이 하나뿐인 사건 **{s['events_with_1_combo']}** · 둘 이상 {s['events_with_2plus_combos']}. 문구가 세운 조합 {s['units_created_by_phrases']}(전부 세 칸 사전 값 {s['units_created_all_dict']} · 미등록 포함 {s['units_created_with_unregistered']} · 위반 {len(s['units_created_bad'])}) · 사건별 {_kv(s['units_created_by_event'])} · 부위 kind {_kv(s['units_created_by_site_kind'])} · 수식 {_kv(s['units_created_by_qualifier'])}.")
    A("")
    A(md_table(["사건", "조합", "이름 유래", "문구 생성", "단위 (부위 · 수식 · 엣지 경과 · 상대 부위 보존 · 세운 문구)"], [(e["event"], e["combos"], e["from_names"], e["created"], " · ".join(f"({u['site'] or 'none'}" + (f":{u['site_dict_kind']}" if u.get("site_dict_kind") else "") + f", {u['qualifier'] or 'none'}" + (f" · 경과 {_kv(u['edge_courses'])}" if u["edge_courses"] else "") + (f" · 상대 {','.join(u['relative_site_text'])}" if u["relative_site_text"] else "") + (f" ← {u['created_by_phrase']}" if u["created_by_phrase"] else "") + ")" for u in e["units"])) for e in s["event_combo_table"]]))
    A("")
    A("#### 9.6.11 phrase_shape · 발생률/조건 조각 (V3.1-8 보강)")
    A("")
    A(f"- 자리 기준 shape {_kv(s['phrase_shape'])} · 항목 기준 {_kv(s['phrase_shape_entries'])} · auto 의 shape {_kv(s['phrase_shape_by_status'].get('auto'))} · unlinked 의 shape {_kv(s['phrase_shape_by_status'].get('unlinked'))} · 발생률·조건 조각을 R15 로 올리는 항목 {s['incidence_condition_entries']}.")
    A("")
    A(md_table(["kind"] + SHAPES, [(k, *[v.get(sh, 0) for sh in SHAPES]) for k, v in s["phrase_shape_by_kind"].items()]))
    A("")
    A(md_table(["#", "정규화형", "표면형(최대 3)", "kind", "자리", "incidence", "condition", "status"], [(i + 1, x["normalized"][:50], " / ".join(v[:50] for v in x["variants"]), ",".join(x["kinds"]), x["locators"], ", ".join(x["incidence"]) or "—", ", ".join(x["condition"]) or "—", x["status"]) for i, x in enumerate(s["incidence_condition_all"])]))
    A("")
    A("#### 9.6.12 문구 사전 항목 전부 (V3.1-10) — 정규화형 · 표면형 수 · 자리 수 · kind · status · 단위 · parsed")
    A("")
    A(md_table(["#", "PHR-", "정규화형", "표면형", "자리", "kind", "status", "shape", "단위(사건·부위·수식)", "경과", "parsed(정도/시간/발생률/조건)", "미등록"], [(i + 1, e["id"], e["normalized"][:40], len(e["raw_variants"]), len(e["locators"]), ",".join(e["kinds"]), e["status"], e["parsed"]["phrase_shape"], " + ".join(f"({c['event']}, {c['site'] or 'none'}, {c['qualifier'] or 'none'})" for c in e["candidates"]) or "—", ",".join(e["parsed"]["courses"]) or "—", "/".join(",".join(e["parsed"][k]) for k in ("degree", "timing", "incidence", "condition")), ",".join(e["unregistered"][:6]) or "—") for i, e in enumerate(R["adverse"]["phrase_dictionary"])]))
    return "\n".join(o)


def condition_md(R):
    c = R["condition"]
    s = c["summary"]
    o = []
    A = o.append
    A("### 9.7 조건 축 · 결정 kind 실측 (v3.1 신설)")
    A("")
    A("#### 9.7.0 조건 사전 접힘 실측 (V3.1-4) — 이름 298 → 단위 N · 접힌 표 전부 · raw_name")
    A("")
    A(f"- 원장 문장 자리 {s['occurrences']}(9 키) · 정규화 distinct 이름 **{s['names_distinct']}**(kind 포함 {s['names_distinct_with_kind']}) → 단위 **{s['units_total']}**(사전 단위 {s['units_dict']} + raw_name {s['units_raw']}) — {s['names_to_units']}. 사전 값으로 완전히 분해된 이름 {s['names_dict']} · raw_name 이름 {s['names_raw']} · 조건 조각 둘 이상인 이름 {s['names_with_2plus_units']}(원칙 B). kind 별 단위 {_kv(s['units_by_kind'])}(사전 {_kv(s['units_dict_by_kind'])} · raw {_kv(s['units_raw_by_kind'])}).")
    A(f"- 사전 person_condition: 정준값 {s['dictionary_values']} · 동의어 {s['dictionary_synonyms']} · 쓰인 값 {s['dictionary_values_used']} · 안 쓰인 값 {len(s['dictionary_values_unused'])}{(': ' + ', '.join(s['dictionary_values_unused'])) if s['dictionary_values_unused'] else ''} · kind 분포 {_kv(s['dictionary_by_kind'])}. 표지어 {len(s['markers'])}(locator 없는 것 {s['markers_without_locator'] or 0}). 문장 부록 {s['phrases']}(exact {s['phrases_by_match'].get('exact', 0)} · raw {s['phrases_by_match'].get('raw', 0)} · 단위에 붙은 부록 {s['phrases_attached']} · distinct locator {s['phrases_attached_distinct']}) · 문장이 세운 단위 0(단위는 이름이 만든다).")
    A(f"- raw_name 의 미등록 조각 distinct {s['unregistered_distinct']} · 총 {s['unregistered_total']} · 상위: " + " · ".join(f"`{f}`×{n}" for f, n in s["unregistered_top"][:30]))
    A("")
    A("이소트레티노인·레티노이드 문장 전부(어디로 갔나):")
    A("")
    A(md_table(["#", "kind", "원문", "status", "단위"], [(i + 1, x["kind"], x["text"][:90], x["status"], ", ".join(x["units"])) for i, x in enumerate(s["isotretinoin"])]))
    A("")
    A("표지어 실측:")
    A("")
    A(md_table(["표지어", "적중", "locator(최대 6)"], [(m["word"], m["hits"], " · ".join(f"`{x}`" for x in m["locators"][:6]) or "—") for m in s["markers"]]))
    A("")
    A("접힌 표 전부 — 단위마다 어떤 이름이 갔는지(사전 단위 먼저 · 이름 수 순 · raw_name 은 이름 하나씩):")
    A("")
    A(md_table(["#", "name_kind", "kind", "단위(정준값 / raw 원문)", "이름 수", "자리 수", "이름 전부", "미등록 조각", "표지어"], [(i + 1, f["name_kind"], f["kind"], f["name"][:80], f["n_names"], f["n_sources"], " · ".join(x[:60] for x in f["names"]), ", ".join(f["candidate_name"]) or "—", ", ".join(f["qualifier_text"]) or "—") for i, f in enumerate(c["folded"])]))
    A("")
    A("#### 9.7.1 product_reclassify 대상 예 (V3.1-1) — id 재계산(값은 결정 · EXO-02)")
    A("")
    pr = R["product_reclassify"]
    A(f"- 제품 {pr['products_total']} · 계열별 {_kv(pr['products_by_family'])}.")
    A(md_table(["제품", "지금 계열", "지금 PRD-", "→ 계열", "새 PRD-", "alias(reclassified_from)", "새 자리에 같은 이름 있음"], [(x["product"], x["family"], x["current_id"], x["to_modality_code"], x["new_id"], x["alias_reclassified_from"], "○" if x["collision"] else "") for x in pr["examples"]]))
    A("")
    A("#### 9.7.2 R32 출처 후보 열거 (V3.1-2) — 제품 note·legal_warning·regulatory_status 문장 전수 (레코드·엣지는 edge_create 로만)")
    A("")
    rc = R["r32_candidates"]
    A(f"- 후보 {len(rc)}(제품 {len({x['product'] for x in rc})} · 키별 {_kv(Counter(x['key'] for x in rc))}). 어느 문장이 규칙인지는 사람 판정(「주사 사용 금지」류는 severity=prohibited 후보).")
    A("")
    A(md_table(["#", "locator", "제품", "계열", "PRD-", "키", "문장"], [(i + 1, f"`{x['locator']}`", x["product"], x["family"], x["product_id"] or "—", x["key"], x["text"][:120]) for i, x in enumerate(rc)]))
    return "\n".join(o)


def disclosure_md(R):
    s = R["adverse"]["summary"]["disclosures"]
    o = []
    A = o.append
    A("### 9.8 필수 고지 실측 (V3.1-7) — 계열 17 × 고지 109 · clinical_rule(disclosure) · R32 · 문구 사전 · 부작용 조각 연결")
    A("")
    A(f"- 고지 문장 {s['n']}(계열 {s['modalities']}) → clinical_rule(kind=disclosure) 레코드 **{s['distinct_sentences']}**(같은 문장이 여러 계열: {len(s['shared_sentences'])}) · R32(basis=ledger) {s['n']} · 문구 사전 항목 {s['phrase_entries']}. 단위 연결(자리): auto **{s['auto']}** · unlinked {s['unlinked']} · 세운 단위 {s['created_units']} · 언급된 사건 {len(s['events_mentioned'])}: {', '.join(s['events_mentioned'])}.")
    if s["shared_sentences"]:
        A("- 여러 계열이 공유하는 고지: " + " · ".join(f"「{x['text'][:50]}」({', '.join(x['modalities'])})" for x in s["shared_sentences"]))
    A("")
    A(md_table(["계열", "고지", "auto", "unlinked"], [(m, v["n"], v["auto"], v["unlinked"]) for m, v in s["by_modality"].items()]))
    A("")
    A(md_table(["#", "계열", "locator", "문장", "status", "shape", "후보(사건 · 부위 · 수식 · 있음)", "경과", "미등록"], [(i + 1, r["modality"], f"`{r['locator']}`", r["text"][:100], r["status"], r["phrase_shape"], " + ".join(f"({a}, {b or 'none'}, {c or 'none'}{'·있음' if d else '·없음'})" for a, b, c, d in r["candidates"]) or "—", ",".join(r["courses"]) or "—", ", ".join(r["unregistered"][:8]) or "—") for i, r in enumerate(s["rows"])]))
    return "\n".join(o)


def main():
    dic, rules, rrules, L, v3 = load_all()
    bc = bronze_check(LEDGER)
    assert bc["hashes_file"] and not bc["mismatch"], f"브론즈 2판 해시 불일치 {bc}"
    R = run_all(dic, rules, L, rrules, v3)
    R["procedure"]["v21_none_fold_split"] = V3.v21_split(R)
    print(procedure_md(R, (v3 or {}).get("procedure", {}).get("summary")))
    print()
    print(adverse_md(R, (v3 or {}).get("adverse", {}).get("summary")))
    print()
    print(condition_md(R))
    print()
    print(disclosure_md(R))
    json.dump(R, open(os.path.join(HERE, "erd-v3.1-tuples.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    print("\n→ erd-v3.1-tuples.json")


if __name__ == "__main__":
    main()
