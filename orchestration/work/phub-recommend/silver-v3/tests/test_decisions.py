# -*- coding: utf-8 -*-
"""ERD v3.1 §5.2 결정 kind 20 × target/new_value 분기 · §5.4 적용 순서 ⓪①~⑦(① 안 kind 순서) · §1.1 결정 target 안정 키. 합성 원장 + 합성 결정."""
import json

from base import ERD, T, build, log, mkid, norm
from registry import covers, mark
import synth
from synth import dec
from lib.decompose import ref_anchor
from lib.units31 import unit_id3

D = "2026-02-01"


def cat(f, n):
    return mkid("CAT", f"{f}|{n}")


def prd(code, name):
    return mkid("PRD", f"{code}|{name}")


SUB_ALPHA = mkid("SUB", "M1|주름알파")
TEC_INJ, TEC_THERMAL = mkid("TEC", "injection"), mkid("TEC", "thermal")       # technique 개체 id(고정 id · to_id)
TQ_INJ, TQ_THERMAL = mkid("DIC", "technique|injection"), mkid("DIC", "technique|thermal")  # 튜플의 technique_id = 기법 사전 id(§1.1)
SIT = lambda name, zone=None: mkid("SIT", zone or name)  # noqa
DIC = lambda d, c: mkid("DIC", f"{d}|{c}")  # noqa
EV = lambda c: DIC("adverse_event_type", c)  # noqa
CO = lambda c: DIC("course", c)  # noqa
QU = lambda c: DIC("adverse_qualifier", c)  # noqa


def entry(S, name, canonical):
    d = next(x for x in S.ctx["dic"]["dictionaries"] if x["name"] == name)
    return next((e for e in d["entries"] if norm(e["canonical"]) == norm(canonical)), None)


def spec(S, a):
    return S.ctx["AM"].spec.get(a)


def resolve(S, a):
    return S.ctx["AM"].resolve(a)


# ---------------------------------------------------------------------------
# ① 사전 단계 — dictionary_add · canonical_rename · (④ event_split) · ①→②
# ---------------------------------------------------------------------------
DICT_DECS = [
    dec("DEC-T-01-ADD1", "dictionary_add", {"dictionary": "site"}, {"canonical": "미지조각", "synonyms": [], "category": None, "kind": "anatomical"}),
    dec("DEC-T-01-ADD2", "dictionary_add", {"dictionary": "adverse_event_type"}, {"canonical": "미지증상", "synonyms": ["카테터"], "category": "염증/감염"}),
    dec("DEC-T-01-ADD3", "dictionary_add", {"dictionary": "없는사전"}, {"canonical": "x", "synonyms": [], "category": None}),
    dec("DEC-T-01-ADD4", "dictionary_add", {"dictionary": "product_name"}, {"canonical": "알파포", "synonyms": [{"value": "AlphaFour", "is_marketing_name": True}], "category": None, "code": "M1"}),
    dec("DEC-T-01-RN1", "canonical_rename", {"dictionary": "modality", "code": "M1", "canonical": "알파톡신"},
        {"canonical": "알파 독소", "old_as_synonym": True, "old_id_as_alias": True, "is_marketing_name": True}),
    dec("DEC-T-01-RN2", "canonical_rename", {"dictionary": "adverse_event_type", "code": None, "canonical": "통증"},
        {"canonical": "동통", "old_as_synonym": True, "old_id_as_alias": True, "is_marketing_name": None}),
    dec("DEC-T-01-RN3", "canonical_rename", {"dictionary": "adverse_event_type", "code": None, "canonical": "부종"},
        {"canonical": "멍", "old_as_synonym": True, "old_id_as_alias": True, "is_marketing_name": None}),  # 다른 값의 정준값 → 거부
    dec("DEC-T-04-SPLIT", "event_split", {"event": "과민반응"}, {"new_events": [{"canonical": "아나필락시스", "synonyms": [], "category": "전신"}]}),
    dec("DEC-T-02-AFTER-ADD", "canonical_mapping", {"from_ref": prd("M1", "알파톡"), "scope": ["*"]}, {"to_id": prd("M1", "알파포")}),
    # v3.1 ① dictionary_remove — 동의어 하나(synonym) · 값(synonym 없음 · 쓰면 거부) · ① 안 kind 순서(add 뒤 remove — decided_at 이 앞서도)
    dec("DEC-T-01-RMSYN", "dictionary_remove", {"dictionary": "adverse_event_type", "canonical": "부종", "synonym": "붓기"}, {"removed": True}),
    dec("DEC-T-01-RMUSE", "dictionary_remove", {"dictionary": "adverse_event_type", "canonical": "멍", "synonym": None}, {"removed": True}),
    dec("DEC-T-01-RMLATE", "dictionary_remove", {"dictionary": "course", "canonical": "영구", "synonym": "가상영구"}, {"removed": True}, decided_at="2026-01-01"),
    dec("DEC-T-01-ADDLATE", "dictionary_add", {"dictionary": "course"}, {"canonical": "영구", "synonyms": ["가상영구"], "category": None}, decided_at="2026-03-01"),
    dec("DEC-T-01-ADDFREE", "dictionary_add", {"dictionary": "adverse_qualifier"}, {"canonical": "가상물질", "synonyms": [], "category": None}),
    dec("DEC-T-01-RMFREE", "dictionary_remove", {"dictionary": "adverse_qualifier", "canonical": "가상물질"}, {"removed": True}),
    # v3.1 ① phrase_map — PHR- id · normalized · units [] = 부작용 아님
    dec("DEC-T-01-PMAP", "phrase_map", {"phrase_id": mkid("PHR", "새로운증상")}, {"units": [{"event": "부종", "site": "none", "qualifier": "none"}], "courses": ["일시"], "status": "approved"}),
    dec("DEC-T-01-PMAPN", "phrase_map", {"normalized": "미지반응"}, {"units": [], "courses": None, "status": "approved"}),
    dec("DEC-T-01-PMAPX", "phrase_map", {"phrase_id": "PHR-0000000000"}, {"units": [], "courses": None, "status": "approved"}),
    dec("DEC-T-01-PMAPBAD", "phrase_map", {"normalized": "합성고지"}, {"units": [{"event": "없는사건", "site": "none", "qualifier": "none"}], "courses": None, "status": "approved"}),
    # v3.1 ⓪ product_reclassify — product_id · product(사전 값)
    dec("DEC-T-00-PRC1", "product_reclassify", {"product_id": prd("M1", "알파쓰리")}, {"to_modality_code": "M2"}),
    dec("DEC-T-00-PRC2", "product_reclassify", {"product": {"dictionary": "product_name", "canonical": "감마투"}}, {"to_modality_code": "M1"}),
    dec("DEC-T-00-PRCX", "product_reclassify", {"product": {"dictionary": "product_name", "canonical": "없는제품"}}, {"to_modality_code": "M1"}),
]


class DictionaryStage(T):
    @classmethod
    def setUpClass(cls):
        cls.w, cls.S = build("dict", DICT_DECS)
        cls.w0, cls.S0 = build("plain")

    @covers("kind:dictionary_add", "kind:dictionary_add:new_value.kind=str", "kind:dictionary_add:new_value.kind=null", "order:①:dictionary_add")
    def test_dictionary_add(self):
        S = self.S
        self.assertEqual(log(S, "DEC-T-01-ADD1")["stage"], "①")
        e = entry(S, "site", "미지조각")
        self.assertEqual((e["id"], e["category"] if "category" in e else None, e["kind"]), (DIC("site", "미지조각"), None, "anatomical"))
        self.assertEqual(e["sources"][0]["decision_id"], "DEC-T-01-ADD1")
        # 분해를 다시 돌린다 — 「베타원 미지조각」 은 이제 튜플 · 항목 「알파원 미지조각」 complete
        r = [x for rr in S.ctx["proc"]["ref_rows"].values() for x in rr if x["label"] == "베타원 미지조각"][0]
        self.assertEqual(r["result"], "tuple")
        self.assertEqual(S.ctx["proc"]["PT"].catalog[("M1", "알파원 미지조각")]["status"], "complete")
        self.assertEqual(S.E["site"][SIT("미지조각")]["attrs"]["kind"][0]["value"], "anatomical")
        # category=str — 사건 사전 · 부작용 분해도 다시
        e2 = entry(S, "adverse_event_type", "미지증상")
        self.assertEqual(e2["category"], "염증/감염")
        rows = {r["text"]: r for r in S.ctx["adv"]["complications"]}
        self.assertEqual(rows["미지증상 멍"]["event_kind"], "dict")
        self.assertEqual(rows["카테터 감염"]["event_kind"], "dict")
        # 동의어 is_marketing_name 표시
        e4 = entry(S, "product_name", "알파포")
        self.assertEqual(e4["synonyms"][0].get("is_marketing_name"), True)
        # 사전이 없으면 거부
        self.assertEqual(log(S, "DEC-T-01-ADD3")["result"], "rejected")

    @covers("kind:canonical_rename", "kind:canonical_rename:target.code=str", "kind:canonical_rename:target.code=null", "kind:canonical_rename:new_value.is_marketing_name=bool",
            "kind:canonical_rename:new_value.is_marketing_name=null", "order:①:canonical_rename")
    def test_canonical_rename(self):
        S, S0 = self.S, self.S0
        e = entry(S, "modality", "알파 독소")
        self.assertEqual((e["code"], e["id"]), ("M1", DIC("modality", "알파 독소")))
        self.assertEqual(e["renamed_from"][0]["id"], DIC("modality", "알파톡신"))
        old = [s for s in e["synonyms"] if s["value"] == "알파톡신"][0]
        self.assertEqual((old["link"], old.get("is_marketing_name")), ("renamed_from", True))
        # 코드 기반 개체 id 그대로 — MOD- · CAT- · PRD- · 튜플 · 엣지
        self.assertEqual(set(S.E["modality"]), set(S0.E["modality"]))
        self.assertEqual(set(S.E["catalog_item"]), set(S0.E["catalog_item"]))
        self.assertEqual(spec(S, cat("M1", "알파원 이마"))["what_id"], spec(S0, cat("M1", "알파원 이마"))["what_id"])
        # 옛 정준값은 동의어라 분해가 계속 닿는다
        r = [x for x in S.ctx["proc"]["mk_rows"] if x["label"] == "알파톡신(알파투)"][0]
        self.assertEqual(r["result"], "tuple")
        # 코드 없는 값(사건) — DIC 재계산 · is_marketing_name 표시 없음
        e2 = entry(S, "adverse_event_type", "동통")
        self.assertEqual(e2["id"], EV("동통"))
        self.assertNotIn("is_marketing_name", [s for s in e2["synonyms"] if s["value"] == "통증"][0])
        self.assertEqual(log(S, "DEC-T-01-RN3")["result"], "rejected")

    @covers("kind:event_split", "order:④:event_split")
    def test_event_split(self):
        S = self.S
        lg = log(S, "DEC-T-04-SPLIT")
        self.assertEqual((lg["result"], lg["stage"]), ("applied", "④"))
        self.assertNotIn("아나필락시스", [s["value"] for s in entry(S, "adverse_event_type", "과민반응")["synonyms"]])
        u = [u for u in S.E["adverse_effect"].values() if u["attrs"]["event"][0]["value"] == "아나필락시스"]
        self.assertTrue(u)
        u0 = [u for u in self.S0.E["adverse_effect"].values() if u["attrs"]["event"][0]["value"] == "과민반응"]
        self.assertTrue(u0)

    @covers("order:①->②", "kind:canonical_mapping:target.from_ref=MOD-/SUB-/PRD-_id", "kind:canonical_mapping:target.scope=[\"*\"]", "stable:allow:PRD-")
    def test_dict_then_mapping(self):
        """② 가 ① 에서 생긴 사전 값(알파포)을 to_id 로 쓴다 — ① 이 먼저라 적용된다."""
        S = self.S
        lg = log(S, "DEC-T-02-AFTER-ADD")
        self.assertEqual(lg["result"], "applied")
        a = ref_anchor("알파톡", "M2")
        self.assertEqual(spec(S, a)["what_id"], prd("M1", "알파포"))
        idx = [x["id"] for x in S.apply_log]
        self.assertLess(idx.index("DEC-T-01-ADD4"), idx.index("DEC-T-02-AFTER-ADD"))


    @covers("kind:dictionary_remove", "kind:dictionary_remove:target.synonym=str", "kind:dictionary_remove:target.synonym=null", "order:①:dictionary_remove")
    def test_dictionary_remove(self):
        S = self.S
        lg = log(S, "DEC-T-01-RMSYN")
        self.assertEqual((lg["result"], lg["stage"]), ("applied", "①"))
        self.assertNotIn("붓기", [x["value"] for x in entry(S, "adverse_event_type", "부종")["synonyms"]])
        d = next(x for x in S.ctx["dic"]["dictionaries"] if x["name"] == "adverse_event_type")
        self.assertEqual(d["removed_synonyms"][-1]["decision_id"], "DEC-T-01-RMSYN")
        # 값 제거 — 쓰는 레코드가 있으면 거부(in_use) · 안 쓰면 빠지고 이력
        lg = log(S, "DEC-T-01-RMUSE")
        self.assertEqual(lg["result"], "rejected")
        self.assertIn("in_use", lg["why"])
        self.assertIsNotNone(entry(S, "adverse_event_type", "멍"))
        self.assertEqual(log(S, "DEC-T-01-RMFREE")["result"], "applied")
        self.assertIsNone(entry(S, "adverse_qualifier", "가상물질"))
        dq = next(x for x in S.ctx["dic"]["dictionaries"] if x["name"] == "adverse_qualifier")
        self.assertEqual(dq["removed_entries"][-1]["canonical"], "가상물질")
        # ① 안 kind 순서: dictionary_remove 는 같은 단계의 dictionary_add 를 전부 적용한 뒤(decided_at 이 앞서도)
        self.assertEqual(log(S, "DEC-T-01-RMLATE")["result"], "applied")
        idx = [x["id"] for x in S.apply_log]
        self.assertLess(idx.index("DEC-T-01-ADDLATE"), idx.index("DEC-T-01-RMLATE"))

    @covers("kind:phrase_map", "kind:phrase_map:target.phrase_id", "kind:phrase_map:target.normalized", "order:①:phrase_map", f"rule:tuple_rules.adverse.status_values[approved]")
    def test_phrase_map(self):
        S = self.S
        AU = S.ctx["AU"]
        lg = log(S, "DEC-T-01-PMAP")
        self.assertEqual((lg["result"], lg["stage"]), ("applied", "①"))
        e = AU.phrases[mkid("PHR", "새로운증상")]
        u = unit_id3(EV("부종"), "none", "none")
        self.assertEqual((e["status"], e["units"], e["mapped_courses"]), ("approved", [u], ["일시"]))
        # 그 항목의 자리에서 R15(source_phrases · 경과 = 지도 경과)
        es = [x for x in S.R["R15"] if mkid("PHR", "새로운증상") in x["attrs"].get("source_phrases", {}).get("value", [])]
        self.assertTrue(es and all(x["attrs"]["course"]["value"] == ["일시"] for x in es))
        # normalized target · units [] = 부작용 아님(approved · 단위 없음 · 게이트에서 빠진다)
        e2 = AU.phrases[mkid("PHR", "미지반응")]
        self.assertEqual((log(S, "DEC-T-01-PMAPN")["result"], e2["status"], e2["units"]), ("applied", "approved", []))
        self.assertEqual(log(S, "DEC-T-01-PMAPX")["result"], "no_target")
        self.assertEqual(log(S, "DEC-T-01-PMAPBAD")["result"], "rejected")
        idx = [x["id"] for x in S.apply_log]
        self.assertLess(idx.index("DEC-T-01-RMSYN"), idx.index("DEC-T-01-PMAP"))   # ① 끝(remove 뒤)

    @covers("kind:product_reclassify", "kind:product_reclassify:target.product_id", "kind:product_reclassify:target.product", "order:⓪:product_reclassify")
    def test_product_reclassify(self):
        S = self.S
        lg = log(S, "DEC-T-00-PRC1")
        self.assertEqual((lg["result"], lg["stage"], lg["old_id"], lg["new_id"]), ("applied", "⓪", prd("M1", "알파쓰리"), prd("M2", "알파쓰리")))
        rec = S.E["product"][prd("M2", "알파쓰리")]
        self.assertIn(prd("M1", "알파쓰리"), [a["value"] for a in rec["aliases"]])     # 옛 id 는 alias
        self.assertNotIn(prd("M1", "알파쓰리"), S.E["product"])
        r4 = [e for e in S.R["R4"] if e["to"]["id"] == prd("M2", "알파쓰리")]
        self.assertTrue(r4 and all(e["from"]["id"] == mkid("MOD", "M2") for e in r4))   # R4 새 계열
        self.assertEqual(entry(S, "product_name", "알파쓰리")["code"], "M2")
        self.assertEqual(log(S, "DEC-T-00-PRC2")["new_id"], prd("M1", "감마투"))
        self.assertEqual(log(S, "DEC-T-00-PRCX")["result"], "rejected")
        idx = [x["id"] for x in S.apply_log]
        self.assertLess(idx.index("DEC-T-00-PRC1"), idx.index("DEC-T-01-ADD1"))     # ⓪ → ①


# ---------------------------------------------------------------------------
# ② ③ ④ — canonical_mapping · tuple_assign(_multi) · adverse_tuple_assign · fold_approve
# ---------------------------------------------------------------------------
A_HEAT = ref_anchor("알파원 열 주사", None)
A_OR = ref_anchor("알파투/베타원", None)
A_S = ref_anchor("알파원 이마+미간", None)
A_MIX = ref_anchor("알파원+베타원/감마원", None)
A_MP = ref_anchor("알파투 베타원", None)
A_BETA_S = ref_anchor("베타필러(턱+볼)", None)
A_BETA_BOL = ref_anchor("베타필러 볼", "M2")
A_LABEL = ref_anchor("미지조각2 이마", "M1")
A_G1, A_G2 = ref_anchor("감마원 볼", "M3"), ref_anchor("감마원,볼", "M3")
A_T1, A_T2 = ref_anchor("감마원 턱", "M3"), ref_anchor("감마원  턱", "M3")
LOC_RAW = "complications.json:categories[].complications[].name@M1/7"     # 괴사 (이마)
LOC_RAWQ = "complications.json:categories[].complications[].name@M1/10"   # 부종 · 공기
LOC_EXPR = "extracted.json:{code}.safety.common[]@M1/1"                   # 새로운증상

TUPLE_DECS = [
    dec("DEC-T-02-R5", "canonical_mapping", {"from_ref": "R5:M1", "scope": ["*"]}, {"to_id": TEC_INJ}),
    dec("DEC-T-02-R5SUB", "canonical_mapping", {"from_ref": "R5:M3-1", "scope": [cat("M3", "감마원 피부")]}, {"to_id": TEC_THERMAL}),
    dec("DEC-T-02-LABEL", "canonical_mapping", {"from_ref": "미지조각2", "scope": [A_LABEL]}, {"to_id": prd("M1", "알파투")}),
    dec("DEC-T-02-MOD", "canonical_mapping", {"from_ref": prd("M2", "베타원"), "scope": [cat("M2", "베타원 볼")]}, {"to_id": mkid("MOD", "M2")}),
    dec("DEC-T-03-CAT", "tuple_assign", {"catalog_item_id": cat("M3", "감마토닝")}, {"what_kind": "product", "what_id": prd("M3", "감마원"), "site_id": SIT("볼"), "technique_id": TEC_THERMAL}),
    dec("DEC-T-03-REF", "tuple_assign", {"ref_id": A_HEAT}, {"what_kind": "product", "what_id": prd("M1", "알파원"), "site_id": "none", "technique_id": TEC_THERMAL}),
    dec("DEC-T-03-M", "tuple_assign", {"ref_id": A_OR + "#m1"}, {"what_kind": "product", "what_id": prd("M2", "베타원"), "site_id": SIT("볼"), "technique_id": TEC_INJ}),
    dec("DEC-T-03-S", "tuple_assign", {"ref_id": A_S + "#s1"}, {"what_kind": "product", "what_id": prd("M1", "알파원"), "site_id": SIT("미간", "glabella"), "technique_id": TEC_INJ}),
    dec("DEC-T-03-BAD", "tuple_assign", {"ref_id": A_MP}, {"what_kind": "product", "what_id": "PRD-0000000000", "site_id": "none", "technique_id": "none"}),
    dec("DEC-T-03-LAYER", "tuple_assign", {"ref_id": A_MP}, {"what_kind": "product", "what_id": prd("M1", "알파투"), "site_id": SIT("피부"), "technique_id": "none"}),
    dec("DEC-T-03-NOREF", "tuple_assign", {"ref_id": "REF-ffffffffff"}, {"what_kind": "product", "what_id": prd("M1", "알파투"), "site_id": "none", "technique_id": "none"}),
    dec("DEC-T-03-MC", "tuple_assign_multi", {"catalog_item_id": cat("M1", "알파원 이마 미간")},
        {"tuples": [{"what_kind": "product", "what_id": prd("M1", "알파원"), "site_id": SIT("이마", "forehead"), "technique_id": "none"},
                    {"what_kind": "product", "what_id": prd("M1", "알파원"), "site_id": SIT("미간", "glabella"), "technique_id": "none"}], "member_mode": "and"}),
    dec("DEC-T-03-MOR", "tuple_assign_multi", {"ref_id": A_MIX},
        {"tuples": [{"what_kind": "product", "what_id": prd("M1", "알파원"), "site_id": "none", "technique_id": "none"},
                    {"what_kind": "product", "what_id": prd("M2", "베타원"), "site_id": "none", "technique_id": "none"},
                    {"what_kind": "product", "what_id": prd("M3", "감마원"), "site_id": "none", "technique_id": "none"}], "member_mode": "or"}),
    dec("DEC-T-03-MAND", "tuple_assign_multi", {"ref_id": A_MP},
        {"tuples": [{"what_kind": "product", "what_id": prd("M1", "알파투"), "site_id": "none", "technique_id": "none"},
                    {"what_kind": "product", "what_id": prd("M2", "베타원"), "site_id": "none", "technique_id": "none"}], "member_mode": "and"}),
    dec("DEC-T-03-ADVR", "adverse_tuple_assign", {"locator": LOC_RAW, "kind": "raw_name"},
        {"tuples": [{"event_id": EV("괴사"), "site_id": SIT("이마", "forehead"), "qualifier_id": "none"}], "courses": ["지연"]}),
    dec("DEC-T-03-ADVQ", "adverse_tuple_assign", {"locator": LOC_RAWQ, "kind": "raw_name"},
        {"tuples": [{"event_id": EV("부종"), "site_id": "none", "course_id": CO("일시"), "qualifier_id": QU("공기")}]}),   # 옛 네 칸 — 경과는 R15 로
    dec("DEC-T-03-ADVE", "adverse_tuple_assign", {"locator": LOC_EXPR, "kind": "expression"},
        {"tuples": [{"event_id": EV("부종"), "site_id": "none", "course_id": CO("일시"), "qualifier_id": "none"}]}),
    dec("DEC-T-03-ADVX", "adverse_tuple_assign", {"locator": "complications.json:categories[].complications[].name@M9/0", "kind": "raw_name"},
        {"tuples": [{"event_id": EV("멍"), "site_id": "none", "course_id": CO("미상"), "qualifier_id": "none"}]}),
    dec("DEC-T-04-FOLDC", "fold_approve", {"anchors": [cat("M1", "알파원 이마"), cat("M2", "알파원 이마")]}, {"keep_anchor": cat("M1", "알파원 이마")}),
    dec("DEC-T-04-FOLDM", "fold_approve", {"anchors": [A_OR + "#m0", cat("M1", "알파원")]}, {"keep_anchor": cat("M1", "알파원")}),
    dec("DEC-T-04-FOLDS", "fold_approve", {"anchors": [A_BETA_S + "#s1", A_BETA_BOL]}, {"keep_anchor": A_BETA_BOL}),
    dec("DEC-T-04-FOLD7", "fold_approve", {"anchors": [A_G1, A_G2]}, {"keep_anchor": A_G1}),
    dec("DEC-T-04-FOLDX", "fold_approve", {"anchors": [A_G1, "REF-eeeeeeeeee"]}, {"keep_anchor": A_G1}),
    # ③→④ — 지정(③)한 anchor 를 접는다(④): 남는 튜플은 ③ 이 정한 값
    dec("DEC-T-04-AFTER3", "fold_approve", {"anchors": [A_HEAT, A_T1]}, {"keep_anchor": A_HEAT}),
]


class TupleStage(T):
    @classmethod
    def setUpClass(cls):
        cls.w, cls.S = build("tuples", TUPLE_DECS)
        cls.w0, cls.S0 = build("plain")

    @covers("kind:canonical_mapping", "kind:canonical_mapping:target.from_ref=R5:<계열>", "order:②:canonical_mapping", "stable:allow:TEC-")
    def test_mapping_r5(self):
        S = self.S
        self.assertEqual(log(S, "DEC-T-02-R5")["stage"], "②")
        s = spec(S, cat("M1", "알파원 이마"))
        self.assertEqual((s["technique_id"], s["technique_origin"]), (TQ_INJ, "decision"))
        self.assertEqual(spec(S, cat("M2", "베타원 볼"))["technique_id"], "none")   # 다른 계열(M2)은 R5:M1 범위 밖
        # V3-8 하위분류 단위 — 그 하위분류 항목만 · R5 엣지(modality_subcategory → technique)
        self.assertEqual(spec(S, cat("M3", "감마원 피부"))["technique_id"], TQ_THERMAL)
        self.assertTrue([e for e in S.R["R5"] if e["from"]["type"] == "modality_subcategory" and e["attrs"]["basis"]["value"] == "canonical_mapping"])

    @covers("kind:canonical_mapping:target.from_ref=라벨", "kind:canonical_mapping:target.scope=적용_범위의_anchor_목록", "stable:allow:REF-")
    def test_mapping_label(self):
        S = self.S
        r = [x for x in S.ctx["proc"]["mk_rows"] if x["label"] == "미지조각2 이마"][0]
        self.assertEqual(r["result"], "tuple")
        self.assertEqual(S.ctx["proc"]["PT"].tuples[r["procedure_id"]]["what_id"], prd("M1", "알파투"))
        self.assertEqual(log(S, "DEC-T-02-LABEL")["result"], "applied")
        # scope 밖 anchor 는 그대로(같은 조각이 다른 참조에 있어도) — 결정 전 빌드에서는 ⑨
        r0 = [x for x in self.S0.ctx["proc"]["mk_rows"] if x["label"] == "미지조각2 이마"][0]
        self.assertEqual(r0["result"], "unresolved")

    @covers("kind:canonical_mapping:target.from_ref=원장_canonical_category_의_CAT-_id", "stable:allow:CAT-", "stable:allow:SUB-", "stable:allow:MOD-")
    def test_mapping_catalog_category_and_mod(self):
        S = self.S
        memo = [d for d in S.ctx["decisions_approved"] if d["kind"] == "canonical_mapping" and d["target"]["from_ref"] == cat("M1", "알파톡신 이마")][0]
        self.assertEqual(memo["new_value"]["to_id"], SUB_ALPHA)
        self.assertEqual(spec(S, cat("M1", "알파톡신 이마"))["what_id"], SUB_ALPHA)
        self.assertEqual(spec(S, cat("M2", "베타원 볼"))["what_id"], mkid("MOD", "M2"))   # PRD → MOD(scope 안만)
        others = [a for a, x in S.ctx["AM"].spec.items() if not x.get("virtual") and x.get("what_id") == prd("M2", "베타원")]
        self.assertTrue(others)   # scope 밖(같은 what 의 다른 anchor)은 그대로

    @covers("kind:tuple_assign", "kind:tuple_assign:target.catalog_item_id", "kind:tuple_assign:target.ref_id", "order:③:tuple_assign", "stable:allow:SIT-")
    def test_tuple_assign(self):
        S = self.S
        s = spec(S, cat("M3", "감마토닝"))
        self.assertEqual((s["what_id"], s["site_id"], s["technique_id"], s["status"]), (prd("M3", "감마원"), SIT("볼"), TQ_THERMAL, "complete"))
        tid = resolve(S, cat("M3", "감마토닝"))[0]
        t = S.E["procedure"][tid]
        self.assertEqual(t["attrs"]["all_dict_values"][0]["value"], True)   # 세 칸 사전 값 → 접힘 가능(anchor 없는 id)
        self.assertEqual(tid, mkid("PRC", f"{prd('M3', '감마원')}|{SIT('볼')}|{TQ_THERMAL}"))
        self.assertIn("DEC-T-03-CAT", t["attrs"]["decision_ids"][0]["value"])
        # 거부: 사전에 없는 값 · layer 부위(V3-5) · 원장에 없는 anchor
        self.assertEqual(log(S, "DEC-T-03-BAD")["result"], "rejected")
        self.assertIn("V3-5", log(S, "DEC-T-03-LAYER")["why"])
        self.assertEqual(log(S, "DEC-T-03-NOREF")["result"], "rejected")

    @covers("kind:tuple_assign:target.ref_id", "conflict:⑨:established_by_decision")
    def test_tuple_assign_unresolved_ref(self):
        """V3-9 — 미해결 참조(⑨ · 튜플 없음)에도 적용(결정이 자리를 세운다) · 그 ⑨ 는 결정으로 닫힌다."""
        S = self.S
        lg = log(S, "DEC-T-03-REF")
        self.assertEqual((lg["result"], lg.get("established")), ("applied", True))
        self.assertTrue(resolve(S, A_HEAT))
        c = [c for c in S.conflicts if c["kind"] == "unresolved_reference" and c.get("ref_id") == A_HEAT][0]
        self.assertEqual((c["status"], c["decision_id"]), ("resolved", "DEC-T-03-REF"))
        self.assertTrue([e for e in S.R["R12"] if e["attrs"].get("target_label", {}).get("value") == "알파원 열 주사"])

    @covers("stable:allow:#m<i>", "stable:allow:#s<i>")
    def test_tuple_assign_member_anchors(self):
        S = self.S
        self.assertEqual(spec(S, A_OR + "#m1")["what_id"], prd("M2", "베타원"))
        self.assertEqual(spec(S, A_S + "#s1")["technique_id"], TQ_INJ)
        self.assertEqual(len(resolve(S, A_S)), 2)

    @covers("kind:tuple_assign_multi", "kind:tuple_assign_multi:target.catalog_item_id", "kind:tuple_assign_multi:target.ref_id", "kind:tuple_assign_multi:new_value.member_mode=and",
            "kind:tuple_assign_multi:new_value.member_mode=or", "order:③:tuple_assign_multi")
    def test_tuple_assign_multi(self):
        S = self.S
        lg = log(S, "DEC-T-03-MC")
        self.assertEqual((lg["shape"], lg["member_mode"], lg["sub_anchors"]), ("multi_tuple", "and", [cat("M1", "알파원 이마 미간") + "#s0", cat("M1", "알파원 이마 미간") + "#s1"]))
        self.assertEqual(len([e for e in S.R["R26"] if e["to"]["id"] == cat("M1", "알파원 이마 미간")]), 2)   # 분류 항목이면 튜플마다 R26
        lg = log(S, "DEC-T-03-MOR")
        self.assertEqual((lg["shape"], lg["member_mode"], lg.get("established")), ("combo_ref", "or", True))
        self.assertEqual(len(resolve(S, A_MIX)), 3)
        lg = log(S, "DEC-T-03-MAND")
        self.assertEqual((lg["shape"], lg["member_mode"]), ("combo_ref", "and"))
        es = [e for e in S.R["R12"] if e["attrs"].get("target_label", {}).get("value") == "알파원+베타원/감마원"]
        self.assertEqual({e["attrs"]["member_mode"]["value"] for e in es}, {"or"})
        self.assertEqual(len(es), 3)

    @covers("kind:adverse_tuple_assign", "order:③:adverse_tuple_assign", "stable:allow:locator")
    def test_adverse_tuple_assign(self):
        S = self.S
        AU = S.ctx["AU"]
        u = unit_id3(EV("괴사"), SIT("이마", "forehead"), "none")
        self.assertEqual(AU.name_units[LOC_RAW], [u])
        self.assertIn(u, S.E["adverse_effect"])              # 기존에 없던 단위 — 결정이 세운다(세 칸 사전 값)
        raw0 = self.S0.ctx["AU"].name_units[LOC_RAW][0]
        self.assertNotIn(raw0, S.E["adverse_effect"])           # raw_name 단위는 지정 단위로 대체
        es = [e for e in S.R["R15"] if e["to"]["id"] == u]
        self.assertTrue(es and es[0]["attrs"]["course"]["value"] == ["지연"])   # courses → R15 경과
        uq = unit_id3(EV("부종"), "none", QU("공기"))
        self.assertEqual(S.E["adverse_effect"][uq]["attrs"]["qualifier"][0]["value"], "공기")   # V3-1 qualifier_id
        self.assertEqual([e["attrs"]["course"]["value"] for e in S.R["R15"] if e["to"]["id"] == uq], [["일시"]])   # 옛 네 칸 course_id → R15 경과
        self.assertIn("옛 네 칸", log(S, "DEC-T-03-ADVQ")["note"])
        # 옛 kind=expression — 그 자리의 문구 사전 항목 지도로(phrase_map 과 같은 효과)
        lg = log(S, "DEC-T-03-ADVE")
        self.assertEqual((lg["result"], AU.phrases[lg["phrase_id"]]["status"]), ("applied", "approved"))
        self.assertEqual(log(S, "DEC-T-03-ADVX")["result"], "rejected")

    @covers("kind:fold_approve", "kind:fold_approve:target.anchors=CAT-/REF-_id", "kind:fold_approve:target.anchors=조합_멤버_anchor", "kind:fold_approve:target.anchors=부위별_튜플_anchor",
            "order:④:fold_approve", "order:③->④")
    def test_fold_approve(self):
        S = self.S
        keep = resolve(S, cat("M1", "알파원 이마"))
        self.assertEqual(resolve(S, cat("M2", "알파원 이마")), keep)
        t = S.E["procedure"][keep[0]]
        self.assertIn(self.S0.ctx["AM"].resolve(cat("M2", "알파원 이마"))[0], [a["value"] for a in t["aliases"]])   # 접힌 튜플 id 는 alias
        self.assertEqual(len([e for e in S.R["R26"] if e["from"]["id"] == keep[0]]), 2)   # 출처·R26 을 keep 로
        self.assertEqual(resolve(S, A_OR + "#m0"), resolve(S, cat("M1", "알파원")))
        self.assertEqual(resolve(S, A_BETA_S + "#s1"), resolve(S, A_BETA_BOL))
        self.assertEqual(log(S, "DEC-T-04-FOLDX")["result"], "rejected")
        # ③→④: ③ 이 세운 anchor 를 ④ 가 접는다 — 남는 튜플 = ③ 지정값
        self.assertEqual(resolve(S, A_T1), resolve(S, A_HEAT))
        self.assertEqual(S.E["procedure"][resolve(S, A_HEAT)[0]]["attrs"]["technique_id"][0]["value"], TQ_THERMAL)

    @covers("order:②->③")
    def test_mapping_then_assign(self):
        """② R5:M1 이 기법을 붙인 anchor 를 ③ 이 다시 지정하면 ③ 값이 남는다."""
        S = self.S
        s = spec(S, A_S + "#s1")
        self.assertEqual(s["technique_id"], TQ_INJ)
        self.assertEqual(spec(S, A_HEAT)["technique_id"], TQ_THERMAL)   # ② 는 injection 을 줄 자리지만(미해결이라 ② 때 튜플 없음) ③ thermal
        idx = [x["id"] for x in S.apply_log]
        self.assertLess(idx.index("DEC-T-02-R5"), idx.index("DEC-T-03-REF"))


# ---------------------------------------------------------------------------
# ⑤ ⑥ ⑦ · ⓪ · 기록만 · status
# ---------------------------------------------------------------------------
def late_decs(S0):
    c4 = next(c for c in S0.conflicts if c["rule_ref"] == "④")
    loc_cond = "pre-procedure-checklist.json:universal_checks[].label@0"
    return [
        dec("DEC-T-03-PRE", "adverse_tuple_assign", {"locator": LOC_RAW, "kind": "raw_name"},
            {"tuples": [{"event_id": EV("괴사"), "site_id": SIT("이마", "forehead"), "qualifier_id": "none"}], "courses": None}),
        dec("DEC-T-04-PRE", "fold_approve", {"anchors": [cat("M1", "알파원 이마"), cat("M2", "알파원 이마")]}, {"keep_anchor": cat("M1", "알파원 이마")}),
        # ③→⑤ · ④→⑤: 결정이 세운 단위 · 접힌 anchor 를 끝으로
        dec("DEC-T-05-R30", "edge_create", {"relation": "R30", "from_ref": {"kind": "adverse_tuple", "tuple": {"event": "색전", "site": "none", "course": "미상", "qualifier": "공기"}},
                                            "to_ref": {"kind": "adverse_tuple", "tuple": {"event": "괴사", "site": "이마", "course": "미상", "qualifier": "none"}}}, {"attrs": {"basis": "합성 인과"}}),
        dec("DEC-T-05-R16", "edge_create", {"relation": "R16", "from_ref": {"kind": "anchor", "anchor": cat("M2", "알파원 이마")},
                                            "to_ref": {"kind": "locator", "locator": "consent-checklist.json:categories[].contraindications[]@0/1"}}, {"attrs": {"level": "consent"}}),
        dec("DEC-T-05-SIT", "edge_create", {"relation": "R11", "from_ref": {"kind": "dict_value", "dict": {"dictionary": "problem_subcategory_label", "canonical": "잔주름"}},
                                            "to_ref": {"kind": "dict_value", "dict": {"id": SIT("턱")}}}, {"attrs": {}}),
        dec("DEC-T-05-REN", "edge_create", {"relation": "R22", "from_ref": {"kind": "dict_value", "dict": {"dictionary": "site", "canonical": "턱"}},
                                            "to_ref": {"kind": "dict_value", "dict": {"dictionary": "modality", "canonical": "알파 독소"}}}, {"attrs": {}}),
        dec("DEC-T-01-REN", "canonical_rename", {"dictionary": "modality", "code": "M1", "canonical": "알파톡신"},
            {"canonical": "알파 독소", "old_as_synonym": True, "old_id_as_alias": True, "is_marketing_name": None}),
        dec("DEC-T-05-TEC", "edge_create", {"relation": "R5", "from_ref": {"kind": "dict_value", "dict": {"id": mkid("MOD", "M2")}},
                                            "to_ref": {"kind": "dict_value", "dict": {"id": TEC_THERMAL}}}, {"attrs": {"basis": "합성"}}),
        dec("DEC-T-06-OVR", "conflict_override", {"conflict_key": c4["stable_key"]}, {"chosen_value": False}),
        dec("DEC-T-07-CAT", "exclude", {"kind": "catalog_item", "key": cat("M1", "베타필러 턱")}, {"excluded": True}),
        dec("DEC-T-07-REF", "exclude", {"kind": "reference", "key": ref_anchor("감마원 턱", "M3")}, {"excluded": True}),
        dec("DEC-T-07-LED", "exclude", {"kind": "ledger_record", "key": loc_cond}, {"excluded": True}),
        dec("DEC-T-07-DIC", "exclude", {"kind": "dictionary_value", "key": {"dictionary": "technique", "canonical": "regeneration"}}, {"excluded": True}),
        dec("DEC-T-CR", "conflict_resolution", {"erd_ref": "§5.1", "review_item": None}, {"disposition": "합성 처분"}),
        dec("DEC-T-SR", "scope_review", {"erd_ref": "§12", "review_item": None}, {"disposition": "합성 처분"}),
        dec("DEC-T-PROP", "dictionary_add", {"dictionary": "site"}, {"canonical": "제안부위", "synonyms": [], "category": None}, status="proposed"),
        dec("DEC-T-REJ", "dictionary_add", {"dictionary": "site"}, {"canonical": "거부부위", "synonyms": [], "category": None}, status="rejected"),
        dec("DEC-T-PRC", "tuple_assign", {"ref_id": "PRC-0123456789"}, {"what_kind": "product", "what_id": prd("M1", "알파투"), "site_id": "none", "technique_id": "none"}),
        dec("DEC-T-ADV", "fold_approve", {"anchors": ["ADV-0123456789", cat("M1", "알파원")]}, {"keep_anchor": cat("M1", "알파원")}),
        dec("DEC-T-CFL", "conflict_close", {"conflict_key": {"kind": "value_conflict", "locators": ["CFL-0123456789"]}}, {"verdict": "not_same", "note": "x"}),
    ]


class LateStage(T):
    @classmethod
    def setUpClass(cls):
        cls.w0, cls.S0 = build("plain")
        cls.decs = late_decs(cls.S0)
        cls.w, cls.S = build("late", cls.decs)

    @covers("order:④->⑤", "kind:edge_create")
    def test_edge_after_fold_and_assign(self):
        S = self.S
        lg = log(S, "DEC-T-05-R30")
        self.assertEqual(lg["result"], "applied")
        u_to = unit_id3(EV("괴사"), SIT("이마", "forehead"), "none")
        self.assertTrue([e for e in S.R["R30"] if e["to"]["id"] == u_to])
        lg = log(S, "DEC-T-05-R16")
        keep = S.ctx["AM"].resolve(cat("M1", "알파원 이마"))[0]
        self.assertEqual(lg["ends"][0].split("→")[0], f"procedure:{keep}")
        idx = [x["id"] for x in S.apply_log]
        self.assertLess(idx.index("DEC-T-04-PRE"), idx.index("DEC-T-05-R16"))

    def test_dict_value_fixed_ids_and_renamed(self):
        S = self.S
        self.assertEqual(log(S, "DEC-T-05-SIT")["result"], "applied")
        self.assertEqual(log(S, "DEC-T-05-TEC")["result"], "applied")
        # ① 이름 바꾼 정준값으로 가리켜도 같은 MOD-(코드 기반 id)
        lg = log(S, "DEC-T-05-REN")
        self.assertEqual((lg["result"], lg["ends"][0].split("→")[1]), ("applied", f"modality:{mkid('MOD', 'M1')}"))

    @covers("kind:conflict_override", "order:⑥:conflict_override", "order:⑤->⑥")
    def test_override(self):
        S = self.S
        c = [c for c in S.conflicts if c.get("decision_id") == "DEC-T-06-OVR"][0]
        self.assertEqual((c["status"], c["chosen_value"]), ("resolved", False))
        idx = [x["stage"] for x in S.apply_log if x["stage"] in ("⑤", "⑥", "⑦")]
        self.assertEqual(idx, sorted(idx, key=["⑤", "⑥", "⑦"].index))

    @covers("kind:exclude", "kind:exclude:target.kind=catalog_item", "kind:exclude:target.kind=reference", "kind:exclude:target.kind=ledger_record", "kind:exclude:target.kind=dictionary_value",
            "order:⑦:exclude", "order:⑥->⑦", "stable:allow:dict_value")
    def test_exclude(self):
        S = self.S
        for did in ("DEC-T-07-CAT", "DEC-T-07-REF", "DEC-T-07-LED", "DEC-T-07-DIC"):
            self.assertEqual((log(S, did)["result"], log(S, did)["stage"]), ("applied", "⑦"), did)
        self.assertEqual(S.E["catalog_item"][cat("M1", "베타필러 턱")]["status"], "excluded")
        self.assertEqual(S.ctx["AM"].resolve(cat("M1", "베타필러 턱")), [])
        self.assertEqual(S.ctx["AM"].resolve(ref_anchor("감마원 턱", "M3")), [])
        cond = S.E["person_condition"][mkid("CND", "check|알레르기")]   # v3.1 조건 단위(사전 값 · kind)
        self.assertEqual(cond["status"], "excluded")
        self.assertEqual(S.ctx["excluded_dict_values"][0]["canonical"], "regeneration")
        # ⑦ 은 마지막 — ⑥ 다음
        st = [x["stage"] for x in S.apply_log if x["stage"] in ("⑥", "⑦")]
        self.assertEqual(st[-1], "⑦")

    @covers("kind:reclassification", "order:⓪:reclassification")
    def test_reclassification(self):
        S = self.S
        cid = cat("M1", "알파원 볼")
        self.assertIn(cid, S.E["catalog_item"])                     # CAT- id 불변(트리 위치 계열 코드)
        e = [e for e in S.R["R2"] if e["to"]["id"] == cid][0]
        self.assertEqual(e["attrs"]["reclassified_modality_id"]["value"], mkid("MOD", "M2"))
        self.assertEqual([x["stage"] for x in S.apply_log if x["kind"] == "reclassification"], ["⓪"])

    @covers("kind:ledger_correction_note", "kind:verification_hold", "kind:conflict_resolution", "kind:scope_review")
    def test_record_only(self):
        S = self.S
        rec = {x["kind"]: x["result"] for x in S.apply_log if x["stage"] == "—"}
        self.assertEqual(rec, {"ledger_correction_note": "recorded", "verification_hold": "recorded", "conflict_resolution": "recorded", "scope_review": "recorded"})

    @covers("order:status=approved", "order:status=proposed", "order:status=rejected")
    def test_status(self):
        S = self.S
        listed = {d["id"]: d["status"] for d in S.ctx["decisions_listed"]}
        self.assertEqual((listed.get("DEC-T-PROP"), listed.get("DEC-T-REJ")), ("proposed", "rejected"))
        self.assertIsNone(entry(S, "site", "제안부위"))
        self.assertIsNone(entry(S, "site", "거부부위"))
        self.assertIn("DEC-T-07-CAT", [d["id"] for d in S.ctx["decisions_approved"]])

    @covers("stable:forbid:PRC-", "stable:forbid:ADV-", "stable:forbid:CFL-")
    def test_forbidden_derived_ids(self):
        S = self.S
        inv = {x["id"]: x["errors"] for x in S.ctx["decisions_invalid"]}
        for did, p in (("DEC-T-PRC", "PRC-"), ("DEC-T-ADV", "ADV-"), ("DEC-T-CFL", "CFL-")):
            self.assertIn(did, inv)
            self.assertTrue(any(p in e for e in inv[did]), inv[did])
            self.assertIsNone(log(S, did))


# ---------------------------------------------------------------------------
# 같은 단계 안 순서 — decided_at · id
# ---------------------------------------------------------------------------
ORDER_DECS = [
    dec("DEC-T-O-B", "canonical_rename", {"dictionary": "adverse_event_type", "code": None, "canonical": "감염증"}, {"canonical": "감염질환", "old_as_synonym": True}, decided_at="2026-02-02"),
    dec("DEC-T-O-A", "canonical_rename", {"dictionary": "adverse_event_type", "code": None, "canonical": "감염"}, {"canonical": "감염증", "old_as_synonym": True}, decided_at="2026-02-01"),
    dec("DEC-T-O-2", "canonical_rename", {"dictionary": "adverse_event_type", "code": None, "canonical": "괴사증"}, {"canonical": "조직괴사", "old_as_synonym": True}, decided_at="2026-02-03"),
    dec("DEC-T-O-1", "canonical_rename", {"dictionary": "adverse_event_type", "code": None, "canonical": "괴사"}, {"canonical": "괴사증", "old_as_synonym": True}, decided_at="2026-02-03"),
]


class SameStageOrder(T):
    @covers("order:same_stage=decided_at", "order:same_stage=id")
    def test_same_stage(self):
        w, S = build("order", ORDER_DECS)
        for did in ("DEC-T-O-A", "DEC-T-O-B", "DEC-T-O-1", "DEC-T-O-2"):
            self.assertEqual(log(S, did)["result"], "applied", did)
        self.assertIsNotNone(entry(S, "adverse_event_type", "감염질환"))
        self.assertIsNotNone(entry(S, "adverse_event_type", "조직괴사"))
        idx = [x["id"] for x in S.apply_log]
        self.assertLess(idx.index("DEC-T-O-A"), idx.index("DEC-T-O-B"))
        self.assertLess(idx.index("DEC-T-O-1"), idx.index("DEC-T-O-2"))


class ConflictKeyStable(T):
    @covers("stable:allow:conflict_key")
    def test_conflict_key(self):
        w0, S0 = build("plain")
        c = next(c for c in S0.conflicts if c["rule_ref"] == "⑥")
        w, S = build("ck", [dec("DEC-T-CK", "conflict_close", {"conflict_key": c["stable_key"]}, {"verdict": "both_valid", "note": "합성"})])
        c2 = [x for x in S.conflicts if x["stable_key"] == c["stable_key"]][0]
        self.assertEqual((c2["status"], c2["close_verdict"], c2["decision_id"]), ("dismissed", "both_valid", "DEC-T-CK"))
        self.assertEqual(c2["id"], c["id"])   # 결정이 CFL- 를 쓰지 않아도 같은 레코드(안정 키)
