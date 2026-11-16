# ERD v3.1 발주서 — 5차 빌드·적합성 시험에서 드러난 틈 6건 (사용자 승인 2026-11-05 「3.1 진행」)

동결 v3(`ERD-FROZEN.md` v3 절 · `erd-v3.*` · 생성기 `*_v3.py` · `erd-v3-tuples.py` · `erd-v3-check.py`)을 **v3.1 로 개정**한다. 근거 `ERD-V3-CANDIDATES.md` 「v3.1 후보」 V3.1-1~4 + 적합성 시험이 짚은 틈 2. 그 밖은 v3 그대로. 사용자 정의 3·명시 예외·승계 문장 유지.
입력·금지는 v3 발주서와 같다(원장 = 브론즈 2판). 추가로 읽어도 되는 것: `silver-v3/out/report.md` §13 · `silver-v3/decisions/batch3-proposed/DEC-*-EXO-0{2,5,6}.json` · `silver-v3/tests/enumerate_cases.py` 출력(경우의 수 형식 — 새 kind·관계가 거기서 자동으로 잡히게) · `silver-v3/README.md`. silver-v3/lib 코드는 읽지 않는다.

## 변경 6건
| # | 변경 | 어디 |
|---|---|---|
| V3.1-1 | 결정 kind `product_reclassify`: target{product_id(PRD-) 또는 (dictionary product_name, canonical)} · new_value{to_modality_code}. 제품 id 는 계열 코드 기반이라 재계산, 옛 id alias(`reclassified_from`), R4 offers_product 이동, R3·R9 등 제품을 끝으로 쓰는 엣지는 새 id 로. 적용 단계 ⓪(원장 적재 직후·reclassification 과 같은 자리) | §5.2 · 적용 순서 |
| V3.1-2 | 관계 R32 `rule_applies_to`: clinical_rule → product \| technique \| proc_axis(계열·하위분류·시술) · 속성 scope(전체/계열/제품) · severity · source_locator · decision_id. 값은 edge_create 로만(원장이 구조화하지 않음) — 단 원장 products note 「화장품 허가 (주사 사용 불법)」처럼 제품 note 에 규칙 문장이 있으면 clinical_rule 레코드의 출처로 열거(값 자동 생성은 안 함) | §3 · §2.19 |
| V3.1-3 | 결정 kind `dictionary_remove`: target{dictionary, canonical, synonym?} — synonym 있으면 동의어 하나 제거, 없으면 값 제거(그 값을 쓰는 레코드가 있으면 거부). 제거 이력 `removed_synonyms[]`/`removed_entries[]` 보존. 적용 단계 ① (dictionary_add 뒤) | §5.2 |
| V3.1-4 | person_condition 식별을 문자열에서 **조건 사전**으로: `condition_dictionary`(정준값 · 동의어 · kind condition/check/age_group · 출처 필수) + 조건 개체 식별자 = 사전 정준값 (+ kind). 원장 문장은 표현(condition_expression? 아니면 adverse_expression 과 같은 「원문 표현」 개체를 공용으로 — 작성자가 둘 중 ERD 일관성 높은 쪽 택하고 사유) 으로 보존·연결. 사전 초기값은 원장 이름 전수에서 **완전 일치만** 접고, 나머지는 raw_name 조건으로(부작용 raw_name 과 같은 원칙 — 미등록 조각 있으면 접지 않음). 실측: 조건 298 → N | §2.15 · §1.6 신설 · 사전 |
| V3.1-5 | 「회」(횟수)·「N차」(회차) 가 갈 자리 명시: R12 member 엣지 속성 `session_count`(회) · `session_index`(차) · R9/R17/R18 는 `qualifier_text` 만. resolve_rules 의 「회 → count」 문장을 이 속성으로 | §3 R12 · resolve_rules |
| V3.1-6 | stopwords 와 사전 값 겹침: 「관리」가 modality_group 사전 값과 겹침 — 규칙을 「stopword 는 분해 조각에서만 제외하고, 사전 값으로의 통째 일치는 먼저 본다」로 명시하고 겹침 목록을 검산이 세게 | resolve_rules.stopwords |

## 검산·실측
`erd-v3.1-check.py` = v3 전부 + 6건 반영 + 새 kind·관계가 `decision_kinds`/`relations` 에 들어가 적합성 열거기(`tests/enumerate_cases.py`)가 읽는 형식인지. `erd-v3.1-tuples.py` = v3 실측 전부 + 조건 사전 접힘 실측(298 → N · 접힌 표 전부 · raw_name 수) + R32 출처 후보 열거 + 「회/차」 자리 실측.

## 산출물
`erd-v3.1.*`(md · json · column-map · dictionaries · check.py · tuples.py/.json · 생성기 `*_v31.py`). 이전 판 보존. §11 「v3 → v3.1 변경 목록」· §12 「v3.1 밖 관찰」.

## 보고
6건 반영 위치 · 개체·관계·사전 수 변화 · 조건 298 → N 과 접힌 표 요약 · 검산 결과. 본문 재붙임 금지.
