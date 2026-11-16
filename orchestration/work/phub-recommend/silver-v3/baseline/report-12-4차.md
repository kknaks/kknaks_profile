## 12. 4차 빌드 · 브론즈 2판 + 결정 묶음 2B

3차 = `baseline/manifest-3차.json`(브론즈 1판 · 결정 묶음 2A 까지) · 4차 = 원장 phub-ledger 판 2(HASHES.txt 검증 · manifest `bronze_version`) + `decisions/batch2b/` approved 57 건(사용자 게이트 답 2026-11-05).

### 결정 묶음 2B 적용

| 결과 | 건 |
|---|---|
| applied | 48 |
| recorded | 7 |
| rejected | 2 |

| kind | applied | recorded | rejected | no_target |
|---|---|---|---|---|
| adverse_tuple_assign | 15 | 0 | 0 | 0 |
| canonical_mapping | 9 | 0 | 0 | 0 |
| event_split | 3 | 0 | 0 | 0 |
| fold_approve | 21 | 0 | 0 | 0 |
| scope_review | 0 | 7 | 0 | 0 |
| tuple_assign | 0 | 0 | 2 | 0 |

거부·대상 없음:

- `DEC-2026-11-04-B2B-SLS-02` tuple_assign — rejected: anchor 또는 지정 값이 실버에 없다
- `DEC-2026-11-04-B2B-SLS-09` tuple_assign — rejected: anchor 또는 지정 값이 실버에 없다

결정을 만들지 않은 답(원장 2판으로 해소):

- `slash-together-or/03` = per_site — 원장 2판에서 이름의 `/` 가 `+` 로 바뀌어 참조 anchor(REF-)가 사라졌다 — 결정을 만들지 않음(원장 2판으로 해소)
- `slash-together-or/08` = per_site — 원장 2판에서 이름의 `/` 가 `+` 로 바뀌어 참조 anchor(REF-)가 사라졌다 — 결정을 만들지 않음(원장 2판으로 해소)
- `slash-together-or/12` = per_site — 원장 2판에서 이름의 `/` 가 `+` 로 바뀌어 참조 anchor(REF-)가 사라졌다 — 결정을 만들지 않음(원장 2판으로 해소)

### 브론즈 2판으로 바뀐 참조

3차 미해결 참조 중 2판에서 원장 이름이 바뀐 것 4 — 그중 해결 0 · 새 이름으로도 미해결 4.

| 3차 anchor | 1판 이름 | 2판 이름 | 4차 |
|---|---|---|---|
| REF-393ecee04b | 보톡스(턱선/광대) | 보톡스(턱선+광대) | 미해결(⑨) REF-6c649b6a74 |
| REF-55c667d515 | 보톡스 이마/미간 | 보톡스 이마+미간 | 미해결(⑨) REF-14e31cbffb |
| REF-9cc2bf84b1 | 필러 팔자/볼 | 필러 팔자+볼 | 미해결(⑨) REF-073838857f |
| REF-e8ed11044f | 필러 볼/턱 | 필러 볼+턱 | 미해결(⑨) REF-11c54d1449 |

- `+` 로 바뀐 이름은 §1.4 조합 규칙상 primary 를 가진 멤버가 하나뿐이라(「보톡스 이마」+「미간」) 조합이 아니라 부위 둘(multi_site) → 여전히 ⑨. 1판 anchor 를 가리키던 per_site 답 3(slash 03·08·12)은 anchor 가 없어 결정을 만들지 않았다 — 새 anchor 에 다시 정하려면 tuple_assign_multi 를 미해결 참조에 적용하는 빌더 보강이 먼저다.

### 게이트 4종

|  | 3차 | 4차 | 변화 |
|---|---|---|---|
| unresolved_references | 282 | 282 | +0 |
| unregistered_fragments | 2152 | 2152 | +0 |
| unlinked_expressions | 2156 | 2158 | +2 |
| catalog_partial | 345 | 344 | -1 |

### 충돌 kind 별

|  | 3차 | 4차 | 변화 |
|---|---|---|---|
| ④ value_conflict auto_resolved_by_trust | 1 | 1 | 0 |
| ⑥ value_conflict open | 49 | 49 | 0 |
| ⑦ duplicate_candidate open | 156 | 156 | 0 |
| ⑧ unregistered_value open | 2152 | 2152 | 0 |
| ⑨ unresolved_reference open | 282 | 282 | 0 |

### 개체

|  | 3차 | 4차 | 변화 |
|---|---|---|---|
| adverse_effect | 57 | 59 | +2 |
| adverse_expression | 2935 | 2935 | 0 |
| anatomical_structure | 36 | 36 | 0 |
| catalog_item | 521 | 521 | 0 |
| citation | 313 | 313 | 0 |
| clinical_rule | 29 | 29 | 0 |
| complaint | 121 | 121 | 0 |
| conflict | 2640 | 2640 | 0 |
| decision | 219 | 276 | +57 |
| evidence_statement | 87 | 87 | 0 |
| modality | 17 | 17 | 0 |
| modality_subcategory | 73 | 73 | 0 |
| package | 228 | 228 | 0 |
| person_condition | 298 | 298 | 0 |
| problem | 14 | 14 | 0 |
| problem_subcategory | 53 | 53 | 0 |
| procedure | 647 | 613 | -34 |
| product | 378 | 378 | 0 |
| site | 22 | 22 | 0 |
| source_file | 22 | 22 | 0 |
| technique | 12 | 12 | 0 |

### 관계

|  | 3차 | 4차 | 변화 |
|---|---|---|---|
| R1 | 74 | 74 | 0 |
| R2 | 521 | 521 | 0 |
| R3 | 159 | 159 | 0 |
| R4 | 476 | 476 | 0 |
| R5 | 25 | 25 | 0 |
| R6 | 53 | 53 | 0 |
| R7 | 232 | 232 | 0 |
| R8 | 105 | 105 | 0 |
| R9 | 594 | 594 | 0 |
| R10 | 21 | 21 | 0 |
| R11 | 12 | 12 | 0 |
| R12 | 448 | 448 | 0 |
| R13 | 32 | 32 | 0 |
| R14 | 146 | 146 | 0 |
| R15 | 793 | 778 | -15 |
| R16 | 455 | 455 | 0 |
| R17 | 21 | 21 | 0 |
| R18 | 118 | 118 | 0 |
| R19 | 378 | 378 | 0 |
| R20 | 119 | 119 | 0 |
| R21 | 45 | 45 | 0 |
| R22 | 22 | 22 | 0 |
| R23 | 53 | 53 | 0 |
| R24 | 207 | 207 | 0 |
| R25 | 9261 | 9261 | 0 |
| R26 | 521 | 521 | 0 |
| R27 | 647 | 613 | -34 |
| R28 | 36 | 36 | 0 |
| R29 | 685 | 673 | -12 |
| R30 | 0 | 0 | 0 |
| R31 | 2 | 3 | +1 |

