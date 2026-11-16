# -*- coding: utf-8 -*-
"""ERD v3.1 실버 단위 — 부작용 단위(세 칸 · V3.1-9) · 문구 사전(V3.1-10) · 조건 단위(V3.1-4).

부작용: 분해(lib/adverse31.run_adverse31) 결과를 받아 결정이 바꾸는 자리를 둔다.
  - complications 이름 locator(ERD 꼴 `…name@<계열>/<순번>`) → 단위 목록 · (이름, 단위) → R15 경과(원칙 C: 사건 멤버에 붙은 경과만)
  - 문구 사전 항목 PHR- → 단위 목록(status auto · approved) · (항목, 단위) → R15 경과 · 항목의 문구 자리(contexts) = R15 출발 · 부록
  ③ adverse_tuple_assign(raw_name) · ① phrase_map 이 이것을 바꾼다. 단위가 없으면 결정이 세운다(세 칸 전부 사전 값이어야).
조건: 조건 단위(사전 · raw_name)와 문장 자리(원장 위치) → 단위 목록(R16·R17 끝).

ERD 꼴 locator 는 결정 target·안정 키용이고, provenance(derived_from)는 원장 위치 locator(배열 인덱스 · 코드 키)다 — erd2p 가 옮긴다.
"""
from collections import OrderedDict

from .provenance import P, loc
from .util import dedupe, mkid, norm


def unit_id3(event_id, site_id, qualifier_id):
    """v3.1 부작용 단위 식별자 — 세 칸(event · site · qualifier · 없음은 'none' · 경과 없음)."""
    return mkid("ADV", f"{event_id}|{site_id or 'none'}|{qualifier_id or 'none'}")


ACTIVE_PHRASE = ("auto", "approved", "exact", "new")   # 단위에 닿는 문구 사전 status — v3.1 auto · approved / v3.2 exact · new · approved
PARSED_REFS = (("degree", "degree_text"), ("timing", "timing_text"), ("incidence", "incidence_text"), ("condition", "condition_text"))


class AdverseUnits:
    def __init__(self, ctx):
        self.ctx = ctx
        A = ctx["adv"]
        self.A = A
        self.AT = A["AT"]
        self.ids = ctx["ids"]
        self.erd2p = OrderedDict()
        for r in A["complications"]:
            self.erd2p[r["locator"]] = P("complications.json", "categories[].complications[].name", r["rec"])
        for r in A["phrase_occurrences"]:
            if r.get("rec") is not None:
                self.erd2p.setdefault(r["locator"], P(r["file"], r["path"], r["rec"]))
        self.units = OrderedDict()
        for tid, t in self.AT.tuples.items():
            u = OrderedDict((k, v) for k, v in t.items() if k not in ("sources", "explanations"))
            u["occ"] = dedupe(loc(self.erd2p[s_["locator"]]) for s_ in t["sources"] if s_.get("origin") == "complications" and s_.get("locator") in self.erd2p)
            u["origins"] = list(t["origins"])
            u["decision_ids"] = []
            u["relative_site_text"] = list(t.get("relative_site_text") or [])
            self.units[tid] = u
        # complications 이름 → 단위 · 경과
        self.name_units, self.name_rec, self.name_row, self.name_courses = OrderedDict(), {}, {}, {}
        for r in A["complications"]:
            lc = r["locator"]
            self.name_units[lc] = list(r["unit_ids"])
            self.name_rec[lc] = r["rec"]
            self.name_row[lc] = r
            for uid in r["unit_ids"]:
                self.name_courses[(lc, uid)] = dedupe(co for c in r["candidates"] if c.get("unit_id") == uid or (r["event_kind"] == "dict" and self.AT.units.get((c["event_id"], c["site_id"], c["qualifier_id"])) == uid) for co in c["courses"])
        # 문구 사전
        self.phrases = OrderedDict()
        for e in A["phrase_dictionary"]:
            x = dict(e)
            x["units"] = list(e["units"])
            x["decision_ids"] = []
            x["mapped_courses"] = None
            x["mapped_by"] = None
            self.phrases[e["id"]] = x
        self.loc_phrase = {}
        for pid, e in self.phrases.items():
            for c in e["contexts"]:
                self.loc_phrase.setdefault(c["locator"], pid)
        self.norm_phrase = {e["normalized"]: pid for pid, e in self.phrases.items()}
        self.edge_units = []   # ⑤ edge_create 가 세운 단위

    # ------------------------------------------------------------------ 사전 id
    def _by_id(self, table, i):
        return next((e for e in table.values() if e["id"] == i), None)

    def labels_to_ids(self, event, site, qualifier):
        """사전 정준값(·동의어) 세 칸 → (event_id, site_id, qualifier_id, relative_text) · 사전에 없으면 None + 사유."""
        ids = self.ids
        ev = ids.event.get(norm(ids.event_surface.get(norm(event or ""), event or "")))
        st = site or "none"
        if ev is None and norm(event or "") in getattr(ids, "event_decomposed", {}):
            # v3.3(V3.3-C(1)): 옛 사전 값(분해 꼴 「혈관 폐색」)을 가리킨 결정 → (사건 폐색, 부위 혈관) — 부위가 none 이거나 같을 때만
            dcp = ids.event_decomposed[norm(event)]
            if st not in ("none", None) and norm(st) != norm(dcp.get("site") or ""):
                return None, f"사건 「{event}」 은 분해 꼴(→ {dcp['event']} + 부위 {dcp.get('site')})인데 부위 「{site}」 가 다르다"
            ev = ids.event.get(norm(ids.event_surface.get(norm(dcp["event"]), dcp["event"])))
            st = dcp.get("site") or "none"
            self.ctx.setdefault("decomposed_refs", []).append({"event": event, "to_event": dcp["event"], "to_site": st, "rule": dcp.get("rule")})
        if ev is None:
            return None, f"사건 「{event}」 이 사건 사전에 없다"
        rel = None
        if st in ("none", None):
            sid = "none"
        elif norm(st) in ids.rsite_surface:
            sid, rel = "none", ids.rsite_surface[norm(st)]
        elif norm(st) in ids.site_surface:
            sid = ids.site[norm(ids.site_surface[norm(st)])]["id"]
        else:
            return None, f"부위 「{site}」 가 부위 사전에 없다"
        q = qualifier or "none"
        if q == "none":
            qid = "none"
        else:
            qe = ids.qualifier.get(norm(ids.qualifier_surface.get(norm(q), q)))
            if qe is None:
                return None, f"수식 「{qualifier}」 이 수식 사전에 없다"
            qid = qe["id"]
        return (ev["id"], sid, qid, rel), None

    def unit_for(self, event_id, site_id, qualifier_id, decision_id, relative_text=None):
        """지정 단위(세 칸 사전 id) — 있으면 그 단위, 없으면 결정이 세운다. site_id 가 상대 부위 사전 id 면 none(조각은 relative_site_text · V3.1-9)."""
        ids = self.ids
        ev = self._by_id(ids.event, event_id)
        if ev is None:
            return None
        rel = relative_text
        site_id = site_id or "none"
        site_label, site_dict_kind = None, None
        if site_id != "none":
            rs = self._by_id(ids.rsite, site_id)
            if rs is not None:
                rel, site_id = rs["label"], "none"
            else:
                ss = next((e for e in ids.site.values() if e["id"] == site_id), None)
                if ss is None:
                    return None
                site_label, site_dict_kind = ss["label"], ids.site_kind.get(norm(ss["label"]))
        qualifier_id = qualifier_id or "none"
        qu = None
        if qualifier_id != "none":
            qu = self._by_id(ids.qualifier, qualifier_id)
            if qu is None:
                return None
        uid = unit_id3(event_id, site_id, qualifier_id)
        u = self.units.get(uid)
        if u is None:
            u = OrderedDict([("id", uid), ("event_kind", "dict"), ("event", ev["label"]), ("event_id", event_id), *([("event_category", ev["category"])] if "category" in ev else []), ("site_kind", "site" if site_id != "none" else "none"),
                             ("site", site_label), ("site_id", site_id), ("site_dict_kind", site_dict_kind), ("qualifier", qu["label"] if qu else None), ("qualifier_id", qualifier_id),
                             ("qualifier_basis", "decision" if qu else None), ("status", "complete"), ("unregistered_fragments", []), ("origins", ["decision"]), ("anchor", None), ("all_dict_values", True),
                             ("candidate_name", []), ("event_fragments", [ev["label"]]), ("extra_sites", []), ("extra_qualifiers", []), ("relative_site_text", []), ("site_basis", None),
                             ("created_by_phrase", None), ("occ", [decision_id]), ("decision_ids", [decision_id])])
            self.units[uid] = u
        elif decision_id not in u["decision_ids"]:
            u["decision_ids"].append(decision_id)
        if rel and rel not in u["relative_site_text"]:
            u["relative_site_text"].append(rel)
        return uid

    def course_labels(self, values):
        """경과 값(정준값·동의어 · 「미상」은 엣지 null) → 경과 사전 정준값 목록 · 사전 밖이면 None."""
        out = []
        for v in values or []:
            c = self.ids.course_surface.get(norm(v))
            if c is None:
                return None
            if c != "미상" and c not in out:
                out.append(c)
        return out

    # ------------------------------------------------------------------ 결정
    def assign_name(self, lc, uids, courses_by_uid, decision_id):
        """③ adverse_tuple_assign(raw_name) — 이름의 단위를 지정 단위로 · 경과는 (이름, 단위) R15 엣지 속성."""
        old = self.name_units[lc]
        self.name_units[lc] = list(uids)
        for u in uids:
            uu = self.units[u]
            if decision_id not in uu["decision_ids"]:
                uu["decision_ids"].append(decision_id)
            p = loc(P("complications.json", "categories[].complications[].name", self.name_rec[lc]))
            if p not in uu["occ"]:
                uu["occ"].append(p)
            if "complications" not in uu["origins"]:
                uu["origins"].append("complications")
            self.name_courses[(lc, u)] = list(courses_by_uid.get(u) or [])
        for o in old:
            if o not in uids:
                self.name_courses.pop((lc, o), None)
                self.units[o].setdefault("replaced_by", [])
                self.units[o]["replaced_by"] = dedupe(self.units[o]["replaced_by"] + list(uids))

    def map_phrase(self, pid, uids, courses, decision_id, how):
        """① phrase_map(·옛 표현 지정) — 항목 지도 확정(status=approved) · 단위 · 경과(courses 가 None 이면 후보의 경과)."""
        e = self.phrases[pid]
        e["status"] = "approved"
        e["units"] = list(uids)
        e["mapped_courses"] = courses
        e["mapped_by"] = how
        e["decision_ids"].append(decision_id)
        for u in uids:
            uu = self.units[u]
            if decision_id not in uu["decision_ids"]:
                uu["decision_ids"].append(decision_id)

    def phrase_of(self, target):
        pid = target.get("phrase_id")
        if pid:
            return pid if pid in self.phrases else None
        nrm = target.get("normalized")
        if nrm is not None:
            return self.norm_phrase.get(norm(nrm)) or self.norm_phrase.get(nrm)
        return None

    def phrase_courses(self, pid, uid):
        e = self.phrases[pid]
        if e.get("mapped_courses") is not None:
            return list(e["mapped_courses"])
        return dedupe(co for c in e["candidates"] if c.get("unit_id") == uid or (c.get("event_id") and unit_id3(c["event_id"], c["site_id"], c["qualifier_id"]) == uid) for co in c.get("courses") or [])

    def ctx_loc(self, c):
        return loc(P(c["file"], c["path"], c["rec"])) if c.get("rec") is not None else None

    def find_units(self, text):
        """문구 하나를 §1.5 로 분해해 세 칸 전부 사전 값이면 지금 있는 단위 id(pih-risk 「PIH」 같은 고정 문구용)."""
        AT = self.AT
        tuples, untouched, extras = AT.assemble(AT.split(text))
        if untouched or extras["extra_sites"] or extras["extra_courses"] or extras["extra_qualifiers"]:
            return []
        out = []
        for c in AT.unit_candidates(tuples):
            k = AT.unit_key(c)
            uid = unit_id3(*k)
            if uid in self.units:
                out.append(uid)
        return out

    # ------------------------------------------------------------------ 마감
    def referenced(self):
        ref = set(u for v in self.name_units.values() for u in v)
        ref |= set(u for e in self.phrases.values() if e["status"] in ACTIVE_PHRASE for u in e["units"])
        ref |= set(self.edge_units)
        return ref

    def finish(self):
        """결정 뒤 — 안 쓰이게 된 단위(이름·문구·결정 어디에도 없음)를 빼고, 문구 자리 occ · 원천 · created_by_phrase · explanations 부록을 다시 단다."""
        ref = self.referenced()
        for uid in list(self.units):
            if uid not in ref:
                del self.units[uid]
        for u in self.units.values():
            u["explanations"] = []
        for pid, e in self.phrases.items():
            if e["status"] not in ACTIVE_PHRASE:
                continue
            for uid in e["units"]:
                u = self.units.get(uid)
                if u is None:
                    continue
                for c in e["contexts"]:
                    lc = self.ctx_loc(c)
                    if lc and lc not in u["occ"]:
                        u["occ"].append(lc)
                    if c["kind"] not in u["origins"]:
                        u["origins"].append(c["kind"])
                    u["explanations"].append(OrderedDict([("phrase_id", pid), ("kind", c["kind"]), ("lang", e["langs"][0] if e["langs"] else None), ("locator", c["locator"]), ("ledger_locator", lc)]))
                for tr in e.get("translations", []):
                    p = self.erd2p.get(tr["record"])
                    u["explanations"].append(OrderedDict([("phrase_id", pid), ("kind", "patient_text"), ("lang", tr["lang"]), ("locator", tr["locator"]),
                                                          ("ledger_locator", loc(P(p["file"], p["path"].replace(".statement", f".patient_{tr['lang']}"), p["rec"])) if p else None)]))
        for u in self.units.values():
            if not u["occ"]:
                u["occ"] = list(u.get("decision_ids") or [])


class CondUnits:
    """v3.1(V3.1-4) 조건 단위 — 문장 자리(원장 위치 locator) → 단위 목록."""

    def __init__(self, ctx):
        C = ctx["cond"]
        self.C = C
        self.units = OrderedDict((u["id"], u) for u in C["units"])
        self.by_loc = OrderedDict()
        for r in C["phrases"]:
            self.by_loc[loc(P(*r["ledger"]))] = list(r["unit_ids"])

    def of(self, pv):
        return self.by_loc.get(loc(pv), [])
