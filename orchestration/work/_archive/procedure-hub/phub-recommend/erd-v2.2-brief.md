# ERD v2.2 발주서 — 독립 검토 반영 (사용자 승인 2026-11-04 「진행하자」)

v2.1(`erd-v2.1.*` · 생성기 `*_v21.py` · `erd-v2.1-tuples.py` · `erd-v2.1-check.py`)을 개정한다.
근거: `erd-v2.1-review.md` ⑤ 「동결 전 꼭 고칠 것」 6건 중 **5건 수용 + 1건(④) 변형**. 그 밖은 손대지 않는다. 검토서의 「동결 후 결정 레코드로」 9건은 이번 범위가 아니다(결정 kind 가 생기면 갈 자리만 생긴다).

## 수정 6건
1. **미상은 식별자 값이 아니다** (검토 1). site 또는 technique 가 미상(none)인 튜플은 다른 항목과 접히지 않는다. 구현: 미상 칸이 하나라도 있으면 식별자에 catalog_item id(또는 참조 자리 id)를 섞어 항목별 고유. 접힘 조건을 문서에 문자 그대로: 「세 칸 전부 사전 값일 때만」. §9.5.2 의 3건과 참조 16튜플이 갈라지는지 실측.
2. **조각을 버리고 접지 않는다** (검토 2). primary(what 후보) 또는 site 조각이 둘 이상이면 combo_ref 또는 미해결. §1.4 규칙 8 삭제. `extra_sites` 가 null 인 실측 불일치는 산출물 쪽을 고쳐 실제 값을 담는다.
3. **기법 상속을 끈다** (검토 3). R5 계열→기법을 시술 튜플에 자동으로 붙이지 않는다. technique 는 이름 조각이 기법 사전에 닿을 때만, 아니면 미상. 상속은 결정 kind `canonical_mapping` 후보로만 §9 에 목록.
4. **규칙 ④(신뢰 순위 자동 해결)는 유지하되 기록한다** (검토 4 변형 · 사용자 결정). 순위로 자동 해결된 충돌도 conflict 레코드를 만든다: status=`auto_resolved_by_trust`, chosen_value, values[].trust_tier, rule_ref=④. 결정 레코드로 뒤집을 수 있게 decision kind `conflict_override` 를 둔다.
5. **decision 개체를 빌드가 읽는 모양으로** (검토 5). kind 열거형에 최소 추가: `dictionary_add`(dictionary, canonical, synonyms[], category?) · `tuple_assign`(catalog_item_id | ref_id → what_kind, what_id, site_id, technique_id) · `fold_approve`(procedure_ids[] → keep_id) · `event_split`(event, new_events[]) · `canonical_mapping`(from_ref → to_id, scope) · `conflict_override`(conflict_id → chosen_value) · `exclude`(id, reason). 공통 필드: id · kind · target(구조체) · new_value(구조체) · reason · decided_by · decided_at · status(proposed|approved|rejected) · source_refs[]. **빌드는 status=approved 만 읽는다.** 기존 결정 레코드 22건을 이 모양으로 옮긴다(who 는 검토 3-E 대로 승인 시점 기준으로 정정).
6. **course 출처 일원화** (검토 6). 이름 수식어(일시적·지연성·영구·가역적)에서만 읽는다. duration·incidence 는 엣지 속성으로만. §1.5·§2.14·§4 세 곳을 같은 문장으로.

## 검산
`erd-v2.2-check.py` = v2.1 항목 전부 + 「미상 포함 튜플 접힘 0 · 버린 조각 0(extra_* 실값) · 상속 기법 0 · ④ 자동 해결마다 conflict 레코드 규칙 명시 · decision kind 7 + 공통 필드 · 기존 결정 22 이관 · course 출처 문장 3곳 동일」.
`erd-v2.2-tuples.py` 재실행 → §9.5·§9.6 v2.1 과 나란히. 접힌 표(§9.5.2)는 「세 칸 전부 사전 값」인 것만 남아야 한다.

## 산출물
`erd-v2.2.md` · `erd-v2.2.json` · `erd-v2.2-column-map.md` · `erd-v2.2-dictionaries.json` · `erd-v2.2-check.py` · `erd-v2.2-tuples.py/.json` · 생성기 `*_v22.py`. 이전 판 파일은 지우지 않는다. 끝에 「v2.1 → v2.2 변경 목록(검토 항목 번호 대응)」.

## 보고
521 → N · 접힌 튜플 수 · what_kind 분포 · none 비율 · decision kind 수와 이관 22 · 검산 결과. 본문 재붙임 금지.
