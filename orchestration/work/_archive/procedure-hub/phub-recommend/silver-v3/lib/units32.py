# -*- coding: utf-8 -*-
"""ERD v3.2 실버 단위 — units31.AdverseUnits(이름 → 단위 · 문구 사전 지도 · 결정이 바꾸는 자리) 위에 v3.2 자리를 더한다.

- 문구 사전: 부작용 문구 종류만(status exact · new · approved) + 메모·설명문 항목(status note · sentence · 단위 없음 · phrase_map 대상)
- 원장 사건 노드(event_kind=ledger · adverse_event_type origin=ledger · unreviewed) — 단위의 event_kind 를 dict|ledger 로
- 자기 테이블(참조만 · 단위를 세우지 않는다): 타임라인 줄(R34) · 응급 징후(R35) · 필수 고지(clinical_rule.adverse_ref) · 문헌 adverse_effects(evidence_statement.adverse_ref)
- 옛 판 결정의 새 구조: 타임라인 줄 locator(v3·v3.1 ERD 꼴 `…@M16/6`)를 가리킨 adverse_tuple_assign(kind=expression) → 그 줄의 참조(adverse_ref)를 지정 단위로 · 경과는 계열 R15 엣지 경과
- V3.2-8 단위 일반값(참조): general_description(이 단위를 참조하는 문헌 adverse_effects EVS-) · general_management(이 단위로 접힌 complications 이름의 management locator)
"""
from collections import OrderedDict

from .provenance import P, loc
from .units31 import AdverseUnits
from .util import dedupe, norm


class AdverseUnits32(AdverseUnits):
    def __init__(self, ctx):
        super().__init__(ctx)
        A = self.A
        self.ledger = OrderedDict((norm(n["canonical"]), n) for n in A["ledger_events"])
        for u in self.units.values():
            u["event_kind"] = "ledger" if norm(u.get("event") or "") in self.ledger else "dict"
        # 메모·설명문(V3.2-7) — 단위 없음 · phrase_map 대상(설명문은 사람 지정)
        for e in A["memo_phrases"]:
            x = dict(e)
            for k, v in (("kinds", ["safety_phrase"]), ("langs", ["ko"]), ("modality_codes", []), ("units", []), ("created_units", []), ("candidates", []), ("reasons", []),
                         ("translations", []), ("citations", []), ("accuracy", []), ("extra_sites", []), ("extra_courses", []), ("extra_qualifiers", [])):
                x.setdefault(k, list(v))
            x["parsed"] = dict(x.get("parsed") or {}, phrase_shape="not_adverse_note" if e["status"] == "note" else "explanatory_sentence")
            x["decision_ids"], x["mapped_courses"], x["mapped_by"] = [], None, None
            self.phrases[e["id"]] = x
            for c in x["contexts"]:
                self.loc_phrase.setdefault(c["locator"], e["id"])
            self.norm_phrase.setdefault(e["normalized"], e["id"])
        for r in A["phrase_occurrences"]:
            if r.get("rec") is not None:
                self.erd2p.setdefault(r["locator"], P(r["file"], r["path"], r["rec"]))
        # 자기 테이블 — 참조만
        self.timelines = A["timelines"]
        self.lines = OrderedDict()
        self.line_by_erd = {}
        for T in self.timelines:
            for ph in T["phases"]:
                for ln in ph["lines"]:
                    ln.setdefault("decision_ids", [])
                    ln.setdefault("mapped_courses", None)
                    self.lines[ln["locator"]] = (T, ph, ln)
                    if ln.get("erd_locator"):
                        self.line_by_erd[ln["erd_locator"]] = ln["locator"]
                        self.erd2p.setdefault(ln["erd_locator"], P("post-procedure-timeline.json", ln["path"], ln["rec"]))
        self.signs = A["emergency_signs"]
        self.disclosures = A["disclosures"]
        self.literature = A["literature"]
        # ERD 꼴 locator(응급 징후 · 고지 `@<계열>/<순번>`) → 원장 위치(결정 source_refs · 게이트 원문)
        for sg in self.signs:
            for lc, r in zip(sg["locators"], sg["recs"]):
                self.erd2p.setdefault(lc, P("consent-checklist.json", "categories[].emergency_signs[]", r))
        for d in self.disclosures:
            self.erd2p.setdefault(d["locator"], P("consent-checklist.json", "categories[].mandatory_disclosures[]", d["rec"]))

    # ------------------------------------------------------------------ 결정 — 타임라인 줄(옛 판 표현 지정의 새 구조)
    def line_of(self, lc):
        if lc in self.lines:
            return lc
        return self.line_by_erd.get(lc)

    def assign_line(self, line_loc, uids, courses, decision_id):
        """타임라인 줄의 참조를 지정 단위로 — 줄은 단위를 세우지 않는 자기 테이블이라 결정이 세운 단위를 가리키기만 한다(R34 · 계열 R15 경과)."""
        T, ph, ln = self.lines[line_loc]
        ln["adverse_ref_before"] = list(ln["adverse_ref"])
        ln["adverse_ref"] = list(uids)
        ln["ref_status"] = "ref"
        ln["mapped_courses"] = list(courses or [])
        ln["decision_ids"].append(decision_id)
        for u in uids:
            uu = self.units[u]
            if decision_id not in uu["decision_ids"]:
                uu["decision_ids"].append(decision_id)

    # ------------------------------------------------------------------ 마감
    def referenced(self):
        ref = set(u for v in self.name_units.values() for u in v)
        ref |= set(u for e in self.phrases.values() if e["status"] in ACTIVE for u in e["units"])
        ref |= set(self.edge_units)
        ref |= set(u for _, _, ln in self.lines.values() if ln.get("decision_ids") for u in ln["adverse_ref"])
        return ref

    def finish(self):
        super().finish()
        live = set(self.units)
        dropped = []
        for _, _, ln in self.lines.values():
            gone = [u for u in ln["adverse_ref"] if u not in live]
            if gone:
                dropped.append((ln["locator"], gone))
                ln["adverse_ref"] = [u for u in ln["adverse_ref"] if u in live]
                if not ln["adverse_ref"]:
                    ln["ref_status"] = "normal_memo" if ln["reaction_level"] == "normal" else "none"
        for coll in (self.signs, self.disclosures, self.literature):
            for x in coll:
                gone = [u for u in x["adverse_ref"] if u not in live]
                if gone:
                    dropped.append((x.get("locator") or (x.get("locators") or [None])[0], gone))
                    x["adverse_ref"] = [u for u in x["adverse_ref"] if u in live]
                    if not x["adverse_ref"]:
                        x["ref_status"] = "none"
        self.dropped_refs = dropped
        # V3.2-8 ① 단위 일반값(참조) — 결정 뒤 단위 기준으로 다시
        for u in self.units.values():
            u["general_description"], u["general_management"] = [], []
            u["event_kind"] = "ledger" if norm(u.get("event") or "") in self.ledger else "dict"
            u["event_origin_locators"] = list(self.ledger[norm(u["event"])]["locators"]) if u["event_kind"] == "ledger" else []
            u["side_fragments"] = []
        for lit in self.literature:
            for uid in lit["adverse_ref"]:
                self.units[uid]["general_description"].append(OrderedDict([("ref", lit["id"]), ("locator", lit["locator"])]))
        L = self.ctx["L"]
        for lc, uids in self.name_units.items():
            ci, i = self.name_rec[lc]
            cat = L["complications.json"]["categories"][ci]
            if cat["complications"][i].get("management") in (None, "", [], {}):
                continue
            ml = loc(P("complications.json", "categories[].complications[].management", (ci, i)))
            for uid in uids:
                if uid in self.units:
                    self.units[uid]["general_management"].append(OrderedDict([("ref", f"R15:{cat['id']}→{uid}"), ("locator", ml), ("name_locator", lc)]))
        for pid, e in self.phrases.items():
            if e["status"] in ACTIVE:
                for uid in e["units"]:
                    if uid in self.units:
                        self.units[uid]["side_fragments"] = dedupe(self.units[uid]["side_fragments"] + list(e["parsed"].get("side") or []))


ACTIVE = ("auto", "approved", "exact", "new")
