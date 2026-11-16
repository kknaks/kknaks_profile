# SPEC-006 v2.2 · v2.3 근거 셈(spec006-v22-count.py · 결정론)

배치 rerun-v4 `b202611011148-c6ed3a` · rerun-v3 `b202610311552-d39a4d` · gold-export `b031371c4c69cea1`

## A. 걸음 해부(case3)

```json
{
 "runs": 182,
 "walked": 148,
 "fallback": 34,
 "stop": {
  "budget": 116,
  "steps": 10,
  "enough": 28,
  "empty": 28
 },
 "steps_n": {
  "0": 11,
  "1": 82,
  "2": 53,
  "3": 21,
  "4": 15
 },
 "neighbor_peek_reached": 79,
 "neighbor_fact_reached": 49,
 "steps_n_median_all": 1.0,
 "step1_picked_sections_median": 2.0,
 "step1_picked_neighbors_median": 2.0,
 "step1_picked_neighbors_ge1": 131,
 "budget_stops": 104,
 "budget_stop_at_step1": 62,
 "budget_stop_with_queued_neighbors": 94,
 "queued_neighbors_median": 3.0,
 "budget_stop_first_call_excluded": 17
}
```

| 섹션(단독 expand 호출) | n | 중앙 B | p95 | 최대 |
|---|---|---|---|---|
| method | 51 | 8117 | 8467 | 8802 |
| recovery | 38 | 2558.0 | 2685 | 3061 |
| safety.side_effects | 28 | 9793.0 | 16001 | 21246 |
| overview | 25 | 9247 | 9639 | 9690 |
| checks | 24 | 8693.5 | 9016 | 9016 |
| evidence | 15 | 5878 | 9765 | 10079 |
| safety.complications | 13 | 5973 | 6871 | 6871 |
| timeline | 10 | 7583.0 | 8011 | 8011 |
| aftercare | 7 | 39849 | 57988 | 57988 |
| products | 5 | 3404 | 8333 | 8333 |
| safety.pih | 4 | 5283.5 | 5912 | 5912 |
| site_caution | 4 | 13901.0 | 15201 | 15201 |
| ops | 3 | 4465 | 4498 | 4498 |
| emergency | 2 | 6426.5 | 7327 | 7327 |
| disclosure | 2 | 6547.0 | 7087 | 7087 |

## B. 답이 산 곳(실패 행 인용 → 골드 hit · 시작 노드 기준 가장 가까운 것)

행 621 · 골드 hit 461

### both (n=461)

전체: 금기 조건 100 · 계열 81 · 조합 81 · 섹션(시작 노드) 63 · 쌍 관계 39 · 전역 · scope 35 · 고민 관계 17 · 제품 15 · 다른 시술 15 · 부위 위험 8 · 합병증 6 · 부위 1

홉: 0:63 · 1:218 · 2:151 · 3:24 · 4:3 · 9:2

| 의도 | 분포 |
|---|---|
| I-01 | 금기 조건 24 · 조합 9 · 쌍 관계 5 · 부위 위험 5 · 전역 · scope 3 · 계열 2 · 제품 1 · 고민 관계 1 · 다른 시술 1 · 합병증 1 · 섹션(시작 노드) 1 |
| I-02 | 금기 조건 8 · 섹션(시작 노드) 6 · 부위 위험 3 · 계열 2 · 조합 2 · 전역 · scope 2 · 고민 관계 2 · 다른 시술 1 |
| I-03 | 섹션(시작 노드) 12 · 계열 8 · 다른 시술 5 · 금기 조건 4 · 쌍 관계 1 |
| I-04 | 섹션(시작 노드) 20 · 계열 18 · 제품 5 · 금기 조건 5 · 조합 3 · 다른 시술 2 · 합병증 2 · 전역 · scope 1 |
| I-05 | 계열 17 · 금기 조건 16 · 섹션(시작 노드) 15 · 전역 · scope 10 · 조합 5 · 고민 관계 4 · 제품 3 · 부위 1 · 합병증 1 · 다른 시술 1 |
| I-06 | 조합 37 · 계열 23 · 금기 조건 15 · 고민 관계 8 · 쌍 관계 4 · 섹션(시작 노드) 3 · 제품 3 · 다른 시술 3 · 전역 · scope 1 |
| I-07 | 쌍 관계 25 · 전역 · scope 10 · 조합 5 · 금기 조건 4 · 계열 3 · 제품 2 · 고민 관계 1 · 합병증 1 |
| I-08 | 쌍 관계 2 · 금기 조건 1 |
| I-09 | 금기 조건 19 · 조합 10 · 계열 6 · 섹션(시작 노드) 5 · 전역 · scope 3 · 쌍 관계 1 · 고민 관계 1 · 합병증 1 |
| I-10 | 조합 6 · 전역 · scope 5 · 금기 조건 2 · 다른 시술 2 · 섹션(시작 노드) 1 · 제품 1 · 쌍 관계 1 |
| I-11 | 조합 4 · 금기 조건 2 · 계열 2 |

### v4 (n=224)

전체: 계열 46 · 금기 조건 40 · 조합 38 · 섹션(시작 노드) 37 · 쌍 관계 16 · 전역 · scope 15 · 제품 11 · 다른 시술 9 · 고민 관계 7 · 부위 위험 3 · 부위 1 · 합병증 1

홉: 0:37 · 1:103 · 2:73 · 3:9 · 4:1 · 9:1

| 의도 | 분포 |
|---|---|
| I-01 | 금기 조건 11 · 조합 6 · 쌍 관계 2 · 부위 위험 2 · 제품 1 · 계열 1 · 고민 관계 1 · 전역 · scope 1 |
| I-02 | 섹션(시작 노드) 4 · 계열 2 · 조합 2 · 금기 조건 1 · 부위 위험 1 |
| I-03 | 섹션(시작 노드) 5 · 계열 3 · 다른 시술 3 |
| I-04 | 섹션(시작 노드) 13 · 계열 9 · 제품 3 · 조합 2 · 금기 조건 2 · 다른 시술 1 · 합병증 1 |
| I-05 | 계열 11 · 섹션(시작 노드) 9 · 금기 조건 6 · 조합 4 · 전역 · scope 4 · 제품 3 · 고민 관계 2 · 부위 1 |
| I-06 | 계열 14 · 조합 13 · 금기 조건 7 · 섹션(시작 노드) 3 · 다른 시술 3 · 고민 관계 3 · 제품 1 · 전역 · scope 1 |
| I-07 | 쌍 관계 12 · 전역 · scope 6 · 조합 3 · 제품 2 · 고민 관계 1 · 금기 조건 1 · 계열 1 |
| I-08 | 쌍 관계 1 |
| I-09 | 금기 조건 9 · 조합 4 · 계열 4 · 섹션(시작 노드) 2 · 쌍 관계 1 · 전역 · scope 1 |
| I-10 | 조합 3 · 다른 시술 2 · 전역 · scope 2 · 섹션(시작 노드) 1 · 금기 조건 1 · 제품 1 |
| I-11 | 금기 조건 2 · 계열 1 · 조합 1 |

### v3 (n=237)

전체: 금기 조건 60 · 조합 43 · 계열 35 · 섹션(시작 노드) 26 · 쌍 관계 23 · 전역 · scope 20 · 고민 관계 10 · 다른 시술 6 · 부위 위험 5 · 합병증 5 · 제품 4

홉: 0:26 · 1:115 · 2:78 · 3:15 · 4:2 · 9:1

| 의도 | 분포 |
|---|---|
| I-01 | 금기 조건 13 · 부위 위험 3 · 쌍 관계 3 · 조합 3 · 전역 · scope 2 · 다른 시술 1 · 계열 1 · 합병증 1 · 섹션(시작 노드) 1 |
| I-02 | 금기 조건 7 · 섹션(시작 노드) 2 · 전역 · scope 2 · 고민 관계 2 · 부위 위험 2 · 다른 시술 1 |
| I-03 | 섹션(시작 노드) 7 · 계열 5 · 금기 조건 4 · 다른 시술 2 · 쌍 관계 1 |
| I-04 | 계열 9 · 섹션(시작 노드) 7 · 금기 조건 3 · 제품 2 · 조합 1 · 전역 · scope 1 · 다른 시술 1 · 합병증 1 |
| I-05 | 금기 조건 10 · 섹션(시작 노드) 6 · 계열 6 · 전역 · scope 6 · 고민 관계 2 · 합병증 1 · 다른 시술 1 · 조합 1 |
| I-06 | 조합 24 · 계열 9 · 금기 조건 8 · 고민 관계 5 · 쌍 관계 4 · 제품 2 |
| I-07 | 쌍 관계 13 · 전역 · scope 4 · 금기 조건 3 · 조합 2 · 계열 2 · 합병증 1 |
| I-08 | 금기 조건 1 · 쌍 관계 1 |
| I-09 | 금기 조건 10 · 조합 6 · 섹션(시작 노드) 3 · 전역 · scope 2 · 계열 2 · 고민 관계 1 · 합병증 1 |
| I-10 | 조합 3 · 전역 · scope 3 · 쌍 관계 1 · 금기 조건 1 |
| I-11 | 조합 3 · 계열 1 |

### v4_case3_unknown (n=23)

전체: 금기 조건 10 · 섹션(시작 노드) 6 · 계열 2 · 쌍 관계 2 · 전역 · scope 2 · 조합 1

홉: 0:6 · 1:7 · 2:7 · 3:2 · 4:1

| 의도 | 분포 |
|---|---|
| I-01 | 금기 조건 2 · 조합 1 |
| I-02 | 금기 조건 1 |
| I-04 | 섹션(시작 노드) 3 · 금기 조건 1 |
| I-05 | 섹션(시작 노드) 3 · 금기 조건 2 |
| I-06 | 계열 2 · 금기 조건 1 |
| I-07 | 쌍 관계 2 · 전역 · scope 1 |
| I-09 | 금기 조건 1 · 전역 · scope 1 |
| I-11 | 금기 조건 2 |

### 의도별 첫 걸음 이웃 종류 순서(결정론 규칙)

n ≥ 10 이면 그 의도 · 아니면 전체 · 셈 내림차순 · 동점 = 전체 셈 → ('부위 위험', '금기 조건', '쌍 관계', '조합', '계열', '합병증', '고민 관계', '제품', '부위', '근거') 순 · 위 3

| 의도 | 행 | 근거 | 순서 | 섹션 행 | 섹션 1위 |
|---|---|---|---|---|---|
| _all | 461 | - | 금기 조건 → 조합 → 계열 | 63 | - |
| I-01 | 53 | intent | 금기 조건 → 조합 → 쌍 관계 | 1 | False |
| I-02 | 26 | intent | 금기 조건 → 부위 위험 → 조합 | 6 | False |
| I-03 | 30 | intent | 계열 → 금기 조건 → 쌍 관계 | 12 | True |
| I-04 | 56 | intent | 계열 → 금기 조건 → 제품 | 20 | True |
| I-05 | 73 | intent | 계열 → 금기 조건 → 조합 | 15 | False |
| I-06 | 97 | intent | 조합 → 계열 → 금기 조건 | 3 | False |
| I-07 | 51 | intent | 쌍 관계 → 조합 → 금기 조건 | 0 | False |
| I-08 | 3 | _all | 금기 조건 → 조합 → 계열 | 0 | False |
| I-09 | 46 | intent | 금기 조건 → 조합 → 계열 | 5 | False |
| I-10 | 18 | intent | 조합 → 금기 조건 → 쌍 관계 | 1 | False |
| I-11 | 8 | _all | 금기 조건 → 조합 → 계열 | 0 | False |

### v2.3 첫 걸음 이웃 edge kind 표

1홉 행 edge kind 셈 · n ≥ 10 이면 그 의도 · 아니면 전체 · 내림차순(동점 = 전체 셈 → 이름) · 1홉 행 90% 덮을 때까지(최소 3)

섹션 상한 2 의도(시작 노드 섹션이 1위): ['I-03', 'I-04']

| 의도 | 1홉 행 | 근거 | edge kind(순서) | 덮음 |
|---|---|---|---|---|
| _all | 185 | - | requires_check → product_family → procedure_relation → key_family → anchors_combo → treats → key_technique → treats_unit → child_of | 171 |
| I-01 | 15 | intent | anchors_combo → procedure_relation → site_caution → requires_check → treats → child_of | 14 |
| I-02 | 7 | _all | requires_check → product_family → procedure_relation → key_family → anchors_combo → treats → key_technique → treats_unit → child_of | 7 |
| I-03 | 15 | intent | product_family → key_technique → requires_check | 14 |
| I-04 | 19 | intent | product_family → requires_check → key_family | 18 |
| I-05 | 33 | intent | requires_check → key_family → product_family → treats → anchors_combo → treats_unit → product_unit | 31 |
| I-06 | 40 | intent | product_family → treats → requires_check → treats_unit → child_of → procedure_relation → anchors_combo → product_unit | 37 |
| I-07 | 25 | intent | procedure_relation → requires_check → key_family → anchors_combo | 25 |
| I-08 | 1 | _all | requires_check → product_family → procedure_relation → key_family → anchors_combo → treats → key_technique → treats_unit → child_of | 1 |
| I-09 | 20 | intent | requires_check → key_family → product_family → requires_check_unit → procedure_relation | 18 |
| I-10 | 5 | _all | requires_check → product_family → procedure_relation → key_family → anchors_combo → treats → key_technique → treats_unit → child_of | 5 |
| I-11 | 5 | _all | requires_check → product_family → procedure_relation → key_family → anchors_combo → treats → key_technique → treats_unit → child_of | 4 |

## C. 짧은 꼴 재생(기록된 expand 호출 · 같은 fact)

```json
{
 "60": {
  "calls": 444,
  "short_median": 1721.0,
  "short_p95": 2552,
  "short_max": 2897,
  "ratio_median": 0.202,
  "step1_all_calls_left": {
   "12000": {
    "median": 8378.5,
    "lt0": 0
   },
   "16000": {
    "median": 12378.5,
    "lt0": 0
   },
   "20000": {
    "median": 16378.5,
    "lt0": 0
   }
  }
 },
 "80": {
  "calls": 444,
  "short_median": 1721.0,
  "short_p95": 2584,
  "short_max": 3066,
  "ratio_median": 0.206,
  "step1_all_calls_left": {
   "12000": {
    "median": 8219.0,
    "lt0": 0
   },
   "16000": {
    "median": 12219.0,
    "lt0": 0
   },
   "20000": {
    "median": 16219.0,
    "lt0": 0
   }
  }
 },
 "120": {
  "calls": 444,
  "short_median": 1721.0,
  "short_p95": 2693,
  "short_max": 3204,
  "ratio_median": 0.211,
  "step1_all_calls_left": {
   "12000": {
    "median": 8052.5,
    "lt0": 0
   },
   "16000": {
    "median": 12052.5,
    "lt0": 0
   },
   "20000": {
    "median": 16052.5,
    "lt0": 0
   }
  }
 }
}
```

### 새 걸음 규칙 예산 추정 · 「충분」 · 되돌아감

```json
{
 "line_n": 80,
 "nb_slim_assumed_b": 300,
 "section_call_short": {
  "n": 387,
  "median": 2037,
  "p95": 2630
 },
 "walk4_by_sections_per_step": {
  "1": {
   "first_step_median": 2937,
   "later_step_median": 2037,
   "walk4_median": 9048,
   "walk4_p95": 11420
  },
  "2": {
   "first_step_median": 2937,
   "later_step_median": 4074,
   "walk4_median": 15159,
   "walk4_p95": 19310
  },
  "3": {
   "first_step_median": 2937,
   "later_step_median": 6111,
   "walk4_median": 21270,
   "walk4_p95": 27200
  }
 },
 "enough_noul_by_step": {
  "1": {
   "n": 171,
   "median": 0.05,
   "ge_0.5": 0,
   "ge_0.3": 0
  },
  "2": {
   "n": 89,
   "median": 0.08,
   "ge_0.5": 11,
   "ge_0.3": 22
  },
  "3": {
   "n": 36,
   "median": 0.125,
   "ge_0.5": 4,
   "ge_0.3": 8
  },
  "4": {
   "n": 15,
   "median": 0.17,
   "ge_0.5": 1,
   "ge_0.3": 4
  }
 },
 "fallback_reasons": {
  "no_facts/budget/steps1/step1_first_call_excluded": 10,
  "no_facts/budget/steps3": 2,
  "no_facts/empty/steps2": 3,
  "no_facts/empty/steps3": 1,
  "no_facts/enough/steps1": 3,
  "no_facts/enough/steps2": 3,
  "no_facts/steps/steps4": 1,
  "no_start/empty/steps0": 11
 },
 "collected_facts_per_walk": {
  "median": 14.0,
  "p95": 26
 },
 "collected_full_text_bytes_per_walk": {
  "median": 2235.0,
  "p95": 3903,
  "max": 4877
 }
}
```

## D. stray

```json
{
 "n": 15,
 "case2_calls": 521,
 "questions": 15,
 "bytes_rule_all": true,
 "next_same_name": 13,
 "input_shape": {
  "normal": 2,
  "empty": 10,
  "stringified_array": 3
 },
 "prev": {
  "resolve": 10,
  "procedure_card": 3,
  "recommend": 1,
  "check_conditions": 1
 }
}
```

| 문항 | 차례 | 이름 | 오류 B | =64+len | 직전 | 다음 | 다음 성공 | 입력 꼴 |
|---|---|---|---|---|---|---|---|---|
| Q031 | 2/3 | procedure_card | 78 | True | resolve | procedure_card | True | normal |
| Q066 | 5/6 | check_conditions_placeholder | 92 | True | resolve | check_conditions | True | empty |
| Q089 | 3/4 | expand | 70 | True | procedure_card | expand | True | stringified_array |
| Q109 | 2/3 | check_conditions | 80 | True | resolve | check_conditions | True | empty |
| Q115 | 2/3 | check_conditions | 80 | True | resolve | procedure_card | True | empty |
| Q125 | 2/4 | procedure_card | 78 | True | resolve | procedure_card | False | normal |
| Q149 | 3/4 | procedure_card | 78 | True | recommend | procedure_card | True | empty |
| Q164 | 2/3 | procedure_card | 78 | True | resolve | procedure_card | True | stringified_array |
| Q167 | 3/4 | procedure_card | 78 | True | resolve | procedure_card | True | empty |
| Q172 | 4/7 | neighbors | 73 | True | resolve | neighbors | True | empty |
| Q175 | 4/5 | combos | 70 | True | procedure_card | combos | True | empty |
| Q197 | 3/7 | peek | 68 | True | check_conditions | peek | True | empty |
| Q234 | 4/5 | expand | 70 | True | procedure_card | expand | True | empty |
| Q235 | 2/3 | check_conditions | 80 | True | resolve | procedure_card | True | empty |
| Q239 | 2/3 | procedure_card | 78 | True | resolve | procedure_card | True | stringified_array |
