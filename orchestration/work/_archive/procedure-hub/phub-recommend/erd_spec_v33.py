# -*- coding: utf-8 -*-
"""ERD v3.3 명세 (데이터). erd_spec_v32.py(v3.2 · 동결)를 읽어 발주서 erd-v3.3-brief.md 의 사용자 결정 A~G(2026-11-06)만 덧씌운다.
  V3.3-A 제품 구성품(소모품) 구조 — product.kind=component · R36 component_of · what 이 기기 product 또는 그 component. 값 0 · 구조만(원장 칸 없음 · 미래 칸).
  V3.3-B 토큰화 = 형태소 분석기(kiwipiepy 0.24 판 고정 · 사전 값 전부 사용자 단어 등록) — §1.3 「조사·어미 목록에서 뗀다」 문장 교체 · 기존 목록은 「분석기 보조 목록」으로 격하.
  V3.3-C 부작용 사전·부위 — (1) R2 를 기존 사건 사전 값에도(「혈관 폐색」→ 폐색 + 부위 혈관 · 정맥염·혈관외유출은 사용자 결정 필요) (2) 부위 사전 동맥·정맥·안동맥(parent) (3) 폐색 ≠ 색전 · R30 후보는 제안 (4) 승인 씨앗 부위 15 · 성분 6 = 결정 레코드(dictionary_add · 8차 적용) — ERD 값 아님.
  V3.3-D 접미사 ~감·~증·~형성 = 표기 꼴 · 대표 이름 = 현상 이름 · 쌍 20 은 fold_approve 결정 · 접미사 아닌 3쌍은 사용자.
  V3.3-E adverse_event_type.category(7분류) 삭제 — 원장 출처 0(ERD v2 발주서 창작). 분류는 원장 값만(complications severity · taxonomy safety 칸 = frequency_class · 엣지 course).
  V3.3-F 「무엇을·어떻게 세분」 묶음 — 설계안 2~3 표만(적용 0 · 결정은 사용자).
  V3.3-G 원장 3판(synergy 정식 이름 · M8›기타 항목 2) · 실측 재생성 · 「이름 교체 + 부위 분리」 결정 kind 필요 여부 검토.
사용자 정의 1·2·3 · 명시 예외 · 원칙 A~D 는 v3.2 그대로. 원장 21 = 브론즈 3판(`bronze/phub-ledger/` · HASHES.txt 3판) · 2판은 `bronze/phub-ledger-v2/`(대조용).
erd_build_v33.py · erd_colmap_v33.py · erd-v3.3-tuples.py 가 읽는다. v3.2 명세·산출물은 손대지 않는다.
A~G 밖의 개체·속성·사전 값·분류는 새로 만들지 않는다 — 애매한 것은 USER_DECISIONS_NEEDED(「사용자 결정 필요」)에 적고 빈 자리로 둔다.
"""
import copy
import os
import sys
import types

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import erd_spec_v32 as V32  # noqa

for _k, _v in vars(V32).items():
    if _k.startswith("_") or isinstance(_v, types.ModuleType):
        continue
    globals()[_k] = _v

ERD_VERSION = "v3.3"
PREVIOUS_VERSION = "v3.2"
WRITTEN = "2026-11-06"
LEDGER_DIR = os.path.join(HERE, "bronze", "phub-ledger")        # 원장의 집 · 3판
LEDGER_DIR_V2 = os.path.join(HERE, "bronze", "phub-ledger-v2")  # 2판(대조 · v3.2 실측 기준)
BRONZE_VERSION = 3
BRONZE_DATE = "2026-11-06"
BRONZE_HASHES = os.path.join(LEDGER_DIR, "HASHES.txt")
BRONZE_CHANGELOG = os.path.join(LEDGER_DIR, "CHANGELOG.md")
KIWI_PYTHON = os.path.join(HERE, "silver-v3", ".venv-kiwi", "bin", "python")
KIWI_PINNED = "0.24"

ENTITIES = copy.deepcopy(V32.ENTITIES)
RELATIONS = copy.deepcopy(V32.RELATIONS)
RESOLVE_RULES = copy.deepcopy(V32.RESOLVE_RULES)
TUPLE_RULES = copy.deepcopy(V32.TUPLE_RULES)
ERD_ENUMS = copy.deepcopy(V32.ERD_ENUMS)
ID_RULE = copy.deepcopy(V32.ID_RULE)
NORMALIZE_RULE = copy.deepcopy(V32.NORMALIZE_RULE)
DECISION_KINDS = [list(x) for x in V32.DECISION_KINDS]
PRINCIPLES = [(k, v) for k, v in V32.PRINCIPLES]
PRINCIPLES_TEXT = V32.PRINCIPLES_TEXT


def _ent(key):
    return next(e for e in ENTITIES if e["key"] == key)


def _rel(rid):
    return next(r for r in RELATIONS if r["id"] == rid)


# ---------------------------------------------------------------------------
# V3.3-A 제품 구성품(소모품) — 구조만 · 값 0
# ---------------------------------------------------------------------------
COMPONENT_RULE = ("**제품 구성품(V3.3-A · 사용자 2026-11-06 「포텐자 시술이면 포텐자 팁도 무엇을에 포함 되야 하는거 아니야 ? 기기 시술은 기기 시술도구도 포함」)**: 기기 시술의 「무엇을」은 기기 제품 또는 그 제품의 **구성품**(소모품 · 팁·카트리지·핸드피스·트랜스듀서 같은 교체·장착 부품)이다 — 성분 what(V3.2-6)과 대칭. "
                  "구조: product 개체에 `kind ∈ {product, component}` · component 는 R36 component_of(component → 기기 product · N:1)로 기기에 묶이고, 시술 튜플의 what 은 기기 product 또는 그 component(what_kind=component · R27 끝 product(kind=component) · 접힘 조건은 사전 what 과 같다). "
                  "**값 0 · 구조만** — 원장 21 에 구성품 칸이 없다(「포텐자 팁」0회 · 팁·카트리지·핸드피스는 주의·설명 문장 안에만 · 실측 §9.18). 구성품 값은 원장에 구성품 칸이 생길 때(기기 사진·기법 설명 조사 파일 입구 · V3-7 media_refs 와 같은 길) 그 칸에서 세운다 — 문장 안의 낱말로 추정해 세우지 않는다(추정 금지). column-map 에는 「원장 칸 없음 · 미래 칸」으로 표기.")
FUTURE_COLUMNS_V33 = [
    # (미래 칸(원장에 없음) · 행선지 · 표적 · 비고)
    ("products.*.products[].components[].name", "개체", "product.name(kind=component)", "V3.3-A 미래 칸 — 구성품 이름(팁·카트리지·핸드피스·트랜스듀서 …) · 지금 원장 칸 없음 · 값 0"),
    ("products.*.products[].components[].of", "엣지", "R36.component_of(to=기기 product)", "V3.3-A 미래 칸 — 구성품이 붙는 기기 제품 · 값 0"),
    ("products.*.products[].components[].kind", "개체", "product.component_kind", "V3.3-A 미래 칸 — 구성품 종류 라벨(원장 칸이 생길 때 그 값 그대로 · 열거형은 정하지 않았다 · 값 0)"),
]
COMPONENT_EVIDENCE_WORDS = ["팁", "카트리지", "핸드피스", "트랜스듀서"]   # 실측 §9.18 — 원장 어느 자리에 나오나(시술 라벨 자리 0 이면 「값 0」의 근거)

_pr = _ent("product")
_pr["definition"] += " " + COMPONENT_RULE
_pr["attrs"].append(("kind", "enum(product|component)", True, [], "v3.3(V3.3-A): product = 제품(약제·기기·실 · 기본) · component = 기기 구성품(소모품) · 원장 칸 없음 → 지금 전부 product(값 0)"))
_pr["attrs"].append(("component_of", "PRD-|null", False, [], "v3.3(V3.3-A): kind=component 일 때 붙는 기기 product(R36) · 아니면 null · 값 0"))
_pr["attrs"].append(("component_kind", "str|null", False, [], "v3.3(V3.3-A): 구성품 종류 라벨 — 원장 칸이 생길 때 그 값 그대로(열거형 정하지 않음) · 지금 null"))
_pc = _ent("procedure")
_pc["attrs"] = [a if a[0] != "what_kind" else ("what_kind", "enum(modality|modality_subcategory|product|catalog_item|ingredient|component)", True, a[3], (a[4] or "") + " · v3.3(V3.3-A): component = 기기 구성품(product.kind=component) — 성분 what 과 대칭 · 값 0") for a in _pc["attrs"]]
_r27 = _rel("R27")
_r27["to"] = "modality|modality_subcategory|product|product(kind=component)|catalog_item"
_r27["attrs"] = [(a, b if a != "what_kind" else "enum(modality|modality_subcategory|product|catalog_item|ingredient|component)", c) for a, b, c in _r27["attrs"]]
_r27["note"] = (_r27["note"] or "") + " · v3.3(V3.3-A): 끝이 product(kind=component)일 수 있다(what_kind=component) — 값 0"
RELATIONS.append({"id": "R36", "name": "component_of", "from": "product(kind=component)", "to": "product", "card": "N:1", "attrs": [("component_kind", "str|null", "v3.3(V3.3-A): 구성품 종류 라벨(원장 칸 생길 때) · 지금 null")],
                  "sources": [], "note": "v3.3(V3.3-A): " + COMPONENT_RULE})
ERD_ENUMS["product.kind"] = ["product", "component"]
ERD_ENUMS["procedure.what_kind"] = ["modality", "modality_subcategory", "product", "catalog_item", "ingredient", "component"]
if "component" not in ERD_ENUMS["edge_end_kind"]:
    ERD_ENUMS["edge_end_kind"] = list(ERD_ENUMS["edge_end_kind"]) + ["component"]
ID_RULE["product_component"] = "v3.3(V3.3-A): PRD-<sha256(기기 PRD- id|norm(구성품 이름))[:10]> — 구성품은 기기 제품 안에서 유일 · 값 0"
TUPLE_RULES["component"] = {"rule": COMPONENT_RULE, "values": 0, "future_columns": [{"column": a, "dest": b, "target": c, "note": d} for a, b, c, d in FUTURE_COLUMNS_V33], "evidence_words": COMPONENT_EVIDENCE_WORDS}
TUPLE_RULES["procedure"]["what"] = list(TUPLE_RULES["procedure"]["what"]) + ["v3.3(V3.3-A): what 은 기기 product 또는 그 component(product.kind=component · R36) — 성분 what 과 대칭 · 원장 칸 없음 → 값 0"]

# ---------------------------------------------------------------------------
# V3.3-B 토큰화 = 형태소 분석기 — 규칙 문장 교체 · 목록은 보조로 격하
# ---------------------------------------------------------------------------
TOKENIZE_RULE_V33 = ("**토큰화(V3.3-B · 사용자 2026-11-06 「형태소 분석기를 쓴다」 · 근거 `silver-v3/out-dryrun/report.md` · `out-dryrun2/report.md` · `out-dryrun3/report.md`)**: 부작용 문구·조건·시술 라벨의 토큰은 「조사·어미 목록에서 뗀다」가 아니라 **형태소 분석기 kiwipiepy(판 고정 0.24 · 사전 값 전부 사용자 단어 등록)의 품사**로 가른다. "
                     "**핵심어** = 명사(NNG·NNP · 사용자 단어로 등록된 사전 값은 SL 포함) + **용언 어간 + ㅁ/음 명사형 어절**(ETN · 어절 그대로가 이름 — 따가움·막힘·처짐 · 뒤 접속 조사·기호만 뗀다). 조사(J*)·어미(E*)·접사(XS*)·부사(MAG·MAJ)·수사(NR·SN)·기호(S*)·동사/형용사(VV·VA · 명사형 어절 안은 제외)는 핵심어가 될 수 없다. "
                     "**문장꼴** = 절이 있을 때만 — 용언 + 연결/종결 어미(EC·EF · 「-게」 부사형 제외), 또는 관형형(ETM)·부사형 어절 앞에 그 용언의 논항(격조사 어절)이 있을 때, 또는 관형형 뒤 어절 머리가 의존명사(NNB)·「현상·느낌·증상·경우」일 때. 절 없이 명사 앞에 붙은 **관형어 하나는 수식어**(R1 · R15 qualifier_text · 보존). 「이상」은 수식어가 아니다(1차 드라이런 오분해 — 색소이상→색소). "
                     "사건 말 앞의 부위·구조 말(부위 사전 · R2)은 **붙여 써도** 분석기가 형태소로 갈라 부위 칸으로 뗀다(「동맥폐색」「혈관폐색」→ (폐색, 동맥)·(폐색, 혈관) · 뒤 말이 사전 사건일 때만 · 뒤 말이 사전 사건이 아니면 애매 → 사용자). 괄호 안 영문 약어·수치·%·비교(「(Vascular Occlusion)」「(0.04mL)」「(박피에 비해 작음)」)는 사건 후보가 아니다 — R15 속성 또는 문헌 후보(parsed.explanation 보존). 같은 묶음의 「--」「—」「:」 뒤는 서술(predicate · 보존). 분석기 결과도 사전 통째 일치가 먼저다(V3-6 · V3.1-6 · 사전 값은 사용자 단어라 한 형태소로 나온다). "
                     "**v3.2 의 목록**(조사 27 · 용언 어미 18 · 문법 낱말 21 · relaxed 접미 9 · predicate 어미 7 · 접속 조사 5 · note_words 35 · core_exclude 7 · fallback_core 7)은 규칙이 아니라 **분석기 보조 목록**(analyzer_assist)이다 — 분석기가 어절을 가르지 못한 자리(미등록 외래어·붙여 쓴 꼴)에서만 뒤에 쓰고, 뗀 조각은 grammar_tokens[] 로 보존한다(원칙 B). "
                     "ERD 실측(`erd-v3.3-tuples.py`)은 분석기 없이 돈다(실버 빌더 lib 가 분석기를 든다 · 8차) — 그래서 §9 의 노드 수는 v3.2 규칙 수치이고 분석기 적용 수치는 드라이런 3차 §5(새 노드 179 · 사건 노드 222 · ⑦ strong 36)에 있다. 판 고정은 실측이 센다(§9.19 kiwipiepy 버전 · 등록할 사전 값 수).")
ANALYZER_RULE = {"name": "kiwipiepy", "version_pinned": KIWI_PINNED, "interpreter": "silver-v3/.venv-kiwi/bin/python", "user_words": "사전 값 전부(정준값·동의어 · all_surfaces) — 한 형태소(SL/NNP)로 나오게 등록",
                 "core_pos": ["NNG", "NNP", "SL(사전 값)", "용언 어간+ETN(-ㅁ/-음) 명사형 어절"], "not_core_pos": ["J*", "E*", "XS*", "MAG", "MAJ", "NR", "SN", "S*", "VV", "VA"],
                 "clause": "용언+EC/EF(-게 제외) | ETM·부사형 앞 격조사 논항 | ETM 뒤 NNB·현상·느낌·증상·경우", "single_modifier_is_qualifier": True, "not_modifier": ["이상"],
                 "paren_not_event": "라틴·숫자·%·비교 과반", "predicate_markers": ["--", "—", ":"], "whole_dictionary_match_first": True, "list_role": "analyzer_assist"}
RESOLVE_RULES["tokenize"] = dict(RESOLVE_RULES["tokenize"])
RESOLVE_RULES["tokenize"]["rule"] = TOKENIZE_RULE_V33
RESOLVE_RULES["tokenize"]["analyzer"] = ANALYZER_RULE
RESOLVE_RULES["tokenize"]["list_role"] = "analyzer_assist"
RESOLVE_RULES["tokenize"]["assist_rule_v32"] = V32.TOKENIZE_RULE
RESOLVE_RULES["tokenize"]["order"] = ["사전 통째 일치(사용자 단어)", "형태소 분석(kiwipiepy 0.24) — 품사로 핵심어·수식어·문장꼴", "분석기 보조 목록(어절을 못 가른 자리만) — 수식어·stopword·표지어 → 문법 낱말 → 조사·어미", "미등록"]
RESOLVE_RULES["tokenize"]["preserved_as"] = "grammar_tokens[] · predicate · explanation"
TUPLE_RULES["phrase_kinds"] = dict(TUPLE_RULES["phrase_kinds"])
TUPLE_RULES["phrase_kinds"]["list_role"] = "analyzer_assist"
TUPLE_RULES["phrase_kinds"]["clause_rule"] = ANALYZER_RULE["clause"]
ERD_ENUMS["tokenize.list_role"] = ["analyzer_assist"]
ERD_ENUMS["tokenize.core_pos"] = ANALYZER_RULE["core_pos"]

# ---------------------------------------------------------------------------
# V3.3-C 부작용 사전·부위 — R2 를 사전 값에도 · 부위 3 · 폐색 ≠ 색전 · 승인 씨앗은 결정 레코드
# ---------------------------------------------------------------------------
R2_DICT_RULE = ("**R2 를 기존 사건 사전 값에도(V3.3-C(1) · 사용자 2026-11-06 「R2 는 기존 사전 43값에도」 · 드라이런 3차 §3.3 N3)**: 사건 사전 값(정준값·동의어)이 「부위 말 + 사건 말」을 **띄어 쓴 꼴**이면 사건 말이 값이고 부위 말은 부위 칸이다 — 「혈관 폐색」→ 사건 **폐색** + 부위 **혈관**(site · layer) · 동의어 「Vascular Occlusion」은 폐색의 동의어로 간다 · 옛 값 「혈관 폐색」은 사전 값이 아니라 **분해 꼴**(decomposed_from · 옛 DIC- id 는 alias)로 남고 문구 사전 raw_variants 가 원문을 보존한다. "
                "그래서 「동맥 폐색」「안동맥 폐색」「혈관 폐색」은 같은 사건 폐색의 부위가 다른 단위가 된다(정의 2). 띄어쓰기 없이 붙은 값(「정맥염」「혈관외유출」)은 뒤 말이 사건 말인지 애매하므로 분해하지 않고 「사용자 결정 필요」에 둔다 — 추정으로 가르지 않는다(원장 문구의 붙은 꼴 「혈관폐색」은 뒤 말 폐색이 사전 사건이라 분석기(V3.3-B)가 가른다 · 목록 규칙 실측에서는 새 노드 1 로 남는다 §9.20). "
                "동의어 중 「피부 딤플링」「피부 괴사」는 이미 정준값(딤플링·괴사)으로 접히므로 값 변경이 없다(N3 동치표 일치). 사전 43 값 중 분해 1 · 애매 2 · 분해 안 함 40(§9.20).")
SITE_ADDED_V33 = [
    # (값, kind, parent, 승인 근거) — 사용자 승인 2026-11-06 · 드라이런 3차 §3.5 N4 임시 값을 사전 값으로 · locator 는 실측이 센다(§9.20)
    ("동맥", "layer", "혈관", "사용자 승인 2026-11-06(HANDOFF 「부위 사전에 동맥·정맥·안동맥」) · dryrun3 §3.5 N4"),
    ("정맥", "layer", "혈관", "사용자 승인 2026-11-06 · dryrun3 §3.5 N4(부위로 떨어진 자리 0 — 정맥염은 붙은 꼴 · 사용자 결정 필요)"),
    ("안동맥", "layer", "동맥", "사용자 승인 2026-11-06 · dryrun3 §3.5 N4(자리 3 · 「안동맥 역행성 색전」「0.04mL 안동맥 폐색 임계량」「안동맥 0.04mL 폐색 위험」)"),
]
EVENT_DECOMPOSED_V33 = [
    # (옛 정준값, 새 정준값(사건 말), 부위 말, 동의어 처리, 근거)
    ("혈관 폐색", "폐색", "혈관", "Vascular Occlusion → 폐색 동의어 · 「혈관 폐색」= 분해 꼴(raw_variant · alias)", "사용자 2026-11-06 · dryrun3 §2 (라) · §3.3 N3 #22"),
]
OCCLUSION_EMBOLISM_RULE = ("**폐색 ≠ 색전(V3.3-C(3) · 사용자 2026-11-06)**: 폐색(Occlusion)과 색전(Embolism)은 다른 사건이다 — 접지 않고 동의어로도 두지 않는다(드라이런 3차 N5: 한 묶음인 자리 0). 「혈관폐색/색전」의 `/` 는 대안(또는)이라 두 사건에 다 붙는다(V3-4). "
                           "원장 문구가 둘을 한 문장에 인과로 적은 자리(「혈관 막힘으로 인한 피부 괴사」「혈관 폐색(역행성 색전 메커니즘)」)는 **R30 leads_to 후보 — 색전 → 폐색 · 폐색 → 괴사** 로 §9.20 에 제안만 둔다(edge_create 결정이 approved 일 때만 엣지 · 지금 R30 엣지 0 · 레코드 만들지 않았다).")
R30_CANDIDATE_RULES = [("색전", "폐색", ["색전"], ["폐색", "막힘"]), ("폐색", "괴사", ["폐색", "막힘"], ["괴사"])]   # (from, to, from 말, to 말) — 한 문구에 둘 다 나오면 후보(원장 근거 · 제안)
SEED_APPROVED_V33 = {
    # 사용자 승인 2026-11-06 — ERD 사전 값이 아니라 결정 레코드(dictionary_add · 8차 적용)로 들어간다. ERD 는 「승인됨 · 8차 적용」으로만 표기 · locator 는 실측(§9.21 · v3.2 씨앗 후보 행)
    "site": [("눈밑", "anatomical", "눈가"), ("눈꺼풀", "anatomical", "눈가"), ("코끝", "anatomical", "코"), ("목주름", "anatomical", "목"), ("얼굴 전체", "region", "얼굴"), ("바디 전체", "region", None), ("복부", "anatomical", "바디 전체"), ("옆구리", "anatomical", "바디 전체"),
             ("팔뚝", "anatomical", "바디 전체"), ("허벅지", "anatomical", "바디 전체"), ("종아리", "anatomical", "바디 전체"), ("힙", "anatomical", "바디 전체"), ("가슴", "anatomical", "바디 전체"), ("겨드랑이", "anatomical", "바디 전체"), ("두피", "region", None)],
    "ingredient_material": [("HA", None, None), ("히알루론산", None, None), ("TCA", None, None), ("글리콜산", None, None), ("살리실산", None, None), ("페놀", None, None)],
}
SEED_APPROVED_NOTE = "승인됨 · 8차 적용(dictionary_add 결정 레코드 · 사용자 2026-11-06 「부위는 일단 추가 해야하는게 맞지」 · 성분 6 = 17 중 성분인 것 · 11 은 기계 오추출로 버림(코디 판단 · 표에 보임)) — ERD 사전 값 아님 · parent 는 v3.2-4 계층"
SITE_CLOSED = list(V32.SITE_CLOSED) + [(v, k, p, []) for v, k, p, _ in SITE_ADDED_V33]
_st = _ent("site")
_st["definition"] += " v3.3(V3.3-C(2)): 조직층 혈관 아래 **동맥 · 정맥 · 안동맥(parent 동맥)** 을 사전 값으로(사용자 승인 2026-11-06 · kind layer · parent 로 계층) — 부작용 단위의 부위 칸(「동맥 폐색」→ (폐색, 동맥))."
_st["attrs"] = [a if a[0] != "parent" else ("parent", "SIT-|null", False, [], (a[4] or "") + " · v3.3(V3.3-C): 동맥·정맥 → 혈관 · 안동맥 → 동맥(값 있음) · 그 밖은 null(승인 씨앗 parent 는 8차 결정 레코드)") for a in _st["attrs"]]
_a = _ent("adverse_effect")
_a["definition"] += " v3.3(V3.3-C): 사건 사전 값 자체에도 R2 — 「혈관 폐색」은 사건 폐색 + 부위 혈관(§1.5 R2_DICT_RULE) · 폐색 ≠ 색전 · R30 후보는 제안(§9.20)."
_r31 = _rel("R31")
_r31["note"] = (_r31["note"] or "") + " · v3.3(V3.3-C): layer 값에 동맥·정맥·안동맥(parent 계층) — (폐색, 혈관)·(폐색, 동맥)·(폐색, 안동맥)은 다른 단위"
_r30 = _rel("R30")
_r30["note"] = (_r30["note"] or "") + " · v3.3(V3.3-C(3)): 후보 색전 → 폐색 · 폐색 → 괴사 는 원장 문구 근거와 함께 §9.20 에 제안만(edge_create 는 사용자 · 엣지 0)"
TUPLE_RULES["adverse"]["r2_dictionary"] = R2_DICT_RULE
TUPLE_RULES["adverse"]["event_decomposed_v33"] = [{"old": a, "event": b, "site": c, "synonyms": d, "basis": e} for a, b, c, d, e in EVENT_DECOMPOSED_V33]
TUPLE_RULES["adverse"]["occlusion_embolism"] = OCCLUSION_EMBOLISM_RULE
TUPLE_RULES["adverse"]["r30_candidate_rules"] = [{"from": a, "to": b, "from_words": c, "to_words": d} for a, b, c, d in R30_CANDIDATE_RULES]
TUPLE_RULES["site_closed"] = {"rule": V32.SITE_DICT_RULE + " v3.3(V3.3-C(2)): 동맥·정맥·안동맥 추가(사전 값 · parent).", "values": [{"value": v, "kind": k, "parent": p, "synonym_candidates": s} for v, k, p, s in SITE_CLOSED]}
TUPLE_RULES["seed"] = dict(TUPLE_RULES["seed"])
TUPLE_RULES["seed"]["approved_v33"] = {"note": SEED_APPROVED_NOTE, "site": [{"value": v, "kind": k, "parent": p} for v, k, p in SEED_APPROVED_V33["site"]], "ingredient_material": [{"value": v} for v, _, _ in SEED_APPROVED_V33["ingredient_material"]]}

# ---------------------------------------------------------------------------
# V3.3-D 접미사 ~감·~증·~형성 = 표기 꼴
# ---------------------------------------------------------------------------
SUFFIX_VARIANT_RULE = ("**접미사 표기 꼴(V3.3-D · 사용자 2026-11-06 「형성은 같은거고 … 둘다 증상아니야 ?」→「응 같다고 하자」)**: 사건 말에 **~감 · ~증 · ~형성** 이 붙은 꼴은 같은 사건의 **표기 꼴**이다 — 대표 이름(정준값)은 **현상 이름**(건조·경결·흉터·색전·자반·가피·수포·결절·반흔·경화·경직·마비·박탈·자극·통증·화상·따가움)이고 접미 꼴은 동의어(표기 변형)로 내려가며 원문은 문구 사전 raw_variants 에 그대로 남는다. "
                       "이것은 사전 값 변경이므로 ERD 가 값을 고치지 않는다 — 드라이런 3차 §3.6 의 **쌍 20 은 fold_approve 결정 레코드**(⑦ 닫기 · 8차 적용 · 사전 쪽이 접미 꼴인 쌍(자극감 ↔ 자극)은 canonical_rename 도 함께 · §9.22 표). 접미사가 아닌 3쌍(압통감 ↔ 통증 · 저림감 ↔ 감각 이상 · 가려움증 ↔ 소양감)은 임상 동치라 사용자가 따로 본다(「사용자 결정 필요」). "
                       "⑦ strong 규칙의 「감각」(「감각 ↔ X」)은 사용자 결정에 없으므로 표기 꼴이 아니라 ⑦ 후보 그대로. 새로 나오는 접미 쌍도 규칙으로 자동 접지 않는다 — ⑦ strong 후보로 올라와 fold_approve 로 닫는다(규칙 단위 승인은 이번 20 쌍까지).")
SUFFIX_VARIANTS = ["감", "증", "형성"]
CANONICAL_PHENOMENON_NAMES = ["건조", "경결", "흉터", "색전", "자반", "가피", "수포", "결절", "반흔", "경화", "경직", "마비", "박탈", "자극", "통증", "화상", "따가움"]   # 사용자 2026-11-06 · HANDOFF 「11-06 밤」
SUFFIX_PAIRS_V33 = [
    # (a, b, 규칙, 대표 이름(현상) · 사용자 목록, 결정) — dryrun3 §3.6 23 쌍 중 접미사 20
    ("건조감", "건조", "suffix_감", "건조", "fold_approve"), ("흉터형성", "흉터", "suffix_형성", "흉터", "fold_approve"), ("경결감", "경결", "suffix_감", "경결", "fold_approve"), ("따가움감", "따가움", "suffix_감", "따가움", "fold_approve"),
    ("가피형성", "가피", "suffix_형성", "가피", "fold_approve"), ("자극감", "자극", "suffix_감", "자극", "fold_approve + canonical_rename(사전 정준값 자극감 → 자극)"), ("경화감", "경화", "suffix_감", "경화", "fold_approve"), ("건조증", "건조", "suffix_증", "건조", "fold_approve"),
    ("표정 경직감", "표정 경직", "suffix_감", "경직(표정 경직은 수식어 표정 + 경직)", "fold_approve"), ("결절감", "결절", "suffix_감", "결절", "fold_approve"), ("경직감", "경직", "suffix_감", "경직", "fold_approve"), ("마비감", "마비", "suffix_감", "마비", "fold_approve"),
    ("박탈감", "박탈", "suffix_감", "박탈", "fold_approve"), ("색전증", "색전", "suffix_증", "색전", "fold_approve"), ("수포형성", "수포", "suffix_형성", "수포", "fold_approve"), ("자반증", "자반", "suffix_증", "자반", "fold_approve"),
    ("통증감", "통증", "suffix_감", "통증", "fold_approve"), ("화상감", "화상", "suffix_감", "화상", "fold_approve"), ("결절형성", "결절", "suffix_형성", "결절", "fold_approve"), ("반흔형성", "반흔", "suffix_형성", "반흔", "fold_approve"),
]
NON_SUFFIX_PAIRS_V33 = [("압통감", "통증"), ("저림감", "감각 이상"), ("가려움증", "소양감")]   # 접미사 아님(임상 동치) — 사용자
TUPLE_RULES["phrase_kinds"]["suffix_variant_rule"] = SUFFIX_VARIANT_RULE
TUPLE_RULES["phrase_kinds"]["spelling_variant_suffixes"] = SUFFIX_VARIANTS
TUPLE_RULES["phrase_kinds"]["canonical_phenomenon_names"] = CANONICAL_PHENOMENON_NAMES
TUPLE_RULES["phrase_kinds"]["suffix_pairs_v33"] = [{"a": a, "b": b, "rule": r, "canonical": c, "decision": d} for a, b, r, c, d in SUFFIX_PAIRS_V33]
TUPLE_RULES["phrase_kinds"]["non_suffix_pairs_user"] = [{"a": a, "b": b} for a, b in NON_SUFFIX_PAIRS_V33]
TUPLE_RULES["phrase_kinds"]["dup_rules"] = {"strong": ["paren_pair(원장 병기 X(Y))", "suffix_감|증|형성(표기 꼴 · V3.3-D · 닫기는 fold_approve)", "suffix_감각(⑦ 후보 · 사용자 결정 없음)", "word_contains(짧은 쪽이 긴 쪽의 낱말)", "jamo1"], "weak(표시만 · 기본 게이트 아님)": ["substring", "prefix≥2", "first_syllable(둘 다 2자 이하)"]}
NORMALIZE_RULE["v3_3"] = {"name": "norm_v3", "steps": list(V32.NORM_V2["steps"]) + ["(d) 접미사 표기 꼴(V3.3-D): X+감·증·형성 ↔ X 는 같은 사건의 표기 꼴 — 값은 결정(fold_approve · canonical_rename)으로만 바뀐다 · 자동 적용 0"], "note": V32.NORM_V2["note"] + " (d) 는 판정 규칙이지 자동 접기가 아니다."}

# ---------------------------------------------------------------------------
# V3.3-E adverse_event_type.category 삭제
# ---------------------------------------------------------------------------
CATEGORY_DELETE_RULE = ("**사건 사전 category 삭제(V3.3-E · 사용자 2026-11-06 「묶음 라벨이 필요한거야 ? 왜 만드냐고」)**: adverse_event_type 의 7분류(국소 일시 반응 · 염증/감염 · 혈관 · 신경 · 색소 · 구조/이물 · 전신)는 원장 21 파일에 **0회** — ERD v2 발주서가 지어 넣은 라벨(사용자 지시 아님 · 이름부터 틀림: 1달 가는 통증도 「일시 반응」). 사전 항목의 `category`·`category_review` · 결정 kind dictionary_add·event_split 의 new_value `category` · 단위 레코드의 `event_category` · 보고서의 「분류」 열을 전부 뺀다(§9.23 전수 표). "
                        "부작용의 분류는 **원장 값만** — complications `severity`(mild~critical · R15 속성) · taxonomy/extracted safety 칸(common / uncommon / serious · R15 frequency_class) · 엣지 경과(R15 course). 게이트의 「노드별 종류」 질문도 없어진다.")
CATEGORY_TOUCHED_V33 = [
    # (산출물 · 자리 · v3.2 수(실측이 센다) · 처리)
    ("erd-v3.2-dictionaries.json", "adverse_event_type.entries[].category · category_review", "entries 302 · category_review 40", "v3.3 사전에서 키 삭제(ERD 값 40 · 파생 262 전부)"),
    ("erd-v3.2-tuples.json", "adverse.tuples[].event_category", "단위 328", "v3.3 실측 레코드에서 키 삭제"),
    ("erd-v3.2.json", "decision_kinds dictionary_add.new_value 「category: str|null」 · event_split.new_value 「category」", "kind 2", "v3.3 kind 정의에서 category 삭제(kind 수 20 그대로)"),
    ("erd-v3.2.md §5", "결정 kind 표 new_value 열", "행 2", "v3.3 §5 표에서 빠짐"),
    ("erd_spec_v2.py", "주석 「category ∈ {국소 일시 반응 …}」 · 사건 사전 초기값 (canonical, category, synonyms) 튜플", "v2 발주서 창작 — 원천", "이전 판 파일은 손대지 않음(보존) · 원천 기록"),
    ("erd-v2.3 ~ v3.1 tuples/md", "complications_by_category · tuples_by_category · adv_folded.category · §9 「분류」 열", "이전 판", "보존(판 이력) · v3.3 산출물에는 없음"),
    ("silver-v3/lib/adverse31.py · decompose.py", "ids.event[*].category · 단위 rec.event_category · adv_folded.category · *_by_category 집계", "lib 참조 자리 10(읽기만 · e.get 이라 키 없으면 None)", "실버 빌더 8차 개정 몫(ERD 범위 밖 · 목록만)"),
    ("silver-v3/out/gate", "「노드별 종류 묻기」 질문", "HANDOFF 11-06", "질문 자체가 없어짐(사용자)"),
    ("adverse_effect 개체 속성", "event_category", "v3.2 §2.14 속성 표에 없음(0)", "변경 없음 — 발주서가 든 「adverse_effect.attrs.event_category」는 실측 레코드 키였다"),
]
DECISION_KINDS = [list(x) for x in DECISION_KINDS]
for x in DECISION_KINDS:
    if x[0] == "dictionary_add":
        x[3] = "obj(canonical: str, synonyms: str[], kind: str|null — site 는 kind·parent · person_condition 은 kind)"
        x[4] = x[4] + ". v3.3(V3.3-E): new_value 의 category 삭제(원장 출처 0) · v3.3(V3.3-C): site 는 parent 를 받는다(승인 씨앗 15 · 8차)"
    if x[0] == "event_split":
        x[3] = "obj(new_events: obj[](canonical, synonyms[]))"
        x[4] = x[4] + ". v3.3(V3.3-E): new_events 의 category 삭제"
    if x[0] == "fold_approve":
        x[4] = x[4] + ". v3.3(V3.3-D): 접미사 표기 꼴 쌍 20 을 이 kind 로 닫는다(대표 = 현상 이름 · 사전 쪽이 접미 꼴이면 canonical_rename 과 함께)"
    if x[0] == "canonical_rename":
        x[4] = x[4] + ". v3.3(V3.3-G): 「이름 교체 + 부위 분리」는 이 kind 로 되지 않는다(글자만 바꿈 · 부위 칸 인자 없음) — §5 G 검토 · 조합 절차 문장"
DECISION_KINDS = [tuple(x) for x in DECISION_KINDS]
DECISION_KINDS_NOTE_V33 = {"dictionary_add": "V3.3-E category 삭제 · V3.3-C site parent", "event_split": "V3.3-E category 삭제", "fold_approve": "V3.3-D 접미사 쌍 20", "canonical_rename": "V3.3-G 조합 절차"}
TUPLE_RULES["adverse"]["category_deleted"] = CATEGORY_DELETE_RULE
TUPLE_RULES["adverse"]["classification_from_ledger_only"] = ["complications.json:categories[].complications[].severity → R15.severity(dict:severity)", "taxonomy/extracted safety.common|uncommon|serious → R15.frequency_class(dict:frequency_class)", "R15.course(dict:course)"]

# ---------------------------------------------------------------------------
# V3.3-F 「무엇을·어떻게 세분」 묶음 — 설계안만(적용 0)
# ---------------------------------------------------------------------------
F_BUNDLE_RULE = ("**「무엇을·어떻게 세분」 묶음(V3.3-F · 설계안만 · 결정은 사용자)**: 지금 ERD 에 자리가 없어 ⑨ 미해결 또는 수식어로 떨어지는 값 넷 — 성분(필러 HA · 필링 산 · v3.2 ingredient what 있음) · 소모품(V3.3-A 구조만) · 실 재질/형태(M7 하위분류 재질별 PDO·PCL / 형태별 코그·모노·볼륨실 / 브랜드 — 한 시술이 셋을 동시에 가짐 · 지금 what 하나만) · **깊이·세기**(심부 필링 · 얕은 필링 · HA 필러(딥) · 필링(약한 산) · 케미컬 필링(중간 깊이) · 저출력 IPL/Nd:YAG/피코토닝 — 수식어로 버리면 심부/얕은 필링 튜플이 같아져 금기 엣지가 섞임). "
                 "선택지 셋을 원장 근거(§9.24 실측)와 영향 수치와 함께 §9.24 표로 둔다 — **어느 안도 적용하지 않았다**(개체·속성·사전 값 추가 0 · 사용자 결정 필요 표).")
F_OPTIONS_V33 = [
    # (안, 구조, 바뀌는 자리, 장점, 단점 · 열린 질문) — 영향 수치는 실측(§9.24)이 채운다
    ("F-1 what 복합 키", "procedure.what 을 (what_id, spec) 복합 키로 — spec = {ingredient, component, material, shape, depth, intensity} 중 있는 것(사전 값) · 없으면 빈 칸 · 식별자 PRC-sha256(what_id|spec|site|technique)", "procedure 식별자 · R27 · 접힘 조건(spec 까지 같아야 접힘) · what 사전 6개(spec 칸마다 닫힌 사전)", "튜플 하나로 끝(엣지 끝 불변) · 심부/얕은 필링이 다른 튜플", "식별자가 바뀜(PRC- 전부 재계산 · alias) · spec 칸마다 사전·승인 필요 · 「미상이면 접지 않음」이 spec 칸까지 커진다"),
    ("F-2 technique 에 depth·intensity 속성", "깊이·세기만 technique 축의 속성(technique.depth · technique.intensity · 닫힌 사전) · 성분·소모품·실 재질/형태는 what 축(ingredient what · component what · 실은 재질/형태 둘 중 하나만 what)", "technique 개체 속성 2 · 사전 2(depth · intensity) · 실 재질/형태 중 하나는 여전히 수식어", "식별자 불변(기법 칸 안) · 바꾸는 자리가 작다", "실의 재질·형태 동시 표현은 못 함 · technique=none 인 튜플(지금 100%)에 깊이만 있는 경우 기법 칸이 「none + depth」가 된다"),
    ("F-3 별도 세분 개체", "procedure_spec 개체(PRS- · procedure → spec 1:N · kind ∈ ingredient|component|material|shape|depth|intensity · value = 사전 값 · locator) · 튜플 세 칸은 그대로 · 접힘은 spec 집합까지 같을 때만", "개체 1 · 관계 1(R37 has_spec) · 사전 kind 별", "세 칸 정의 1 불변 · 한 시술이 재질·형태·브랜드를 동시에 가짐 · 값 추가가 사전·결정으로 닫힘", "엣지 끝이 「튜플 + spec 집합」이 되어 R15 금기 엣지가 spec 를 봐야 함 · 개체 하나 더"),
]
F_DEPTH_WORDS = ["심부", "딥", "얕은", "약한", "중간 깊이", "저출력", "중간"]   # 발주서 명시 6종 자리 + dryrun 성분 씨앗의 깊이·세기 값 — 실측이 라벨 자리를 센다
F_THREAD_WORDS = ["PDO", "PCL", "PLLA", "코그", "모노", "볼륨실", "실"]
TUPLE_RULES["f_bundle"] = {"rule": F_BUNDLE_RULE, "options": [{"option": a, "structure": b, "changes": c, "pros": d, "cons": e} for a, b, c, d, e in F_OPTIONS_V33], "applied": None, "depth_words": F_DEPTH_WORDS, "thread_words": F_THREAD_WORDS}

# ---------------------------------------------------------------------------
# V3.3-G 원장 3판 · 결정 kind 검토
# ---------------------------------------------------------------------------
LEDGER3_RULE = ("**원장 3판(V3.3-G · 사용자 2026-11-06 · `bronze/phub-ledger/CHANGELOG.md` 3)**: synergy from/to 줄임말 18종 59자리 → taxonomy 정식 이름(「Mxx-」 접두 제거 · 부위가 붙으면 「이름 부위」) · taxonomy M8›기타 항목 2 신설(「저출력레이저(LLLT)」「다이오드 레이저」 · name 만) · README 규칙 2(synergy 는 taxonomy 정식 이름 그대로 · 없으면 taxonomy 에 먼저 세운다). "
                "ERD: 분류 항목 521 → 523 · synergy 노드 라벨은 §1.3 분해에서 「Mxx-」 접두 없이 바로 정식 이름에 닿는다(남은 「Mxx-」 접두 자리는 4판 후보 · 사용자 답 대기). 실측 전부 3판으로 재생성(§9 · v3.2 2판 열과 나란히). 2판은 `bronze/phub-ledger-v2/` 에 보존(v3.2 검산 재실행용).")
G_KIND_ASSESSMENT = ("**「사전 값 이름 교체 + 부위 분리」 결정 kind 검토(V3.3-G · dryrun3 §8 「dictionary_add + canonical_rename 조합은 미검증」)**: 사실 — canonical_rename 은 정준값 글자만 바꾸고 부위 칸 인자가 없다 · 사전 통째 일치가 먼저라 「혈관 폐색」이 값(정준값·동의어)으로 남아 있는 한 부위가 서지 않는다 · dictionary_add(site) 는 부위 값만 더한다. "
                     "판정: **새 kind 는 만들지 않는다.** 이유 — (1) 띄어 쓴 「부위 말 + 사건 말」 꼴은 v3.3 부터 ERD 규칙(R2_DICT_RULE)이 적재 때 가르므로 결정이 필요 없다(이번 1 값 「혈관 폐색」은 ERD 개정으로 반영 · 실측 §9.20 이 (폐색, 혈관) 단위를 센다 — 조합 결과는 추정이 아니라 실측). "
                     "(2) 남는 자리는 붙은 꼴 2(정맥염·혈관외유출)뿐이고 사용자가 「분해」로 정하면 조합 절차로 닫힌다 — **조합 절차**: ① dictionary_add(site · 부위 말 · parent) → ① canonical_rename(adverse_event_type · 「X Y」→「Y」 · old_as_synonym=false · 옛 DIC- id alias) → 빌드 재분해에서 「X Y」 글자가 부위 X + 사건 Y 로 갈린다(§1.5 원칙 C 같은 멤버) → 검산 「옛 값이 어느 사전 표면형에도 없음 · (Y, X) 단위 있음」. "
                     "사용자가 「분해 안 함」으로 정하면 결정 0. 둘 다 같은 kind 둘로 되므로 kind 수는 20 그대로 — 조합을 한 레코드로 묶는 것은 적용 순서 ① 안의 같은 자리라 원자성 문제가 없다(둘 다 approved 여야 빌드가 읽는다). 새 kind 가 필요해지는 조건은 「부위 말이 사전 밖이면서 동시에 여러 사전 값을 한 번에 가를 때」인데 지금 그런 자리는 0 이다.")
TUPLE_RULES["bronze"] = {"version": BRONZE_VERSION, "dir": "bronze/phub-ledger", "hashes": "bronze/phub-ledger/HASHES.txt", "changelog": "bronze/phub-ledger/CHANGELOG.md", "previous_dir": "bronze/phub-ledger-v2", "diff_from_v2": "synergy from/to 줄임말 18종 59자리 → 정식 이름 · taxonomy M8-6 항목 2 신설 · README 규칙 2"}
TUPLE_RULES["bronze_version"] = BRONZE_VERSION
RESOLVE_RULES["bronze"] = dict(TUPLE_RULES["bronze"])
TUPLE_RULES["g_kind_assessment"] = G_KIND_ASSESSMENT
TUPLE_RULES["ledger3"] = LEDGER3_RULE

# ---------------------------------------------------------------------------
# 「사용자 결정 필요」 — A~G 안에서 애매한 것(빈 자리로 둔다 · 추측으로 메우지 않는다)
# ---------------------------------------------------------------------------
USER_DECISIONS_NEEDED = [
    # (항목, 어디서 나왔나, 선택지(있으면), 결정)
    ("「정맥염」 분해 여부", "V3.3-C(1) · dryrun3 §3.3 N3 #21 — 붙은 꼴(정맥 + 염) · 「염」이 단독 사건 말인지 애매", "분해 안 함(정맥염 유지) / 분해((염, 정맥)) / 다른 사건 말로", ""),
    ("「혈관외유출」 분해 여부", "V3.3-C(1) · dryrun3 §3.3 N3 #24 — 붙은 꼴(혈관 + 외유출)", "분해 안 함(혈관외유출 유지) / 분해((외유출, 혈관))", ""),
    ("접미사 아닌 3쌍 — 압통감 ↔ 통증 · 저림감 ↔ 감각 이상 · 가려움증 ↔ 소양감", "V3.3-D · dryrun3 §3.6 #23 #18 #5 — 임상 동치(접미사 규칙 밖)", "같다(fold_approve) / 다르다(conflict_close not_same) / 쌍마다", ""),
    ("⑦ strong 규칙의 「감각」 접미(「X감각 ↔ X」)", "V3.3-D — 사용자 결정은 감·증·형성 셋 · 「감각」은 v3.2 규칙에만 있음", "표기 꼴에 넣는다 / ⑦ 후보 그대로(기본값 · 지금 ERD)", ""),
    ("접미 꼴 단독 정준값 4 — 열감 · 당김감 · 작열감 · 소양감(쌍 없음)", "V3.3-D 「대표 이름 = 현상 이름」을 쌍 없는 사전 값에도 적용하나", "그대로 둠(기본값 · 지금 ERD) / canonical_rename(열·당김·작열·소양)", ""),
    ("성분 씨앗 17 중 버린 11(LED · 심부 · 딥 · 얕은 · 약한 · 주입 · 동일 · 별도 · 부자연스러운 · 자연스러운 · 코그)", "V3.3-C(4) — 코디 판단 「기계 오추출 · 기본값 버림」 · 심부·딥·얕은·약한 4 는 F 묶음의 깊이·세기 값", "버림 확정 / 깊이·세기 4 는 F 결정 뒤", ""),
    ("「무엇을·어떻게 세분」 묶음 — F-1 / F-2 / F-3 / 보류", "V3.3-F · §9.24 설계안 표(원장 근거 · 영향 수치)", "F-1 what 복합 키 / F-2 technique 속성 / F-3 별도 개체 / 보류(⑨ 유지)", ""),
    ("구성품 종류 라벨(팁·카트리지·핸드피스·트랜스듀서 …)의 열거형", "V3.3-A — 원장 칸 없음 · 값 0 · 열거형을 지금 정하면 창작", "원장 칸 생길 때 그 값 / 지금 정함", ""),
    ("synergy 「Mxx-」 접두 34종 171자리 통일(원장 4판 후보)", "V3.3-G · HANDOFF 「남은 원장 수정(4판 후보)」 · 사용자 답 대기", "4판에서 통일 / 그대로", ""),
    ("R30 후보 색전 → 폐색 · 폐색 → 괴사(edge_create)", "V3.3-C(3) · §9.20 원장 문구 근거 — 제안만", "edge_create approved / 보류", ""),
]

# ---------------------------------------------------------------------------
# 변경 목록 · 사용자 정의 관계
# ---------------------------------------------------------------------------
USER_DEFINITIONS_V33_NOTE = ("v3.3 은 사용자 정의 1·2·3 · 명시 예외 · 원칙 A~D 의 글자를 바꾸지 않는다(소개정). 바뀌는 것은 사용자 결정 A~G(2026-11-06)뿐 — 구성품 구조(값 0) · 토큰화 규칙 문장(목록 → 형태소 분석기) · 사건 사전 값에도 R2(「혈관 폐색」1 값 · 부위 3 값 · 폐색 ≠ 색전) · 접미사 표기 꼴 규칙 · category 삭제 · 세분 묶음 설계안(적용 0) · 원장 3판 실측. "
                             "v3.3 은 **A~G 밖의 개체·속성·사전 값·분류를 새로 만들지 않았다** — 애매한 것은 §12 「사용자 결정 필요」 표에 빈 자리로 있다. 사전 값·속성마다 원장 출처(파일·키·locator)를 실측으로 붙였고(§4 provenance), 출처가 없는 v3.2 값은 §4 「출처 없는 값」 표에 전수로 적었다(삭제는 사용자).")
CHANGE_LIST_V33 = [
    ("V3.3-A", "제품 구성품(소모품) 구조 — product.kind · component_of · component_kind · R36 component_of · what_kind component · 값 0(원장 칸 없음 · 미래 칸)", "§1.4 · §2 product·procedure · R27 · R36 · 열거형 product.kind·what_kind · column-map 미래 칸 3 · 실측 §9.18", "A"),
    ("V3.3-B", "토큰화 = 형태소 분석기(kiwipiepy 0.24 판 고정 · 사전 값 사용자 단어) — 핵심어·문장꼴·수식어·괄호·서술 규칙 · v3.2 목록은 분석기 보조 목록", "§1.3 · resolve_rules.tokenize(rule·analyzer·list_role) · phrase_kinds.list_role · 실측 §9.19", "B"),
    ("V3.3-C", "R2 를 사건 사전 값에도(혈관 폐색 → 폐색 + 혈관) · 부위 동맥·정맥·안동맥 · 폐색 ≠ 색전 · R30 후보 제안 · 승인 씨앗 부위 15·성분 6 = 결정 레코드(8차)", "§1.5 · §2 site·adverse_effect · R30·R31 · 사전 adverse_event_type(1 값) · site(+3) · tuple_rules.adverse.r2_dictionary · seed.approved_v33 · 실측 §9.20 · §9.21", "C"),
    ("V3.3-D", "접미사 ~감·~증·~형성 = 표기 꼴 · 대표 = 현상 이름 · 쌍 20 fold_approve · 3쌍 사용자 · 「감각」은 ⑦ 그대로", "§1.1 norm_v3(d) · §1.5 · phrase_kinds.suffix_* · dup_rules · fold_approve 비고 · 실측 §9.22", "D"),
    ("V3.3-E", "adverse_event_type.category 삭제 — 사전·결정 kind·실측 레코드·보고서 · 분류는 원장 값만", "§1.5 · §4 · §5 dictionary_add·event_split · 사전 키 삭제 · 실측 event_category 삭제 · 전수 표 §9.23", "E"),
    ("V3.3-F", "「무엇을·어떻게 세분」 묶음 설계안 3(F-1 복합 키 · F-2 technique 속성 · F-3 별도 개체) — 원장 근거·영향 수치 · 적용 0", "§1.4 · tuple_rules.f_bundle · 실측 §9.24 · 사용자 결정 필요", "F"),
    ("V3.3-G", "원장 3판(synergy 정식 이름 · M8-6 항목 2 · 분류 항목 523) · 실측 재생성 · 「이름 교체 + 부위 분리」 kind 불필요(조합 절차 문장)", "§1 · §5 G 검토 · tuple_rules.bronze · 실측 §9 전부 · §9.25", "G"),
]
