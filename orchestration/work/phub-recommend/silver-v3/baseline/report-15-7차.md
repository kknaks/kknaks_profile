## 15. 7차 빌드 · ERD v3.2

6차 = `baseline/manifest-6차.json`(ERD v3.1 · 결정 457) · 7차 = ERD **v3.2**(`erd-v3.2.json` · `erd-v3.2-dictionaries.json` 의 파생 항목(원장 사건 노드 · 장비 제품)은 빼고 분해가 다시 세운다 · 빌더 `lib/v32.py` · 발주서 `silver-build-7-brief.md`). ③ 결정 적용 전 분해 = `erd-v3.2-tuples.json` 요약 차이 0/171(§5 · 행 대조는 check ③). 결정은 6차와 같은 저장소(새 결정 0) — 옛 결정을 v3.2 구조로 옮겨 적용했다.

### 결정 적용(7차)

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

거부·대상 없음: **0** — 기존 결정(_bootstrap · batch1 · 2a · 2b · 3) 전부 v3.2 빌더가 받았다.

v3.2 새 구조로 옮겨 적용한 옛 결정(거부 아님 · 사유는 적용 로그 note):

- 옛 이름 단위(raw_name) 대상 adverse_tuple_assign **10** — v3.2 에는 이름 단위가 없다(V3.2-0 노드 원칙). 같은 locator 의 이름 단위(원장 사건 노드 · 사전 사건)를 지정 단위로 대체:

| 결정 | 이름 locator | v3.2 분해 단위(대체 전) | 지정 단위 |
|---|---|---|---|
| B2B-ISE-01 | M1/2 | 홍반, 부종 | (홍반, none, none), (부종, none, none) |
| B2B-PAR-01 | M9/4 | 감각 이상 | (감각 이상, none, none) |
| B2B-PAR-02 | M14/2 | 감각 이상 | (감각 이상, none, none) |
| B2B-PAR-03 | M14/3 | 홍반, 부종 | (홍반, none, none), (부종, none, none) |
| B2B-PAR-04 | M16/4 | 경결, 섬유화 | (경결, none, none) |
| B3-ADV-01 | M9/4 | 감각 이상 | (감각 이상, none, none) |
| B3-ADV-02 | M14/2 | 감각 이상 | (감각 이상, none, none) |
| B3-ADV-03 | M14/3 | 홍반, 부종 | (홍반, none, none), (부종, none, none) |
| B3-ADV-04 | M14/1 | 괴사, 동상 | (괴사, 피부, none), (괴사, 피하 지방층, none), (동상, none, none) |
| B3-ADV-05 | M16/4 | 경결 | (경결, none, none), (섬유화, none, none) |

- 옛 표현 지정(kind=expression · 부작용 문구 자리) **10** — 그 자리의 부작용 문구 사전 항목 지도(phrase_map 과 같은 효과 · status approved): `B2B-TEV-01`→PHR-0d10bd307d, `B2B-TEV-02`→PHR-4db30daf7b, `B2B-TEV-03`→PHR-4db30daf7b, `B2B-TEV-04`→PHR-0d10bd307d, `B2B-TEV-05`→PHR-559472746f, `B2B-TEV-06`→PHR-4db30daf7b, `B2B-TEV-07`→PHR-4db30daf7b, `B2B-TEV-08`→PHR-0d10bd307d, `B2B-TEV-09`→PHR-559472746f, `B2B-TEV-10`→PHR-0d10bd307d
- 옛 표현 지정(타임라인 줄) **3** — v3.2 타임라인 줄은 문구 사전이 아니라 자기 테이블(post_procedure_timeline · V3.2-9) — 그 줄의 참조(adverse_ref · R34)를 지정 단위로 · 경과는 계열 R15 경과: `B3-ADV-COURSE-01`(M16/6 → 줄 5/3/0 · 경과 지속), `B3-ADV-COURSE-02`(M16/9 → 줄 5/4/1 · 경과 지속), `B3-ADV-COURSE-03`(M16/9 → 줄 5/2/1 · 경과 지속)

### 개체

|  | 6차 | 7차 | 변화 | 비고 |
|---|---|---|---|---|
| adverse_effect | 71 | 338 | +267 | 원장 사건 노드 단위(V3.2-0) · 이름 단위(raw_name) 없음 |
| anatomical_structure | 36 | 36 | 0 |  |
| catalog_item | 521 | 521 | 0 |  |
| citation | 313 | 313 | 0 |  |
| clinical_rule | 139 | 139 | 0 |  |
| complaint | 121 | 121 | 0 |  |
| conflict | 2818 | 1290 | -1528 | 아래 충돌 표 |
| decision | 457 | 457 | 0 |  |
| evidence_statement | 87 | 119 | +32 | + 문헌 adverse_effects 32(kind=adverse_effects · V3.2-0) |
| modality | 17 | 17 | 0 |  |
| modality_subcategory | 73 | 73 | 0 |  |
| package | 230 | 230 | 0 |  |
| person_condition | 312 | 310 | -2 | 토큰화(V3.2-1)로 raw_name 일부가 사전 단위로 |
| problem | 14 | 14 | 0 |  |
| problem_subcategory | 53 | 53 | 0 |  |
| procedure | 645 | 646 | +1 | 토큰화·성분 what·장비 승격 |
| product | 378 | 421 | +43 | 장비 제품 자동 등록 78(origin=taxonomy · V3.2-5) — 그중 step1 제품과 이름이 닿아 합친 것 포함 |
| site | 28 | 28 | 0 |  |
| source_file | 22 | 22 | 0 |  |
| technique | 12 | 12 | 0 |  |
| post_procedure_timeline | 0 | 10 | +10 | v3.2 신설(V3.2-9) |
| emergency_sign | 0 | 52 | +52 | v3.2 신설(V3.2-0) |

### 관계

|  | 6차 | 7차 | 변화 | 비고 |
|---|---|---|---|---|
| R1 | 74 | 74 | 0 |  |
| R2 | 521 | 521 | 0 |  |
| R3 | 163 | 241 | +78 | 장비 승격(항목 이름 = 제품) |
| R4 | 476 | 554 | +78 | + 장비 제품(계열 → 제품) |
| R5 | 25 | 25 | 0 |  |
| R6 | 53 | 53 | 0 |  |
| R7 | 232 | 232 | 0 |  |
| R8 | 105 | 105 | 0 |  |
| R9 | 594 | 594 | 0 |  |
| R10 | 21 | 21 | 0 |  |
| R11 | 12 | 12 | 0 |  |
| R12 | 481 | 482 | +1 |  |
| R13 | 32 | 32 | 0 |  |
| R14 | 146 | 146 | 0 |  |
| R15 | 1429 | 2511 | +1082 | (출발, 단위) 마다 하나 · 이름+문구+타임라인+응급 참조 · inheritance · layer |
| R16 | 514 | 514 | 0 |  |
| R17 | 20 | 20 | 0 |  |
| R18 | 119 | 119 | 0 |  |
| R19 | 346 | 378 | +32 | + 문헌 adverse_effects 인용 |
| R20 | 87 | 119 | +32 | + 계열 → adverse_effects 근거 |
| R21 | 45 | 45 | 0 |  |
| R22 | 22 | 22 | 0 |  |
| R23 | 53 | 53 | 0 |  |
| R24 | 225 | 225 | 0 |  |
| R25 | 6419 | 4602 | -1817 |  |
| R26 | 521 | 521 | 0 |  |
| R27 | 645 | 643 | -2 | 성분 what 튜플은 R27 끝 없음(해석 보류) |
| R28 | 55 | 55 | 0 |  |
| R30 | 3 | 3 | 0 |  |
| R31 | 14 | 51 | +37 | 단위가 는 만큼 |
| R32 | 112 | 112 | 0 |  |
| R33 | 0 | 10 | +10 | v3.2 신설 |
| R34 | 0 | 366 | +366 | v3.2 신설(줄 → 단위 참조) |
| R35 | 0 | 70 | +70 | v3.2 신설 |

### 충돌 kind 별

|  | 6차 | 7차 | 변화 | 비고 |
|---|---|---|---|---|
| ④ value_conflict auto_resolved_by_trust | 1 | 1 | 0 |  |
| ⑥ value_conflict open | 49 | 49 | 0 |  |
| ⑦ duplicate_candidate open | 152 | 471 | +319 |  |
| ⑦ duplicate_candidate resolved | 4 | 4 | 0 |  |
| ⑧ unregistered_value open | 2352 | 506 | -1846 |  |
| ⑨ unresolved_reference open | 260 | 259 | -1 |  |

### 게이트

|  | 6차 | 7차 | 비고 |
|---|---|---|---|
| unresolved_references | 260 | 259 |  |
| unregistered_fragments | 2352 | 506 | 부작용 문구 미등록 조각은 핵심어 노드 · side · 설명으로(⑧ 은 시술·조건 축 위주) |
| unlinked_phrases | 1032 | 0 | v3.2 부작용 축에 미연결 상태 없음(새 노드 · 메모 · 설명문) |
| unlinked_phrase_locators | 1641 | 0 |  |
| catalog_partial | 336 | 259 |  |
| conflicts_md_duplicate | 156 | 475 | + ⑦ 원장 사건 노드 쌍(strong · weak) · 장비 제품 ↔ 기존 제품 |

### 부작용 문구 분포(V3.2-0 · V3.2-7)

|  | 결정 전(ERD 실측) | 7차(결정 뒤) |
|---|---|---|
| 부작용 문구 자리 | 2285 | 2285 |
| 자리 status | new 835 · exact 1407 · sentence 13 · note 30 | new 835 · exact 1399 · approved 10 · sentence 11 · note 30 |
| 문구 사전 항목(부작용) · 메모 항목 | 530 · 28 | 536 · 27 |
| 항목 status | new 341 · exact 189 + 메모 sentence 7 · note 21 | new 342 · exact 191 · approved 3 · sentence 6 · note 21 |
| 어느 단위에도 안 붙은 부작용 문구(unlinked) | 0 | 0 |
| complications 이름 65 | exact 62 · new 3 | exact 62 · new 3 |

exact = 사전 사건에 닿음 · new = 핵심어 새 노드에 닿음 · note = 메모(사건 0 + 메모 어휘) · sentence = 설명문(문턱) · approved = 옛 표현 지정이 문구 사전 지도로. 미연결 상태는 없다(ERD §0.2).

### 원장 사건 노드 · ⑦ duplicate_candidate

|  | 결정 전(ERD 실측) | 7차(결정 뒤) |
|---|---|---|
| 원장 사건 노드(origin=ledger · unreviewed) | 262 | 260 |
| 부작용 단위 · event_kind | 328 | 338 · dict 66 · ledger 272 |
| ⑦ 노드 쌍 strong / weak | 98 / 207 | 96 / 207 (충돌 레코드 strong·open 96 · weak·open 207) |
| ⑦ 장비 제품 ↔ 기존 제품(접두) | 13(씨앗 ⑦) | 18 |

결정 전 → 7차 노드 차이: 빠짐 두피 민감성, 두피 온감 · 새로 없음 — 이미 approved 인 ① 사전 결정(부위·동의어 추가)이 그 토막의 조각을 사전 값으로 만들어 핵심어가 남지 않았다.

### 타임라인 줄 · 응급 징후 · 고지 · 문헌(자기 테이블 · 참조만)

|  | 결정 전(ERD 실측) | 7차(결정 뒤) |
|---|---|---|
| 타임라인 · 단계 · 줄 | 10 · 43 · 435 | 10 · 43 · 435 |
| 줄 상태 | ref_partial 109 · normal_memo 78 · ref 192 · none 56 | ref_partial 107 · normal_memo 78 · ref 194 · none 56 |
| R34 timeline_refers | 368 | 366 |
| 응급 징후(SGN) · 상태 | 52 · ref 26 · none 7 · ref_partial 19 | 52 · ref 27 · none 7 · ref_partial 18 |
| R35 sign_refers | 69 | 70 |
| 필수 고지 자리 · 상태 | 109 · none 58 · ref 10 · ref_partial 41 | 109 · none 58 · ref 10 · ref_partial 41 |
| 문헌 adverse_effects · 상태 | 32 · none 20 · ref_partial 12 | 32 · none 20 · ref_partial 12 |

| 반응 등급 | ref | ref_partial | none | normal_memo |
|---|---|---|---|---|
| normal | 52 | 32 | 0 | 78 |
| abnormal | 43 | 19 | 24 | 0 |
| caution | 45 | 26 | 22 | 0 |
| emergency | 54 | 30 | 10 | 0 |

- R33 has_timeline 10: 끝 procedure 6 · modality 4 — 타임라인 이름이 튜플로 풀리면 그 튜플, 아니면 category 계열(V3.2-9).
- 결정이 바꾼 줄: 5/2/1(DEC-2026-11-05-B3-ADV-COURSE-03), 5/3/0(DEC-2026-11-05-B3-ADV-COURSE-01), 5/4/1(DEC-2026-11-05-B3-ADV-COURSE-02) · 참조 끝이 사라져 뺀 참조: 0

### 항목 자신 · 제품 승격 · 성분 what(V3.2-5 · V3.2-6)

|  | 6차 | 결정 전(ERD v3.2 실측) | 7차 |
|---|---|---|---|
| 분류 항목 → what_kind(항목 521) | — | catalog_item 324 · product 187 · modality_subcategory 7 · ingredient 3 | product 245 · catalog_item 266 · modality_subcategory 7 · ingredient 3 |
| 항목 자신이 시술(분류 항목 원천 튜플 what=catalog_item) | 342 | 324 | 263 |
| 튜플 what_kind(전체) | catalog_item 348 · product 190 · modality_subcategory 46 · modality 61 | catalog_item 326 · product 216 · modality_subcategory 14 · ingredient 3 · modality 41 | catalog_item 267 · product 269 · modality_subcategory 46 · ingredient 3 · modality 61 |
| 장비 제품 자동 등록(origin=taxonomy) | 0 | 151 | 78 |

- 장비 자동 등록: 장비 항목 176 · 결정 전 등록 151 → 7차 78 — 결정 전에 등록되던 것 중 7차에 등록하지 않은 73(사유 already 73): approved 결정(dictionary_add · 묶음 1 등)이 이미 그 이름을 사전 값(product_name:BBL, product_name:BBL 히어로, product_name:노블린, product_name:더마샤인, product_name:더블로골드S, product_name:듀오타이트, product_name:디스커버리 피코, product_name:라라젯, product_name:라이트쉬어 듀엣, product_name:리니어펌, product_name:리팟, product_name:리프테라 …)으로 두어 「이미 사전 값」이다 — 그 항목도 product 로 승격되는 것은 같다.
- 성분 what(분류 항목): PDO[M7], PCL[M7], PLLA[M7] · R27 끝 없는 성분 what 튜플 3(성분은 사전 값 · 개체 아님 — 해석 보류)

### ⑨ 미해결 참조

6차 260 → 7차 **259** — 풀림 1 · 새로 0. 사유별(7차) unregistered 204 · 고민 사전 일치 없음(질문 12) 29 · multi_primary 18 · canonical_category 가 하위분류 사전에 없다(질문 23) 6 · combo_outside_fragment 2

풀린 참조: 「서브시전(subcision)」@—

### R15 may_cause · 속성 상속(V3.2-8 · 참조만)

R15 2511(결정 전 ERD (출발, 단위) 2476) · layer family 301 · item 2184 · 타임라인 참조가 있는 엣지 155 · 응급 참조 73 · 경과 있는 엣지 438 · basis 없는 상속 0 · 값 복사 0.

항목·제품 출발(layer=item) — 속성마다 basis:

| 속성 | item | family | unit | none |
|---|---|---|---|---|
| severity | 0 | 966 | 0 | 1218 |
| incidence | 0 | 966 | 0 | 1218 |
| onset | 0 | 966 | 0 | 1218 |
| duration | 0 | 135 | 0 | 2049 |
| mechanism | 0 | 966 | 0 | 1218 |
| management | 0 | 966 | 416 | 802 |
| prevention | 0 | 966 | 0 | 1218 |
| risk_factors | 0 | 966 | 0 | 1218 |

계열 출발(layer=family) — 속성마다 basis:

| 속성 | family | unit | none |
|---|---|---|---|
| severity | 91 | 0 | 210 |
| incidence | 91 | 0 | 210 |
| onset | 91 | 0 | 210 |
| duration | 23 | 0 | 278 |
| mechanism | 91 | 0 | 210 |
| management | 91 | 87 | 123 |
| prevention | 91 | 0 | 210 |
| risk_factors | 91 | 0 | 210 |

### 결정 묶음 5 게이트(노드 단위 · `out/gate/batch5.json`·`.md`)

| 묶음 | 자리 | 추천 |
|---|---|---|
| ledger-nodes | 260 | 0 |
| dup-strong | 96 | 1 |
| seed-site | 15 | 0 |
| seed-ingredient_material | 17 | 0 |
| seed-product_abbrev | 29 | 0 |
| m5-rename | 1 | 0 |
| m16-technique | 6 | 4 |
| site-synonyms | 6 | 1 |
| air-embolism-qualifier | 1 | 0 |
| records | 1 | 0 |

고를 자리 432 · 옵션 3060 · 추천 6 · 원문 935(읽기 실패 0) · ⑦ weak 207 은 `batch5-weak.json`(게이트에 올리지 않음). 고른 답 → `python3 apply_gate.py --gate out/gate/batch5.json --answers answers.json`(→ decisions/batch5/).
