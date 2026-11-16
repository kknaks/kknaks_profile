# -*- coding: utf-8 -*-
"""ERD v3.1 §1.5 부작용 단위·문구 사전 · §1.6 조건 단위 — 참조 구현 `erd-v3.1-tuples.py` 의 v3.1 부분(AdverseUnits31 · run_adverse31 ·
ConditionTuples · run_condition · R32 후보 · product_reclassify 예)을 한 모듈로 옮겼다. v3 분해(멤버 · 원칙 B·C · 접두 가름 · 조립)는
lib/decompose.AdverseTuples 를 그대로 쓴다. 같은 입력(사전 · tuple_rules · 원장)에 같은 단위 · 같은 id · 같은 등록 순서 · 같은 문구 사전 항목이
나와야 한다(check.py ③ 이 erd-v3.1-tuples.json 요약 adverse · condition 과 키 단위로 대조한다).

V3.1-9 단위 (사건, 부위, 물질) — 상대 부위는 none(relative_site_text 보존) · 경과는 R15 엣지 속성(원칙 C: 사건 멤버에 붙은 경과만)
V3.1-8 안전 문구 수식어 목록·패턴(tuple_rules.adverse.adverse_stopwords) — 미등록 조각이 아니라 parsed
V3.1-10 문구 사전(정규화형 1줄 · raw_variants · units · parsed · status auto/unlinked) · 부록(R15 source_phrases · 단위 explanations · 게이트)
V3.1-7 필수 고지(kind=disclosure) 문구 · V3.1-4 조건 사전 단위(사전 · raw_name) + phrases 부록
"""
import re
import unicodedata
from collections import Counter, OrderedDict, defaultdict

from .decompose import ADV_MEMBER_SPLIT, ADV_PAREN, ADV_STRIP, CODE_KEY_RE, AdverseTuples, adverse_phrases, locator
from .util import dedupe as _dedupe, mkid, norm

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




SHAPES = ["event_only", "event_site", "event_degree_course", "event_incidence_condition", "explanatory", "unresolved"]
MOD_CLASSES = ("degree", "timing", "incidence", "condition", "connector", "misc")


class AdverseUnits31(AdverseTuples):
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
            rec = {"id": tid, "event_kind": "dict", "event": ev["label"], "event_id": key[0], **({"event_category": ev["category"]} if "category" in ev else {}), "site_kind": "site" if c["site"] else "none", "site": c["site"][1] if c["site"] else None, "site_id": key[1],
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
            cat = self.ids.event[norm(all_events[0])].get("category") if all_events else None
            rec = {"id": tid, "event_kind": "raw_name", "event": text, "event_id": event_id, **({} if getattr(self.ids, "v33", False) else {"event_category": cat}), "site_kind": "none", "site": None, "site_id": "none", "site_dict_kind": None,
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
    for kind, text, src in adverse_phrases(L):
        out.append((kind, text, src))
        if kind == "evidence_statement":
            rec = src["locator"].split("@", 1)[1]
            ae = next(a for code_, cat_ in L["literature-evidence.json"]["categories"].items() if code_ == src["modality"] for i_, a in enumerate(cat_.get("adverse_effects") or []) if f"{code_}/{i_}" == rec)
            for lang in ("ko", "en", "zh", "ja"):
                if ae.get(f"patient_{lang}"):
                    out.append(("patient_text", ae[f"patient_{lang}"], dict(src, kind="patient_text", lang=lang, path=f"categories.{{code}}.adverse_effects[].patient_{lang}", origin=f"literature.patient_{lang}", locator=src["locator"].replace(".statement@", f".patient_{lang}@"), statement_locator=src["locator"], patient_ko=None)))
    for ci, cat in enumerate(L["consent-checklist.json"]["categories"]):
        for i, x in enumerate(cat.get("mandatory_disclosures") or []):
            out.append(("disclosure", x, {"origin": "consent.disclosure", "file": "consent-checklist.json", "path": "categories[].mandatory_disclosures[]", "modality": cat["id"], "record": i, "context": {"disclosure": True}, "rec": (ci, i),
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
    for ci, cat in enumerate(L["complications.json"]["categories"]):
        for i, c in enumerate(cat["complications"]):
            loc = locator("complications.json", "categories[].complications[].name", f"{cat['id']}/{i}")
            r = AT.run_name(c["name"], {"origin": "complications", "file": "complications.json", "path": "categories[].complications[].name", "modality": cat["id"], "record": i, "locator": loc, "rec": (ci, i)})
            r["rec"] = (ci, i)
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
            occ_rows.append({"kind": kind, "lang": src["lang"], "text": text, "locator": src["locator"], "statement_locator": src["statement_locator"], "translation": True, "modality": src.get("modality"), "origin": src["origin"],
                             "file": src["file"], "path": src["path"], "rec": src.get("rec")})
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
        e["contexts"].append({"locator": src["locator"], "kind": kind, "origin": src["origin"], "from": _from_end(src), "modality": src.get("modality"), "context": src.get("context") or {},
                              "file": src["file"], "path": src["path"], "rec": src.get("rec"), "item": src.get("item"), "product": src.get("product"), "text": text})
        occ_rows.append({"kind": kind, "lang": lang, "text": text, "locator": src["locator"], "phrase_id": e["id"], "status": e["status"], "phrase_shape": e["parsed"]["phrase_shape"], "modality": src.get("modality"), "origin": src["origin"], "from": _from_end(src), "translation": False,
                         "file": src["file"], "path": src["path"], "rec": src.get("rec")})
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
    return OrderedDict([("summary", summary), ("tuples", list(A.values())), ("complications", comp_rows), ("folded", adv_folded), ("phrase_dictionary", E), ("phrase_occurrences", occ_rows), ("edges", [dict(e, from_=list(e["from"])) for e in all_edges.values()]), ("created_units", created_units),
                        ("AT", AT)])


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


def condition_ledger_recs(L):
    """condition_occurrences 와 같은 순서 — 원장 위치(file, path, rec 튜플 · provenance 용)."""
    out = []
    for ci, c in enumerate(L["consent-checklist.json"]["categories"]):
        for i, x in enumerate(c.get("contraindications") or []):
            out.append(("consent-checklist.json", "categories[].contraindications[]", (ci, i)))
    for code, v in L["extracted.json"].items():
        if not CODE_KEY_RE.match(code):
            continue
        for k in ("absolute", "relative"):
            for i, x in enumerate((v.get("contraindications") or {}).get(k) or []):
                out.append(("extracted.json", f"{{code}}.contraindications.{k}[]", (code, i)))
    for mi, m in enumerate(L["taxonomy.json"]["modality"]):
        for k in ("absolute", "relative"):
            for i, x in enumerate(((m.get("extracted") or {}).get("contraindications") or {}).get(k) or []):
                out.append(("taxonomy.json", f"modality[].extracted.contraindications.{k}[]", (mi, i)))
        for si, sc in enumerate(m["subcategories"]):
            for ii, it in enumerate(sc["items"]):
                for i, x in enumerate(((it.get("extracted") or {}).get("safety") or {}).get("contraindications") or []):
                    out.append(("taxonomy.json", "modality[].subcategories[].items[].extracted.safety.contraindications[]", (mi, si, ii, i)))
    for i, u in enumerate(L["pre-procedure-checklist.json"]["universal_checks"]):
        out.append(("pre-procedure-checklist.json", "universal_checks[].label", (i,)))
    for ci, c in enumerate(L["pre-procedure-checklist.json"]["category_specific"]):
        for i, ch in enumerate(c["checks"]):
            out.append(("pre-procedure-checklist.json", "category_specific[].checks[].label", (ci, i)))
    for i, a in enumerate(L["treatment-optimization.json"]["by_age_group"]):
        out.append(("treatment-optimization.json", "by_age_group[].age", (i,)))
    return out


def run_condition(dic_json, rules, L, ct_cls=None):
    CT = (ct_cls or ConditionTuples)(dic_json, rules)   # v3.2: lib.v32.ConditionTuples32(토큰화 · 병기)
    occ = condition_occurrences(L)
    recs = condition_ledger_recs(L)
    assert len(recs) == len(occ)
    rows = []
    for o, lr in zip(occ, recs):
        ph = CT.run(*o)
        ph["ledger"] = lr
        for uid in ph["unit_ids"]:
            CT.units[uid]["phrases"][-1]["ledger"] = lr
        rows.append(ph)
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


