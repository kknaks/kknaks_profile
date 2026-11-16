# -*- coding: utf-8 -*-
"""ERD v3.1 §1.5 — 부작용 단위·문구 규칙(tuple_rules.adverse · 원칙 A~D · V3-1 수식 칸 · V3-5 조직층 · V3.1-8 수식어 · V3.1-9 단위 세 칸·경과 엣지 · V3.1-10 문구 사전).
규칙마다 양성·음성. 단위 = (사건, 부위, 물질) · 경과는 R15 엣지 속성 · 상대 부위는 none · 문구는 개체가 아니라 문구 사전 항목."""
from base import ERD, Engines, T, build, engines, mkid, norm
from registry import covers, mark
import enumerate_cases as EC

TA = "rule:tuple_rules.adverse"
ADV = ERD["tuple_rules"]["adverse"]
SW = ADV["adverse_stopwords"]


def units(E, row):
    """이름 행 → [(event, site, qualifier)] (세 칸)."""
    return sorted((E.AT.tuples[u]["event"], E.AT.tuples[u]["site"], E.AT.tuples[u]["qualifier"]) for u in row["unit_ids"])


def courses(row, event):
    return sorted({co for c in row["candidates"] if c["event"] == event for co in c["courses"]})


def uid3(E, event, site=None, qualifier=None):
    ev = E.ids.event[norm(event)]["id"]
    sid = E.ids.site[norm(site)]["id"] if site else "none"
    qid = E.ids.qualifier[norm(qualifier)]["id"] if qualifier else "none"
    return mkid("ADV", f"{ev}|{sid}|{qid}")


class Split(T):
    @covers(f"{TA}.split:pos", f"{TA}.split:neg", f"{TA}.tuple:pos", f"{TA}.tuple:neg", f"{TA}.principles:pos", f"{TA}.principles:neg", f"{TA}.unit:pos", f"{TA}.unit:neg")
    def test_members_and_one_unit_per_event(self):
        E = Engines()
        # 멤버 구분 `· / , + 및 또는 — -- :` — 멤버마다 사건 하나 = 단위 하나(세 칸)
        for sep in ("·", "/", ",", "+", " 및 ", " 또는 ", "—", "--", ":"):
            r = E.name(f"멍{sep}부종", locator=f"complications.json:categories[].complications[].name@S/{sep}")
            self.assertEqual(units(E, r), [("멍", None, None), ("부종", None, None)], sep)
        # 음성: 구분 기호가 아닌 `-` 는 멤버를 나누지 않는다(한 토큰 → 미등록 · raw_name)
        r = E.name("멍-부종")
        self.assertEqual((r["event_kind"], r["unregistered"]), ("raw_name", ["멍-부종"]))
        # 원칙 B: 한 멤버에 사건 둘이면 단위 둘
        self.assertEqual(len(E.name("멍 부종", locator="c:p@S/b")["unit_ids"]), 2)
        # 단위 식별자 = 세 칸(사건 · 부위 · 물질) — 경과·상대 부위는 칸이 아니다
        u = E.AT.tuples[E.name("부종", locator="c:p@S/u")["unit_ids"][0]]
        self.assertEqual(u["id"], uid3(E, "부종"))
        self.assertNotIn("course", u)

    @covers(f"{TA}.course:pos", f"{TA}.course:neg", f"{TA}.course_is_edge_attribute:pos", f"{TA}.course_is_edge_attribute:neg")
    def test_course_member_only_and_edge_attribute(self):
        E = Engines()
        # 경과는 사건이 놓인 멤버의 수식어만 — 단위는 하나(경과가 칸이 아니다) · 경과는 그 단위 후보의 courses(R15 엣지 속성)
        r = E.name("멍 · 지연성 통증", locator="c:p@C/0")
        self.assertEqual(units(E, r), [("멍", None, None), ("통증", None, None)])
        self.assertEqual((courses(r, "통증"), courses(r, "멍")), (["지연"], []))
        a, b = E.name("일시적 멍", locator="c:p@C/1"), E.name("멍", locator="c:p@C/2")
        self.assertEqual(a["unit_ids"], b["unit_ids"])          # 경과가 달라도 같은 단위
        self.assertEqual(courses(a, "멍"), ["일시"])
        # 음성: 멤버 밖 경과는 가져오지 않는다 — 사건 없는 멤버의 경과는 붙지 않은 조각(raw_name)
        r = E.name("부종 · 일시적", locator="c:p@C/3")
        self.assertEqual((r["event_kind"], r["extra_courses"]), ("raw_name", ["일시"]))
        # 음성(엣지 속성): 단위 레코드에 경과 칸이 없다
        self.assertFalse(any("course" in t or "course_id" in t for t in E.AT.tuples.values()))

    @covers(f"{TA}.site:pos", f"{TA}.site:neg", f"{TA}.site_member_only:pos", f"{TA}.site_member_only:neg", "enum:adverse_effect.site_basis=member",
            "enum:adverse_effect.site_basis=site_list", "enum:adverse_effect.site_ref_kind=site", "enum:adverse_effect.site_ref_kind=none",
            f"{TA}.relative_site_is_none:pos", f"{TA}.relative_site_is_none:neg")
    def test_site_rules(self):
        E = Engines()
        # 상대 부위(주사 부위)는 칸이 아니라 none · relative_site_text 보존
        r = E.name("주사 부위 부종", locator="c:p@R/0")
        u = E.AT.tuples[r["unit_ids"][0]]
        self.assertEqual((u["site_id"], u["site_kind"], u["relative_site_text"]), ("none", "none", ["주사 부위"]))
        self.assertEqual(u["id"], uid3(E, "부종"))
        # 음성(상대 부위 none): 절대 부위(이마)는 칸이다
        r2 = E.name("이마 부종", locator="c:p@R/1")
        u2 = E.AT.tuples[r2["unit_ids"][0]]
        self.assertEqual((u2["site"], u2["site_kind"], u2["site_basis"]), ("이마", "site", "member"))
        # 부위 나열(바로 앞 멤버) → 부위마다 단위(원칙 B) · site_list
        r = E.name("이마/미간 통증", locator="c:p@R/2")
        self.assertEqual(units(E, r), [("통증", "미간", None), ("통증", "이마", None)])
        self.assertEqual({E.AT.tuples[x]["site"]: E.AT.tuples[x]["site_basis"] for x in r["unit_ids"]}, {"이마": "site_list", "미간": "member"})
        # 음성: 바깥 부위는 괄호 안 사건에 붙지 않는다(멤버 밖)
        r = E.name("괴사 (이마)", locator="c:p@R/3")
        self.assertEqual((r["event_kind"], r["extra_sites"]), ("raw_name", ["이마"]))
        r = E.name("주사 부위 반응 (부종)", locator="c:p@R/4")
        self.assertEqual(r["event_kind"], "raw_name")

    def test_site_kinds_and_layers(self):
        E = Engines()
        kinds = {E.ids.site_kind[norm(e["canonical"])] for e in next(d for d in E.dic["dictionaries"] if d["name"] == "site")["entries"]}
        for layer in ADV["site_layers"]:
            r = E.name(f"{layer} 괴사", locator=f"c:p@L/{layer}")
            self.assertEqual(r["event_kind"], "dict", layer)
            u = E.AT.tuples[r["unit_ids"][0]]
            self.assertEqual((u["site"], u["site_dict_kind"]), (layer, "layer"), layer)
            mark(f"{TA}.site_layers[{layer}]", "test_site_kinds_and_layers")
        mark(f"{TA}.site_layers:neg", "test_site_kinds_and_layers")
        self.assertEqual(E.ids.site_kind[norm("이마")], "anatomical")  # 조직층 아닌 부위는 layer 가 아니다
        for k in ("anatomical", "layer", "region"):
            self.assertIn(k, kinds)
        # relative — 상대 부위 사전 값(사건 축) · v3.1: 칸에 오지 않는다
        self.assertIn(norm("주사 부위"), E.ids.rsite_surface)
        for k in ADV["site_kinds"]:
            mark(f"{TA}.site_kinds[{k}]", "test_site_kinds_and_layers")
        for k in ERD["enums"]["site.kind"]:
            mark(f"enum:site.kind={k}", "test_site_kinds_and_layers")

    @covers(f"{TA}.qualifier:pos", f"{TA}.qualifier:neg", f"{TA}.qualifier_none_is_value:pos", f"{TA}.qualifier_none_is_value:neg", "enum:adverse_effect.qualifier_basis=member",
            "enum:adverse_effect.qualifier_basis=prefix_split", f"{TA}.qualifier_values:neg")
    def test_qualifier(self):
        E = Engines()
        a = E.name("공기색전", locator="c:p@Q/1")
        b = E.name("색전", locator="c:p@Q/2")
        ua, ub = E.AT.tuples[a["unit_ids"][0]], E.AT.tuples[b["unit_ids"][0]]
        self.assertEqual((ua["event"], ua["qualifier"], ua["qualifier_basis"]), ("색전", "공기", "prefix_split"))
        self.assertEqual((ub["qualifier"], ub["qualifier_id"]), (None, "none"))
        self.assertNotEqual(ua["id"], ub["id"])  # (색전, none, 공기) ≠ (색전, none, none)
        self.assertEqual(ub["id"], uid3(E, "색전"))
        c = E.name("혈전 색전", locator="c:p@Q/3")
        self.assertEqual((E.AT.tuples[c["unit_ids"][0]]["qualifier"], E.AT.tuples[c["unit_ids"][0]]["qualifier_basis"]), ("혈전", "member"))
        d = E.name("공기 혈전 색전", locator="c:p@Q/4")
        self.assertEqual(sorted(x[2] for x in units(E, d)), ["공기", "혈전"])   # 수식 후보 둘 → 수식마다(원칙 B)
        e = E.name("부종 · 공기", locator="c:p@Q/5")
        self.assertEqual((e["event_kind"], e["extra_qualifiers"]), ("raw_name", ["공기"]))
        f = E.name("공기색전증", locator="c:p@Q/6")
        self.assertEqual(f["unregistered"], ["공기색전증"])

    def test_qualifier_values(self):
        E = Engines()
        for q in ADV["qualifier_values"]:
            r = E.name(f"{q}색전", locator=f"c:p@V/{q}")
            u = E.AT.tuples[r["unit_ids"][0]]
            self.assertEqual((u["event"], u["qualifier"]), ("색전", q), q)
            mark(f"{TA}.qualifier_values[{q}]", "test_qualifier_values")

    @covers(f"{TA}.raw_name_cells:pos", f"{TA}.raw_name_cells:neg", "enum:adverse_effect.event_kind=dict", "enum:adverse_effect.status=complete",
            f"{TA}.status:pos", f"{TA}.status:neg", f"{TA}.id:pos", f"{TA}.id:neg")
    def test_raw_name(self):
        E = Engines()
        loc = "complications.json:categories[].complications[].name@M1/8"
        r = E.name("미지증상 지연성 통증", locator=loc)
        u = E.AT.tuples[r["unit_ids"][0]]
        self.assertEqual((u["event_kind"], u["status"], u["raw_reason"], u["site_id"], u["qualifier_id"]), ("raw_name", "partial", "unregistered", "none", "none"))
        self.assertEqual(u["dict_tuples"], [("통증", None, "지연", None)])  # 사전 분해는 보존만(경과는 엣지의 재료)
        self.assertEqual(u["id"], mkid("ADV", f"RAW:{loc}|none|none|{loc}"))
        r2 = E.name("괴사 (이마)", locator="c:p@M1/9")
        self.assertEqual((E.AT.tuples[r2["unit_ids"][0]]["status"], E.AT.tuples[r2["unit_ids"][0]]["raw_reason"]), ("unresolved", "unattached_fragments"))
        r3 = E.name("미지증상 괴사 (이마)", locator="c:p@M1/10")
        self.assertEqual(E.AT.tuples[r3["unit_ids"][0]]["raw_reason"], "unregistered+unattached_fragments")
        r4 = E.name("미지증상 지연성 통증", locator="c:p@M2/0")
        self.assertNotEqual(r4["unit_ids"], r["unit_ids"])    # 같은 이름이라도 locator 가 다르면 다른 raw 단위
        a, b = E.name("멍", locator="c:p@A/0"), E.name("멍 (타박상)", locator="c:p@A/1")
        self.assertEqual(a["unit_ids"], b["unit_ids"])        # 음성: 전부 사전 값이면 dict 단위(complete) — 같은 세 칸이면 접힌다
        self.assertEqual(E.AT.tuples[a["unit_ids"][0]]["status"], "complete")

    @covers(f"{TA}.fold_condition:pos", f"{TA}.fold_condition:neg", f"{TA}.fold_rule:pos", f"{TA}.fold_rule:neg", f"{TA}.no_similarity:pos", f"{TA}.no_similarity:neg")
    def test_fold(self):
        E = Engines()
        a = E.name("멍 · 타박상", locator="c:p@F/0")  # 동의어 = 같은 사건 → 한 단위
        self.assertEqual(len(set(a["unit_ids"])), 1)
        self.assertEqual(set(a["unit_ids"]), set(E.name("멍", locator="c:p@F/1")["unit_ids"]))
        # 상대 부위·경과가 달라도 같은 단위(세 칸 같음)
        self.assertEqual(set(E.name("주사 부위 부종", locator="c:p@F/4")["unit_ids"]), set(E.name("일시적 부종", locator="c:p@F/5")["unit_ids"]))
        c = E.name("멍듦", locator="c:p@F/2")   # 음성: 비슷한 표기(유사도)는 접지 않는다
        self.assertEqual(c["event_kind"], "raw_name")
        self.assertNotEqual(set(E.name("공기색전", locator="c:p@F/3")["unit_ids"]), set(E.name("색전", locator="c:p@F/6")["unit_ids"]))   # 음성: 물질 칸이 다르면 다른 단위


class Modifiers(T):
    """V3.1-8 안전 문구 수식어 목록·패턴 — 미등록 조각이 아니라 parsed · 정규화형에서 빠진다."""

    @covers(f"{TA}.adverse_stopwords.rule:pos", f"{TA}.adverse_stopwords.rule:neg", f"{TA}.adverse_stopwords.words:neg", f"{TA}.adverse_stopwords.classes:neg")
    def test_words(self):
        E = engines()
        base = E.phrase("부종")
        for w in SW["words"]:
            r = E.phrase(f"부종 {w['word']}", locator=f"x:y@W/{w['word']}")
            self.assertIn(w["word"], r["parsed"][w["class"]], w["word"])
            self.assertEqual((r["normalized"], r["status"]), (base["normalized"], "auto"), w["word"])
            mark(f"{TA}.adverse_stopwords.words[{w['word']}]", "test_words")
            mark(f"{TA}.adverse_stopwords.classes[{w['class']}]", "test_words")
        # 음성: 토큰 일부(붙여 쓴 「경미한부종」)에는 적용하지 않는다(완전 일치만) · 목록 밖 단어는 미등록
        r = E.phrase("경미한부종", locator="x:y@W/neg")
        self.assertEqual((r["status"], r["unregistered"]), ("unlinked", ["경미한부종"]))
        self.assertEqual(E.phrase("부종 뚜렷한", locator="x:y@W/neg2")["unregistered"], ["뚜렷한"])
        self.assertEqual(set(SW["classes"]), {"degree", "timing", "incidence", "condition", "connector", "misc"})

    @covers(f"{TA}.adverse_stopwords.patterns:neg")
    def test_patterns(self):
        E = engines()
        samples = {r"^\d+(?:[.,]\d+)?(?:[-~]\d+(?:[.,]\d+)?)?%$": "10%", r"^\d[\d,]*명$": "455명", r"^\d+[-~]\d+$": "1-3", r"^\d+(?:[.,]\d+)?(?:mL|ml|cc|mm|cm|도|U|단위)(?:로도|이상|이하|로)?$": "0.04mL로도"}
        for p in SW["patterns"]:
            tok = samples.get(p["regex"], "3일")
            r = E.phrase(f"부종 {tok}", locator=f"x:y@P/{tok}")
            self.assertIn(tok, r["parsed"][p["class"]], p["regex"])
            self.assertEqual(r["status"], "auto", p["regex"])
            mark(f"{TA}.adverse_stopwords.patterns[{EC.list_item_label(p)}]", "test_patterns")
        self.assertEqual(E.phrase("부종 10퍼센트", locator="x:y@P/neg")["unregistered"], ["10퍼센트"])   # 음성: 패턴 밖은 미등록

    @covers(f"{TA}.adverse_stopwords.threshold:pos", f"{TA}.adverse_stopwords.threshold:neg", f"{TA}.adverse_stopwords.locators:pos", f"{TA}.adverse_stopwords.locators:neg")
    def test_threshold_and_locators(self):
        # 목록은 원장 실측 빈도 ≥ threshold 조각에서만 · 단어·패턴마다 locator ≥1(출처 없는 단어는 목록에 못 남는다)
        self.assertTrue(all(w["hits"] >= SW["threshold"] for w in SW["words"]))
        self.assertTrue(all(w["locators"] and all("@" in x for x in w["locators"]) for w in SW["words"]))
        self.assertTrue(all(p["locators"] for p in SW["patterns"]))
        # 음성: 빈도가 모자란(목록 밖) 조각은 parsed 가 아니라 미등록으로 남는다
        self.assertIn("뚜렷한", engines().phrase("부종 뚜렷한", locator="x:y@T/0")["unregistered"])


class Phrases(T):
    """V3.1-10 문구 사전 — 정규화형 1줄 · status auto/unlinked · phrase_shape · fragment_classes · 부록."""

    @covers(f"{TA}.status_values:neg", f"{TA}.expressions:pos", f"{TA}.expressions:neg")
    def test_status(self):
        E = engines()
        self.assertEqual(E.phrase("멍")["status"], "auto")
        self.assertEqual(E.phrase("멍 미지어")["reasons"], ["unregistered"])
        self.assertEqual(E.phrase("멍 · 이마")["reasons"], ["unattached_fragments"])
        self.assertEqual(E.phrase("이마")["reasons"][0], "no_event")
        self.assertTrue(set(ERD["tuple_rules"]["adverse"]["status_values"]) >= {"auto", "approved", "unlinked"})
        # 문구는 가리키기만(표현 개체 없음) — 판정은 단위 후보(세 칸)뿐
        c = E.phrase("공기색전 의심")["candidates"][0]
        self.assertEqual((c["event"], c["site"], c["qualifier"]), ("색전", None, "공기"))
        self.assertNotIn("course", c)

    @covers(f"{TA}.phrase_shape:pos", f"{TA}.phrase_shape:neg", f"{TA}.phrase_shapes:neg", f"{TA}.fragment_classes:neg")
    def test_shapes_and_classes(self):
        E = engines()
        want = {"event_only": "멍", "event_site": "주사 부위 부종", "event_degree_course": "경미한 부종", "event_incidence_condition": "부종 드물게", "explanatory": "부종 (가상설명)", "unresolved": "미지어 증상"}
        labels = {"event_incidence_condition": "3"}
        for shape, text in want.items():
            r = E.phrase(text, locator=f"x:y@S/{shape}")
            self.assertEqual(r["phrase_shape"], shape, text)
            mark(f"{TA}.phrase_shapes[{labels.get(shape, shape)}]", "test_shapes_and_classes")
        first = {w["class"]: w["word"] for w in reversed(SW["words"])}
        cls = {"event": "멍", "site": "이마 부종", "relative_site": "주사 부위 부종", "course": "일시적 부종", "qualifier": "공기색전", "explanation": "부종 (가상설명)", "unregistered": "부종 미지어"}
        cls.update({c: f"부종 {first[c]}" for c in SW["classes"]})
        for c, text in cls.items():
            got = {x["class"] for x in E.phrase(text, locator=f"x:y@F/{c}")["fragment_classes"]}
            self.assertIn(c, got, text)
            mark(f"{TA}.fragment_classes[{c}]", "test_shapes_and_classes")
        # 음성: 모든 토큰이 정해진 class 하나 — class 밖 토큰 0
        allowed = set(ADV["fragment_classes"])
        for text in list(want.values()) + list(cls.values()):
            self.assertTrue(all(x["class"] in allowed for x in E.phrase(text)["fragment_classes"]), text)

    @covers(f"{TA}.input.complications:pos", f"{TA}.input.complications:neg", f"{TA}.input.phrases:pos", f"{TA}.input.phrases:neg", f"{TA}.normal_phrases:pos", f"{TA}.normal_phrases:neg",
            f"{TA}.literature:pos", f"{TA}.literature:neg", f"{TA}.locator:pos", f"{TA}.locator:neg", f"{TA}.phrase_dictionary:pos", f"{TA}.phrase_dictionary:neg",
            f"{TA}.expressions_create_units:pos", f"{TA}.expressions_create_units:neg", f"{TA}.expressions_create_raw_units:pos", f"{TA}.expressions_create_raw_units:neg",
            f"{TA}.disclosure:pos", f"{TA}.disclosure:neg")
    def test_build_inputs_and_appendix(self):
        w, S = build("plain")
        A, AU = S.ctx["adv"], S.ctx["AU"]
        n_names = sum(len(c["complications"]) for c in S.ctx["L"]["complications.json"]["categories"])
        self.assertEqual(len(A["complications"]), n_names)
        # 음성: raw_name 단위는 complications 이름에서만 — 문구는 raw 단위를 만들지 않는다
        self.assertTrue(all(u["anchor"].startswith("complications.json:") for u in AU.units.values() if u["event_kind"] == "raw_name"))
        files = {c["file"] for e in AU.phrases.values() for c in e["contexts"]}
        self.assertEqual(files, {"consent-checklist.json", "post-procedure-timeline.json", "extracted.json", "taxonomy.json", "literature-evidence.json"})
        self.assertNotIn("complications.json", files)
        # 타임라인 normal — 닿으면(auto) R15(reaction_level=normal · source_phrases) · 아니면 게이트만
        r15n = [e for e in S.R["R15"] if e["attrs"].get("reaction_level", {}).get("value") == "normal"]
        self.assertTrue(r15n and all(e["attrs"]["source_phrases"]["value"] for e in r15n))
        un = [e for e in AU.phrases.values() if "미지반응" in e["raw_variants"]][0]
        self.assertEqual(un["status"], "unlinked")
        self.assertFalse([e for e in S.R["R15"] if un["id"] in e["attrs"].get("source_phrases", {}).get("value", [])])
        # 문헌 — statement 와 patient_ko 는 각자 항목(레코드 단위 「두 쪽 전부」 없음) · 영문 statement unlinked 라도 patient_ko 「멍」 은 auto
        st = [e for e in AU.phrases.values() if "Fake bruising" in e["raw_variants"]][0]
        ko = [e for e in AU.phrases.values() if "멍" in e["raw_variants"]][0]
        self.assertEqual((st["status"], ko["status"]), ("unlinked", "auto"))
        self.assertIn("patient_text", ko["kinds"])
        self.assertTrue(any(tr["lang"] == "en" for e in AU.phrases.values() for tr in e["translations"]))
        # locator — ERD 꼴 `@<계열>/<순번>` · provenance 는 원장 위치(배열 인덱스)
        self.assertIn("consent-checklist.json:categories[].emergency_signs[]@M1/0", ko["locators"])
        self.assertNotIn("consent-checklist.json:categories[].emergency_signs[]@0/0", ko["locators"])
        # 문구 사전: 같은 정규화형은 어느 출처든 한 항목 · 다른 정규화형은 다른 항목
        self.assertGreaterEqual(len(ko["locators"]), 5)
        self.assertEqual(ko["id"], mkid("PHR", ko["normalized"]))
        self.assertNotEqual(ko["id"], st["id"])
        # 조각 전부 사전 값인 문구는 단위를 세운다(이마 부종 → (부종, 이마, none)) · 미등록이 섞이면 세우지 않는다
        made = [u for u in AU.units.values() if u.get("created_by_phrase")]
        self.assertTrue(made and all(u["all_dict_values"] and not u["unregistered_fragments"] for u in made))
        self.assertTrue(any(u["site"] == "이마" and u["event"] == "부종" for u in made))
        self.assertFalse([u for u in AU.units.values() if u["event_kind"] == "raw_name" and u.get("created_by_phrase")])
        # 필수 고지 — clinical_rule(disclosure) + R32(ledger) + 문구 사전(kind=disclosure) · auto 면 R15 disclosure=true
        disc = [r for r in S.E["clinical_rule"].values() if r["attrs"]["kind"][0]["value"] == "disclosure"]
        self.assertEqual(len(disc), 2)
        self.assertEqual(len([e for e in S.R["R32"] if e["attrs"]["basis"]["value"] == "ledger"]), 2)
        self.assertTrue([e for e in S.R["R15"] if e["attrs"].get("disclosure", {}).get("value") is True])
        gd = [e for e in AU.phrases.values() if "합성 고지" in e["raw_variants"]][0]
        self.assertEqual((gd["status"], gd["kinds"]), ("unlinked", ["disclosure"]))   # 음성: 미등록 조각 고지는 게이트만(R15 없음 · R32 는 있다)
        self.assertNotIn("mandatory_disclosures", S.E["modality"][mkid("MOD", "M1")]["attrs"])

    def test_r15_course_member_level(self):
        """S-1 — 문구 유래 R15.course 는 그 단위 후보의 경과만(「주사 부위 일시적 부종 및 멍」의 멍 엣지는 null)."""
        E = engines()
        r = E.phrase("주사 부위 일시적 부종 및 멍")
        by = {c["event"]: c["courses"] for c in r["candidates"]}
        self.assertEqual((by["부종"], by["멍"]), (["일시"], []))


class Conditions(T):
    """V3.1-4 조건 단위(열거기 밖 · 빌더 구멍 확인용) — 완전 일치만 접고 미등록이면 raw_name · 표지어는 qualifier_text."""

    def test_condition_units(self):
        E = Engines()
        a = E.cond("임신")
        b = E.cond("임신 여부", path="category_specific[].checks[].label", file="pre-procedure-checklist.json")
        self.assertEqual((a["match"], a["condition_fragments"]), ("exact", ["임신"]))
        self.assertEqual((b["match"], b["qualifier_text"]), ("exact", ["여부"]))
        self.assertNotEqual(a["unit_ids"], b["unit_ids"])          # kind(condition · check)가 식별자에 들어간다
        self.assertEqual(a["unit_ids"], [mkid("CND", "condition|임신")])
        c = E.cond("가상 질환")
        self.assertEqual((c["match"], c["unit_ids"]), ("raw", [mkid("CND", f"RAW:condition|{norm('가상 질환')}")]))
        w, S = build("plain")
        self.assertIn(mkid("CND", "check|알레르기"), S.E["person_condition"])
        self.assertTrue([e for e in S.R["R16"] if e["to"]["id"] == mkid("CND", "condition|임신") and e["attrs"]["source_phrases"]["value"]])
