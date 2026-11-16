# -*- coding: utf-8 -*-
"""ERD v3 §1.3·§1.4 — 참조 분해 · 시술 튜플 규칙(resolve_rules.step2/step3 · tuple_rules.procedure). 규칙마다 양성·음성."""
import unicodedata

from base import ERD, RULES, Engines, T, build, engines, mkid, norm
from registry import covers, mark
from lib.decompose import ref_anchor, tuple_id

S2 = "rule:resolve_rules.step2_decompose"
S3 = "rule:resolve_rules.step3_assemble"
TP = "rule:tuple_rules.procedure"


def spans(row):
    return [(k, v) for g in row["groups"] for m in g["members"] for k, v in m["spans"]]


class Decompose(T):
    @covers(f"{S2}.paren_regex:pos", f"{S2}.paren_regex:neg", f"{S2}.paren_rule:pos", f"{S2}.paren_rule:neg")
    def test_paren(self):
        r = engines().ref("감마원(얼굴)", "M3")
        self.assertEqual([g["where"] for g in r["groups"]], ["outer", "inner"])
        self.assertEqual(r["groups"][1]["members"][0]["text"], "얼굴")
        r2 = engines().ref("감마원 턱", "M3")
        self.assertEqual([g["where"] for g in r2["groups"]], ["outer"])

    def test_combo_symbols(self):
        E = engines()
        for sym in ERD["resolve_rules"]["step2_decompose"]["combo_symbols"]:
            r = E.ref(f"알파투{sym}베타원", None)
            self.assertEqual(r["result"], "combo_ref", sym)
            self.assertEqual(r["member_count"], 2, sym)
            mark(f"{S2}.combo_symbols[{sym}]", "test_combo_symbols")
        r = E.ref("알파투-베타원", None)  # 조합 기호가 아닌 `-` 는 나누지 않는다
        self.assertEqual(r["result"], "unresolved")
        self.assertEqual(r["unresolved_reason"], "unregistered")
        mark(f"{S2}.combo_symbols:neg", "test_combo_symbols")

    @covers(f"{S2}.combo_symbols_meaning.+:pos", f"{S2}.combo_symbols_meaning.+:neg", f"{S2}.combo_symbols_meaning.&:pos", f"{S2}.combo_symbols_meaning.&:neg",
            f"{S2}.combo_symbols_meaning.,:pos", f"{S2}.combo_symbols_meaning.,:neg", f"{S2}.combo_symbols_meaning./:pos", f"{S2}.combo_symbols_meaning./:neg",
            f"{S3}.combo.member_modes[and]", f"{S3}.combo.member_modes[or]", f"{S3}.combo.member_modes:neg", f"{TP}.member_modes[and]", f"{TP}.member_modes[or]", f"{TP}.member_modes:neg",
            "enum:R12.member_mode=and", "enum:R12.member_mode=or", "enum:reference.unresolved_reason=combo_mixed")
    def test_symbol_meaning(self):
        E = engines()
        for sym in "+&,":
            self.assertEqual(E.ref(f"알파투{sym}베타원")["member_mode"], "and", sym)
        # `/` — 대안(primary) 둘 = or · 부위 둘 = and(무엇을 하나 × 부위 여럿)
        self.assertEqual(E.ref("알파투/베타원")["member_mode"], "or")
        r = E.ref("알파톡신 턱/볼", "M1")
        self.assertEqual((r["result"], r["member_mode"]), ("multi_tuple", "and"))
        # 음성: `+` 와 `/` 가 섞이면 mixed → ⑨ combo_mixed(어느 모드도 아니다)
        r = E.ref("알파투+베타원/감마원")
        self.assertEqual((r["result"], r["unresolved_reason"]), ("unresolved", "combo_mixed"))
        self.assertNotIn(r.get("member_mode"), ("and", "or"))

    @covers(f"{S2}.secondary_split:pos", f"{S2}.secondary_split:neg", f"{S2}.secondary_rule:pos", f"{S2}.secondary_rule:neg")
    def test_secondary_split_longest_span(self):
        E = engines()
        r = E.ref("알파투 턱 주사", "M1")
        self.assertEqual(spans(r), [("product", "알파투"), ("site", "턱"), ("technique", "injection")])
        # 가장 긴 구간: 「알파원 턱 주사」 는 분류 항목 이름 하나(토큰 셋을 한 조각으로)
        r = E.ref("알파원 턱 주사 2cc", "M1")
        self.assertEqual(spans(r)[0], ("procedure", "알파원 턱 주사"))
        # 음성: 통째 일치(분류 항목 이름)는 공백으로 나누지 않는다
        r = E.ref("알파원 턱 주사", "M1")
        self.assertTrue(r["whole_match"])
        self.assertEqual(len(spans(r)), 1)

    def test_dictionary_order(self):
        R = engines().PT.R
        probe = {"product": ("알파투", "M1"), "modality_subcategory": ("주름알파", "M1"), "procedure": ("감마토닝", "M3"), "site": ("이마", None), "spec": ("2cc", None), "product_tier": ("국산", None)}
        for k in RULES["step2_decompose"]["dictionary_order"]:
            text, fam = probe[k]
            self.assertEqual(R.classify(text, fam)["kind"], k, k)
            mark(f"{S2}.dictionary_order[{k}]", "test_dictionary_order")
        self.assertIsNone(R.classify("없는말", None))
        mark(f"{S2}.dictionary_order:neg", "test_dictionary_order")

    @covers(f"{S2}.overlap_rule:pos", f"{S2}.overlap_rule:neg")
    def test_overlap(self):
        R = engines().PT.R
        # 분류 항목 이름 「알파원」 = 제품 「알파원」 → procedure(단위 시술)
        self.assertEqual(R.classify("알파원", "M1")["kind"], "procedure")
        # 하위분류 라벨 「감마투」 = 제품 「감마투」 → modality_subcategory
        self.assertEqual(R.classify("감마투", "M3")["kind"], "modality_subcategory")
        # 음성: 한쪽에만 있으면 그 사전
        self.assertEqual(R.classify("알파투", "M1")["kind"], "product")

    @covers(f"{S2}.modality_lookup:pos", f"{S2}.modality_lookup:neg")
    def test_modality_lookup(self):
        R = engines().PT.R
        c = R.classify("알파톡신", None)
        self.assertEqual((c["kind"], c["code"]), ("modality", "M1"))
        self.assertNotEqual(R.classify("알파투", None)["kind"], "modality")

    @covers(f"{S2}.spec_regex:pos", f"{S2}.spec_regex:neg", f"{S2}.spec_dictionary:pos", f"{S2}.spec_dictionary:neg", "rule:resolve_rules.step3_assemble.tuple[specs]")
    def test_spec(self):
        R = engines().PT.R
        for t in ("2cc", "4회", "1차", "3 바이알", "10단위 기준"):
            self.assertEqual(R.classify(t, None)["kind"], "spec", t)
        self.assertEqual(R.classify("KRW", None)["kind"], "spec")  # unit 사전 정준값
        self.assertIsNone(R.classify("cc2", None))
        self.assertIsNone(R.classify("원화", None))
        r = engines().ref("알파투 2cc", "M1")
        self.assertIn(("spec", "2cc"), r["qualifiers"])

    @covers(f"{S2}.scope_rule:pos", f"{S2}.scope_rule:neg")
    def test_scope(self):
        E = engines()
        # 계열 안 먼저: 「알파원 이마」 는 M1·M2 두 계열 항목 — 힌트 M2 면 M2 항목
        r = E.ref("알파원 이마", "M2")
        self.assertEqual(r["via_item"], "알파원 이마")
        self.assertEqual(r["anchor"], E.item("M2", "알파원 이마")["anchor"])
        # 계열 안에 없으면 전 계열(다른 계열의 조각) — 타 계열 표시
        c = E.PT.R.classify("알파투", "M3")
        self.assertTrue(c["cross_family"])
        # 음성: 전 계열에서 둘 이상 계열(공용원 M1|M2 · 힌트 없음) → 모호 = 미등록 조각
        r = E.ref("공용원", None)
        self.assertEqual((r["result"], r["unresolved_reason"]), ("unresolved", "unregistered"))

    @covers(f"{S2}.dictionary_order_note:pos", f"{S2}.dictionary_order_note:neg")
    def test_procedure_slot_reads_catalog_names(self):
        E = engines()
        names = {norm(n) for m in E.L["taxonomy.json"]["modality"] for sc in m["subcategories"] for n in [it["name"] for it in sc["items"]]}
        self.assertEqual(set(E.lex.idx["procedure"]), names)
        # 음성: 제조사(manufacturer)는 바깥 묶음에서 조각이 아니다(inner 에서만)
        self.assertEqual(E.ref("알파톡신 다라제약", "M1")["result"], "unresolved")


class Stopwords(T):
    def test_each_word(self):
        E = engines()
        for w in RULES["step2_decompose"]["stopwords"]["words"]:
            r = E.ref(f"알파투 {w['word']}", "M1")
            self.assertEqual(r["result"], "tuple", w["word"])
            self.assertEqual(r["qualifier_text"], [w["word"]], w["word"])
            self.assertEqual(r["unregistered"], [])
            mark(f"{S2}.stopwords.words[{w['word']}]", "test_each_word")
            self.assertTrue(w["locators"], f"{w['word']} 출처 locator 없음")
        r = E.ref("알파투 대충", "M1")  # 목록 밖 단어
        self.assertEqual((r["result"], r["unresolved_reason"]), ("unresolved", "unregistered"))
        mark(f"{S2}.stopwords.words:neg", "test_each_word")

    @covers(f"{S2}.stopwords.rule:pos", f"{S2}.stopwords.rule:neg", f"{S2}.stopwords.match:pos", f"{S2}.stopwords.match:neg", f"{TP}.stopwords:pos", f"{TP}.stopwords:neg",
            f"{S2}.stopwords.locators:pos", f"{S2}.stopwords.locators:neg")
    def test_independent_token_only(self):
        E = engines()
        r = E.ref("알파투 터치업 집중", "M1")
        self.assertEqual(r["qualifier_text"], ["터치업", "집중"])
        self.assertEqual(r["result"], "tuple")
        # 음성: 토큰 일부(진정관리의 관리)는 떼지 않는다
        r = E.ref("알파투 진정관리", "M1")
        self.assertEqual(r["unregistered"], ["진정관리"])
        # 음성: stopwords 를 끄면(V3-3 전) 같은 단어는 미등록 조각
        E0 = Engines(stopwords=False)
        r0 = E0.ref("알파투 터치업", "M1")
        self.assertEqual((r0["result"], r0["unregistered"]), ("unresolved", ["터치업"]))
        # 출처 locator 는 단어마다 ≥1, 사전 값과 겹치지 않는다
        words = {norm(w["word"]) for w in RULES["step2_decompose"]["stopwords"]["words"]}
        allv = {norm(v) for d in E.dic["dictionaries"] for e in d["entries"] for v in [e["canonical"]] + [s["value"] for s in e["synonyms"]]}
        self.assertFalse(words & allv)

    @covers(f"{S2}.stopwords.session_regex:pos", f"{S2}.stopwords.session_regex:neg", f"{S2}.stopwords.count_regex:pos", f"{S2}.stopwords.count_regex:neg",
            "rule:resolve_rules.step3_assemble.tuple[tiers]", f"{S2}.stopwords.session_rule:pos", f"{S2}.stopwords.session_rule:neg", f"{S2}.stopwords.count_target:pos",
            f"{S2}.stopwords.count_target:neg", f"{S2}.stopwords.session_target:pos", f"{S2}.stopwords.session_target:neg", "rule:resolve_rules.step3_assemble.session.rule:pos",
            "rule:resolve_rules.step3_assemble.session.rule:neg", "rule:resolve_rules.step3_assemble.session.r12[session_index]", "rule:resolve_rules.step3_assemble.session.r12[session_count]",
            "rule:resolve_rules.step3_assemble.session.r12:neg", "rule:resolve_rules.step3_assemble.session.others:pos", "rule:resolve_rules.step3_assemble.session.others:neg",
            f"{TP}.session:pos", f"{TP}.session:neg")
    def test_session_count(self):
        """V3.1-5 — R12 자리: 「N차」 → session_index · 「N회」 → session_count(첫 값만 · 나머지 qualifier_text) · R9/R17/R18·시장가 자리: qualifier_text 만."""
        from base import R12_SLOT, R9_SLOT
        from lib.decompose import MARKET_SLOT
        E = engines()
        r = E.ref("알파투 1차", "M1", slot=R12_SLOT)
        self.assertEqual((r["session_index"], r["session_count"], r["session_target"]), (1, None, "R12.session_index/session_count"))
        r = E.ref("알파투 4회", "M1", slot=R12_SLOT)
        self.assertEqual((r["session_index"], r["session_count"]), (None, 4))
        self.assertIn(("spec", "4회"), r["qualifiers"])
        self.assertEqual(r["unregistered"], [])
        r = E.ref("알파투 4회 2회", "M1", slot=R12_SLOT)        # 둘 이상이면 첫 값이 속성 · 나머지 qualifier_text(버리지 않음)
        self.assertEqual((r["session_count"], r["qualifier_text"]), (4, ["2회"]))
        # 음성(다른 자리): R9 · 시장가는 속성 자리가 없어 qualifier_text 만
        r = E.ref("알파투 4회", "M1", slot=R9_SLOT)
        self.assertEqual((r["session_count"], r["session_index"], r["qualifier_text"], r["session_target"]), (None, None, ["4회"], "qualifier_text"))
        r = E.ref("알파투 1차", "M1", slot=MARKET_SLOT)
        self.assertEqual((r["session_index"], r["qualifier_text"]), (None, ["1차"]))
        # 음성: 규격 꼴이 아니면(4회차) 회차·횟수 둘 다 아니다
        r = E.ref("알파투 4회차", "M1", slot=R12_SLOT)
        self.assertEqual((r["unregistered"], r["session_index"], r["session_count"]), (["4회차"], None, None))
        r = E.ref("알파투 국산", "M1")
        self.assertIn(("product_tier", "국산"), r["qualifiers"])

    @covers(f"{S2}.stopwords.overlap_rule:pos", f"{S2}.stopwords.overlap_rule:neg", f"{S2}.stopwords.overlap:neg",
            f"{TP}.stopword_overlap:pos", f"{TP}.stopword_overlap:neg")
    def test_overlap(self):
        """V3.1-6 — stopword 와 사전 값이 겹쳐도 통째 일치가 먼저 · stopword 는 남은 독립 토큰에만. 겹침 목록 = 값 사전 전수(문구 사전 제외)."""
        import copy
        import synth
        from lib.decompose import stopword_overlap
        dic = synth.dictionaries()
        self.assertEqual(stopword_overlap(dic, RULES), [])          # 음성: 합성 사전에는 겹침 없음
        d2 = copy.deepcopy(dic)
        next(d for d in d2["dictionaries"] if d["name"] == "modality_group")["entries"].append(synth._e("modality_group", "관리"))
        ov = stopword_overlap(d2, RULES)
        self.assertEqual([(o["word"], o["dictionaries"][0]["name"]) for o in ov], [("관리", "modality_group")])
        self.assertEqual([o["word"] for o in RULES["step2_decompose"]["stopwords"]["overlap"]], ["관리"])   # ERD 규칙 데이터와 같은 단어
        E2 = Engines(dic=d2)
        r = E2.ref("알파투 관리", "M1")                               # 분해 사전 밖 값과의 겹침 — stopword 그대로
        self.assertEqual((r["result"], r["qualifier_text"]), ("tuple", ["관리"]))
        r = E2.ref("알파원 진정관리", "M1")                            # 음성: 토큰 일부에는 적용하지 않는다
        self.assertIn("진정관리", r["unregistered"])


class CompanyParen(T):
    @covers(f"{S2}.company_paren.rule:pos", f"{S2}.company_paren.rule:neg", f"{S2}.company_paren.dictionaries[0]", f"{S2}.company_paren.dictionaries[product_name]",
            f"{S2}.company_paren.dictionaries:neg", f"{S2}.company_paren.scope:pos", f"{S2}.company_paren.scope:neg", f"{S2}.company_paren.product_of_company:pos",
            f"{S2}.company_paren.product_of_company:neg", f"{TP}.company_paren:pos", f"{TP}.company_paren:neg", f"{TP}.what[10]", "enum:reference.unresolved_reason=company_product")
    def test_company_paren(self):
        E = engines()
        alpha2 = E.ids.prod[norm("알파투")]["id"]
        r = E.ref("알파톡신(다라제약)", "M1")
        self.assertEqual((r["result"], E.tuple_of(r)["what_id"]), ("tuple", alpha2))
        self.assertEqual(r["company"], "다라제약")
        # `/` 로 이어진 복수 회사명 각각
        r = E.ref("베타필러(사아제약)", "M2")
        self.assertEqual(E.tuple_of(r)["what_id"], E.ids.prod[norm("베타원")]["id"])
        # 동의어(가나 → 가나제약)는 회사 사전 동의어
        self.assertEqual(E.PT.R.classify3("가나", "M1", "inner")["kind"], "manufacturer")
        # (b) 제품 사전 — 그 제품 · 다른 계열이면 cross_family
        r = E.ref("알파톡신(알파투)", "M1")
        self.assertEqual(E.tuple_of(r)["what_id"], alpha2)
        r = E.ref("알파톡신(베타원)", "M1")
        self.assertIn("(타 계열)", r["what_basis"])
        # 음성: 회사 제품이 둘 이상(가나제약 M1 3) · 없음(마바제약 M1 0) → ⑨ company_product
        for lab in ("알파톡신(가나제약)", "알파톡신(마바제약)"):
            r = E.ref(lab, "M1")
            self.assertEqual((r["result"], r["unresolved_reason"]), ("unresolved", "company_product"), lab)
        # 음성: 괄호 안 조각이 둘 이상이면 이 규칙이 아니다 — 회사 조각은 버리지 않고 미등록(⑨)
        r = E.ref("알파톡신(다라제약 가나제약)", "M1")
        self.assertNotEqual(r.get("company"), "다라제약")
        self.assertEqual((r["result"], r["unresolved_reason"]), ("unresolved", "unregistered"))
        self.assertEqual(sorted(r["unregistered"]), ["가나제약", "다라제약"])
        # 음성: 바깥 what 이 없으면 회사 제품을 정할 수 없다(⑨ company_product · 조각을 버리지 않는다)
        r = E.ref("이마(다라제약)", "M1")
        self.assertEqual((r["result"], r["unresolved_reason"]), ("unresolved", "company_product"))
        # 음성: 회사 사전에 없는 회사(사전 밖)는 미등록 조각
        r = E.ref("알파톡신(라마제약)", "M1")
        self.assertEqual(r["unresolved_reason"], "unregistered")


class Assemble(T):
    @covers(f"{S3}.resolved:pos", f"{S3}.resolved:neg", f"{S3}.decomposed:pos", f"{S3}.decomposed:neg", f"{S3}.unresolved:pos", f"{S3}.unresolved:neg",
            "enum:reference.status=resolved", "enum:reference.status=decomposed", "enum:reference.status=unresolved", "rule:resolve_rules.step3_assemble.tuple[family]",
            "rule:resolve_rules.step3_assemble.tuple[1]", "rule:resolve_rules.step3_assemble.tuple[sites]", "rule:resolve_rules.step3_assemble.tuple:neg")
    def test_resolve_v11(self):
        R = engines().PT.R
        r = R.resolve("알파투", "M1")
        self.assertEqual((r["status"], r["depth"]), ("resolved", "product"))
        r = R.resolve("알파투 턱", "M1")
        self.assertEqual(r["status"], "decomposed")
        self.assertEqual([s["kind"] for s in r["spans"]], ["product", "site"])
        self.assertEqual(r["family"], "M1")
        r = R.resolve("알파투 미지조각", "M1")
        self.assertEqual(r["status"], "unresolved")
        self.assertEqual([u["text"] for u in r["untouched"]], ["미지조각"])
        self.assertEqual([s["kind"] for s in r["spans"]], ["product"])  # 닿은 조각은 partial 로 기록
        # 튜플 조립 자리: 기법은 v1.1 튜플 칸이 아니다(§1.4 에서 시술 튜플 칸)
        self.assertNotIn("technique", RULES["step3_assemble"]["tuple"])

    @covers(f"{S3}.no_similarity:pos", f"{S3}.no_similarity:neg", f"{TP}.no_similarity:pos", f"{TP}.no_similarity:neg", f"{TP}.what:neg")
    def test_no_similarity(self):
        E = engines()
        for lab in ("알파투2", "알파투즈", "알파투스"):
            r = E.ref(lab, "M1")
            self.assertEqual(r["result"], "unresolved", lab)
        r = E.ref("ALPHATWO", "M1")
        self.assertEqual(r["result"], "tuple")  # 동의어 완전 일치(정규화 norm_v1: casefold · 공백 제거)
        self.assertEqual(E.ref("알파 투", "M1")["result"], "tuple")

    @covers(f"{S3}.fallback_to_parent:pos", f"{S3}.fallback_to_parent:neg", f"{S3}.fallback_to_parent_note:pos", f"{S3}.fallback_to_parent_note:neg",
            f"{TP}.fallback_to_parent:pos", f"{TP}.fallback_to_parent:neg", f"{TP}.what[8]", f"{TP}.what[9]", "enum:reference.result=none")
    def test_no_fallback_to_parent(self):
        E = engines()
        it = E.item("M1", "알파원 미지조각")
        t = E.PT.tuples[it["procedure_id"]]
        self.assertEqual((t["what_kind"], it["status"], it["candidate_name"]), ("catalog_item", "partial", ["미지조각"]))
        self.assertNotEqual(t["what_id"], E.ids.sub["M1-1"]["id"])
        r = E.ref("베타원 미지조각", "M2")
        self.assertEqual(r["result"], "unresolved")
        self.assertNotIn("procedure_id", r)
        # primary 없음: 항목은 자기 자신(complete · no_primary) · 참조는 힌트 계열 · 힌트도 없으면 튜플 없음(result none)
        it = E.item("M1", "알파톡신 이마")
        self.assertEqual((it["self_reason"], it["status"]), ("no_primary", "complete"))
        r = E.ref("이마", "M3")
        self.assertEqual(r["what_basis"], "hint_family:M3")
        self.assertEqual(E.ref("이마", None)["result"], "none")

    @covers(f"{S3}.combo.rule:pos", f"{S3}.combo.rule:neg", f"{TP}.combo:pos", f"{TP}.combo:neg", f"{TP}.combo_v22:pos", f"{TP}.combo_v22:neg",
            f"{S3}.combo.multi_site_with_symbol:pos", f"{S3}.combo.multi_site_with_symbol:neg", f"{S3}.combo.unregistered_side:pos", f"{S3}.combo.unregistered_side:neg",
            "enum:reference.result=combo_ref", "enum:reference.result=multi_tuple", "enum:reference.unresolved_reason=combo_outside_fragment", "enum:reference.unresolved_reason=multi_site")
    def test_combo(self):
        E = engines()
        r = E.ref("알파투+베타원", None)
        self.assertEqual((r["result"], r["member_count"]), ("combo_ref", 2))
        self.assertEqual(r["member_anchors"], [ref_anchor("알파투+베타원", None) + "#m0", ref_anchor("알파투+베타원", None) + "#m1"])
        # 무엇을 하나 × 부위 여럿(+ · / · 괄호 안) → 같은 what 튜플 여럿(#s<i>)
        for lab, hint in (("알파톡신 턱+볼", "M1"), ("알파톡신 턱/볼", "M1"), ("베타필러(턱+볼)", "M2")):
            r = E.ref(lab, hint)
            self.assertEqual(r["result"], "multi_tuple", lab)
            self.assertEqual(r["member_anchors"], [ref_anchor(lab, hint) + f"#s{i}" for i in range(2)])
            self.assertEqual(len({E.PT.tuples[t]["what_id"] for t in r["member_ids"]}), 1)
        # 음성: 분리 기호 없이 한 멤버 안 부위 둘 → multi_site(⑨)
        r = E.ref("알파톡신 턱 볼", "M1")
        self.assertEqual((r["result"], r["unresolved_reason"]), ("unresolved", "multi_site"))
        # 음성: 어느 쪽이 미등록이면 규칙 적용 없이 ⑨ unregistered
        r = E.ref("알파투+미지조각", None)
        self.assertEqual((r["result"], r["unresolved_reason"]), ("unresolved", "unregistered"))
        r = E.ref("알파톡신 턱+미지조각", "M1")
        self.assertEqual(r["unresolved_reason"], "unregistered")
        # v2.2: 멤버 밖 primary·site → combo_outside_fragment
        r = E.ref("알파투+베타원 이마(감마원)", None)
        self.assertEqual((r["result"], r["unresolved_reason"]), ("unresolved", "combo_outside_fragment"))
        # 음성: 멤버 밖 계열명 조각(멤버 what 의 계열)은 조합을 막지 않는다(family_fragments)
        r = E.ref("알파톡신(알파투+알파톡)", None)
        self.assertNotEqual(r.get("unresolved_reason"), "combo_outside_fragment")

    @covers(f"{S3}.combo.alternatives_in_paren:pos", f"{S3}.combo.alternatives_in_paren:neg", f"{TP}.what[11]")
    def test_alternatives_in_paren(self):
        E = engines()
        r = E.ref("알파투(알파원/알파톡)", "M1")
        self.assertEqual((r["result"], r["member_mode"]), ("tuple", "or"))
        self.assertEqual([a["text"] for a in r["alternatives"]], ["알파원", "알파톡"])
        self.assertEqual(E.tuple_of(r)["what_id"], E.ids.prod[norm("알파투")]["id"])
        # 음성: 괄호 안이 `+`(함께)면 대안이 아니다
        r = E.ref("알파투(알파원+알파톡)", "M1")
        self.assertFalse(r.get("alternatives"))


class What(T):
    @covers(f"{TP}.what[0]", f"{TP}.fold_condition:pos", f"{TP}.fold_condition:neg", f"{TP}.fold_rule:pos", f"{TP}.fold_rule:neg", f"{TP}.id:pos", f"{TP}.id:neg")
    def test_fold_and_id(self):
        E = engines()
        a = E.item("M1", "알파원 턱 주사")
        b = E.item("M1", "알파원 주사법 턱")
        self.assertEqual(a["procedure_id"], b["procedure_id"])  # 세 칸 전부 사전 값 → 접힘
        t = E.PT.tuples[a["procedure_id"]]
        self.assertTrue(t["all_dict_values"])
        self.assertEqual(t["id"], mkid("PRC", f"{t['what_id']}|{t['site_id']}|{t['technique_id']}"))
        # 음성: 미상 칸(technique none)이면 anchor 가 식별자에 들어가 항목마다 고유
        x, y = E.item("M1", "알파원 이마"), E.item("M2", "알파원 이마")
        self.assertNotEqual(x["procedure_id"], y["procedure_id"])
        tx = E.PT.tuples[x["procedure_id"]]
        self.assertEqual(tx["id"], tuple_id(tx["what_id"], tx["site_id"], tx["technique_id"], tx["what_kind"], x["anchor"])[0])
        self.assertFalse(tx["all_dict_values"])

    @covers(f"{TP}.what[1]", "enum:procedure.what_kind=product", f"{TP}.what[5]")
    def test_what_product(self):
        E = engines()
        r = E.ref("알파투 턱", "M1")
        self.assertEqual(E.tuple_of(r)["what_kind"], "product")
        # 계열 사전과 제품 색인 양쪽에 닿는 조각(알파톡) → product
        r = E.ref("알파톡", None)
        self.assertEqual(E.tuple_of(r)["what_kind"], "product")
        self.assertEqual(E.PT.R.classify("알파톡", None)["kind"], "modality")

    @covers(f"{TP}.what[2]", "enum:procedure.what_kind=catalog_item", "enum:reference.unresolved_reason=unusable_primary", f"{TP}.what[7]")
    def test_what_catalog_item(self):
        E = engines()
        r = E.ref("알파원 턱 주사 2cc", "M1")
        self.assertEqual(E.tuple_of(r)["what_kind"], "product")  # 항목 튜플의 what(사전 값)
        r = E.ref("감마토닝 볼", "M3")   # 참조: 항목 자신이 what 인 항목도 쓴다
        self.assertEqual(E.tuple_of(r)["what_kind"], "catalog_item")
        # 분류 항목: 항목 자신 what 인 항목 조각은 못 쓰는 primary
        it = E.item("M3", "감마토닝 볼")
        self.assertEqual((it["self_reason"], it["status"]), ("unusable_primary", "ambiguous"))
        # 참조: what 을 못 정하는 primary(조합 항목에 통째 일치) → ⑨ unusable_primary
        r = E.ref("알파원+베타원", "M1")
        self.assertEqual((r["result"], r["unresolved_reason"]), ("unresolved", "unusable_primary"))

    @covers(f"{TP}.what[3]", "enum:procedure.what_kind=modality_subcategory")
    def test_what_subcategory(self):
        E = engines()
        r = E.ref("주름알파 이마", "M1")
        self.assertEqual(E.tuple_of(r)["what_kind"], "modality_subcategory")
        it = E.item("M2", "주름알파 볼")  # 분류 항목에서 다른 계열 라벨
        self.assertEqual(it["self_reason"], "unusable_primary")

    @covers(f"{TP}.what[4]", "enum:procedure.what_kind=modality")
    def test_what_modality(self):
        E = engines()
        r = E.ref("알파톡신 턱", None)
        self.assertEqual(E.tuple_of(r)["what_kind"], "modality")
        r = E.ref("알파톡신 알파투", None)
        self.assertEqual(E.tuple_of(r)["what_kind"], "product")
        self.assertEqual(r["family_fragments"], ["modality:알파톡신"])
        self.assertEqual(E.item("M1", "알파톡신 이마")["self_reason"], "no_primary")  # 자기 계열명 = family_fragments
        self.assertEqual(E.item("M1", "베타필러 턱")["self_reason"], "unusable_primary")  # 다른 계열명

    @covers(f"{TP}.what[6]", "enum:reference.unresolved_reason=multi_primary")
    def test_multi_primary(self):
        E = engines()
        r = E.ref("알파투 베타원", None)
        self.assertEqual((r["result"], r["unresolved_reason"]), ("unresolved", "multi_primary"))
        self.assertEqual(E.item("M1", "알파원 베타원")["self_reason"], "multi_primary")
        # 같은 what 을 가리키는 조각은 하나로 센다
        r = E.ref("알파투 AlphaTwo", "M1")
        self.assertEqual(r["result"], "tuple")


class SiteTechnique(T):
    @covers(f"{TP}.site:pos", f"{TP}.site:neg", "enum:catalog_item.tuple_status=ambiguous", "enum:procedure.status=ambiguous", f"{TP}.extra:pos", f"{TP}.extra:neg")
    def test_site(self):
        E = engines()
        r = E.ref("알파투 턱", "M1")
        self.assertEqual(E.tuple_of(r)["site"], "턱")
        it = E.item("M1", "알파원 이마 미간")
        t = E.PT.tuples[it["procedure_id"]]
        self.assertEqual((it["status"], t["site_id"], sorted(it["extra_sites"])), ("ambiguous", "none", ["미간", "이마"]))
        self.assertEqual(t["status"], "ambiguous")
        # 참조가 항목에 닿았고 그 항목 튜플에 site 가 있으면 그 값도 센다 → 부위 둘 = multi_site
        r = E.ref("알파원 이마 턱", "M1")
        self.assertEqual((r["result"], r["unresolved_reason"]), ("unresolved", "multi_site"))
        self.assertEqual(sorted(r["detail"]), ["이마", "턱"])
        # extra: 사전 값 what 튜플이면 [] · 미해결이면 닿은 조각 전부
        ok = E.item("M1", "알파원 이마")
        self.assertEqual((ok["extra_primaries"], ok["extra_sites"]), ([], []))
        self.assertEqual(sorted(r["extra_sites"]), ["턱"])

    @covers(f"{TP}.site:pos")
    def test_multi_tuple_counts_item_site(self):
        """「무엇을 하나 × 부위 여럿」의 primary 멤버가 분류 항목(그 튜플에 site)에 닿으면 그 site 도 부위 여럿의 하나(V3-4 + §1.4 site)."""
        E = engines()
        r = E.ref("알파원 이마+미간", "M1")
        self.assertEqual((r["result"], r["sites"]), ("multi_tuple", ["이마", "미간"]))
        self.assertEqual({E.PT.tuples[t]["what_id"] for t in r["member_ids"]}, {E.ids.prod[norm("알파원")]["id"]})

    @covers("rule:tuple_rules.adverse.site_kinds:neg", f"{TP}.qualifiers:pos", f"{TP}.qualifiers:neg")
    def test_layer_not_procedure_site_and_qualifiers(self):
        E = engines()
        r = E.ref("알파투 피부", "M1")
        t = E.tuple_of(r)
        self.assertEqual((t["site_id"], r["layer_fragments"]), ("none", ["피부"]))
        # 규격·등급은 수식(참조 쪽) — 튜플 칸을 바꾸지 않는다
        a, b = E.ref("알파투 턱 주사", "M1"), E.ref("알파투 턱 주사 2cc 국산", "M1")
        self.assertEqual(a["procedure_id"], b["procedure_id"])  # 세 칸 사전 값 → 같은 튜플
        self.assertEqual(b["qualifiers"], [("spec", "2cc"), ("product_tier", "국산")])
        self.assertEqual(a["qualifiers"], [])

    @covers(f"{TP}.technique:pos", f"{TP}.technique:neg", f"{TP}.technique_inheritance:pos", f"{TP}.technique_inheritance:neg", "enum:procedure.technique_origin=fragment",
            "enum:procedure.technique_origin=none", "enum:reference.unresolved_reason=multi_technique")
    def test_technique(self):
        E = engines()
        t = E.tuple_of(E.ref("알파투 턱 주사", "M1"))
        self.assertEqual((t["technique"], t["technique_origin"]), ("injection", "fragment"))
        t = E.tuple_of(E.ref("알파투 턱", "M1"))  # M1 계열 기본 기법(injection)을 붙이지 않는다
        self.assertEqual((t["technique_id"], t["technique_origin"]), ("none", "none"))
        self.assertIn("injection", E.ids.family_tech["M1"])
        r = E.ref("알파투 열 주사", "M1")
        self.assertEqual((r["result"], r["unresolved_reason"]), ("unresolved", "multi_technique"))


class Inputs(T):
    @covers(f"{TP}.input.catalog_items:pos", f"{TP}.input.catalog_items:neg", f"{TP}.status:pos", f"{TP}.status:neg", "enum:catalog_item.tuple_status=complete",
            "enum:catalog_item.tuple_status=partial", "enum:procedure.status=complete", "enum:procedure.status=partial", f"{TP}.cat_family:pos", f"{TP}.cat_family:neg")
    def test_catalog_items(self):
        E = engines()
        items = [(m["id"], it["name"]) for m in E.L["taxonomy.json"]["modality"] for sc in m["subcategories"] for it in sc["items"]]
        self.assertEqual(sorted(E.PT.catalog), sorted(items))
        self.assertNotIn(("P1", "이마 주름"), E.PT.catalog)  # 고민 항목은 분류 항목 입력이 아니다
        st = {c["status"] for c in E.PT.catalog.values()}
        self.assertLessEqual({"complete", "partial", "ambiguous"}, st)
        self.assertEqual(E.PT.tuples[E.item("M1", "알파원 미지조각")["procedure_id"]]["status"], "partial")
        # CAT- = 트리 위치 계열 코드 + 이름 · 같은 이름 다른 계열은 다른 CAT-
        self.assertEqual(E.item("M1", "알파원 이마")["catalog_item_id"], mkid("CAT", "M1|알파원 이마"))
        self.assertNotEqual(E.item("M1", "알파원 이마")["catalog_item_id"], E.item("M2", "알파원 이마")["catalog_item_id"])

    @covers(f"{TP}.fragments:pos", f"{TP}.fragments:neg")
    def test_whole_match_first(self):
        E = engines()
        r = E.ref("알파원 HB+", "M1")  # 값 안의 조합 기호는 통째 일치면 쪼개지 않는다
        self.assertTrue(r["whole_match"])
        self.assertEqual(E.tuple_of(r)["what_label"], "알파원 HB+")
        r = E.ref("알파투+베타원", None)
        self.assertFalse(r["whole_match"])
        # 자기 이름은 분류 항목 색인에서 제외 — 항목 「알파원」 은 자기 자신이 아니라 제품 알파원
        it = E.item("M1", "알파원")
        self.assertEqual((it["what_kind"], it["self_reason"] if "self_reason" in it else None), ("product", None))

    def test_references_input(self):
        w, S = build("plain")
        rows = [r for rr in S.ctx["proc"]["ref_rows"].values() for r in rr] + S.ctx["proc"]["mk_rows"]
        labels = {r["label"] for r in rows}
        self.assertIn("알파원 이마", labels)          # 시술 종류 · market
        self.assertIn("감마원 볼", labels)
        self.assertNotIn("알파원 이마 다른이름", labels)  # pih name 은 분해 대상 아님(id 깊이)
        self.assertNotIn("이마 주름", labels)          # 고민 자리 제외
        mark(f"{TP}.input.references:pos", "test_references_input")
        mark(f"{TP}.input.references:neg", "test_references_input")


class EdgeEnds(T):
    @covers(f"{TP}.edge_end:pos", f"{TP}.edge_end:neg", f"{TP}.edge_end_kinds[procedure]", f"{TP}.edge_end_kinds[modality]", f"{TP}.edge_end_kinds[subcategory]",
            f"{TP}.edge_end_kinds[product]", f"{TP}.edge_end_kinds[unresolved]", f"{TP}.edge_end_kinds:neg", f"{TP}.code_references:pos", f"{TP}.code_references:neg",
            "enum:target_depth=modality", "enum:target_depth=subcategory", "enum:target_depth=procedure", "enum:target_depth=product", "enum:reference.result=tuple",
            "enum:reference.result=node", "enum:reference.result=unresolved", "enum:reference.unresolved_reason=unregistered")
    def test_edge_ends(self):
        w, S = build("plain")
        depth = {}
        for rel in ("R9", "R12", "R15", "R16", "R17", "R18"):
            for e in S.R.get(rel, []):
                for side in ("from", "to"):
                    if e[side]["type"] in ("procedure", "modality", "modality_subcategory", "product"):
                        d = e["attrs"].get("target_depth" if side == "to" else "from_target_depth")
                        if d:
                            depth.setdefault(d["value"], set()).add(e[side]["type"])
        self.assertEqual(depth.get("procedure"), {"procedure"})
        self.assertEqual(depth.get("modality"), {"modality"})
        self.assertEqual(depth.get("subcategory"), {"modality_subcategory"})
        self.assertEqual(depth.get("product"), {"product"})
        # catalog_item 은 끝이 아니다 · 분류 항목 id(M1-1-1) 자리는 그 항목 튜플
        for rel in ("R9", "R12", "R15", "R16", "R17", "R18"):
            self.assertFalse([e for e in S.R.get(rel, []) if "catalog_item" in (e["from"]["type"], e["to"]["type"])], rel)
        cat = mkid("CAT", "M1|알파원")
        self.assertTrue([e for e in S.R["R12"] if e["attrs"].get("target_label", {}).get("value") == "M1-1-1" and e["to"]["type"] == "procedure"])
        # 미해결 → 끝 없음(⑨ 레코드)
        unres = [c for c in S.conflicts if c["kind"] == "unresolved_reference" and c.get("label") == "베타원 미지조각"]
        self.assertTrue(unres)
        self.assertFalse([e for e in S.R["R12"] if e["attrs"].get("target_label", {}).get("value") == "베타원 미지조각"])
        # 자유 텍스트 자리의 코드(§1.4 code_references) — 「M1」→ modality · 「M1-1」→ subcategory · 「M1-1-2」→ 그 항목 튜플 · 「M1-2-3」(조합 항목)→ 멤버 튜플
        by = {e["attrs"]["target_label"]["value"]: e for e in S.R["R12"] if e["attrs"].get("month", {}).get("value") == 2}
        self.assertEqual((by["M1"]["to"]["type"], by["M1"]["attrs"]["target_depth"]["value"]), ("modality", "modality"))
        self.assertEqual(by["M1-1"]["to"]["type"], "modality_subcategory")
        self.assertEqual(by["M1-1-2"]["attrs"]["via_catalog_item"]["value"], mkid("CAT", "M1|알파원 이마"))
        self.assertEqual(len([e for e in S.R["R12"] if e["attrs"].get("target_label", {}).get("value") == "M1-2-3"]), 2)
        self.assertTrue([e for e in S.R["R18"] if e["attrs"].get("from_label", {}).get("value") == "M2" and e["from"]["type"] == "modality"])
        # 코드 참조: M 코드 아닌 값(Q8) → ⑨
        self.assertTrue([c for c in S.conflicts if c["kind"] == "unresolved_reference" and c.get("label") == "Q8"])
        self.assertTrue(cat)
