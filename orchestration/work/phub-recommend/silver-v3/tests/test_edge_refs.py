# -*- coding: utf-8 -*-
"""ERD v3.2 §5 edge_create — ref 구조체 5(anchor · locator · procedure_tuple · adverse_tuple(세 칸) · dict_value) × 관계 34(R29 없음 · R32 · R33 · R34 · R35) 의 양끝.
경우는 enumerate_cases.ref_cases 가 erd-v3.2.json 에서 뽑는다(허용 끝 = accept · 허용 밖·만들 수 없는 관계 = reject). 합성 빌드는 v3.2(synth.ERD33_PATH).
합성 빌드 한 번에 경우마다 결정 하나(edge_create)를 넣고, 적용 로그·만든 엣지의 끝 종류를 본다."""
import collections

from base import ERD, T, build, mkid
from registry import covers, mark
import enumerate_cases as EC
import synth
from lib.provenance import loc

KIND_ORDER = ["anchor", "adverse_tuple", "dict_value", "locator", "procedure_tuple"]
DIC = synth.dictionaries()


def dict_name_for(etype):
    names = {d["name"] for d in DIC["dictionaries"]}
    for n in (etype, f"{etype}_label", f"{etype}_name"):
        if n in names:
            return n
    return None


# dict_value 가 가리킬 사전 값(합성 사전의 정준값 — 계열 안에서 하나인 값)
DICT_VALUE = {"modality": "알파톡신", "modality_subcategory": "주름알파", "product": "알파투", "technique": "injection", "site": "턱", "problem": "주름고민",
              "problem_subcategory": "잔주름", "catalog_item": "알파원 턱 주사", "person_condition": "알레르기"}


def unique_locators(S):
    """원장 locator → 그 locator 를 출처로 가진 실버 레코드가 하나뿐인 것(개체 종류별 · 정렬)."""
    idx = collections.defaultdict(set)
    for et, recs in S.E.items():
        for rid, rec in recs.items():
            seen = set()
            for cells in list(rec["attrs"].values()) + [rec.get("aliases", [])]:
                for c in cells:
                    for p in c.get("prov", []):
                        seen.add(loc(p))
            seen |= {d for d in rec.get("derived_from", []) if ".json:" in d}
            for l in seen:
                idx[l].add((et, rid))
    out = collections.defaultdict(list)
    for l in sorted(idx):
        if len(idx[l]) == 1:
            et, rid = next(iter(idx[l]))
            out[et].append((l, rid))
    return out


class RefFactory:
    def __init__(self, S):
        self.S = S
        self.ul = unique_locators(S)
        it = S.ctx["items"][("M1", "알파원 턱 주사")]
        self.anchor = it["cat"]["catalog_item_id"]
        t = S.ctx["proc"]["PT"].tuples[it["cat"]["procedure_id"]]
        self.ptuple = {"what_id": t["what_id"], "site_id": t["site_id"], "technique_id": t["technique_id"]}

    def make(self, kind, etype):
        if kind == "anchor":
            return {"kind": "anchor", "anchor": self.anchor}
        if kind == "procedure_tuple":
            return {"kind": "procedure_tuple", "tuple": dict(self.ptuple)}
        if kind == "adverse_tuple":
            return {"kind": "adverse_tuple", "tuple": {"event": "멍", "site": "none", "qualifier": "none"}}
        if kind == "dict_value":
            return {"kind": "dict_value", "dict": {"dictionary": dict_name_for(etype), "canonical": DICT_VALUE[etype]}}
        if kind == "locator":
            if etype == "adverse_effect":
                return {"kind": "locator", "locator": "complications.json:categories[].complications[].name@M1/7"}  # complications 이름의 ERD locator(v3.2 이름 → 단위)
            return {"kind": "locator", "locator": self.ul[etype][0][0]}
        raise ValueError(kind)

    def expected_id(self, kind, etype):
        """양성 경우에 만들어질 끝 id(한 끝만 보는 종류)."""
        if kind == "locator" and etype != "adverse_effect":
            return self.ul[etype][0][1]
        return None


def filler(case_by, rel, side):
    """반대쪽 끝 — 그 관계 그 쪽에서 accept 인 (kind, 개체) 중 KIND_ORDER 첫 번째."""
    for k in KIND_ORDER:
        for c in case_by[(rel, side)]:
            if c["ref_kind"] == k and c["expect"] == "accept":
                return c
    return None


class EdgeRefs(T):
    @classmethod
    def setUpClass(cls):
        erd = EC.load(synth.ERD33_PATH)
        cls.cases = [c for c in EC.enumerate_all(erd, DIC_REAL()) if c["category"] == "ref"]
        w, S0 = build("plain33", erd_path=synth.ERD33_PATH)
        F = RefFactory(S0)
        case_by = collections.defaultdict(list)
        for c in cls.cases:
            case_by[(c["relation"], c["side"])].append(c)
        decs, plan = [], {}
        for i, c in enumerate(cls.cases):
            other = "to" if c["side"] == "from" else "from"
            fc = filler(case_by, c["relation"], other)
            mine = F.make(c["ref_kind"], c["end_type"])
            theirs = F.make(fc["ref_kind"], fc["end_type"]) if fc else {"kind": "anchor", "anchor": F.anchor}
            tgt = {"relation": c["relation"], "from_ref": mine if c["side"] == "from" else theirs, "to_ref": mine if c["side"] == "to" else theirs}
            did = f"DEC-2099-01-01-E{i:04d}"
            decs.append(synth.dec(did, "edge_create", tgt, {"attrs": {"basis": "합성 시험"}}))
            plan[c["id"]] = (did, c, F.expected_id(c["ref_kind"], c["end_type"]))
        cls.plan = plan
        cls.w, cls.S = build("edge_refs33", decs, erd_path=synth.ERD33_PATH)

    def test_ref_cases(self):
        S = self.S
        logs = {x["id"]: x for x in S.apply_log if x["kind"] == "edge_create"}
        bad = []
        for cid, (did, c, want_id) in self.plan.items():
            lg = logs.get(did)
            ok = True
            if c["expect"] == "accept":
                if not lg or lg["result"] != "applied":
                    ok = False
                else:
                    side_types = {e.split("→")[0 if c["side"] == "from" else 1].split(":")[0] for e in lg["ends"]}
                    side_ids = {e.split("→")[0 if c["side"] == "from" else 1].split(":", 1)[1] for e in lg["ends"]}
                    if side_types != {c["end_type"]} or (want_id and side_ids != {want_id}):
                        ok = False
            else:
                if not lg or lg["result"] != "rejected":
                    ok = False
            if ok:
                mark(cid, "test_ref_cases")
            else:
                bad.append((cid, c["expect"], lg and lg.get("result"), lg and (lg.get("why") or lg.get("ends"))))
        self.assertEqual(bad, [], f"{len(bad)} 경우 실패: {bad}")

    @covers("kind:edge_create", "kind:edge_create:ref.kind=anchor", "kind:edge_create:ref.kind=locator", "kind:edge_create:ref.kind=procedure_tuple",
            "kind:edge_create:ref.kind=adverse_tuple", "kind:edge_create:ref.kind=dict_value", "order:⑤:edge_create")
    def test_edge_attrs_and_provenance(self):
        """만든 엣지: 결정 attrs 를 칸으로(derived_from = 결정 id) · decision_id · 끝 깊이. 같은 양끝 엣지가 있으면 덧붙인다(중복 생성 없음)."""
        S = self.S
        made = [e for rel in S.R for e in S.R[rel] if str(e["attrs"].get("decision_id", {}).get("value", "")).startswith("DEC-2099-01-01-E")]
        self.assertTrue(made)
        for e in made:
            self.assertEqual(e["attrs"]["basis"]["value"], "합성 시험")
            self.assertTrue(e["attrs"]["basis"]["derived_from"][0].startswith("DEC-"))
        kinds = {x["result"] for x in S.apply_log if x["kind"] == "edge_create"}
        self.assertEqual(kinds, {"applied", "rejected"})
        merged = [x for x in S.apply_log if x["kind"] == "edge_create" and x.get("merged_into_existing")]
        self.assertTrue(merged)


def DIC_REAL():
    import json
    import os
    with open(os.path.join(EC.ERD_DIR, "erd-v3.3-dictionaries.json"), encoding="utf-8") as f:
        return json.load(f)
