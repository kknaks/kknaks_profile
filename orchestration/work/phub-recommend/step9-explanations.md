# 실버 9단계 — 설명 사실 원장(step9-explanations)

> 생성 `step9-apply.py`(결정론 · 두 번 cmp 같음) · 결정 `step9-decisions.json`(사용자 11-01 「추천으로 데이터 결정하자」) · 조사 `step9-research.md`. **원장 인용은 work/ 안에만**(공개 레포 커밋 안 함). 골드 반영(section `safety.management` 등)은 다음 허브 발주.

## 셈

| 칸 | 값 |
|---|---|
| records | 5,847 |
| attached_records | 5,161 |
| node_slots | 2,946 |
| facts_out | 5,312 |
| alternatives | 343 |
| source_conflicts | 12 |
| value_dictionary | 8 |
| section_map | 435 |
| human_check | 0 |
| open | 0 |

레코드 상태:

| 상태 | 레코드 |
|---|---|
| source_conflict(싣지 않음) | 12 |
| 대조본 같음(same_as taxonomy products) | 38 |
| 대조본 같음(same_as taxonomy 정본) | 286 |
| 붙음 | 5,161 |
| 붙이지 않음(고민 CC → 붙을 노드 없음(부위)) | 10 |
| 붙이지 않음(고민 CC → 붙을 노드 없음(시술 아님)) | 10 |
| 붙이지 않음(고민 항목 → 붙을 노드 없음(부위)) | 5 |
| 붙이지 않음(고민 항목 → 붙을 노드 없음(시술 아님)) | 5 |
| 붙이지 않음(원문 보관(6단계 패키지)) | 145 |
| 붙이지 않음(원문 보관(값)) | 146 |
| 붙이지 않음(원문 보관(시술 아님(다른 단계))) | 14 |
| 붙이지 않음(원문 보관(시술 아님)) | 8 |
| 붙이지 않음(원문 보관(원장님 문의)) | 7 |

규칙별:

| 규칙 | 레코드 |
|---|---|
| R9-1 | 4,284 |
| R9-2 | 600 |
| R9-2b | 1 |
| R9-3 | 585 |
| R9-4 | 17 |
| R9-5 | 357 |
| R9-8 | 3 |

## D9-3 같은 노드 · 같은 칸(node_slots)

| 분류 | 칸 수 | 뜻 |
|---|---|---|
| 한 원천 | 2,317 | 원천 레코드 하나 — 충돌 아님 |
| 같음 | 33 | 원천 여럿 · 값 같음(same_as) |
| ① 포함 관계 | 43 | 한쪽이 다른 쪽을 정규화 포함 · 또는 숫자 · 단위 집합 같음 → 긴 쪽 하나 |
| ② 숫자 다름 | 196 | resolved 하나 · 나머지 alternatives(343) — 늦은 쪽 68 · 원천 우선순위 62 · 짧은 쪽 66 |
| ③ 숫자 없는 다른 문장 | 357 | 둘 다 실음 · multi_source |

| 분류 · 칸 | 수 |
|---|---|
| ① cc_detail | 2 |
| ① detail | 1 |
| ① indications.primary | 1 |
| ① mechanism | 10 |
| ① onset_duration.duration | 11 |
| ① onset_duration.onset | 8 |
| ① onset_duration.peak_effect | 3 |
| ① overview | 7 |
| ② cc_detail | 2 |
| ② detail | 11 |
| ② mechanism | 34 |
| ② onset_duration.duration | 69 |
| ② onset_duration.onset | 70 |
| ② overview | 10 |
| ③ alternatives | 32 |
| ③ cc_detail | 37 |
| ③ description | 1 |
| ③ detail | 72 |
| ③ indications.extended | 1 |
| ③ indications.primary | 89 |
| ③ indications.secondary | 2 |
| ③ mechanism | 46 |
| ③ onset_duration.duration | 4 |
| ③ overview | 73 |

## 골드로 나갈 fact(section 별 · 다음 허브 발주)

| section | fact |
|---|---|
| disclosure | 2 |
| method | 638 |
| overview | 3,762 |
| recovery | 910 |

8단계 실버 그대로 · section 만 정함(R9-6 · D9-1):

| section | 칸 |
|---|---|
| safety.complications | 176 |
| safety.management | 129 |
| safety.side_effects | 130 |

## 대조본 source_conflict(싣지 않음 · D9-4 · R9-2a)

| 규칙 | 원천 경로 | 칸 | 대조 정본 |
|---|---|---|---|
| D9-4 | `extracted.M12.mechanism` | mechanism | family:M12 |
| D9-4 | `extracted.M12.overview` | overview | family:M12 |
| D9-4 | `extracted.M17.mechanism` | mechanism | family:M17 |
| D9-4 | `extracted.M17.overview` | overview | family:M17 |
| D9-4 | `extracted.M2.indications.extended[6]` | indications.extended | family:M2 |
| D9-4 | `extracted.M2.mechanism` | mechanism | family:M2 |
| D9-4 | `extracted.M5.mechanism` | mechanism | family:M5 |
| R9-2a | `products.biostimulator.products[3].ingredient` | ingredient | M3-P-3 |
| R9-2a | `products.biostimulator.products[4].ingredient` | ingredient | M3-P-4 |
| R9-2a | `products.botulinum_toxin.products[10].note` | note | M1-P-10 |
| R9-2a | `products.prp_exosome.products[3].note` | note | M5-P-3 |
| R9-2a | `products.prp_exosome.products[4].note` | note | M5-P-4 |

## 값 사전(D9-7 · 시맨틱 value_dictionary)

| 사전 | 키 | 원문 |
|---|---|---|
| reaction_levels | abnormal | 이상 반응 -- 모니터링 필요, 경과 관찰 |
| reaction_levels | caution | 주의 반응 -- 24-48시간 내 클리닉 연락 |
| reaction_levels | emergency | 응급 반응 -- 즉시 응급실/클리닉 |
| reaction_levels | normal | 정상 반응 -- 예상 범위, 조치 불필요 |
| severity_levels | critical | 위급 — 응급 대응, 비가역적 손상 가능 |
| severity_levels | mild | 경미 — 자연 소실, 경과 관찰 |
| severity_levels | moderate | 중등도 — 치료 필요, 클리닉 방문 |
| severity_levels | severe | 중증 — 즉시 치료, 후유증 가능 |

## ② 처분 예(처음 10)

| 노드 | 칸 | 고른 방법 | resolved | alternatives |
|---|---|---|---|---|
| product:M1-1-2 | mechanism | 원천 우선순위 | 「SNARE 복합체(SNAP-25)를 절단하여 신경 말단에서의 아세틸콜린 분비를 차단한다. 」 | 「SNARE 복합체(SNAP-25)를 절단하여 신경말단에서의 아세틸콜린 분」 |
| product:M1-2-1 | mechanism | 원천 우선순위 | 「신경 말단에서 SNARE 복합체(SNAP-25)를 절단하여 아세틸콜린 분비를 차단, 근육 」 | 「SNARE 복합체(SNAP-25)를 절단하여 신경근접합부에서 아세틸콜린의」 |
| product:M1-2-1 | onset_duration.onset | 늦은 쪽 | 「3-7일 이내 효과 시작, 2-4주 점진적 개선, 1개월 완전 효과」 | 「2-3일부터 효과 시작」 |
| product:M1-2-2 | mechanism | 원천 우선순위 | 「Clostridium botulinum Type A가 신경근 접합부에서 SNARE 복합체(」 | 「SNARE 복합체(SNAP-25)를 선택적으로 절단하여 아세틸콜린 분비를」 |
| product:M1-2-3 | mechanism | 원천 우선순위 | 「Clostridium botulinum Type A 독소가 SNARE 복합체의 SNAP-2」 | 「보톡스는 SNAP-25 SNARE 복합체를 절단하여 신경근 접합부에서 아」 |
| product:M1-2-3 | onset_duration.duration | 짧은 쪽 | 「완전 효과 도달 1개월, 유지 기간 3-4개월」 | 「3-6개월」 |
| product:M1-2-3 | onset_duration.onset | 늦은 쪽 | 「3-7일」 | 「2-3일」 |
| product:M10-1-1 | onset_duration.duration | 짧은 쪽 | 「3-6개월 유지, 정기적 시술로 지속 효과」 | 「6-9개월」 |
| product:M10-1-1 | onset_duration.onset | 늦은 쪽 | 「2-4주」 | 「1-2주 후부터 단계적 개선, 4주 후 명확한 효과」 |
| product:M10-2-2 | onset_duration.duration | 짧은 쪽 | 「3-6개월 효과 유지, 월 1-2회 정기 시술로 지속」 | 「6-12개월」 |

## open — 0

