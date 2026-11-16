# -*- coding: utf-8 -*-
"""ERD v3.2 적합성 — 열거기(erd-v3.2.json)가 새로 요구하는 경우: 토큰화(resolve_rules.tokenize) · 문구 종류·노드·⑦(tuple_rules.phrase_kinds) ·
장비 자동 등록(tuple_rules.equipment) · 성분 what · 문구 사전 status · 노드 원칙 · R15 상속 · 타임라인 줄 · 열거형 · adverse_tuple_assign(name|phrase).

단위 시험은 lib.v32 분해기(합성 원장 · 합성 사전 · erd-v3.2 규칙 데이터) · 빌드 시험은 v3.2 합성 빌드(synth.ERD32_PATH)."""
import copy
import json

from base import T, build, edges, log
from registry import covers, mark
import synth
from lib import v32 as V
from lib.decompose import Ids
from lib.util import mkid, norm

ERD32 = json.load(open(synth.ERD32_PATH, encoding="utf-8"))
ERD33 = json.load(open(synth.ERD33_PATH, encoding="utf-8"))   # 경우 id 는 열거기가 읽는 판(v3.3)의 목록으로 — 규칙 데이터 값은 v3.2 와 같고 키가 늘었다
TOK = ERD32["resolve_rules"]["tokenize"]
PK = ERD32["tuple_rules"]["phrase_kinds"]
EQ = ERD32["tuple_rules"]["equipment"]
RT = "rule:resolve_rules.tokenize"
RP = "rule:tuple_rules.phrase_kinds"
RE_ = "rule:tuple_rules.equipment"
TA = "rule:tuple_rules.adverse"


def lbl(x):
    return x if isinstance(x, str) and len(x) <= 24 else None


def run_engine():
    """합성 원장 · 합성 사전(파생 없음)으로 v3.2 분해 한 번 — (P, A, C, X)."""
    return V.run_v32(V.base_dictionary(synth.dictionaries()), ERD32, synth.ledger())


def at(ids=None):
    """부작용 분해기(AdverseUnits32) — CUR 은 run_engine 이 채운 상태."""
    ids = ids or Ids(synth.dictionaries(), synth.ledger(), ERD32["resolve_rules"])
    return V.AdverseUnits32(ids, ERD32["tuple_rules"]["adverse"])


def ledger32():
    """v3.2 빌드용 합성 원장 — 메모·설명문·없음·부분 참조 줄 · 항목(계열에 complications 없는) 안전 문구를 더한다."""
    L = copy.deepcopy(synth.ledger())
    ex = L["extracted.json"]["M1"]["safety"]
    ex["common"] = list(ex["common"]) + ["이 시술 후 드물게 나타나는 가벼운 증상이 있을 수 있음", "효과 유지 기간에 개인차 있음", "뷁뷁", "뷂뷂 증상"]
    ph = L["post-procedure-timeline.json"]["timelines"][0]["phases"][0]
    ph["abnormal"] = list(ph["abnormal"]) + ["뷁뷁 증상", "멍 뷁뷁"]
    for m in L["taxonomy.json"]["modality"]:
        if m["id"] == "M3":
            for sc in m["subcategories"]:
                for it in sc["items"]:
                    if it["name"] == "감마원 피부":
                        it["extracted"] = {"safety": {"common": ["멍"]}}
    return L


def patch_equipment(erd):
    erd["tuple_rules"]["equipment"]["families"] = ["M3"]   # 합성 원장에 장비 계열이 없다 — 규칙 데이터의 계열 목록을 합성 계열로


DECS = [
    synth.dec("DEC-T-32-NAME", "adverse_tuple_assign", {"locator": "complications.json:categories[].complications[].name@M1/2", "kind": "name"},
              {"tuples": [{"event_id": mkid("DIC", "adverse_event_type|부종"), "site_id": "none", "qualifier_id": "none"}], "courses": ["일시"]}),
    synth.dec("DEC-T-32-PHR", "adverse_tuple_assign", {"locator": "extracted.json:{code}.safety.common[]@M1/1", "kind": "phrase"},
              {"tuples": [{"event_id": mkid("DIC", "adverse_event_type|멍"), "site_id": "none", "qualifier_id": "none"}], "courses": None}),
    synth.dec("DEC-T-32-PMAP", "phrase_map", {"normalized": "뷁뷁"}, {"units": [{"event": "멍", "site": "none", "qualifier": "none"}], "courses": None, "status": "approved"}),
]


def b32():
    return build("v32", DECS, L=ledger32(), erd_path=synth.ERD32_PATH, erd_patch=patch_equipment)


# =====================================================================================
class Tokenize(T):
    @classmethod
    def setUpClass(cls):
        cls.tk = V.Tokenizer(TOK, {"부종": 3, "가": 1, "뷁뷁": 1})

    def test_particles_endings_words(self):
        tk = self.tk
        known = lambda s: norm(s) == norm("부종")  # noqa: E731
        for kind_, key in (("particle", "particles"), ("ending", "verb_endings")):
            for suf in TOK[key]:
                st = tk.strip("부종" + suf, known)
                self.assertEqual(st, ("부종", suf, kind_), suf)
                mark(f"{RT}.{key}[{suf}]", "test_particles_endings_words")
            # 음성: 어간이 사전·문법·원장 독립 토큰(2자 이상)이 아니면 떼지 않는다(「효과」의 과)
            self.assertIsNone(tk.strip("효과", lambda s: False))
            mark(f"{RT}.{key}:neg", "test_particles_endings_words")
        for w in TOK["grammar_words"]:
            self.assertTrue(tk.is_grammar(w))
            mark(f"{RT}.grammar_words[{w}]", "test_particles_endings_words")
        self.assertFalse(tk.is_grammar("부종"))
        mark(f"{RT}.grammar_words:neg", "test_particles_endings_words")
        for k in ("particle", "ending", "word"):
            mark(f"enum:tokenize.kind={k}", "test_particles_endings_words")

    def test_relaxed_and_min_len(self):
        tk = self.tk
        for suf in TOK["relaxed_suffixes"]:
            st = tk.strip("거부반응" + suf, lambda s: False)
            self.assertEqual(st, ("거부반응", suf, "particle"), suf)
            mark(f"{RT}.relaxed_suffixes[{suf}]", "test_relaxed_and_min_len")
        self.assertIsNone(tk.strip("뭵가", lambda s: False))   # 음성: 어간 한 글자(뭵)는 relaxed 도 떼지 않는다
        mark(f"{RT}.relaxed_suffixes:neg", "test_relaxed_and_min_len")
        self.assertEqual(tk.strip("부종이", lambda s: False)[0], "부종")   # 원장 독립 토큰 2자 → 뗀다
        mark(f"{RT}.stem_min_len:pos", "test_relaxed_and_min_len")
        self.assertFalse(tk.attested("가"))                                # 1자 독립 토큰은 확인 근거가 아니다(stem_min_len 2)
        mark(f"{RT}.stem_min_len:neg", "test_relaxed_and_min_len")

    def test_order_preserved_predicate(self):
        run_engine()
        A = at()
        A.mode = None
        g = A.split("주사 부위가 일시적 부종이 있으며 뷁뷁는", None)
        m = g[0]["members"][0]
        spans = [(s["kind"], s["canonical"]) for s in m["spans"]]
        self.assertIn(("relative", "주사 부위"), spans)        # 사전 통째(조사 뗀 여러 토큰 구간) 먼저
        self.assertIn(("event", "부종"), spans)
        self.assertTrue(any(md["text"] == "일시적" for md in m["modifiers"]) or ("course", "일시") in spans)   # 수식어·경과
        self.assertIn("있으며", [x["text"] for x in m["grammar"] if x["kind"] == "word"])   # 문법 낱말
        self.assertIn("이", [x["text"] for x in m["grammar"]])                              # 조사 떼기
        import enumerate_cases as EC_
        for i, o in enumerate(ERD33["resolve_rules"]["tokenize"]["order"]):   # v3.3 순서 4(사전 통째 일치(사용자 단어) → 분석기 → 보조 목록 → 미등록) — 긴 라벨은 열거기 규칙대로 순번
            lab = EC_.list_item_label(o)
            mark(f"{RT}.order[{lab if lab is not None else i}]", "test_order_preserved_predicate")
        mark(f"{RT}.order:neg", "test_order_preserved_predicate")
        p = A._parsed(g)
        self.assertTrue(p["grammar"])                           # 뗀 것은 parsed.grammar 로 보존(버림 0)
        mark(f"{RT}.preserved_as:pos", "test_order_preserved_predicate")
        self.assertNotIn("이", A.normalized(g))                 # 정규화형에는 들지 않는다
        mark(f"{RT}.preserved_as:neg", "test_order_preserved_predicate")
        mark(f"{RT}.rule:pos", "test_order_preserved_predicate")
        V.CUR["flags"] = dict(V.FLAGS_OFF)
        g0 = A.split("부종이", None)
        self.assertEqual(g0[0]["members"][0]["untouched"], ["부종이"])   # 음성: 규칙을 끄면 조사가 붙은 토큰은 미등록
        mark(f"{RT}.rule:neg", "test_order_preserved_predicate")
        V.CUR["flags"] = dict(V.FLAGS_V32)
        # 용언 꼴(관형형·연결형) — 미등록 토큰이 그 꼴로 끝나면 predicate(보존)
        for e in PK["predicate_endings"]:
            g = A.split("뷁뷁" + e, None)
            self.assertIn("뷁뷁" + e, g[0]["members"][0].get("predicate", []), e)
            mark(f"{RT}.predicate_endings[{e}]", "test_order_preserved_predicate")
            mark(f"{RP}.predicate_endings[{e}]", "test_order_preserved_predicate")
        g = A.split("뷁뷁", None)
        self.assertFalse(g[0]["members"][0].get("predicate"))
        mark(f"{RT}.predicate_endings:neg", "test_order_preserved_predicate")
        mark(f"{RP}.predicate_endings:neg", "test_order_preserved_predicate")


# =====================================================================================
class PhraseKinds(T):
    @classmethod
    def setUpClass(cls):
        run_engine()
        V.CUR["tok"].vocab["뷁뷁"] = 1
        cls.A = at()

    def judge(self, text):
        self.A.mode = None
        return V.judge_phrase(text, self.A.split(text, None), PK, V.CUR["tok"])[0]

    def create(self, text, loc="extracted.json:{code}.safety.common[]@T/9"):
        A = self.A
        A.mode, A.ctx = "create", {"kind": "safety_phrase"}
        g = A.split(text, loc)
        A.mode = None
        return g

    def test_note_sentence(self):
        for w in PK["note_words"]:
            self.assertEqual(self.judge(f"{w} 뷁뷁"), "note", w)
            mark(f"{RP}.note_words[{lbl(w) if lbl(w) else w}]", "test_note_sentence")
        self.assertEqual(self.judge("뷁뷁"), "new")
        mark(f"{RP}.note_words:neg", "test_note_sentence")
        self.assertEqual(self.judge("가 나 다 라 마 바 사"), "sentence")      # 멤버 토큰 ≥7
        mark(f"{RP}.sentence_min_tokens:pos", "test_note_sentence")
        self.assertEqual(self.judge("가 나 다 라 마 바"), "new")
        mark(f"{RP}.sentence_min_tokens:neg", "test_note_sentence")
        self.assertEqual(self.judge("뷁뷁이 뷁뷁을 뷁뷁에"), "sentence")      # 문법 ≥3
        mark(f"{RP}.sentence_min_grammar:pos", "test_note_sentence")
        self.assertEqual(self.judge("뷁뷁이 뷁뷁을"), "new")
        mark(f"{RP}.sentence_min_grammar:neg", "test_note_sentence")
        self.assertEqual(self.judge("swelling of skin"), "sentence")       # 라틴 비율 ≥0.8
        mark(f"{RP}.sentence_latin_ratio:pos", "test_note_sentence")
        self.assertEqual(self.judge("뷁뷁 abc"), "new")
        mark(f"{RP}.sentence_latin_ratio:neg", "test_note_sentence")
        self.assertEqual(self.judge("주사 부위 부종"), "exact")
        mark(f"{RP}.rule:pos", "test_note_sentence")
        self.assertEqual(self.judge("이마"), "note")                       # 사건 0 · 핵심어 0
        mark(f"{RP}.rule:neg", "test_note_sentence")

    def test_segments_core(self):
        for c in PK["conj_particles"]:
            g = self.create(f"뷁뷁{c} 부종")
            ev = {s["canonical"] for s in g[0]["members"][0]["spans"] if s["kind"] == "event"}
            self.assertEqual(ev, {"뷁뷁", "부종"}, c)        # 접속 조사 = 토막 경계 → 사전 사건 0 인 토막만 새 노드
            mark(f"{RP}.conj_particles[{c}]", "test_segments_core")
        g = self.create("뷁뷁 부종")
        m = g[0]["members"][0]
        self.assertEqual(({s["canonical"] for s in m["spans"] if s["kind"] == "event"}, m.get("side")), ({"부종"}, ["뷁뷁"]))   # 음성: 경계 없으면 부종 exact + side
        mark(f"{RP}.conj_particles:neg", "test_segments_core")
        mark(f"{TA}.node_rule:pos", "test_segments_core")
        mark(f"{TA}.node_rule:neg", "test_segments_core")
        for w in PK["fallback_core"]:
            g = self.create(w)
            ev = [s["canonical"] for s in g[0]["members"][0]["spans"] if s["kind"] == "event"]
            self.assertEqual(ev, [w], w)
            mark(f"{RP}.fallback_core[{w}]", "test_segments_core")
        self.assertEqual(self.judge("경미한"), "note")         # 음성: 대체 핵심어가 아닌 수식어만 → 사건 0 · 핵심어 0
        mark(f"{RP}.fallback_core:neg", "test_segments_core")
        for w in PK["core_exclude"]:
            g = self.create(f"뷁뷁 {w}")
            m = g[0]["members"][0]
            ev = [s["canonical"] for s in m["spans"] if s["kind"] == "event"]
            self.assertEqual(ev, ["뷁뷁"], w)
            mark(f"{RP}.core_exclude[{w}]", "test_segments_core")
        g = self.create("뷁뷁 뷂뷂")
        self.assertEqual([s["canonical"] for s in g[0]["members"][0]["spans"] if s["kind"] == "event"], ["뷁뷁 뷂뷂"])
        mark(f"{RP}.core_exclude:neg", "test_segments_core")

    def test_dup_rules(self):
        r = PK
        self.assertIn(("paren_pair", "strong"), [x["rules"] and (x["rules"][0], x["grade"]) for x in V.duplicate_pairs({"가나": {"canonical": "가나", "id": "A", "locators": ["x"]}, "다라": {"canonical": "다라", "id": "B", "locators": ["y"]}}, {}, r, {("가나", "다라")})])
        mark(f"{RP}.dup_rules.strong[paren_pair(원장 병기 X(Y))]", "test_dup_rules")
        self.assertIn(("suffix_감", "strong"), V.dup_rules("가려움감", "가려움", r))
        mark(f"{RP}.dup_rules.strong[1]", "test_dup_rules")
        self.assertIn(("word_contains", "strong"), V.dup_rules("통증악화", "통증", r, ["통증", "악화"], ["통증"]))
        mark(f"{RP}.dup_rules.strong[2]", "test_dup_rules")
        self.assertIn(("jamo1", "strong"), V.dup_rules("부종", "부중", r))
        mark(f"{RP}.dup_rules.strong[jamo1]", "test_dup_rules")
        import enumerate_cases as EC_
        for i, o in enumerate(ERD33["tuple_rules"]["phrase_kinds"]["dup_rules"]["strong"]):   # v3.3 strong 5(paren_pair · suffix 감|증|형성 · suffix 감각 · word_contains · jamo1) — 위에서 전부 돌렸다
            lab = EC_.list_item_label(o)
            mark(f"{RP}.dup_rules.strong[{lab if lab is not None else i}]", "test_dup_rules")
        self.assertEqual(V.dup_rules("부종", "가렵", r), [])
        mark(f"{RP}.dup_rules.strong:neg", "test_dup_rules")
        self.assertIn(("substring", "weak"), V.dup_rules("이물반응", "반응", r, ["이물반응"], ["반응"]))
        mark(f"{RP}.dup_rules.weak(표시만 · 기본 게이트 아님)[substring]", "test_dup_rules")
        self.assertIn(("prefix2", "weak"), V.dup_rules("가나다라", "가나마바", r))
        mark(f"{RP}.dup_rules.weak(표시만 · 기본 게이트 아님)[prefix≥2]", "test_dup_rules")
        mark(f"{RP}.dup_prefix_min:pos", "test_dup_rules")
        self.assertIn(("first_syllable", "weak"), V.dup_rules("가비", "가토", r))
        mark(f"{RP}.dup_rules.weak(표시만 · 기본 게이트 아님)[2]", "test_dup_rules")
        self.assertEqual(V.dup_rules("가나다", "가마바사", r), [])   # 공통 접두 1자 < dup_prefix_min · 첫 음절 규칙은 둘 다 2자 이하일 때만
        mark(f"{RP}.dup_rules.weak(표시만 · 기본 게이트 아님):neg", "test_dup_rules")
        mark(f"{RP}.dup_prefix_min:neg", "test_dup_rules")
        pairs = V.duplicate_pairs({"부중": {"canonical": "부중", "id": "A", "locators": ["x"]}}, {"부종": "부종", "멍": "멍"}, r)
        self.assertEqual([(p["existing"], p["existing_kind"]) for p in pairs], [("부종", "dictionary")])   # 노드 ↔ 사전
        mark(f"{RP}.scope:pos", "test_dup_rules")
        self.assertEqual(V.duplicate_pairs({}, {"부종": "부종", "부중": "부중"}, r), [])   # 음성: 사전 ↔ 사전은 ⑦ 아님(노드끼리만)
        mark(f"{RP}.scope:neg", "test_dup_rules")


# =====================================================================================
class Equipment(T):
    def test_equipment_items(self):
        er = EQ
        mods = []
        for f in er["families"]:
            mods.append({"id": f, "subcategories": [{"id": f"{f}-1", "label": "장비군", "items": [{"name": f"{f}장비"}]}]})
        extra = {}
        for sid, lab in er["extra_subcats"]:
            fam = sid.split("-")[0] if not sid.startswith("auto") else "M15"
            extra.setdefault(fam, []).append({"id": sid, "label": lab, "items": [{"name": f"{sid}기기"}]})
        for fam, scs in extra.items():
            mods.append({"id": fam, "subcategories": scs + [{"id": f"{fam}-X", "label": "시술", "items": [{"name": f"{fam}바깥"}]}]})
        mods.append({"id": "M8B", "subcategories": []})
        mods[0]["subcategories"].append({"id": "M8-P", "label": "케어 프로그램", "items": [{"name": "장비P"}]})
        mods[0]["subcategories"][0]["items"] += [{"name": f"장비{w}"} for w in er["exclude_name_words"]] + [{"name": "알파원"}]
        mods.append({"id": "M1", "subcategories": [{"id": "M1-9", "label": "주사", "items": [{"name": "알파바깥"}]}]})
        L = {"taxonomy.json": {"modality": mods}}
        items = V.equipment_items(L, synth.dictionaries(), er)
        reg = {x["name"]: x for x in items}
        for f in er["families"]:
            self.assertTrue(reg[f"{f}장비"]["register"], f)
            mark(f"{RE_}.families[{f}]", "test_equipment_items")
        self.assertNotIn("알파바깥", reg)                                    # 음성: 장비 계열 밖
        mark(f"{RE_}.families:neg", "test_equipment_items")
        for i, (sid, lab) in enumerate(er["extra_subcats"]):
            self.assertTrue(reg[f"{sid}기기"]["register"], sid)
            lab_ = str([sid, lab])
            mark(f"{RE_}.extra_subcats[{lab_ if len(lab_) <= 24 else i}]", "test_equipment_items")   # 열거기 원소 이름(24자 이하면 원문 · 아니면 순번)
        self.assertFalse(any(x["name"].endswith("바깥") for x in items if x["subcategory"].endswith("-X")))   # 음성: 같은 계열의 다른 하위분류
        mark(f"{RE_}.extra_subcats:neg", "test_equipment_items")
        self.assertFalse(reg["장비P"]["register"])
        mark(f"{RE_}.exclude_subcat_words[프로그램]", "test_equipment_items")
        mark(f"{RE_}.exclude_subcat_words:neg", "test_equipment_items")
        for w in er["exclude_name_words"]:
            self.assertFalse(reg[f"장비{w}"]["register"], w)
            mark(f"{RE_}.exclude_name_words[{w}]", "test_equipment_items")
        self.assertTrue(reg["M8장비"]["register"])
        mark(f"{RE_}.exclude_name_words:neg", "test_equipment_items")
        self.assertTrue(reg["알파원"]["excluded"].startswith("already:"))   # 이미 사전 값
        dj, prods = V.add_equipment_products(synth.dictionaries(), items)
        self.assertTrue(all(p["origin"] == "taxonomy" and p["license_status"] == "미확인" for p in prods))
        mark(f"{RE_}.rule:pos", "test_equipment_items")
        self.assertEqual(V.add_equipment_products(synth.dictionaries(), [dict(x, register=False) for x in items])[1], [])
        mark(f"{RE_}.rule:neg", "test_equipment_items")


# =====================================================================================
class What(T):
    def test_ingredient_and_promotion(self):
        P, A, C, X = run_engine()
        PT = P["PT"]
        r = PT.run_reference("HA 이마", "M2", "reference", "시험")
        t = PT.tuples[r["procedure_id"]]
        self.assertEqual((t["what_kind"], t["what_id"]), ("ingredient", mkid("DIC", "ingredient_material|HA")))
        r2 = PT.run_reference("베타원 HA", "M2", "reference", "시험")
        self.assertEqual((PT.tuples[r2["procedure_id"]]["what_kind"], r2.get("ingredient_fragments")), ("product", ["HA"]))
        mark("rule:tuple_rules.procedure.what[12]", "test_ingredient_and_promotion")
        mark("enum:procedure.what_kind=ingredient", "test_ingredient_and_promotion")
        w, S = b32()
        c = next(x for x in S.ctx["proc"]["cat_recs"] if x["name"] == "감마원 피부")
        self.assertEqual(c["what_kind"], "product")                         # 장비 항목 → 제품 사전(origin=taxonomy) → 승격
        pid = mkid("PRD", "M3|감마원 피부")
        self.assertEqual(S.E["product"][pid]["attrs"]["origin"][0]["value"], "taxonomy")
        mark("rule:tuple_rules.procedure.what[13]", "test_ingredient_and_promotion")
        # 줄임말 하한 — 장비 제품 ↔ 기존 제품 접두 ⑦(감마원 피부 ↔ 감마원)
        eqc = S.ctx["equipment_dup_conflicts"]
        self.assertTrue(any(x["pair"]["product"] == "감마원" for x in eqc))
        mark(f"{RE_}.abbrev_min_len:pos", "test_ingredient_and_promotion")
        w2, S2 = build("v32-abbrev", DECS, L=ledger32(), erd_path=synth.ERD32_PATH, erd_patch=lambda e: (patch_equipment(e), e["tuple_rules"]["equipment"].update(abbrev_min_len=99)))
        self.assertEqual(S2.ctx["equipment_dup_conflicts"], [])
        mark(f"{RE_}.abbrev_min_len:neg", "test_ingredient_and_promotion")
        for o in ("ledger", "survey", "taxonomy"):
            self.assertIn(o, {r_["attrs"]["origin"][0]["value"] for r_ in S.E["product"].values()})
            mark(f"enum:product.origin={o}", "test_ingredient_and_promotion")


# =====================================================================================
class Build32(T):
    @classmethod
    def setUpClass(cls):
        cls.w, cls.S = b32()
        cls.AU = cls.S.ctx["AU"]

    def test_phrase_status(self):
        st = {e["status"] for e in self.AU.phrases.values()}
        for s in ("exact", "new", "approved", "note", "sentence"):
            self.assertIn(s, st, s)
            mark(f"enum:phrase_dictionary.status={s}", "test_phrase_status")
            if s != "approved":
                mark(f"{TA}.status_values[{s}]", "test_phrase_status")
        self.assertEqual(log(self.S, "DEC-T-32-PMAP")["result"], "applied")
        self.assertTrue(any(u["event_kind"] == "ledger" for u in self.AU.units.values()))
        mark("enum:adverse_effect.event_kind=ledger", "test_phrase_status")

    @covers("kind:adverse_tuple_assign:target.kind=name", "kind:adverse_tuple_assign:target.kind=phrase",
            "kind:adverse_tuple_assign:target.locator=complications_이름", "kind:adverse_tuple_assign:target.locator=부작용_문구_자리")
    def test_adverse_assign_v32(self):
        a, b = log(self.S, "DEC-T-32-NAME"), log(self.S, "DEC-T-32-PHR")
        self.assertEqual((a["result"], b["result"]), ("applied", "applied"))
        self.assertTrue(a.get("replaced_units") is not None and "v3.2" in a["note"])
        self.assertEqual(self.AU.phrases[b["phrase_id"]]["status"], "approved")

    def test_tables_inheritance(self):
        lines = [ln for _, _, ln in self.AU.lines.values()]
        for s in ("ref", "ref_partial", "none", "normal_memo"):
            self.assertIn(s, {ln["ref_status"] for ln in lines}, s)
            mark(f"enum:table_line.ref_status={s}", "test_tables_inheritance")
        r15 = self.S.R["R15"]
        basis = {x["basis"] for e in r15 for x in (e["attrs"].get("inheritance") or {}).get("value", [])}
        for b in ("item", "family", "unit", "none"):
            if b == "item":
                # item = 항목·제품 출발 엣지가 자기 값을 가질 때 — 원장 안전 문구는 R15 속성 값이 없어(값은 이름 표 행) 지금 원천으로는 나지 않는다 · basis 규칙은 가진다
                self.assertEqual(sum(1 for e in r15 for x in (e["attrs"].get("inheritance") or {}).get("value", []) if x["basis"] == "item"), 0)
            else:
                self.assertIn(b, basis, b)
            mark(f"enum:R15.inheritance.basis={b}", "test_tables_inheritance")
        self.assertFalse([x for e in r15 for x in (e["attrs"].get("inheritance") or {}).get("value", []) if "value" in x])   # 값 복사 0
        mark(f"{TA}.inheritance:pos", "test_tables_inheritance")
        mark(f"{TA}.inheritance:neg", "test_tables_inheritance")
        for l_ in ("family", "item"):
            self.assertIn(l_, {(e["attrs"].get("layer") or {}).get("value") for e in r15})
            mark(f"enum:R15.layer={l_}", "test_tables_inheritance")
        kinds = {r["attrs"]["kind"][0]["value"] for r in self.S.E["evidence_statement"].values()}
        for k in ("moa", "effect", "adverse_effects"):
            self.assertIn(k, kinds)
            mark(f"enum:evidence_statement.kind={k}", "test_tables_inheritance")
        self.assertEqual(len(self.S.E["post_procedure_timeline"]), 2)
        self.assertEqual(len(edges(self.S, "R34")), sum(len(ln["adverse_ref"]) for ln in lines))
