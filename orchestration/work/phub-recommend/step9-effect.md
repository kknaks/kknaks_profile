# 실버 9단계 효과 재셈 — A 행 닫힘(행 단위)

> `step9-effect.py`(결정론 · 읽기만) · 레코드 `step9-explanations.json` · 조사 판 판정 `step9-research.json` 과 행마다 대조.

## 2차 A(rerun-v3 · fail-triage2 cls=A) — 54행

| 판정 | 행 |
|---|---|
| alternatives 에만(골드 안 나감) | 2 |
| 값 사전(시맨틱 · 골드 globals) | 1 |
| 골드 section 으로(실버 변경 없음) | 11 |
| 실버 9단계로 닫힘 | 39 |
| 안 닫힘 | 1 |

조사 판과 다른 행: 2

| 문항 | 케이스 | 원장 경로 | 판정 | 근거 | 붙는 노드 | 조사 판 |
|---|---|---|---|---|---|---|
| Q005 | case3 | `taxonomy.modality[0].subcategories[2].items[5].extracted.onset_duration.duration` | 실버 9단계로 닫힘 | S9:taxonomy.modality[0].subcategories[2].items[5].extracted. | unit_procedure:U5-010 · unit_procedure:U5-011 · unit_procedure:U5-012 | 실버 9단계로 닫힘 |
| Q009 | case2 | `taxonomy.modality[8].subcategories[3].items[0].extracted.mechanism` | 실버 9단계로 닫힘 | S9:taxonomy.modality[8].subcategories[3].items[0].extracted. | product:auto-40-1774737181584 | 실버 9단계로 닫힘 |
| Q009 | case3 | `taxonomy.modality[8].subcategories[3].items[0].extracted.onset_duration.duration` | 실버 9단계로 닫힘 | S9:taxonomy.modality[8].subcategories[3].items[0].extracted. | product:auto-40-1774737181584 | 실버 9단계로 닫힘 |
| Q039 | case2 | `products.skin_booster.products[3].note` | 실버 9단계로 닫힘 | S9:taxonomy.modality[3].products[3].note | unit_procedure:U5-009 | 실버 9단계로 닫힘 |
| Q039 | case3 | `products.skin_booster.products[3].note` | 실버 9단계로 닫힘 | S9:taxonomy.modality[3].products[3].note | unit_procedure:U5-009 | 실버 9단계로 닫힘 |
| Q040 | case3 | `taxonomy.modality[0].subcategories[2].items[5].extracted.onset_duration.duration` | 실버 9단계로 닫힘 | S9:taxonomy.modality[0].subcategories[2].items[5].extracted. | unit_procedure:U5-010 · unit_procedure:U5-011 · unit_procedure:U5-012 | 실버 9단계로 닫힘 |
| Q047 | case2 | `complications.categories[1].complications[0].management` | 골드 section 으로(실버 변경 없음) | safety.management | family:M2 | 골드 section 으로(실버 변경 없음) |
| Q047 | case3 | `complications.categories[1].complications[0].management` | 골드 section 으로(실버 변경 없음) | safety.management | family:M2 | 골드 section 으로(실버 변경 없음) |
| Q054 | case2 | `extracted.M3.onset_duration.onset` | 실버 9단계로 닫힘 | S9:taxonomy.modality[2].extracted.onset_duration.onset | family:M3 | 실버 9단계로 닫힘 |
| Q055 | case2 | `extracted.M2.onset_duration.duration` | 실버 9단계로 닫힘 | S9:taxonomy.modality[1].extracted.onset_duration.duration | family:M2 | 실버 9단계로 닫힘 |
| Q057 | case2 | `extracted.M4.overview` | 실버 9단계로 닫힘 | S9:taxonomy.modality[3].extracted.overview | family:M4 | 실버 9단계로 닫힘 |
| Q067 | case3 | `extracted.M2.onset_duration.duration` | 실버 9단계로 닫힘 | S9:taxonomy.modality[1].extracted.onset_duration.duration | family:M2 | 실버 9단계로 닫힘 |
| Q087 | case3 | `extracted.M11.related_techniques[2]` | 실버 9단계로 닫힘 | S9:taxonomy.modality[10].extracted.related_techniques[2] | family:M11 | 실버 9단계로 닫힘 |
| Q087 | case3 | `extracted.M12.mechanism` | 실버 9단계로 닫힘 | S9:taxonomy.modality[11].extracted.mechanism | family:M12 | 실버 9단계로 닫힘 |
| Q089 | case3 | `extracted.M11.indications.primary[0]` | 실버 9단계로 닫힘 | S9:taxonomy.modality[10].extracted.indications.primary[0] | family:M11 | 실버 9단계로 닫힘 |
| Q089 | case3 | `extracted.M11.indications.primary[0]` | 실버 9단계로 닫힘 | S9:taxonomy.modality[10].extracted.indications.primary[0] | family:M11 | 실버 9단계로 닫힘 |
| Q105 | case3 | `pih-risk.procedures[6].name` | 안 닫힘 | 라벨 · 메타 칸 또는 대상 밖 |  | 안 닫힘 |
| Q114 | case2 | `extracted.M8.indications.primary[0]` | 실버 9단계로 닫힘 | S9:taxonomy.modality[7].extracted.indications.primary[0] | family:M8 | 실버 9단계로 닫힘 |
| Q117 | case2 | `problem-packages.problems[5].complaints[1].alternatives[0]` | 실버 9단계로 닫힘 | S9:problem-packages.problems[12].complaints[0].alternatives[ | unit_procedure:U5-009 · unit_procedure:U5-018 · unit_procedure:U5-019 · unit_procedure:U5-023 | 실버 9단계로 닫힘 |
| Q118 | case2 | `problem-packages.problems[5].complaints[6].cc_detail` | 실버 9단계로 닫힘 | S9:problem-packages.problems[5].complaints[6].cc_detail | unit_procedure:U5-023 · unit_procedure:U5-024 · unit_procedure:U5-025 | 실버 9단계로 닫힘 |
| Q118 | case2 | `problem-packages.problems[5].complaints[7].cc_detail` | 실버 9단계로 닫힘 | S9:problem-packages.problems[5].complaints[7].cc_detail | unit_procedure:U5-018 · unit_procedure:U5-019 · unit_procedure:U5-040 · unit_procedure:U5-142 | 실버 9단계로 닫힘 |
| Q123 | case3 | `extracted.M8.indications.primary[1]` | 실버 9단계로 닫힘 | S9:taxonomy.modality[7].extracted.indications.primary[1] | family:M8 | 실버 9단계로 닫힘 |
| Q133 | case3 | `extracted.M2.indications.primary[2]` | 실버 9단계로 닫힘 | S9:taxonomy.modality[1].extracted.indications.primary[2] | family:M2 | 실버 9단계로 닫힘 |
| Q140 | case3 | `complications.categories[4].complications[1].management` | 골드 section 으로(실버 변경 없음) | safety.management | family:M8 | 골드 section 으로(실버 변경 없음) |
| Q162 | case2 | `extracted.M15.mechanism` | 실버 9단계로 닫힘 | S9:taxonomy.modality[14].extracted.mechanism | family:M15 | 실버 9단계로 닫힘 |
| Q162 | case3 | `extracted.M15.onset_duration.onset` | 실버 9단계로 닫힘 | S9:taxonomy.modality[14].extracted.onset_duration.onset | family:M15 | 실버 9단계로 닫힘 |
| Q167 | case2 | `complications.categories[8].complications[2].management` | 골드 section 으로(실버 변경 없음) | safety.management | family:M15 | 골드 section 으로(실버 변경 없음) |
| Q167 | case3 | `complications.categories[8].complications[2].management` | 골드 section 으로(실버 변경 없음) | safety.management | family:M15 | 골드 section 으로(실버 변경 없음) |
| Q168 | case2 | `extracted.M15.indications.primary[1]` | 실버 9단계로 닫힘 | S9:taxonomy.modality[14].extracted.indications.primary[1] | family:M15 | 실버 9단계로 닫힘 |
| Q168 | case2 | `extracted.M15.overview` | 실버 9단계로 닫힘 | S9:taxonomy.modality[14].extracted.overview | family:M15 | 실버 9단계로 닫힘 |
| Q168 | case3 | `extracted.M15.indications.primary[1]` | 실버 9단계로 닫힘 | S9:taxonomy.modality[14].extracted.indications.primary[1] | family:M15 | 실버 9단계로 닫힘 |
| Q169 | case2 | `complications.categories[8].complications[1].prevention` | 골드 section 으로(실버 변경 없음) | safety.management | family:M15 | 골드 section 으로(실버 변경 없음) |
| Q171 | case2 | `complications.categories[8].complications[1].management` | 골드 section 으로(실버 변경 없음) | safety.management | family:M15 | 골드 section 으로(실버 변경 없음) |
| Q172 | case2 | `complications.categories[8].complications[2].prevention` | 골드 section 으로(실버 변경 없음) | safety.management | family:M15 | 골드 section 으로(실버 변경 없음) |
| Q172 | case3 | `complications.categories[8].complications[2].prevention` | 골드 section 으로(실버 변경 없음) | safety.management | family:M15 | 골드 section 으로(실버 변경 없음) |
| Q174 | case2 | `complications.categories[8].complications[2].management` | 골드 section 으로(실버 변경 없음) | safety.management | family:M15 | 골드 section 으로(실버 변경 없음) |
| Q175 | case2 | `taxonomy.modality[14].subcategories[0].items[45].extracted.mechanism` | 실버 9단계로 닫힘 | S9:taxonomy.modality[14].subcategories[0].items[45].extracte | unit_procedure:U5-034 | 실버 9단계로 닫힘 |
| Q175 | case3 | `extracted.M15.indications.primary[1]` | 실버 9단계로 닫힘 | S9:taxonomy.modality[14].extracted.indications.primary[1] | family:M15 | 실버 9단계로 닫힘 |
| Q178 | case3 | `extracted.M7.overview` | 실버 9단계로 닫힘 | S9:taxonomy.modality[6].extracted.overview | family:M7 | 실버 9단계로 닫힘 |
| Q179 | case2 | `complications.categories[3].complications[7].management` | 골드 section 으로(실버 변경 없음) | safety.management | family:M7 | 골드 section 으로(실버 변경 없음) |
| Q206 | case2 | `post-procedure-timeline.reaction_levels.caution` | 값 사전(시맨틱 · 골드 globals) | value_dictionary | scope:all | 값 사전(시맨틱 · 골드 globals) |
| Q210 | case2 | `taxonomy.modality[7].subcategories[3].items[3].extracted.indications.primary[0]` | 실버 9단계로 닫힘 | S9:taxonomy.modality[7].subcategories[3].items[3].extracted. | product:M8-4-3 | 실버 9단계로 닫힘 |
| Q211 | case2 | `taxonomy.modality[7].subcategories[0].items[7].extracted.indications.primary[0]` | 실버 9단계로 닫힘 | S9:taxonomy.modality[7].subcategories[0].items[7].extracted. | unit_procedure:U5-137 | 실버 9단계로 닫힘 |
| Q214 | case2 | `taxonomy.modality[14].subcategories[3].items[0].extracted.onset_duration` | alternatives 에만(골드 안 나감) | S9:taxonomy.modality[14].subcategories[3].items[0].extracted | product:M15-4-1 | 실버 9단계로 닫힘 ← 다름 |
| Q214 | case2 | `taxonomy.modality[14].subcategories[3].items[0].extracted.onset_duration.duration` | 실버 9단계로 닫힘 | S9:taxonomy.modality[14].subcategories[3].items[0].extracted | product:M15-4-1 | 실버 9단계로 닫힘 |
| Q214 | case3 | `taxonomy.modality[14].subcategories[3].items[0].extracted.onset_duration.onset` | alternatives 에만(골드 안 나감) | S9:taxonomy.modality[14].subcategories[3].items[0].extracted | product:M15-4-1 | 실버 9단계로 닫힘 ← 다름 |
| Q218 | case2 | `taxonomy.modality[8].subcategories[2].items[0].extracted.indications.primary` | 실버 9단계로 닫힘 | S9:taxonomy.modality[8].subcategories[2].items[0].extracted. | product:M9-3-1 | 실버 9단계로 닫힘 |
| Q218 | case3 | `taxonomy.modality[8].subcategories[2].items[0].extracted.indications.primary` | 실버 9단계로 닫힘 | S9:taxonomy.modality[8].subcategories[2].items[0].extracted. | product:M9-3-1 | 실버 9단계로 닫힘 |
| Q221 | case3 | `extracted.M7.onset_duration.duration` | 실버 9단계로 닫힘 | S9:taxonomy.modality[6].extracted.onset_duration.duration | family:M7 | 실버 9단계로 닫힘 |
| Q230 | case2 | `taxonomy.modality[0].subcategories[2].items[5].extracted.onset_duration.duration` | 실버 9단계로 닫힘 | S9:taxonomy.modality[0].subcategories[2].items[5].extracted. | unit_procedure:U5-010 · unit_procedure:U5-011 · unit_procedure:U5-012 | 실버 9단계로 닫힘 |
| Q230 | case3 | `taxonomy.modality[0].subcategories[2].items[5].extracted.onset_duration.duration` | 실버 9단계로 닫힘 | S9:taxonomy.modality[0].subcategories[2].items[5].extracted. | unit_procedure:U5-010 · unit_procedure:U5-011 · unit_procedure:U5-012 | 실버 9단계로 닫힘 |
| Q231 | case2 | `taxonomy.modality[0].subcategories[2].items[5].extracted.onset_duration.onset` | 실버 9단계로 닫힘 | S9:taxonomy.modality[0].subcategories[2].items[5].extracted. | unit_procedure:U5-010 · unit_procedure:U5-011 · unit_procedure:U5-012 | 실버 9단계로 닫힘 |
| Q232 | case2 | `taxonomy.modality[0].subcategories[2].items[5].extracted.onset_duration.duration` | 실버 9단계로 닫힘 | S9:taxonomy.modality[0].subcategories[2].items[5].extracted. | unit_procedure:U5-010 · unit_procedure:U5-011 · unit_procedure:U5-012 | 실버 9단계로 닫힘 |
| Q232 | case3 | `taxonomy.modality[0].subcategories[2].items[5].extracted.onset_duration.duration` | 실버 9단계로 닫힘 | S9:taxonomy.modality[0].subcategories[2].items[5].extracted. | unit_procedure:U5-010 · unit_procedure:U5-011 · unit_procedure:U5-012 | 실버 9단계로 닫힘 |

## rerun-v5a case3 A(gold_match 무히트 · 조사 셈 30) — 30행

| 판정 | 행 |
|---|---|
| alternatives 에만(골드 안 나감) | 1 |
| 골드 section 으로(실버 변경 없음) | 6 |
| 실버 9단계로 닫힘 | 19 |
| 안 닫힘 | 4 |

조사 판과 다른 행: 1

| 문항 | 케이스 | 원장 경로 | 판정 | 근거 | 붙는 노드 | 조사 판 |
|---|---|---|---|---|---|---|
| Q003 | case3 | `taxonomy.modality[0].subcategories[2].items[7].extracted.indications.primary[0]` | 실버 9단계로 닫힘 | S9:taxonomy.modality[0].subcategories[2].items[7].extracted. | unit_procedure:U5-016 · unit_procedure:U5-017 | 실버 9단계로 닫힘 |
| Q009 | case3 | `taxonomy.modality[8].subcategories[3].items[0].extracted.mechanism` | 실버 9단계로 닫힘 | S9:taxonomy.modality[8].subcategories[3].items[0].extracted. | product:auto-40-1774737181584 | 실버 9단계로 닫힘 |
| Q015 | case3 | `extracted.M9.onset_duration.duration` | 실버 9단계로 닫힘 | S9:taxonomy.modality[8].extracted.onset_duration.duration | family:M9 | 실버 9단계로 닫힘 |
| Q035 | case3 | `complications.categories[0].complications[1].management` | 골드 section 으로(실버 변경 없음) | safety.management | family:M1 | 골드 section 으로(실버 변경 없음) |
| Q036 | case3 | `post-procedure-timeline.timelines[0].phases[1].period` | 안 닫힘 | 라벨 · 메타 칸 또는 대상 밖 |  | 안 닫힘 |
| Q039 | case3 | `products.skin_booster.products[3].note` | 실버 9단계로 닫힘 | S9:taxonomy.modality[3].products[3].note | unit_procedure:U5-009 | 실버 9단계로 닫힘 |
| Q040 | case3 | `taxonomy.modality[0].subcategories[2].items[5].extracted.onset_duration.duration` | 실버 9단계로 닫힘 | S9:taxonomy.modality[0].subcategories[2].items[5].extracted. | unit_procedure:U5-010 · unit_procedure:U5-011 · unit_procedure:U5-012 | 실버 9단계로 닫힘 |
| Q043 | case3 | `extracted.M7.overview` | 실버 9단계로 닫힘 | S9:taxonomy.modality[6].extracted.overview | family:M7 | 실버 9단계로 닫힘 |
| Q046 | case3 | `complications.categories[1].complications[2].management` | 골드 section 으로(실버 변경 없음) | safety.management | family:M2 | 골드 section 으로(실버 변경 없음) |
| Q047 | case3 | `complications.categories[1].complications[0].management` | 골드 section 으로(실버 변경 없음) | safety.management | family:M2 | 골드 section 으로(실버 변경 없음) |
| Q050 | case3 | `complications.categories[1].complications[6].management` | 골드 section 으로(실버 변경 없음) | safety.management | family:M2 | 골드 section 으로(실버 변경 없음) |
| Q054 | case3 | `extracted.M3.onset_duration.onset` | 실버 9단계로 닫힘 | S9:taxonomy.modality[2].extracted.onset_duration.onset | family:M3 | 실버 9단계로 닫힘 |
| Q075 | case3 | `extracted.M9.onset_duration.onset` | 실버 9단계로 닫힘 | S9:taxonomy.modality[8].extracted.onset_duration.onset | family:M9 | 실버 9단계로 닫힘 |
| Q087 | case3 | `extracted.M11.related_techniques[2]` | 실버 9단계로 닫힘 | S9:taxonomy.modality[10].extracted.related_techniques[2] | family:M11 | 실버 9단계로 닫힘 |
| Q107 | case3 | `pih-risk.description` | 안 닫힘 | 라벨 · 메타 칸 또는 대상 밖 |  | 안 닫힘 |
| Q133 | case3 | `extracted.M2.indications.primary[2]` | 실버 9단계로 닫힘 | S9:taxonomy.modality[1].extracted.indications.primary[2] | family:M2 | 실버 9단계로 닫힘 |
| Q162 | case3 | `extracted.M15.mechanism` | 실버 9단계로 닫힘 | S9:taxonomy.modality[14].extracted.mechanism | family:M15 | 실버 9단계로 닫힘 |
| Q165 | case3 | `post-procedure-timeline.timelines[9].phases[3].label` | 안 닫힘 | 라벨 · 메타 칸 또는 대상 밖 |  | 안 닫힘 |
| Q168 | case3 | `extracted.M15.indications.primary[1]` | 실버 9단계로 닫힘 | S9:taxonomy.modality[14].extracted.indications.primary[1] | family:M15 | 실버 9단계로 닫힘 |
| Q171 | case3 | `complications.categories[8].complications[1].management` | 골드 section 으로(실버 변경 없음) | safety.management | family:M15 | 골드 section 으로(실버 변경 없음) |
| Q172 | case3 | `complications.categories[8].complications[2].prevention` | 골드 section 으로(실버 변경 없음) | safety.management | family:M15 | 골드 section 으로(실버 변경 없음) |
| Q175 | case3 | `extracted.M15.indications.primary[1]` | 실버 9단계로 닫힘 | S9:taxonomy.modality[14].extracted.indications.primary[1] | family:M15 | 실버 9단계로 닫힘 |
| Q178 | case3 | `extracted.M2.indications` | 실버 9단계로 닫힘 | S9:taxonomy.modality[1].extracted.indications.primary[0] | family:M2 | 실버 9단계로 닫힘 |
| Q214 | case3 | `taxonomy.modality[14].subcategories[3].items[0].extracted.onset_duration.onset` | alternatives 에만(골드 안 나감) | S9:taxonomy.modality[14].subcategories[3].items[0].extracted | product:M15-4-1 | 실버 9단계로 닫힘 ← 다름 |
| Q216 | case3 | `extracted.M4.overview` | 실버 9단계로 닫힘 | S9:taxonomy.modality[3].extracted.overview | family:M4 | 실버 9단계로 닫힘 |
| Q218 | case3 | `taxonomy.modality[8].subcategories[2].items[0].extracted.indications.primary` | 실버 9단계로 닫힘 | S9:taxonomy.modality[8].subcategories[2].items[0].extracted. | product:M9-3-1 | 실버 9단계로 닫힘 |
| Q219 | case3 | `procedure-profiles.profiles[2]` | 안 닫힘 | 라벨 · 메타 칸 또는 대상 밖 |  | 안 닫힘 |
| Q222 | case3 | `taxonomy.modality[8].subcategories[1].items[2].extracted.mechanism` | 실버 9단계로 닫힘 | S9:taxonomy.modality[8].subcategories[1].items[2].extracted. | product:M9-2-5 | 실버 9단계로 닫힘 |
| Q231 | case3 | `taxonomy.modality[0].subcategories[2].items[5].extracted.onset_duration` | 실버 9단계로 닫힘 | S9:taxonomy.modality[0].subcategories[2].items[5].extracted. | unit_procedure:U5-010 · unit_procedure:U5-011 · unit_procedure:U5-012 | 실버 9단계로 닫힘 |
| Q232 | case3 | `taxonomy.modality[0].subcategories[2].items[5].extracted.onset_duration.duration` | 실버 9단계로 닫힘 | S9:taxonomy.modality[0].subcategories[2].items[5].extracted. | unit_procedure:U5-010 · unit_procedure:U5-011 · unit_procedure:U5-012 | 실버 9단계로 닫힘 |

