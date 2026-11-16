#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ERD v2.4 — 튜플 분해 실측기. v2.3(erd-v2.3-tuples.py) 위에 3차 독립 검토(erd-v2.3-review.md ⑥) 반영 수정 1·2·3 만 바꾼다(발주서 erd-v2.4-brief.md). 독립 실행.
시술 축(①②③ · 코드 참조 · 엣지 끝 분포)은 v2.3 그대로(코드 재사용) — 바뀐 것은 부작용 축 §1.5 뿐이다.

원칙(발주서 · 시술 축 v2.1~v2.3 과 동일하게 부작용 축에 적용):
  A. 미상 칸이 하나라도 있으면 다른 이름과 접지 않는다.
  B. 조각을 버리지 않는다. 한 칸에 후보가 둘이면 단위를 둘로 나누거나(부위 「이마/눈가」→ 둘) 미해결로 둔다.
  C. 수식어(경과·부위)는 같은 멤버 안에서 바로 붙은 사건에만 준다. 이름 전체에서 끌어오지 않는다.
  D. 표현(adverse_expression)은 단위를 가리키기만 한다. 표현에서 새 단위를 만들지 않는다.

v2.3 → v2.4:
  1. (2-A′) site 는 C 원칙 — 사건이 놓인 멤버 안의 부위 조각만. 멤버 밖(같은 묶음 · outer · 이름 전체)에서 가져오지 않는다.
     부위 조각만으로 된 멤버(사건·경과·미등록 0)가 같은 묶음에서 사건 멤버 바로 앞에 있으면 그 멤버와 한 멤버로 읽는다(부위 나열 「이마/눈가 당김감」).
     한 멤버에 부위 후보가 둘 이상이면 B 원칙 — 부위마다 튜플(당김감×이마 + 당김감×눈가). 경과 후보가 둘 이상이면 같은 방식(경과마다).
     사건에 붙지 않은 부위·경과 조각은 버리지 않고 extra_sites·extra_courses 에 보존하고 접지 않는다.
  2. (2-B′) raw_name 튜플에는 course·site 를 주지 않는다 — 둘 다 none/미상(식별자 RAW:anchor 만으로 고유). 사전 분해 결과는 dict_tuples·event_fragments·extra_* 에 보존.
     complications 이름은 미등록 조각 ≥1 **또는** 사건에 붙지 않은 부위·경과 조각 ≥1 이면 raw_name(접지 않음).
  3. (2-C′) 표현은 단위를 만들지 않는다 — 분해 결과(candidates)가 기존 단위(complications 65 이름 유래 사전 튜플)와 세 칸 완전 일치하고 미등록 0 · 남는 조각 0 일 때만 R29(match_status=exact).
     아니면 unlinked + candidates 보존(adverse_tuple_assign 의 재료). 표현만으로 생기는 튜플 0.

입력(같은 폴더): erd-v2.4-dictionaries.json(없으면 v2.3) · erd-v2.4.json(tuple_rules/resolve_rules — 없으면 erd_spec_v24) · erd-v2.3-tuples.py(→ v2.2 → v2.1 → v2) · 원장 21 · erd-v2.3-tuples.json(§9.5·§9.6 나란히 비교용)
출력: 표준 출력에 §9.5/§9.6 표 + erd-v2.4-tuples.json
실행: python3 erd-v2.4-tuples.py
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


V23 = load_module("erd_v23_tuples", os.path.join(HERE, "erd-v2.3-tuples.py"))
V22 = V23.V22
V2 = V23.V2
norm, mkid, md_table, with_alias, LEDGER = V2.norm, V2.mkid, V2.md_table, V2.with_alias, V2.LEDGER
locator = V23.locator
PRINCIPLES = OrderedDict([
    ("A", "미상 칸이 하나라도 있으면 다른 이름과 접지 않는다."),
    ("B", "조각을 버리지 않는다. 한 칸에 후보가 둘이면 단위를 둘로 나누거나(부위 「이마/눈가」→ 둘) 미해결로 둔다."),
    ("C", "수식어(경과·부위)는 **같은 멤버 안에서 바로 붙은 사건**에만 준다. 이름 전체에서 끌어오지 않는다."),
    ("D", "표현(adverse_expression)은 단위를 **가리키기만** 한다. 표현에서 새 단위를 만들지 않는다."),
])


def _dedupe(xs):
    return list(dict.fromkeys(xs))


# ---------------------------------------------------------------------------
# 부작용 — 수정 1(site 멤버만 · 부위 나열 · 후보 둘이면 둘) · 수정 2(raw 칸 none/미상) · 수정 3(표현은 가리키기만)
# ---------------------------------------------------------------------------
class AdverseTuples24(V23.AdverseTuples23):
    def __init__(self, ids):
        super().__init__(ids)
        self.units = {}  # (event_id, site_id, course_id) → tuple id — complications 65 유래 사전 튜플만(기존 단위)

    def site_key(self, site):
        if site is None:
            return "none"
        if site[0] == "relative":
            return self.ids.rsite[norm(site[1])]["id"]
        return self.ids.site[norm(site[1])]["id"]

    def assemble(self, groups):
        """C: 사건이 놓인 멤버 안의 부위·경과만. 부위 나열 멤버(부위만 · 바로 앞)는 뒤 멤버와 한 멤버. B: 한 칸에 후보 둘 이상이면 후보마다 튜플. 붙지 않은 조각은 extra 에 보존."""
        out, merges = [], []
        extra_sites, extra_courses = [], []
        for g in groups:
            ms = g["members"]
            pending = []  # 부위 나열 멤버의 부위 후보(바로 뒤 사건 멤버에 붙는다)
            pending_text = []
            for idx, m in enumerate(ms):
                spans = m["spans"]
                events = _dedupe(s["canonical"] for s in spans if s["kind"] == "event")
                sites = _dedupe((s["kind"], s["canonical"]) for s in spans if s["kind"] in ("relative", "site"))
                courses = _dedupe(s["canonical"] for s in spans if s["kind"] == "course")
                if not events:
                    nxt = ms[idx + 1] if idx + 1 < len(ms) else None
                    if sites and not courses and not m["untouched"] and nxt is not None and any(s["kind"] == "event" for s in nxt["spans"]):
                        pending += sites
                        pending_text.append(m["text"])
                        continue
                    extra_sites += [s[1] for s in sites] + [s[1] for s in pending]
                    extra_courses += courses
                    pending, pending_text = [], []
                    continue
                site_list = bool(pending)
                all_sites = _dedupe(pending + sites)
                if site_list:
                    merges.append({"where": g["where"], "site_members": list(pending_text), "event_member": m["text"], "sites": [s[1] for s in all_sites], "events": events})
                pending, pending_text = [], []
                site_opts = all_sites or [None]
                course_opts = courses or ["미상"]
                for ev in events:
                    for st in site_opts:
                        for co in course_opts:
                            out.append({"event": ev, "site": st, "course": co, "member": (" / ".join(pending_text) + " / " if site_list and pending_text else "") + m["text"],
                                        "site_basis": ("site_list" if site_list and st in pending else "member") if st else None, "course_basis": "member" if courses else None,
                                        "n_site_candidates": len(all_sites), "n_course_candidates": len(courses)})
            extra_sites += [s[1] for s in pending]
        untouched = [u for g in groups for m in g["members"] for u in m["untouched"]]
        seen, uniq = set(), []
        for t in out:
            k = (t["event"], t["site"], t["course"])
            if k not in seen:
                seen.add(k)
                uniq.append(t)
        return uniq, untouched, {"extra_sites": _dedupe(extra_sites), "extra_courses": _dedupe(extra_courses), "site_list_merges": merges}

    def register(self, t, src, untouched, extras=None):
        """complications 65 유래 사전 튜플(event_kind=dict · 세 칸 전부 사전 값 · 미등록 0 · 남는 조각 0)만 여기로 온다. 기존 단위 색인에 등록."""
        assert not untouched
        tid = V2.AdverseTuples.register(self, t, src, untouched)
        rec = self.tuples[tid]
        rec.setdefault("event_kind", "dict")
        rec.setdefault("event_id", self.ids.event[norm(t["event"])]["id"])
        rec.setdefault("anchor", None)
        rec.setdefault("all_dict_values", True)
        rec.setdefault("candidate_name", [])
        rec.setdefault("event_fragments", [rec["event"]])
        rec.setdefault("extra_sites", [])
        rec.setdefault("extra_courses", [])
        rec.setdefault("site_basis", t.get("site_basis"))
        rec.setdefault("course_basis", t.get("course_basis"))
        self.units[(rec["event_id"], rec["site_id"], rec["course_id"])] = tid
        return tid

    def register_raw(self, text, tuples, untouched, extras, src, anchor):
        """수정 2: raw_name 튜플의 site/course 칸은 none/미상 — 이름 전체에서 끌어오지 않음. 사전 분해 결과는 보존만."""
        all_events = _dedupe(t["event"] for t in tuples)
        sites = _dedupe([t["site"][1] for t in tuples if t["site"]] + list(extras["extra_sites"]))
        courses = _dedupe([t["course"] for t in tuples if t["course"] != "미상"] + list(extras["extra_courses"]))
        cid = self.ids.course[norm("미상")]["id"]
        event_id = f"RAW:{anchor}"
        tid = mkid("ADV", f"{event_id}|none|{cid}|{anchor}")
        rec = self.tuples.get(tid)
        if rec is None:
            cat = self.ids.event[norm(all_events[0])]["category"] if all_events else None
            rec = {"id": tid, "event_kind": "raw_name", "event": text, "event_id": event_id, "event_category": cat, "site_kind": "none", "site": None, "site_id": "none", "course": "미상", "course_id": cid,
                   "status": "partial" if untouched else "unresolved", "unregistered_fragments": list(untouched), "origins": [], "sources": [], "anchor": anchor, "all_dict_values": False, "candidate_name": list(untouched),
                   "event_fragments": all_events, "extra_sites": sites, "extra_courses": courses, "site_basis": None, "course_basis": None,
                   "dict_tuples": [(t["event"], t["site"][1] if t["site"] else None, t["course"]) for t in tuples], "raw_reason": ("unregistered" if untouched else "") + ("+" if untouched and (extras["extra_sites"] or extras["extra_courses"]) else "") + ("unattached_fragments" if (extras["extra_sites"] or extras["extra_courses"]) else "")}
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
            key = (ev["id"], sid, cid)
            out.append({"event": t["event"], "event_id": ev["id"], "site": t["site"][1] if t["site"] else None, "site_kind": t["site"][0] if t["site"] else "none", "site_id": sid, "course": t["course"], "course_id": cid,
                        "would_be_id": mkid("ADV", f"{ev['id']}|{sid}|{cid}"), "exists": key in self.units, "unit_id": self.units.get(key), "site_basis": t["site_basis"], "course_basis": t["course_basis"], "member": t["member"]})
        return out

    def run_name(self, text, src):
        """complications 이름(정체성 원천)."""
        groups = self.split(text)
        tuples, untouched, extras = self.assemble(groups)
        spans = [(s["kind"], s["canonical"], s["text"]) for g in groups for m in g["members"] for s in m["spans"]]
        unattached = bool(extras["extra_sites"] or extras["extra_courses"])
        base = {"text": text, "spans": spans, "locator": src["locator"], "unregistered": untouched, "extra_sites": extras["extra_sites"], "extra_courses": extras["extra_courses"], "site_list_merges": extras["site_list_merges"],
                "b_splits": [(t["event"], t["site"][1] if t["site"] else None, t["course"], t["n_site_candidates"], t["n_course_candidates"]) for t in tuples if t["n_site_candidates"] >= 2 or t["n_course_candidates"] >= 2],
                "dict_tuples": [(t["event"], t["site"][1] if t["site"] else None, t["course"]) for t in tuples], "event_fragments": _dedupe(t["event"] for t in tuples)}
        if untouched or unattached:
            tid = self.register_raw(text, tuples, untouched, extras, src, src["locator"])
            r = self.tuples[tid]
            base.update({"event_kind": "raw_name", "tuples": [(r["event"], None, "미상", None, None)], "tuple_ids": [tid], "candidate_name": untouched, "anchor": src["locator"], "raw_reason": r["raw_reason"]})
            return base
        ids = [self.register(t, src, untouched) for t in tuples]
        base.update({"event_kind": "dict" if ids else None, "tuples": [(t["event"], t["site"][1] if t["site"] else None, t["course"], t["course_basis"], t["site_basis"]) for t in tuples], "tuple_ids": ids, "candidate_name": [], "anchor": None})
        return base

    def run_expression(self, text, src):
        """표현 — 단위를 가리키기만 한다(D). exact = 미등록 0 · 남는 조각 0 · 후보 전부 기존 단위와 세 칸 완전 일치. 아니면 unlinked + candidates."""
        groups = self.split(text)
        tuples, untouched, extras = self.assemble(groups)
        spans = [(s["kind"], s["canonical"], s["text"]) for g in groups for m in g["members"] for s in m["spans"]]
        cands = self.candidates_of(tuples)
        reasons = []
        if not cands:
            reasons.append("no_event")
        if untouched:
            reasons.append("unregistered")
        if extras["extra_sites"] or extras["extra_courses"]:
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
        return {"text": text, "spans": spans, "locator": src.get("locator"), "unregistered": untouched, "extra_sites": extras["extra_sites"], "extra_courses": extras["extra_courses"], "site_list_merges": extras["site_list_merges"],
                "b_splits": [(t["event"], t["site"][1] if t["site"] else None, t["course"], t["n_site_candidates"], t["n_course_candidates"]) for t in tuples if t["n_site_candidates"] >= 2 or t["n_course_candidates"] >= 2],
                "candidates": cands, "tuples": [(t["event"], t["site"][1] if t["site"] else None, t["course"], t["course_basis"], t["site_basis"]) for t in tuples],
                "tuple_ids": _dedupe(ids), "match_status": "exact" if exact else "unlinked", "unlinked_reasons": reasons}


def run_adverse(ids, rules, L):
    AT = AdverseTuples24(ids)
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
            r["patient_ko"] = {"text": src["patient_ko"], "tuples": r2["tuples"], "b_splits": r2["b_splits"], "site_list_merges": r2["site_list_merges"], "candidates": r2["candidates"], "tuple_ids": r2["tuple_ids"], "unregistered": r2["unregistered"], "extra_sites": r2["extra_sites"], "extra_courses": r2["extra_courses"], "match_status": r2["match_status"], "unlinked_reasons": r2["unlinked_reasons"]}
            union = r["candidates"] + [c for c in r2["candidates"] if c["would_be_id"] not in {x["would_be_id"] for x in r["candidates"]}]
            # 문헌 레코드 = statement(en) + patient_ko(ko) 한 레코드. 두 쪽 전부 exact 일 때만 exact(레코드 단위로 가리키기만 · 원칙 A·D)
            reasons = _dedupe(r["unlinked_reasons"] + r2["unlinked_reasons"])
            exact = r["match_status"] == "exact" and r2["match_status"] == "exact"
            if not exact and (r["tuple_ids"] or r2["tuple_ids"]):
                # 한쪽만 exact 였으면 그쪽이 붙인 출처를 뗀다 — 레코드 단위로 가리키기만
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
        adv_folded.append({"adverse_id": tid, "event_kind": t["event_kind"], "event": t["event"], "category": t["event_category"], "site_kind": t["site_kind"], "site": t["site"], "course": t["course"], "status": t["status"] if t["event_kind"] == "raw_name" else ("partial" if own_unreg else "complete"),
                           "all_dict_values": t["all_dict_values"], "anchor": t["anchor"], "n_names": len(names), "names": names, "unregistered": own_unreg, "event_fragments": t["event_fragments"], "extra_sites": t["extra_sites"], "extra_courses": t["extra_courses"],
                           "dict_tuples": t.get("dict_tuples"), "raw_reason": t.get("raw_reason"), "site_basis": t.get("site_basis"), "course_basis": t.get("course_basis")})
    adv_folded.sort(key=lambda x: (-x["n_names"], x["event_kind"], x["category"] or "", x["event"]))
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
    course_split = [{"name": f"{r['text']} [{r['modality']}]", "event_kind": r["event_kind"], "tuples": r["dict_tuples"]} for r in comp_rows
                    if r["dict_tuples"] and any(c in r["text"] for c in ("일시적", "지연성", "가역적", "Transient", "Delayed", "영구", "Late-Onset"))]
    # 수정 1 실측 — 멤버 밖에서 온 부위 0(멤버 밖에서 온 site) · 부위 나열 합치기 · 후보 둘 이상 분할 · 두통×주사 부위
    all_rows = comp_rows + expr_rows + [dict(r["patient_ko"], kind="patient_text", text=r["patient_ko"]["text"]) for r in expr_rows if r.get("patient_ko")]
    site_outside_member = [(r["text"][:40], t[:3]) for r in all_rows for t in r["tuples"] if t[1] and t[4] not in ("member", "site_list")]
    site_list_merges = [{"text": r["text"], "kind": r.get("kind", "complications"), "merges": r["site_list_merges"]} for r in all_rows if r.get("site_list_merges")]
    multi_cand = [{"text": r["text"], "kind": r.get("kind", "complications"), "tuples": [t[:3] for t in r["b_splits"]], "site_candidates": max(t[3] for t in r["b_splits"]), "course_candidates": max(t[4] for t in r["b_splits"])} for r in all_rows if r.get("b_splits")]
    headache_injection = [(r["text"][:40], t[:3]) for r in all_rows for t in r["tuples"] if t[0] == "두통" and t[1] == "주사 부위"]
    headache_injection_tuples = [t["id"] for t in A.values() if t["event"] == "두통" and t["site"] == "주사 부위"]
    unattached = [{"text": r["text"], "kind": r.get("kind", "complications"), "extra_sites": r["extra_sites"], "extra_courses": r["extra_courses"]} for r in all_rows if r["extra_sites"] or r["extra_courses"]]
    # 수정 2 실측 — raw_name 칸
    raw_cells = {"n": len(raw), "site_none": sum(1 for t in raw if t["site_id"] == "none"), "course_unknown": sum(1 for t in raw if t["course"] == "미상"), "with_dict_tuples": sum(1 for t in raw if t.get("dict_tuples")),
                 "by_reason": dict(Counter(t["raw_reason"] for t in raw)), "with_extra_sites": sum(1 for t in raw if t["extra_sites"]), "with_extra_courses": sum(1 for t in raw if t["extra_courses"])}
    # 수정 3 실측 — 표현 유래 새 튜플 0 · partial 연결 0 · 후보 단위
    new_from_expr = [t["id"] for t in A.values() if "complications" not in t["origins"]]
    partial_linked = [r["text"][:40] for r in expr_rows if r["tuple_ids_union"] and (r["unregistered"] or (r.get("patient_ko") or {}).get("unregistered") or r["extra_sites"] or r["extra_courses"] or (r.get("patient_ko") or {}).get("extra_sites") or (r.get("patient_ko") or {}).get("extra_courses"))]
    cand_units = Counter()
    cand_units_detail = {}
    for r in expr_rows:
        for c in all_cands(r):
            if not c["exists"]:
                cand_units[c["would_be_id"]] += 1
                cand_units_detail.setdefault(c["would_be_id"], {"event": c["event"], "site": c["site"], "site_kind": c["site_kind"], "course": c["course"], "expressions": 0, "kinds": Counter()})
                cand_units_detail[c["would_be_id"]]["expressions"] += 1
                cand_units_detail[c["would_be_id"]]["kinds"][r["kind"]] += 1
    cand_units_list = [dict(v, id=k, kinds=dict(v["kinds"])) for k, v in sorted(cand_units_detail.items(), key=lambda x: -x[1]["expressions"])]
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
        ("complications_by_category", dict(Counter(A[t]["event_category"] for t in comp_tuple_ids))),
        ("event_dictionary_values", len(ids.event)),
        ("event_dictionary_used_by_complications", len({A[t]["event"] for t in comp_tuple_ids if A[t]["event_kind"] == "dict"})),
        ("event_dictionary_unused", sorted(set(e["label"] for e in ids.event.values()) - {A[t]["event"] for t in comp_tuple_ids if A[t]["event_kind"] == "dict"})),
        ("course_dictionary_values", len(ids.course)),
        ("relative_site_values", len(ids.rsite)),
        ("course_member_only", True),
        ("site_member_only", True),
        ("expressions_create_units", False),
        ("course_split_examples", course_split),
        ("lop", [{"name": r["text"], "event_kind": r["event_kind"], "tuples": [t[:3] for t in r["tuples"]], "dict_tuples": r["dict_tuples"]} for r in lop]),
        # 수정 1
        ("site_outside_member", len(site_outside_member)),
        ("site_outside_member_examples", site_outside_member[:10]),
        ("site_list_merges", len(site_list_merges)),
        ("site_list_merges_all", site_list_merges),
        ("multi_candidate_splits", len(multi_cand)),
        ("multi_candidate_splits_all", multi_cand),
        ("headache_x_injection_site", len(headache_injection)),
        ("headache_x_injection_site_tuples", headache_injection_tuples),
        ("unattached_fragments_texts", len(unattached)),
        ("unattached_fragments_all", unattached),
        # 수정 2
        ("raw_cells", raw_cells),
        # 수정 3
        ("expressions", OrderedDict((k, kind_summary(k)) for k in ["safety_phrase", "emergency_sign", "symptom_phrase", "evidence_statement"])),
        ("expressions_by_origin", OrderedDict((o, {"n": sum(1 for r in expr_rows if r["origin"] == o), "linked": sum(1 for r in expr_rows if r["origin"] == o and r["linked"]), "unlinked": sum(1 for r in expr_rows if r["origin"] == o and not r["linked"])}) for o in dict.fromkeys(r["origin"] for r in expr_rows))),
        ("expressions_total", {"n": len(expr_rows), "linked": sum(1 for r in expr_rows if r["linked"]), "unlinked": sum(1 for r in expr_rows if not r["linked"]), "match_status": dict(Counter(r["match_status"] for r in expr_rows)),
                               "unlinked_reasons": dict(Counter(x for r in expr_rows if not r["linked"] for x in r["unlinked_reasons"])), "patient_text_records": 4 * sum(1 for r in expr_rows if r["kind"] == "evidence_statement")}),
        ("expressions_raw_name_tuples", sum(1 for t in A.values() if t["event_kind"] == "raw_name" and "complications" not in t["origins"])),
        ("expressions_new_tuples", len(new_from_expr)),
        ("expressions_partial_linked", len(partial_linked)),
        ("expressions_partial_linked_examples", partial_linked[:10]),
        ("candidate_units_not_existing", len(cand_units)),
        ("candidate_units_not_existing_expressions", sum(cand_units.values())),
        ("candidate_units_not_existing_all", cand_units_list),
        ("literature_basis", dict(Counter(r.get("basis") for r in expr_rows if r["kind"] == "evidence_statement"))),
        ("tuples_total", len(A)),
        ("tuples_dict", len(dict_t)),
        ("tuples_raw_name", len(raw)),
        ("tuples_by_origin", OrderedDict((o, sum(1 for t in A.values() if o in t["origins"])) for o in dict.fromkeys(o for t in A.values() for o in t["origins"]))),
        ("tuples_status", dict(Counter(t["status"] for t in A.values()))),
        ("tuples_by_course", dict(Counter(t["course"] for t in A.values()))),
        ("tuples_by_site_kind", dict(Counter(t["site_kind"] for t in A.values()))),
        ("tuples_by_category", dict(Counter(t["event_category"] for t in A.values()))),
        ("tuples_all_dict_values", sum(1 for t in A.values() if t["all_dict_values"])),
        ("tuples_with_expression_sources", sum(1 for t in A.values() if any(s_["origin"] != "complications" for s_ in t["sources"]))),
        ("tuples_with_2plus_names_raw", sum(1 for f in af2 if f["event_kind"] == "raw_name")),
        ("folded_with_2plus_names", len(af2)),
        ("folded_with_partial_name", sum(1 for f in af2 if f["status"] == "partial")),
        ("folded_partial_detail", [{"event": f["event"], "site": f["site"], "course": f["course"], "names": f["names"], "unregistered": f["unregistered"]} for f in af2 if f["status"] == "partial"]),
        ("unregistered_distinct", len(adv_unreg)),
        ("unregistered_total", sum(adv_unreg.values())),
        ("unregistered_all", adv_unreg.most_common()),
        ("unregistered_by_origin", {k: v.most_common() for k, v in adv_unreg_by_origin.items()}),
    ])
    return OrderedDict([("summary", summary), ("tuples", list(A.values())), ("complications", comp_rows), ("folded", adv_folded), ("expressions", expr_rows)])


# ---------------------------------------------------------------------------
# 전체 실행 · 집계 — 시술 축은 v2.3 그대로
# ---------------------------------------------------------------------------
def run_all(dic_json, rules, L, resolve_rules=None):
    if resolve_rules is None:
        sys.path.insert(0, HERE)
        import erd_spec_v24
        resolve_rules = erd_spec_v24.RESOLVE_RULES
    out = V23.run_all(dic_json, rules, L, resolve_rules)
    ids = V2.Ids(dic_json, L)
    out["adverse"] = run_adverse(ids, rules, L)
    out["erd_version"] = "v2.4"
    out["site_member_only"] = True
    out["expressions_create_units"] = False
    out["raw_name_cells"] = "none/미상"
    out["principles"] = PRINCIPLES
    return out


v21_split = V23.v21_split


def load_v23_summary():
    try:
        j = json.load(open(os.path.join(HERE, "erd-v2.3-tuples.json"), encoding="utf-8"))
        return j["procedure"]["summary"], j["adverse"]["summary"]
    except (FileNotFoundError, KeyError):
        return None, None


def _kv(d):
    return ", ".join(f"{k}={v}" for k, v in (d or {}).items())


def procedure_md(R, v23s=None):
    """시술 축 §9.5 — v2.3 과 수치가 같다(규칙 불변). v2.3 표 생성기를 v2.3 수치와 나란히 돌리고 판 표기만 바꾼다."""
    v23s = v23s or load_v23_summary()[0] or {}
    s = V23.procedure_md(R, v23s)
    return s.replace("v2.3", "v2.4").replace("v2.2", "v2.3").replace("erd-v2.3-tuples", "erd-v2.4-tuples").replace("erd-v2.2-tuples", "erd-v2.3-tuples")


def adverse_md(R, v23a=None):
    s = R["adverse"]["summary"]
    v23a = v23a or load_v23_summary()[1] or {}
    g = lambda k, d="—": v23a.get(k, d)  # noqa
    o = []
    A = o.append
    A("#### 9.6.1 complications 65 → 튜플 (v2.3 → v2.4 나란히)")
    A("")
    A(md_table(["항목", "v2.3", "v2.4"], [
        ("이름", g("complications_names"), s["complications_names"]), ("튜플이 생긴 이름", g("complications_names_with_tuple"), s["complications_names_with_tuple"]),
        ("튜플이 안 생긴 이름(사건 조각 없음)", "; ".join(g("complications_names_without_tuple", [])) or "0", "; ".join(s["complications_names_without_tuple"]) or "0"),
        ("raw_name 튜플이 된 이름(이름마다 고유)", f"**{g('complications_names_raw')}** (사전 튜플 이름 {g('complications_names_dict')})", f"**{s['complications_names_raw']}** (사유 {_kv(s['complications_names_raw_by_reason'])} · 사전 튜플 이름 {s['complications_names_dict']})"),
        ("사건이 둘 이상인 이름(튜플 둘 이상)", g("complications_names_multi_tuple"), s["complications_names_multi_tuple"]),
        ("튜플 수(distinct)", f"**{g('complications_distinct_tuples')}** (사전 {g('complications_distinct_tuples_dict')} + raw_name {g('complications_distinct_tuples_raw')} · 비율 {g('complications_fold_ratio')})", f"**{s['complications_distinct_tuples']}** (65 → N · 사전 튜플 {s['complications_distinct_tuples_dict']} + raw_name {s['complications_distinct_tuples_raw']} · 비율 {s['complications_fold_ratio']})"),
        ("둘 이상 이름이 접힌 튜플", f"{g('complications_tuples_with_2plus_names')} (미등록 섞임 {g('complications_folded_with_unregistered')})", f"{s['complications_tuples_with_2plus_names']} (전부 세 칸 사전 값·미등록 0: {s['complications_folded_all_dict_values']} · 미등록 조각 섞임 **{s['complications_folded_with_unregistered']}**)"),
        ("경과", _kv(g("complications_by_course", {})), _kv(s["complications_by_course"]) + f" (사전 튜플만 {_kv(s['complications_by_course_dict_only'])})"),
        ("부위", _kv(g("complications_by_site_kind", {})), _kv(s["complications_by_site_kind"])),
        ("분류", _kv(g("complications_by_category", {})), _kv(s["complications_by_category"])),
        ("사건 사전 최종 값", f"**{g('event_dictionary_values')}**", f"**{s['event_dictionary_values']}** (사전 튜플 이름이 쓴 값 {s['event_dictionary_used_by_complications']} · 안 쓰인 값: {', '.join(s['event_dictionary_unused']) or '없음'})"),
        ("경과 사전 값 · 상대 부위 사전 값", f"{g('course_dictionary_values')} · {g('relative_site_values')}", f"{s['course_dictionary_values']} · {s['relative_site_values']}"),
    ]))
    A("")
    A("#### 9.6.2 65 가 접힌 결과 — 튜플마다 어떤 이름들이 갔는지 전부 (v2.4 재실측 · raw_name 튜플은 이름 하나씩 · site none · course 미상)")
    A("")
    rows = [(i + 1, f["event_kind"], f["category"] or "—", f["event"] if f["event_kind"] == "dict" else f"(raw) {f['event']}", f"{f['site'] or 'none'}({f['site_kind']})", f["course"], f["n_names"], " · ".join(f["names"]),
             ", ".join(f["unregistered"]) or "—",
             ((" + ".join(f"({t[0]}, {t[1] or 'none'}, {t[2]})" for t in (f["dict_tuples"] or [])) or "(사건 조각 없음)") if f["event_kind"] == "raw_name" else "—") + (f" / S:{','.join(f['extra_sites'])}" if f["extra_sites"] else "") + (f" / C:{','.join(f['extra_courses'])}" if f["extra_courses"] else ""))
            for i, f in enumerate(R["adverse"]["folded"])]
    A(md_table(["#", "event_kind", "분류", "event", "site", "course", "이름 수", "접힌 complications 이름(전부)", "미등록 조각(candidate_name)", "raw_name 의 사전 분해(dict_tuples · 보존만) / extra"], rows))
    A("")
    A("#### 9.6.2a 경과 규칙 실측 (사건에 바로 붙은 수식어만 · v2.3 그대로) — 수식어가 있는 이름 전부(사전 분해 결과)")
    A("")
    A(md_table(["#", "이름", "event_kind", "사전 분해 (event, site, course)"], [(i + 1, x["name"], x["event_kind"], " + ".join(f"({t[0]}, {t[1] or 'none'}, {t[2]})" for t in x["tuples"])) for i, x in enumerate(s["course_split_examples"])]))
    A("")
    for x in s["lop"]:
        dt = " + ".join("(%s, %s, %s)" % (t[0], t[1] or "none", t[2]) for t in x["dict_tuples"])
        A(f"- LOP: 「{x['name']}」 → event_kind={x['event_kind']} · 튜플 칸 {[t for t in x['tuples']]} · 사전 분해 {dt} — v2.4: raw 칸은 none/미상(이름 전체에서 끌어오지 않음 · 2-B′), 사전 분해는 dict_tuples 에 보존(adverse_tuple_assign 의 재료)")
    A("")
    A("#### 9.6.2b 부위 규칙 실측 (v2.4 수정 1 · 2-A′ · 원칙 B·C) — 이름·표현 전부")
    A("")
    A(f"- 사건 멤버 밖(같은 묶음 · outer · 이름 전체)에서 온 site 가 들어간 튜플·후보 **{s['site_outside_member']}** (v2.3 은 멤버 밖에서 끌어온 쌍 119 · 검토 2-A′) — 튜플·후보마다 site_basis ∈ {{member, site_list}} 를 다시 세었다.")
    A(f"- 「두통 × 주사 부위」류 틀린 조합: 튜플·후보 **{s['headache_x_injection_site']}** · 튜플 {s['headache_x_injection_site_tuples'] or 0} (v2.3 ADV-ef3a30183f 는 사라졌다).")
    A(f"- 부위 나열 멤버 합치기(부위 조각만인 멤버가 같은 묶음에서 사건 멤버 바로 앞) **{s['site_list_merges']}** 건 — 전부:")
    for m in s["site_list_merges_all"]:
        A(f"  - [{m['kind']}] 「{m['text']}」 → " + " · ".join(f"{x['site_members']} + 「{x['event_member']}」 → 부위 후보 {x['sites']} × 사건 {x['events']}" for x in m["merges"]))
    A(f"- 한 칸(부위 또는 경과)에 후보가 둘 이상이라 단위를 나눈 것(원칙 B · 사건마다 후보 수만큼) **{s['multi_candidate_splits']}** 건 — 전부(괄호 안 동의어가 만드는 같은 사건의 미상 튜플은 여기 속하지 않는다 · §12):")
    for m in s["multi_candidate_splits_all"]:
        A(f"  - [{m['kind']}] 「{m['text']}」 → " + " + ".join(f"({t[0]}, {t[1] or 'none'}, {t[2]})" for t in m["tuples"]) + f" (부위 후보 {m['site_candidates']} · 경과 후보 {m['course_candidates']})")
    A(f"- 사건에 붙지 않은 부위·경과 조각이 남은 문자열(버리지 않고 extra_* 에 보존 · 접지 않는다) **{s['unattached_fragments_texts']}** 건 — 전부(complications 이름은 raw_name · 표현은 unlinked):")
    for m in s["unattached_fragments_all"]:
        A(f"  - [{m['kind']}] 「{m['text']}」 → S:{m['extra_sites']} C:{m['extra_courses']}")
    A("")
    A("#### 9.6.2c raw_name 칸 실측 (v2.4 수정 2 · 2-B′)")
    A("")
    rc = s["raw_cells"]
    A(f"- raw_name 튜플 {rc['n']}: site none **{rc['site_none']}/{rc['n']}** · course 미상 **{rc['course_unknown']}/{rc['n']}** (v2.3: course 지연·일시 3 · site 주사 부위 2 가 이름 전체에서 왔다) · 사유 {_kv(rc['by_reason'])} · 사전 분해 보존(dict_tuples) {rc['with_dict_tuples']} · extra_sites 보존 {rc['with_extra_sites']} · extra_courses 보존 {rc['with_extra_courses']}")
    A("")
    A("#### 9.6.3 표현(adverse_expression) → 단위 (v2.4: match_status exact / unlinked — 표현은 단위를 가리키기만 한다)")
    A("")
    rows = [(k, v["n"], v["linked"], v["unlinked"], _kv(v["unlinked_reasons"]), v["distinct_tuples"], v["new_tuples_not_from_complications"], v["candidate_units_not_existing"]) for k, v in s["expressions"].items()]
    t = s["expressions_total"]
    rows.append(("**합계**", t["n"], t["linked"], t["unlinked"], _kv(t["unlinked_reasons"]), "", s["expressions_new_tuples"], s["candidate_units_not_existing"]))
    A(md_table(["kind", "표현 수", "exact(R29)", "unlinked", "unlinked 사유(중복 셈)", "distinct 튜플(기존 단위)", "65 에 없던 새 튜플", "기존 단위에 없는 후보 단위(distinct)"], rows))
    A("")
    A("- 출처별(exact/전체): " + " · ".join(f"{k} {v['linked']}/{v['n']}" for k, v in s["expressions_by_origin"].items()))
    ge = g("expressions_total", {})
    A(f"- v2.3: linked {ge.get('linked')}/{ge.get('n')} (그중 partial {ge.get('match_status', {}).get('partial')}) → v2.4 exact {t['linked']}/{t['n']} · unlinked {t['unlinked']} — 미등록 조각이 있거나(unregistered) · 사건에 붙지 않은 조각이 남거나(unattached_fragments) · 후보가 기존 단위에 없거나(no_unit) · 사건 조각이 없으면(no_event) 연결하지 않는다(원칙 A·D). partial 인데 연결된 표현 **{s['expressions_partial_linked']}**.")
    A(f"- 표현이 만든 튜플(raw_name {s['expressions_raw_name_tuples']} · 사전 튜플 {s['expressions_new_tuples']}) — v2.3 의 「65 에 없던 새 튜플 57」은 **0**. 그 자리는 후보 단위 {s['candidate_units_not_existing']}(표현 {s['candidate_units_not_existing_expressions']} 건)로 표현 레코드의 candidates 에 남는다(adverse_tuple_assign kind=expression 의 재료).")
    A(f"- 문헌 32: statement/patient_ko 두 쪽 전부 exact 일 때만 — " + ", ".join(f"{k}={v}" for k, v in s["literature_basis"].items()) + f" · patient_text 표현 레코드 {t['patient_text_records']}(4개 언어 × 32)")
    A("")
    A("#### 9.6.4 튜플 전체 집계 (65 유래뿐 · v2.3 → v2.4)")
    A("")
    A(md_table(["항목", "v2.3", "v2.4"], [
        ("튜플 수", f"**{g('tuples_total')}** (사전 {g('tuples_dict')} + raw_name {g('tuples_raw_name')})", f"**{s['tuples_total']}** (사전 {s['tuples_dict']} + raw_name {s['tuples_raw_name']}) = complications 65 유래 전부"),
        ("원천별(표현은 exact 로 붙은 출처)", _kv(g("tuples_by_origin", {})), _kv(s["tuples_by_origin"])),
        ("표현 출처가 붙은 튜플", "—", s["tuples_with_expression_sources"]),
        ("상태", _kv(g("tuples_status", {})), _kv(s["tuples_status"])), ("경과", _kv(g("tuples_by_course", {})), _kv(s["tuples_by_course"])),
        ("부위", _kv(g("tuples_by_site_kind", {})), _kv(s["tuples_by_site_kind"])), ("분류", _kv(g("tuples_by_category", {})), _kv(s["tuples_by_category"])),
        ("세 칸 전부 사전 값(접힘 가능) 튜플", g("tuples_all_dict_values"), s["tuples_all_dict_values"]),
        ("미등록 조각", f"distinct {g('unregistered_distinct')} · 총 {g('unregistered_total')}", f"distinct {s['unregistered_distinct']} · 총 {s['unregistered_total']}"),
    ]))
    A("")
    A(f"표현에서 새로 생긴 튜플(65 에 없던 것): **{s['expressions_new_tuples']}** (v2.3 57). 기존 단위에 없는 후보 단위 {s['candidate_units_not_existing']} 중 표현 수 상위 40(전부는 `erd-v2.4-tuples.json → adverse.summary.candidate_units_not_existing_all`):")
    A("")
    A(md_table(["#", "event", "site", "course", "표현 수", "kind"], [(i + 1, c["event"], f"{c['site'] or 'none'}({c['site_kind']})", c["course"], c["expressions"], _kv(c["kinds"])) for i, c in enumerate(s["candidate_units_not_existing_all"][:40])]))
    A("")
    A("#### 9.6.5 미등록 조각 전부 (출처별 · 횟수) — 사전 추가는 실버 빌드의 결정 묶음(dictionary_add · adverse_tuple_assign)")
    A("")
    for k, v in s["unregistered_by_origin"].items():
        A(f"- **{k}** ({len(v)}): " + " · ".join(f"`{f}`×{n}" for f, n in v))
    A("")
    A("#### 9.6.6 미등록 조각 있는 이름이 접혔는가 — v2.4 재실측")
    A("")
    A(f"- 둘 이상 이름이 접힌 부작용 튜플 {s['folded_with_2plus_names']} 중 미등록 조각 있는 이름이 섞인 튜플 **{s['folded_with_partial_name']}** (v2.3: {g('folded_with_partial_name')}). raw_name 튜플 {s['complications_distinct_tuples_raw']} 은 전부 이름 하나씩(접힘 0) · 칸은 none/미상.")
    if s["folded_with_partial_name"]:
        A("")
        A(md_table(["#", "event", "site", "course", "접힌 이름(전부)", "미등록 조각"], [(i + 1, d["event"], d["site"] or "none", d["course"], " · ".join(d["names"]), ", ".join(d["unregistered"])) for i, d in enumerate(s["folded_partial_detail"])]))
    A("")
    A("v2.3 의 raw_name 18 은 v2.4 에서도 raw_name 이며 칸만 none/미상으로 바뀌었다(「육아종 / 지연성 염증성 결절」[M2] 지연 → 미상 · 「통증·불편감 및 지연성 통증(LOP)」[M14] 지연 → 미상 · 「감각이상·저림 (…가역적)」[M16] 일시 → 미상 · 「주사 부위 반응 (…)」[M7]·「주사부위 반응 (…)」[M9] 주사 부위 → none · extra_sites 보존). 사전 분해는 dict_tuples 에 남는다.")
    return "\n".join(o)


def load_all():
    for name in ("erd-v2.4-dictionaries.json", "erd-v2.3-dictionaries.json"):
        if os.path.exists(os.path.join(HERE, name)):
            dic = json.load(open(os.path.join(HERE, name), encoding="utf-8"))
            break
    try:
        erd = json.load(open(os.path.join(HERE, "erd-v2.4.json"), encoding="utf-8"))
        rules, rrules = erd["tuple_rules"], erd["resolve_rules"]
    except (FileNotFoundError, KeyError):
        sys.path.insert(0, HERE)
        import erd_spec_v24
        rules, rrules = erd_spec_v24.TUPLE_RULES, erd_spec_v24.RESOLVE_RULES
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
    json.dump(R, open(os.path.join(HERE, "erd-v2.4-tuples.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    print("\n→ erd-v2.4-tuples.json")


if __name__ == "__main__":
    main()
