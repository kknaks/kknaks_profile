# -*- coding: utf-8 -*-
"""ERD v3 명세 (데이터). erd_spec_v24.py(v2.4 · 동결)를 읽어 실버 빌드 1~4차에서 드러난 구조·규칙 변경 10건(발주서 erd-v3-brief.md · ERD-V3-CANDIDATES.md V3-1~8 + 빌더 제약 V3-9·10)만 덧씌운다.
  V3-1  부작용 튜플 선택 수식 칸 qualifier(물질·기전) — (event, site, course, qualifier?) · 사전 adverse_qualifier · 식별자에 포함 · 없음 = none(값) · 접힘·표현 연결 규칙에 반영 (§1.5 · §2.14 · 사전)
  V3-2  분해 규칙: 괄호 안 조각이 회사 사전(manufacturer)·제품 사전에 닿으면 바깥 what 의 그 회사/제품으로 (§1.3/§1.4 resolve_rules.company_paren)
  V3-3  분해 규칙: 수식어 제외 목록(stopwords) — 조각이 아니라 참조 속성 qualifier_text(회차는 R12 session_index) · 목록은 규칙 데이터 · 출처 locator 필수 (resolve_rules.stopwords)
  V3-4  조합 기호 규칙 확정: `+` 항상 함께 · `/` 양쪽 조각으로(같은 what 의 부위 둘 → 함께 · 대안 둘 → 또는 · 괄호 안 대안은 바깥 하나) · 「무엇을 하나 × 부위 여럿」은 같은 what 의 튜플 여럿 + R12 member_mode (resolve_rules.combo · R12)
  V3-5  부위 개체 kind 열거형 anatomical · relative · layer · region — 사전 값 출처 필수 (§2.7 · 사전 site)
  V3-6  결정 kind canonical_rename — 사전 정준값 교체(같은 코드·id · 옛 정준값은 동의어로 · is_marketing_name 선택) · 적용 ① (§5)
  V3-7  technique · product 에 description(출처 locator 필수) · media_refs[](path·sha256·captured_at·source·kind) (§2.5 · §2.6)
  V3-8  기법 상속: 계열 기본 기법은 하위분류 단위로 둘 수 있다(R5 를 modality|modality_subcategory → technique) · 섞인 계열(M16)은 하위분류별·항목별 지정 · 상속은 canonical_mapping 결정으로만 (R5 · §9.5.6)
  V3-9  결정 적용 대상 확장: tuple_assign · tuple_assign_multi · adverse_tuple_assign 가 미해결 참조·조합 참조에도 적용(anchor = REF-id · REF-…#m<i>) (§5 · 빌더 규칙)
  V3-10 fold_approve 는 접히는 anchor 쌍의 ⑦ duplicate_candidate 를 닫는다(status=resolved · decision_id) (§5 규칙 ⑦)
사용자 정의 3(ERD-FROZEN §동결 조건)과 명시 예외(부작용 축 none·미상은 값)는 그대로. 원장 21 은 브론즈 2판 `bronze/phub-ledger/`(1판과의 차이 CHANGELOG 6곳). erd_build_v3.py 가 읽는다. v2.4 명세는 손대지 않는다.
"""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import erd_spec_v24 as V24  # noqa

ERD_VERSION = "v3"
PREVIOUS_VERSION = "v2.4"
SNAPSHOT = V24.SNAPSHOT                                  # 1판 스냅샷 기준일(원장 바탕)
BRONZE_VERSION = 2
BRONZE_DATE = "2026-11-05"
LEDGER_DIR = os.path.join(HERE, "bronze", "phub-ledger")  # 원장의 집(메달리온 브론즈 2판)
LEDGER_DIR_V1 = V24.LEDGER_DIR                           # 1판(대조용)
BRONZE_HASHES = os.path.join(LEDGER_DIR, "HASHES.txt")
BRONZE_CHANGELOG = os.path.join(LEDGER_DIR, "CHANGELOG.md")
STEP1_FILE = V24.STEP1_FILE
STEP1_TIER2_SOURCE_RE = V24.STEP1_TIER2_SOURCE_RE
SOURCE_FILES = list(V24.SOURCE_FILES)
SOURCE_KIND = dict(V24.SOURCE_KIND)
TRUST_FLAGS = dict(V24.TRUST_FLAGS)
NORMALIZE_RULE = copy.deepcopy(V24.NORMALIZE_RULE)
Q25 = list(V24.Q25)
DISPOSITIONS = dict(V24.DISPOSITIONS)
SITE_LABELS_KEEP = list(V24.SITE_LABELS_KEEP)
Q14_ORAL_DRUGS = list(V24.Q14_ORAL_DRUGS)
ADVERSE_EVENT_CATEGORIES = list(V24.ADVERSE_EVENT_CATEGORIES)
ADVERSE_EVENT_CATEGORY_REVIEW = list(V24.ADVERSE_EVENT_CATEGORY_REVIEW)
RELATIVE_SITES = list(V24.RELATIVE_SITES)
COURSES = list(V24.COURSES)
COURSE_DROPPED = list(V24.COURSE_DROPPED)
FOLD_CONDITION = V24.FOLD_CONDITION
FOLD_RULE = V24.FOLD_RULE
RULE4 = V24.RULE4
DECISION_COMMON_FIELDS = list(V24.DECISION_COMMON_FIELDS)
DECISION_STATUS = list(V24.DECISION_STATUS)
DECISION_BUILD_RULE = V24.DECISION_BUILD_RULE
EDGE_END_RULE = V24.EDGE_END_RULE
EDGE_END_KINDS = list(V24.EDGE_END_KINDS)
TARGET_DEPTH = list(V24.TARGET_DEPTH)
COURSE_RULE = V24.COURSE_RULE
LOCATOR_RULE = V24.LOCATOR_RULE
DECISION_APPLY_ORDER_RULE = V24.DECISION_APPLY_ORDER_RULE
DECISION_KINDS_NEW = list(V24.DECISION_KINDS_NEW)
DECISION_KINDS_NEW_V23 = list(V24.DECISION_KINDS_NEW_V23)
DECISION_KINDS_RESHAPED_V23 = dict(V24.DECISION_KINDS_RESHAPED_V23)
PROC_AXIS_EDGES = list(V24.PROC_AXIS_EDGES)
R29_TAXONOMY_SAFETY_KEYS = list(V24.R29_TAXONOMY_SAFETY_KEYS)
PRINCIPLES = list(V24.PRINCIPLES)
PRINCIPLES_TEXT = V24.PRINCIPLES_TEXT
SITE_RULE = V24.SITE_RULE
RAW_NAME_RULE = V24.RAW_NAME_RULE
CAT_FAMILY_RULE = V24.CAT_FAMILY_RULE
BRONZE_SNAPSHOT = SNAPSHOT

# ---------------------------------------------------------------------------
# 사용자 정의 3 + 명시 예외 (ERD-FROZEN · 그대로 유지 — v3 가 깨면 안 된다)
# ---------------------------------------------------------------------------
USER_DEFINITIONS = [
    ("1", "시술 = (무엇을, 어디에, 어떻게) 튜플. 미상 칸이 있으면 접지 않음. 조각 버리지 않음. 엣지 끝 = 시술 튜플."),
    ("2", "부작용 = (사건, 부위, 경과) 튜플. 원인 시술은 엣지. 표현은 가리키기만."),
    ("3", "원장 불변. 충돌은 레코드(④ 자동 해결도 기록). 결정 16 kind · 안정 키 · 적용 순서 ①~⑦. 빌드는 approved 만 읽음."),
]
EXPLICIT_EXCEPTION = ("부작용 축에서 부위 없음(none)·경과 미상은 사전 값으로 본다. (멍, none, 미상) 은 하나의 단위라 「멍 (타박상)」「멍 / 반상출혈」「멍·타박상」등이 접힌다. "
                      "시술 축의 「미상이면 접지 않음」과 다른 이유: 부작용의 부위 없음은 「모름」이 아니라 「어디서든 나는 사건」이고, 어느 시술에서 나는지는 R15 엣지가 든다. "
                      "v3: 수식 칸 없음(qualifier none)도 같은 뜻의 값이다 — 「물질·기전이 적히지 않은 사건」이지 미상이 아니다.")
USER_DEFINITIONS_V3 = [
    ("1", USER_DEFINITIONS[0][1]),
    ("2", "부작용 = (사건, 부위, 경과) 세 칸 + 선택 수식 칸(물질·기전 · 없음은 none 값) 튜플. 원인 시술은 엣지. 표현은 가리키기만. (R-4 · V3-1)"),
    ("3", "원장 불변. 충돌은 레코드(④ 자동 해결도 기록). 결정 17 kind · 안정 키(REF-…#m<i>·#s<i> 포함) · 적용 순서 ①~⑦(① dictionary_add/canonical_rename). 빌드는 approved 만 읽음. (R-4 · V3-6 · R-1)"),
]
USER_DEFINITIONS_V3_NOTE = ("v3 는 정의 1~3 의 뜻을 뒤집지 않고 확장한다(R-4: 동결 원문은 위에, v3 승계 문장은 아래 — 「그대로」는 뜻이지 글자가 아니다). 정의 2 의 튜플에 **선택** 수식 칸 qualifier 가 더해지고(V3-1 · 없으면 none 값 — 세 칸은 그대로), 정의 3 의 「결정 16 kind」는 canonical_rename 이 더해져 17(V3-6), "
                            "적용 순서 ①~⑦ 의 ① 에 canonical_rename 이 들어간다. 그 밖(안정 키 · approved 만 · 원장 불변 · 엣지 끝 = 튜플 · 조각 버리지 않음 · 표현은 가리키기만)은 그대로다. 명시 예외(부작용 축 none·미상은 값)도 그대로이며 qualifier none 은 그 예외와 같은 뜻의 값이다.")

# ---------------------------------------------------------------------------
# V3-1 — 부작용 수식 칸 qualifier (물질·기전) · 사전 adverse_qualifier (값마다 출처)
# ---------------------------------------------------------------------------
_CN = ("complications.json", "categories[].complications[].name")
_CE = ("consent-checklist.json", "categories[].emergency_signs[]")
_ES = ("extracted.json", "{code}.safety.serious[]")
_TS = ("taxonomy.json", "modality[].extracted.safety.serious[]")
_TIS = ("taxonomy.json", "modality[].subcategories[].items[].extracted.safety.serious[]")
_TPS = ("taxonomy.json", "modality[].products[].extracted.safety.serious[]")
_AVD = ("anatomy-danger-zones.json", "zones[].vessels[].danger")
_AFR = ("anatomy-danger-zones.json", "zones[].filler_specific.primary_risk")
_ACM = ("anatomy-danger-zones.json", "critical_safety_facts.mechanism")
# (canonical, kind, 정준값 출처, [(synonym, 출처)...]) — 값·동의어 전부 그 잎 키 값의 부분 문자열(kind=derived)
ADVERSE_QUALIFIERS = [
    ("공기", "물질", _CN, [], "「공기색전·카테터 관련 감염」[M16] 의 색전 물질 · consent emergency_signs 「공기색전 의심」"),
    ("필러", "물질", _ES, [], "「혈관 막힘 (필러가 혈관에 들어가…)」 류 · anatomy vessels[].danger 「NLF 필러 시 안면동맥 천자」"),
    ("지방", "물질", _CE, [], "「심한 호흡곤란, 흉통(지방색전증 의심)」 · extracted safety.serious 「지방 색전증」"),
    ("혈전", "물질", _AVD, [], "anatomy vessels[].danger 「정맥 천자 → 혈종, 드물게 정맥 혈전」"),
    ("역행성", "기전", _TIS, [], "「혈관 폐색(역행성 색전 메커니즘)」 · anatomy vessels[].danger 「역행성 색전 시 실명」 · critical_safety_facts.mechanism"),
]
ADVERSE_QUALIFIER_EXTRA_SOURCES = {"공기": [_CE], "필러": [_TS, _AVD], "지방": [_ES, _CN], "역행성": [_AVD, _AFR, _ACM, _TPS]}
ADVERSE_QUALIFIER_KINDS = ["물질", "기전"]
QUALIFIER_RULE = ("**수식 칸(qualifier · V3-1)**: 부작용 튜플은 (event, site, course, qualifier?) — qualifier 는 **선택** 칸으로 사건의 물질·기전(공기 · 필러 · 지방 · 혈전 — 물질 / 역행성 — 기전)을 적는다. 값은 사전 `adverse_qualifier`(값마다 원장 출처 필수 · 사전에 없는 조각은 미등록)에서만 온다. "
                  "qualifier 가 없으면 **none(값)** — 명시 예외와 같은 뜻으로 「물질·기전이 적히지 않은 사건」이지 미상이 아니다. 식별자는 qualifier 를 포함한다(ADV-sha256(event_id|site_id|course_id|qualifier_id) · 없으면 'none'). "
                  "분해: 수식 조각은 원칙 C — **사건이 놓인 멤버 안의 수식 조각만** 그 사건의 qualifier 다(멤버 밖에서 가져오지 않는다). 토큰이 통째로 어느 사전에도 닿지 않으면 **접두 수식 + 사건**으로 한 번 가른다(「공기색전」→ 공기 + 색전 — 접두가 수식 사전, 나머지가 사건 사전에 완전 일치할 때만 · 유사도 아님). "
                  "한 멤버에 수식 후보가 둘 이상이면 원칙 B — 수식마다 튜플. 사건에 붙지 않은 수식 조각은 extra_qualifiers 에 보존하고 그 문자열은 접지 않는다(이름 → raw_name · 표현 → unlinked · 부위·경과와 같다). "
                  "**접힘 조건**은 「세 칸 + 수식 칸 전부 사전 값일 때만」(qualifier none 은 명시 예외의 값) — 「공기색전」→ (색전, none, 미상, 공기) 와 「혈관폐색/색전」의 (색전, none, 미상, none) 은 다른 단위다(접히지 않음). "
                  "**표현 연결**은 후보 네 칸이 기존 단위와 완전 일치할 때만 exact(원칙 D 그대로) — 수식 칸이 다르면 no_unit. 사건 사전 동의어 「공기색전」은 v3 에서 뺀다(수식 + 사건으로 가른 결과가 그 자리를 대신한다 — 사전 값 변경은 이 하나뿐 · §11). 「섬유화」(경결 동의어)는 그대로 둔다(기전으로 옮길지는 결정 · §12).")

# ---------------------------------------------------------------------------
# V3-5 — 부위 kind · 조직층 값 (출처 필수)
# ---------------------------------------------------------------------------
SITE_KINDS = ["anatomical", "relative", "layer", "region"]
_CP = ("complications.json", "categories[].complications[].prevention")
_CMD = ("consent-checklist.json", "categories[].mandatory_disclosures[]")
_ASD = ("anatomy-danger-zones.json", "zones[].safe_injection_depth")
_ACP = ("anatomy-danger-zones.json", "zones[].clinical_pearls[]")
_ATN = ("anatomy-danger-zones.json", "zones[].tissue_data.notes")
# (canonical, 정준값 출처, [(synonym, 출처)...], 비고) — 전부 derived(부분 문자열)
SITE_LAYERS = [
    ("피부", _CN, [], "complications 이름 「피부 괴사 (…)」[M14] · anatomy tissue_data.notes 「이마 피부-골막 거리」"),
    ("피하 지방층", _CP, [("피하지방", _CMD), ("피하층", _ASD)], "complications prevention 「피하지방층」[M14] · consent 「피하지방」 · anatomy safe_injection_depth 「피하층」"),
    ("근육", _ACP, [], "anatomy clinical_pearls 「눈물고랑 근육 섬유」 · tissue_data.notes"),
    ("혈관", _AVD, [], "anatomy vessels[].danger 「혈관 폐색 → 피부 괴사」 · complications 이름 「혈관폐색」(사건 쪽은 사건 사전)"),
    ("점막", _ASD, [], "anatomy safe_injection_depth 「점막-피부 경계 … 점막하」"),
]
SITE_LAYER_EXTRA_SOURCES = {"피부": [_ATN, _ASD], "근육": [_ATN], "혈관": [_ASD, _ATN], "점막": [_ATN, _ACP]}
SITE_REGION_VALUES = ["얼굴"]   # 기존 taxonomy 부위 라벨 중 「넓은 구역」 — 값 추가 없음(바디·두피는 미등록 조각 · dictionary_add 후보 §12)
SITE_KIND_RULE = ("**부위 kind(V3-5)**: site 사전(개체 site)의 값마다 kind ∈ {anatomical(얼굴 부위 — anatomy 11 + taxonomy 부위 라벨 9), relative(주사 부위·시술 부위 — 사전 relative_site 의 값 · id 불변), layer(조직층 — 피부 · 피하 지방층 · 근육 · 혈관 · 점막), region(넓은 구역 — 얼굴 · 바디·두피 는 사전 값이 아직 없어 미등록 조각 · dictionary_add 후보)}. "
                  "layer 값은 anatomy-danger-zones 층 정보(safe_injection_depth · tissue_data.notes · clinical_pearls · vessels[].danger)와 complications 이름·prevention 에서 derived 로 왔다(값마다 출처). "
                  "시술 튜플의 site 는 anatomical·region 만 쓴다(layer 는 시술 자리가 아니다 — 시술 이름의 layer 조각은 미등록이 아니라 `layer_fragments` 로 보존 · 칸에 넣지 않는다). 부작용 튜플의 site 는 네 kind 전부 — (괴사, 피부) · (괴사, 피하 지방층) 이 가능해진다(지정은 adverse_tuple_assign · 「피부 괴사」「지방괴사」는 지금 사건 사전 동의어라 자동으로 갈리지 않는다 · §12).")

# ---------------------------------------------------------------------------
# V3-3 — 수식어 제외 목록(stopwords) · 규칙 데이터 (locator 는 build 가 원장에서 실측해 채운다 · 출처 없는 단어는 목록에 못 남는다)
# ---------------------------------------------------------------------------
STOPWORDS_BRIEF = ["회", "차", "터치업", "유지", "집중", "연말", "하반기", "가을", "관리", "케어", "과도한", "빈도"]
STOPWORDS_LEDGER = ["특별", "터치", "여름철", "병용", "보조", "동시", "콤보"]   # 원장 실측에서 추가 — 참조 라벨의 독립 토큰 · 어느 사전에도 안 닿는 일정·강도 수식어
STOPWORD_RULE = ("**수식어 제외 목록(stopwords · V3-3)**: 분해에서 아래 단어가 **독립 토큰**(공백 토큰 그대로 · 정규화 완전 일치)으로 나오면 조각(미등록 조각)이 아니라 참조의 `qualifier_text` 속성으로 보존한다 — 시술 튜플의 칸을 정하지 않고 미해결 사유도 되지 않는다. "
                 "회차·횟수(「1차」「4회」)는 규격 정규식(`\\d+(회|차)`)이 먼저 잡으며 `차` 는 R12 엣지 `session_index`, `회` 는 count 로 간다. 목록은 규칙 데이터(resolve_rules.stopwords · 단어마다 원장 locator ≥1 실측 — 출처 없는 단어는 목록에 두지 않는다). "
                 "발주서 12 + 원장 실측 추가 7(특별 · 터치 · 여름철 · 병용 · 보조 · 동시 · 콤보). 토큰 일부(「진정관리」의 관리 · 「울쎄라급」)에는 적용하지 않는다(완전 일치만 · 유사도 없음). 사전 값과 겹치는 단어는 없다(검산).")

# ---------------------------------------------------------------------------
# V3-2 — 괄호 안 회사·제품 규칙
# ---------------------------------------------------------------------------
COMPANY_PAREN_RULE = ("**괄호 안 회사·제품 규칙(V3-2)**: 괄호 안(inner 묶음)이 조각 **하나**이고 그 조각이 (a) 회사 사전(manufacturer · 정준값과 동의어 · `/` 로 이어진 복수 회사명은 각각)에 닿으면 바깥 what(계열명 또는 제품명)의 **그 회사 제품**으로 what 을 정한다 — 바깥 what 의 계열 안 제품 중 제조사가 그 회사인 제품이 정확히 하나일 때만(둘 이상·없음은 ambiguous · reason company_product) · (b) 제품 사전에 닿으면 **그 제품**이 what(「스킨부스터(리쥬란)」= 리쥬란 · 바깥은 그 제품의 계열이어야 하며 다른 계열이면 cross_family 표시). "
                      "괄호 안 조각이 둘 이상이고 `/` 로 나뉜 대안이면 V3-4(괄호 안 대안은 바깥 하나 · alternatives). 닿지 않으면 기존대로(미등록 조각 → partial/⑨). 「보톡스(엘러간)」은 taxonomy 항목 1 + problem-combos products 문장 7 + extracted related_techniques 2(더모톡신) 에 있으나 「엘러간」은 회사 사전(앨러간/애브비)에 **닿지 않는다** — 규칙은 데이터로 있고 적용은 dictionary_add(회사 동의어) 뒤다(실측 §9.5.9).")

# ---------------------------------------------------------------------------
# V3-4 — 조합 기호 규칙 확정 (+ / · 부위 여럿 · member_mode)
# ---------------------------------------------------------------------------
COMBO_RULE = ("**조합 기호 규칙(V3-4 · 확정)**: `+` 는 **항상 함께**(and). `/` 는 **양쪽 조각으로** 정한다 — 같은 what 의 **부위** 둘 → 함께(and) · **대안**(계열 · 하위분류 · 장비 · 재질 · 제품 — primary 조각) 둘 → 또는(or) · **괄호 안 대안은 바깥 하나**(what = 바깥 primary · 괄호 안은 `alternatives[]` 속성 · member_mode or). "
              "**「무엇을 하나 × 부위 여럿」**(「보톡스 이마+미간」「보톡스(턱선+광대)」「필러 볼+턱」 — primary 를 가진 멤버가 하나이고 나머지 멤버가 부위 조각뿐)은 조합 패키지(combo_ref)가 아니라 **같은 what 의 시술 튜플 여럿**(부위마다 하나 · anchor = REF-…#s<i>)이며 패키지 멤버 엣지(R12)가 각각 붙는다(member_mode and). "
              "primary 를 가진 멤버가 둘 이상이면 combo_ref(멤버마다 튜플 · member_mode = 기호에 따라 and|or · 한 라벨 안에 `+` 와 `/` 가 섞이면 mixed 로 두고 미해결 사유 combo_mixed). 한 멤버 안에 분리 기호 없이 부위 조각이 둘이면 v2.2 그대로 multi_site(버리고 접지 않음 · ⑨). "
              "기호 뜻은 원장 작성 규칙(`bronze/phub-ledger/README.md`: `+` 함께 · `/` 대안)과 같다 — 2판은 부위 나열의 `/` 6곳을 `+` 로 고쳤다(CHANGELOG). 어느 쪽 조각이 미등록이면 규칙은 적용되지 않고 ⑨(unregistered)다(규칙은 사전 값을 만들지 않는다).")
MEMBER_MODES = ["and", "or"]

# ---------------------------------------------------------------------------
# V3-6 · V3-9 · V3-10 — 결정 kind
# ---------------------------------------------------------------------------
RENAME_RULE = ("**canonical_rename(V3-6 · R-2)**: 사전 정준값 교체 — 코드가 있는 값(계열 M1 등)은 **코드 기반 개체 id(MOD-<code> · CAT-·PRD- 의 계열 코드)가 그대로**라 정준값을 바꿔도 개체·튜플·엣지의 id 는 바뀌지 않는다. 사전 항목 id 는 유도식 DIC-sha256(사전|정준값)(§1.1)이라 **재계산되며 옛 DIC- id 는 alias(renamed_from)로 남는다**. 옛 정준값은 동의어로 내리고(link=renamed_from) 선택적으로 is_marketing_name 을 표시한다. "
               "dictionary_add 로는 새 값이 생기므로 쓰지 않는다. 대상(값은 묶음 3 결정 · ERD 는 kind 만): M1 「보톡스」→「보툴리눔 톡신」 · M3 → 「바이오스티뮬레이터」 · M5 → 「자가혈 유래 시술」. 적용 ①(dictionary_add 와 같은 단계 · decided_at 순).")
DECISION_ANCHOR_RULE = ("**결정 적용 대상 확장(V3-9 · R-1)**: tuple_assign · tuple_assign_multi 의 target.ref_id 는 **미해결 참조(⑨ · 튜플 없음)와 조합 참조(combo_ref · 멤버 anchor REF-…#m<i>) · 부위별 튜플(REF-…#s<i> · V3-4)**에도 적용된다 — anchor 가 튜플을 가리키지 않아도 결정이 그 anchor 의 튜플을 **세운다**(분해 결과를 덮는 것이 아니라 없는 자리를 채운다). "
                        "adverse_tuple_assign 도 같다(locator 가 raw_name·unlinked 표현이면 그 자리를 세운다 — v2.4 그대로). 빌더 규칙: anchor 가 실버에 없다는 이유로 거부하지 않는다(4차에서 거부된 HIFU(슈링크/울쎄라) 2건의 자리). 지정값 자체는 사전 값이어야 한다(없으면 rejected · 사유 dictionary).")
FOLD_CLOSE_RULE = ("**fold_approve 가 ⑦ 을 닫는다(V3-10)**: fold_approve(approved)가 접는 anchor 쌍에 ⑦ duplicate_candidate 레코드가 있으면 그 conflict 를 status=resolved · decision_id=그 결정으로 닫는다(close_verdict 없음 · 같은 것으로 판정). "
                   "쌍이 아닌 ⑦(접지 않는다)은 conflict_close(not_same)로 닫는다. 「단계 끝 = open 0」에 닿는 두 길이다.")

DECISION_KINDS = []
for k, br, t, nv, n in V24.DECISION_KINDS:
    if k == "dictionary_add":
        DECISION_KINDS.append((k, br, t, nv, n))
        DECISION_KINDS.append(("canonical_rename", True, "obj(dictionary: 사전 이름, code: str|null — 계열 코드 등, canonical: str — 지금 정준값)", "obj(canonical: str — 새 정준값, old_as_synonym: true, old_id_as_alias: true — 옛 DIC- id 는 alias(renamed_from), is_marketing_name: bool|null)", "v3(V3-6): " + RENAME_RULE))
        continue
    if k == "tuple_assign_multi":
        n = n.replace("참조 자리면 package(kind=combo_ref)로 멤버 각각 R12, 분류 항목이면 튜플마다 R26", "v3(R-3 · V3-4): 같은 what 의 부위 여럿이면 multi_tuple(튜플 여럿 · R12 가 각각 · member_mode and · anchor REF-…#s<i>), primary 가 둘 이상(대안·함께)이면 combo_ref(member_mode 는 new_value.member_mode) · 분류 항목이면 튜플마다 R26")
        nv = "obj(tuples: obj[](what_kind, what_id, site_id, technique_id) — 둘 이상, member_mode: and|or — 같은 what × 부위 여럿이면 and 고정)"
    if k in ("tuple_assign", "tuple_assign_multi"):
        n = n + ". v3(V3-9): target.ref_id 가 미해결 참조(튜플 없음)·조합 참조(REF-…#m<i>)여도 적용 — 결정이 그 anchor 의 튜플을 세운다(빌더는 anchor 부재로 거부하지 않는다)"
    elif k == "adverse_tuple_assign":
        nv = "obj(tuples: obj[](event_id, site_id, course_id, qualifier_id — 없으면 'none') — 하나 이상)"
        n = n + ". v3(V3-1): 지정 튜플에 qualifier_id(없으면 'none') · V3-9: locator 가 raw_name·unlinked 표현이면 그 자리를 세운다(거부 없음)"
    elif k == "fold_approve":
        t = t.replace("조합 멤버 anchor(…#m<i>)", "조합 멤버 anchor(…#m<i>) · 부위별 튜플 anchor(…#s<i> · V3-4 · R-1)")
        n = n + ". v3(V3-10): 접는 anchor 쌍의 ⑦ duplicate_candidate 를 status=resolved · decision_id 로 닫는다"
    elif k == "edge_create":
        n = n.replace("tuple: obj(event, site, course — 사전 정준값)", "tuple: obj(event, site, course, qualifier — 사전 정준값 · qualifier 없으면 none)")
    DECISION_KINDS.append((k, br, t, nv, n))
DECISION_KINDS_NEW_V3 = ["canonical_rename"]
DECISION_KINDS_NOTE_V3 = {"tuple_assign": "V3-9 미해결·조합 anchor 적용", "tuple_assign_multi": "V3-9 미해결·조합 anchor 적용", "adverse_tuple_assign": "V3-1 qualifier_id · V3-9", "fold_approve": "V3-10 ⑦ 닫음", "edge_create": "V3-1 ref 구조체 qualifier"}
DECISION_APPLY_ORDER = []
for st, ks, why in V24.DECISION_APPLY_ORDER:
    if st == "①":
        ks, why = ["dictionary_add", "canonical_rename"], why + " · v3: canonical_rename 도 사전 단계(같은 코드·id 유지)"
    DECISION_APPLY_ORDER.append((st, list(ks), why))
DECISION_APPLY_ORDER_RULE = DECISION_APPLY_ORDER_RULE.replace("① dictionary_add →", "① dictionary_add / canonical_rename →")
DECISION_TARGET_RULE = V24.DECISION_TARGET_RULE.replace("참조 자리 id(REF- · 조합 멤버 REF-…#m<i>)", "참조 자리 id(REF- · 조합 멤버 REF-…#m<i> · 부위별 튜플 REF-…#s<i>(V3-4 · R-1))").replace("부작용 튜플은 (event, site, course) 사전 값 세 쌍으로", "부작용 튜플은 (event, site, course, qualifier — 없음은 none) 사전 값 네 쌍으로(R-4)") + ". v3(V3-9): REF- 는 튜플이 없는 미해결 참조·조합 멤버(REF-…#m<i>)·부위별 튜플(REF-…#s<i>)도 target 이다"

QUALITY_RULES = []
for no, cls, rule in V24.QUALITY_RULES:
    if no == "⑦":
        rule = rule + ". v3(V3-10): fold_approve 가 접는 anchor 쌍의 ⑦ 은 그 결정으로 닫힌다(status=resolved · decision_id)"
    QUALITY_RULES.append((no, cls, rule))

# ---------------------------------------------------------------------------
# V3-7 — technique · product 설명·매체 참조
# ---------------------------------------------------------------------------
MEDIA_RULE = ("**설명·매체 참조(V3-7)**: technique · product 에 `description`(str · 출처 locator 필수 — 원장 잎 키 또는 새 브론즈 원천(조사 파일)의 locator · 출처 없는 값 금지)과 `media_refs[]`(obj(path, sha256, captured_at, source, kind ∈ {photo, diagram, video, document})). "
              "사진·도판 파일 자체는 브론즈 밖 에셋(reference/ 등)이고 실버에는 참조(path · sha256)만 둔다. 값은 **새 브론즈 원천(조사 파일 · source_file.kind=research_artifact)** 입구로 채운다 — 원장 21 에는 이 값이 없으므로 지금은 비어 있다(출처 키 [] · 실버가 만들지 않는다).")
MEDIA_KINDS = ["photo", "diagram", "video", "document"]

# ---------------------------------------------------------------------------
# V3-8 — 기법 상속 하위분류 단위
# ---------------------------------------------------------------------------
R5_SUBCAT_RULE = ("**기법 상속(V3-8)**: R5 applies_technique 는 modality **또는 modality_subcategory** → technique. 계열 기본 기법(procedure-profiles mechanism[])은 계열 단위 출처뿐이지만, 상속 결정은 **하위분류 단위**로 둘 수 있다 — canonical_mapping(target.from_ref = R5:<계열> 또는 R5:<하위분류 id> · scope = 그 아래 CAT-/REF- 목록). "
                  "계열이 섞여 있으면(M16 수액 — intravenous 일괄 불가 · 지방분해주사·두피 메조 등 피하/근육 주사 혼재) 하위분류별 또는 항목별(scope 를 항목 CAT- 하나로) 지정한다. 상속은 결정(canonical_mapping)으로만 — 자동 아님(v2.2 유지 · technique_inheritance=false). §9.5.6 후보 표는 하위분류별로 scope 를 가른다.")

# ---------------------------------------------------------------------------
# 분해 규칙 §1.3 (데이터) — stopwords · company_paren · combo
# ---------------------------------------------------------------------------
RESOLVE_RULES = copy.deepcopy(V24.RESOLVE_RULES)
RESOLVE_RULES["name"] = "decompose_v3"
RESOLVE_RULES["bronze"] = {"version": BRONZE_VERSION, "dir": "bronze/phub-ledger", "hashes": "bronze/phub-ledger/HASHES.txt", "changelog": "bronze/phub-ledger/CHANGELOG.md", "diff_from_v1": "부위 나열의 `/` → `+` 6곳(treatment-optimization 2 · treatment-sequence 4)"}
RESOLVE_RULES["step2_decompose"]["combo_symbols_meaning"] = {"+": "함께(and)", "/": "양쪽 조각으로 — 부위 둘이면 함께(and) · 대안 둘이면 또는(or)", "&": "함께(and) — `+` 와 같다", ",": "나열 — `+` 와 같다(and)"}
RESOLVE_RULES["step2_decompose"]["stopwords"] = {"rule": STOPWORD_RULE, "words": [{"word": w, "origin": "brief"} for w in STOPWORDS_BRIEF] + [{"word": w, "origin": "ledger"} for w in STOPWORDS_LEDGER],
                                                 "match": "독립 토큰 · norm_v1 완전 일치", "session_regex": r"^(\d+)\s*(차)$", "count_regex": r"^(\d+)\s*(회)$", "locators": "build 가 원장 참조·이름 자리에서 실측(단어마다 ≥1 · 아래 words[].locators)"}
RESOLVE_RULES["step2_decompose"]["company_paren"] = {"rule": COMPANY_PAREN_RULE, "dictionaries": ["manufacturer(정준값·동의어 · `/` 분리 회사명 각각)", "product_name"], "scope": "inner 묶음의 조각이 하나일 때", "product_of_company": "바깥 what 의 계열 안 제품 중 manufacturer 가 그 회사인 제품이 정확히 하나일 때만(products.json · taxonomy products[].manufacturer)"}
RESOLVE_RULES["step2_decompose"]["dictionary_order_note"] += " · v3: stopwords 는 사전이 아니라 제외 목록(조각 전 단계) · manufacturer 는 inner 묶음에서만 본다(company_paren)"
RESOLVE_RULES["step3_assemble"]["combo"] = {"rule": COMBO_RULE, "member_modes": MEMBER_MODES, "multi_site_with_symbol": "primary 멤버 하나 + 부위 멤버들(`+`/`/`) → 같은 what 의 튜플 여럿(anchor REF-…#s<i>) · R12 member_mode and",
                                            "alternatives_in_paren": "inner 묶음이 `/` 대안(primary 조각 둘 이상)이면 what = 바깥 primary · alternatives[] 보존 · member_mode or", "unregistered_side": "어느 쪽 조각이 미등록이면 규칙 적용 없이 ⑨(unregistered)"}
RESOLVE_RULES["step3_assemble"]["unresolved"] += ". v3: 분리 기호(`+`/`/`)로 나뉜 부위 멤버는 multi_site 가 아니라 같은 what 의 튜플 여럿(V3-4) · 한 멤버 안의 부위 둘은 여전히 multi_site · 기호가 섞이면 combo_mixed"

# ---------------------------------------------------------------------------
# 식별자
# ---------------------------------------------------------------------------
ID_RULE = copy.deepcopy(V24.ID_RULE)
ID_RULE["adverse_effect"] = ("네 칸(event · site · course · qualifier) 전부 사전 값이면(미등록 조각 0 · 붙지 않은 조각 0 · event_kind=dict) ADV-<sha256(event_id|site_id|course_id|qualifier_id)[:10]>, raw_name 튜플은 ADV-<sha256(RAW:<anchor>|none|<course_id(미상)>|none|<anchor>)[:10]> — "
                             "event_id = 사건 사전 id, site_id = site 개체 id(anatomical·layer·region) | 상대 부위 사전 id | 'none', course_id = 경과 사전 id('미상' 포함), qualifier_id = adverse_qualifier 사전 id | 'none'(v3 · 없음은 값), anchor = 그 이름의 원장 locator. "
                             "v3: 수식 칸이 식별자에 들어간다 — (색전, none, 미상, 공기) ≠ (색전, none, 미상, none). 튜플은 complications 65 이름에서만 생긴다(표현은 가리키기만 · 2-C′)")
ID_RULE["procedure"] = V24.ID_RULE["procedure"] + ". v3(V3-4): 「무엇을 하나 × 부위 여럿」 참조의 부위별 튜플 anchor 는 REF-…#s<i>(i = 부위 순서) · 조합 멤버는 그대로 #m<i>"
ID_RULE["adverse_expression_candidates"] = "표현 레코드의 candidates[] = (event, site, course, qualifier) 후보 + would_be_id(ADV-sha256(event_id|site_id|course_id|qualifier_id)) + exists. 튜플이 아니다(원칙 D)"
ID_RULE["dictionary_entry"] = "DIC-<sha256(사전 이름|정준값)[:10]> — 유도식. canonical_rename(V3-6 · R-2)이 정준값을 바꾸면 재계산되고 옛 DIC- id 는 alias(renamed_from). 코드 기반 개체 id(MOD-<code> · CAT-/PRD- 의 계열 코드)는 정준값과 무관해 바뀌지 않는다"
ID_RULE["reference"] = V24.ID_RULE["reference"] + ". v3(V3-9): 튜플이 없는 미해결 참조의 REF- 도 결정 target 이다"

# ---------------------------------------------------------------------------
# 개체 — 구조 21 그대로 · site(kind) · product/technique(description · media_refs) · adverse_effect(qualifier) · adverse_expression(candidates qualifier) · decision
# ---------------------------------------------------------------------------
ENTITIES = copy.deepcopy(V24.ENTITIES)


def _ent(key):
    return next(e for e in ENTITIES if e["key"] == key)


# V3-5 site
_s = _ent("site")
_s["definition"] += (" v3(V3-5): 값마다 kind ∈ {anatomical, relative, layer, region}. 조직층(layer) 값 5(피부 · 피하 지방층 · 근육 · 혈관 · 점막)가 사전에 들어왔다(값마다 anatomy-danger-zones 층 정보·complications 이름·prevention 출처). "
                     "relative(주사 부위·시술 부위)는 사전 relative_site 의 값으로 id 가 바뀌지 않는다. region = 얼굴(바디·두피는 아직 미등록 조각). 시술 튜플의 site 칸에는 anatomical·region 만, 부작용 튜플의 site 칸에는 네 kind 전부.")
_s["attrs"] = [a if a[0] != "site_kind" else ("site_kind", "enum(backbone|taxonomy_site_label|layer)", True, [], "anatomy 11 = backbone, taxonomy 부위 라벨 10 = taxonomy_site_label, v3 조직층 5 = layer (값의 출처 종류)") for a in _s["attrs"]]
_s["attrs"].insert(3, ("kind", "enum(anatomical|relative|layer|region)", True, ["anatomy-danger-zones.json:zones[].name_ko", "taxonomy.json:problem[].subcategories[].label", "complications.json:categories[].complications[].name", "complications.json:categories[].complications[].prevention", "anatomy-danger-zones.json:zones[].safe_injection_depth", "anatomy-danger-zones.json:zones[].clinical_pearls[]", "anatomy-danger-zones.json:zones[].vessels[].danger"],
                       "v3(V3-5): " + SITE_KIND_RULE))

# V3-7 product · technique
for key in ("product", "technique"):
    _e = _ent(key)
    _e["attrs"] += [
        ("description", "str|null", False, [], "v3(V3-7): 설명문. 출처 locator 필수(원장 잎 키 또는 새 브론즈 원천(조사 파일)) — 출처 없는 값 금지. 원장 21 에는 없어 지금은 null(실버가 만들지 않는다)"),
        ("media_refs", "obj[](path, sha256, captured_at, source, kind)|null", False, [], "v3(V3-7): 매체 참조(사진·도판·영상·문서). 파일은 브론즈 밖 에셋, 실버는 path·sha256 참조만. kind ∈ {photo, diagram, video, document}. 새 브론즈 원천 입구로 채움(현장 기기 사진 109장 등) · 지금은 null"),
    ]
    _e["definition"] += " v3(V3-7): description(출처 locator 필수) · media_refs[](브론즈 밖 에셋 참조)를 가진다 — 새 브론즈 원천(조사 파일) 입구로 채운다."

# V3-8 technique 정의
_ent("technique")["definition"] += " v3(V3-8): R5 는 modality|modality_subcategory → technique. 계열 기본 기법의 상속 결정(canonical_mapping)은 하위분류 단위로 둘 수 있고 섞인 계열(M16)은 하위분류별·항목별 지정 — 자동 상속은 여전히 없다."
_ent("modality_subcategory")["definition"] += " v3(V3-8): R5 의 from 이 될 수 있다(하위분류 단위 기본 기법 — canonical_mapping target.from_ref=R5:<하위분류 id>)."

# V3-1 adverse_effect
_a = _ent("adverse_effect")
_a["definition"] = _a["definition"] + " v3(V3-1): 튜플에 선택 수식 칸 qualifier(물질·기전 · 사전 adverse_qualifier · 없음 = none 값 · 식별자 포함)가 더해진다 — " + QUALIFIER_RULE
_a["identity"] = "sha256(event_id|site_id|course_id|qualifier_id)[:10] — 네 칸 전부 사전 값일 때(qualifier 없음 = 'none' 값). raw_name 튜플은 sha256(RAW:anchor|none|미상 id|none|anchor) — 이름마다 고유"
_aattrs = []
for a in _a["attrs"]:
    _aattrs.append(a)
    if a[0] == "course":
        _aattrs.append(("qualifier", "dict:adverse_qualifier|none", True, ["complications.json:categories[].complications[].name"], "v3(V3-1): 물질·기전 수식(공기 · 필러 · 지방 · 혈전 · 역행성). 사건이 놓인 멤버 안의 수식 조각만(원칙 C) · 없으면 none(값 · 미상 아님). raw_name 은 none"))
        _aattrs.append(("qualifier_id", "str|none", True, [], "adverse_qualifier 사전 id 또는 'none' — 식별자에 들어간다"))
        _aattrs.append(("qualifier_basis", "enum(member|prefix_split)|null", False, [], "v3: 수식이 어디서 왔나 — member(멤버 안 독립 조각) · prefix_split(「공기색전」처럼 토큰 접두를 가른 것) · null(none)"))
    if a[0] == "extra_courses":
        _aattrs.append(("extra_qualifiers", "str[]", True, [], "v3(V3-1): 사건에 붙지 않은 수식 조각 전부(원칙 B 보존 · 있으면 raw_name). dict 튜플은 []"))
    if a[0] == "site_ref_kind":
        _aattrs[-1] = ("site_ref_kind", a[1], a[2], a[3], a[4] + " · v3(V3-5): site 개체의 kind 는 anatomical|layer|region(사전 site) · relative 는 relative_site 사전")
_a["attrs"] = _aattrs
for i, a in enumerate(_a["attrs"]):
    if a[0] == "dict_tuples":
        _a["attrs"][i] = ("dict_tuples", "obj[](event, site, course, qualifier)|null", False, [], a[4] + " · v3: qualifier 포함")
_x = _ent("adverse_expression")
_x["definition"] += " v3(V3-1): 후보(candidates)는 (event, site, course, qualifier) 네 칸 — 수식 칸까지 기존 단위와 완전 일치할 때만 exact."
_xattrs = []
for a in _x["attrs"]:
    if a[0] == "candidates":
        a = ("candidates", "obj[](event, site, site_kind, course, qualifier, would_be_id, exists, unit_id|null, site_basis, course_basis, qualifier_basis, member)", True, [], a[4] + " · v3: qualifier 칸 포함(없으면 none)")
    elif a[0] == "match_status":
        a = (a[0], a[1], a[2], a[3], a[4] + " · v3: 네 칸(수식 포함) 완전 일치가 exact 의 조건")
    _xattrs.append(a)
    if a[0] == "extra_courses":
        _xattrs.append(("extra_qualifiers", "str[]", True, [], "v3(V3-1): 사건에 붙지 않은 수식 조각(보존 · 있으면 unlinked)"))
_x["attrs"] = _xattrs

# decision 정의
_d = _ent("decision")
_d["definition"] += " v3: kind 17(+canonical_rename · V3-6) · tuple_assign(_multi)·adverse_tuple_assign 는 미해결·조합 anchor 에도 적용(V3-9) · fold_approve 가 ⑦ 을 닫는다(V3-10)."
_dattrs = []
for a in _d["attrs"]:
    if a[0] == "kind":
        a = ("kind", "enum(" + "|".join(k[0] for k in DECISION_KINDS) + ")", True, [], "§5.2 표(17 · v3 +canonical_rename). 빌드 적용 kind(build_reads=true): " + " · ".join(k[0] for k in DECISION_KINDS if k[1]) + " · 적용 순서 §5 표")
    _dattrs.append(a)
_d["attrs"] = _dattrs
_c = _ent("conflict")
_cattrs = []
for a in _c["attrs"]:
    if a[0] == "status":
        a = (a[0], a[1], a[2], a[3], a[4] + " · v3(V3-10): fold_approve(approved)가 접는 anchor 쌍의 ⑦ 은 resolved · decision_id")
    _cattrs.append(a)
_c["attrs"] = _cattrs
_pk = _ent("package")
_pk["definition"] += " v3(V3-4): combo_ref 멤버 엣지(R12)에 member_mode(and|or). 「무엇을 하나 × 부위 여럿」 참조는 combo_ref 가 아니라 같은 what 의 튜플 여럿이며 R12 가 각각 붙는다(member_mode and)."

# ---------------------------------------------------------------------------
# 관계 — 구조 31 그대로 · R5 from · R12/R9/R17/R18 속성(member_mode · qualifier_text · session_index · alternatives) · R31 비고
# ---------------------------------------------------------------------------
RELATIONS = copy.deepcopy(V24.RELATIONS)


def _rel(rid):
    return next(r for r in RELATIONS if r["id"] == rid)


_r5 = _rel("R5")
_r5["from"] = "modality|modality_subcategory"
_r5["note"] = (_r5["note"] or "") + ". v3(V3-8): " + R5_SUBCAT_RULE
_r5["attrs"] = list(_r5["attrs"]) + [("basis", "enum(ledger|canonical_mapping)", "v3: ledger = procedure-profiles mechanism[](계열) · canonical_mapping = 결정으로 둔 하위분류 단위 기본 기법(decision_id)")]
_r12 = _rel("R12")
_r12["attrs"] = list(_r12["attrs"]) + [
    ("member_mode", "enum(and|or)", "v3(V3-4): and = 함께(`+` · 부위 나열 · 「무엇을 하나 × 부위 여럿」의 튜플마다) · or = 대안(`/` 대안 · 괄호 안 대안)"),
    ("session_index", "int|null", "v3(V3-3): 회차 수식(「1차」) — 규격 `\\d+차` 에서"),
    ("qualifier_text", "str[]", "v3(V3-3): stopwords 로 뗀 수식어 원문(유지 · 집중 · 연말 …) — 튜플 칸이 아니다"),
    ("alternatives", "str[]|null", "v3(V3-4): 괄호 안 대안(HIFU(슈링크/울쎄라)의 슈링크·울쎄라 — 사전에 닿은 조각의 id 목록) · 끝은 바깥 what 하나"),
]
_r12["note"] = (_r12["note"] or "") + ". v3(V3-4): " + COMBO_RULE
for rid in ("R9", "R17", "R18"):
    r = _rel(rid)
    r["attrs"] = list(r["attrs"]) + [("qualifier_text", "str[]", "v3(V3-3): stopwords 로 뗀 수식어 원문"), ("alternatives", "str[]|null", "v3(V3-4): 괄호 안 대안 — 끝은 바깥 what 하나"), ("member_mode", "enum(and|or)|null", "v3(V3-4): 참조가 같은 what 의 부위별 튜플 여럿이면 and(엣지가 튜플마다) · 대안이면 or")]
_r30 = _rel("R30")
_r30["note"] = _r30["note"].replace("(event, site, course) 사전 값 세 쌍", "(event, site, course, qualifier — 없음은 none) 사전 값 네 쌍(R-4)")
_r31 = _rel("R31")
_r31["note"] = (_r31["note"] or "") + " · v3(V3-5): site 의 kind 는 anatomical|layer|region(조직층 값 5 추가) — (괴사, 피부)·(괴사, 피하 지방층) 가능"
_r29 = _rel("R29")
_r29["note"] = (_r29["note"] or "") + " · v3(V3-1): 후보 네 칸(수식 포함) 완전 일치일 때만 exact"
_r29["attrs"] = [a if a[0] != "matched_fragments" else ("matched_fragments", "obj(event, site, course, qualifier)", "분해에서 닿은 조각 · v3 qualifier 포함") for a in _r29["attrs"]]
_r15 = _rel("R15")
_r15["note"] = (_r15["note"] or "") + " · v3: 끝 튜플의 수식 칸(qualifier)은 튜플의 것 — 엣지에 넣지 않는다"

ERD_ENUMS = copy.deepcopy(V24.ERD_ENUMS)
ERD_ENUMS["site.kind"] = list(SITE_KINDS)
ERD_ENUMS["site.site_kind"] = ["backbone", "taxonomy_site_label", "layer"]
ERD_ENUMS["adverse_qualifier.kind"] = list(ADVERSE_QUALIFIER_KINDS)
ERD_ENUMS["adverse_effect.qualifier_basis"] = ["member", "prefix_split"]
ERD_ENUMS["R12.member_mode"] = list(MEMBER_MODES)
ERD_ENUMS["media_refs.kind"] = list(MEDIA_KINDS)
ERD_ENUMS["decision.kind"] = [k[0] for k in DECISION_KINDS]
ERD_ENUMS["decision.apply_order"] = [" / ".join(ks) for _, ks, _ in DECISION_APPLY_ORDER]
ERD_ENUMS["reference.result"] = ["tuple", "multi_tuple", "combo_ref", "node", "unresolved", "none"]
ERD_ENUMS["reference.unresolved_reason"] = list(ERD_ENUMS.get("reference.unresolved_reason", [])) + ["company_product", "combo_mixed"]
ERD_ENUMS["adverse_expression.unlinked_reason"] = ["unregistered", "unattached_fragments", "no_unit", "no_event"]

# ---------------------------------------------------------------------------
# 튜플 규칙 v3 (데이터) — erd-v3-tuples.py 가 그대로 실행
# ---------------------------------------------------------------------------
TUPLE_RULES = copy.deepcopy(V24.TUPLE_RULES)
TUPLE_RULES["name"] = "tuples_v3"
TUPLE_RULES["bronze_version"] = BRONZE_VERSION
TUPLE_RULES["user_definitions"] = [{"no": n, "text": t} for n, t in USER_DEFINITIONS]
TUPLE_RULES["explicit_exception"] = EXPLICIT_EXCEPTION
_P = TUPLE_RULES["procedure"]
_P["input"]["catalog_items"] += " — v3: 원장 = 브론즈 2판(bronze/phub-ledger)"
_P["input"]["references"] += " — v3: 2판 이름(`+` 6곳) · stopwords 는 조각 전 단계에서 뗀다"
_P["stopwords"] = STOPWORD_RULE
_P["company_paren"] = COMPANY_PAREN_RULE
_P["combo"] = COMBO_RULE
_P["combo_v22"] = V24.TUPLE_RULES["procedure"]["combo"]
_P["site"] = _P["site"] + " · v3(V3-4): 분리 기호(`+`/`/`)로 나뉜 부위 멤버는 multi_site 가 아니라 같은 what 의 튜플 여럿(anchor REF-…#s<i> · R12 member_mode and) · v3(V3-5): layer 값은 시술 site 칸에 넣지 않는다(layer_fragments 보존)"
_P["qualifiers"] = _P["qualifiers"] + " · v3(V3-3): stopwords 토큰은 조각이 아니라 참조 속성 qualifier_text · `\\d+차` 는 session_index"
_P["what"] = list(_P["what"]) + ["v3(V3-2): inner 묶음의 유일한 조각이 회사 사전에 닿으면 바깥 what 계열의 그 회사 제품(정확히 하나일 때) · 제품 사전에 닿으면 그 제품", "v3(V3-4): inner 묶음이 `/` 대안(primary 둘 이상)이면 what = 바깥 primary · alternatives 보존(or)"]
_P["id"] = ID_RULE["procedure"]
_P["member_modes"] = list(MEMBER_MODES)
_Q = TUPLE_RULES["adverse"]
_Q["qualifier"] = QUALIFIER_RULE
_Q["split"] = _Q["split"].replace("사전 순서 relative_site → site → course → adverse_event_type", "사전 순서 relative_site → site(anatomical·layer·region) → course → adverse_qualifier → adverse_event_type") + " · v3: 통째로 안 닿는 토큰은 접두 수식 + 사건으로 한 번 가른다(공기색전 → 공기 + 색전 · 완전 일치만)"
_Q["tuple"] = _Q["tuple"] + " · v3(V3-1): qualifier 도 같은 멤버 안의 수식 조각만 · 후보 둘 이상이면 수식마다 · 없으면 none(값)"
_Q["fold_condition"] = "세 칸 + 수식 칸 전부 사전 값일 때만 (qualifier none 은 값)"
_Q["fold_rule"] = V24.ADVERSE_FOLD_RULE + ". v3(V3-1): 수식 칸이 다르면 다른 단위 — (색전, none, 미상, 공기) ≠ (색전, none, 미상, none)"
_Q["expressions"] = V24.EXPRESSION_RULE + " v3(V3-1): 후보 네 칸(수식 포함) 완전 일치일 때만 exact."
_Q["id"] = ID_RULE["adverse_effect"]
_Q["site_kinds"] = list(SITE_KINDS)
_Q["site_layers"] = [c for c, *_ in SITE_LAYERS]
_Q["qualifier_values"] = [c for c, *_ in ADVERSE_QUALIFIERS]
_Q["qualifier_none_is_value"] = True
ADVERSE_FOLD_RULE = _Q["fold_rule"]
EXPRESSION_RULE = _Q["expressions"]

# v2.4 → v3 변경 목록 (V3-# 대응 · 어디서)
CHANGE_LIST = [
    ("R-1~R-4", "독립 검토(erd-v3-review.md) 문장 수정 4", "R-1 §1.1·§5.2 target/fold_approve anchors 에 REF-…#s<i> · R-2 §5.2 canonical_rename id 규칙(코드 기반 id 유지 · DIC- 재계산+alias · §1.1 id_rule.dictionary_entry) · R-3 §5.2 tuple_assign_multi 비고(multi_tuple vs combo_ref · member_mode) · R-4 §0 승계 문장(세 칸 + 선택 수식 칸 · kind 17) · R30 네 쌍 · target 규칙 「세 쌍」 삭제"),
    ("V3-1", "부작용 튜플 수식 칸 qualifier", "§1.5 수식 규칙 · §2.14 qualifier/qualifier_id/qualifier_basis/extra_qualifiers · §2.15 candidates · §4 사전 adverse_qualifier(값 5 · 출처) · R29 · §1.1 식별자 · 사건 사전 동의어 「공기색전」 제거 · 실측 §9.6.7"),
    ("V3-2", "괄호 안 회사·제품 규칙", "§1.3 resolve_rules.step2_decompose.company_paren · §1.4 what 규칙 · 실측 §9.5.9"),
    ("V3-3", "수식어 제외 목록 stopwords", "§1.3 resolve_rules.step2_decompose.stopwords(단어 19 · locator) · §1.4 qualifiers · R9/R12/R17/R18 qualifier_text · R12 session_index · 실측 §9.5.10"),
    ("V3-4", "조합 기호 규칙 확정 · 부위 여럿 · member_mode", "§1.3 resolve_rules.step3_assemble.combo · §1.4 combo/site · R12 member_mode/alternatives · §2.13 package · 실측 §9.5.11(16건 + 전수)"),
    ("V3-5", "부위 kind 열거형 · 조직층 값 5", "§2.8 site.kind(발주서 표기 §2.7) · §4.2 사전 site(kind · layer 5 출처) · §1.5 split 순서 · R31 · 실측 §9.6.8"),
    ("V3-6", "결정 kind canonical_rename", "§5.2 kind 17 · §5.4 적용 ① · enum decision.kind"),
    ("V3-7", "technique·product description · media_refs", "§2.6 product · §2.7 technique(발주서 표기 §2.5·§2.6) · enum media_refs.kind · §5.1 새 브론즈 원천"),
    ("V3-8", "기법 상속 하위분류 단위", "R5 from modality|modality_subcategory · R5.basis · §2.7/§2.3 정의 · §9.5.6 후보 하위분류별(M16 수액 7 하위분류)"),
    ("V3-9", "결정 적용 대상 확장(미해결·조합 anchor)", "§5.2 tuple_assign/tuple_assign_multi/adverse_tuple_assign 비고 · §1.1 target 규칙 · §5 빌더 규칙"),
    ("V3-10", "fold_approve 가 ⑦ 을 닫는다", "§5 규칙 ⑦ · §5.2 fold_approve 비고 · §2.20 conflict.status · §9.3"),
]
