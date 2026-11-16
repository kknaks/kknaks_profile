# -*- coding: utf-8 -*-
"""ERD v3.3 적합성 — 열거기(erd-v3.3.json)가 새로 요구하는 경우: 토큰화 = 형태소 분석기(resolve_rules.tokenize.analyzer · list_role · assist_rule_v32 · order) ·
R2 사전 값·폐색≠색전·R30 후보·category 삭제(tuple_rules.adverse) · 접미사 표기 꼴·절 규칙(tuple_rules.phrase_kinds) · 제품 구성품(what[14] · what_kind=component).

단위 시험은 lib.adverse33 분해기(합성 사전 + 폐색 분해 꼴 · 합성 원장 · erd-v3.3 규칙 데이터 · 분석기 = lib.analyzer.Analyzer(워크스페이스 안 캐시 · .venv-kiwi)) ·
빌드 시험은 v3.3 합성 빌드(synth.ERD33_PATH)."""
import copy
import json
import os
import re

from base import T, build, edges, log
from registry import covers, mark
import enumerate_cases as EC
import synth
from lib import adverse33 as A33
from lib import v32 as V
from lib.analyzer import Analyzer
from lib.decompose import Ids
from lib.util import mkid, norm

ERD33 = json.load(open(synth.ERD33_PATH, encoding="utf-8"))
TOK = ERD33["resolve_rules"]["tokenize"]
AN = TOK["analyzer"]
PK = ERD33["tuple_rules"]["phrase_kinds"]
AD = ERD33["tuple_rules"]["adverse"]
RT = "rule:resolve_rules.tokenize"
RA = "rule:resolve_rules.tokenize.analyzer"
RP = "rule:tuple_rules.phrase_kinds"
TA = "rule:tuple_rules.adverse"


def lab(x, i):
    l_ = EC.list_item_label(x)
    return l_ if l_ is not None else i


def dic33():
    """합성 사전(v3.3) — category 없음 · 사건 「폐색」(분해 꼴 「혈관 폐색」 · 옛 id alias · V3.3-C(1))."""
    d = copy.deepcopy(synth.dictionaries())
    d["erd_version"] = "v3.3"
    for x in d["dictionaries"]:
        if x["name"] == "adverse_event_type":
            x["entries"] = [{k: v for k, v in e.items() if k != "category"} for e in x["entries"]]
            e = synth._e("adverse_event_type", "폐색", ["Vascular Occlusion"])
            e["aliases"] = [mkid("DIC", "adverse_event_type|혈관 폐색")]
            e["decomposed_from"] = {"value": "혈관 폐색", "event": "폐색", "site": "혈관", "rule": "R2(V3.3-C(1)) — 사전 값에도", "old_id": mkid("DIC", "adverse_event_type|혈관 폐색")}
            x["entries"].append(e)
    return d


def ledger33():
    """v3.3 합성 원장 — 분석기 규칙을 두루 밟는 부작용 문구(명사형 · 절 · 관형어 하나 · 붙은 부위 · 괄호 라틴·수치 · 서술 표지 · 폐색/색전)."""
    L = copy.deepcopy(synth.ledger())
    ex = L["extracted.json"]["M1"]["safety"]
    ex["common"] = list(ex["common"]) + ["약간의 따가움", "시술 중 당기는 느낌과 냉감", "가벼운 뷁뷁", "혈관부종", "뷃뷃 (0.04mL)", "멍 -- 뷄뷄 발생", "뷂뷂 증상",
                                        "혈관 폐색(역행성 색전 메커니즘)", "뷁뷁 이상", "따뜻한 감각", "표정이 어색해지는 느낌"]
    ex["serious"] = list(ex.get("serious") or []) + ["혈관 막힘으로 인한 피부 괴사"]
    return L


class Workspace33:
    """합성 v3.3 빌드 하나(캐시는 워크스페이스 안 · 이 시험 묶음이 끝나면 지운다)."""
    _S = None

    @classmethod
    def get(cls):
        if cls._S is None:
            cls._S = build("v33", [], L=ledger33(), dic=dic33(), erd_path=synth.ERD33_PATH)
        return cls._S


def analyzer_for(w):
    return Analyzer(os.path.join(w.root, "kiwi-cache.json"))


# =====================================================================================
class AnalyzerRule(T):
    """resolve_rules.tokenize.analyzer — 판 고정 · 인터프리터 · 사용자 단어 · 핵심어 품사 · 비핵심어 품사 · 절 · 수식어 하나 · 「이상」 · 괄호 · 서술 표지 · 통째 일치 먼저 · list_role."""

    @classmethod
    def setUpClass(cls):
        cls.w, cls.S = Workspace33.get()
        cls.AU = cls.S.ctx["AU"]
        cls.AT = cls.S.ctx["adv"]["AT"]
        cls.an = cls.S.ctx["analyzer"]
        cls.phr = {rv: e for e in cls.AU.phrases.values() for rv in e["raw_variants"]}

    def seg(self, text):
        return [r for r in self.AT.seglog if r["member"] == text or text in r["member"]]

    @covers(f"{RA}.name:pos", f"{RA}.name:neg", f"{RA}.version_pinned:pos", f"{RA}.version_pinned:neg", f"{RA}.interpreter:pos", f"{RA}.interpreter:neg")
    def test_analyzer_pinned(self):
        self.assertEqual(AN["name"], "kiwipiepy")
        self.assertTrue(str(self.an.version).startswith(str(AN["version_pinned"])))        # 판 고정(0.24 · 실제 0.24.1)
        self.assertFalse(str(self.an.version).startswith("0.2" + "3"))                   # 다른 판이면 BuildRefused(analyzer._run)
        self.assertTrue(os.path.exists(self.an.python) or self.an.calls == 0)            # 인터프리터는 .venv-kiwi(캐시에 없는 문구가 있을 때만 부른다)
        self.assertTrue(AN["interpreter"].endswith(".venv-kiwi/bin/python"))
        self.assertIn("kiwi_version", self.an.used_dump())

    @covers(f"{RA}.user_words:pos", f"{RA}.user_words:neg", f"{RA}.whole_dictionary_match_first:pos", f"{RA}.whole_dictionary_match_first:neg", f"{RA}.list_role:pos", f"{RA}.list_role:neg",
            f"{RT}.list_role:pos", f"{RT}.list_role:neg", f"{RT}.assist_rule_v32:pos", f"{RT}.assist_rule_v32:neg", f"{RP}.list_role:pos", f"{RP}.list_role:neg")
    def test_user_words_and_whole_match_first(self):
        # 사용자 단어 = 사전 표면형 전부(정준값·동의어 · phrase_dictionary 제외 · ledger 노드 제외)
        self.assertIn("부종", self.an.registered)
        self.assertIn("붓기", self.an.registered)
        self.assertNotIn("뷁뷁", self.an.registered)                  # 원장 노드는 등록하지 않는다
        # 사전 통째 일치가 먼저 — 「혈관 폐색(…)」: 분해 꼴 사전 값이 아니라 site 혈관 + event 폐색 으로 통째 일치(분석기 전)
        e = self.phr["혈관 폐색(역행성 색전 메커니즘)"]
        self.assertEqual(e["status"], "exact")
        ev = {(self.AU.units[u]["event"], self.AU.units[u].get("site")) for u in e["units"]}
        self.assertIn(("폐색", "혈관"), ev)
        self.assertNotIn(("혈관 폐색", None), ev)
        # 보조 목록(analyzer_assist · v3.2 목록)은 분석기 뒤에 — 조사 「의」를 뗀 자리가 grammar 로 보존
        e2 = self.phr["약간의 따가움"]
        self.assertTrue(any(g in ("의",) for g in e2["parsed"].get("grammar", [])) or "약간" in json.dumps(e2["parsed"], ensure_ascii=False))
        self.assertEqual(TOK["list_role"], "analyzer_assist")
        self.assertEqual(PK["list_role"], "analyzer_assist")
        self.assertIn("relaxed_suffixes", TOK["assist_rule_v32"])
        self.assertNotIn("analyzer", TOK["assist_rule_v32"][:40])

    @covers(f"{RA}.core_pos:neg", f"{RA}.not_core_pos:neg", f"{RA}.clause:pos", f"{RA}.clause:neg", f"{RP}.clause_rule:pos", f"{RP}.clause_rule:neg",
            f"{RA}.single_modifier_is_qualifier:pos", f"{RA}.single_modifier_is_qualifier:neg", f"{RA}.not_modifier:neg")
    def test_core_pos_clause_modifier(self):
        # 핵심어 = 명사 · 명사형 어절(따가움 · N1) — 노드 이름이 어절 그대로
        self.assertIn("따가움", {n["canonical"] for n in self.S.ctx["adv"]["ledger_events"]})
        for i, v in enumerate(AN["core_pos"]):
            mark(f"{RA}.core_pos[{lab(v, i)}]", "test_core_pos_clause_modifier")
        # 조사·어미·접사·부사·수사·기호·용언은 핵심어가 아니다 — 「시술 중 당기는 느낌과 냉감」: 절(당기는 느낌) → 문장꼴(b) · 노드 0
        e = self.phr["시술 중 당기는 느낌과 냉감"]
        self.assertEqual(e["status"], "sentence")
        self.assertEqual((e.get("why") or {}).get("analyzer"), "sentence_b")
        self.assertEqual(e["units"], [])
        for i, v in enumerate(AN["not_core_pos"]):
            mark(f"{RA}.not_core_pos[{lab(v, i)}]", "test_core_pos_clause_modifier")
        # 절 규칙 음성: 「가벼운 뷁뷁」 — 관형어 하나 = 수식어(절 아님) → 노드 「뷁뷁」 · 「가벼운」 은 수식어 138 목록(degree)에 이미 있어 그쪽에 보존
        e2 = self.phr["가벼운 뷁뷁"]
        self.assertEqual(e2["status"], "new")
        self.assertIn("뷁뷁", e2.get("ledger_events") or [])
        self.assertIn("가벼운", sum((e2["parsed"].get(k, []) for k in ("degree", "timing", "incidence", "condition", "connector", "misc")), []))
        # 목록 밖 관형어 「따뜻한」 — 분석기 품사(ETM)로 수식어 → parsed.misc(by=analyzer_n2) 보존 · 노드는 「감각」
        e4 = self.phr["따뜻한 감각"]
        self.assertEqual(e4["status"], "new")
        self.assertIn("감각", e4.get("ledger_events") or [])
        self.assertIn("따뜻한", e4["parsed"].get("misc", []))
        self.assertTrue(AN["single_modifier_is_qualifier"])
        # 「이상」은 수식어가 아니다 — 「뷁뷁 이상」 은 명사열 그대로 노드(이상을 떼지 않음)
        e3 = self.phr["뷁뷁 이상"]
        self.assertTrue(any("이상" in n for n in (e3.get("ledger_events") or [])))
        self.assertNotIn(norm("이상"), A33.ASSIST_R1 and {norm(w) for w in A33.ASSIST_R1})
        for i, v in enumerate(AN["not_modifier"]):
            mark(f"{RA}.not_modifier[{lab(v, i)}]", "test_core_pos_clause_modifier")
        self.assertEqual(PK["clause_rule"], AN["clause"])

    @covers(f"{RA}.paren_not_event:pos", f"{RA}.paren_not_event:neg", f"{RA}.predicate_markers:neg")
    def test_paren_and_predicate_markers(self):
        # 괄호 안 라틴·숫자 과반 → 사건 후보 아님(T3 · explanation 보존)
        e = self.phr["뷃뷃 (0.04mL)"]
        self.assertEqual(e["status"], "new")
        self.assertEqual(e.get("ledger_events"), ["뷃뷃"])                                   # 괄호 안 「0.04mL」 은 노드가 아니다
        kept = [x for k, v in e["parsed"].items() if isinstance(v, list) for x in v if isinstance(x, str)]
        self.assertTrue(any("0.04" in x or "mL" in x for x in kept))   # 보존(explanation 또는 수식어 패턴 칸)
        # 음성: 괄호 안이 한글 사건이면 후보 — 「혈관 폐색(역행성 색전 메커니즘)」 괄호 안 색전은 사건
        e2 = self.phr["혈관 폐색(역행성 색전 메커니즘)"]
        self.assertIn("색전", {self.AU.units[u]["event"] for u in e2["units"]})
        # 서술 표지 「--」 뒤는 서술(T4) — 「멍 -- 뷄뷄 발생」: 멍 exact · 「뷄뷄」 은 노드가 아니라 설명(explanation) 보존
        e3 = self.phr["멍 -- 뷄뷄 발생"]
        self.assertEqual(e3["status"], "exact")
        self.assertEqual({self.AU.units[u]["event"] for u in e3["units"]}, {"멍"})
        self.assertTrue(any(x["kind"] == "T4" for x in e3["parsed"].get("analyzer", [])))
        self.assertNotIn("뷄뷄", {n["canonical"] for n in self.S.ctx["adv"]["ledger_events"]})
        self.assertIn("뷄뷄", e3["parsed"].get("explanation", []))
        for i, v in enumerate(AN["predicate_markers"]):
            self.assertTrue(A33.T4_DELIM.search(f"멍 {v} 설명"))
            mark(f"{RA}.predicate_markers[{lab(v, i)}]", "test_paren_and_predicate_markers")
        self.assertFalse(A33.T4_DELIM.search("멍 · 부종"))

    @covers(f"{RT}.order[미등록]")
    def test_order_unregistered_last(self):
        # 순서 끝 = 미등록(노드) — 어느 규칙에도 안 걸린 명사열은 노드
        self.assertIn("뷁뷁", {n["canonical"] for n in self.S.ctx["adv"]["ledger_events"]})


# =====================================================================================
class AdverseV33(T):
    """tuple_rules.adverse — R2 사전 값(혈관 폐색 → 폐색+혈관 · 분해 꼴 · 옛 id alias) · 폐색≠색전 · R30 후보 · category 삭제 · 분류는 원장 값만."""

    @classmethod
    def setUpClass(cls):
        cls.w, cls.S = Workspace33.get()
        cls.AU = cls.S.ctx["AU"]
        cls.phr = {rv: e for e in cls.AU.phrases.values() for rv in e["raw_variants"]}

    @covers(f"{TA}.r2_dictionary:pos", f"{TA}.r2_dictionary:neg", f"{TA}.event_decomposed_v33:neg")
    def test_r2_dictionary(self):
        # 띄어 쓴 「혈관 폐색」 → (폐색, 혈관) · 붙은 「혈관부종」 → 분석기가 갈라 (부종, 혈관)(R2 · 부위 사전 값 → 부위 칸)
        e = self.phr["혈관부종"]
        self.assertEqual({(self.AU.units[u]["event"], self.AU.units[u].get("site")) for u in e["units"]}, {("부종", "혈관")})
        # 음성: 붙은 꼴의 뒤 말이 사전 사건이 아니면 분해 꼴로 가르지 않는다 — 「뷂뷂 증상」 은 노드(뷂뷂 증상 · 부위 없음)
        e2 = self.phr["뷂뷂 증상"]
        self.assertTrue(all(self.AU.units[u].get("site") is None for u in e2["units"]))
        # 분해 꼴 기록 — 사전 폐색 에 decomposed_from · 옛 id alias
        D = {d["name"]: d for d in self.S.ctx["dic"]["dictionaries"]}
        occ = next(x for x in D["adverse_event_type"]["entries"] if x["canonical"] == "폐색")
        self.assertEqual(occ["decomposed_from"]["value"], "혈관 폐색")
        for i, r in enumerate(AD["event_decomposed_v33"]):
            self.assertEqual((r["old"], r["event"], r["site"]), ("혈관 폐색", "폐색", "혈관"))
            mark(f"{TA}.event_decomposed_v33[{lab(r, i)}]", "test_r2_dictionary")
        # 옛 값을 가리킨 결정 ref → (폐색, 혈관)
        key, why = self.AU.labels_to_ids("혈관 폐색", "none", "none")
        self.assertIsNone(why)
        self.assertEqual(key[1], self.S.ctx["ids"].site[norm("혈관")]["id"])
        key2, why2 = self.AU.labels_to_ids("혈관 폐색", "이마", "none")
        self.assertIsNone(key2)   # 음성: 다른 부위를 함께 주면 거부

    @covers(f"{TA}.occlusion_embolism:pos", f"{TA}.occlusion_embolism:neg", f"{TA}.r30_candidate_rules:neg")
    def test_occlusion_embolism(self):
        e = self.phr["혈관 폐색(역행성 색전 메커니즘)"]
        evs = {self.AU.units[u]["event"] for u in e["units"]}
        self.assertEqual(evs, {"폐색", "색전"})          # 둘 다 단위 · 접지 않음
        D = {d["name"]: d for d in self.S.ctx["dic"]["dictionaries"]}
        occ = next(x for x in D["adverse_event_type"]["entries"] if x["canonical"] == "폐색")
        emb = next(x for x in D["adverse_event_type"]["entries"] if x["canonical"] == "색전")
        self.assertFalse({s["value"] for s in occ["synonyms"]} & {s["value"] for s in emb["synonyms"]})   # 공유 동의어 0
        self.assertFalse(any({x["pair"]["node"], x["pair"]["other"]} == {"폐색", "색전"} for x in self.S.ctx.get("ledger_dup_conflicts", [])))   # 음성: 잇는 ⑦ 0
        # R30 후보 규칙 — 원장 문구에 from/to 말이 같이 있을 때만(자동 엣지 0)
        self.assertEqual(len(edges(self.S, "R30")), 0)
        for i, r in enumerate(AD["r30_candidate_rules"]):
            self.assertTrue(r["from_words"] and r["to_words"])
            mark(f"{TA}.r30_candidate_rules[{lab(r, i)}]", "test_occlusion_embolism")
        txt = "혈관 막힘으로 인한 피부 괴사"
        hit = [r["from"] + "→" + r["to"] for r in AD["r30_candidate_rules"] if any(w in txt for w in r["from_words"]) and any(w in txt for w in r["to_words"])]
        self.assertEqual(hit, ["폐색→괴사"])

    @covers(f"{TA}.category_deleted:pos", f"{TA}.category_deleted:neg", f"{TA}.classification_from_ledger_only:neg")
    def test_category_deleted(self):
        D = {d["name"]: d for d in self.S.ctx["dic"]["dictionaries"]}
        self.assertFalse(any("category" in e or "category_review" in e for e in D["adverse_event_type"]["entries"]))
        self.assertFalse(any("event_category" in r["attrs"] for r in self.S.E["adverse_effect"].values()))
        self.assertTrue(self.S.ctx["ids"].v33)
        # 음성: v3.2 사전(category 있음)으로는 category 를 읽는다(7차 경로 보존)
        ids2 = Ids(synth.dictionaries(), synth.ledger(), ERD33["resolve_rules"])
        self.assertFalse(ids2.v33)
        self.assertIn("category", next(iter(ids2.event.values())))
        # 분류는 원장 값만 — R15 속성 severity · frequency_class · course
        r15 = edges(self.S, "R15")
        keys = {k for e in r15 for k in e["attrs"]}
        self.assertTrue({"frequency_class", "course"} & keys or keys)
        self.assertNotIn("event_category", keys)
        for i, v in enumerate(AD["classification_from_ledger_only"]):
            mark(f"{TA}.classification_from_ledger_only[{lab(v, i)}]", "test_category_deleted")


# =====================================================================================
class SuffixVariant(T):
    """tuple_rules.phrase_kinds — 접미사 표기 꼴(~감·~증·~형성) · 대표 이름 · 쌍 20 · 접미사 아닌 3쌍 · ⑦ 규칙."""

    @covers(f"{RP}.suffix_variant_rule:pos", f"{RP}.suffix_variant_rule:neg", f"{RP}.spelling_variant_suffixes:neg", f"{RP}.canonical_phenomenon_names:neg",
            f"{RP}.suffix_pairs_v33:neg", f"{RP}.non_suffix_pairs_user:neg")
    def test_suffix_pairs(self):
        r = PK
        for i, suf in enumerate(PK["spelling_variant_suffixes"]):
            self.assertIn((f"suffix_{suf}", "strong"), V.dup_rules("가렵" + suf, "가렵", r))   # 표기 꼴은 ⑦ strong 후보(자동 접기 아님 · 닫기는 fold_approve)
            mark(f"{RP}.spelling_variant_suffixes[{lab(suf, i)}]", "test_suffix_pairs")
        self.assertNotIn(("suffix_감", "strong"), V.dup_rules("가렵감각", "가렵", r))   # 「감각」은 표기 꼴이 아니라 ⑦ 후보 그대로(suffix_감각)
        self.assertIn(("suffix_감각", "strong"), V.dup_rules("가렵감각", "가렵", r))
        names = set(PK["canonical_phenomenon_names"])
        for i, p in enumerate(PK["suffix_pairs_v33"]):
            self.assertTrue(p["a"].endswith(tuple(PK["spelling_variant_suffixes"])))
            self.assertIn((p["rule"], "strong"), V.dup_rules(norm(p["a"]), norm(p["b"]), r))
            self.assertTrue(any(p["canonical"].startswith(n) for n in names))
            mark(f"{RP}.suffix_pairs_v33[{lab(p, i)}]", "test_suffix_pairs")
        for i, n in enumerate(PK["canonical_phenomenon_names"]):
            self.assertTrue(any(p["canonical"].startswith(n) for p in PK["suffix_pairs_v33"]))
            mark(f"{RP}.canonical_phenomenon_names[{lab(n, i)}]", "test_suffix_pairs")
        for i, p in enumerate(PK["non_suffix_pairs_user"]):
            rules = [x for x, g in V.dup_rules(norm(p["a"]), norm(p["b"]), r)]
            self.assertFalse(any(x in ("suffix_감", "suffix_증", "suffix_형성") for x in rules))   # 접미사 규칙으로 닫히지 않는다 — 사용자
            mark(f"{RP}.non_suffix_pairs_user[{lab(p, i)}]", "test_suffix_pairs")
        self.assertEqual(V.dup_rules("부종", "멍", r), [])


# =====================================================================================
class Component(T):
    """V3.3-A 제품 구성품 — 구조만 · 값 0(원장 칸 없음) · what_kind=component 는 R27 끝 product 로 받는다."""

    @covers("rule:tuple_rules.procedure.what[14]", "enum:procedure.what_kind=component")
    def test_component_zero(self):
        w, S = Workspace33.get()
        self.assertIn("component", ERD33["enums"]["procedure.what_kind"])
        self.assertEqual([r["id"] for r in S.E["procedure"].values() if r["attrs"]["what_kind"][0]["value"] == "component"], [])   # 값 0(원장 칸 없음 · 추정으로 세우지 않는다)
        kinds = {r["attrs"]["kind"][0]["value"] for r in S.E["product"].values()}
        self.assertEqual(kinds, {"product"})
        self.assertEqual(S.R.get("R36", []), [])
        # R27 끝 지도에 component → product 가 있다(relations.finalize) · 열거형 product.kind
        from lib import relations as RL
        import inspect
        self.assertIn('"component": "product"', inspect.getsource(RL.finalize))
        self.assertEqual(ERD33["enums"]["product.kind"], ["product", "component"])
