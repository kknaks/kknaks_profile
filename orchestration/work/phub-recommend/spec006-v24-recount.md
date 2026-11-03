# SPEC-006 v2.4 근거 셈 — 받는 자리 정의 하나로(spec006-v24-recount.py · 결정론)

빌드 `b031371c4c69cea1`

## 461 행 자리

0홉·1쪽 93 · 1홉·1쪽 120 · 0홉·2쪽+ 19 · 1홉·2쪽+ 94 · 2홉+ 75 · 받을 곳 없음 33 · 이름·속성만 27

| 의도 | 0홉·1쪽 | 1홉·1쪽 | 0홉·2쪽+ | 1홉·2쪽+ | 2홉+ | 받을 곳 없음 | 이름·속성만 |
|---|---|---|---|---|---|---|---|
| I-01 | 2 | 14 | 1 | 19 | 12 | 2 | 3 |
| I-02 | 9 | 5 | 2 | 6 | 2 | 0 | 2 |
| I-03 | 16 | 2 | 0 | 10 | 2 | 0 | 0 |
| I-04 | 27 | 10 | 2 | 10 | 1 | 0 | 6 |
| I-05 | 21 | 20 | 7 | 16 | 4 | 5 | 0 |
| I-06 | 13 | 30 | 5 | 11 | 27 | 2 | 9 |
| I-07 | 1 | 10 | 0 | 3 | 13 | 22 | 2 |
| I-08 | 0 | 0 | 1 | 0 | 0 | 2 | 0 |
| I-09 | 3 | 15 | 1 | 15 | 9 | 0 | 3 |
| I-10 | 1 | 11 | 0 | 2 | 4 | 0 | 0 |
| I-11 | 0 | 3 | 0 | 2 | 1 | 0 | 2 |

## 순서 표 v2.4

받는 자리 = 노드 자신의 section 줄 1쪽 · 1홉·1쪽 행(S 줄 1쪽에 없고 edge kind k 이웃 X 의 줄 1쪽에 있음)의 edge kind 셈 · n ≥ 10 이면 그 의도 · 아니면 전체 · 내림차순(동점 = 전체 셈 → 이름) · 의도 1홉·1쪽 행 90% 덮을 때까지(최소 3) · S 가 계열 · 제품이면 단위 이웃 종류 {'family': 'key_family', 'product': 'product_unit'} 를 늘 더함

걸음 1 섹션 2 의도(0홉·1쪽 1위): ['I-02', 'I-03', 'I-04', 'I-05'] · 단위 이웃 규칙이 461 의 1홉·1쪽에 더하는 덮음 0

| 의도 | 1홉·1쪽 행 | 근거 | edge kind(순서) | 덮음 | 셈 |
|---|---|---|---|---|---|
| _all | 120 | - | treats → treats_unit → key_family → requires_check → product_family → procedure_relation → key_technique → anchors_combo → key_site | 108 | {'treats': 33, 'treats_unit': 31, 'key_family': 30, 'requires_check': 17, 'product_family': 15, 'procedure_relation': 13, 'key_technique': 10, 'anchors_combo': 8, 'key_site': 5, 'product_unit': 5, 'requires_check_unit': 4, 'uses_product': 4, 'site_caution_unit': 3, 'concern_avoid': 2, 'concern_avoid_unit': 2, 'has_statement': 2, 'has_complication': 1, 'procedure_pair': 1, 'site_caution': 1} |
| I-01 | 14 | intent | treats → treats_unit → key_family → key_site → site_caution_unit → procedure_relation → requires_check_unit | 13 | {'treats': 5, 'treats_unit': 5, 'key_family': 3, 'key_site': 3, 'site_caution_unit': 3, 'has_statement': 1, 'procedure_relation': 1, 'requires_check_unit': 1, 'site_caution': 1} |
| I-02 | 5 | _all | treats → treats_unit → key_family → requires_check → product_family → procedure_relation → key_technique → anchors_combo → key_site | 5 |  |
| I-03 | 2 | _all | treats → treats_unit → key_family → requires_check → product_family → procedure_relation → key_technique → anchors_combo → key_site | 2 |  |
| I-04 | 10 | intent | key_family → product_family → procedure_relation | 9 | {'key_family': 8, 'product_family': 6, 'procedure_relation': 2, 'key_technique': 1} |
| I-05 | 20 | intent | treats → treats_unit → key_technique → product_unit → uses_product → key_family → requires_check → product_family | 18 | {'treats': 9, 'treats_unit': 7, 'key_technique': 4, 'product_unit': 2, 'uses_product': 2, 'anchors_combo': 1, 'has_statement': 1, 'key_family': 1, 'key_site': 1, 'product_family': 1, 'requires_check': 1} |
| I-06 | 30 | intent | key_family → treats → treats_unit → procedure_relation → requires_check → product_family → key_technique → product_unit | 29 | {'key_family': 9, 'procedure_relation': 7, 'treats': 7, 'treats_unit': 7, 'requires_check': 4, 'key_technique': 3, 'product_family': 3, 'product_unit': 3, 'uses_product': 2, 'anchors_combo': 1} |
| I-07 | 10 | intent | treats → treats_unit → requires_check → anchors_combo → key_family | 9 | {'anchors_combo': 3, 'requires_check': 3, 'treats': 3, 'treats_unit': 3, 'concern_avoid': 2, 'concern_avoid_unit': 2, 'key_family': 2, 'product_family': 1} |
| I-09 | 15 | intent | requires_check → key_family → product_family → requires_check_unit → treats → treats_unit → procedure_relation → key_site | 14 | {'requires_check': 6, 'key_family': 4, 'product_family': 3, 'requires_check_unit': 3, 'has_complication': 1, 'key_site': 1, 'procedure_pair': 1, 'procedure_relation': 1, 'treats': 1, 'treats_unit': 1} |
| I-10 | 11 | intent | treats → treats_unit → key_technique → key_family → requires_check | 10 | {'treats': 6, 'treats_unit': 6, 'key_technique': 2, 'anchors_combo': 1, 'key_family': 1, 'procedure_relation': 1, 'requires_check': 1} |
| I-11 | 3 | _all | treats → treats_unit → key_family → requires_check → product_family → procedure_relation → key_technique → anchors_combo → key_site | 3 |  |

## 34 행

```json
{
 "rows": 34,
 "place": {
  "0홉·1쪽": 4,
  "1홉·1쪽": 8,
  "0홉·2쪽+": 1,
  "1홉·2쪽+": 8,
  "2홉+": 5,
  "받을 곳 없음": 8,
  "이름·속성만": 0
 },
 "shown": {
  "v22": 4,
  "v23": 9,
  "v24_no_unit": 12,
  "v24": 12
 },
 "shown_1hop": {
  "v22": 0,
  "v23": 5,
  "v24_no_unit": 8,
  "v24": 8
 },
 "zero_hop_p1": 4,
 "zero_hop_p1_in_section2_intents": 3,
 "missed_1hop_p1": [],
 "note": "34 행 문항은 461 행(표 근거)과 겹친다 — 표본 안 · 상한 참고"
}
```

| 문항 | 의도 | S 종류 | hit | 자리 | 종류 · 섹션 | v2.2 | v2.3 | v2.4(단위 규칙 없이) | v2.4 |
|---|---|---|---|---|---|---|---|---|---|
| Q020 | I-08 | product | 6 | 받을 곳 없음 | procedure_relation | False | False | False | False |
| Q027 | I-05 | unit_procedure | 1 | 0홉·2쪽+ | timeline | False | False | False | False |
| Q055 | I-04 | family | 1 | 0홉·1쪽 | disclosure | True | True | True | True |
| Q056 | I-07 | family | 1 | 받을 곳 없음 | procedure_relation | False | False | False | False |
| Q064 | I-07 | family | 3 | 2홉+ |  | False | False | False | False |
| Q070 | I-09 | family | 6 | 1홉·2쪽+ | procedure_relation | False | False | False | False |
| Q078 | I-02 | family | 1 | 0홉·1쪽 | overview | True | True | True | True |
| Q083 | I-05 | family | 5 | 1홉·2쪽+ | key_family · procedure_relation · product_family | False | False | False | False |
| Q097 | I-07 | family | 6 | 받을 곳 없음 | procedure_relation | False | False | False | False |
| Q098 | I-10 | family | 1 | 0홉·1쪽 | overview | True | True | True | True |
| Q099 | I-09 | concern | 1 | 2홉+ |  | False | False | False | False |
| Q102 | I-06 | family | 1 | 1홉·2쪽+ | key_family | False | False | False | False |
| Q106 | I-06 | family | 1 | 1홉·1쪽 | key_family | False | False | True | True |
| Q112 | I-07 | family | 11 | 받을 곳 없음 | procedure_relation | False | False | False | False |
| Q114 | I-07 | concern | 1 | 1홉·1쪽 | concern_avoid · concern_avoid_unit · treats · treats_unit | False | False | True | True |
| Q117 | I-11 | concern | 1 | 1홉·2쪽+ | anchors_combo | False | False | False | False |
| Q121 | I-01 | family | 1 | 1홉·1쪽 | key_family | False | False | True | True |
| Q124 | I-04 | family | 2 | 1홉·1쪽 | key_family · product_family | False | True | True | True |
| Q131 | I-05 | concern | 1 | 1홉·1쪽 | treats · treats_unit | False | True | True | True |
| Q133 | I-06 | concern | 1 | 2홉+ |  | False | False | False | False |
| Q136 | I-03 | technique | 2 | 1홉·2쪽+ | key_technique | False | False | False | False |
| Q140 | I-05 | family | 1 | 1홉·2쪽+ | key_family | False | False | False | False |
| Q141 | I-09 | concern | 1 | 1홉·2쪽+ | treats | False | False | False | False |
| Q161 | I-09 | check_condition | 5 | 1홉·1쪽 | requires_check_unit | False | True | True | True |
| Q169 | I-09 | family | 1 | 1홉·1쪽 | requires_check | False | True | True | True |
| Q185 | I-07 | family | 2 | 2홉+ |  | False | False | False | False |
| Q186 | I-07 | family | 3 | 받을 곳 없음 | procedure_relation | False | False | False | False |
| Q198 | I-06 | concern | 1 | 1홉·1쪽 | treats · treats_unit | False | True | True | True |
| Q200 | I-07 | product | 1 | 받을 곳 없음 | procedure_relation | False | False | False | False |
| Q201 | I-07 | family | 1 | 받을 곳 없음 | procedure_relation | False | False | False | False |
| Q212 | I-06 | product | 1 | 2홉+ |  | False | False | False | False |
| Q215 | I-05 | unit_procedure | 1 | 받을 곳 없음 | scope | False | False | False | False |
| Q233 | I-07 | family | 8 | 1홉·2쪽+ | key_family · procedure_relation | False | False | False | False |
| Q239 | I-04 | product | 1 | 0홉·1쪽 | safety.complications | True | True | True | True |
