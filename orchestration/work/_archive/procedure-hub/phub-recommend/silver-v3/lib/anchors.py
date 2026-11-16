# -*- coding: utf-8 -*-
"""anchor 지도 — 결정이 가리키는 안정 키(CAT-/REF-/locator) → 튜플.

시술: anchor(CAT- · REF- · …#m<i> · v3 …#s<i>) 마다 튜플 명세(what, site, technique). 튜플 id 는 명세 + anchor 로 매번 계산(§1.1).
v3(V3-9): 튜플이 없는 미해결 참조 · 조합 멤버 · 부위별 anchor 도 결정 target — 결정이 그 anchor 의 명세를 세운다(establish).
결정 ② canonical_mapping · ③ tuple_assign(_multi) · ④ fold_approve · ⑦ exclude 는 anchor 의 명세·행선지를 바꾼다.
엣지는 anchor 를 가리키고, 쓰기 직전에 resolve(anchor) 로 최종 튜플 id 를 받는다 — 파생 id 를 결정이 직접 가리키지 않는다.
부작용(v3.1): 단위·문구 사전은 lib/units31.py(AdverseUnits).
"""
from collections import OrderedDict, defaultdict

from .decompose import tuple_id, DICT_WHAT_KINDS
from .provenance import P, loc, rec_str
from .util import mkid, norm, dedupe


class AnchorMap:
    def __init__(self, ctx):
        self.ctx = ctx
        self.spec = OrderedDict()       # anchor -> spec
        self.redirect = {}              # anchor -> anchor (fold)
        self.multi = {}                 # anchor -> [sub anchors]
        self.excluded = {}              # anchor -> decision id
        self.base_ids = {}              # anchor -> 결정 전 튜플 id
        self.established = {}           # anchor -> 결정 id (V3-9 — 분해가 튜플을 만들지 않은 자리를 결정이 세움)
        self.ref_occ = {}               # 참조 anchor(REF-) -> (occ, origin) — 미해결 참조 포함(V3-9 의 재료)
        self.dropped = {}               # anchor -> 결정 id (바탕 anchor 를 결정이 다시 지정해 쓰이지 않게 된 #m/#s 멤버 anchor)

    def add(self, anchor, t, origin, occ, extra=None):
        """t = 분해기 튜플 레코드(PT.tuples[...])."""
        s = self.spec.get(anchor)
        if s is None:
            s = {"anchor": anchor, "what_kind": t["what_kind"], "what_id": t["what_id"], "what_label": t["what_label"], "family": t.get("family"),
                 "site_id": t["site_id"], "site": t["site"], "technique_id": t["technique_id"], "technique": t["technique"], "technique_origin": t["technique_origin"],
                 "origins": [], "occ": [], "status": t["status"], "unregistered_fragments": list(t.get("unregistered_fragments", [])),
                 "candidate_name": list(t.get("candidate_name", [])), "extra_primaries": [], "extra_sites": [], "decision_ids": []}
            self.spec[anchor] = s
            self.base_ids[anchor] = t["id"]
        if origin not in s["origins"]:
            s["origins"].append(origin)
        for o in occ:
            if o not in s["occ"]:
                s["occ"].append(o)
        for k, v in (extra or {}).items():
            if v:
                s[k] = list(dict.fromkeys(s.get(k, []) + list(v)))
        return s

    def establish(self, anchor, decision_id):
        """V3-9 — 튜플이 없는 anchor(미해결 참조 REF- · 그 #m<i>/#s<i>)에 빈 명세를 세운다. 그 참조가 원장에 없으면 None."""
        if anchor in self.spec:
            return self.spec[anchor]
        base = anchor.split("#", 1)[0]
        if base not in self.ref_occ:
            return None
        occ, origin = self.ref_occ[base]
        s = {"anchor": anchor, "what_kind": None, "what_id": None, "what_label": None, "family": None, "site_id": "none", "site": None, "technique_id": "none", "technique": None,
             "technique_origin": "none", "origins": [origin], "occ": list(occ), "status": "complete", "unregistered_fragments": [], "candidate_name": [], "extra_primaries": [], "extra_sites": [],
             "decision_ids": [], "established_by": decision_id}
        self.spec[anchor] = s
        self.established[anchor] = decision_id
        if anchor != base:
            # 부위별·멤버 anchor 를 세우면 바탕 참조는 그 anchor 들의 묶음(multi)
            if base not in self.spec:
                self.spec[base] = {"anchor": base, "occ": list(occ), "origins": [origin], "virtual": True, "established_by": decision_id}
                self.established[base] = decision_id
            subs = self.multi.setdefault(base, [])
            if anchor not in subs:
                subs.append(anchor)
                subs.sort()
        return s

    @staticmethod
    def tid(s):
        return tuple_id(s["what_id"], s["site_id"], s["technique_id"], s["what_kind"], s["anchor"])[0]

    def resolve(self, anchor):
        """anchor → 최종 튜플 id 목록(제외면 [])."""
        seen = set()
        a = anchor
        while a in self.redirect and a not in seen:
            seen.add(a)
            a = self.redirect[a]
        if a in self.excluded or anchor in self.excluded:
            return []
        if a in self.multi:
            return dedupe(t for m in self.multi[a] for t in self.resolve(m))
        s = self.spec.get(a)
        return [self.tid(s)] if s and not s.get("virtual") and s.get("what_id") else []

    def reassign_base(self, anchor, decision_id):
        """조합·부위 여럿 anchor 를 결정이 한 튜플(또는 지정 여럿)로 다시 정할 때 — 옛 멤버 anchor(#m/#s)는 바탕 anchor 로 접는다."""
        for m in self.multi.pop(anchor, []):
            if m != anchor:
                self.dropped[m] = decision_id
                self.redirect[m] = anchor
        s = self.spec.get(anchor)
        if s is not None:
            s.pop("virtual", None)
        return s

    def tuples(self):
        """튜플 id → 합친 레코드(같은 id 에 닿은 anchor 전부)."""
        out = OrderedDict()
        for a, s in self.spec.items():
            if a in self.multi or a in self.redirect or a in self.excluded or a in self.dropped or s.get("virtual"):
                continue
            tid = self.tid(s)
            t = out.get(tid)
            if t is None:
                all_dict = s["what_kind"] in DICT_WHAT_KINDS and s["site_id"] != "none" and s["technique_id"] != "none"
                t = {"id": tid, "what_kind": s["what_kind"], "what_id": s["what_id"], "what_label": s["what_label"], "family": s["family"], "site_id": s["site_id"], "site": s["site"],
                     "technique_id": s["technique_id"], "technique": s["technique"], "technique_origin": s["technique_origin"], "anchor": None if all_dict else s["anchor"],
                     "all_dict_values": all_dict, "origins": [], "occ": [], "anchors": [], "status": "complete", "unregistered_fragments": [], "candidate_name": [],
                     "extra_primaries": [], "extra_sites": [], "decision_ids": [], "alias_ids": []}
                out[tid] = t
            t["anchors"].append(a)
            for k in ("origins", "occ", "unregistered_fragments", "candidate_name", "extra_primaries", "extra_sites", "decision_ids") + V32_KEYS:
                t.setdefault(k, [])
                for v in s.get(k, []):
                    if v not in t[k]:
                        t[k].append(v)
            st = s["status"]
            if st == "partial" or t["status"] == "partial":
                t["status"] = "partial"
            elif st == "ambiguous":
                t["status"] = "ambiguous"
            b = self.base_ids.get(a)
            if b and b != tid and b not in t["alias_ids"]:
                t["alias_ids"].append(b)
        # fold 로 사라진 anchor 의 결정 전 id 는 alias
        for a, k in self.redirect.items():
            for tid in self.resolve(k):
                b = self.base_ids.get(a)
                if tid in out and b and b != tid and b not in out[tid]["alias_ids"]:
                    out[tid]["alias_ids"].append(b)
                for o in self.spec.get(a, {}).get("occ", []):
                    if tid in out and o not in out[tid]["occ"]:
                        out[tid]["occ"].append(o)
                for o in self.spec.get(a, {}).get("origins", []):
                    if tid in out and o not in out[tid]["origins"]:
                        out[tid]["origins"].append(o)
        for a, subs in self.multi.items():
            for m in subs:
                for tid in self.resolve(m):
                    if tid in out:
                        for o in self.spec.get(a, {}).get("occ", []):
                            if o not in out[tid]["occ"]:
                                out[tid]["occ"].append(o)
        return out


V32_KEYS = ("grammar_tokens", "ingredient_fragments", "gloss")   # v3.2(V3.2-1 · V3.2-2 · V3.2-6) 이름·참조 분해가 뗀 조사·어미 · 병기 gloss · 성분 조각(보존 · 칸 아님)


def _v32_extra(r):
    return {k: list(r.get(k) or []) for k in V32_KEYS if r.get(k)}


def build_anchor_map(ctx):
    """분해 결과(① 분류 항목 · ② 참조 · ③ market) → AnchorMap. 결정 전 튜플 집합은 분해기 PT.tuples 와 같아야 한다(빌드가 검사)."""
    D = ctx["proc"]
    PT = D["PT"]
    AM = AnchorMap(ctx)
    items = ctx["items"]
    for c in D["cat_recs"]:
        it = items[(c["family"], c["name"])]
        occ = [it["name_loc"]]
        extra = {"extra_primaries": c.get("extra_primaries", []), "extra_sites": c.get("extra_sites", []), **_v32_extra(c)}
        if c["result"] in ("combo_ref", "multi_tuple"):
            for a, pid in zip(c["member_anchors"], c["member_pids"]):
                AM.add(a, PT.tuples[pid], "catalog_item", occ, _v32_extra(c))
            AM.multi[c["catalog_item_id"]] = list(c["member_anchors"])
            AM.spec.setdefault(c["catalog_item_id"], {"anchor": c["catalog_item_id"], "occ": occ, "origins": ["catalog_item"], "virtual": True})
        else:
            AM.add(c["catalog_item_id"], PT.tuples[c["procedure_id"]], "catalog_item", occ, extra)
    occs = ctx["occ"]
    from .decompose import MARKET_SLOT
    rows = dict(D["ref_rows"])
    rows[MARKET_SLOT] = D["mk_rows"]
    for slot, rr in rows.items():
        origin = "market_pricing" if slot == MARKET_SLOT else "reference"
        occ_by = defaultdict(list)
        for lab, hint, pv, _ in occs[slot]:
            occ_by[(lab, hint)].append(loc(pv))
        for r in rr:
            occ = occ_by[tuple(r["_in"])]
            if r.get("ref_id") and r["result"] != "node":
                prev = AM.ref_occ.get(r["ref_id"])
                AM.ref_occ[r["ref_id"]] = (dedupe((prev[0] if prev else []) + occ), prev[1] if prev else origin)
            if r["result"] == "tuple":
                AM.add(r["anchor"], PT.tuples[r["procedure_id"]], origin, occ, _v32_extra(r))
            elif r["result"] in ("combo_ref", "multi_tuple"):
                for a, pid in zip(r["member_anchors"], r["member_pids"]):
                    AM.add(a, PT.tuples[pid], origin, occ, _v32_extra(r))
                if r["result"] == "multi_tuple":
                    # 「무엇을 하나 × 부위 여럿」(V3-4) — 참조 anchor 는 부위별 튜플(#s<i>)의 묶음
                    AM.multi[r["ref_id"]] = list(r["member_anchors"])
                    s0 = AM.spec.setdefault(r["ref_id"], {"anchor": r["ref_id"], "occ": [], "origins": [origin], "virtual": True})
                    for o in occ:
                        if o not in s0["occ"]:
                            s0["occ"].append(o)
    return AM
