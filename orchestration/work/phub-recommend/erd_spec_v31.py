# -*- coding: utf-8 -*-
"""ERD v3.1 명세 (데이터). erd_spec_v3.py(v3 · 동결)를 읽어 발주서 erd-v3.1-brief.md 의 변경 6건 + 코디·사용자 추가 4건(V3.1-7~10 · 2026-11-05)만 덧씌운다.
  V3.1-1  결정 kind product_reclassify — 제품의 계열 코드 교체(PRD- id 재계산 · 옛 id alias reclassified_from · R4 이동 · 제품 끝 엣지는 새 id) · 적용 ⓪ (§5.2 · §2.6 · R4 · §1.1)
  V3.1-2  관계 R32 rule_applies_to — clinical_rule → product|technique|proc_axis · 속성 scope·severity·source_locator·decision_id·basis · 값은 edge_create 로만(제품 note 규칙 문장은 clinical_rule(kind=product_note) 출처 후보로 열거만) (§3 · §2.19)
  V3.1-3  결정 kind dictionary_remove — 동의어 하나 또는 값 제거(쓰는 레코드 있으면 거부) · 제거 이력 removed_synonyms[]/removed_entries[] · 적용 ①(dictionary_add·canonical_rename 뒤) (§5.2)
  V3.1-4  person_condition 식별을 문자열에서 조건 사전(person_condition · 발주서의 condition_dictionary)으로 — 정준값·동의어·kind·출처 · 식별자 = kind|정준값 · 원장 문장은 단위의 phrases[] 부록 + R16/R17/R18 source_phrases[] 로 보존 · 초기값은 원장 이름 전수에서 완전 일치만 접고 나머지는 raw_name (§2.16 · §1.6 · 사전)
  V3.1-5  「회」(횟수)·「N차」(회차) 자리 — R12 session_count·session_index · R9/R17/R18 는 qualifier_text 만 (R12 · resolve_rules.stopwords)
  V3.1-6  stopwords 와 사전 값 겹침 — 「stopword 는 분해 조각에서만 제외하고 사전 값으로의 통째 일치는 먼저 본다」 · 겹침 목록은 검산이 센다(관리 ↔ modality_group) (resolve_rules.stopwords.overlap)
  V3.1-7  consent mandatory_disclosures[] → clinical_rule(kind=disclosure · 원문 · locator) + R32(basis=ledger · 계열) · 같은 문장은 문구 사전(kind=disclosure)으로 부작용 단위에 닿는다 · modality.mandatory_disclosures 속성 삭제 (§2.19 · R32 · column-map 이동 1)
  V3.1-8  안전 문구 수식어 목록(adverse stopwords · 규칙 데이터 · 미등록 조각 빈도 ≥4 에서 · locator 필수) — 정도·시간·연결어·기타 + 발생률·조건·시간 패턴 — 조각으로 세지 않고 문구 사전 항목 parsed 에 보존 (§1.5 · 사전 phrase_dictionary)
  V3.1-9  **사용자 정의 2 개정(2026-11-05)** — 부작용 단위 = (사건, 부위, 물질) 세 칸 · 부위는 단위를 가르는 것만(조직층 · 절대 부위) · 상대 부위(주사 부위·시술 부위)는 none 과 같다 · **경과(일시·지연·지속·영구·재발)는 단위 칸이 아니라 R15 엣지 속성** · 식별자 ADV-sha256(event|site|qualifier) · 명시 예외 「부위 none · 물질 none 은 값」 (§0 · §1.5 · §2.14 · R15 · §1.1)
  V3.1-10 **안전 문구 사전(phrase_dictionary)** — 원장 문구(safety · 타임라인 · 응급 징후 · 환자 설명 · 문헌 문장 · 고지)를 정규화형(norm_v1 + 수식어 제거) 기준으로 한 줄씩 {normalized · raw_variants · units · parsed · status(auto|approved|unlinked) · locators} · 조각 전부 사전 값이면 auto 로 단위 조합(없으면 생성 · 시술 튜플과 대칭) · 아니면 unlinked 게이트 · 결정 kind phrase_map(①) · R15 가 source_phrases[] 로 참조하고 course/degree/timing/incidence 는 거기서 · **adverse_expression 개체·R29 삭제**(표현은 개체가 아니라 부록 — 사용자 정의 2 「표현은 가리키기만」을 더 강하게) · 조건 문장도 같은 원칙으로 부록(condition_expression 없음) (§2 · §3 · §4 · §5.2 · column-map 표현 행 28)
사용자 정의 1·3 과 명시 예외의 논리는 그대로(정의 2 는 사용자 결정으로 개정 · §0 에 동결 원문 + v3 승계 + v3.1 개정). 원장 21 = 브론즈 2판. erd_build_v31.py 가 읽는다. v3 명세는 손대지 않는다.
"""
import copy
import os
import sys
import types

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import erd_spec_v3 as V3  # noqa

for _k, _v in vars(V3).items():
    if _k.startswith("_") or isinstance(_v, types.ModuleType):
        continue
    globals()[_k] = _v

ERD_VERSION = "v3.1"
PREVIOUS_VERSION = "v3"
BRONZE_VERSION = V3.BRONZE_VERSION
BRONZE_DATE = V3.BRONZE_DATE

ENTITIES = copy.deepcopy(V3.ENTITIES)
RELATIONS = copy.deepcopy(V3.RELATIONS)
RESOLVE_RULES = copy.deepcopy(V3.RESOLVE_RULES)
TUPLE_RULES = copy.deepcopy(V3.TUPLE_RULES)
ERD_ENUMS = copy.deepcopy(V3.ERD_ENUMS)
ID_RULE = copy.deepcopy(V3.ID_RULE)
DECISION_APPLY_ORDER = copy.deepcopy(V3.DECISION_APPLY_ORDER)
QUALITY_RULES = list(V3.QUALITY_RULES)
DECISION_KINDS_NOTE_V3 = dict(V3.DECISION_KINDS_NOTE_V3)
DECISION_KINDS_NEW_V3 = list(V3.DECISION_KINDS_NEW_V3)

# ---------------------------------------------------------------------------
# 사용자 정의 3 + 명시 예외 — 동결 원문(ERD-FROZEN) · v3 승계 · v3.1 개정(정의 2 는 사용자 결정 2026-11-05)
# ---------------------------------------------------------------------------
USER_DEFINITIONS = list(V3.USER_DEFINITIONS)
USER_DEFINITIONS_V3 = list(V3.USER_DEFINITIONS_V3)
EXPLICIT_EXCEPTION = V3.EXPLICIT_EXCEPTION
USER_DEFINITION_2_V31 = ("부작용 = **(사건, 부위, 물질)** 단위. 부위는 단위를 실제로 가르는 것만 — 조직층(layer) 또는 시술 자리와 무관한 절대 부위(필러 뒤 「시력 변화」의 눈) — 이고, 상대 부위(주사 부위·시술 부위)는 none 과 같다(시술 자리는 기본값). "
                         "경과(일시·지연·지속·영구·재발)는 단위 칸이 아니라 R15 엣지 속성(어느 시술 뒤 얼마나 가나). 원인 시술은 엣지. 표현은 가리키기만 — 문구는 개체가 아니라 문구 사전 항목이며 엣지·단위의 부록이다. (사용자 결정 2026-11-05 · V3.1-9 · V3.1-10)")
USER_DEFINITIONS_V31 = [
    ("1", USER_DEFINITIONS[0][1]),
    ("2", USER_DEFINITION_2_V31),
    ("3", "원장 불변. 충돌은 레코드(④ 자동 해결도 기록). 결정 20 kind(v3 17 + product_reclassify · dictionary_remove · phrase_map) · 안정 키(REF-…#m<i>·#s<i> · PRD- 는 product_reclassify 뒤 새 id · 옛 id 는 alias · 문구 사전 항목 PHR- = 정규화형 유도) · 적용 순서 ⓪(원장 적재 때 reclassification·product_reclassify) ①~⑦(① dictionary_add → canonical_rename → dictionary_remove → phrase_map). 빌드는 approved 만 읽음. (V3.1-1 · V3.1-3 · V3.1-10)"),
]
EXPLICIT_EXCEPTION_V31 = ("부작용 축에서 **부위 없음(none) · 물질 없음(none)은 사전 값으로 본다**(사용자 결정 2026-11-05 · 경과는 단위 칸에서 나갔으므로 「경과 미상」은 더 이상 단위의 값이 아니라 엣지 속성의 빈값이다). (부종, none, none) 은 하나의 단위라 「주사 부위 부종」「일시적 부종」「경미한 부종」이 전부 같은 단위에 닿고, 「멍 (타박상)」「멍 / 반상출혈」「멍·타박상」은 (멍, none, none) 에 닿는다 — "
                          "보톡스 부종과 필러 부종은 같은 부작용이며 지속 기간은 시술의 성질(엣지)이다. 시술 축의 「미상이면 접지 않음」과 다른 이유는 v2.4 와 같다: 부작용의 부위 없음은 「모름」이 아니라 「어디서든 나는 사건」이고, 어느 시술에서 나는지는 R15 엣지가 든다. 「지연성 염증성 결절」은 단위 (결절, none, none) + 엣지 경과 지연(+ 수식어 염증성은 문구 사전 parsed)으로 표현된다. 멍·타박상·반상출혈 = 동의어 유지. 분리는 결정 event_split 으로.")
USER_DEFINITIONS_V31_NOTE = ("v3.1 은 정의 1·3 의 뜻을 뒤집지 않고, **정의 2 는 사용자 결정(2026-11-05)으로 개정**한다 — 동결 원문·v3 승계 문장은 위에 그대로 두고 v3.1 개정 문장을 아래에 둔다. 개정의 근거: 보톡스 부종·필러 부종은 같은 부작용인데 v3 까지는 (부종, none, 미상)/(부종, 주사 부위, 미상)/(부종, none, 일시) 세 단위가 임상 근거 없이 표기 차이로 갈렸다. 그래서 경과를 단위에서 빼 R15 엣지 속성으로, 상대 부위를 none 으로 둔다(명시 예외는 「부위 none · 물질 none 은 값」). "
                             "「표현은 가리키기만」은 v3.1 에서 더 강해진다 — 표현은 개체(adverse_expression)가 아니라 **문구 사전 항목**(정규화형 기준 한 줄 · 단위를 가리키는 지도)이며, 실버에서는 R15 엣지의 source_phrases[] 부록·단위의 explanations[] 부록·게이트 목록(unlinked_phrases)으로만 나타난다(V3.1-10). 조각이 전부 사전 값인 문구는 시술 참조가 튜플을 만드는 것과 같은 규칙으로 조합 단위를 세우지만(auto), 그 정체성은 사전 값 세 칸이지 표현이 아니다. 원칙 D 는 「문구는 미등록 조각이 섞인 단위를 만들지 않는다」로 고쳐 쓴다(2-C′ 가 막으려던 것은 partial 조각으로 세운 단위). 원칙 B(조각을 버리지 않는다)는 수식어·발생률·조건·설명 조각을 문구 사전 parsed 에 보존하는 것으로 지킨다(검산 N-8). "
                             "정의 3 의 「결정 kind」는 17 → 20, 적용 순서 ①~⑦ 은 그대로이고 ⓪ 에 product_reclassify 가 reclassification 옆에, ① 끝에 phrase_map 이 선다. 조건 축(V3.1-4)은 부작용 축의 원칙 A(미등록 조각이 있으면 접지 않음 — raw_name)·B(한 이름에 조건 조각 둘이면 단위 둘)를 그대로 쓰고 조건 문장은 단위·엣지의 부록이다.")
PRINCIPLES = [(k, v) if k != "D" else ("D", "표현(원장 문구)은 단위를 **가리키기만** 한다 — 문구는 개체가 아니라 문구 사전 항목·부록이며, **미등록 조각이 섞인 단위를 만들지 않는다**(조각이 전부 사전 값인 조합만 단위가 되고 그 정체성은 사전 값이지 표현이 아니다 · v3.1 V3.1-9/10 · 2-C′ 가 막으려던 것은 partial 조각으로 세운 단위).") for k, v in V3.PRINCIPLES]
PRINCIPLES_TEXT = " · ".join(f"{k}. {v}" for k, v in PRINCIPLES)

# ---------------------------------------------------------------------------
# V3.1-1 — product_reclassify
# ---------------------------------------------------------------------------
PRODUCT_RECLASSIFY_RULE = ("**product_reclassify(V3.1-1)**: 제품(PRD-)의 **계열 코드를 교체**하는 결정. target 은 PRD- id(안정 키 · 계열 코드 + 제품명으로 유도) 또는 (dictionary=product_name, canonical=제품명). new_value.to_modality_code 는 계열 코드(M코드 · modality 사전 code). "
                           "제품 id 는 계열 코드 기반(§2.6 식별자 = 계열 코드 + 정규화 제품명)이라 **재계산**되고 옛 PRD- id 는 alias(`reclassified_from`)로 남는다 — 결정·엣지가 옛 id 로 가리킨 것은 alias 로 닿는다. product_name 사전 항목의 code 도 새 계열로(DIC- id 는 사전 이름|정준값 유도라 그대로). "
                           "**R4 offers_product** 는 옛 계열 → 새 계열로 옮기고(section_key 보존 · 원장 products.json 의 category_id 와 다르면 ⑥ value_conflict 가 아니라 결정 출처 derived_from 으로 기록), **제품을 끝으로 쓰는 엣지 전부**(R3 · R27 · 시술 축 엣지 R9/R12/R15/R16/R17/R18 의 product 끝(target_depth=product))는 새 id 로. what=product 인 시술 튜플(PRC-)은 파생 id 라 재계산된다(anchor 불변). "
                           "새 (계열|제품명) 의 PRD- 가 이미 있으면(같은 이름의 제품이 그 계열에 있을 때) 그 레코드로 합치고(aliases·출처·엣지 합침 · 옛 id 는 alias) 레코드를 둘 두지 않는다. CAT- 는 taxonomy 트리 위치라 바뀌지 않는다(v2.4). "
                           "적용 ⓪ — 원장 적재 직후 reclassification 과 같은 자리(사전 단계 ① 보다 먼저: 분해·R4·엣지가 새 계열을 읽는다). 대상 예: 엑소좀 통합 ② M5 제품 ASCEplus · EXOSOME SKIN → M4(batch3-proposed EXO-02 · 값은 결정).")

# ---------------------------------------------------------------------------
# V3.1-3 — dictionary_remove
# ---------------------------------------------------------------------------
DICTIONARY_REMOVE_RULE = ("**dictionary_remove(V3.1-3)**: 사전 값의 **동의어 하나**(target.synonym 있음) 또는 **값 자체**(target.synonym 없음)를 뺀다. 값 제거는 그 값을 쓰는 레코드(사전 값이 곧 개체 식별인 개체 레코드 · 그 값을 what/site/technique/event/qualifier/조건 칸이나 R15.course 속성으로 쓰는 튜플·단위·엣지 · 그 값이 끝인 엣지)가 하나라도 있으면 **거부**(rejected · 사유 in_use — 먼저 그 레코드를 옮기거나 exclude 한다). "
                          "제거 이력은 사전에 보존한다 — 사전 레코드의 `removed_synonyms[]`(value · canonical · decision_id · removed_at) · `removed_entries[]`(canonical · id · decision_id · removed_at) — 다시 넣으려면 dictionary_add(새 결정). 빌드는 분해를 다시 돌린다(동의어가 빠지면 그 표면형은 미등록 조각이 된다). "
                          "적용 ① — 같은 단계의 dictionary_add·canonical_rename 을 **전부 적용한 뒤**(① 안에서 kind 순서 dictionary_add → canonical_rename → dictionary_remove · 그 안에서는 decided_at 순 · 같으면 id 순) — 추가한 값의 동의어를 같은 묶음에서 빼는 결정이 순서에 흔들리지 않게. 대상 예: 시장가 「PRP/엑소좀」을 M5 계열 동의어에서(EXO-06) · 「피부 괴사」를 괴사 동의어에서 빼 (괴사, 피부)로 읽기(D-6). v3 가 ERD 로 직접 뺀 「공기색전」은 사전 removed_synonyms 에 by=ERD v3(V3-1) 로 같이 기록한다(결정 id 없음 · 이력만).")

# ---------------------------------------------------------------------------
# V3.1-2 · V3.1-7 — R32 rule_applies_to · clinical_rule kind(product_note · disclosure)
# ---------------------------------------------------------------------------
R32_RULE = ("**R32 rule_applies_to(V3.1-2 · V3.1-7)**: clinical_rule → product | technique | proc_axis(계열 · 하위분류 · 시술 튜플). 속성 scope(all = 끝과 무관하게 전 계열(기법 끝 「주사 기법 전부」) · modality = 그 계열의 제품·시술 전부(끝이 계열) · product = 그 제품 하나) · severity(prohibited · caution · info — ERD 열거형 · 「불법」「금지」는 prohibited) · source_locator(규칙 문장의 원장 locator) · decision_id(edge_create 결정 · basis=edge_create 일 때) · basis(ledger | edge_create). "
            "**값의 두 길**: (a) basis=ledger — consent-checklist categories[].mandatory_disclosures[](V3.1-7)는 원장이 계열(categories[].id)로 구조화했으므로 clinical_rule(kind=disclosure) → modality 엣지를 빌드가 만든다(scope=modality · severity=info · source_locator=그 문장 locator). (b) basis=edge_create — 그 밖(제품 note 의 규칙 문장 「화장품 허가 (주사 사용 불법)」 · 이소트레티노인 대기 기간 같은 규칙 문장)은 원장이 구조화하지 않았으므로 **edge_create 로만** 값이 생긴다(from_ref = clinical_rule 의 locator(kind=locator) · to_ref = dict_value(product_name · technique · modality) 또는 anchor/procedure_tuple). "
            "제품 note·legal_warning·regulatory_status 에 규칙 문장이 있으면 clinical_rule(kind=product_note)의 **출처 후보로 열거만** 한다(§9.7.2 전수 · 레코드와 엣지는 edge_create 가 locator 를 가리킬 때 세운다 — 값 자동 생성은 하지 않는다 · 어느 문장이 「규칙」인지는 사람 판정). 끝이 product 면 product_reclassify 뒤 새 PRD- id 로 따라간다(V3.1-1).")
DISCLOSURE_RULE = ("**필수 고지(V3.1-7 · 사용자 「동의서도 테이블이 필요한 거 아니냐」)**: consent-checklist.json `categories[].mandatory_disclosures[]`(계열 17 × 문장 109)는 v3 까지 modality.mandatory_disclosures 문자열 속성이었다. v3.1 은 문장마다 **clinical_rule 레코드(kind=disclosure · text = 원문 그대로 · 식별자 = kind + 정규화 문장 — 같은 문장이 여러 계열에 있으면 레코드 하나)를 두고 R32 rule_applies_to(basis=ledger · scope=modality · severity=info · source_locator)로 그 계열(categories[].id)에 연결한다**. modality.mandatory_disclosures 속성은 뺀다(column-map 행선지 이동: modality.mandatory_disclosures → clinical_rule.text). "
                   "고지 문장 안의 부작용 조각(혈관폐색 · 괴사 · 실명 · 멍 · 부종 …)은 **같은 문장을 문구 사전(phrase_dictionary · kind=disclosure · 같은 locator) 항목으로도 두어** §1.5 규칙 그대로 단위에 닿는다 — 조각이 전부 사전 값이면 auto(단위 조합 · R15 from=그 계열 · disclosure=true · source_phrases) · 아니면 unlinked 게이트. clinical_rule(disclosure).phrase_ids 가 그 PHR- 항목을 가리킨다(파생 · 같은 locator). "
                   "「R29 유사 관계를 clinical_rule 에서 따로 두기」가 아니라 「문구 사전 항목을 하나 더 두기」를 택한 까닭(V3.1-10 과 일관): 부작용 문구의 단위 연결은 전부 문구 사전 한 길로 가고, clinical_rule 은 규칙 문장 개체로 남는다 — 한 문장이 규칙이면서 부작용 문구인 것은 원장의 사실이다. "
                   "동의서 뷰(계열별 고지 R32 + R16 금기 + emergency_signs 문구의 R15)는 **골드 뷰이며 실버 레코드로 조립 가능하다** — ERD 는 이 한 줄만 둔다. pre-procedure-checklist 의 규칙 문장(checks[].label 의 「— 대기 원칙」류)에 같은 원칙을 적용할지는 §12 관찰.")

# ---------------------------------------------------------------------------
# V3.1-4 — 조건 사전(person_condition) · 조건 문장 부록
# ---------------------------------------------------------------------------
# (canonical, [synonyms], note) — 값·동의어 전부 사람 조건 이름 9 키 값의 부분 문자열(kind=derived · 출처 횟수는 build 가 센다 · 0 이면 빌드 실패)
# 초기값 선정: 원장 이름 298 의 분해 멤버(조합 기호·괄호로 나눈 조각 · 표지어 제외)에서 조건 개념을 이루는 조각을 ERD 가 고른다(부작용 사건 사전 40 과 같은 방식).
# 동의어는 둘뿐 — (a) 괄호 동치: 이름이 「X(Y)」꼴이고 Y 가 다른 이름에서 독립 멤버로도 나타남 · (b) 표기 변형: 한랭/한냉/냉 · 병 접미. 뜻이 같은 다른 말(심장박동기 ↔ 심박조율기 · 레이노 현상 ↔ 레이노 증후군)은 합치지 않는다(결정 dictionary_add).
CONDITION_CORES = [
    ("켈로이드 체질", [], "consent·extracted·taxonomy 「켈로이드 체질」 ×10 · pre-procedure 「켈로이드 체질 확인」"),
    ("임신", [], "「임신 및 수유 중」 ×15 · 「임신/수유 중」 · 「임신 중」 · 「임신 여부」"),
    ("수유", [], "「임신 및 수유 중」 · 「수유 여부」"),
    ("임산부", [], "extracted/taxonomy 「임산부」"),
    ("자가면역질환", [], "consent 「자가면역 질환」 ×4 · pre-procedure universal 「자가면역 질환」 · 「자가면역질환 여부」(공백 변형은 정규화로 같다)"),
    ("심장박동기", ["페이스메이커"], "괄호 동치 「심장박동기(페이스메이커) 사용자」 · 「페이스메이커/전자 의료기기 여부」(독립 멤버)"),
    ("심박조율기", [], "consent 「심박조율기 또는 이식형 전자장치」 — 심장박동기와 합치지 않는다(결정)"),
    ("이식형 전자장치", [], "consent 「심박조율기 또는 이식형 전자장치」"),
    ("이식형 제세동기", [], "extracted/taxonomy 「… 또는 이식형 제세동기 사용자」"),
    ("전자 의료기기", [], "pre-procedure 「페이스메이커/전자 의료기기 여부」"),
    ("항응고제", [], "pre-procedure 「항응고제/항혈소판제」 · 「항응고제/아스피린 복용 여부」"),
    ("항혈소판제", [], "pre-procedure 「항응고제/항혈소판제」"),
    ("항응고제 복용", [], "consent 「항응고제 복용 중」 ×3 · taxonomy 항목 「항응고제 복용」 · pre-procedure 「항응고제 복용 여부」"),
    ("NSAIDs 복용", [], "consent 「NSAIDs 복용 중(…)」 · pre-procedure 「NSAIDs 복용 중단 여부 (…)」"),
    ("아스피린", [], "pre-procedure 「항응고제/아스피린 복용 여부 (멍 위험)」"),
    ("당뇨병", ["당뇨"], "표기 변형(병 접미) · consent 「조절되지 않는 당뇨」 ×3 · extracted 「당뇨병 환자」"),
    ("고혈압", [], "extracted/taxonomy 「고혈압 환자」"),
    ("신장질환", [], "extracted/taxonomy 「신장질환 환자」"),
    ("신부전", [], "consent 「심부전 또는 신부전(…)」 · pre-procedure 「심부전/신부전 여부」"),
    ("심부전", [], "consent · extracted 「심부전 환자 (…)」"),
    ("심폐질환", [], "extracted/taxonomy 「심각한 심폐질환 환자」"),
    ("허혈성 심질환", [], "extracted/taxonomy 「허혈성 심질환 (…)」"),
    ("간질", [], "consent 「간질 또는 경련 질환」 · extracted 「간질(뇌전증) 환자」(뇌전증은 독립 멤버로 없어 동의어 아님)"),
    ("경련 질환", [], "consent 「간질 또는 경련 질환」"),
    ("경련성 질환", [], "pre-procedure 「간질/경련성 질환 여부」"),
    ("신경계 질환", [], "pre-procedure 「신경계 질환 여부 (간질 등)」"),
    ("암", ["악성 종양"], "괄호 동치 「악성 종양(암)이 있는 경우」 · 「암 환자 또는 혈액암」 · consent 「악성 종양」(독립 멤버) — 출현 많은 「암」이 정준값"),
    ("혈액암", [], "consent 「암 환자 또는 혈액암」"),
    ("활동성 감염", [], "consent 「활동성 감염」 ×2 · 「활동성 감염 또는 패혈증」 · taxonomy 항목 「활동성 감염 부위」"),
    ("감염", [], "pre-procedure 「활동성 여드름/감염 부위 확인」 · 「시술 부위 감염/염증 여부」"),
    ("염증", [], "consent 「시술 부위 활동성 감염 또는 염증」 · pre-procedure 「시술 부위 감염/염증 여부」"),
    ("패혈증", [], "consent 「활동성 감염 또는 패혈증」 · pre-procedure 「활동성 감염/패혈증 여부」"),
    ("시술 부위 감염", [], "consent 「시술 부위 감염」 · 「시술 부위 감염 또는 활동성 피부질환」 · pre-procedure 「시술 부위 감염/염증 여부」"),
    ("시술 부위 활동성 감염", [], "consent 「시술 부위 활동성 감염」 ×3 · pre-procedure 「시술 부위 활동성 감염 여부」"),
    ("활동성 피부 감염", [], "consent 「활동성 피부 감염 또는 개방성 상처」 · 「활동성 피부 감염(HSV, 세균감염 등)」"),
    ("활동성 바이러스 감염", [], "extracted/taxonomy 「활동성 바이러스 감염 (단순포진 등)」"),
    ("단순포진", [], "extracted/taxonomy 「활동성 바이러스 감염 (단순포진 등)」"),
    ("만성감염", [], "pre-procedure 「피부결핵/매독 등 만성감염 여부」"),
    ("피부결핵", [], "pre-procedure 「피부결핵/매독 등 만성감염 여부」"),
    ("매독", [], "pre-procedure 「피부결핵/매독 등 만성감염 여부」"),
    ("활동성 여드름", [], "consent 「활동성 여드름 또는 피부 감염」 · pre-procedure 「활동성 여드름/감염 부위 확인」"),
    ("여드름", [], "extracted/taxonomy 「심한 여드름이 진행 중인 경우」(조각)"),
    ("헤르페스", [], "pre-procedure 「활동성 여드름/감염/헤르페스 여부」"),
    ("헤르페스 병력", [], "pre-procedure universal 「헤르페스 병력」 · 「헤르페스 병력 확인 — …」"),
    ("알레르기 병력", [], "pre-procedure universal 「알레르기 병력」 · consent 「시술 성분에 대한 알레르기 병력」(조각)"),
    ("HA 성분 알레르기", [], "pre-procedure 「HA 성분 알레르기 여부」"),
    ("히알루로니다아제 알레르기", [], "pre-procedure 「히알루로니다아제 알레르기 여부」"),
    ("광과민성 질환", [], "consent 「광과민성 질환」 · pre-procedure 「광과민성 질환/약물 복용 여부」 · extracted 「광과민성 질환이 있는 경우 (…)」"),
    ("광과민성 약물 복용", [], "consent 「광과민성 약물 복용 중」 · pre-procedure 「광과민성 질환/약물 복용 여부」(조각)"),
    ("면역억제 상태", [], "consent 「면역억제 상태」 ×2"),
    ("혈액 응고 장애", [], "consent 「혈액 응고 장애」 · extracted/taxonomy 「혈액 응고 장애가 있는 경우」"),
    ("응고장애", [], "pre-procedure 「혈액질환/응고장애 여부」 · 「출혈 경향/응고장애 여부」"),
    ("혈액질환", [], "consent 「혈소판 기능 장애 또는 혈액 질환」 · pre-procedure 「혈액질환/응고장애 여부」"),
    ("혈소판 기능 장애", [], "consent 「혈소판 기능 장애 또는 혈액 질환」 · extracted 「혈소판 기능 장애가 있는 경우」"),
    ("혈소판감소증", [], "pre-procedure 「혈소판감소증/혈액질환 여부」"),
    ("출혈 경향", [], "consent 「항응고제 복용 중 또는 출혈 경향」 · pre-procedure 「출혈 경향/응고장애 여부」"),
    ("탈장", ["헤르니아"], "괄호 동치 「헤르니아(탈장)」 · pre-procedure 「탈장 여부 (복부 시술 시)」(독립 멤버) · 「시술 부위 탈장(hernia)」"),
    ("금속 임플란트", [], "taxonomy 항목 「금속 임플란트 부위」 · pre-procedure 「금속 임플란트 확인 — …」"),
    ("시술 부위 금속 임플란트", [], "consent 「시술 부위 금속 임플란트」 ×3 · pre-procedure 「시술 부위 금속 임플란트 여부」"),
    ("체내 금속 임플란트", [], "pre-procedure 「체내 금속 임플란트 여부 (시술 부위)」 · 「체내 금속 임플란트/페이스메이커 여부」"),
    ("레이노 현상", [], "consent 「레이노 현상(중증)」 · extracted 「레이노 현상 (…)」"),
    ("레이노 증후군", [], "pre-procedure 「레이노 증후군 여부」 — 레이노 현상과 합치지 않는다(결정)"),
    ("한랭두드러기", ["한냉두드러기"], "표기 변형(한랭/한냉) · consent 「한랭 두드러기(cold urticaria)」 · extracted 「한랭두드러기 (…)」 · pre-procedure 「한냉두드러기/한냉글로불린혈증 여부」"),
    ("한랭 글로불린혈증", ["한냉글로불린혈증", "냉글로불린혈증"], "표기 변형(한랭/한냉/냉) · consent 「한랭 글로불린혈증(cryoglobulinemia)」 · pre-procedure 「한냉두드러기/한냉글로불린혈증 여부」 · extracted 「냉글로불린혈증 (…)」"),
    ("발작성 한랭 혈색소뇨증", ["발작성 한냉혈색소뇨증", "발작성 냉혈색소뇨증"], "표기 변형(한랭/한냉/냉) · consent · pre-procedure · extracted"),
    ("G6PD 결핍증", [], "extracted 「G6PD 결핍증 환자 (…)」 · pre-procedure 「G6PD 결핍증 여부 (…)」"),
    ("G6PD 결핍", [], "consent 「G6PD 결핍(비타민C 고용량 시)」 — 결핍증과 합치지 않는다(결정)"),
    ("중증근무력증", [], "consent 「신경근접합부 질환(중증근무력증 등)」 · extracted 「중증근무력증 / 루게릭병 (…) 환자」"),
    ("루게릭병", [], "extracted 「중증근무력증 / 루게릭병 (…) 환자」"),
    ("신경근접합부 질환", [], "consent 「신경근접합부 질환(중증근무력증 등)」 · pre-procedure 「… 확인」"),
    ("신경근 질환", [], "taxonomy 항목 「신경근 질환」"),
    ("신경근육 질환", [], "taxonomy 항목 「신경근육 질환」"),
    ("이소트레티노인 복용", [], "consent 「이소트레티노인 복용 중 또는 중단 후 …」 ×2 · pre-procedure 「이소트레티노인 복용 여부/중단 시점 확인 — …」"),
    ("이소트레티노인 복용력", [], "pre-procedure universal 「이소트레티노인 복용력」"),
    ("레티노이드", [], "consent 「임신 및 수유 중(특히 이소트레티노인, 레티노이드 절대 금기)」 · pre-procedure 「임신 테스트 (레티노이드 처방 시 필수)」"),
    ("흡연", [], "consent 「흡연(생착률 저하)」 · extracted 「흡연 및 경구 피임약, …」"),
    ("경구 피임약", [], "extracted/taxonomy 「흡연 및 경구 피임약, 갱년기 에스트로겐 복용 중」"),
    ("기저질환", [], "pre-procedure universal 「기저질환」"),
    ("현재 복용 약물", [], "pre-procedure universal 「현재 복용 약물」"),
    ("최근 시술 이력", [], "pre-procedure universal 「최근 시술 이력」"),
    ("시술 부위 피부 상태", [], "pre-procedure universal 「시술 부위 피부 상태」 · extracted 「시술 부위 피부 상태가 나쁜 경우나 …」"),
    ("기대치", [], "pre-procedure universal 「기대치 확인」"),
    ("활동성 피부질환", [], "consent 「시술 부위 활동성 피부질환」 · 「시술 부위 감염 또는 활동성 피부질환」 · pre-procedure 「시술 부위 감염/활동성 피부질환 여부」"),
    ("습진", [], "consent 「시술 부위 활동성 습진, 건선」 · pre-procedure 「활동성 피부염/습진/건선 여부」"),
    ("건선", [], "consent 「시술 부위 활동성 습진, 건선」 · pre-procedure 「활동성 피부염/습진/건선 여부」"),
    ("활동성 피부염", [], "pre-procedure 「활동성 피부염/습진/건선 여부」"),
    ("방사선 치료", [], "extracted/taxonomy 「방사선 치료 중인 사람」"),
    ("이물반응", [], "consent 「이물반응/육아종 병력」"),
    ("육아종", [], "consent 「이물반응/육아종 병력」"),
    ("개방성 상처", [], "consent 「활동성 피부 감염 또는 개방성 상처」"),
    ("최근 수술", [], "consent 「최근 수술(시술 부위 6주 이내)」 · extracted 「최근 수술 이력이 있는 부위」"),
    ("아미노글리코시드 항생제 복용", [], "consent 「아미노글리코시드 항생제 복용 중」 · pre-procedure 「아미노글리코시드 항생제 복용 여부 (…)」"),
    ("D-페니실라민 복용", [], "pre-procedure 「D-페니실라민 복용 여부 (…)」"),
    ("Fitzpatrick 피부타입", [], "pre-procedure 「Fitzpatrick 피부타입 확인 (I-VI)」"),
    ("20대", [], "treatment-optimization by_age_group[].age"),
    ("30대", [], "treatment-optimization by_age_group[].age"),
    ("40대", [], "treatment-optimization by_age_group[].age"),
    ("50대+", [], "treatment-optimization by_age_group[].age"),
]
CONDITION_MARKERS = ["확인", "여부", "환자", "경우", "사람", "있는", "주의", "필요", "중", "시", "등", "사용자", "장착자", "부위"]   # 표지어 — 조각이 아니라 문장 부록의 qualifier_text · 단어마다 locator ≥1 실측(검산)
CONDITION_KIND_BY_SOURCE = {"consent-checklist.json:categories[].contraindications[]": "condition", "extracted.json:{code}.contraindications.absolute[]": "condition", "extracted.json:{code}.contraindications.relative[]": "condition",
                            "taxonomy.json:modality[].extracted.contraindications.absolute[]": "condition", "taxonomy.json:modality[].extracted.contraindications.relative[]": "condition", "taxonomy.json:modality[].subcategories[].items[].extracted.safety.contraindications[]": "condition",
                            "pre-procedure-checklist.json:universal_checks[].label": "check", "pre-procedure-checklist.json:category_specific[].checks[].label": "check", "treatment-optimization.json:by_age_group[].age": "age_group"}
CONDITION_RULE = ("**조건 사전(V3.1-4 · 발주서의 condition_dictionary · 사전 이름 `person_condition`)**: 사람 조건 개체(§2.15)는 v3 까지 정규화 이름 문자열이 식별자였다(298). v3.1 은 **사전 정준값이 식별자**다 — CND-<sha256(kind|정준값)[:10]>(kind ∈ condition·check·age_group 은 원장 키에서(표 CONDITION_KIND_BY_SOURCE) · 같은 정준값이 두 kind 에서 오면 단위 둘 · 발주서 「(+ kind)」). "
                  "사전 person_condition: 정준값 · 동의어 · kind(그 값이 나타난 kind 들) · 출처 필수(값·동의어 전부 사람 조건 이름 9 키 값의 부분 문자열 · derived). 초기값은 원장 이름 298 의 분해 조각에서 ERD 가 고른 조건 핵심 " + str(len(CONDITION_CORES)) + "(부작용 사건 사전과 같은 방식 · 값마다 출처 횟수) · 동의어는 괄호 동치(이름이 「X(Y)」꼴이고 Y 가 다른 이름에서 독립 멤버로도 나타남 · 출현 많은 쪽이 정준값)와 표기 변형(한랭/한냉/냉 · 병 접미)뿐 — 뜻이 같은 다른 말은 합치지 않는다(dictionary_add 결정). "
                  "**분해(부작용 축과 같은 원칙)**: 이름 전체가 사전 값(+kind 무관)과 정규화 완전 일치하면 그대로 그 값(「50대+」처럼 조합 기호가 든 값을 쪼개지 않는다) · 아니면 이름을 괄호로 outer/inner, `· / , + 및 또는 — :` 로 멤버로 나누고 멤버마다 공백 토큰을 왼쪽부터 가장 긴 구간으로 사전(정준값·동의어 · 정규화 완전 일치)에 맞춘다. 표지어(CONDITION_MARKERS " + " · ".join(CONDITION_MARKERS) + " — 독립 토큰 · 규칙 데이터 · 단어마다 locator)는 조각이 아니라 문장 부록의 qualifier_text. 남는 토큰 = 미등록 조각. "
                  "**완전 일치만 접는다**: 이름의 조각이 전부 사전 값(+표지어)이면 멤버 안 조건 조각마다 단위 하나(원칙 B · 「임신 및 수유 중」→ (임신) + (수유)) 로 접히고, 미등록 조각이 하나라도 있으면 그 이름은 **raw_name 단위**(CND-<sha256(RAW:kind|정규화 원문)[:10]> · 같은 원문·같은 kind 는 하나 · 닿은 조각은 condition_fragments 에 보존 · 접히지 않음 · 원칙 A). 유사도·조사 분리·추측은 없다 — 「자가면역질환이 있는 경우 …」의 「자가면역질환이」는 조사가 붙어 완전 일치가 아니므로 raw_name(§12 관찰). "
                  "**문장 보존(부록 · V3.1-10 과 같은 원칙)**: 원장 문장 자리 하나(9 키 · 471)는 개체가 아니라 그 이름이 만든 단위의 `phrases[]` 부록(text · kind · locator · modality_code · level_hint · match exact|raw · 조각·미등록·표지어·괄호 원문)이고, R16/R17/R18 엣지는 `source_phrases[]`(locator)로 어느 문장에서 왔는지 든다. 문장은 단위를 세우지 않는다 — 단위는 이름이 만든다(이름 = 문장 원문이므로 문장마다 단위가 있다 · exact = 사전 단위 · raw = raw_name 단위). R16·R17·R18 의 person_condition 끝은 단위 id 다. "
                  "발주서의 「condition_expression 또는 adverse_expression 공용」 중 어느 쪽도 두지 않는 까닭: V3.1-10 이 부작용 표현 개체를 없애고 문구를 부록으로 내렸으므로, 조건 문장도 같은 원칙(문장은 개체가 아니라 단위·엣지의 부록)을 따르는 쪽이 일관된다. raw_name 조건을 사전 단위로 옮기는 길은 dictionary_add(person_condition · 동의어 = 원문 전체 또는 조각) 뒤 재분해 — 전용 kind 는 두지 않는다(§12). 실측 §9.7.")

# ---------------------------------------------------------------------------
# V3.1-5 · V3.1-6 — 회/차 자리 · stopwords 겹침
# ---------------------------------------------------------------------------
SESSION_RULE = ("**「회」·「N차」 자리(V3.1-5)**: 규격 정규식이 잡는 `\\d+회`(횟수)·`\\d+차`(회차)는 튜플 칸이 아니라 엣지 속성이다 — 참조 자리가 R12 member(annual_plans · optimal_combo · sequence · comparison · combos)이면 **R12.session_count**(회 · int)·**R12.session_index**(차 · int)로, R9/R17/R18 자리이면 엣지 속성 자리가 없으므로 **qualifier_text 에 규격 원문**(「4회」「1차」)으로만 보존한다. market-pricing(③ · 엣지 아님)은 참조 레코드의 qualifier_text. "
                "한 라벨에 회·차가 둘 이상이면 첫 값이 속성, 나머지는 qualifier_text(버리지 않음). v3 의 「`회` 는 count 로 간다」 문장은 이 속성으로 바뀐다. 실측 §9.5.12(라벨마다 자리 · 관계 · 간 곳).")
STOPWORD_OVERLAP_RULE = ("**stopwords 와 사전 값 겹침(V3.1-6)**: stopword 는 **분해 조각(토큰) 단계에서만** 제외한다 — 조각이 통째로(또는 가장 긴 토큰 구간으로) 어느 사전 값에 완전 일치하는지를 **먼저** 보고, 그 뒤 남은 독립 토큰에만 stopword 를 적용한다. 그래서 「관리」가 modality_group 사전 값(taxonomy modality[].group)과 겹쳐도 분해 사전(product · modality_subcategory · catalog_item_name · site · modality + spec)이 아닌 사전은 분해가 읽지 않으므로 충돌하지 않고, 「LDM 초음파 관리」처럼 통째 일치하는 분류 항목 이름은 떼지 않는다. "
                         "겹침 목록은 규칙 데이터(resolve_rules.stopwords.overlap · 단어 × 사전 이름 · 48 사전 전수 · 정준값·동의어)이며 **검산이 센다**(N-6: 실측 = 목록). v3 의 「사전 값과 겹치는 단어는 없다」는 분해 사전 7 기준의 문장이었고 v3.1 이 전 사전 기준으로 고친다.")

# ---------------------------------------------------------------------------
# V3.1-8 — 안전 문구 수식어 목록(adverse stopwords) · 패턴 — 미등록 조각 빈도 ≥4(erd-v3-tuples.json 부작용 축 전수)에서 고른다. 단어마다 locator 실측 · class
# ---------------------------------------------------------------------------
ADVERSE_STOPWORD_THRESHOLD = 4
ADVERSE_STOPWORDS = {
    "degree": ["경미한", "심한", "과도한", "가벼운", "약간의", "극히", "매우", "미세", "미세한", "부적절한", "비정상적", "깊은", "광범위", "강한", "낮은", "급격한", "약간", "과도", "과다", "정도", "미미", "완전", "더", "비슷한", "예상보다"],
    "timing": ["후", "시작", "직후", "초기", "지속", "지속적", "소실", "점차", "점점", "즉시", "즉각적", "일시적으로", "일시적인", "수일", "수시간", "시간", "Day", "내", "아직", "호전", "정상화", "완료", "최종", "잔존", "만성", "원래", "시점", "소요", "진행"],
    "incidence": ["드물게", "드묾", "드물음", "드문", "드물지만", "거의", "대부분", "주로", "발생률"],
    "condition": ["시", "중", "반복", "시술", "주입", "주사", "사용", "투여", "도포", "치료", "설정", "에너지", "노출", "누르면", "특히", "경우", "따라", "관리가"],
    "connector": ["and", "with", "in", "of", "is", "can", "cause"],
    "misc": ["형성", "발생", "가능", "가능성", "위험", "위험이", "의심", "징후", "현상", "느낌", "증상", "것", "수", "있음", "없음", "있습니다", "될", "생길", "보이는", "인한", "의한", "관련", "필요", "주의", "금지", "금기", "등", "안", "들", "결과", "상태", "차이", "판단", "고려", "확인", "부작용", "효과", "효과가", "변화", "감소", "증가", "악화", "약화", "개선", "생성", "오히려", "줄어들", "일으킬", "일으키는", "adverse"],
}
ADVERSE_PATTERNS = [
    ("incidence", r"^\d+(?:[.,]\d+)?(?:[-~]\d+(?:[.,]\d+)?)?%$", "백분율(1% · 0.05-0.39% · 10%)"),
    ("incidence", r"^\d[\d,]*명$", "「N명(중)」 — 455명 중 1명"),
    ("timing", r"^\d+(?:[-~]\d+)?(?:시간|일|주|개월|년|분)(?:간|째|내|이내|이상|후|이후|정도|후에)?$", "기간·시점(24시간 이상 · 1-2일 · 3-7일 · 2-3개월)"),
    ("timing", r"^\d+[-~]\d+$", "숫자 구간(Day 1-3 의 1-3)"),
    ("condition", r"^\d+(?:[.,]\d+)?(?:mL|ml|cc|mm|cm|도|U|단위)(?:로도|이상|이하|로)?$", "용량·온도 조건(0.04mL로도 · 37.5도)"),
]
ADVERSE_STOPWORD_RULE = ("**안전 문구 수식어 목록(V3.1-8 · adverse stopwords · 규칙 데이터)**: 원장 문구(문구 사전 항목)·complications 이름의 분해에서 아래 단어·패턴이 **독립 토큰**(정규화 완전 일치 · 패턴은 정규식)으로 나오면 미등록 조각이 아니라 **문구 사전 항목의 parsed 에 보존**한다 — 정도(degree) · 시간(timing) · 발생률(incidence) · 조건(condition) · 연결어(connector) · 기타(misc). 수식어를 뗀 나머지의 정규화형이 문구 사전의 키(normalized)다. "
                         "경과 사전(일시 · 지연 · 영구 · 재발 · 미상 과 동의어)에 완전 일치하는 말은 경과(course · R15 엣지 속성)로 먼저 잡힌다(사전 순서가 먼저 · 「일시적으로」「일시적인」은 경과 동의어가 아니라 시간 수식어로 남는다 — 경과 동의어 추가는 dictionary_add · §12). 「지속」은 ERD 사전(v3 값 5)에는 없고 승인된 실버 결정 DICT-COURSE-01(dictionary_add · course · ①)로 들어온다 — 결정 적용 뒤에는 「지속」「지속적」「잔여」「점진적으로 커지는」이 수식어가 아니라 경과로 읽힌다(사전 순서가 먼저 · 수식어 목록은 그 뒤). ERD 실측(결정 전)에서는 시간 수식어로 보존된다. "
                         "목록은 원장 전수 실측에서 왔다: v3 부작용 축 미등록 조각(erd-v3-tuples.json adverse.summary.unregistered_all) 중 빈도 ≥ " + str(ADVERSE_STOPWORD_THRESHOLD) + " 인 조각을 전부 검토해 수식어·연결어·기타에 드는 것만 올렸고(사건·부위·해부·기기 후보 조각 — 홍조 · 손상 · 알레르기 · 건조감 · 신경 · 각질 · 흉터 … — 은 올리지 않았다 · 그것은 dictionary_add 의 몫), 단어·패턴마다 locator ≥1 을 실측한다(검산 N-8 · 출처 없는 단어는 목록에 못 남는다). 빈도 < " + str(ADVERSE_STOPWORD_THRESHOLD) + " 조각은 목록 밖(미등록 그대로 · 목록 확장은 규칙 데이터 개정). "
                         "조사가 붙은 토큰(「멍이」「피부가」「부위가」)은 완전 일치가 아니므로 여전히 미등록이다(§12). 토큰 일부(「홍반과」의 홍반)에는 적용하지 않는다(완전 일치만 · 유사도 없음). 수식어는 사건을 정하지 않고 단위의 세 칸에도 들지 않는다 — 원칙 B(조각을 버리지 않는다)는 parsed 보존으로 지킨다.")

# ---------------------------------------------------------------------------
# V3.1-9 — 단위 (사건, 부위, 물질) · 경과는 엣지 · V3.1-10 — 문구 사전 · 부록
# ---------------------------------------------------------------------------
PHRASE_SHAPES = ["event_only", "event_site", "event_degree_course", "event_incidence_condition", "explanatory", "unresolved"]
FRAGMENT_CLASSES = ["event", "site", "relative_site", "course", "qualifier", "degree", "timing", "incidence", "condition", "connector", "misc", "explanation", "unregistered"]
UNIT_RULE = ("**부작용 단위(V3.1-9 · 사용자 정의 2 개정)**: 단위 = (사건, 부위, 물질) 세 칸 · 식별자 ADV-<sha256(event_id|site_id|qualifier_id)[:10]>. 부위 칸은 **단위를 실제로 가르는 부위만** — site 사전의 조직층(layer) · 절대 부위(anatomical · region: 필러 뒤 「시력 변화」의 눈 주변처럼 시술 자리와 무관할 수 있는 곳) — 이고 **상대 부위(relative_site: 주사 부위 · 시술 부위)는 none 과 같다**(시술 자리는 기본값 · 조각은 parsed.relative_site 에 보존). "
             "**경과(course · 일시 · 지연 · 영구 · 재발)는 단위 칸이 아니라 R15 엣지 속성**이다 — 어느 시술 뒤 얼마나 가는지는 시술의 성질(보톡스 부종과 필러 부종은 같은 단위 · 지속 기간은 엣지). 물질·기전(qualifier · adverse_qualifier 사전 · 없음 = none 값)은 v3 그대로 단위 칸. 분해 규칙(원칙 C: 사건이 놓인 멤버 안의 부위·경과·수식만 · 원칙 B: 한 칸에 후보 둘이면 단위 둘 · 경과 후보 둘이면 엣지 경과 둘)은 v2.4 그대로이고 칸만 바뀐다. "
             "complications 65 이름: 조각이 전부 사전 값이고 사건에 붙지 않은 조각이 없으면 세 칸 단위(접힘 · 이름의 경과는 category → 단위 R15 엣지의 course), 미등록 조각이나 붙지 않은 조각이 있으면 raw_name 단위(ADV-<sha256(RAW:<anchor>|none|none|<anchor>)[:10]> · 칸은 none/none · 접히지 않음 · adverse_tuple_assign 의 대상) — v2.4 원칙 A 그대로. "
             "실례: 「지연성 염증성 결절」→ 단위 (결절, none, none) + R15.course=지연(염증성은 미등록 조각이면 raw_name · 수식어 목록에 있으면 parsed). 「주사 부위 부종」→ (부종, none, none) · parsed.relative_site=주사 부위. 「혈관 폐색(미간·코)」→ (혈관 폐색, 미간, none) + (혈관 폐색, 코, none)(절대 부위는 칸). 「공기색전」→ (색전, none, 공기).")
QUALIFIER_RULE = ("**수식 칸(qualifier · V3-1 · v3.1 세 칸)**: 부작용 단위는 (event, site, qualifier) — qualifier 는 **선택** 칸으로 사건의 물질·기전(공기 · 필러 · 지방 · 혈전 — 물질 / 역행성 — 기전)을 적는다. 값은 사전 `adverse_qualifier`(값마다 원장 출처 필수 · 사전에 없는 조각은 미등록)에서만 온다. "
                  "qualifier 가 없으면 **none(값)** — 명시 예외와 같은 뜻으로 「물질·기전이 적히지 않은 사건」이지 미상이 아니다. 식별자는 qualifier 를 포함한다(ADV-sha256(event_id|site_id|qualifier_id) · 없으면 'none' · 경과는 식별자에 없다 — R15.course). "
                  "분해: 수식 조각은 원칙 C — **사건이 놓인 멤버 안의 수식 조각만** 그 사건의 qualifier 다(멤버 밖에서 가져오지 않는다). 토큰이 통째로 어느 사전에도 닿지 않으면 **접두 수식 + 사건**으로 한 번 가른다(「공기색전」→ 공기 + 색전 — 접두가 수식 사전, 나머지가 사건 사전에 완전 일치할 때만 · 유사도 아님). "
                  "한 멤버에 수식 후보가 둘 이상이면 원칙 B — 수식마다 단위. 사건에 붙지 않은 수식 조각은 extra_qualifiers 에 보존하고 그 문자열은 접지 않는다(이름 → raw_name · 문구 → unlinked). "
                  "**접힘 조건**은 「세 칸(사건 · 부위 · 물질) 전부 사전 값일 때만」(none 은 명시 예외의 값) — 「공기색전」→ (색전, none, 공기) 와 「혈관폐색/색전」의 (색전, none, none) 은 다른 단위다(접히지 않음). 문구 auto 도 세 칸 완전 일치로 단위에 닿는다. 사건 사전 동의어 「공기색전」은 v3 에서 뺐다(이력 removed_synonyms).")
_Q_SITE_RULE_V31 = V3.SITE_RULE.replace("없으면 site=none, course=미상(축의 정의값 · 검토 2-D 는 §12)", "없으면 site=none(v3.1: 경과는 칸이 아니라 R15.course · 없으면 null)") + " · v3.1(V3.1-9): 상대 부위(주사 부위 · 시술 부위) 조각은 칸이 아니라 none + parsed.relative_site(보존) · 절대 부위(anatomical·layer·region)만 칸"
PHRASE_DICTIONARY_RULE = ("**안전 문구 사전(V3.1-10 · phrase_dictionary · 사용자 「원장 문구들은 부록으로」)**: 원장 문구(extracted/taxonomy safety 문구 · 타임라인 증상 · consent 응급 징후 · 문헌 adverse_effects 문장 + 환자 설명 4개 국어 · 필수 고지)를 **정규화형(norm_v1 + 수식어 목록·패턴 토큰 제거)** 기준으로 한 줄씩 둔다 — 항목 = {id PHR-<sha256(normalized)[:10]>, normalized, raw_variants[](원문 표면형 전부), kinds[], lang, locators[](원장 자리 전부), units[](사건·부위·물질 사전 단위 ADV- id · 없으면 []), parsed{events · sites · relative_sites · courses · qualifiers · degree · timing · incidence · condition · connector · misc · explanation · phrase_shape · candidates}, status(auto | approved | unlinked), created_units[], citations[](문헌), accuracy(문헌)}. "
                          "**auto**: 조각이 전부 사전 값(사건·부위·상대 부위·경과·수식 · 수식어 목록·패턴은 조각이 아님)이고 사건에 붙지 않은 조각이 없으면 후보 (사건, 부위, 물질)마다 **단위를 만들고(없으면 생성 · 있으면 연결)** — §1.3/§1.4 에서 참조가 세 칸 전부 사전 값이면 튜플을 만드는 것과 같은 규칙 — 그 문구가 놓인 자리(계열 코드 · 항목 · 제품)에서 단위로 R15 엣지를 세운다(source_phrases[] 에 PHR- id · **course 는 그 단위의 후보 parsed.candidates[].courses — 사건이 놓인 멤버에 붙은 경과만(원칙 C · 「주사 부위 일시적 부종 및 멍」의 멍 엣지는 경과 null)** · degree/timing/incidence/condition 은 항목의 parsed 를 가리킨다). **unlinked**: 사전에 없는 조각(outer 미등록 · inner 괄호의 미등록 = 설명문 · 붙지 않은 사전 조각)이 하나라도 있거나 사건이 없으면 — 조각·후보를 항목에 보존하고 단위는 만들지 않으며(문구는 미등록 조각이 섞인 단위를 만들지 않는다 · 원칙 A · 원칙 D) 실버 개체가 아니라 **게이트 목록(unlinked_phrases)** 에만 있다. **approved**: 결정 phrase_map 이 units·parsed 를 정한 항목 — 다음 스냅샷의 같은 정규화형 문구는 결정 없이 그 지도를 따른다(auto 도 같다 · 사전이 곧 캐시). "
                          "같은 정규화형은 어느 출처에서 와도 항목 하나다(raw_variants · locators 가 늘 뿐). 문헌 레코드는 statement(영문)와 patient_ko 가 각각 항목이며 각자 판정한다(v2.4 의 「두 쪽 전부」 규칙은 레코드 단위였고 v3.1 은 문구 단위라 뺀다 · §11) · patient_en/zh/ja 는 statement 항목의 translations[] 이며 그 레코드가 닿는 단위의 explanations[] 부록으로 간다. "
                          "**부록**: 실버에서 문구는 (a) R15 엣지의 source_phrases[](PHR- id · text · kind · locator · frequency_class · phrase_shape · parsed 조각) (b) 부작용 단위의 explanations[](문헌 statement·환자 설명 등 특정 시술이 아니라 계열/단위에 대한 것 · PHR- id) (c) 게이트 unlinked_phrases(조각·후보 보존) 중 하나이며 **합이 문구 자리 수와 같다**(실측 §9.6.11: 2,935 + 고지 109). adverse_expression 개체·R29 는 없다 — 사용자 정의 2 「표현은 가리키기만」을 더 강하게 만족시킨다(표현에 정체성이 없다). "
                          "evidence_statement(moa · effects 87)는 개체로 **유지**한다 — 그것은 부작용 문구가 아니라 계열에 대한 근거 문장(R20 · R19)이고 단위에 닿는 분해 대상이 아니다. adverse_effects 문장 32 는 문구 사전으로 간다(v2 에서 adverse_expression 으로 갔던 것). R19 cites 의 from 에서 adverse_expression 을 빼고 문헌 문구의 인용은 항목의 citations[] 에 둔다. R20 의 to 는 evidence_statement 뿐.")

# ---------------------------------------------------------------------------
# 결정 kind 20 · 적용 순서
# ---------------------------------------------------------------------------
PHRASE_MAP_RULE = ("**phrase_map(V3.1-10)**: 문구 사전 항목의 지도를 사람이 정한다 — target 은 PHR- id(정규화형 유도 · 안정 키) 또는 normalized 문자열. new_value.units 는 (사건, 부위, 물질) 사전 정준값(없으면 none)의 목록(하나 이상 · 없으면 [] = 부작용 아님 판정), courses/parsed 는 선택(엣지 경과 등 덮어쓰기). 적용하면 status=approved · units 에 없는 단위는 세운다(지정값은 사전 값이어야 · 아니면 rejected 사유 dictionary). "
                   "raw_name 단위(complications 이름)는 여전히 adverse_tuple_assign(kind=raw_name) 의 몫이고 문구는 전부 phrase_map 이다. 적용 ① 끝(dictionary_add → canonical_rename → dictionary_remove → phrase_map · 지정 단위가 사전 값을 읽어야 하므로) — 그 뒤 분해·R15 가 지도를 읽는다.")
DECISION_KINDS = []
for k, br, t, nv, n in V3.DECISION_KINDS:
    if k == "canonical_rename":
        DECISION_KINDS.append((k, br, t, nv, n))
        DECISION_KINDS.append(("dictionary_remove", True, "obj(dictionary: 사전 이름, canonical: str — 정준값, synonym: str|null — 있으면 그 동의어 하나 제거 · 없으면 값 제거)", "obj(removed: true)", "v3.1(V3.1-3): " + DICTIONARY_REMOVE_RULE))
        DECISION_KINDS.append(("phrase_map", True, "obj(phrase_id: PHR-id | normalized: str — 둘 중 하나)", "obj(units: obj[](event, site, qualifier — 사전 정준값 · 없으면 none) — 없으면 [] = 부작용 아님, courses: str[]|null — 경과 사전 정준값, status: approved)", "v3.1(V3.1-10): " + PHRASE_MAP_RULE))
        continue
    if k == "reclassification":
        DECISION_KINDS.append((k, br, t, nv, n))
        DECISION_KINDS.append(("product_reclassify", True, "obj(product_id: PRD-id | product: obj(dictionary: product_name, canonical: str) — 둘 중 하나)", "obj(to_modality_code: str — 새 계열 코드(M코드))", "v3.1(V3.1-1): 적용 ⓪(원장 적재 직후 · reclassification 과 같은 자리). " + PRODUCT_RECLASSIFY_RULE))
        continue
    if k == "edge_create":
        n = n.replace("R30 leads_to(혈관 폐색 → 피부 괴사) 등", "R30 leads_to(혈관 폐색 → 피부 괴사) · R32 rule_applies_to(clinical_rule → product|technique|proc_axis · V3.1-2 · basis=edge_create · attrs scope·severity) 등")
        n = n.replace("tuple: obj(event, site, course, qualifier — 사전 정준값 · qualifier 없으면 none)", "tuple: obj(event, site, qualifier — 사전 정준값 · site·qualifier 없으면 none · v3.1 세 칸)")
        n = n + ". v3.1: dict_value 의 dictionary 에 person_condition(조건 사전 · 끝 person_condition 단위 · V3.1-4)이 들어간다 · from_ref kind=locator 가 clinical_rule 의 문장 locator(제품 note 포함)를 가리키면 그 레코드를 세운다(R32) · R15 를 결정으로 세울 때 course 는 attrs.course"
    elif k == "dictionary_add":
        n = n + ". v3.1: person_condition(조건 사전)도 대상 — 동의어 = 원문 전체 또는 조각 · 적용 뒤 조건 분해를 다시 돌린다(raw_name → 사전 단위) · new_value.kind(condition|check|age_group)는 사전 person_condition 일 때 읽는다. 문구 사전(phrase_dictionary)은 dictionary_add 가 아니라 phrase_map 으로"
    elif k == "adverse_tuple_assign":
        t = "obj(locator: 원장 locator — complications 이름(raw_name 단위의 anchor), kind: raw_name)"
        nv = "obj(tuples: obj[](event_id, site_id, qualifier_id — 없으면 'none') — 하나 이상, courses: str[]|null — 그 이름의 category → 단위 R15 엣지 경과)"
        n = ("부작용 원천에 (사건, 부위, 물질) 단위를 사람이 지정한다. v3.1(V3.1-9/10): **대상 = raw_name 단위 전부**(미등록 조각 · 붙지 않은 조각이 있는 complications 이름) — 표현 레코드는 개체가 아니므로 문구는 phrase_map 으로. raw_name 단위는 지정 단위로 대체되고 locator 가 출처로 남는다 · 지정 단위가 없으면 세운다(세 칸 사전 값이어야 · 아니면 rejected). 적용 ③. "
             "예 「카테터 관련 감염」→ (감염, none, none) 또는 수식 사전 추가 뒤 (감염, none, 카테터) · 「지연성 염증성 결절」→ (결절, none, none) + courses [지연]. V3-9: locator 가 raw_name 이면 그 자리를 세운다(거부 없음) · 미해결 anchor 규칙과 같다")
    elif k == "fold_approve":
        n = n.replace("anchor 가 가리키는 튜플 둘 이상을 하나로", "anchor 가 가리키는 튜플 둘 이상을 하나로(시술 축 · 부작용 단위는 세 칸이 같으면 이미 같은 id 라 fold 대상이 아니다)")
    DECISION_KINDS.append((k, br, t, nv, n))
DECISION_KINDS_NEW_V31 = ["product_reclassify", "dictionary_remove", "phrase_map"]
DECISION_KINDS_NOTE_V31 = {"edge_create": "V3.1-2 R32 · V3.1-4 person_condition dict_value · V3.1-9 adverse_tuple 세 칸", "dictionary_add": "V3.1-4 조건 사전 대상", "adverse_tuple_assign": "V3.1-9/10 raw_name 만 · 세 칸 + courses"}
for i, st in enumerate(DECISION_APPLY_ORDER):
    if st[0] == "①":
        DECISION_APPLY_ORDER[i] = ("①", ["dictionary_add", "canonical_rename", "dictionary_remove", "phrase_map"], st[2] + " · v3.1: dictionary_remove 는 같은 단계의 add·rename 을 전부 적용한 뒤 · phrase_map 은 맨 끝(kind 순서 · 그 안은 decided_at 순)")
DECISION_APPLY_ORDER_RULE = V3.DECISION_APPLY_ORDER_RULE.replace("① dictionary_add / canonical_rename →", "① dictionary_add / canonical_rename / dictionary_remove / phrase_map(이 순서) →").replace("원장 메모 결정(reclassification · 원장 작성자)은 ⓪ 원장 적재 때", "원장 메모 결정(reclassification · 원장 작성자)과 product_reclassify(V3.1-1)는 ⓪ 원장 적재 때(같은 자리 · decided_at 순)") + ". v3.1: ① 안에서만 kind 순서가 있다(dictionary_add → canonical_rename → dictionary_remove → phrase_map)"
DECISION_TARGET_RULE = V3.DECISION_TARGET_RULE.replace("원장에서 직접 나온 고정 id(MOD-/SUB-/PRD-/SIT-/TEC-)", "원장에서 직접 나온 고정 id(MOD-/SUB-/PRD-/SIT-/TEC- · v3.1: PRD- 는 product_reclassify 가 계열 코드를 바꾸면 재계산되고 옛 id 는 alias(reclassified_from)로 닿는다)").replace("사전 값(사전 이름 + 정준값)", "사전 값(사전 이름 + 정준값 · v3.1: 조건 사전 person_condition 포함 — 조건 단위 CND- 는 사전 값으로 가리킨다 · 문구 사전 항목 PHR-(정규화형 유도)도 안정 키)").replace("부작용 튜플은 (event, site, course, qualifier — 없음은 none) 사전 값 네 쌍으로(R-4)", "부작용 단위는 (event, site, qualifier — 없음은 none) 사전 값 세 쌍으로(V3.1-9)") + ". v3.1: CND-(조건 단위 · 사전 정준값 유도) · 문구 자리는 locator 또는 PHR- 로 가리킨다"
for i, (no, cls, rule) in enumerate(QUALITY_RULES):
    if no == "⑨":
        QUALITY_RULES[i] = (no, cls, rule + ". v3.1(V3.1-4): 조건 raw_name 단위는 ⑧ unregistered_value(미등록 조각)로 센다 — 참조 깨짐이 아니다. v3.1(V3.1-10): 문구 unlinked 는 게이트 unlinked_phrases(⑧ 미등록 조각 · 후보 보존)")

# ---------------------------------------------------------------------------
# 식별자
# ---------------------------------------------------------------------------
ID_RULE["product"] = ("PRD-<sha256(계열 코드|norm(제품명))[:10]> — v3.1(V3.1-1): product_reclassify 가 계열 코드를 바꾸면 재계산 · 옛 id 는 aliases(reclassified_from) · 새 (계열|제품명) 의 PRD- 가 이미 있으면 그 레코드로 합침")
ID_RULE["adverse_effect"] = ("v3.1(V3.1-9): 세 칸(event · site · qualifier) 전부 사전 값이면(미등록 조각 0 · 붙지 않은 조각 0 · event_kind=dict) ADV-<sha256(event_id|site_id|qualifier_id)[:10]>, raw_name 단위는 ADV-<sha256(RAW:<anchor>|none|none|<anchor>)[:10]> — event_id = 사건 사전 id, site_id = site 개체 id(anatomical·layer·region 만 · 상대 부위는 'none') | 'none', qualifier_id = adverse_qualifier 사전 id | 'none'(없음은 값), anchor = 그 이름의 원장 locator. "
                             "경과는 식별자에 없다(R15.course). 단위는 complications 65 이름과 auto 문구(문구 사전 · 조각 전부 사전 값)에서 생긴다 — 같은 세 칸은 어느 출처에서 와도 같은 id")
ID_RULE["person_condition"] = ("v3.1(V3.1-4): 사전 단위 CND-<sha256(kind|정준값)[:10]>(kind ∈ condition·check·age_group · 정준값 = 사전 person_condition) · raw_name 단위 CND-<sha256(RAW:kind|norm(원문))[:10]>(같은 원문·같은 kind 는 하나 · anchor = 첫 locator · 전 locator 는 phrases[]). v3 의 CND-<sha256(정규화 이름)> 은 쓰지 않는다")
ID_RULE["phrase"] = "PHR-<sha256(normalized)[:10]> — normalized = 수식어 목록·패턴 토큰을 뺀 토큰들의 norm_v1 연결(공백 없음). 문구 사전 항목 id · 안정 키의 조건(S-5): 원장 바이트·수식어 목록·**경과 사전과 분해 사전(사건·부위·상대 부위·수식)** 이 같을 때 같다 — 경과·수식어·사전 값이 바뀌면(dictionary_add 「지속」 뒤 「안면 비대칭 지속」이 별 항목으로 갈리듯) 정규화형이 바뀔 수 있으므로, 옛 항목(approved 포함)은 **raw_variants 로 새 항목에 재귀속**하고 옛 PHR- 는 alias 로 남긴다(결정 target 이 끊기지 않게)"
ID_RULE["clinical_rule"] = "RUL-<sha256(kind|정규화 문장)[:10]> — v3.1: kind 에 disclosure(필수 고지) · product_note(제품 note 규칙 문장 · edge_create 가 세울 때만) 추가. 같은 고지 문장이 여러 계열에 있으면 레코드 하나 · R32 여럿"
ID_RULE["adverse_expression"] = "v3.1(V3.1-10): 개체가 아니다 — 문구 자리는 원장 locator 로, 정규화형은 PHR- 로 가리킨다(v3 의 AEX- 는 쓰지 않는다)"
ID_RULE["adverse_expression_candidates"] = "v3.1: 문구 사전 항목의 parsed.candidates[] = (event, site, qualifier) 후보 + would_be_id(ADV-sha256(event_id|site_id|qualifier_id)) + exists — auto 면 단위가 있다(없으면 생성)"
ID_RULE["decision_target"] = DECISION_TARGET_RULE

# ---------------------------------------------------------------------------
# 개체 — 21 − adverse_expression = 20
# ---------------------------------------------------------------------------
ENTITIES = [e for e in ENTITIES if e["key"] != "adverse_expression"]


def _ent(key):
    return next(e for e in ENTITIES if e["key"] == key)


# V3.1-1 product
_pr = _ent("product")
_pr["identity"] = "계열 코드 + 정규화 제품명 (survey 제품은 계열 코드 없으면 'survey' + 정규화 display_name; 원장 대응이 되면 원장 제품 id 를 쓰고 step1 쪽은 alias). v3.1(V3.1-1): product_reclassify 가 계열 코드를 바꾸면 PRD- 재계산 · 옛 id 는 alias(reclassified_from)"
_pr["definition"] += " v3.1(V3.1-1): 계열은 결정 product_reclassify(⓪)로 옮길 수 있다 — id 재계산 · 옛 id alias · R4 이동 · 제품 끝 엣지 전부 새 id(§5.2). v3.1(V3.1-2): note·legal_warning·regulatory_status 의 규칙 문장은 clinical_rule(kind=product_note) 출처 후보로 열거된다(§9.7.2 · 레코드·R32 는 edge_create 로만)."
_pr["attrs"].append(("reclassified_from", "str[]|null", False, [], "v3.1(V3.1-1): product_reclassify 로 계열이 바뀐 제품의 옛 PRD- id(alias) · 바뀐 적 없으면 null"))

# V3.1-7 modality — mandatory_disclosures 속성 삭제
_mo = _ent("modality")
_mo["attrs"] = [a for a in _mo["attrs"] if a[0] != "mandatory_disclosures"]
_mo["definition"] += " v3.1(V3.1-7): 필수 고지(consent mandatory_disclosures[])는 속성이 아니라 clinical_rule(kind=disclosure) 레코드이며 R32 rule_applies_to(basis=ledger)로 이 계열에 닿는다 — 동의서 뷰는 골드에서 조립한다."

# V3.1-2 · V3.1-7 clinical_rule
_cr = _ent("clinical_rule")
_cr["definition"] = ("특정 개체에 자동으로 붙일 수 없는 원칙·규칙·안전 사실 문장(29). 사람이 결정 개체로 시술 쌍·부작용에 연결할 때까지 독립 개체로 둔다. v3.1(V3.1-2): R32 rule_applies_to 로 제품·기법·시술 축에 닿는다(basis edge_create · 값은 결정으로만). v3.1(V3.1-7): kind=disclosure — consent 필수 고지 문장(계열 17 × 109 · 원문 그대로 · locator) · R32(basis=ledger)로 그 계열에 · 같은 문장의 문구 사전 항목(kind=disclosure)이 부작용 단위에 닿는다(phrase_ids). kind=product_note — 제품 note 규칙 문장(출처 후보 열거 · edge_create 가 세울 때만 레코드). " + DISCLOSURE_RULE)
_cr["identity"] = "kind + 정규화 문장 (v3.1: disclosure 도 같은 규칙 — 같은 문장이 여러 계열에 있으면 레코드 하나 · R32 여럿)"
_crattrs = []
for a in _cr["attrs"]:
    if a[0] == "kind":
        a = ("kind", "enum(principle|combination_rule|critical_safety_fact|disclosure|product_note)", True, [], "v3.1: disclosure = consent mandatory_disclosures[](V3.1-7) · product_note = 제품 note·legal_warning·regulatory_status 의 규칙 문장(V3.1-2 · edge_create 가 locator 를 가리킬 때만 레코드)")
    elif a[0] == "text":
        a = ("text", "str", True, list(a[3]) + ["consent-checklist.json:categories[].mandatory_disclosures[]", "products.json:prp_exosome.products[].legal_warning", "products.json:prp_exosome.products[].regulatory_status", "products.json:*.products[].note", "taxonomy.json:modality[].products[].note"], a[4] + " · v3.1: 고지 문장은 원문 그대로(V3.1-7) · 제품 note 키는 후보 출처(product_note · 레코드는 결정 뒤)")
    _crattrs.append(a)
_crattrs += [
    ("source_locator", "str", True, [], "v3.1: 문장의 원장 locator(식별 보조 · R32.source_locator 와 같다 · 같은 문장이 여러 자리면 전부 sources)"),
    ("modality_codes", "str[]", False, ["consent-checklist.json:categories[].id"], "v3.1(V3.1-7): disclosure 가 놓인 계열 코드 전부(= R32 basis=ledger 의 끝)"),
    ("phrase_ids", "str[]|null", False, [], "v3.1(V3.1-7): disclosure 의 같은 locator 로 만든 문구 사전 항목(kind=disclosure)의 PHR- id — 부작용 단위 연결은 그쪽(R15 source_phrases). 그 밖 kind 는 null"),
]
_cr["attrs"] = _crattrs

# V3.1-4 person_condition (개체 식별 변경 · 문장 부록)
_pc = _ent("person_condition")
_pc["definition"] = ("시술 대상자의 상태·병력·복용·체질·연령대. 금기(절대/상대)·동의서 금기·시술 전 확인 항목·연령대 권고가 모두 이 개체와의 엣지. v3.1(V3.1-4): **조건 단위** — 식별자는 문자열이 아니라 조건 사전(person_condition)의 정준값(+kind)이고, 원장 이름이 사전 값(+표지어)으로 완전히 분해되지 않으면 raw_name 단위(접히지 않음). 원장 문장은 phrases[] 부록으로 보존된다. " + CONDITION_RULE)
_pc["identity"] = ID_RULE["person_condition"]
_SRC_COND = [k for k in CONDITION_KIND_BY_SOURCE]
_pc["attrs"] = [
    ("name", "str", True, list(_SRC_COND), "v3.1: 사전 단위 = 사전 정준값 · raw_name 단위 = 이름 원문. 반복 문자열(임신 및 수유 중 15회)은 하나로 병합(같은 정규화 원문 · 같은 kind)"),
    ("name_kind", "enum(dict|raw_name)", True, [], "v3.1(V3.1-4): dict = 사전 정준값 단위(접힘 가능) · raw_name = 미등록 조각이 있는 이름 자신(접히지 않음 · dictionary_add 의 대상)"),
    ("kind", "enum(condition|check|age_group)", True, [], "원장 키에서(CONDITION_KIND_BY_SOURCE) · 식별자에 들어간다"),
    ("dictionary_id", "str|null", False, [], "v3.1: 사전 person_condition 항목 DIC- id(dict 단위) · raw_name 은 null"),
    ("candidate_name", "str[]", True, list(_SRC_COND), "v3.1: raw_name 단위의 미등록 조각(사전 추가의 재료) · dict 단위는 []"),
    ("condition_fragments", "str[]", True, [], "v3.1: 이름에서 사전에 닿은 조건 조각 전부(실값 · 버리지 않는다) · dict 단위는 [정준값]"),
    ("qualifier_text", "str[]", True, [], "v3.1: 표지어(CONDITION_MARKERS)로 뗀 토큰 원문 — 조각이 아니다"),
    ("anchor", "str|null", True, [], "v3.1: raw_name 단위의 원장 locator(첫 자리 · 전 자리는 phrases[]) · dict 단위는 null"),
    ("phrases", "obj[](text, kind, locator, modality_code, level_hint, match exact|raw, condition_fragments, unregistered_fragments, qualifier_text, explanation_text)", True, list(_SRC_COND), "v3.1(V3.1-4 · V3.1-10 과 같은 원칙): 이 단위를 만든 원장 문장 자리 전부(부록 · 개체 아님) — 문장은 단위를 세우지 않는다(단위는 이름이 만든다)"),
    ("description", "str", False, ["pre-procedure-checklist.json:universal_checks[].description"], ""),
    ("universal", "bool", False, [], "pre-procedure universal_checks = true (계열 엣지 없이 전 계열 적용)"),
    ("universal_level", "dict:condition_level", False, ["pre-procedure-checklist.json:universal_checks[].type"], ""),
    ("maintenance", "str", False, ["treatment-optimization.json:by_age_group[].maintenance"], "연령대만"),
    ("annual_focus", "str", False, ["treatment-optimization.json:by_age_group[].annual_focus"], "연령대만"),
    ("note", "str", False, ["treatment-optimization.json:by_age_group[].note"], ""),
]

# V3.1-9 adverse_effect — 세 칸
_a = _ent("adverse_effect")
_a["definition"] = ("독립 개체 · **(사건, 부위, 물질) 단위**(v3.1 V3.1-9 · 사용자 정의 2 개정). 시술·계열·제품·부위와 엣지(R15)로만 연결되고 등급·발생률·시기·**경과**·지속·대처는 엣지 속성. 단위는 complications 65 이름과 auto 문구(문구 사전 · 조각 전부 사전 값)에서 생긴다 — 같은 세 칸은 어느 출처에서 와도 같은 단위. " + UNIT_RULE + " 원칙 A~D 는 §0(v3.1 문장).")
_a["aliases"] = "없음 (표면형은 사건 사전 동의어 · 문구 표면형은 문구 사전 항목 raw_variants)"
_a["identity"] = "sha256(event_id|site_id|qualifier_id)[:10] — 세 칸 전부 사전 값일 때(site·qualifier 없음 = 'none' 값 · 상대 부위는 none). raw_name 단위는 sha256(RAW:anchor|none|none|anchor) — 이름마다 고유"
_aattrs = []
for a in _a["attrs"]:
    n = a[0]
    if n in ("course", "course_id", "course_basis", "extra_courses"):
        continue
    if n == "event_kind":
        a = (n, a[1], True, [], "dict = 사건 사전 값(세 칸 전부 사전 값 — complications 이름 또는 auto 문구 유래 · 접힘 가능) · raw_name = complications 이름에 미등록 조각이 있거나 사건에 붙지 않은 조각이 남아(이름 자신이 사건 자리 · 접히지 않음 · adverse_tuple_assign 대상)")
    elif n == "site_ref_kind":
        a = (n, "enum(site|none)", True, a[3], "v3.1: site 개체(R31 · anatomical·layer·region) | none — 상대 부위(relative_site)는 none(조각은 R15/문구 parsed.relative_site)")
    elif n == "site_ref_id":
        a = (n, a[1], True, a[3], "v3.1: site 개체 id(anatomical·layer·region) 또는 none — 상대 부위 사전 id 는 칸에 오지 않는다(none · relative_site_text 보존). 부위 규칙: " + _Q_SITE_RULE_V31)
    elif n == "all_dict_values":
        a = (n, a[1], a[2], a[3], "v3.1: event 가 사전 값이고 미등록 조각 0 · 붙지 않은 조각 0 이면 true — 그때만 접힘(site none · qualifier none 은 명시 예외의 값 · 경과는 칸이 아니다)")
    elif n == "status":
        a = ("status", "enum(complete|partial|unresolved)", True, [], "complete = 미등록 조각 0 · 붙지 않은 조각 0(사전 단위) · partial = 미등록 조각 ≥1(raw_name) · unresolved = 미등록 0 이지만 사건에 붙지 않은 부위·경과·수식 조각이 남음(raw_name)")
    elif n == "origins":
        a = (n, a[1], True, a[3], "v3.1: 이 단위를 만든 원천 — complications · 또는 auto 문구의 kind(safety_phrase · symptom_phrase · emergency_sign · evidence_statement · patient_text · disclosure)")
    elif n == "extra_sites":
        a = (n, a[1], True, [], "사건에 붙지 않은 부위 조각 전부(raw_name · 원칙 B 보존). dict 단위는 []")
    elif n == "dict_tuples":
        a = ("dict_tuples", "obj[](event, site, course, qualifier)|null", False, [], "raw_name 단위에 §1.5 사전 분해 결과를 보존만(course 포함 — 엣지 경과의 재료 · 단위 칸이 아니다). dict 단위는 null")
    _aattrs.append(a)
    if n == "site_basis":
        _aattrs.append(("relative_site_text", "str[]", True, [], "v3.1(V3.1-9): 이름에서 사건에 붙은 상대 부위 조각(주사 부위 · 시술 부위) — 칸은 none · 보존"))
        _aattrs.append(("created_by_phrase", "str|null", False, [], "v3.1(V3.1-10): 이 단위를 처음 세운 문구 사전 항목 PHR- id(complications 유래면 null)"))
        _aattrs.append(("explanations", "obj[](phrase_id, kind, lang, locator)", True, [], "v3.1(V3.1-10): 특정 시술이 아니라 단위에 대한 문구 부록 — 문헌 statement·환자 설명(translations)·auto 문구 전부(phrase_id)"))
_a["attrs"] = _aattrs

# decision 정의
_d = _ent("decision")
_d["definition"] += " v3.1: kind 20(+product_reclassify ⓪ · +dictionary_remove ① · +phrase_map ①) · edge_create 가 R32 와 조건 사전 dict_value 와 세 칸 adverse_tuple 을 받는다."
for i, a in enumerate(_d["attrs"]):
    if a[0] == "kind":
        _d["attrs"][i] = ("kind", "enum(" + "|".join(k[0] for k in DECISION_KINDS) + ")", True, [], "§5.2 표(20 · v3 17 + v3.1 product_reclassify · dictionary_remove · phrase_map). 빌드 적용 kind(build_reads=true): " + " · ".join(k[0] for k in DECISION_KINDS if k[1]) + " · 적용 순서 §5 표")
_ev = _ent("evidence_statement")
_ev["definition"] += " v3.1(V3.1-10): 개체 유지 — moa·effects 는 계열 근거 문장(R20·R19)이고 단위에 닿는 분해 대상이 아니다. adverse_effects 문장 32 는 문구 사전(kind=evidence_statement)으로."
_cf = _ent("conflict")
_cf["definition"] += " v3.1(V3.1-10): 문구 unlinked 는 게이트 unlinked_phrases(⑧ · 조각·후보 보존)."

# ---------------------------------------------------------------------------
# 관계 — 31 − R29 + R32 = 32
# ---------------------------------------------------------------------------
RELATIONS = [r for r in RELATIONS if r["id"] != "R29"]


def _rel(rid):
    return next(r for r in RELATIONS if r["id"] == rid)


_r12 = _rel("R12")
_r12["attrs"] = [a if a[0] != "session_index" else ("session_index", "int|null", "v3(V3-3) · v3.1(V3.1-5): 회차 수식(「1차」) — 규격 `\\d+차` 에서 · R12 자리에만(R9/R17/R18 는 qualifier_text)") for a in _r12["attrs"]]
_r12["attrs"].append(("session_count", "int|null", "v3.1(V3.1-5): 횟수 수식(「4회」「3회 패키지」) — 규격 `\\d+회` 에서 · R12 자리에만 · 둘 이상이면 첫 값(나머지는 qualifier_text)"))
_r12["note"] = (_r12["note"] or "") + " · v3.1(V3.1-5): " + SESSION_RULE
for rid in ("R9", "R17", "R18"):
    r = _rel(rid)
    r["attrs"] = [a if a[0] != "qualifier_text" else ("qualifier_text", "str[]", "v3(V3-3): stopwords 로 뗀 수식어 원문 · v3.1(V3.1-5): 이 자리의 `\\d+회`·`\\d+차` 규격 원문도 여기(엣지 속성 자리 없음)") for a in r["attrs"]]
    r["note"] = (r["note"] or "") + " · v3.1(V3.1-5): 회·차 규격은 qualifier_text 만(R12 가 아니다)"
for rid in ("R16", "R17", "R18"):
    r = _rel(rid)
    r["attrs"] = list(r["attrs"]) + [("source_phrases", "str[]", "v3.1(V3.1-4): 이 엣지를 낸 조건 문장의 원장 locator 전부(단위 phrases[] 부록의 키)")]
_r16 = _rel("R16")
_r16["note"] = (_r16["note"] or "") + " · v3.1(V3.1-4): person_condition 끝은 조건 단위 id(CND- · 사전 단위 또는 raw_name 단위) — 문장이 아니라 그 문장이 만든 단위. level 은 문장의 level_hint·원장 키에서"
_r17 = _rel("R17")
_r17["note"] = (_r17["note"] or "") + " · v3.1(V3.1-4): from 은 age_group 단위(사전 person_condition kind=age_group · 20대 …)"
_r18 = _rel("R18")
_r18["note"] = (_r18["note"] or "") + " · v3.1(V3.1-4): person_condition 끝은 조건 단위 id"
_r15 = _rel("R15")
_r15["attrs"] = [a for a in _r15["attrs"] if a[0] != "expression_id"] + [
    ("course", "dict:course[]|null", "v3.1(V3.1-9 · S-1): **경과는 엣지 속성** — 그 단위의 사건이 놓인 멤버에 붙은 경과 조각만(원칙 C · 일시 · 지연 · 영구 · 재발 · 둘 이상이면 전부) · 없으면 null(미상). 문구 유래면 source_phrases 항목의 **parsed.candidates[단위].courses**(항목 전체 parsed.courses 가 아니다 — 「주사 부위 일시적 부종 및 멍」의 멍 엣지는 null), 이름 유래면 그 이름의 dict_tuples 중 그 사건의 경과. 경과 값 집합 = course 사전(ERD 값 5 · 결정 dictionary_add 로 확장 가능 — 승인된 실버 결정 DICT-COURSE-01 「지속」이 ① 에서 들어오면 그 뒤 「지속」「지속적」은 수식어가 아니라 경과로 읽힌다)"),
    ("source_phrases", "str[]", "v3.1(V3.1-10): 이 엣지를 낸 문구 사전 항목 PHR- id 전부(부록 — text · kind · locator · frequency_class · phrase_shape · parsed 조각은 항목에 있다) · complications 유래면 []"),
    ("degree_text", "ref(PHR- · parsed.degree)|null", "v3.1(V3.1-8): 값 복사가 아니라 문구 사전 항목 참조"),
    ("timing_text", "ref(PHR- · parsed.timing)|null", "v3.1(V3.1-8): 문구 사전 항목 참조"),
    ("incidence_text", "ref(PHR- · parsed.incidence)|null", "v3.1(V3.1-9): 발생률 조각 — 문구 사전 항목 참조(incidence 문자열 속성과 별개 · 문구에서 온 것)"),
    ("condition_text", "ref(PHR- · parsed.condition)|null", "v3.1(V3.1-9): 조건 조각 — 문구 사전 항목 참조"),
    ("created_by_phrase", "bool", "v3.1(V3.1-10): 끝 단위를 문구가 세웠으면 true"),
    ("disclosure", "bool", "v3.1(V3.1-7): 고지 문장(kind=disclosure) 유래면 true · from = 그 계열"),
]
_r15["sources"] = list(_r15["sources"]) + [s_ for s_ in next(r for r in V3.RELATIONS if r["id"] == "R29")["sources"] if s_ not in _r15["sources"]] + ["consent-checklist.json:categories[].mandatory_disclosures[]"]   # v3.1: R29 가 들던 문구 출처는 R15 가 든다
_r15["note"] = (_r15["note"] or "").replace("표현 유래 엣지(expression_id)는 그 표현이 R29 exact 일 때만 생긴다 — 끝은 기존 단위(complications 65 유래 튜플) · 표현이 세운 튜플은 없다", "v3.1(V3.1-10): 문구 유래 엣지는 문구 사전 항목이 auto|approved 일 때 생기고 끝 단위는 문구가 세웠을 수 있다(created_by_phrase) · 경과·정도·시간·발생률·조건은 항목 parsed 를 참조") + " · v3.1(V3.1-9): 경과는 이 엣지의 course 속성(단위 칸이 아니다)"
_r19 = _rel("R19")
_r19["from"] = "evidence_statement|clinical_rule"
_r19["note"] = "v3.1(V3.1-10): 문헌 adverse_effects 문구의 인용은 문구 사전 항목의 citations[] 에(개체 아님) · clinical_rule(disclosure)는 인용 없음"
_r20 = _rel("R20")
_r20["to"] = "evidence_statement"
_r20["note"] = "코드 키로 확정. v3.1(V3.1-10): adverse_effects 문장은 문구 사전 항목이며 단위의 explanations[] 부록으로 간다(이 관계의 끝이 아니다)"
_r31 = _rel("R31")
_r31["note"] = (_r31["note"] or "") + " · v3.1(V3.1-9): 끝은 anatomical·layer·region 만 — 상대 부위는 none(엣지 없음 · 단위 relative_site_text)"
_r30 = _rel("R30")
_r30["note"] = _r30["note"].replace("(event, site, course, qualifier — 없음은 none) 사전 값 네 쌍(R-4)", "(event, site, qualifier — 없음은 none) 사전 값 세 쌍(V3.1-9)")
_r4 = _rel("R4")
_r4["note"] = (_r4["note"] or "") + " · v3.1(V3.1-1): product_reclassify(⓪)가 적용되면 from 은 새 계열(원장 category_id 와 다르면 결정 derived_from) · 끝 PRD- 는 새 id"
for rid in ("R3", "R27"):
    r = _rel(rid)
    r["note"] = (r["note"] or "") + " · v3.1(V3.1-1): 제품 끝은 product_reclassify 뒤 새 PRD- id(옛 id alias)"
RELATIONS.append({"id": "R32", "name": "rule_applies_to", "from": "clinical_rule", "to": "product|technique|proc_axis", "card": "N:M",
                  "attrs": [("scope", "enum(all|modality|product)", "v3.1(V3.1-2): all = 끝과 무관하게 전 계열(기법 끝) · modality = 그 계열의 제품·시술 전부(끝이 계열) · product = 그 제품 하나"),
                            ("severity", "enum(prohibited|caution|info)", "v3.1(V3.1-2): ERD 열거형(원장 출처 없음) — 「불법」「금지」prohibited · 주의 caution · 고지 info(disclosure 기본)"),
                            ("source_locator", "str", "v3.1: 규칙 문장의 원장 locator(clinical_rule.source_locator 와 같다)"),
                            ("decision_id", "str|null", "v3.1: edge_create 결정 id(basis=edge_create) · ledger 면 null"),
                            ("basis", "enum(ledger|edge_create)", "v3.1(V3.1-7): ledger = consent mandatory_disclosures → 계열(빌드가 만든다) · edge_create = 그 밖(결정으로만)"),
                            ("target_depth", "enum(modality|subcategory|procedure|product|technique)", "v3.1: 끝의 깊이")],
                  "sources": ["consent-checklist.json:categories[].id", "consent-checklist.json:categories[].mandatory_disclosures[]"],
                  "note": R32_RULE + " proc_axis 끝은 v2.3 엣지 끝 규칙(튜플 또는 그 층까지만 적힌 노드)을 따른다."})
PROC_AXIS_EDGES = list(V3.PROC_AXIS_EDGES) + ["R32"]

ERD_ENUMS["decision.kind"] = [k[0] for k in DECISION_KINDS]
ERD_ENUMS["decision.apply_order"] = [" / ".join(ks) for _, ks, _ in DECISION_APPLY_ORDER]
ERD_ENUMS["clinical_rule.kind"] = ["principle", "combination_rule", "critical_safety_fact", "disclosure", "product_note"]
ERD_ENUMS["adverse_expression.kind"] = ["evidence_statement", "symptom_phrase", "emergency_sign", "patient_text", "safety_phrase", "disclosure"]   # v3.1: 문구 사전 항목 kind (열거형 키 이름은 적합성 열거기 호환으로 유지)
ERD_ENUMS["adverse_expression.match_status"] = ["auto", "approved", "unlinked"]   # v3.1: = phrase_dictionary.status (키 이름은 열거기 호환)
ERD_ENUMS["adverse_expression.unlinked_reason"] = ["unregistered", "unattached_fragments", "no_event"]
ERD_ENUMS["phrase_dictionary.status"] = ["auto", "approved", "unlinked"]
ERD_ENUMS["phrase_dictionary.kind"] = list(ERD_ENUMS["adverse_expression.kind"])
ERD_ENUMS["phrase_dictionary.phrase_shape"] = list(PHRASE_SHAPES)
ERD_ENUMS["phrase_dictionary.fragment_class"] = list(FRAGMENT_CLASSES)
ERD_ENUMS["adverse_stopword.class"] = ["degree", "timing", "incidence", "condition", "connector", "misc"]
ERD_ENUMS["adverse_effect.site_ref_kind"] = ["site", "none"]
ERD_ENUMS["R32.scope"] = ["all", "modality", "product"]
ERD_ENUMS["R32.severity"] = ["prohibited", "caution", "info"]
ERD_ENUMS["R32.basis"] = ["ledger", "edge_create"]
ERD_ENUMS["person_condition.name_kind"] = ["dict", "raw_name"]
ERD_ENUMS["person_condition.kind"] = ["condition", "check", "age_group"]
ERD_ENUMS["condition_phrase.match"] = ["exact", "raw"]

# ---------------------------------------------------------------------------
# 분해 규칙 §1.3 · 튜플 규칙 (데이터)
# ---------------------------------------------------------------------------
RESOLVE_RULES["name"] = "decompose_v3_1"
_sw = RESOLVE_RULES["step2_decompose"]["stopwords"]
_sw["rule"] = V3.STOPWORD_RULE.replace("`차` 는 R12 엣지 `session_index`, `회` 는 count 로 간다", "`차` 는 R12 엣지 `session_index`, `회` 는 R12 엣지 `session_count` 로 간다(R9/R17/R18 자리면 qualifier_text 만 · V3.1-5)").replace("사전 값과 겹치는 단어는 없다(검산).", "분해 사전 밖 사전 값과 겹치는 단어는 overlap 목록(V3.1-6 · 검산이 센다)에 적는다 — 통째 일치가 먼저라 충돌하지 않는다.")
STOPWORD_RULE = _sw["rule"]
_sw["session_rule"] = SESSION_RULE
_sw["count_target"] = "R12.session_count (R9|R17|R18|market-pricing 은 qualifier_text)"
_sw["session_target"] = "R12.session_index (R9|R17|R18|market-pricing 은 qualifier_text)"
_sw["overlap_rule"] = STOPWORD_OVERLAP_RULE
_sw["overlap"] = []   # build 가 사전 전수에서 채운다 — [{word, dictionaries:[{name, canonical, as}]}]
RESOLVE_RULES["step2_decompose"]["dictionary_order_note"] += " · v3.1(V3.1-6): stopword 제외는 사전 통째 일치 뒤(조각 단계)"
RESOLVE_RULES["step3_assemble"]["session"] = {"rule": SESSION_RULE, "r12": ["session_index", "session_count"], "others": "qualifier_text"}

TUPLE_RULES["name"] = "tuples_v3_1"
TUPLE_RULES["user_definitions"] = [{"no": n, "text": t} for n, t in USER_DEFINITIONS]
TUPLE_RULES["user_definitions_v31"] = [{"no": n, "text": t} for n, t in USER_DEFINITIONS_V31]
TUPLE_RULES["explicit_exception_v31"] = EXPLICIT_EXCEPTION_V31
TUPLE_RULES["principles"] = [{"key": k, "text": v} for k, v in PRINCIPLES]
_P = TUPLE_RULES["procedure"]
_P["stopwords"] = STOPWORD_RULE
_P["session"] = SESSION_RULE
_P["stopword_overlap"] = STOPWORD_OVERLAP_RULE
_P["qualifiers"] = _P["qualifiers"] + " · v3.1(V3.1-5): `\\d+회` 는 R12 session_count · `\\d+차` 는 R12 session_index · R9/R17/R18 자리는 qualifier_text 만"
_Q = TUPLE_RULES["adverse"]
_Q["principles"] = PRINCIPLES_TEXT
_Q["input"]["phrases"] += " · v3.1(V3.1-7): consent mandatory_disclosures 109(kind=disclosure) — 전부 문구 사전 항목(개체 아님)"
_Q["split"] = _Q["split"].replace("사전 순서 relative_site → site(anatomical·layer·region) → course → adverse_qualifier → adverse_event_type", "사전 순서 relative_site(→ 칸 none · parsed) → site(anatomical·layer·region · 칸) → course(→ R15 엣지) → adverse_qualifier(칸) → adverse_event_type(칸)") + " · v3.1(V3.1-8): 사전에 안 닿는 토큰은 수식어 목록·패턴(정도 · 시간 · 발생률 · 조건 · 연결어 · 기타)에 대어 parsed 로 보존하고, 그래도 남으면 미등록(outer) 또는 설명(inner · 미등록으로 센다)"
_Q["tuple"] = _Q["tuple"].replace("튜플", "단위").replace("없으면 site=none, course=미상", "없으면 site=none(상대 부위도 none) · 경과는 단위 칸이 아니라 R15 엣지 속성(멤버 안 경과 조각 전부 · 없으면 null)") + " · v3.1(V3.1-9): 단위 = (사건, 부위, 물질) 세 칸"
_Q["unit"] = UNIT_RULE
_Q["qualifier"] = QUALIFIER_RULE
_Q["fold_condition"] = "세 칸(사건 · 부위 · 물질) 전부 사전 값일 때만 (site none · qualifier none 은 값 · 상대 부위는 none · 경과는 칸이 아니다)"
_Q["fold_rule"] = ("부작용 접힘 조건(v3.1 · V3.1-9): **세 칸 전부 사전 값일 때만** 다른 이름·문구와 접힌다 — 조각이 전부 사전(사건 · 부위 · 상대 부위 · 경과 · 수식)에 닿아 미등록 조각이 0 이고 사건에 붙지 않은 조각이 없을 때. 부위 none · 물질 none 은 명시 예외의 값. 상대 부위는 none 과 같고 경과는 R15 엣지로 가므로 「주사 부위 부종」「일시적 부종」「경미한 부종」「부종」은 같은 단위 (부종, none, none). "
                   "complications 이름에 미등록 조각이 하나라도 있거나 붙지 않은 조각이 남으면 접지 않는다(raw_name 단위 · anchor · 원칙 A·B). 문구는 미등록 조각이 섞인 단위를 만들지 않는다(원칙 D) — 조각 전부 사전 값인 문구만 단위를 세운다(auto)")
ADVERSE_FOLD_RULE = _Q["fold_rule"]
_Q["raw_name"] = V3.RAW_NAME_RULE.replace("site=none · course=미상(둘 다 미상 · 식별자 RAW:anchor 만으로 고유)", "site=none · qualifier=none(식별자 RAW:anchor 만으로 고유 · v3.1 경과는 칸이 아니다)").replace("dict_tuples(사건, 부위, 경과)", "dict_tuples(사건, 부위, 경과, 수식 — 경과는 엣지의 재료)")
RAW_NAME_RULE = _Q["raw_name"]
_Q["expressions"] = PHRASE_DICTIONARY_RULE
EXPRESSION_RULE = PHRASE_DICTIONARY_RULE
_Q["adverse_stopwords"] = {"rule": ADVERSE_STOPWORD_RULE, "threshold": ADVERSE_STOPWORD_THRESHOLD, "classes": list(ADVERSE_STOPWORDS.keys()),
                          "words": [{"word": w, "class": c} for c, ws in ADVERSE_STOPWORDS.items() for w in ws], "patterns": [{"class": c, "regex": rx, "note": n} for c, rx, n in ADVERSE_PATTERNS],
                          "locators": "build 가 문구·이름 자리에서 실측(단어·패턴마다 ≥1 · words[].locators / patterns[].locators)"}
_Q["phrase_dictionary"] = PHRASE_DICTIONARY_RULE
_Q["phrase_shape"] = ("**phrase_shape(V3.1-9 보강 · 사용자 「안전 문구도 더 카테고리화」)**: 문구 사전 항목의 parsed 에서 결정론으로 단다 — 모든 토큰은 다음 중 정확히 하나로 분류된다(검산 N-10 · 버리는 조각 0): " + " · ".join(FRAGMENT_CLASSES) + ". "
                      "shape 판정(우선순위): 사건 조각이 없거나 미등록 조각(outer)이 있으면 unresolved; 발생률·조건 조각이 있으면 event_incidence_condition; 정도·시간·경과 조각이 있으면 event_degree_course; 설명(괄호 미등록) 조각이 있으면 explanatory; 부위(절대·상대) 조각이 있으면 event_site; 그 밖(사건 + 수식·연결어·기타만) event_only. 한 문구가 여러 종류를 가지면 우선순위가 높은 하나가 shape 이고 전부는 fragment_classes 에 남는다. "
                      "event_incidence_condition 의 발생률·조건 조각은 그 문구가 만드는 R15 엣지 속성 incidence_text·condition_text 로 올린다 — 값 복사가 아니라 문구 사전 항목 참조. 열거값과 패턴은 원장 전수(§9.6.9)에서 뽑았고 단어·패턴마다 locator 가 있다.")
PHRASE_SHAPE_RULE = _Q["phrase_shape"]
_Q["phrase_shapes"] = list(PHRASE_SHAPES)
_Q["fragment_classes"] = list(FRAGMENT_CLASSES)
_Q["status_values"] = ["auto", "approved", "unlinked"]
_Q["expressions_create_units"] = "all_dict_cells_only"
_Q["expressions_create_raw_units"] = False
_Q["course_is_edge_attribute"] = True
_Q["relative_site_is_none"] = True
_Q["id"] = ID_RULE["adverse_effect"]
_Q["disclosure"] = DISCLOSURE_RULE
_Q["normal_phrases"] = _Q["normal_phrases"].replace("닿으면 R29 + R15(reaction_level=normal), 아니면 표현만", "닿으면(auto) R15(reaction_level=normal · source_phrases), 아니면 문구 사전 unlinked 항목만(v3.1)")
_Q["site"] = _Q_SITE_RULE_V31
SITE_RULE = _Q["site"]
_Q["course"] = V3.COURSE_RULE + " v3.1(V3.1-9): 경과는 단위 칸이 아니라 R15 엣지 속성 course 다 — 읽는 규칙(사건에 바로 붙은 수식어만 · 멤버 밖 금지)은 그대로이고 값이 가는 자리만 바뀐다. 수식어가 없으면 엣지 course=null(미상)."
COURSE_RULE = _Q["course"]
TUPLE_RULES["condition"] = {
    "name": "condition_v3_1",
    "input": {"names": "사람 조건 이름 9 키(" + " · ".join(_SRC_COND) + ") 값 자리 471 · 정규화 distinct 298(kind 포함 299)", "dictionary": "person_condition(정준값 " + str(len(CONDITION_CORES)) + " · 동의어 · kind · 출처 derived)"},
    "rule": CONDITION_RULE,
    "split": "괄호로 outer/inner · `· / , + 및 또는 — :` 로 멤버 · 멤버마다 공백 토큰을 왼쪽부터 가장 긴 구간으로 사전(정준값·동의어 · norm_v1 완전 일치) · 표지어는 qualifier_text · 남는 토큰 = 미등록",
    "markers": list(CONDITION_MARKERS),
    "kind_by_source": dict(CONDITION_KIND_BY_SOURCE),
    "fold_condition": "조각 전부 사전 값(+표지어)일 때만 — 멤버 안 조건 조각마다 단위 하나(원칙 B) · 미등록 조각 있으면 raw_name(원칙 A)",
    "id": ID_RULE["person_condition"],
    "phrases": "조건 문장 자리 하나(471) = 단위의 phrases[] 부록 하나(개체 아님) · R16/R17/R18.source_phrases 가 locator 로 든다 · 문장은 단위를 세우지 않는다(단위는 이름이 만든다 · exact | raw)",
    "no_similarity": True, "particle_split": False,
    "synonym_rules": ["괄호 동치: 이름이 「X(Y)」꼴이고 Y 가 다른 이름에서 독립 멤버로도 나타남(출현 많은 쪽이 정준값)", "표기 변형: 한랭/한냉/냉 · 병 접미(당뇨/당뇨병) · 공백(정규화)"],
}

# v3 → v3.1 변경 목록
CHANGE_LIST_V31 = [
    ("V3.1-1", "결정 kind product_reclassify(⓪)", "§5.2 kind 20 · §5.4 ⓪ · §2.6 product 식별자·reclassified_from · §1.1 id_rule.product · R4/R3/R27 비고 · 실측 §9.7.1(대상 예 · id 재계산)"),
    ("V3.1-2", "관계 R32 rule_applies_to", "§3 R32(scope · severity · source_locator · decision_id · basis) · §2.19 clinical_rule kind product_note · edge_create 비고 · 실측 §9.7.2(제품 note 규칙 문장 후보 전수)"),
    ("V3.1-3", "결정 kind dictionary_remove(①)", "§5.2 kind 20 · §5.4 ① 순서 · 사전 removed_synonyms/removed_entries(「공기색전」 이력 포함)"),
    ("V3.1-4", "조건 사전 person_condition · 조건 단위 식별 · 문장 부록", "§2.15 식별자·phrases[] · R16/R17/R18 source_phrases · §1.6 조건 분해 규칙 · §4 사전 person_condition · §1.1 id_rule · 실측 §9.7(298 → N · 접힌 표 전부 · raw_name)"),
    ("V3.1-5", "회·차 자리", "R12 session_count·session_index · R9/R17/R18 qualifier_text · resolve_rules.stopwords.session_rule · 실측 §9.5.12"),
    ("V3.1-6", "stopwords 겹침 규칙·목록", "resolve_rules.stopwords.overlap_rule/overlap · §1.3 · 실측 §9.5.13 · 검산 N-6"),
    ("V3.1-7", "필수 고지 → clinical_rule(disclosure) + R32(ledger) + 문구 사전(disclosure)", "§2.19 · §2.2 modality 속성 삭제 · R32 basis · R15 출처·disclosure · column-map 이동 · 실측 §9.8(계열 17 × 고지 109 · 부작용 조각 연결)"),
    ("V3.1-8", "안전 문구 수식어 목록(adverse stopwords · 패턴)", "§1.5 · tuple_rules.adverse.adverse_stopwords · 문구 사전 parsed · R15 degree/timing 참조 · 실측 §9.6.9 · 검산 N-8"),
    ("V3.1-9", "사용자 정의 2 개정 — 단위 (사건, 부위, 물질) · 상대 부위 none · 경과는 R15 엣지 속성 · 명시 예외 개정 · 원칙 D 문장", "§0 · §1.1 id_rule.adverse_effect · §1.5 · §2.14 adverse_effect(세 칸 · relative_site_text) · R15.course · R30/R31 비고 · edge_create/adverse_tuple_assign 세 칸 · 실측 §9.6(65 → N · 사건별 조합)"),
    ("V3.1-10", "안전 문구 사전 phrase_dictionary · adverse_expression 개체·R29 삭제 · 부록(R15 source_phrases · 단위 explanations · 게이트 unlinked_phrases) · 결정 kind phrase_map · evidence_statement 유지 · 조건 문장도 부록", "§2(개체 20) · §3(관계 31 = 31 − R29 + R32 · R19/R20 끝) · §4 사전 phrase_dictionary · §5.2 kind 20 · §1.5 · column-map 표현 행 28 → dict:phrase_dictionary · 실측 §9.6.10/§9.6.11(2,935 → 항목 N · auto/unlinked · 부록 합) · 검산 N-9·N-10·N-11"),
]
