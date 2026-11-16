# 실물에서 확인한 설계 차이와 미정

이 폴더의 `schema.json`만 명시적으로 정교화했다. 기존 `design.json`, HTML, 원장, 실버 정본은 수정하지 않았다. Task `task_9a80516d7b7c`, Dispatch `ctx_55cef790e0f9`에서 코디네이터에게 두 차례 `ask`했고 아래 pilot 한정 표현을 허용받았다. 이는 임상 승인이나 본 설계 확정이 아니며 독립 검수 대상이다.

## 1. 규칙 없는 매핑과 기존 규칙의 구분

- 기존안 `mapping.rule:{id,version,code_sha256}`는 필수 object여서 원문 조합 구성원의 미정 매핑에도 가짜 규칙을 넣어야 한다.
- pilot에서는 `rule:null`을 허용하고 필수 `state`와 비어 있지 않은 `reason`을 결합한다. 원문 문자열의 `source_refs`는 반드시 남는다. `candidates:[]`, `selected_refs:[]`는 대상 미결정이며 적용 없음/승인을 뜻하지 않는다.
- **이미 있는 규칙은 null로 지우지 않는다.** 네 CC correspondence의 정확한 행과 기존 `step7-apply.py` 판/hash, 비교 멤버 두 개의 기존 같은 생성기 판/hash, 제품 compatibility의 `step5-apply.py` 판/hash, duration 두 원문행의 기존 R9-1 동일 제품 대응과 `step9-apply.py` 판/hash를 보존했다. 해당 source_record에는 기존 match/basis/gate_status/flag 등도 그대로 있다. 과거 임상 검토자나 판정 날짜를 새로 만들지 않았다.
- 코디 답변: “mapping.rule=null은 실제 rule 근거가 없는 경우에만 state/reason과 함께 두고 기존에 존재하는 규칙은 보존하세요.”
- 최소 변경: 원안 rule을 nullable로, reason 필수 string 추가. 이관 시에는 미정→확정 전환을 실제 판정/규칙 증거와 함께 검증해야 한다.
- 검증: `null_rule_reason`, `existing_mapping_rule`, `cc_existing_correspondence_rule_retained`, `comparison_candidate_exact`; 변조 `existing_mapping_rule_dropped`, `candidate_promoted_to_selected`.

## 2. R8-0001의 필드별 조건과 명시 순서무관

원문 `contraindications.json:/rules/0`은 `interval="같은 날 가능"`, `note="동일 부위는 보톡스 먼저 → 필러 순서 권장. 주입 부위가 다르면 순서 무관"`이다. 기존 실버 `/claims/0`의 `review_status=staff_check`를 유지한다.

- 기존안 first의 단일 `value`와 타입이 구체적이지 않은 `options`를 pilot에서 엄격한 `{scope_ref,value,raw_ref}[]`로 구체화했다. 상위 first.value는 null이며 `same_site→a`, `different_site→explicit_no_required_order` 두 분기를 둔다. a는 실제 `family:M1` mapping, b는 `family:M2` mapping이다.
- `explicit_no_required_order`(원문 명시 순서무관), `not_declared`(미기재), `unknown`(모름)은 별개 enum이다. 현재 원문에 뒤 두 상태를 억지로 추가하지 않았다. same_day=true의 원문 ref와 first 분기의 원문 ref도 다르다. days=null을 0일로 계산하지 않았다.
- 코디 답변: “원문이 다른 부위에서 순서 무관이라고 명시한 것과 순서가 미기재인 것을 같은 enum으로 표현하지 마세요.”
- 원래 승인규칙 없는 unknown에 가짜 resolution을 만들지 않았다. first 조건을 모르면 scalar null이고 원천 claim은 staff_check다. 이 원문에서 “어떤 순서든 임상적으로 승인됨”을 만들지 않는다.
- 최소 변경: options 원소 타입과 order enum 명시. 이관 시 scalar first만 읽는 소비자는 options/scope를 읽도록 바뀌어야 한다.
- 검증: `first_branches_preserved`, `endpoint_a_M1_b_M2`, `unknown_site_no_first`, `staff_check_preserved`; 변조 `first_condition_deleted`, `first_unconditional_a`, `explicit_no_order_conflated_with_not_declared`, `same_site_endpoint_swap`.

## 3. LOSS-02의 설계 예시 제품 표기 오류

- `taxonomy.json:/modality/0/subcategories/2/items/7`의 ID `auto-2-1774737181584`는 턱선보톡스 원문행이다. `step5-units.json:/extracted/25`는 `attach="단위 시술"`, `units=["U5-016"]`이며 `/ledger/25`에서도 확인된다.
- 기존안 LOSS-02의 `gold.node_effect=product:auto-2-1774737181584`를 그대로 entity로 발급하면 존재하지 않는 제품을 만든다. pilot은 원문 occurrence를 별도로 두고 실제 기존 `unit_procedure:U5-016`을 claim subject/attachment로 참조한다. 안전 claim에는 원문 M1 family scope도 유지했다.
- 코디 답변: “코디도 step5.extracted[25]의 id/턱선보톡스/attach=단위 시술/units=[U5-016]를 직접 확인했습니다.”
- 최소 변경: 본 설계의 이 예시만 제품→단위시술로 수정하는 후속 작업 필요. 이번에는 수정하지 않았다. 정본 이관에 앞서 product라는 그림 표기를 엔터티 존재 증거로 사용하지 않아야 한다.
- 검증: `existing_entity_identity`, `LOSS02_actual_unit_subject`, `safety_source_family_preserved`; 변조 `identity_from_name`.

## 4. override와 기존 n-ary pair 전개의 실제 근거

- 원안 override는 claim_refs만으로는 아직 별도 claim으로 분해하지 않은 기존 `override_of="family:M4"`, `level="제품 × 계열"`를 직접 보존하기 어렵다. pilot에 `override_of`, `level`, `source_record_ref`를 엄격한 필드로 추가했다. 원문 M4 안전 claim과 제품의 M2 포함 compatibility 후보는 독립이다. M2 적용 승인은 unknown이다.
- relation_claim에는 `source_record_ref`, `existing_expansions[]`, `expansion_policy`를 pilot 필드로 추가했다. 기존 pair ID와 exact 실버 source_record_ref, rule_text/lowering_text/source_index/endpoints_raw/source_arity, 원문 occurrence 후보 집합과 origin_state를 보존한다. 임의 metadata bag은 사용하지 않는다. 새 n-ary→pair 규칙을 승인하거나 실행하지 않았다.
- 같은 legacy CC키는 기존 R8 source_index만으로 원문을 하나로 정할 수 없다. 원문 후보 두 개를 함께 두고 `origin_state=ambiguous`로 남긴다. 선행 audit locator를 단일 확정으로 그대로 수입하지 않고 원문의 problem_id/cc/combos 인덱스로 후보 집합을 독립 복원했다. 튼살 정정은 명확한 원문 그룹 P9-4와 별개로 기존 잘못된 R8 연결도 증거에 남긴다.
- 코디 답변: “override_of/level 및 pair 전개근거는 원래 값과 exact source_record_ref를 가진 엄격한 타입 필드로 보존하고 임의 metadata bag으로 숨기지 마세요.”
- 최소 변경: 위 필드를 본 relation_claim/override 계약에 반영할지 독립 검수 후 결정. 이관 시 기존 pair의 legacy 이름키만으로 새 source_record를 발급하면 안 된다.
- 검증: `existing_expansion_values`, `nary_expansion_parent_arity`, `duplicate_expansion_not_first_match`, `override_M4_scope_metadata`; 변조 `ambiguous_expansion_first_match`, `nary_member_deleted`, `product_M4_override_extended_to_M2`.

## 5. 표현 가능한 채로 남긴 원천 미정

| 사례 | 보존한 사실 | 닫지 않은 질문 |
|---|---|---|
| 팔자 CC / 목주름 문장 | `/problems/1/complaints/3` container와 `/combos/2` reason·evidence, 기존 note111/R8-0279 | 오기인지 별도 부위인지 원장 담당자 확인 필요. source_conflict/unknown 유지 |
| 비교 필러 두 멤버 | subtitle·멤버 원문, U5-082..089 후보, 기존 ambiguous | 각 단독 부위의 적용/추천은 미확정. 팔자 단독 확정 엣지 없음 |
| 바이리즌 | M4 source safety/override와 제품의 다계열 compatibility | M2 허가 제품에 이 M4 원문이 적용되는지 미정 |
| 언어별 설명 | statement 및 patient_ko/en/zh/ja 각 claim | ko의 지연성 한정이 승인된 보충인지 확인 안 함. equivalence=unreviewed |
| duration | 3-6개월·6-9개월 두 원천 claim과 D9-3 보수 policy, alternatives | 조건 차이·임상 합의 미확정. clinical_consensus=false |

이 다섯 항목은 미정 표현에 실패한 schema gap이 아니다. **미정 상태와 근거를 보존하는 것이 이번 수용 기준**이다. 정본 이관/전체 필드 의미 검수/임상 재인증/Gold 활성화는 후속 단계다.
