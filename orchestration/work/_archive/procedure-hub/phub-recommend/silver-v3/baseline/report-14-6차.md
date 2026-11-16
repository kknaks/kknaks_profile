## 14. 6차 빌드 · ERD v3.1 + 엑소좀 approved

5차 = `baseline/manifest-5차.json`(ERD v3 · 결정 묶음 3 approved 24 까지) · 6차 = ERD **v3.1**(`erd-v3.1.json` · `erd-v3.1-dictionaries.json` · 빌더 V3.1-1~10 · 발주서 `silver-build-6-brief.md`) + 엑소좀 EXO-02·05·06 을 v3.1 kind 로 올린 결정 6 건(`decisions/batch3/DEC-2026-11-05-B3-EXO-*` · 사용자 확정 방향). ③ 결정 적용 전 분해 = `erd-v3.1-tuples.json` 요약 차이 0/233(§5 · 시술 · 부작용 · 조건 + 행 대조).

### 결정 적용(6차)

| kind | applied | recorded | rejected | no_target |
|---|---|---|---|---|
| adverse_tuple_assign | 23 | 0 | 0 | 0 |
| canonical_mapping | 11 | 0 | 0 | 0 |
| canonical_rename | 2 | 0 | 0 | 0 |
| conflict_resolution | 0 | 16 | 0 | 0 |
| dictionary_add | 193 | 0 | 0 | 0 |
| dictionary_remove | 1 | 0 | 0 | 0 |
| edge_create | 8 | 0 | 0 | 0 |
| event_split | 3 | 0 | 0 | 0 |
| fold_approve | 21 | 0 | 0 | 0 |
| ledger_correction_note | 0 | 3 | 0 | 0 |
| product_reclassify | 2 | 0 | 0 | 0 |
| reclassification | 1 | 0 | 0 | 0 |
| scope_review | 0 | 10 | 0 | 0 |
| tuple_assign | 6 | 0 | 0 | 0 |
| verification_hold | 0 | 1 | 0 | 0 |

거부·대상 없음: 없음 — 기존 결정(_bootstrap · batch1 · 2a · 2b · 3) 전부 v3.1 빌더가 받았다.

v3.1 로 옮겨 적용한 옛 결정(거부 아님 · 적용 로그 note):

- 옛 네 칸 adverse_tuple_assign(raw_name) 10 — course_id 를 단위에서 빼 그 이름 → 단위 R15 엣지의 course 로(미상은 null) · 상대 부위 site_id 는 none(relative_site_text): `B2B-ISE-01`, `B2B-PAR-01`, `B2B-PAR-02`, `B2B-PAR-03`, `B2B-PAR-04`, `B3-ADV-01`, `B3-ADV-02`, `B3-ADV-03`, `B3-ADV-04`, `B3-ADV-05`
- 옛 adverse_tuple_assign(kind=expression) 13 — 표현은 개체가 아니므로(V3.1-10) 그 자리의 문구 사전 항목 지도로 적용(phrase_map 과 같은 효과 · status=approved · 같은 정규화형 자리 전부): `B2B-TEV-01`→PHR-0d10bd307d, `B2B-TEV-02`→PHR-4db30daf7b, `B2B-TEV-03`→PHR-4db30daf7b, `B2B-TEV-04`→PHR-0d10bd307d, `B2B-TEV-05`→PHR-559472746f, `B2B-TEV-06`→PHR-4db30daf7b, `B2B-TEV-07`→PHR-4db30daf7b, `B2B-TEV-08`→PHR-0d10bd307d, `B2B-TEV-09`→PHR-559472746f, `B2B-TEV-10`→PHR-0d10bd307d, `B3-ADV-COURSE-01`→PHR-f02aa749d6, `B3-ADV-COURSE-02`→PHR-1fd0edfbe0, `B3-ADV-COURSE-03`→PHR-d7c258f5f6
- 옛 네 칸 edge_create(adverse_tuple) 3 — R30 이라 경과 자리 없음(세 칸 끝 · 경과 「미상」 버림 아님 = 원래 null): `B3-R30-01`, `B3-R30-02`, `B3-R30-03`

#### 엑소좀(EXO-02·05·06 · v3.1 kind)

| 결정 | kind | 단계 | 결과 | 내용 |
|---|---|---|---|---|
| EXO-02A | product_reclassify | ⓪ | applied | ASCEplus: M5→M4 · PRD-be57673deb → PRD-e45033395c(옛 id alias) |
| EXO-02B | product_reclassify | ⓪ | applied | EXOSOME SKIN: M5→M4 · PRD-8a1d788eec → PRD-f4264ddf37(옛 id alias) |
| EXO-06 | dictionary_remove | ① | applied | modality 「PRP/자가혈」 동의어 「PRP/엑소좀」 제거 |
| EXO-05A | edge_create | ⑤ | applied | clinical_rule:RUL-dacbdc189b→product:PRD-e45033395c |
| EXO-05B | edge_create | ⑤ | applied | clinical_rule:RUL-dacbdc189b→product:PRD-f4264ddf37 |
| EXO-05C | edge_create | ⑤ | applied | clinical_rule:RUL-dacbdc189b→product:PRD-209656bf00 |

- ② 재분류: R4 5 엣지가 M5 → M4 로 옮겨졌다(reclassified_from_modality · decision_id · section_key 보존). 제품 레코드 id 는 새 PRD-, 옛 id 는 alias.
- ⑤ 임상 규칙: clinical_rule(product_note) 「화장품 허가 (주사 사용 불법)」(`taxonomy.json:modality[].products[].note@4/3`) → R32 3(scope=product · severity=prohibited · basis=edge_create) — ASCEplus · EXOSOME SKIN · 셀엑소좀. 기법=주사 끝은 만들지 않았다(R32 scope=all 은 주사 전체에 걸린다 · 발주서는 제품만).
- ⑥ 「PRP/엑소좀」 M5 동의어 제거 — 효과: treatment-optimization optimal_combo 「PRP/엑소좀」 이 계열 통째 일치가 아니라 `/` 대안(PRP · 엑소좀)으로 분해돼 combo_ref 패키지 +1 · R12 +3, 그리고 그 이름을 그대로 쓰는 원장 계열 레코드 이름 2 곳(market-pricing categories[4].name · procedure-profiles profiles[4].name)이 사전 modality 밖 값 ⑧ 2 로 드러났다(원장 불변 · 판정은 conflict_close 또는 이름 결정).

### 개체

|  | 5차 | 6차 | 변화 | 비고 |
|---|---|---|---|---|
| adverse_effect | 66 | 71 | +5 | 세 칸 단위(V3.1-9) · 문구가 세운 조합 포함 |
| adverse_expression | 2935 | 0 | -2935 | v3.1 삭제(V3.1-10 · 문구 사전) |
| anatomical_structure | 36 | 36 | 0 |  |
| catalog_item | 521 | 521 | 0 |  |
| citation | 313 | 313 | 0 |  |
| clinical_rule | 29 | 139 | +110 | + disclosure(V3.1-7) · product_note(EXO-05) · 식별자 정규화 문장 |
| complaint | 121 | 121 | 0 |  |
| conflict | 2578 | 2818 | +240 | 아래 충돌 표 |
| decision | 324 | 457 | +133 |  |
| evidence_statement | 87 | 87 | 0 |  |
| modality | 17 | 17 | 0 |  |
| modality_subcategory | 73 | 73 | 0 |  |
| package | 229 | 230 | +1 |  |
| person_condition | 298 | 312 | +14 | 조건 단위(V3.1-4 · 사전 + raw_name) |
| problem | 14 | 14 | 0 |  |
| problem_subcategory | 53 | 53 | 0 |  |
| procedure | 645 | 645 | 0 |  |
| product | 378 | 378 | 0 | 엑소좀 2 재분류(id 재계산 · 수 그대로) |
| site | 28 | 28 | 0 |  |
| source_file | 22 | 22 | 0 |  |
| technique | 12 | 12 | 0 |  |

### 관계

|  | 5차 | 6차 | 변화 | 비고 |
|---|---|---|---|---|
| R1 | 74 | 74 | 0 |  |
| R2 | 521 | 521 | 0 |  |
| R3 | 162 | 163 | +1 |  |
| R4 | 476 | 476 | 0 |  |
| R5 | 25 | 25 | 0 |  |
| R6 | 53 | 53 | 0 |  |
| R7 | 232 | 232 | 0 |  |
| R8 | 105 | 105 | 0 |  |
| R9 | 594 | 594 | 0 |  |
| R10 | 21 | 21 | 0 |  |
| R11 | 12 | 12 | 0 |  |
| R12 | 478 | 481 | +3 | session_count(V3.1-5) · EXO-06 combo |
| R13 | 32 | 32 | 0 |  |
| R14 | 146 | 146 | 0 |  |
| R15 | 783 | 1429 | +646 | 이름(이름마다) + 문구((출발, 단위) 마다 · source_phrases) |
| R16 | 457 | 514 | +57 | 끝 = 조건 단위(원칙 B 로 문장 하나가 단위 둘이면 엣지 둘) |
| R17 | 20 | 20 | 0 |  |
| R18 | 119 | 119 | 0 |  |
| R19 | 378 | 346 | -32 | 문헌 adverse_effects 인용은 문구 사전 citations[] |
| R20 | 119 | 87 | -32 | 끝 evidence_statement 만 |
| R21 | 45 | 45 | 0 |  |
| R22 | 22 | 22 | 0 |  |
| R23 | 53 | 53 | 0 |  |
| R24 | 222 | 225 | +3 |  |
| R25 | 9178 | 6419 | -2759 |  |
| R26 | 521 | 521 | 0 |  |
| R27 | 645 | 645 | 0 |  |
| R28 | 55 | 55 | 0 |  |
| R29 | 676 | 0 | -676 | v3.1 삭제 |
| R30 | 3 | 3 | 0 |  |
| R31 | 8 | 14 | +6 | 상대 부위 끝 없음(none) |
| R32 | 0 | 112 | +112 | v3.1 신설 — 고지 ledger + edge_create |

### 게이트

|  | 5차 | 6차 | 비고 |
|---|---|---|---|
| unresolved_references | 260 | 260 |  |
| unregistered_fragments | 2112 | 2352 | ⑧ 부작용 조각은 수식어 목록(V3.1-8)으로 줄고 고지 109 문장의 새 토큰으로 는다 · 조각 행 = (축, 조각) |
| unlinked_expressions→unlinked_phrases | 2155 | 1032 | 표현 레코드(자리) → 문구 사전 unlinked 항목 · 자리 1641 |
| catalog_partial | 336 | 336 |  |

### 충돌 kind 별

|  | 5차 | 6차 | 변화 | 비고 |
|---|---|---|---|---|
| ④ value_conflict auto_resolved_by_trust | 1 | 1 | 0 |  |
| ⑥ value_conflict open | 49 | 49 | 0 |  |
| ⑦ duplicate_candidate open | 152 | 152 | 0 |  |
| ⑦ duplicate_candidate resolved | 4 | 4 | 0 |  |
| ⑧ unregistered_value open | 2112 | 2352 | +240 |  |
| ⑨ unresolved_reference open | 260 | 260 | 0 |  |

### 문구 사전(V3.1-10)

|  | 결정 전(ERD 실측) | 6차(결정 뒤) |
|---|---|---|
| 항목 | 1218 | 1235 |
| status(항목) | unlinked 1033 · auto 185 | unlinked 1032 · auto 197 · approved 6 |
| 문구 자리(고지 포함 · 번역 제외) | 2948 | 2948 |
| 자리 status | unlinked 1637 · auto 1298 · (고지) 109 | unlinked 1641 · auto 1294 · approved 13 |
| 문구가 세운 단위(조합) | 12 | 18 |
| 부록: R15 source_phrases 에 오른 항목 | — | 203 |
| 부록: 게이트 unlinked_phrases | 1033 | 1032 |

결정 뒤 auto 가 는 것은 ① 사전 결정(DICT-COURSE-01 「지속」 · 동의어·부위 추가 등)으로 조각이 사전 값이 된 문구, approved 는 옛 표현 지정(TEV · ADV-COURSE)이 문구 사전 지도로 옮겨진 항목이다. 항목 id(PHR-)는 정규화형 유도라 경과·사전 값이 바뀌면 정규화형이 갈린다(ERD §1.1 S-5 — 지금 approved 항목은 결정 locator 로 다시 찾으므로 끊기지 않는다).

### 단위(V3.1-9 · 사건, 부위, 물질)

단위 71(사전 57 + raw_name 14) — 결정 전(ERD) 61(사전 47 + raw 14). 사건 41 중 조합이 둘 이상인 사건 10 · 하나뿐 31. 문구가 세운 조합 18 · 결정이 세운 단위 2.

| 사건 | 조합 | 단위 (부위 · 물질 · 출처) |
|---|---|---|
| 당김감 | 4 | (none, none) · (눈가:anatomical, none ← 문구) · (이마:anatomical, none ← 문구) · (피부:layer, none ← 문구) |
| 괴사 | 3 | (none, none) · (피부:layer, none) · (피하 지방층:layer, none) |
| 부종 | 3 | (none, none) · (눈가:anatomical, none ← 문구) · (두피:region, none ← 문구) |
| 자극감 | 3 | (none, none) · (두피:region, none ← 문구) · (피부:layer, none ← 문구) |
| 홍반 | 3 | (none, none) · (두피:region, none ← 문구) · (피부:layer, none ← 문구) |
| 비대칭 | 2 | (none, none) · (얼굴:region, none ← 문구) |
| 색전 | 2 | (none, none) · (none, 역행성 ← 문구) |
| 섬유화 | 2 | (none, none) · (사각턱:anatomical, none ← 문구) |
| 정맥염 | 2 | (none, none) · (none, 혈전 ← 문구) |
| 통증 | 2 | (none, none) · (두피:region, none ← 문구) |
| PAH | 1 | (none, none) |
| 감각 이상 | 1 | (none, none) |
| 감염 | 1 | (none, none) |
| 건조 | 1 | (none, none) |
| 결절 | 1 | (none, none) |
| 경결 | 1 | (none, none) |
| 과민반응 | 1 | (none, none ← 문구) |
| 낙설 | 1 | (none, none) |
| 독감 유사 증상 | 1 | (none, none) |
| 동상 | 1 | (none, none) |
| 두통 | 1 | (none, none) |
| 딤플링 | 1 | (none, none ← 문구) |
| 멍 | 1 | (none, none) |
| 바이오필름 | 1 | (none, none) |
| 반흔 | 1 | (none, none) |
| 색소침착 | 1 | (none, none) |
| 소양감 | 1 | (none, none) |
| 수포 | 1 | (none, none ← 문구) |
| 실 노출 | 1 | (none, none) |
| 실 이동 | 1 | (none, none) |
| 실신 | 1 | (none, none) |
| 아나필락시스 | 1 | (none, none ← 문구) |
| 열감 | 1 | (none, none) |
| 육아종 | 1 | (none, none) |
| 이물반응 | 1 | (none, none) |
| 작열감 | 1 | (none, none) |
| 항체 내성 | 1 | (none, none) |
| 혈관 폐색 | 1 | (none, none) |
| 혈관외유출 | 1 | (none, none) |
| 혈종 | 1 | (none, none) |
| 화상 | 1 | (none, none) |

### R15 may_cause(경과 = 엣지 속성 · 원칙 C)

|  | 결정 전(ERD · (출발, 단위) distinct) | 6차 |
|---|---|---|
| 엣지 | 1342 | 레코드 1429 · (출발, 단위) distinct 1372 |
| 이름 유래 / 문구 유래 | 79 / 1306 | 82 / 1321 (+ pih-risk 26) |
| 경과 있는 엣지 | 247 | 262 |
| 경과 값별 | 지연 12 · 재발 2 · 일시 234 · 영구 1 | 일시 237 · 지속 12 · 재발 2 · 지연 12 · 영구 1 |
| 고지 유래(disclosure) | 0 | 0 |

이름 유래 엣지는 이름마다 하나(severity·incidence 같은 속성이 이름의 것)라 레코드 수가 (출발, 단위) distinct 보다 많다. 경과는 그 단위 후보의 경과만 — 검산 V3.1-9 가 문구 엣지마다 확인한다(S-1).

### 조건 단위(V3.1-4)

이름 자리 471 · distinct 298(kind 포함 299) → 단위 **312**(사전 96 + raw_name 216) · kind condition 172 · check 136 · age_group 4 · 문장 부록 529(원칙 B 로 문장 하나가 단위 둘이면 둘에 붙는다) · R16 514 · R17 20. 5차의 person_condition 298(문자열 식별)은 v3.1 에서 쓰지 않는다 — 결정 B3-R16-01·02 의 끝(locator)은 그 문장의 조건 단위로 닿았다.

### 결정 묶음 4 제안(동의어 · proposed — 빌드가 읽지 않음)

`decisions/batch4-proposed/` 130 · 게이트 `out/gate/batch4.json`(2B 스키마) 고를 자리 187 · 추천 있음 13 · 추천 없음 174. ① 부작용 문구 조각 80 · ② 부위·물질 조각 47 · ③ 시술 조각 60. 승인하면 닫히는 문구 자리 합 90 · 참조 합 0(추천대로 고를 때 · 항목 effect).
