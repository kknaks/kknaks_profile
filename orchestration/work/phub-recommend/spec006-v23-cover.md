# SPEC-006 v2.3 근거 셈 E — 안 닿은 34 행 × 걸음 1 선택지(spec006-v23-cover.py · 결정론)

```json
{
 "rows": 34,
 "by_place": {
  "0홉 · S 섹션": 14,
  "1홉 · 순서 표 · 앞 4 밖": 1,
  "1홉 · 순서 표 · 앞 4 안": 2,
  "1홉 · 순서 표 밖 종류": 4,
  "2홉+ · 대기열로만": 5,
  "어느 노드 섹션에도 없음": 8
 },
 "v22_shown": 16,
 "v23_shown": 19,
 "v22_shown_1hop": 2,
 "v23_shown_1hop": 5,
 "zero_hop": 14,
 "zero_hop_in_section2_intents": 3,
 "two_hop_plus": 5,
 "no_holder": 8,
 "no_holder_owner_kinds": {
  "procedure_relation": 7,
  "scope": 1
 },
 "v23_missed_1hop_kinds": {
  "concern_avoid": 1,
  "concern_avoid_unit": 1,
  "treats": 2,
  "treats_unit": 1
 },
 "note": "34 행은 461 행(순서 표 근거)의 부분집합과 겹친다 — 표본 안 셈 · 상한 참고 · 끝 조건은 「선택지에 뜸」 수까지만"
}
```

| 문항 | 의도 | 자리 | 종류 | v2.2 뜸 | v2.3 뜸 |
|---|---|---|---|---|---|
| Q020 | I-08 | 어느 노드 섹션에도 없음 | procedure_relation | False | False |
| Q027 | I-05 | 0홉 · S 섹션 | timeline | True | True |
| Q055 | I-04 | 0홉 · S 섹션 | disclosure | True | True |
| Q056 | I-07 | 어느 노드 섹션에도 없음 | procedure_relation | False | False |
| Q064 | I-07 | 2홉+ · 대기열로만 | 2홉 | False | False |
| Q070 | I-09 | 1홉 · 순서 표 · 앞 4 밖 | procedure_relation · product_family | False | True |
| Q078 | I-02 | 0홉 · S 섹션 | overview | True | True |
| Q083 | I-05 | 0홉 · S 섹션 | aftercare | True | True |
| Q097 | I-07 | 어느 노드 섹션에도 없음 | procedure_relation | False | False |
| Q098 | I-10 | 0홉 · S 섹션 | overview | True | True |
| Q099 | I-09 | 2홉+ · 대기열로만 | 2홉 | False | False |
| Q102 | I-06 | 0홉 · S 섹션 | evidence | True | True |
| Q106 | I-06 | 0홉 · S 섹션 | timeline | True | True |
| Q112 | I-07 | 어느 노드 섹션에도 없음 | procedure_relation | False | False |
| Q114 | I-07 | 1홉 · 순서 표 밖 종류 | concern_avoid · concern_avoid_unit · treats · treats_unit | False | False |
| Q117 | I-11 | 1홉 · 순서 표 · 앞 4 안 | anchors_combo | True | True |
| Q121 | I-01 | 0홉 · S 섹션 | evidence | True | True |
| Q124 | I-04 | 0홉 · S 섹션 | safety.side_effects | True | True |
| Q131 | I-05 | 1홉 · 순서 표 · 앞 4 안 | anchors_combo · treats · treats_unit | True | True |
| Q133 | I-06 | 2홉+ · 대기열로만 | 2홉 | False | False |
| Q136 | I-03 | 1홉 · 순서 표 밖 종류 | key_technique | False | True |
| Q140 | I-05 | 0홉 · S 섹션 | timeline | True | True |
| Q141 | I-09 | 1홉 · 순서 표 밖 종류 | treats | False | False |
| Q161 | I-09 | 0홉 · S 섹션 | checks | True | True |
| Q169 | I-09 | 0홉 · S 섹션 | checks | True | True |
| Q185 | I-07 | 2홉+ · 대기열로만 | 2홉 | False | False |
| Q186 | I-07 | 어느 노드 섹션에도 없음 | procedure_relation | False | False |
| Q198 | I-06 | 1홉 · 순서 표 밖 종류 | treats · treats_unit | False | True |
| Q200 | I-07 | 어느 노드 섹션에도 없음 | procedure_relation | False | False |
| Q201 | I-07 | 어느 노드 섹션에도 없음 | procedure_relation | False | False |
| Q212 | I-06 | 2홉+ · 대기열로만 | 2홉 | False | False |
| Q215 | I-05 | 어느 노드 섹션에도 없음 | scope | False | False |
| Q233 | I-07 | 0홉 · S 섹션 | evidence | True | True |
| Q239 | I-04 | 0홉 · S 섹션 | safety.complications | True | True |
