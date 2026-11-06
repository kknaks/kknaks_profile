# ERD v2.3 발주서 — 2차 독립 검토 반영 (사용자 승인 2026-11-04 「진행하자」)

v2.2(`erd-v2.2.*` · 생성기 `*_v22.py` · `erd-v2.2-tuples.py` · `erd-v2.2-check.py`)를 개정한다.
근거: `erd-v2.2-review.md` ⑥ 「동결 전 꼭 고칠 것」 **7건 전부 수용**. 검토서가 「동결 후 결정으로」로 분류한 것은 범위 밖. 그 밖은 손대지 않는다.

## 수정 7건 (검토서 번호 대응)
1. **시술 축 엣지의 끝 = 시술 튜플.** R3·R9·R12·R15·R16·R17·R18 등 proc_axis 를 끝으로 쓰는 모든 엣지는, 그 자리의 참조가 튜플로 해결됐으면 **procedure 튜플 id** 를 끝으로 쓴다. 계열·하위분류·제품 노드에 직접 붙는 건 참조가 그 층까지만 적혀 있을 때뿐이며 target_depth 로 표시. 실측(`erd-v2.3-tuples.py`)에 「엣지 자리별 끝 분포(procedure / modality / subcategory / product / unresolved)」를 추가.
2. **경과(course)는 사건에 바로 붙은 수식어만.** 이름 안에 사건이 둘 이상이면 수식어가 붙은 사건에만 경과를 주고 나머지는 미상. 「통증·불편감 및 지연성 통증(LOP)」→ (통증, 미상) + (통증, 지연) 둘. 규칙을 §1.5 에 문자 그대로.
3. **부작용도 미등록 조각이 있으면 접지 않는다.** 시술과 같은 원칙(v2.1 규칙). 미등록 조각이 있는 이름은 항목별 고유 튜플(event_kind=raw_name, candidate_name 보존), 접힘은 세 칸 전부 사전 값일 때만. §9.6.2 를 다시 실측.
4. **결정 kind 추가 4종.** `edge_create`(R30 인과 등: from_ref, to_ref, relation, attrs) · `tuple_assign_multi`(catalog_item | ref → tuples[] 여럿, 예 「보톡스 이마/미간」) · `adverse_tuple_assign`(raw_name | expression → event_id, site_id, course_id) · `conflict_close`(conflict_id → verdict=not_same | both_valid | needs_source, note). 각 kind 의 target·new_value 구조체를 §2.21 표에.
5. **결정은 안 바뀌는 키를 가리키고, 적용 순서를 고정한다.** target 은 catalog_item id · 원장 locator(file:key path) · 참조 자리 id · conflict 의 안정 키(출처 locator 쌍)만. PRC-/ADV-/CFL- 같은 파생 id 는 target 금지(검산). 적용 순서: ① dictionary_add ② canonical_mapping ③ tuple_assign / tuple_assign_multi / adverse_tuple_assign ④ fold_approve / event_split ⑤ edge_create ⑥ conflict_override / conflict_close ⑦ exclude. 같은 단계 안은 decided_at 순. §5 에 표로.
6. **기법 상속 잔재 제거.** §2.7 정의 문장과 `technique_id` 출처에서 상속 표현 삭제. 출처는 이름 조각 → 기법 사전뿐.
7. **R29 출처 보완.** adverse_expression → adverse_effect 연결 출처에 taxonomy safety 키 11개 추가(연결 1,405건의 출처).

## 검산
`erd-v2.3-check.py` = v2.2 전부 + 「엣지 끝 분포 실측 존재 · 파생 id 를 target 으로 쓰는 결정 0 · 적용 순서 표 존재 · 결정 kind 16(12+4) · 부작용 미등록 포함 접힘 0 · course 규칙 문장 · 상속 표현 grep 0 · R29 출처 11 키」.
`erd-v2.3-tuples.py` 재실행 → §9.5·§9.6 v2.2 와 나란히 + 엣지 끝 분포 표.

## 산출물
`erd-v2.3.md` · `erd-v2.3.json` · `erd-v2.3-column-map.md` · `erd-v2.3-dictionaries.json` · `erd-v2.3-check.py` · `erd-v2.3-tuples.py/.json` · 생성기 `*_v23.py`. 이전 판은 지우지 않는다. 끝에 「v2.2 → v2.3 변경 목록(검토 번호 대응)」.

## 보고
7건 각각 어디서 고쳤는지 한 줄씩 · 엣지 끝 분포 · 부작용 65 → N · 결정 kind 수 · 검산 결과. 본문 재붙임 금지.
