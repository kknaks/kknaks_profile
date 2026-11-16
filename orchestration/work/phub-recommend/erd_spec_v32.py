# -*- coding: utf-8 -*-
"""ERD v3.2 명세 (데이터). erd_spec_v31.py(v3.1 · 동결)를 읽어 발주서 erd-v3.2-brief.md 6건(V3.2-1~6) + 코디·사용자 추가(V3.2-0 문구 종류 분류·부작용 노드 원칙 · V3.2-7 메모 분리 · V3.2-8 R15 상속 · V3.2-9 타임라인 개체 · 2026-11-05)만 덧씌운다.
  V3.2-0 §0 첫 규칙 — 원장 문구는 먼저 「어느 테이블 것인가」로 가른다. 부작용 단위에는 부작용 문구(complications 이름 · safety.*)만 붙고, 나머지(타임라인 줄 · 응급 징후 줄 · 고지 · 금기 · 문헌·환자 설명)는 자기 테이블에서 부작용 단위를 참조만 한다.
         부작용 축 노드 원칙 교체(사용자 「경결감이 있으면 새 노드로」) — 부작용 문구의 사건이 사전에 없으면 그 멤버의 핵심어가 새 사건 값(origin=ledger · status=unreviewed)이 된다 · 기존 사건과 표기가 비슷하면 ⑦ duplicate_candidate · 접기는 fold_approve · unlinked 상태 없음 · raw_name 단위 없음.
  V3.2-1 토큰화 · V3.2-2 표기 변형 · V3.2-3 씨앗 규칙 · V3.2-4 부위 닫힌 목록 · V3.2-5 장비 = 제품 자동 등록 · V3.2-6 성분 what · V3.2-7 부작용 문구 종류 판정 · V3.2-8 R15 3층 상속 · V3.2-9 post_procedure_timeline · emergency_sign.
사용자 정의 1·3 유지 · 정의 2 는 v3.1 개정판 유지(단위 세 칸) · 원칙 A·D 문장을 V3.2-0 로 고친다(사용자 결정). 원장 21 = 브론즈 2판. erd_build_v32.py · erd-v3.2-tuples.py 가 읽는다. v3.1 명세는 손대지 않는다.
"""
import copy
import os
import sys
import types

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import erd_spec_v31 as V31  # noqa

for _k, _v in vars(V31).items():
    if _k.startswith("_") or isinstance(_v, types.ModuleType):
        continue
    globals()[_k] = _v

ERD_VERSION = "v3.2"
PREVIOUS_VERSION = "v3.1"
ENTITIES = copy.deepcopy(V31.ENTITIES)
RELATIONS = copy.deepcopy(V31.RELATIONS)
RESOLVE_RULES = copy.deepcopy(V31.RESOLVE_RULES)
TUPLE_RULES = copy.deepcopy(V31.TUPLE_RULES)
ERD_ENUMS = copy.deepcopy(V31.ERD_ENUMS)
ID_RULE = copy.deepcopy(V31.ID_RULE)
NORMALIZE_RULE = copy.deepcopy(V31.NORMALIZE_RULE)
DECISION_KINDS = [list(x) for x in V31.DECISION_KINDS]

# ---------------------------------------------------------------------------
# V3.2-1 토큰화 — 조사 · 용언 어미 · 문법 낱말 (한국어 닫힌 부류 중 원장 전수에서 실제로 떼어진 것만 · 0 적중 원소는 뺐다)
# ---------------------------------------------------------------------------
PARTICLES = ["에서는", "에서", "으로", "부터", "까지", "보다", "에게", "에는", "에도", "와의", "이나", "이며", "이고", "이", "가", "을", "를", "은", "는", "의", "에", "로", "와", "과", "도", "만", "나"]
VERB_ENDINGS = ["합니다", "됩니다", "하며", "되며", "하는", "되는", "하여", "되어", "하면", "하게", "되지", "시킬", "할", "될", "한", "된", "함", "됨"]
GRAMMAR_WORDS = ["있으며", "있는", "있을", "있고", "있어", "있으나", "있으면", "없이", "없습니다", "인해", "의해", "비해", "대한", "위해", "따른", "않음", "않으며", "않는", "않았습니다", "합니다", "후에"]
STEM_MIN_LEN = 2
RELAXED_SUFFIXES = ["에서", "으로", "이", "가", "을", "를", "의", "에", "시"]   # 검토 S-4: 어간이 한글 2자 이상이면 독립 토큰 확인 없이 뗀다(거부반응이 · 접촉시) — 은·는·도·와·과·로·만·나 는 명사 꼴과 겹쳐 뺐다(피부과 · 민감도 · 마이크로)
CONJ_PARTICLES = ["와", "과", "이나", "나", "와의"]   # 검토 S-1: 접속 조사가 붙은 토큰 뒤는 토막 경계(「홍조와 부종」→ 홍조 | 부종)
PREDICATE_ENDINGS = ["는", "된", "운", "지고", "하게", "하므로", "되며"]   # 검토 S-4: 용언 꼴(관형형 · 연결형) — 보존(predicate) · 핵심어는 다른 조각이 없을 때만          # 원장 독립 토큰으로만 확인된 어간은 2자 이상(사전 값·수식어·문법 낱말은 1자도)

# ---------------------------------------------------------------------------
# V3.2-7 부작용 문구 종류 판정 — 메모 어휘 · 설명문 문턱 (원장 전수 실측에서 · 바깥 묶음 토큰 기준)
# ---------------------------------------------------------------------------
NOTE_WORDS = ["정상", "유지", "소실", "발현", "여부", "자료", "부족", "불충분", "충분하지", "터치업", "근거", "연구", "증거", "임상", "금기", "금지", "보유자", "상담",
              "권장", "만족스럽지만", "불만족스러운", "효과", "결과", "차이", "사람마다", "개인차", "안전성", "안전한", "필요", "교정", "중단", "평가", "규격화", "모니터링", "확인"]
SENTENCE_MIN_TOKENS = 7
SENTENCE_MIN_GRAMMAR = 3
SENTENCE_LATIN_RATIO = 0.8
CORE_EXCLUDE = ["이하", "미만", "이내", "초과", "포함", "약", "기저"]   # 핵심어에서 빼는 한정·근사 낱말(보존 · parsed.explanation)
FALLBACK_CORE = ["약화", "악화", "감소", "증가", "변화", "저하", "상승"]
DUP_PREFIX_MIN = 2

# ---------------------------------------------------------------------------
# V3.2-5 장비 = 제품 자동 등록 — 장비 계열 + 기타 장비 하위분류 · 제외 규칙
# ---------------------------------------------------------------------------
EQUIP_FAMILIES = ["M8", "M9", "M10", "M11", "M13", "M14"]
EQUIP_EXTRA_SUBCATS = [("M12-1", "수동 MTS 기구"), ("M12-2", "전동 MTS 기기"), ("M15-3", "광치료(LED) 기기"), ("M15-4", "초음파관리 기기"), ("M15-6", "주입장비(하위분류 이름이 장비)"), ("auto-M15-1775360912", "물광/메조건(주입 기기)")]
EQUIP_EXCLUDE_SUBCAT_WORDS = ["프로그램"]            # 하위분류 라벨에 이 말이 있으면 장비가 아니라 시술 묶음(M9-SIG 시그니처 프로그램)
EQUIP_EXCLUDE_NAME_WORDS = ["토닝", "필링", "관리", "프로그램", "주사"]   # 항목 이름에 들어가면 장비명이 아니라 시술명 — 항목 자신 유지(후보 표에 남김)
ABBREV_MIN_LEN = 2                                   # 줄임말 접두 규칙 — 짧은 쪽 정규화 길이 하한

# ---------------------------------------------------------------------------
# V3.2-4 부위 닫힌 목록 — (값, kind, parent, 동의어 후보) · 기존 값은 그대로(parent 만 제안) · 원장 locator 는 실측이 센다(0 이면 「원장에 없음」)
# ---------------------------------------------------------------------------
SITE_CLOSED = [
    ("얼굴", "region", None, []), ("이마", "anatomical", "얼굴", []), ("미간", "anatomical", "얼굴", []), ("관자놀이", "anatomical", "얼굴", []), ("눈가", "anatomical", "얼굴", []), ("눈 주변", "anatomical", "얼굴", []),
    ("눈밑", "anatomical", "눈가", ["눈 밑"]), ("눈꺼풀", "anatomical", "눈가", ["윗눈꺼풀", "안검"]), ("코", "anatomical", "얼굴", []), ("코끝", "anatomical", "코", ["코 끝"]),
    ("팔자주름", "anatomical", "얼굴", ["팔자"]), ("볼", "anatomical", "얼굴", []), ("광대", "anatomical", "얼굴", []), ("턱", "anatomical", "얼굴", ["턱 끝", "턱끝"]), ("턱선", "anatomical", "얼굴", []), ("사각턱", "anatomical", "턱", []),
    ("입술", "anatomical", "얼굴", []), ("목", "anatomical", None, []), ("목주름", "anatomical", "목", []), ("이중턱/턱밑", "anatomical", "턱", ["이중턱", "턱밑"]), ("승모근", "anatomical", "바디 전체", []),
    ("얼굴 전체", "region", "얼굴", ["전체얼굴", "풀페이스", "full face"]),
    ("바디 전체", "region", None, ["바디", "전신", "body"]), ("복부", "anatomical", "바디 전체", ["배", "뱃살"]), ("옆구리", "anatomical", "바디 전체", ["러브핸들"]), ("팔뚝", "anatomical", "바디 전체", ["팔"]),
    ("허벅지", "anatomical", "바디 전체", []), ("종아리", "anatomical", "바디 전체", []), ("힙", "anatomical", "바디 전체", ["엉덩이"]), ("등", "anatomical", "바디 전체", ["등살"]), ("가슴", "anatomical", "바디 전체", []),
    ("겨드랑이", "anatomical", "바디 전체", ["액와"]), ("손", "anatomical", "바디 전체", ["손등"]), ("발", "anatomical", "바디 전체", []),
    ("두피", "region", None, []),
    ("피부", "layer", None, []), ("피하 지방층", "layer", None, []), ("근육", "layer", None, []), ("혈관", "layer", None, []), ("점막", "layer", None, []),
    ("주사 부위", "relative", None, []), ("시술 부위", "relative", None, []),
]

# ---------------------------------------------------------------------------
# V3.2-6 성분 — 문맥 낱말(같은 라벨에 있으면 성분 후보) · 발주서 명시 필링 산 · 실 재질 · 필러 성분
# ---------------------------------------------------------------------------
INGREDIENT_CONTEXT_WORDS = ["필링", "필", "필러", "실", "리프팅실", "스레드"]   # 조각의 바로 앞·뒤 토큰이 이 말이면 성분 후보
INGREDIENT_NAMED = ["TCA", "글리콜산", "살리실산", "페놀", "젖산", "락틱산", "만델릭산", "제스너", "HA", "히알루론산", "PLLA", "PCL", "CaHA", "PDO", "PDLLA", "PN", "PDRN", "보툴리눔톡신"]

# ---------------------------------------------------------------------------
# §0 — 사용자 정의 · 첫 규칙(V3.2-0) · 원칙 A·D 개정
# ---------------------------------------------------------------------------
RULE_ZERO = ("**§0 첫 규칙(V3.2-0 · 사용자 2026-11-05 「왜 미연결을 억지로 붙이려 하냐」)**: 원장 문구는 먼저 **「어느 테이블 것인가」**로 분류하고, 부작용 단위에는 **부작용 문구만** 붙인다. 나머지는 자기 테이블로 정규화한 뒤 부작용·조건을 **참조만** 한다(단위를 세우지 않는다). "
             "「미연결(unlinked)」 집계는 부작용 문구 종류에서만 세고(v3.2 에서는 0 — 아래 노드 원칙), 다른 종류는 각자 테이블의 「참조 성공 / 없음」으로 센다. 문구 사전(phrase_dictionary)은 부작용 문구 종류에만 적용하고, 다른 테이블의 줄은 자기 parsed 속성을 가진다.")
PHRASE_KIND_TABLE = [
    ("부작용 이름·문구", "complications 이름 · extracted/taxonomy(계열·항목·제품) safety.common/uncommon/serious/emergency/long_term/common_adverse_effects/serious_adverse_effects/common_side_effects", "부작용 단위 + R15 + 문구 사전", "붙임(단위 생성·연결 · 사전에 없으면 원장 사건 노드)"),
    ("시술 후 경과", "post-procedure-timeline timelines[].phases[].normal/abnormal/caution/emergency[]", "post_procedure_timeline(V3.2-9)", "줄이 참조(adverse_ref · R34) · 정상 줄은 참조 없으면 경과 메모"),
    ("동의서", "consent-checklist mandatory_disclosures · contraindications · emergency_signs", "clinical_rule(disclosure) · person_condition · emergency_sign(V3.2-0)", "참조(adverse_ref · R35) · 금기는 조건 축"),
    ("시술 전 확인", "pre-procedure-checklist universal_checks · category_specific checks", "person_condition(kind=check · v3.1 구조 그대로)", "참조 없음(조건 축 · R16)"),
    ("메모·설명문·문헌·환자 설명", "safety 안의 메모/설명문(V3.2-7) · literature adverse_effects · patient_*", "문구 사전 메모 항목(status note|sentence) · evidence_statement(kind=adverse_effects)", "참조(adverse_ref) 또는 없음 · 단위 general_description"),
]
NODE_RULE = ("**부작용 축 노드 원칙(V3.2-0 · 사용자 2026-11-05 「경결감이 있으면 새 노드로 만들면 되잖아」 · 검토 S-1 반영 · 시술 축과 대칭)**: 부작용 문구(complications 이름 · safety.*)의 멤버를 **접속 조사(와·과·이나·나)가 붙은 토큰 뒤에서 토막**으로 나누고 토막마다 — "
             "(1) **사전 사건이 닿으면 그 사건에 exact 로 붙인다**(부위·경과·물질은 원칙 C 그대로 · 한 토막에 사건이 둘이면 단위 둘 · 원칙 B). 그 토막의 남은 미등록 토큰은 단위 칸이 아니라 **side**(문구 사전 parsed.side · 보존 · 노드 후보 목록)로 둔다 — 「시술 후 일시적인 홍조와 부종」→ 홍조 | 부종 → 부종 exact + 홍조 new · 「이식 부위의 약간의 부종」→ 부종 exact + side[이식, 부위]. "
             "(2) **사전 사건이 0 인 토막만** 핵심어(미등록 토큰 + 대체 핵심어 수식어(약화·악화·감소·증가·변화·저하·상승) · 원문 순서 · 그것도 없으면 용언 꼴(predicate))를 **새 사건 값**으로 세운다 — adverse_event_type 의 항목(origin=ledger · status=unreviewed · id = DIC-sha256(adverse_event_type|핵심어) · 출처 = 그 핵심어가 나온 locator 전부 · 설명 = 원장 문맥(문구 원문 · 계열 · 빈도 등급 · severity)). "
             "조사·어미·문법 낱말(V3.2-1) · 수식어(V3.1-8) · 부위·상대 부위·경과·물질 · gloss · 핵심어 제외 낱말(이하·미만·이내·초과·포함·약·기저) · 한글 문구 안의 라틴 문자만인 토큰 · 기호는 핵심어에 들지 않는다. 핵심어의 정규화형이 사전 사건 표면형과 같으면 그 사건(exact). "
             "괄호 안 묶음은 사건 조각이 하나라도 있을 때만(사건 나열) 같은 규칙, 아니면 설명(parsed.explanation · 보존). 핵심어는 바탕 분해(사전 그대로)에서 결정론으로 정해지므로 문구 순서와 무관하다. 그래서 「같은 세 칸은 어느 출처든 같은 단위」(정의 2)가 지켜진다 — 사전 사건은 새 노드에 흡수되지 않는다. "
             "**⑦ duplicate_candidate(검토 S-2)는 노드끼리만** — 원장 사건 노드 ↔ 사전 사건(정준값·동의어) · 원장 노드 ↔ 원장 노드(문구 ↔ 노드 쌍은 ⑦ 이 아니다). 표기 규칙의 등급: **strong**(기본 게이트) = 원장 병기 「X(Y)」 · 「X+감·증·형성·감각 ↔ X」 · 짧은 쪽이 긴 쪽의 낱말 · 자모 1 치환 / **weak**(표시만 · 기본 게이트에 올리지 않음) = 낱말 경계 없는 부분 문자열(「반응 ↔ 이물반응」) · 공통 접두 2자 이상 · 첫 음절이 같은 2자 이하. stable_key duplicate_candidate|adverse_event_type|가|나 · 접기는 fold_approve · 유사도 점수·추정 매칭 없음. "
             "부작용 축에는 미연결 상태와 이름 단위(옛 raw_name)가 없다 — 모든 부작용 문구는 기존 단위에 exact 로 붙거나 새 단위를 세운다(new). 다른 테이블의 줄은 원장 사건 노드를 포함한 **이미 있는 단위만** 가리킨다(refer · 세우지 않음 · 사건 옆 토큰은 미등록으로 남아 ref_partial).")
OPEN_CLOSED_RULE = ("**사전 열림/닫힘(V3.2-3 · 사용자 2026-11-05)**: 열린 사전 중 **원장 칸이 종류를 선언한 것**은 원장 어휘가 곧 씨앗이라 자동으로 세운다 — 사건(부작용 문구 칸 · 위 노드 원칙) · 장비 제품(장비 계열·하위분류의 taxonomy 항목 · V3.2-5). "
                    "닫힌 사전(부위·조직층 = site · 상대 부위 · 경과 · 물질 = adverse_qualifier)은 승인 절차를 유지한다 — kind·계층·경과 구분은 임상 해석이라 원장 어휘가 바로 값이 되지 않는다. 성분은 열린 사전이지만 원장이 성분 칸으로 선언한 곳(products.json ingredient/material)은 이미 사전이고 그 밖은 라벨의 문맥(바로 옆 토큰 필링·필러·실)으로 **추정**해야 하므로 승인 묶음으로 둔다(「아이 필러」의 아이). 시술 조각(종류 추정 규칙 밖)도 승인 묶음.")
CLOSED_DICTIONARIES = {"site": True, "relative_site": True, "course": True, "adverse_qualifier": True, "adverse_event_type": False, "ingredient_material": False, "product_name": False}
USER_DEFINITIONS_V32_NOTE = ("v3.2 는 사용자 정의 1·3 의 뜻을 바꾸지 않고, 정의 2 는 v3.1 개정판(단위 = 사건·부위·물질 · 경과는 엣지 · 표현은 가리키기만)을 그대로 쓴다. 바뀌는 것은 원칙 A·D 의 문장(사용자 결정 2026-11-05): 미등록 조각이 있는 부작용 이름·문구는 raw_name/unlinked 가 아니라 **핵심어 새 사건 값**이 되고, 그 값이 사전 값이므로 「미등록 조각이 섞인 단위를 만들지 않는다」(원칙 D)는 그대로 성립한다. "
                             "§0 에 첫 규칙(문구 종류 분류)을 둔다 — 「표현은 가리키기만」을 테이블 단위로 넓힌 것이다. 정의 3 의 결정 kind 는 20 그대로(fold_approve·edge_create 비고만).")
PRINCIPLES = [(k, v) for k, v in V31.PRINCIPLES]
PRINCIPLES = [("A", "부작용 이름·문구의 토막에 사전 사건이 있으면 그 사건에 exact 로 붙고(옆 미등록 토큰은 side 보존), **사전 사건이 0 인 토막만 그 핵심어를 새 사건 값(origin=ledger · unreviewed)으로 세운다** — 사전 사건은 새 노드에 흡수되지 않는다 · 노드끼리 표기가 비슷하면 ⑦ duplicate_candidate(strong/weak) · 접기는 fold_approve(추정 매칭 0 · v3.2 V3.2-0 · 검토 S-1/S-2)") if k == "A" else
              ("D", "표현(원장 문구)은 단위를 **가리키기만** 한다 — 단위는 부작용 문구 종류(이름 · safety.*)만 세우고, 그 칸은 전부 사전 값(원장 사건 값 포함)이다. 다른 테이블의 줄은 이미 있는 단위만 참조한다(V3.2-0).") if k == "D" else (k, v) for k, v in PRINCIPLES]
PRINCIPLES_TEXT = " · ".join(f"{k}. {v}" for k, v in PRINCIPLES)

# ---------------------------------------------------------------------------
# V3.2-1 토큰화 · V3.2-2 정규화(norm_v2) · V3.2-7 · V3.2-8 · V3.2-9 규칙 문장
# ---------------------------------------------------------------------------
TOKENIZE_RULE = ("**토큰화(V3.2-1 · resolve_rules.tokenize · 검토 S-4 보강)**: 보강 — (가) relaxed_suffixes(에서·으로·이·가·을·를·의·에·「~시」): 어간이 원장 독립 토큰이 아니어도 한글 2자 이상이면 뗀다(「거부반응이」·「접촉시」 · 은·는·도·와·과·로·만·나 는 명사 꼴 「피부과·민감도·마이크로」와 겹쳐 빼고 독립 토큰 확인을 유지) (나) predicate_endings(관형형·연결형 -는·-된·-운·-지고·-하게·-하므로·-되며 · 원장에서 실제로 걸린 것만): 그 꼴로 끝나는 미등록 토큰은 용언 꼴(predicate · 보존) — 핵심어에는 다른 조각이 없을 때만 든다 (다) 접속 조사(와·과·이나·나·와의)는 부작용 멤버의 토막 경계(S-1). 원소마다 원장 locator 를 센다. 본래 규칙: 분해(시술 §1.3·§1.4 · 부작용 §1.5 · 조건 §1.6)에서 사전에 통째로 닿지 않은 토큰은 차례로 — 수식어(V3.1-8)·stopword(V3-3)·표지어(V3.1-4) → 문법 낱말(grammar_words · 있으며·합니다·인해 …) → 조사(particles)·용언 어미(verb_endings · 하다/되다 활용) 떼기 → 미등록. "
                 "떼기는 가장 긴 접미부터이며 **어간이 사전 값·수식어·문법 낱말이거나 원장 전체 어휘의 독립 토큰(2자 이상)일 때만** 뗀다(「효과」의 과 · 「농도」의 도 · 「깊이」의 이 같은 오분리 방지). 떼어낸 어간은 다시 사전에 대어 보고(조사 제거 뒤 재일치 · V3.2-2c), 마지막 토큰의 조사를 뗀 여러 토큰 구간도 사전에 댄다(「주사 부위가」→ 주사 부위). "
                 "사전 값으로의 통째 일치가 언제나 먼저다(V3-6 · V3.1-6). 떼어낸 조사·어미·문법 낱말은 버리지 않고 **grammar_tokens[]**(부작용 문구 사전 parsed.grammar · 시술 참조 grammar_tokens · 조건 멤버 grammar)로 보존한다(원칙 B). 목록은 원장 전수 실측에서 왔고 원소마다 locator 를 센다(§9.11 · locator 0 원소는 검산 FAIL).")
NORM_V2 = {"name": "norm_v2", "steps": ["norm_v1(NFKC · casefold · 공백 제거)", "(a) 병기 괄호: 괄호 하나가 바로 앞 토큰에 붙고 괄호 안이 멤버 하나·숫자 없음·한글만↔라틴만이면 병기 — 사전에 닿은 쪽이 있고 다른 쪽이 라틴 문자만이면 라틴 쪽은 조각이 아니라 gloss(보존) · 아니면 둘 다 그대로 + 쌍은 후보", "(b) 자모 변형 쌍: 원장 전체 어휘(어간)에서 같은 자리 자모 하나 치환(편집거리 1)인 쌍을 목록으로 — 승인되면 사전 동의어(dictionary_add) · 자동 적용 0", "(c) 조사·어미 제거 뒤 재일치(V3.2-1)"],
           "note": "norm_v2 는 「같은 것」 판정 규칙이다 — (a)(c) 는 결정론 규칙으로 분해에 적용되고 (b) 는 목록 승인 뒤에만 사전으로 들어간다. 유사도 점수·추측 매칭은 여전히 없다."}
PHRASE_KIND_RULE = ("**부작용 문구 종류 판정(V3.2-7 · tuple_rules.phrase_kinds)**: 부작용 문구 칸(safety.*)에 있어도 부작용이 아닌 문구가 있다. 바탕 분해(사전 그대로)로 차례로 판정한다 — "
                    "(1) exact: 사건이 있고 사전 밖 토큰 0 → 그대로 · (2) **not_adverse_note**(status=note): 사건 조각 0 이고 바깥 묶음에 메모 어휘(note_words · 정상·유지·소실·발현·여부·자료·부족·금기·금지·상담 …)가 있거나, 사건 0·핵심어 0 · "
                    "(3) **explanatory_sentence**(status=sentence): 바깥 멤버 하나의 토큰 ≥ sentence_min_tokens 이거나 바깥 문법 토큰 ≥ sentence_min_grammar 이거나 라틴 문자 비율 ≥ sentence_latin_ratio · (4) 그 밖 new(핵심어 노드). "
                    "메모·설명문은 **unlinked 로 세지 않고** 별도 집계(메모 N · 설명문 N)로 두며 원문·locator 는 문구 사전 메모 항목(memo_phrases)에 보존한다 — 설명문은 phrase_map 대상(사람 지정). phrase_shape 값에 not_adverse_note · explanatory_sentence 를 더한다. 타임라인 normal 은 V3.2-9 타임라인 줄(참조 · 정상 메모)로 간다.")
INHERIT_RULE = ("**R15 속성 상속(V3.2-8 · 사용자 「시술에 부종이 붙는데 부종에 대한 정보가 없다」)**: 세 층 — ① 부작용 단위 자체의 일반 정보: `general_description`(그 단위를 참조하는 문헌 adverse_effects evidence_statement id·locator) · `general_management`(그 단위로 접힌 complications 이름들의 management locator) · ② 계열 → 단위 R15(complications 표 행)의 severity·incidence·onset·duration·mechanism·management·prevention·risk_factors · ③ 항목/제품 → 단위 R15 는 항목 고유 값(safety 문구 parsed · frequency_class)만. "
                "조회 규칙: 항목·제품 엣지에 값이 없으면 같은 계열(R2/R4 로 올라간 계열 코드)의 계열 엣지 값을, 거기도 없으면 단위 일반값을 **참조**하고 속성마다 `basis: item|family|unit|none` 과 `ref`(참조 대상 R15 키 또는 단위 속성) · `ref_locator` 를 단다. **값을 복사하지 않는다**(원장 불변 · provenance 는 참조 대상 locator) — 실버 레코드에는 참조만, 골드에서 펼친다. 실측 §9.15.")
TIMELINE_RULE = ("**post_procedure_timeline(V3.2-9 · 사용자 「타임라인 테이블이 필요한 영역 아니냐」)**: post-procedure-timeline.json timelines[](id · category · name — 끝은 R33 has_timeline: proc_axis → timeline, 이름이 튜플로 해결되면 그 튜플 · 아니면 계열) → phases[](period · label · 순서) → 줄(reaction_level normal|abnormal|caution|emergency · 원문 · locator · parsed · adverse_ref[] · ref_status ref|ref_partial|none|normal_memo). "
                 "줄은 V3.2-0 refer 로 분해해 **이미 있는** 부작용 단위에 닿으면 참조(R34 timeline_refers: 줄 → adverse_effect · 속성 reaction_level · period · phase_label), 정상 줄이 닿지 않으면 경과 메모(normal_memo · 원문 보존). R15 는 타임라인 줄을 출처로 「계열 → 단위」 엣지에 timeline_refs[] 를 **참조로** 얻는다 — v3.1 의 R15 period · phase_label · reaction_level 속성은 이 참조로 대체된다. 타임라인 문구는 문구 사전에 들지 않는다. 골드 「시술 후 안내」는 이 개체를 그대로 쓴다.")
SIGN_RULE = ("**emergency_sign(V3.2-0 · 「응급 징후도 타임라인 줄처럼 자기 자리」)**: consent-checklist categories[].emergency_signs[] — 정규화 문장 하나가 레코드(SGN- · 같은 문장 여러 계열이면 modality_codes 여럿) · parsed · adverse_ref[] · ref_status. R35 sign_refers: emergency_sign → adverse_effect(참조). R15 「계열 → 단위」 엣지는 emergency_sign_refs[] 를 참조로 얻는다. 단위를 세우지 않는다.")
DISCLOSURE_RULE_V32 = ("**필수 고지(V3.1-7 · v3.2 V3.2-0)**: clinical_rule(kind=disclosure) + R32(basis=ledger) 는 v3.1 그대로. v3.1 의 「같은 문장을 문구 사전(kind=disclosure)으로도 두어 단위에 닿는다」는 **삭제** — 고지는 자기 테이블(clinical_rule)의 parsed · adverse_ref[] · ref_status 로 단위를 참조만 한다(phrase_ids 속성 대신 adverse_ref).")
LITERATURE_RULE = ("**문헌 adverse_effects(V3.2-0)**: v3.1 의 문구 사전 항목이 아니라 **evidence_statement(kind=adverse_effects)** 레코드 — statement · patient_text(ko·en·zh·ja) · accuracy · R19 cites · R20(계열 → 근거). statement 와 patient_ko 를 refer 로 분해해 닿은 단위를 adverse_ref[] 로 가리키고, 그 단위의 general_description 이 이 레코드를 참조한다(V3.2-8 ①).")
SEED_RULE = ("**사전 씨앗 규칙(V3.2-3 · §1.7)**: 사전 초기값은 특정 파일이 아니라 **원장 전체 어휘**(분해하는 문자열 자리 전부 — 부작용 이름·문구 · 타임라인 · 동의서 · 문헌 · 조건 · 시술 라벨)에서 온다. 조각(규칙 적용 뒤 미등록 토큰)을 뽑고 **어느 칸(key path)에서 나왔는지로 종류**를 정한다 — "
             "부작용 문구 칸 → 사건(열림 · 원장 칸 선언 → **자동** · 위 노드 원칙) / 장비 계열·하위분류 항목 → 장비 제품(열림 · **자동** · V3.2-5) / 부위 닫힌 목록 값·동의어 → 부위(닫힘 · 승인) / 라벨에서 바로 옆 토큰이 필링·필러·실 이거나 발주서 명시 성분 → 성분(추정 · 승인) / 그 밖 시술 라벨 조각 → 시술 조각(사전 선택 · 승인) / 제품 이름과 접두 관계 → 줄임말·옛 이름(승인). "
             "승인 묶음은 빈도 ≥2 또는 locator ≥2 인 것만 proposed(그 밖은 「빈도 1」) · 출처 locator 전부 · 추천 종류 · 사전마다 닫힘 여부. 승인된 씨앗이 결정 dictionary_add 로 사전 값이 된다(적용 0 · `erd-v3.2-seed-candidates.json/.md`).")
SITE_DICT_RULE = ("**부위 사전 전수(V3.2-4)**: 닫힌 목록 = 얼굴 세부(이마·미간·관자놀이·눈가·눈 주변·눈밑·눈꺼풀·코·코끝·팔자주름(팔자)·볼·광대·턱·턱선·사각턱·입술·목·목주름·이중턱/턱밑) · 바디(복부·옆구리·팔뚝·허벅지·종아리·힙·등·가슴·겨드랑이·손·발·승모근) · 두피 · 전체(얼굴 전체·바디 전체) · 조직층 5 · 상대 2. "
                  "값마다 kind(anatomical·region·layer·relative) · **parent**(계층 · 눈밑 ⊂ 눈가 ⊂ 얼굴 · 몸 부위 ⊂ 바디 전체) · 원장 locator(토큰 열 일치 · 조사 뗀 꼴 포함) · 동의어 후보(전체얼굴·풀페이스 → 얼굴 전체 …). site 사전 항목에 `parent` 필드를 두고(v3.1 값은 null · 제안은 씨앗 묶음) 값 추가는 승인으로만. 「등」처럼 수식어·문법 낱말과 꼴이 같은 값은 동형어 — 자리 수는 상한(확인 필요).")
EQUIP_RULE = ("**장비 = 제품 자동 등록(V3.2-5)**: 장비 계열(M8·M9·M10·M11·M13·M14) + 기타 장비 하위분류(M12-1·M12-2·M15-3·M15-4·M15-6·물광/메조건)의 taxonomy 항목 이름은 제품(장비) 값이다 — product_name 사전 항목(origin=taxonomy · status=unreviewed · license_status=미확인 · code=계열 · 같은 이름은 합침)으로 **자동 등록**. "
              "제외: 하위분류 라벨에 「프로그램」(시술 묶음) · 이름에 토닝·필링·관리·프로그램·주사(시술명) · 이미 계열/하위분류/제품/기법 사전 값. 그래서 「항목 자신이 시술」(catalog_item what)이던 장비 항목은 §1.4 what 규칙(자기 이름은 분류 항목 색인에서 빼고 제품 사전에 닿으면 product)으로 **product 로 승격**된다. "
              "줄임말·옛 이름은 「정식명이 줄임말을 접두로 포함」(또는 반대) 규칙으로 후보를 뽑아 승인 묶음으로(써마지→써마지FLX · 인모드FX→인모드 · 자동 아님) · 자동 장비 제품이 기존 제품과 접두로 닿으면 ⑦ duplicate_candidate.")
INGREDIENT_RULE = ("**성분 what(V3.2-6 · §1.4)**: 시술 분해 사전에 ingredient_material(성분)을 더한다(primary 다음 순서 · 통째 일치 우선). 한 라벨에 다른 primary(계열·하위분류·제품·분류 항목)가 있으면 성분 조각은 ingredient_fragments(보존 · 칸 아님), 없으면 **what = 성분**(what_kind=ingredient · what_id = 성분 사전 항목 DIC- · 접힘 가능한 사전 what) — 「TCA 필링」= (성분 TCA, 부위, 기법)(TCA 승인 · 필링 → 기법 topical 동의어 승인 뒤). "
                   "성분 씨앗: 필링 산(TCA·글리콜산·살리실산·페놀·젖산·만델릭산·제스너) · 필러 성분(HA·히알루론산 …) · 실 재질 · 원장 전수 locator. 톡신 단위(U)는 성분이 아니라 규격(spec·unit 사전).")

# ---------------------------------------------------------------------------
# 개체 — 20 + post_procedure_timeline + emergency_sign = 22
# ---------------------------------------------------------------------------
def _ent(key):
    return next(e for e in ENTITIES if e["key"] == key)


_a = _ent("adverse_effect")
_a["definition"] = _a["definition"] + " v3.2(V3.2-0): 사건 칸은 사전 값 — ERD 사건 사전 또는 **원장 사건 노드**(adverse_event_type 항목 origin=ledger · status=unreviewed · 부작용 문구의 핵심어). raw_name 단위는 없다(이름·문구에 미등록 조각이 있으면 핵심어 사건). 단위를 세우는 것은 부작용 문구 종류(이름 · safety.*)뿐. v3.2(V3.2-8): general_description · general_management(참조)."
_a["attrs"] = [a for a in _a["attrs"] if a[0] not in ("dict_tuples", "raw_reason", "candidate_name", "anchor")]
_a["attrs"] = [a if a[0] != "event_kind" else ("event_kind", "enum(dict|ledger)", True, [], "v3.2: dict = ERD 사건 사전 값 · ledger = 원장 사건 노드(핵심어 · unreviewed · ⑦ 후보는 conflict)") for a in _a["attrs"]]
_a["attrs"] += [("event_origin_locators", "str[]", False, [], "v3.2: event_kind=ledger 일 때 그 사건 값이 나온 원장 locator 전부(사전 항목 sources 와 같다)"),
                ("general_description", "obj[](ref EVS-, locator)", False, ["literature-evidence.json:categories.{code}.adverse_effects[].statement"], "v3.2(V3.2-8 ①): 이 단위를 참조하는 문헌 adverse_effects 근거 문장 — 참조만(값 복사 없음)"),
                ("general_management", "obj[](ref R15 키, locator)", False, ["complications.json:categories[].complications[].management"], "v3.2(V3.2-8 ①): 이 단위로 접힌 complications 이름들의 management locator — 참조만")]
_cr = _ent("clinical_rule")
_cr["attrs"] = [a for a in _cr["attrs"] if a[0] != "phrase_ids"] + [("parsed", "obj|null", False, [], "v3.2(V3.2-0): disclosure 문장의 분해 조각(사건·부위·수식어·문법 · 자기 속성)"),
                                                                    ("adverse_ref", "str[]|null", False, [], "v3.2(V3.2-0): disclosure 가 참조하는 부작용 단위 ADV- (이미 있는 것만 · 세우지 않는다) · v3.1 phrase_ids 대체"),
                                                                    ("ref_status", "enum(ref|ref_partial|none)|null", False, [], "v3.2: disclosure 참조 결과")]
_cr["definition"] += " " + DISCLOSURE_RULE_V32
_ev = _ent("evidence_statement")
_ev["definition"] += " " + LITERATURE_RULE
_ev["attrs"] = [a if a[0] != "kind" else ("kind", "enum(moa|effect|adverse_effects)", True, [], "v3.2: adverse_effects 추가(V3.2-0)") for a in _ev["attrs"]]
_ev["attrs"] = [(n, t, r, list(src) + ([f"literature-evidence.json:categories.{{code}}.adverse_effects[].{n if n != 'patient_text' else 'patient_ko'}"] if n in ("statement", "accuracy_score", "accuracy_note", "added_at", "patient_text") else []) + (["literature-evidence.json:categories.{code}.adverse_effects[].patient_en", "literature-evidence.json:categories.{code}.adverse_effects[].patient_zh", "literature-evidence.json:categories.{code}.adverse_effects[].patient_ja"] if n == "patient_text" else []), note) for n, t, r, src, note in _ev["attrs"]]
_ev["attrs"] += [("adverse_ref", "str[]|null", False, [], "v3.2(V3.2-0): kind=adverse_effects 의 statement·patient_ko 가 참조하는 부작용 단위"), ("ref_status", "enum(ref|ref_partial|none)|null", False, [], "v3.2")]
_pr = _ent("product")
_pr["attrs"] = [a if a[0] != "origin" else ("origin", "enum(ledger|survey|taxonomy)", True, a[3], (a[4] or "") + " · v3.2(V3.2-5): taxonomy = 장비 계열 항목 이름에서 자동 등록(status=unreviewed · license_status=미확인)") for a in _pr["attrs"]]
_pr["definition"] += " " + EQUIP_RULE
_pc = _ent("procedure")
_pc["attrs"] = [a if a[0] != "what_kind" else ("what_kind", "enum(modality|modality_subcategory|product|catalog_item|ingredient)", True, a[3], (a[4] or "") + " · v3.2(V3.2-6): ingredient = 성분 사전 값(primary 가 없을 때)") for a in _pc["attrs"]]
_pc["attrs"].append(("ingredient_fragments", "str[]", False, [], "v3.2(V3.2-6): primary 가 있는 라벨의 성분 조각(보존 · 칸 아님)"))
_pc["attrs"].append(("grammar_tokens", "str[]", False, [], "v3.2(V3.2-1): 떼어낸 조사·어미·문법 낱말(보존)"))
_st = _ent("site")
_st["attrs"].append(("parent", "SIT-|null", False, [], "v3.2(V3.2-4): 부위 계층(눈밑 ⊂ 눈가 ⊂ 얼굴) — 사전 site 항목 parent · 값은 승인(씨앗 묶음)"))
_st["definition"] += " " + SITE_DICT_RULE
ENTITIES.append({"key": "post_procedure_timeline", "prefix": "TML", "label": "시술 후 경과 타임라인", "beyond_minimum": False, "aliases": "없음",
                 "definition": TIMELINE_RULE, "identity": "TML-sha256(timelines[].id)[:10]",
                 "attrs": [("ledger_id", "str", True, ["post-procedure-timeline.json:timelines[].id"], "원장 id(botox …)"),
                           ("name", "str", True, ["post-procedure-timeline.json:timelines[].name"], "시술명 원문 — R33 끝은 §1.3 분해 결과"),
                           ("category", "str", True, ["post-procedure-timeline.json:timelines[].category"], "계열 코드(M16-DCA 는 하위분류)"),
                           ("phases", "obj[](order, period, label, lines[])", True, ["post-procedure-timeline.json:timelines[].phases[].period", "post-procedure-timeline.json:timelines[].phases[].label"], "단계 — period(dict:period) · label(dict:phase_label) · 순서"),
                           ("lines", "obj[](reaction_level, text, locator, parsed, adverse_ref[], ref_status)", True, ["post-procedure-timeline.json:timelines[].phases[].normal[]", "post-procedure-timeline.json:timelines[].phases[].abnormal[]", "post-procedure-timeline.json:timelines[].phases[].caution[]", "post-procedure-timeline.json:timelines[].phases[].emergency[]"], "단계마다의 줄 — reaction_level(dict:reaction_level) · adverse_ref 는 참조만(세우지 않음) · ref_status ref|ref_partial|none|normal_memo")]})
ENTITIES.append({"key": "emergency_sign", "prefix": "SGN", "label": "응급 징후", "beyond_minimum": False, "aliases": "없음",
                 "definition": SIGN_RULE, "identity": "SGN-sha256(정규화 문장)[:10]",
                 "attrs": [("text", "str", True, ["consent-checklist.json:categories[].emergency_signs[]"], "원문(첫 표면형)"),
                           ("modality_codes", "str[]", True, ["consent-checklist.json:categories[].id"], "그 문장이 놓인 계열 전부"),
                           ("locators", "str[]", True, [], "원장 자리 전부"),
                           ("parsed", "obj", True, [], "분해 조각(자기 속성)"),
                           ("adverse_ref", "str[]", True, [], "참조하는 부작용 단위(이미 있는 것만)"),
                           ("ref_status", "enum(ref|ref_partial|none)", True, [], "")]})
_d = _ent("decision")
_d["definition"] += " v3.2: kind 20 그대로 — fold_approve 가 원장 사건 노드(⑦ duplicate_candidate)를 기존 사건으로 접는 것을 받는다(새 값을 기존 값의 동의어로)."

# ---------------------------------------------------------------------------
# 관계 — 31 + R33 + R34 + R35 = 34
# ---------------------------------------------------------------------------
def _rel(rid):
    return next(r for r in RELATIONS if r["id"] == rid)


_r15 = _rel("R15")
_r15["attrs"] = [a for a in _r15["attrs"] if a[0] not in ("period", "phase_label", "reaction_level", "disclosure")] + [
    ("timeline_refs", "str[]", "v3.2(V3.2-9): 이 엣지를 낸 타임라인 줄 locator(참조) — v3.1 period·phase_label·reaction_level 속성 대체(값은 줄에)"),
    ("emergency_sign_refs", "str[]", "v3.2(V3.2-0): 이 엣지를 낸 emergency_sign SGN- (참조)"),
    ("inheritance", "obj[](attr, basis item|family|unit|none, ref, ref_locator)", "v3.2(V3.2-8): 속성마다 값이 어디서 오는지 — 참조만 · 값 복사 금지"),
    ("layer", "enum(family|item)", "v3.2(V3.2-8): family = 계열 출발(complications 표 행 · 계열 safety · 타임라인 · 응급) · item = 분류 항목·제품 출발")]
_r15["sources"] = [s for s in _r15["sources"] if not s.startswith("post-procedure-timeline.json:timelines[].phases[]") and s not in ("consent-checklist.json:categories[].emergency_signs[]", "consent-checklist.json:categories[].mandatory_disclosures[]", "literature-evidence.json:categories.{code}.adverse_effects[].statement", "literature-evidence.json:categories.{code}.adverse_effects[].patient_ko")]
_r15["note"] = (_r15["note"] or "") + " · v3.2(V3.2-0): 엣지를 내는 것은 complications 이름(계열) · 부작용 문구(safety.* · 항목·제품·계열) · 타임라인 줄 참조(R34 → 계열) · 응급 징후 참조(R35 → 계열). 고지·문헌은 엣지를 내지 않는다(참조 속성). " + INHERIT_RULE
_r20 = _rel("R20")
_r20["note"] = "코드 키로 확정. v3.2(V3.2-0): evidence_statement kind=adverse_effects 도 끝이다(문헌 adverse_effects 문장)"
_r20["sources"] = list(_r20["sources"])
_r19 = _rel("R19")
_r19["note"] = "v3.2(V3.2-0): 문헌 adverse_effects 의 인용도 evidence_statement(kind=adverse_effects) → citation"
RELATIONS.append({"id": "R33", "name": "has_timeline", "from": "proc_axis", "to": "post_procedure_timeline", "card": "N:1", "attrs": [("target_depth", "enum(modality|subcategory|procedure)", "끝의 깊이 — 타임라인 이름이 튜플로 해결되면 procedure · 아니면 category 계열")],
                  "sources": ["post-procedure-timeline.json:timelines[].category", "post-procedure-timeline.json:timelines[].name"], "note": "v3.2(V3.2-9): " + TIMELINE_RULE})
RELATIONS.append({"id": "R34", "name": "timeline_refers", "from": "post_procedure_timeline", "to": "adverse_effect", "card": "N:M", "attrs": [("line_locator", "str", "줄 locator"), ("reaction_level", "dict:reaction_level", ""), ("period", "dict:period", ""), ("phase_label", "dict:phase_label", "")],
                  "sources": ["post-procedure-timeline.json:timelines[].phases[].normal[]", "post-procedure-timeline.json:timelines[].phases[].abnormal[]", "post-procedure-timeline.json:timelines[].phases[].caution[]", "post-procedure-timeline.json:timelines[].phases[].emergency[]"], "note": "v3.2(V3.2-9): 줄 → 이미 있는 단위(참조만)"})
RELATIONS.append({"id": "R35", "name": "sign_refers", "from": "emergency_sign", "to": "adverse_effect", "card": "N:M", "attrs": [],
                  "sources": ["consent-checklist.json:categories[].emergency_signs[]"], "note": "v3.2(V3.2-0): " + SIGN_RULE})
PROC_AXIS_EDGES = list(V31.PROC_AXIS_EDGES) + ["R33"]

# ---------------------------------------------------------------------------
# 결정 kind(20 그대로 · 비고) · 열거형 · 식별자
# ---------------------------------------------------------------------------
for x in DECISION_KINDS:
    if x[0] == "fold_approve":
        x[4] = x[4] + ". v3.2(V3.2-0): target 이 사전 값 쌍(dictionary=adverse_event_type, canonical=원장 사건 노드 · into=기존 사건)이면 원장 노드를 기존 사건의 동의어로 접는다(⑦ duplicate_candidate 를 닫는다 · 단위 id 는 기존 사건 기준으로 재계산 · 옛 id alias)"
    if x[0] == "adverse_tuple_assign":
        x[4] = x[4] + ". v3.2(V3.2-0): raw_name 단위가 없어졌으므로 대상 = 이름 locator 의 단위 지정(핵심어 노드 대신 사람이 고른 단위) · v3.1 의 raw_name 대상 결정은 같은 locator 로 닿는다"
    if x[0] == "phrase_map":
        x[4] = x[4] + ". v3.2(V3.2-7): 대상은 부작용 문구 사전 항목(설명문 sentence 포함) — 다른 테이블의 줄은 문구 사전이 아니다"
DECISION_KINDS = [tuple(x) for x in DECISION_KINDS]
DECISION_KINDS_NOTE_V32 = {"fold_approve": "V3.2-0 원장 사건 노드 접기", "adverse_tuple_assign": "V3.2-0 이름·문구 자리 지정(옛 이름 단위 없음)", "phrase_map": "V3.2-7 메모·설명문"}
ERD_ENUMS["adverse_effect.event_kind"] = ["dict", "ledger"]
ERD_ENUMS["phrase_dictionary.status"] = ["exact", "new", "approved", "note", "sentence"]
ERD_ENUMS["adverse_expression.match_status"] = list(ERD_ENUMS["phrase_dictionary.status"])
ERD_ENUMS["phrase_dictionary.kind"] = ["safety_phrase"]
ERD_ENUMS["phrase_dictionary.phrase_shape"] = list(ERD_ENUMS["phrase_dictionary.phrase_shape"]) + ["not_adverse_note", "explanatory_sentence"]
ERD_ENUMS["phrase_dictionary.fragment_class"] = list(ERD_ENUMS["phrase_dictionary.fragment_class"]) + ["grammar", "gloss", "core"]
ERD_ENUMS["procedure.what_kind"] = ["modality", "modality_subcategory", "product", "catalog_item", "ingredient"]
ERD_ENUMS["product.origin"] = ["ledger", "survey", "taxonomy"]
ERD_ENUMS["evidence_statement.kind"] = ["moa", "effect", "adverse_effects"]
ERD_ENUMS["reference.ref_status"] = ["ref", "ref_partial", "none", "normal_memo"]
ERD_ENUMS["R15.inheritance.basis"] = ["item", "family", "unit", "none"]
ERD_ENUMS["R15.layer"] = ["family", "item"]
ERD_ENUMS["dictionary.entry_origin"] = ["erd", "ledger", "taxonomy"]
ERD_ENUMS["dictionary.entry_status"] = ["approved", "unreviewed"]
ERD_ENUMS["tokenize.kind"] = ["particle", "ending", "word"]
ERD_ENUMS["phrase_kind"] = [k for k, *_ in PHRASE_KIND_TABLE]
ID_RULE["adverse_effect"] = ID_RULE["adverse_effect"] + " · v3.2(V3.2-0): event_id 는 ERD 사건 또는 원장 사건 노드(DIC-sha256(adverse_event_type|핵심어))의 사전 id — raw_name(RAW:) 식별자는 쓰지 않는다"
ID_RULE["ledger_event"] = "DIC-sha256(adverse_event_type|핵심어)[:10] — 핵심어 = 바탕 분해의 멤버 핵심어(원문 토큰 공백 연결) · 정규화형이 같으면 같은 값"
ID_RULE["equipment_product"] = "DIC-sha256(product_name|항목 이름)[:10] · 개체 PRD-sha256(계열|이름) — 같은 이름 여러 계열이면 code `|`"
ID_RULE["post_procedure_timeline"] = "TML-sha256(timelines[].id)[:10]"
ID_RULE["emergency_sign"] = "SGN-sha256(정규화 문장)[:10]"
ID_RULE["phrase"] = ID_RULE["phrase"] + " · v3.2: 부작용 문구 종류만 · 정규화형은 토큰화(V3.2-1) 뒤 어간·핵심어 기준(「멍이」= 「멍」) — v3.1 항목은 raw_variants 로 재귀속"

# ---------------------------------------------------------------------------
# 규칙 데이터(json)
# ---------------------------------------------------------------------------
NORMALIZE_RULE["v3_2"] = NORM_V2
RESOLVE_RULES["name"] = "decompose_v3_2"
RESOLVE_RULES["tokenize"] = {"rule": TOKENIZE_RULE, "particles": PARTICLES, "verb_endings": VERB_ENDINGS, "grammar_words": GRAMMAR_WORDS, "stem_min_len": STEM_MIN_LEN, "relaxed_suffixes": RELAXED_SUFFIXES, "predicate_endings": PREDICATE_ENDINGS, "order": ["사전 통째 일치", "수식어·stopword·표지어", "문법 낱말", "조사·어미 떼기(어간 확인)", "미등록"], "preserved_as": "grammar_tokens[]"}
RESOLVE_RULES["normalize_v2"] = NORM_V2
TUPLE_RULES["name"] = "tuples_v3_2"
TUPLE_RULES["rule_zero"] = RULE_ZERO
TUPLE_RULES["phrase_kind_table"] = [{"kind": a, "ledger": b, "table": c, "relation": d} for a, b, c, d in PHRASE_KIND_TABLE]
TUPLE_RULES["principles"] = [{"key": k, "text": v} for k, v in PRINCIPLES]
TUPLE_RULES["adverse"]["node_rule"] = NODE_RULE
TUPLE_RULES["adverse"]["principles"] = PRINCIPLES_TEXT
TUPLE_RULES["adverse"]["expressions_create_units"] = "adverse_kind_only(이름 · safety.*) · 원장 사건 노드 포함"
TUPLE_RULES["adverse"]["unlinked_status"] = False
TUPLE_RULES["adverse"]["raw_name"] = "v3.2(V3.2-0): 없음 — 미등록 조각이 있는 이름은 핵심어 사건 노드"
TUPLE_RULES["adverse"]["status_values"] = list(ERD_ENUMS["phrase_dictionary.status"])
TUPLE_RULES["adverse"]["inheritance"] = INHERIT_RULE
TUPLE_RULES["phrase_kinds"] = {"rule": PHRASE_KIND_RULE, "conj_particles": CONJ_PARTICLES, "predicate_endings": PREDICATE_ENDINGS, "note_words": NOTE_WORDS, "sentence_min_tokens": SENTENCE_MIN_TOKENS, "sentence_min_grammar": SENTENCE_MIN_GRAMMAR, "sentence_latin_ratio": SENTENCE_LATIN_RATIO,
                               "fallback_core": FALLBACK_CORE, "core_exclude": CORE_EXCLUDE, "dup_prefix_min": DUP_PREFIX_MIN, "dup_rules": {"strong": ["paren_pair(원장 병기 X(Y))", "suffix_감|증|형성|감각(X+접미 ↔ X)", "word_contains(짧은 쪽이 긴 쪽의 낱말)", "jamo1"], "weak(표시만 · 기본 게이트 아님)": ["substring", "prefix≥2", "first_syllable(둘 다 2자 이하)"]}, "scope": "노드끼리 — 원장 노드 ↔ 사전 사건 · 원장 노드 ↔ 원장 노드(문구 ↔ 노드 아님)"}
TUPLE_RULES["equipment"] = {"rule": EQUIP_RULE, "families": EQUIP_FAMILIES, "extra_subcats": [list(x) for x in EQUIP_EXTRA_SUBCATS], "exclude_subcat_words": EQUIP_EXCLUDE_SUBCAT_WORDS, "exclude_name_words": EQUIP_EXCLUDE_NAME_WORDS, "abbrev_min_len": ABBREV_MIN_LEN}
TUPLE_RULES["ingredient"] = {"rule": INGREDIENT_RULE, "context_words": INGREDIENT_CONTEXT_WORDS, "named": INGREDIENT_NAMED}
TUPLE_RULES["site_closed"] = {"rule": SITE_DICT_RULE, "values": [{"value": v, "kind": k, "parent": p, "synonym_candidates": s} for v, k, p, s in SITE_CLOSED]}
TUPLE_RULES["seed"] = {"rule": SEED_RULE, "open_closed": OPEN_CLOSED_RULE, "closed": CLOSED_DICTIONARIES, "threshold": "빈도 ≥2 또는 locator ≥2"}
TUPLE_RULES["timeline"] = TIMELINE_RULE
TUPLE_RULES["emergency_sign"] = SIGN_RULE
TUPLE_RULES["procedure"]["what"] = list(TUPLE_RULES["procedure"]["what"]) + ["v3.2(V3.2-6): " + INGREDIENT_RULE, "v3.2(V3.2-5): 장비 항목은 제품 사전(origin=taxonomy)에 자동 등록되므로 자기 이름이 제품 값 → what=product(승격)"]

CHANGE_LIST_V32 = [
    ("V3.2-0", "§0 첫 규칙 — 문구 종류 분류 · 부작용 단위에는 부작용 문구만 · 부작용 축 노드 원칙(사전에 없으면 핵심어 새 사건 · ⑦ · unlinked/raw_name 없음) · 원칙 A·D 문장 · emergency_sign · 고지/문헌 참조", "§0 · §1.5 · §1.8 · §2 adverse_effect·clinical_rule·evidence_statement·emergency_sign · R15 · R35 · 사전 adverse_event_type(origin ledger) · column-map · 실측 §9.9 · §9.13"),
    ("V3.2-1", "토큰화 — 조사·용언 어미·문법 낱말 떼기(어간 확인) · grammar_tokens 보존", "§1.3 · resolve_rules.tokenize · 실측 §9.11"),
    ("V3.2-2", "표기 변형 norm_v2 — (a) 병기 gloss (b) 자모 변형 쌍 목록(적용 0) (c) 조사 제거 뒤 재일치", "§1.1 · resolve_rules.normalize_v2 · 씨앗 파일 variant_pairs · 실측 §9.12"),
    ("V3.2-3", "사전 씨앗 규칙 — 원장 전체 어휘 · 칸 → 종류 · 열림(선언 → 자동)/닫힘(승인) · 승인 묶음", "§1.7 · §4 closed · tuple_rules.seed · erd-v3.2-seed-candidates.* · 실측 §9.17"),
    ("V3.2-4", "부위 사전 전수 — 닫힌 목록 · kind · parent", "§2 site.parent · 사전 site · tuple_rules.site_closed · 씨앗 site"),
    ("V3.2-5", "장비 = 제품 자동 등록 · 항목 자신 → product 승격 · 줄임말 접두 후보", "§2 product.origin taxonomy · 사전 product_name · tuple_rules.equipment · 실측 §9.16"),
    ("V3.2-6", "성분 what · 성분 씨앗", "§1.4 · procedure.what_kind ingredient · tuple_rules.ingredient · 씨앗 ingredient_material"),
    ("V3.2-7", "부작용 문구 종류 판정 — not_adverse_note · explanatory_sentence · unlinked 로 세지 않음", "§1.5 · tuple_rules.phrase_kinds · phrase_shape · 실측 §9.13"),
    ("V3.2-8", "R15 속성 상속 3층(item → family → unit · basis · 참조만)", "R15.inheritance·layer · adverse_effect.general_* · 실측 §9.15"),
    ("V3.2-9", "post_procedure_timeline 개체 · R33 has_timeline · R34 timeline_refers · R15 period/phase_label/reaction_level → timeline_refs", "§2 · §3 · column-map 타임라인 행 · 실측 §9.14"),
]

# ---------------------------------------------------------------------------
# 검토 S-3 — 부작용 축 정의 표의 옛 구조 잔재(raw_name · unlinked · 표현 개체 · RAW: · R29 · 타임라인 reaction_level) 정리
# ---------------------------------------------------------------------------
import re as _re
BANNED = ("raw_name", "unlinked", "adverse_expression", "RAW:", "R29", "reaction_level=normal 로 표시")
SCRUB_NOTE = "(v3.1 까지의 옛 단위 문장 생략 — v3.2 §0.2)"


def scrub(text):
    """문장 단위(「 · 」 · 「. 」)로 나눠 금지어가 든 조각을 지운다. 조건 축(person_condition)의 raw_name 은 다른 개념이라 그대로 둔다."""
    if not isinstance(text, str) or not any(b in text for b in BANNED):
        return text
    parts = _re.split(r"( · |\. )", text)
    out, dropped = [], False
    for i in range(0, len(parts), 2):
        seg = parts[i]
        sep = parts[i + 1] if i + 1 < len(parts) else ""
        if any(b in seg for b in BANNED) and "person_condition" not in seg and "조건" not in seg:
            dropped = True
            continue
        out.append(seg + sep)
    t = "".join(out).strip(" ·.")
    return (t + " " + SCRUB_NOTE).strip() if dropped else t


_a = _ent("adverse_effect")
_drop = {"unregistered_fragments", "event_fragments", "candidate_name", "anchor", "dict_tuples", "raw_reason"}
_new = []
for n, t, r, src, rule in _a["attrs"]:
    if n in _drop:
        continue
    if n == "event":
        t, rule = "dict:adverse_event_type", "사건 사전 값 — ERD 사전 값 또는 원장 사건 노드(origin=ledger · §0.2)"
    elif n == "status":
        t, rule = "enum(complete)", "v3.2: 단위는 늘 세 칸 사전 값(원장 사건 노드 포함)이므로 complete 하나"
    elif n == "origins":
        src, rule = ["complications.json:categories[].complications[].name"] + [s_ for s_ in V31.ENTITIES[[e["key"] for e in V31.ENTITIES].index("adverse_effect")]["attrs"][[a[0] for a in V31.ENTITIES[[e["key"] for e in V31.ENTITIES].index("adverse_effect")]["attrs"]].index("origins")][3] if ".safety." in s_], "v3.2(V3.2-0): 이 단위를 세운 원천 — complications | safety_phrase(부작용 문구 종류)뿐 · 다른 테이블은 참조만"
    elif n in ("extra_sites", "extra_qualifiers"):
        rule = "사건에 붙지 않은 " + ("부위" if n == "extra_sites" else "수식") + " 조각(원칙 B 보존 · 단위 칸 아님)"
    elif n == "qualifier":
        rule = "v3(V3-1): 물질·기전 수식(공기 · 필러 · 지방 · 혈전 · 역행성) · 사건이 놓인 멤버 안의 수식 조각만(원칙 C) · 없으면 none(값)"
    elif n == "all_dict_values":
        rule = "v3.2: 늘 true — 세 칸 전부 사전 값(원장 사건 노드 포함)"
    _new.append((n, t, r, src, scrub(rule)))
_new.append(("side_fragments", "str[]", False, [], "v3.2(검토 S-1): 사전 사건 옆의 미등록 토큰 — 단위 칸이 아니라 문구 사전 항목 parsed.side 에 보존(노드 후보 목록)"))
_a["attrs"] = _new
_a["identity"] = "sha256(event_id|site_id|qualifier_id)[:10] — 세 칸 전부 사전 값(사건 = ERD 값 또는 원장 사건 노드 · site·qualifier 없음 = 'none' 값 · 상대 부위는 none)"
_a["definition"] = scrub(_a["definition"])
_a["aliases"] = scrub(_a["aliases"])
for e in ENTITIES:
    e["definition"] = scrub(e["definition"]) if e["key"] in ("adverse_effect", "evidence_statement", "clinical_rule", "conflict") else e["definition"]
_r15 = _rel("R15")
_r15["note"] = scrub(_r15["note"])
_r15["attrs"] = [(a, b, scrub(c)) for a, b, c in _r15["attrs"]]
for k in [k for k in ERD_ENUMS if k.startswith("adverse_expression.")] + ["adverse_effect.raw_reason"]:
    ERD_ENUMS.pop(k, None)
ERD_ENUMS["adverse_effect.status"] = ["complete"]
ERD_ENUMS["table_line.ref_status"] = ERD_ENUMS.pop("reference.ref_status")
DECISION_KINDS = [list(x) for x in DECISION_KINDS]
for x in DECISION_KINDS:
    if x[0] == "adverse_tuple_assign":
        x[2] = "obj(locator: 원장 locator — complications 이름 또는 부작용 문구 자리, kind: name|phrase)"
        x[3] = "obj(tuples: obj[](event_id, site_id, qualifier_id — 없으면 'none') — 하나 이상, courses: str[]|null)"
        x[4] = "부작용 이름·문구 자리의 단위를 사람이 지정한다(원장 사건 노드 대신 · 지정 단위가 없으면 세운다 — 세 칸 사전 값이어야). 적용 ③. v3.2(V3.2-0): 옛 판의 이름 단위 대상 결정은 같은 locator 로 닿는다"
    else:
        x[4] = scrub(x[4])
DECISION_KINDS = [tuple(x) for x in DECISION_KINDS]
for k in ("adverse_expression", "adverse_expression_candidates"):
    ID_RULE.pop(k, None)
ID_RULE["adverse_effect"] = "v3.2: ADV-<sha256(event_id|site_id|qualifier_id)[:10]> — event_id 는 ERD 사건 사전 id 또는 원장 사건 노드 id(DIC-sha256(adverse_event_type|핵심어)) · site_id = site 개체 id(anatomical·layer·region) | 'none' · qualifier_id = adverse_qualifier 사전 id | 'none'. 경과는 식별자에 없다(R15.course). 같은 세 칸은 어느 출처에서 와도 같은 id"
ID_RULE["decision_target"] = scrub(ID_RULE["decision_target"])
for k in list(TUPLE_RULES["adverse"].keys()):
    v = TUPLE_RULES["adverse"][k]
    if isinstance(v, str):
        TUPLE_RULES["adverse"][k] = scrub(v)
TUPLE_RULES["adverse"].pop("raw_name", None)
TUPLE_RULES["adverse"].pop("unlinked_status", None)
TUPLE_RULES["adverse"]["status_values"] = list(ERD_ENUMS["phrase_dictionary.status"])
TUPLE_RULES["adverse"]["expressions"] = RULE_ZERO
TUPLE_RULES["adverse"]["phrase_dictionary"] = "부작용 문구 사전(V3.2-0 · V3.2-7): 부작용 문구 종류(safety.*)만 정규화형 한 줄 — status exact|new|approved|note|sentence · 다른 테이블의 줄은 자기 parsed"
TUPLE_RULES["adverse"]["expressions_create_raw_units"] = False
